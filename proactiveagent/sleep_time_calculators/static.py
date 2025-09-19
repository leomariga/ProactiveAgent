"""Simple static sleep time calculator"""

from typing import Dict, Any
from .base import SleepTimeCalculator


class StaticSleepCalculator(SleepTimeCalculator):
    """Simple static sleep time calculator"""
    
    def __init__(self, sleep_seconds: int, reasoning: str = "Static sleep time"):
        """
        Initialize with fixed sleep time
        
        Args:
            sleep_seconds: Fixed sleep time in seconds
            reasoning: Explanation for the sleep time
        """
        self.sleep_seconds = sleep_seconds
        self.reasoning = reasoning
    
    async def calculate_sleep_time(
        self, 
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> tuple[int, str]:
        """Return the static sleep time"""
        max_sleep_time = config.get('max_sleep_time', 600)  # Default 10 minutes in seconds
        actual_sleep = min(self.sleep_seconds, max_sleep_time)
        return actual_sleep, f"{self.reasoning} (capped at {max_sleep_time}s)"