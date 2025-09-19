"""Pattern-based sleep time calculator without AI"""

from typing import Dict, Any
from .base import SleepTimeCalculator


class PatternBasedSleepCalculator(SleepTimeCalculator):
    """Pattern-based sleep time calculator without AI"""
    
    def __init__(self, pattern_mappings: Dict[str, int] = None):
        """
        Initialize with pattern mappings
        
        Args:
            pattern_mappings: Dictionary mapping pattern keywords to sleep times in seconds
        """
        self.pattern_mappings = pattern_mappings or {
            'urgent': 30,
            'immediate': 30,
            'frequent': 120,
            'active': 120,
            'moderate': 300,
            'normal': 300,
            'slow': 600,
            'patient': 600,
            'default': 180
        }
    
    async def calculate_sleep_time(
        self, 
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> tuple[int, str]:
        """Calculate sleep time based on pattern keywords"""
        wake_up_pattern = config.get('wake_up_pattern', "")
        max_sleep_time = config.get('max_sleep_time', 600)  # Default 10 minutes in seconds
        pattern_lower = wake_up_pattern.lower()
        
        # Find matching patterns
        matched_patterns = []
        for keyword, sleep_time in self.pattern_mappings.items():
            if keyword in pattern_lower and keyword != 'default':
                matched_patterns.append((keyword, sleep_time))
        
        if matched_patterns:
            # Use the most specific (shortest sleep time) match
            matched_patterns.sort(key=lambda x: x[1])
            chosen_keyword, chosen_time = matched_patterns[0]
            reasoning = f"Pattern match: '{chosen_keyword}' in '{wake_up_pattern}'"
        else:
            # Use default
            chosen_time = self.pattern_mappings['default']
            reasoning = f"No specific pattern found in '{wake_up_pattern}', using default"
        
        actual_sleep = min(chosen_time, max_sleep_time)
        return actual_sleep, reasoning