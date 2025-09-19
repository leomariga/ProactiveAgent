"""Abstract base class for sleep time calculators"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class SleepTimeCalculator(ABC):
    """Abstract base class for sleep time calculation strategies"""
    
    @abstractmethod
    async def calculate_sleep_time(
        self, 
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> tuple[int, str]:
        """
        Calculate how long to sleep before next wake-up
        
        Args:
            config: Full configuration dictionary containing wake_up_pattern, max_sleep_time (int), etc.
            context: Current conversation context
            
        Returns:
            Tuple of (sleep_time_seconds: int, reasoning: str)
        """
        pass