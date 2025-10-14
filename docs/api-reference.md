---
title: API Reference - ProactiveAgent Documentation
description: Complete API reference for ProactiveAgent including providers, decision engines, sleep calculators, and configuration options. Learn how to customize and extend your AI agents.
keywords: ProactiveAgent API, custom decision engines, sleep time calculators, AI provider integration, agent configuration parameters, custom wake patterns, timing decision API
---

# API Reference

Complete API documentation for ProactiveAgent components and configuration options.

## Overview

ProactiveAgent is built with a modular architecture that allows you to customize every aspect of your agent's behavior:

- **[ProactiveAgent](api/agent.md)** - Main agent class that orchestrates everything
- **[Providers](api/providers.md)** - LLM provider integrations (OpenAI, etc.)
- **[Decision Engines](api/decision-engines.md)** - Logic for when to respond
- **[Sleep Calculators](api/sleep-calculators.md)** - Timing between decision cycles
- **[Scheduler](api/scheduler.md)** - Wake-up timing and pattern management

## Quick Navigation

### Core Components
- [ProactiveAgent](api/agent.md) - The main agent class

### Integrations
- [Providers](api/providers.md) - LLM provider abstractions

### Customization
- [Decision Engines](api/decision-engines.md) - Control when your agent responds
- [Sleep Calculators](api/sleep-calculators.md) - Control timing between checks
- [Scheduler](api/scheduler.md) - Internal scheduler implementation

## Providers

Providers are the interface between ProactiveAgent and LLM services. Use the built-in `OpenAIProvider` or create your own.

### Creating a Custom Provider

Extend the `BaseProvider` class and implement the `generate_response` method:

```python
from proactiveagent.providers import BaseProvider

class CustomProvider(BaseProvider):
    def __init__(self, model: str, api_key: str = None):
        self.model = model
        self.api_key = api_key
    
    async def generate_response(
        self, 
        messages: list[dict], 
        system_prompt: str = None
    ) -> str:
        """
        Generate a response from your LLM.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: Optional system prompt
            
        Returns:
            Generated response string
        """
        # Your implementation here
        response = await your_llm_api_call(messages, system_prompt)
        return response

# Use your custom provider
agent = ProactiveAgent(
    provider=CustomProvider(model="your-model"),
    system_prompt="You are a helpful assistant."
)
```

## Configuration

The `decision_config` dictionary controls all aspects of timing and decision-making. This configuration is available to both decision engines and sleep calculators.

### Standard Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `min_response_interval` | int | 30 | Minimum seconds between agent responses |
| `max_response_interval` | int | 600 | Maximum seconds between agent responses |
| `engagement_threshold` | float | 0.5 | Threshold for combined decision score (0.0-1.0) |
| `engagement_high_threshold` | int | 10 | User messages in last hour for "high" engagement |
| `engagement_medium_threshold` | int | 3 | User messages in last hour for "medium" engagement |
| `context_relevance_weight` | float | 0.4 | Weight for context relevance in decision |
| `time_weight` | float | 0.3 | Weight for time elapsed in decision |
| `probability_weight` | float | 0.3 | Weight for AI probability in decision |
| `wake_up_pattern` | str | - | Natural language description of wake pattern |
| `min_sleep_time` | int | 30 | Minimum seconds between wake cycles |
| `max_sleep_time` | int | 600 | Maximum seconds between wake cycles |

### Example with All Parameters

```python
agent = ProactiveAgent(
    provider=OpenAIProvider(model="gpt-5-nano"),
    system_prompt="You are a helpful AI assistant.",
    decision_config={
        # Response timing parameters
        "min_response_interval": 30,      # Prevents spam
        "max_response_interval": 600,     # Prevents abandonment
        
        # Engagement thresholds
        "engagement_threshold": 0.5,      # Decision threshold (0.0-1.0)
        "engagement_high_threshold": 10,  # Messages/hour for high engagement
        "engagement_medium_threshold": 3, # Messages/hour for medium engagement
        
        # Decision weights (must sum to 1.0)
        "context_relevance_weight": 0.4,  # Weight for context factors
        "time_weight": 0.3,                # Weight for time-based factor
        "probability_weight": 0.3,         # Weight for AI decision
        
        # Sleep calculation parameters
        "wake_up_pattern": "Check every 2-3 minutes when active",
        "min_sleep_time": 30,              # Prevents excessive checking
        "max_sleep_time": 600,             # Prevents long inactivity
    },
)
```

### Custom Parameters

You can extend `decision_config` with your own parameters. This is useful when you need to pass configuration to custom decision engines or sleep calculators without hardcoding values.

The `config` dictionary is passed to both decision engines and sleep calculators, allowing you to access any parameters you define:

```python
from proactiveagent.sleep_time_calculators import SleepTimeCalculator

class CustomSleepCalculator(SleepTimeCalculator):
    async def calculate_sleep_time(self, config: dict, context: dict) -> tuple[int, str]:
        # Access standard parameters
        min_sleep = config.get('min_sleep_time', 30)
        max_sleep = config.get('max_sleep_time', 300)
        
        # Access custom parameters
        priority_mode = config.get('priority_mode', False)
        custom_interval = config.get('custom_check_interval', 60)
        
        if priority_mode:
            sleep_time = min(custom_interval // 2, min_sleep)
            return sleep_time, f"Priority mode: checking every {sleep_time}s"
        
        return custom_interval, f"Normal mode: checking every {custom_interval}s"

agent = ProactiveAgent(
    provider=OpenAIProvider(model="gpt-5-nano"),
    system_prompt="You are a helpful assistant.",
    decision_config={
        # Standard parameters
        'min_sleep_time': 30,
        'max_sleep_time': 300,
        # Custom parameters - add any key-value pairs you need
        'custom_check_interval': 120,
        'priority_mode': True,
    }
)

agent.scheduler.sleep_calculator = CustomSleepCalculator()
```

