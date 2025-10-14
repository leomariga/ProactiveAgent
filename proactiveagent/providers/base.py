"""Base provider interface for AI services"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseProvider(ABC):
    """Abstract base class for AI providers"""
    
    def __init__(self, model: str, **kwargs: Any):
        """
        Initialize provider
        
        Args:
            model: Model name/identifier
            **kwargs: Provider-specific configuration
        """
        self.model = model
        self.config = kwargs
    
    @abstractmethod
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None,
        triggered_by_user_message: bool = False,
        **kwargs: Any
    ) -> str:
        """
        Generate a response from the AI
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            system_prompt: Optional system prompt
            triggered_by_user_message: Whether the response was triggered by a user message
            **kwargs: Additional generation parameters
            
        Returns:
            Generated response text
        """
        pass
    
    @abstractmethod
    async def should_respond(
        self,
        messages: List[Dict[str, str]],
        elapsed_time: int,
        context: Dict[str, Any]
    ) -> bool:
        """
        Determine if the AI should respond based on context
        
        Args:
            messages: Conversation history
            elapsed_time: Time since last user message (seconds)
            context: Additional context information
            
        Returns:
            True if AI should respond, False otherwise
        """
        pass
    
    @abstractmethod
    async def calculate_sleep_time(
        self,
        wake_up_pattern: str,
        min_sleep_time: int,
        max_sleep_time: int,
        context: Dict[str, Any]
    ) -> tuple[int, str]:
        """
        Calculate how long to sleep before next wake-up
        
        Args:
            wake_up_pattern: User-defined wake-up pattern description
            min_sleep_time: Minimum allowed sleep time (seconds)
            max_sleep_time: Maximum allowed sleep time (seconds)
            context: Current conversation context
            
        Returns:
            Tuple of (sleep_time_seconds: int, reasoning: str)
        """
        pass