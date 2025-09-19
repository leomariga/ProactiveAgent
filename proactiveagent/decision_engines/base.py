"""Abstract base class for decision engines"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class DecisionEngine(ABC):
    """Abstract base class for response decision strategies"""
    
    @abstractmethod
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
        pass