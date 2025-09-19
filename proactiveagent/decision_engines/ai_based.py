"""AI provider-based decision engine (default behavior)"""

import time
import logging
from typing import List, Dict, Any
from .base import DecisionEngine
from ..providers.base import BaseProvider


class AIBasedDecisionEngine(DecisionEngine):
    """AI provider-based decision engine (default behavior)"""
    
    def __init__(self, provider: BaseProvider):
        """
        Initialize with an AI provider
        
        Args:
            provider: AI provider instance
        """
        self.provider = provider
        self.logger = logging.getLogger(__name__)
    
    async def should_respond(
        self,
        messages: List[Dict[str, str]],
        last_user_message_time: float,
        context: Dict[str, Any],
        config: Dict[str, Any],
        triggered_by_user_message: bool = False
    ) -> tuple[bool, str]:
        """
        Determine if AI should respond and provide reasoning
        
        Args:
            messages: Conversation history
            last_user_message_time: Timestamp of last user message
            context: Current context information
            config: Full configuration dictionary
            triggered_by_user_message: True if this evaluation was triggered by a user message
            
        Returns:
            Tuple of (should_respond: bool, reason: str)
        """
        current_time = time.time()
        elapsed_time = int(current_time - last_user_message_time)
        
        # Get config values directly from dictionary
        min_response_interval = config.get('min_response_interval', 30)  # 30 seconds
        max_response_interval = config.get('max_response_interval', 3600)  # 1 hour
        engagement_threshold = config.get('engagement_threshold', 0.5)
        context_relevance_weight = config.get('context_relevance_weight', 0.4)
        time_weight = config.get('time_weight', 0.3)
        probability_weight = config.get('probability_weight', 0.3)
        
        self.logger.debug(f"[DECISION] Evaluating response. Elapsed: {elapsed_time}s, triggered_by_user: {triggered_by_user_message}")
        
        # Skip minimum interval check if triggered by user message
        if not triggered_by_user_message and elapsed_time < min_response_interval:
            reason = f"Too soon to respond (min interval: {min_response_interval}s)"
            self.logger.info(f"[DECISION] Blocked: {reason}")
            return False, reason
        
        # Check maximum interval - always respond if too much time has passed
        if elapsed_time > max_response_interval:
            reason = f"Maximum interval exceeded ({max_response_interval}s)"
            self.logger.info(f"[DECISION] Forced: {reason}")
            return True, reason
        
        # If triggered by user message and it's very recent, allow immediate response
        if triggered_by_user_message and elapsed_time <= 10:  # Within 10 seconds
            reason = "Immediate response to user message"
            self.logger.info(f"[DECISION] Immediate: {reason}")
            return True, reason
        
        try:
            # Multi-factor analysis
            time_factor = self._calculate_time_factor(elapsed_time, max_response_interval)
            context_factor = self._calculate_context_factor(messages, context, config)
            
            # Use AI provider for intelligent decision
            ai_decision = await self.provider.should_respond(messages, elapsed_time, context)
            
            # Combine factors
            combined_score = (
                time_factor * time_weight +
                context_factor * context_relevance_weight +
                (1.0 if ai_decision else 0.0) * probability_weight
            )
            
            should_respond = combined_score >= engagement_threshold
            
            self.logger.info(f"[DECISION] Score: {combined_score:.2f} (threshold: {engagement_threshold}) → {should_respond}")
            
            reason = self._build_decision_reason(
                should_respond, elapsed_time, time_factor, 
                context_factor, ai_decision, combined_score, engagement_threshold
            )
            
            return should_respond, reason
            
        except Exception as e:
            self.logger.error(f"[DECISION] Error: {str(e)}")
            # Fallback to simple time-based decision
            fallback_decision = elapsed_time > (min_response_interval * 3)
            reason = f"Fallback decision based on time ({elapsed_time}s)"
            self.logger.warning(f"[DECISION] Using fallback: {fallback_decision}")
            return fallback_decision, reason
    
    def _calculate_time_factor(self, elapsed_time: int, max_response_interval: int) -> float:
        """
        Calculate time-based factor for response decision
        
        Args:
            elapsed_time: Seconds since last user message
            max_response_interval: Maximum response interval from config
            
        Returns:
            Time factor (0.0 to 1.0)
        """
        # Sigmoid function for smooth time-based scaling
        normalized_time = elapsed_time / max_response_interval
        return min(1.0, normalized_time ** 0.5)
    
    def _calculate_context_factor(
        self, 
        messages: List[Dict[str, str]], 
        context: Dict[str, Any],
        config: Dict[str, Any]
    ) -> float:
        """
        Calculate context-based factor for response decision
        
        Args:
            messages: Recent conversation messages
            context: Current context information
            config: Full configuration dictionary
            
        Returns:
            Context factor (0.0 to 1.0)
        """
        factor = 0.0
        
        # Check if last message was a question
        if messages and "?" in messages[-1].get('content', ''):
            factor += 0.3
        
        # Check engagement indicators
        user_engagement = context.get('user_engagement', 'medium')
        if user_engagement == 'high':
            factor += 0.4
        elif user_engagement == 'medium':
            factor += 0.2
        
        # Check conversation urgency
        urgency = context.get('urgency', 'normal')
        if urgency == 'high':
            factor += 0.3
        elif urgency == 'medium':
            factor += 0.1
        
        # Check if topic requires follow-up
        if context.get('requires_followup', False):
            factor += 0.2
        
        return min(1.0, factor)
    
    def _build_decision_reason(
        self,
        should_respond: bool,
        elapsed_time: int,
        time_factor: float,
        context_factor: float,
        ai_decision: bool,
        combined_score: float,
        engagement_threshold: float
    ) -> str:
        """Build human-readable decision reason"""
        if should_respond:
            reasons = []
            if time_factor > 0.7:
                reasons.append(f"significant time elapsed ({elapsed_time}s)")
            if context_factor > 0.5:
                reasons.append("high context relevance")
            if ai_decision:
                reasons.append("AI recommends response")
            
            return f"Responding due to: {', '.join(reasons)} (score: {combined_score:.2f})"
        else:
            return f"Not responding - score too low ({combined_score:.2f} < {engagement_threshold})"