In this example:
- `priority_mode` and `custom_check_interval` are custom parameters not part of the standard configuration
- They're accessed in `CustomSleepCalculator` using `config.get()` with sensible defaults
- This keeps configuration flexible and external to the implementation

The `config` dictionary is available in:
- `DecisionEngine.should_respond(config=...)`
- `SleepTimeCalculator.calculate_sleep_time(config=...)`

## Custom Decision Engines

Decision engines control **whether** the agent should respond. Create custom engines by extending the `DecisionEngine` base class.

### Basic Example

```python
from proactiveagent.decision_engines import DecisionEngine
import time

class CustomDecisionEngine(DecisionEngine):
    async def should_respond(
        self,
        messages: list[dict],
        last_user_message_time: float,
        context: dict,
        config: dict,
        triggered_by_user_message: bool
    ) -> tuple[bool, str]:
        """
        Decide whether the agent should respond.
        
        Args:
            messages: Conversation history
            last_user_message_time: Unix timestamp of last user message
            context: Additional context information
            config: Configuration dictionary
            triggered_by_user_message: True if woken by new user message
            
        Returns:
            Tuple of (should_respond: bool, reasoning: str)
        """
        elapsed = time.time() - last_user_message_time
        
        # Always respond to new messages
        if triggered_by_user_message:
            return True, "User sent a message"
        
        # Check against max interval
        max_interval = config.get('max_response_interval', 300)
        if elapsed > max_interval:
            return True, f"Too long since last message ({elapsed}s)"
        
        return False, "Waiting for appropriate timing"

# Use the custom engine
agent = ProactiveAgent(
    provider=provider,
    decision_engine=CustomDecisionEngine(),
    system_prompt="You are a helpful assistant."
)
```

### Context Dictionary

The `context` dictionary contains conversation state:

```python
context = {
    'messages': [...],              # Full conversation history
    'engagement_level': 'medium',   # 'low', 'medium', or 'high'
    'last_user_message_time': 1234567890.0,
    'user_message_count': 5,
}
```

Add custom context when sending messages:

```python
agent.send_message("Hello", context={'user_mood': 'happy', 'priority': 'high'})
```

## Custom Sleep Calculators

Sleep calculators control **when** the agent wakes up next. Create custom calculators by extending the `SleepTimeCalculator` base class.

### Basic Example

```python
from proactiveagent.sleep_time_calculators import SleepTimeCalculator

class CustomSleepCalculator(SleepTimeCalculator):
    async def calculate_sleep_time(
        self,
        config: dict,
        context: dict
    ) -> tuple[int, str]:
        """
        Calculate how long to sleep before next wake cycle.
        
        Args:
            config: Configuration dictionary
            context: Context including messages, engagement level, etc.
            
        Returns:
            Tuple of (sleep_seconds: int, reasoning: str)
        """
        engagement = context.get('engagement_level', 'low')
        
        # Adjust sleep time based on engagement
        sleep_map = {
            'high': 30,    # Check frequently during active conversation
            'medium': 60,  # Moderate checking
            'low': 120     # Infrequent checking when idle
        }
        
        sleep_time = sleep_map.get(engagement, 60)
        
        # Respect min/max bounds
        min_sleep = config.get('min_sleep_time', 30)
        max_sleep = config.get('max_sleep_time', 300)
        sleep_time = max(min_sleep, min(sleep_time, max_sleep))
        
        return sleep_time, f"Engagement: {engagement}, sleeping {sleep_time}s"

# Use the custom calculator
agent = ProactiveAgent(provider=provider)
agent.scheduler.sleep_calculator = CustomSleepCalculator()
```

### When to Use Custom Implementations

| Use Case | Recommended Approach |
|----------|---------------------|
| Simple timing rules | `FunctionBasedDecisionEngine` |
| Custom LLM/API | Custom `Provider` |
| Complex decision logic | Custom `DecisionEngine` |
| Dynamic sleep timing | Custom `SleepTimeCalculator` |
| Full control over behavior | Combine custom components |

## Built-in Components

### Decision Engines

- **`AIBasedDecisionEngine`** (default) - Uses LLM to evaluate context and decide
- **`ThresholdBasedDecisionEngine`** - Priority-based rules with configurable thresholds
- **`FunctionBasedDecisionEngine`** - Custom logic using Python functions
- **`SimpleDecisionEngine`** - Always responds (useful for testing)

### Sleep Calculators

- **`AIBasedSleepCalculator`** (default) - Uses LLM to determine sleep time based on context
- **`StaticSleepCalculator`** - Fixed intervals regardless of context
- **`PatternBasedSleepCalculator`** - Adjust timing based on conversation keywords
- **`FunctionBasedSleepCalculator`** - Custom logic using Python functions

## Detailed Documentation

For detailed API documentation of each component, see:

- **[ProactiveAgent](api/agent.md)** - Main agent class
- **[Providers](api/providers.md)** - LLM provider interfaces
- **[Decision Engines](api/decision-engines.md)** - Decision engine implementations
- **[Sleep Calculators](api/sleep-calculators.md)** - Sleep calculator implementations
- **[Scheduler](api/scheduler.md)** - Internal scheduler
