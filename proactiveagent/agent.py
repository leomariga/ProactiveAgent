"""Main Proactive AI Agent class"""

import asyncio
import threading
import time
import logging
from typing import List, Dict, Any, Optional, Callable, Union
from .providers.base import BaseProvider
from .scheduler import WakeUpScheduler
from .decision_engines import DecisionEngine, AIBasedDecisionEngine

from .utils import (
    setup_logging, 
    create_message_dict, 
    extract_recent_messages,
    calculate_user_engagement,
    sanitize_context,
    validate_callback
)


class ProactiveAgent:
    """Main class for creating proactive AI agents"""
    
    def __init__(
        self,
        provider: BaseProvider,
        callbacks: Optional[List[Callable]] = None,
        decision_config: Optional[Dict[str, Any]] = None,
        decision_engine: Optional[DecisionEngine] = None,
        system_prompt: Optional[str] = None,
        log_level: str = "WARNING"
    ):
        """
        Initialize Proactive AI Agent
        
        Args:
            provider: AI provider instance (e.g., OpenAIProvider)
            callbacks: List of callback functions for responses
            decision_config: Configuration for decision engine (includes wake_up_pattern and max_sleep_time)
            decision_engine: Custom decision engine instance (defaults to AIBasedDecisionEngine)
            system_prompt: Optional system prompt for the AI
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.provider = provider
        self.system_prompt = system_prompt or self._default_system_prompt()
        
        # Use provided config merged with defaults for decision engine
        default_decision_config = {
            'min_response_interval': 15,
            'max_response_interval': 3600,
            'engagement_threshold': 0.5,
            'context_relevance_weight': 0.4,
            'time_weight': 0.3,
            'probability_weight': 0.3,
            'wake_up_pattern': "Check every 2-3 minutes if conversation is active",
            'min_sleep_time': 10,  # 10 seconds minimum
            'max_sleep_time': 120,  # 2 minutes in seconds
            'engagement_high_threshold': 10,
            'engagement_medium_threshold': 3,
        }
        
        # Merge provided config with defaults, ensuring all keys exist
        self.decision_config = {**default_decision_config, **(decision_config or {})}

        self.decision_engine = decision_engine or AIBasedDecisionEngine(provider)
        
        # Conversation state
        self.messages: List[Dict[str, Any]] = []
        self.last_user_message_time: Optional[float] = None
        self.is_running = False
        self.conversation_context: Dict[str, Any] = {}
        
        # Threading
        self.thread: Optional[threading.Thread] = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        
        # Callbacks
        self.callbacks: List[Callable] = []
        self.sleep_time_callbacks: List[Callable] = []
        self.decision_callbacks: List[Callable] = []
        if callbacks:
            for callback in callbacks:
                self.add_callback(callback)
        
        # Initialize scheduler (after callbacks are initialized)
        self.scheduler = WakeUpScheduler(
            provider, 
            self.decision_config, 
            lambda: self.sleep_time_callbacks
        )
        
        # Logging
        self.logger = setup_logging(log_level)
        self.logger.info("Active AI Agent initialized")
    
    def _default_system_prompt(self) -> str:
        """Default system prompt for active agents"""
        return """You are an active AI assistant that proactively engages in conversations. 
        You should be helpful, contextual, and engaging while being mindful not to be intrusive. 
        Consider the time that has passed since the last message and the conversation context 
        when deciding how to respond."""
    
    def add_callback(self, callback: Callable) -> None:
        """
        Add a callback function for receiving AI responses
        
        Args:
            callback: Function that takes (response: str) as parameter
        """
        if validate_callback(callback):
            self.callbacks.append(callback)
            self.logger.debug(f"Added callback: {callback.__name__}")
        else:
            raise ValueError("Invalid callback function signature")
    
    def remove_callback(self, callback: Callable) -> None:
        """Remove a callback function"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
            self.logger.debug(f"Removed callback: {callback.__name__}")
    
    def add_sleep_time_callback(self, callback: Callable) -> None:
        """
        Add a callback function for sleep time estimation events
        
        Args:
            callback: Function that takes (sleep_time: int, reasoning: str) as parameters
        """
        if callable(callback):
            self.sleep_time_callbacks.append(callback)
            self.logger.debug(f"Added sleep time callback: {callback.__name__}")
        else:
            raise ValueError("Invalid sleep time callback function")
    
    def remove_sleep_time_callback(self, callback: Callable) -> None:
        """Remove a sleep time callback function"""
        if callback in self.sleep_time_callbacks:
            self.sleep_time_callbacks.remove(callback)
            self.logger.debug(f"Removed sleep time callback: {callback.__name__}")
    
    def add_decision_callback(self, callback: Callable) -> None:
        """
        Add a callback function for decision engine events
        
        Args:
            callback: Function that takes (should_respond: bool, reasoning: str) as parameters
        """
        if callable(callback):
            self.decision_callbacks.append(callback)
            self.logger.debug(f"Added decision callback: {callback.__name__}")
        else:
            raise ValueError("Invalid decision callback function")
    
    def remove_decision_callback(self, callback: Callable) -> None:
        """Remove a decision callback function"""
        if callback in self.decision_callbacks:
            self.decision_callbacks.remove(callback)
            self.logger.debug(f"Removed decision callback: {callback.__name__}")
    
    def send_message(self, message: str, role: str = "user") -> None:
        """
        Send a message to the conversation
        
        Args:
            message: Message content
            role: Message role ('user' or 'assistant')
        """
        msg_dict = create_message_dict(role, message)
        self.messages.append(msg_dict)
        
        if role == "user":
            self.last_user_message_time = time.time()
            self._update_conversation_context()
            
            # Interrupt current sleep to immediately recalculate sleep time
            if hasattr(self, 'scheduler') and self.scheduler:
                self.scheduler.interrupt_sleep()
                self.logger.debug(f"[AGENT] User message received, triggering sleep recalculation")
            
            # Trigger immediate response evaluation for user messages
            if self.is_running and hasattr(self, 'loop') and self.loop:
                self.logger.debug(f"[AGENT] Triggering immediate response evaluation for user message")
                # Schedule immediate evaluation in the agent's event loop
                asyncio.run_coroutine_threadsafe(
                    self._evaluate_and_respond(self._get_current_context(), triggered_by_user_message=True),
                    self.loop
                )
        
        self.logger.debug(f"Message added: {role}: {message[:50]}...")
    
    def start(self) -> None:
        """Start the active agent in a separate thread"""
        if self.is_running:
            self.logger.warning("Agent is already running")
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._run_agent, daemon=True)
        self.thread.start()
        self.logger.info("Active AI Agent started")
    
    def stop(self) -> None:
        """Stop the active agent"""
        if not self.is_running:
            return
        
        self.is_running = False
        self.scheduler.stop()
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        
        self.logger.info("Active AI Agent stopped")
    
    def _run_agent(self) -> None:
        """Main agent loop running in separate thread"""
        # Create new event loop for this thread
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        try:
            # Start the scheduler
            self.loop.run_until_complete(
                self.scheduler.start(
                    wake_up_callback=self._on_wake_up,
                    context_provider=self._get_current_context
                )
            )
        except Exception as e:
            self.logger.error(f"Error in agent loop: {str(e)}")
        finally:
            self.loop.close()
    
    def _on_wake_up(self, context: Dict[str, Any]) -> None:
        """Called when the scheduler wakes up the agent"""
        if not self.is_running:
            return
        
        self.logger.info(f"[AGENT] Agent woke up, evaluating response decision")
        
        # Run decision making in the event loop
        asyncio.create_task(self._evaluate_and_respond(context))
    
    async def _evaluate_and_respond(self, context: Dict[str, Any], triggered_by_user_message: bool = False) -> None:
        """Evaluate whether to respond and generate response if needed"""
        try:
            if not self.last_user_message_time:
                self.logger.debug("[AGENT] No user messages yet, skipping response evaluation")
                return
            
            elapsed_time = int(time.time() - self.last_user_message_time)
            
            # Get recent messages for decision making
            recent_messages = extract_recent_messages(self.messages, 10)
            
            # Decide whether to respond
            should_respond, reason = await self.decision_engine.should_respond(
                recent_messages,
                self.last_user_message_time,
                context,
                self.decision_config,
                triggered_by_user_message
            )
            
            # Call all decision callbacks
            for i, callback in enumerate(self.decision_callbacks):
                try:
                    callback(should_respond, reason)
                except Exception as e:
                    self.logger.error(f"[AGENT] Decision callback {i+1} error: {str(e)}")
            
            if should_respond:
                self.logger.info(f"[AGENT] Generating response (reason: {reason})")
                await self._generate_and_send_response(recent_messages, context, triggered_by_user_message)
            else:
                self.logger.info(f"[AGENT] No response needed ({reason})")
            
        except Exception as e:
            self.logger.error(f"[AGENT] Error in response evaluation: {str(e)}")
    
    async def _generate_and_send_response(
        self, 
        messages: List[Dict[str, str]], 
        context: Dict[str, Any],
        triggered_by_user_message: bool = False
    ) -> None:
        """Generate and send AI response"""
        try:
            # Add context information to system prompt
            enhanced_prompt = self._create_context_aware_prompt(context)
            
            # Generate response
            response = await self.provider.generate_response(
                messages,
                system_prompt=enhanced_prompt,
                triggered_by_user_message=triggered_by_user_message
            )
            
            if response:
                self.logger.info(f"[AGENT] Response generated: {response[:80]}...")
                
                # Add to conversation history
                self.send_message(response, "assistant")
                
                # Call all callbacks
                for i, callback in enumerate(self.callbacks):
                    try:
                        callback(response)
                    except Exception as e:
                        self.logger.error(f"[AGENT] Callback {i+1} error: {str(e)}")
            else:
                self.logger.warning(f"[AGENT] Provider returned empty response")
            
        except Exception as e:
            self.logger.error(f"[AGENT] Error generating response: {str(e)}")
    
    def _create_context_aware_prompt(self, context: Dict[str, Any]) -> str:
        """Create system prompt with current context"""
        base_prompt = self.system_prompt
        
        elapsed_time = int(time.time() - (self.last_user_message_time or time.time()))
        
        context_info = f"""
        
        Current context:
        - Time since last user message: {elapsed_time} seconds
        - User engagement level: {context.get('user_engagement', 'unknown')}
        - Conversation length: {len(self.messages)} messages
        """
        
        return base_prompt + context_info
    
    def _get_current_context(self) -> Dict[str, Any]:
        """Get current conversation context"""
        context = self.conversation_context.copy()
        
        # Get engagement thresholds from decision config
        high_threshold = self.decision_config.get('engagement_high_threshold', 10)
        medium_threshold = self.decision_config.get('engagement_medium_threshold', 3)
        
        # Add dynamic context
        context.update({
            'conversation_length': len(self.messages),
            'user_engagement': calculate_user_engagement(
                self.messages,
                high_threshold=high_threshold,
                medium_threshold=medium_threshold
            ),
            'last_activity': self.last_user_message_time,
            'current_time': time.time()
        })
        
        return sanitize_context(context)
    
    def _update_conversation_context(self) -> None:
        """Update conversation context based on recent activity"""
        # Simple context updates - can be enhanced
        recent_messages = self.messages[-5:] if len(self.messages) >= 5 else self.messages
        
        # Check for questions
        has_questions = any("?" in msg.get('content', '') for msg in recent_messages)
        self.conversation_context['requires_followup'] = has_questions
        
        # Update urgency based on keywords
        recent_content = " ".join(msg.get('content', '') for msg in recent_messages).lower()
        if any(word in recent_content for word in ['urgent', 'asap', 'immediately', 'help']):
            self.conversation_context['urgency'] = 'high'
        elif any(word in recent_content for word in ['when possible', 'no rush', 'later']):
            self.conversation_context['urgency'] = 'low'
        else:
            self.conversation_context['urgency'] = 'normal'
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the full conversation history"""
        return self.messages.copy()
    
    def clear_conversation_history(self) -> None:
        """Clear the conversation history"""
        self.messages.clear()
        self.last_user_message_time = None
        self.conversation_context.clear()
        self.logger.info("Conversation history cleared")
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """
        Update agent configuration
        
        Args:
            new_config: Dictionary containing configuration updates
        """
        # Update decision config
        self.decision_config.update(new_config)
        
        # Update scheduler configuration
        self.scheduler.update_config(new_config)
        
        self.logger.info(f"Agent configuration updated with: {list(new_config.keys())}")
    
    def set_context(self, key: str, value: Any) -> None:
        """Set a context value"""
        self.conversation_context[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get a context value"""
        return self.conversation_context.get(key, default)
    
    def is_active(self) -> bool:
        """Check if the agent is currently running"""
        return self.is_running
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()