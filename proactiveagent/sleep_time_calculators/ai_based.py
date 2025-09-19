"""AI provider-based sleep time calculator (default behavior)"""

from typing import Dict, Any
from .base import SleepTimeCalculator
from ..providers.base import BaseProvider


class AIBasedSleepCalculator(SleepTimeCalculator):
    """AI provider-based sleep time calculation (default behavior)"""
    
    def __init__(self, provider: BaseProvider):
        """
        Initialize with an AI provider
        
        Args:
            provider: AI provider instance that implements calculate_sleep_time
        """
        self.provider = provider
    
    async def calculate_sleep_time(
        self, 
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> tuple[int, str]:
        """Calculate sleep time using AI provider"""
        wake_up_pattern = config.get('wake_up_pattern', "Check every 2-3 minutes if conversation is active")
        min_sleep_time = config.get('min_sleep_time', 30)  # Default 30 seconds
        max_sleep_time = config.get('max_sleep_time', 600)  # Default 10 minutes in seconds
        return await self.provider.calculate_sleep_time(wake_up_pattern, min_sleep_time, max_sleep_time, context)