"""Simple time-based decision engine without AI"""

import time
import logging
from typing import List, Dict, Any
from .base import DecisionEngine


class SimpleDecisionEngine(DecisionEngine):
    """Simple time-based decision engine without AI"""
    
    def __init__(self):
        """Initialize simple decision engine"""
        self.logger = logging.getLogger(__name__)
    
    async def should_respond(
        self,
        messages: List[Dict[str, str]],
        last_user_message_time: float,
        context: Dict[str, Any],
        config: Dict[str, Any],
        triggered_by_user_message: bool = False
    ) -> tuple[bool, str]:
        """Make simple time-based decision"""
        current_time = time.time()
        elapsed_time = int(current_time - last_user_message_time)
        
        # Get config values directly from dictionary
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
        
        # Simple middle-ground logic
        response_threshold = min_response_interval * 2
        should_respond = elapsed_time >= response_threshold
        reason = f"Simple time-based decision: {elapsed_time}s >= {response_threshold}s" if should_respond else f"Waiting: {elapsed_time}s < {response_threshold}s"
        
        return should_respond, reason