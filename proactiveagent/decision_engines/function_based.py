"""Function-based decision engine adapter"""

import asyncio
from typing import List, Dict, Any, Callable
from .base import DecisionEngine


class FunctionBasedDecisionEngine(DecisionEngine):
    """Adapter for function-based decision engines"""
    
    def __init__(self, decision_function: Callable):
        """
        Initialize with a decision function
        
        Args:
            decision_function: Function that takes (messages, last_user_message_time, context, config, triggered_by_user_message)
                              and returns (should_respond: bool, reason: str)
        """
        self.decision_function = decision_function
    
    async def should_respond(
        self,
        messages: List[Dict[str, str]],
        last_user_message_time: float,
        context: Dict[str, Any],
        config: Dict[str, Any],
        triggered_by_user_message: bool = False
    ) -> tuple[bool, str]:
        """Make decision using the provided function"""
        # Check if function is async
        if asyncio.iscoroutinefunction(self.decision_function):
            return await self.decision_function(messages, last_user_message_time, context, config, triggered_by_user_message)
        else:
            return self.decision_function(messages, last_user_message_time, context, config, triggered_by_user_message)