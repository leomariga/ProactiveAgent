"""Function-based sleep time calculator adapter"""

import asyncio
from typing import Dict, Any, Callable
from .base import SleepTimeCalculator


class FunctionBasedSleepCalculator(SleepTimeCalculator):
    """Adapter for function-based sleep time calculations"""
    
    def __init__(self, calc_function: Callable[[Dict[str, Any], Dict[str, Any]], tuple[int, str]]):
        """
        Initialize with a calculation function
        
        Args:
            calc_function: Function that takes (config, context) 
                          and returns (sleep_seconds, reasoning)
        """
        self.calc_function = calc_function
    
    async def calculate_sleep_time(
        self, 
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> tuple[int, str]:
        """Calculate sleep time using the provided function"""
        # Check if function is async
        if asyncio.iscoroutinefunction(self.calc_function):
            return await self.calc_function(config, context)
        else:
            return self.calc_function(config, context)