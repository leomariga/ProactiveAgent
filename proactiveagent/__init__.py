"""
Proactive AI Agents Library

A Python library for creating proactive AI agents that actively engage users
with configurable wake-up patterns and intelligent response decisions.
"""

__version__ = "0.1.0"
__author__ = "Leonardo Mariga"

from .agent import ProactiveAgent
from .providers.openai_provider import OpenAIProvider

# Export decision engines for convenience
from .decision_engines import (
    DecisionEngine,
    AIBasedDecisionEngine,
    SimpleDecisionEngine,
    ThresholdDecisionEngine,
    FunctionBasedDecisionEngine
)

# Export sleep time calculators for convenience
from .sleep_time_calculators import (
    SleepTimeCalculator,
    AIBasedSleepCalculator,
    StaticSleepCalculator,
    PatternBasedSleepCalculator,
    FunctionBasedSleepCalculator
)

__all__ = [
    "ProactiveAgent", 
    "OpenAIProvider",
    # Decision Engines
    "DecisionEngine",
    "AIBasedDecisionEngine", 
    "SimpleDecisionEngine",
    "ThresholdDecisionEngine",
    "FunctionBasedDecisionEngine",
    # Sleep Time Calculators
    "SleepTimeCalculator",
    "AIBasedSleepCalculator",
    "StaticSleepCalculator", 
    "PatternBasedSleepCalculator",
    "FunctionBasedSleepCalculator"
]