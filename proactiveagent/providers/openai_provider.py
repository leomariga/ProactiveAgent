"""OpenAI provider implementation"""

import asyncio
import json
import random
from typing import List, Dict, Any, Optional
from openai import OpenAI
from pydantic import BaseModel
from .base import BaseProvider


class SleepTimeResponse(BaseModel):
    """Structured response for sleep time calculation"""
    sleep_seconds: int
    reasoning: str


class ResponseDecision(BaseModel):
    """Structured response for should_respond decision"""
    should_respond: bool
    reasoning: str


class OpenAIProvider(BaseProvider):
    """OpenAI provider for Active AI agents"""
    
    def __init__(self, model: str = "gpt-3.5-turbo", **kwargs: Any):
        """
        Initialize OpenAI provider
        
        Args:
            model: OpenAI model name
            **kwargs: Additional OpenAI parameters (including api_key)
        """
        super().__init__(model, **kwargs)
        
        # Pass all kwargs to OpenAI client (it will handle validation)
        self.client = OpenAI(**kwargs)
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None,
        triggered_by_user_message: bool = False,
        **kwargs: Any
    ) -> str:
        """Generate response using OpenAI API"""
        def _sync_generate():
            try:
                # Prepare messages for OpenAI format
                openai_messages = []
                
                if system_prompt:
                    openai_messages.append({"role": "system", "content": system_prompt})
                
                openai_messages.extend(messages)
                
                # Add last message as user role if triggered by user message
                if triggered_by_user_message and messages:
                    last_message = messages[-1]
                    if last_message.get("role") != "user":
                        openai_messages.append({"role": "user", "content": last_message.get("content", "")})
                elif not triggered_by_user_message:
                    # Add empty string as user message when not triggered by user
                    openai_messages.append({"role": "user", "content": ""})
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=openai_messages,
                    **kwargs
                )
                
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                raise Exception(f"OpenAI API error: {str(e)}")
        
        # Run synchronous call in executor
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _sync_generate)
    
    async def should_respond(
        self,
        messages: List[Dict[str, str]],
        elapsed_time: int,
        context: Dict[str, Any],
        **kwargs: Any
    ) -> bool:
        """
        Determine if AI should respond using OpenAI decision-making with structured output
        """
        def _sync_decide():
            try:
                # Create decision prompt
                decision_prompt = f"""
                You are an AI assistant deciding whether to proactively send a message.
                
                Conversation context:
                - Time since last user message: {elapsed_time} seconds
                - Recent messages: {json.dumps(messages[-3:], indent=2)}
                - Context: {json.dumps(context, indent=2)}
                
                Factors to consider:
                1. Has enough time passed to warrant a response?
                2. Is the conversation in a natural state for proactive engagement?
                3. Would a response add value or seem intrusive?
                4. Does the user's last message require or expect a follow-up?
                5. Is there unfinished business or unanswered questions?
                6. What might indicate the elapsed time in the context of user's chat?
                
                Provide your decision (true/false) and reasoning.
                """
                
                import logging
                logger = logging.getLogger(__name__)
                
                response = self.client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[{"role": "user", "content": decision_prompt}],
                    response_format=ResponseDecision,
                    **kwargs
                )
                
                decision_response = response.choices[0].message.parsed
                
                if decision_response:
                    logger.info(f"[AI_DECISION] Decision: {decision_response.should_respond}")
                    logger.debug(f"[AI_DECISION] Reasoning: {decision_response.reasoning}")
                    
                    return decision_response.should_respond
                else:
                    logger.warning("[AI_DECISION] No parsed response, using fallback")
                    # Fallback to simple probability-based decision
                    probability_threshold = context.get('response_probability', 0.3)
                    fallback_decision = random.random() < probability_threshold
                    logger.info(f"[AI_DECISION] Fallback decision: {fallback_decision}")
                    return fallback_decision
                
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                # Fallback to simple probability-based decision
                probability_threshold = context.get('response_probability', 0.3)
                fallback_decision = random.random() < probability_threshold
                logger.info(f"[AI_DECISION] Fallback decision: {fallback_decision} (OpenAI failed: {str(e)})")
                return fallback_decision
        
        # Run synchronous call in executor
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _sync_decide)
    
    async def calculate_sleep_time(
        self,
        wake_up_pattern: str,
        min_sleep_time: int,
        max_sleep_time: int,
        context: Dict[str, Any],
        **kwargs: Any
    ) -> tuple[int, str]:
        """
        Calculate sleep time using OpenAI pattern interpretation with structured output
        """
        def _sync_calculate():
            try:
                # Create sleep calculation prompt
                sleep_prompt = f"""
                You are helping calculate sleep time for an AI agent.
                
                Wake-up pattern: "{wake_up_pattern}"
                Minimum allowed sleep time: {min_sleep_time} seconds
                Maximum allowed sleep time: {max_sleep_time} seconds
                Current context: {json.dumps(context, indent=2)}
                
                Based on the pattern and context, determine appropriate sleep time in seconds.
                Consider:
                - User engagement level
                - Time of day (if available)
                - Conversation urgency
                - Pattern instructions
                
                Provide a sleep time between {min_sleep_time} and {max_sleep_time} seconds, along with your reasoning.
                """
                
                import logging
                logger = logging.getLogger(__name__)
                
                response = self.client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[{"role": "user", "content": sleep_prompt}],
                    response_format=SleepTimeResponse,
                    **kwargs
                )
                
                sleep_response = response.choices[0].message.parsed
                
                if sleep_response:
                    # Ensure sleep time is within bounds
                    final_sleep_time = max(min_sleep_time, min(sleep_response.sleep_seconds, max_sleep_time))
                    
                    logger.info(f"[AI_SLEEP] AI suggested: {sleep_response.sleep_seconds}s → final: {final_sleep_time}s")
                    logger.debug(f"[AI_SLEEP] Reasoning: {sleep_response.reasoning}")
                    
                    return final_sleep_time, sleep_response.reasoning
                else:
                    logger.warning("[AI_SLEEP] No parsed response, using fallback")
                    fallback_time = self._fallback_sleep_calculation(wake_up_pattern, min_sleep_time, max_sleep_time)
                    return fallback_time, "Fallback calculation (AI parsing failed)"
                    
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                fallback_time = self._fallback_sleep_calculation(wake_up_pattern, min_sleep_time, max_sleep_time)
                logger.info(f"[AI_SLEEP] OpenAI failed ({str(e)}), using fallback: {fallback_time}s")
                return fallback_time, f"Fallback calculation (OpenAI error: {str(e)})"
        
        # Run synchronous call in executor
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _sync_calculate)
    
    def _fallback_sleep_calculation(self, wake_up_pattern: str, min_sleep_time: int, max_sleep_time: int) -> int:
        """Fallback sleep calculation when OpenAI call fails"""
        pattern_lower = wake_up_pattern.lower()
        
        if "urgent" in pattern_lower or "immediate" in pattern_lower:
            return max(min_sleep_time, min(30, max_sleep_time))
        elif "frequent" in pattern_lower or "active" in pattern_lower:
            return max(min_sleep_time, min(120, max_sleep_time))  # 2 minutes
        elif "moderate" in pattern_lower or "normal" in pattern_lower:
            return max(min_sleep_time, min(300, max_sleep_time))  # 5 minutes
        elif "slow" in pattern_lower or "patient" in pattern_lower:
            return max(min_sleep_time, min(600, max_sleep_time))  # 10 minutes
        else:
            # Default to middle range
            return max(min_sleep_time, min(180, max_sleep_time))  # 3 minutes