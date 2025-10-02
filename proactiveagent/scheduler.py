"""Wake-up scheduler for Active AI agents"""

import asyncio
import time
import logging
from typing import Dict, Any, Callable, List, Union, Optional
from .providers.base import BaseProvider
from .sleep_time_calculators import SleepTimeCalculator, AIBasedCalculator


class WakeUpScheduler:
    """Manages wake-up timing and pattern interpretation for AI agents"""
    
    def __init__(
        self, 
        provider: BaseProvider, 
        config: Dict[str, Any], 
        get_sleep_time_callbacks_func: callable = None,
        sleep_time_calculator: Optional[SleepTimeCalculator] = None
    ):
        """
        Initialize scheduler
        
        Args:
            provider: AI provider instance
            config: Configuration dictionary
            get_sleep_time_callbacks_func: Function that returns current sleep time callbacks
            sleep_time_calculator: Custom sleep time calculator (defaults to AIBasedCalculator)
        """
        self.provider = provider
        self.config = config
        self.is_running = False
        self.logger = logging.getLogger(__name__)
        self._interrupt_sleep = False
        self.get_sleep_time_callbacks = get_sleep_time_callbacks_func or (lambda: [])
        
        # Use provided calculator or default to AI-based calculation
        self.sleep_time_calculator = sleep_time_calculator or AIBasedCalculator(provider)
        
    
    async def start(
        self, 
        wake_up_callback: Callable[[Dict[str, Any]], None],
        context_provider: Callable[[], Dict[str, Any]]
    ) -> None:
        """
        Start the wake-up scheduler
        
        Args:
            wake_up_callback: Function to call when waking up
            context_provider: Function that returns current context
        """
        self.is_running = True
        
        while self.is_running:
            try:
                # Get current context
                context = context_provider()
                
                # Calculate sleep time using the configured calculator
                sleep_time, reasoning = await self.sleep_time_calculator.calculate_sleep_time(
                    self.config,
                    context
                )
                
                self.logger.info(f"[SCHEDULER] Sleep time calculated: {sleep_time}s ')")
                
                # Call sleep time callbacks
                self._call_sleep_time_callbacks(sleep_time, reasoning)
                
                # Sleep with interruption checking
                interrupted = await self._interruptible_sleep(sleep_time)
                
                # If sleep was interrupted (e.g., due to a user message),
                # skip the immediate wake-up callback to avoid double evaluation.
                if self.is_running and not interrupted:
                    # Wake up and call the callback
                    wake_up_context = context_provider()
                    wake_up_context['wake_up_time'] = time.time()
                    self.logger.info(f"[SCHEDULER] Agent waking up after {sleep_time}s")
                    wake_up_callback(wake_up_context)
                    
            except Exception as e:
                self.logger.error(f"Error in wake-up scheduler: {str(e)}")
                # Sleep for a short time before retrying
                await asyncio.sleep(30)
    
    async def _interruptible_sleep(self, seconds: int) -> bool:
        """
        Sleep that can be interrupted by stopping the scheduler or sleep interruption
        
        Args:
            seconds: Number of seconds to sleep
        
        Returns:
            bool: True if sleep was interrupted, False otherwise
        """
        sleep_interval = 1  # Check every second
        total_slept = 0
        
        while total_slept < seconds and self.is_running and not self._interrupt_sleep:
            await asyncio.sleep(min(sleep_interval, seconds - total_slept))
            total_slept += sleep_interval
        
        # Reset interrupt flag after sleep is broken and report interruption status
        was_interrupted = False
        if self._interrupt_sleep:
            was_interrupted = True
            self._interrupt_sleep = False
            self.logger.info("[SCHEDULER] Sleep interrupted, recalculating immediately")
        
        return was_interrupted
    
    def stop(self) -> None:
        """Stop the wake-up scheduler"""
        self.is_running = False
        self.logger.info("Wake-up scheduler stopped")
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """
        Update scheduler configuration
        
        Args:
            new_config: Dictionary containing configuration updates
        """
        self.config.update(new_config)
    
    def set_sleep_time_calculator(self, calculator: SleepTimeCalculator) -> None:
        """
        Update the sleep time calculator
        
        Args:
            calculator: New sleep time calculator to use
        """
        self.sleep_time_calculator = calculator
        self.logger.info(f"[SCHEDULER] Sleep time calculator updated to: {calculator.__class__.__name__}")
    
    def interrupt_sleep(self) -> None:
        """
        Interrupt the current sleep to trigger immediate recalculation
        """
        self._interrupt_sleep = True
        self.logger.debug("[SCHEDULER] Sleep interruption requested")
    
    def _call_sleep_time_callbacks(self, sleep_time: int, reasoning: str) -> None:
        """
        Call all registered sleep time callbacks
        
        Args:
            sleep_time: Calculated sleep time in seconds
            reasoning: AI's reasoning for the sleep time
        """
        callbacks = self.get_sleep_time_callbacks()
        self.logger.debug(f"[SCHEDULER] Calling {len(callbacks)} sleep time callbacks")
        self.logger.debug(f"[SCHEDULER] Callbacks list: {[cb.__name__ for cb in callbacks]}")
        
        if not callbacks:
            self.logger.debug("[SCHEDULER] No sleep time callbacks registered")
            return
            
        for i, callback in enumerate(callbacks):
            try:
                self.logger.debug(f"[SCHEDULER] Calling sleep time callback {i}: {callback.__name__}")
                callback(sleep_time, reasoning)
            except Exception as e:
                self.logger.error(f"Error in sleep time callback {callback.__name__}: {str(e)}")