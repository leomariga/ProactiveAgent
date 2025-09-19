"""Threshold-based decision engine with configurable parameters"""

import time
import logging
from typing import List, Dict, Any
from .base import DecisionEngine


class ThresholdDecisionEngine(DecisionEngine):
    """Threshold-based decision engine with configurable parameters"""
    
    def __init__(self, response_thresholds: Dict[str, int] = None):
        """
        Initialize with response thresholds
        
        Args:
            response_thresholds: Dictionary mapping context types to response intervals in seconds
        """
        self.response_thresholds = response_thresholds or {
            'urgent': 30,
            'high': 120,
            'medium': 300,
            'normal': 600,
            'low': 1200,
            'default': 300
        }
        self.logger = logging.getLogger(__name__)
    
    async def should_respond(
        self,
        messages: List[Dict[str, str]],
        last_user_message_time: float,
        context: Dict[str, Any],
        config: Dict[str, Any],
        triggered_by_user_message: bool = False
    ) -> tuple[bool, str]:
        """Make threshold-based decision"""
        current_time = time.time()
        elapsed_time = int(current_time - last_user_message_time)
        
        # Get config values
        min_response_interval = config.get('min_response_interval', 30)
        max_response_interval = config.get('max_response_interval', 3600)
        
        # Immediate response to user messages
        if triggered_by_user_message and elapsed_time <= 10:
            return True, "Immediate response to user message"
        
        # Respect minimum interval
        if not triggered_by_user_message and elapsed_time < min_response_interval:
            return False, f"Too soon to respond (min interval: {min_response_interval}s)"
        
        # Force response after maximum interval
        if elapsed_time > max_response_interval:
            return True, f"Maximum interval exceeded ({max_response_interval}s)"
        
        # Determine threshold based on context
        urgency = context.get('urgency', 'normal')
        user_engagement = context.get('user_engagement', 'medium')
        
        # Choose threshold based on priority: urgency > engagement > default
        if urgency in self.response_thresholds:
            threshold = self.response_thresholds[urgency]
            reason_key = f"urgency:{urgency}"
        elif user_engagement in self.response_thresholds:
            threshold = self.response_thresholds[user_engagement]
            reason_key = f"engagement:{user_engagement}"
        else:
            threshold = self.response_thresholds['default']
            reason_key = "default"
        
        should_respond = elapsed_time >= threshold
        reason = f"Threshold decision ({reason_key}): {elapsed_time}s >= {threshold}s" if should_respond else f"Waiting ({reason_key}): {elapsed_time}s < {threshold}s"
        
        return should_respond, reason