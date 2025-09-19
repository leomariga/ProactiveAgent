# Sleep Time Calculators

This directory contains the modular sleep time calculation system for Proactive AI agents. Each calculator implements different strategies for determining how long the agent should sleep between wake-up checks.

## Available Sleep Time Calculators

### `base.py` - SleepTimeCalculator (Abstract Base Class)
The abstract base class that all sleep time calculators must inherit from. Defines the `calculate_sleep_time` method interface.

### `ai_based.py` - AIBasedSleepCalculator
The default calculator that uses AI provider intelligence to determine appropriate sleep times based on conversation patterns and context.

**Features:**
- Uses AI provider's `calculate_sleep_time` method
- Considers wake-up patterns and conversation context
- Respects maximum sleep time limits
- Intelligent, context-aware sleep timing

### `static.py` - StaticSleepCalculator
A simple calculator that returns a fixed sleep time. Good for predictable, deterministic behavior or testing scenarios.

**Features:**
- Fixed sleep time regardless of context
- Respects maximum sleep time configuration
- Custom reasoning messages
- No AI provider dependency

### `pattern_based.py` - PatternBasedSleepCalculator
A calculator that maps keywords in wake-up patterns to specific sleep times without requiring AI calls.

**Features:**
- Keyword-based pattern matching
- Configurable keyword-to-time mappings
- Intelligent pattern priority (shortest time wins)
- Fallback to default time
- No AI provider dependency

### `function_based.py` - FunctionBasedSleepCalculator
An adapter that allows you to use custom functions as sleep time calculators. Supports both sync and async functions.

**Features:**
- Wrap any function as a sleep time calculator
- Automatic async/sync detection
- Full access to config and context
- Maximum flexibility for custom logic

## Usage Examples

```python
from proactiveagent.sleep_time_calculators import (
    AIBasedSleepCalculator,
    StaticSleepCalculator,
    PatternBasedSleepCalculator,
    FunctionBasedSleepCalculator
)

# Default AI-based calculator
calc = AIBasedSleepCalculator(provider)

# Static calculator - always sleep for 3 minutes
calc = StaticSleepCalculator(180, "Fixed 3-minute intervals")

# Pattern-based with custom mappings
calc = PatternBasedSleepCalculator({
    'urgent': 30,       # 30 seconds for urgent patterns
    'frequent': 60,     # 1 minute for frequent checks
    'normal': 180,      # 3 minutes for normal patterns  
    'patient': 300,     # 5 minutes for patient patterns
    'default': 120      # 2 minutes default
})

# Custom function-based calculator
def my_sleep_logic(config, context):
    # Your custom logic here
    return sleep_seconds, reasoning

calc = FunctionBasedSleepCalculator(my_sleep_logic)
```

## Creating Custom Sleep Time Calculators

To create a custom sleep time calculator, inherit from `SleepTimeCalculator` and implement the `calculate_sleep_time` method:

```python
from proactiveagent.sleep_time_calculators.base import SleepTimeCalculator

class MyCustomCalculator(SleepTimeCalculator):
    async def calculate_sleep_time(self, config, context):
        # Your calculation logic here
        sleep_time = 120  # Example: 2 minutes
        reasoning = "Custom calculation based on specific criteria"
        return sleep_time, reasoning
```

## Configuration Access

All calculators receive the full configuration dictionary and should access values directly:

```python
wake_up_pattern = config.get('wake_up_pattern', 'default pattern')
max_sleep_time = config.get('max_sleep_time', 600)  # 10 minutes default
user_activity = context.get('user_engagement', 'medium')
```

## Common Configuration Parameters

- `wake_up_pattern`: String describing when/how often to wake up
- `max_sleep_time`: Maximum sleep time in seconds (hard limit)
- Context may include:
  - `user_engagement`: 'high', 'medium', 'low'
  - `conversation_length`: Number of messages
  - `urgency`: 'urgent', 'normal', 'low'
  - Custom context values set by your application

## Integration with Scheduler

Sleep time calculators are used by the `WakeUpScheduler` class. The scheduler calls `calculate_sleep_time` and uses the returned value to determine when to wake up the agent for the next evaluation cycle.