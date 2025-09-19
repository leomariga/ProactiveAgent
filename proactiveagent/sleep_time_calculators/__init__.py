"""Sleep time calculators package for Active AI agents"""

from .base import SleepTimeCalculator
from .ai_based import AIBasedSleepCalculator
from .function_based import FunctionBasedSleepCalculator
from .static import StaticSleepCalculator
from .pattern_based import PatternBasedSleepCalculator

# Maintain backward compatibility with old naming
AIBasedCalculator = AIBasedSleepCalculator
FunctionBasedCalculator = FunctionBasedSleepCalculator
StaticCalculator = StaticSleepCalculator
PatternBasedCalculator = PatternBasedSleepCalculator

__all__ = [
    'SleepTimeCalculator',
    'AIBasedSleepCalculator',
    'FunctionBasedSleepCalculator', 
    'StaticSleepCalculator',
    'PatternBasedSleepCalculator',
    # Backward compatibility aliases
    'AIBasedCalculator',
    'FunctionBasedCalculator',
    'StaticCalculator', 
    'PatternBasedCalculator'
]