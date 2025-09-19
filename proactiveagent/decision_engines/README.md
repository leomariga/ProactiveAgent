# Decision Engines

This directory contains the modular decision engine system for Proactive AI agents. Each decision engine implements different strategies for determining when the AI should respond to conversations.

## Available Decision Engines

### `base.py` - DecisionEngine (Abstract Base Class)
The abstract base class that all decision engines must inherit from. Defines the `should_respond` method interface.

### `ai_based.py` - AIBasedDecisionEngine 
The default decision engine that uses AI provider intelligence combined with time-based and context-based factors. This provides the most sophisticated decision-making capabilities.

**Features:**
- Multi-factor analysis (time, context, AI recommendation)
- Configurable weights and thresholds
- Intelligent scoring system
- Fallback to time-based decisions on errors

### `simple.py` - SimpleDecisionEngine
A straightforward time-based decision engine that doesn't require AI calls. Good for basic use cases or when you want predictable, deterministic behavior.

**Features:**
- Pure time-based logic
- Immediate response to user messages
- Configurable intervals
- No AI provider dependency

### `threshold_based.py` - ThresholdDecisionEngine
A decision engine that uses configurable thresholds based on conversation context (urgency, engagement level).

**Features:**
- Context-aware thresholds
- Configurable response times per engagement level
- Priority-based decision making (urgency > engagement > default)
- No AI provider dependency

### `function_based.py` - FunctionBasedDecisionEngine
An adapter that allows you to use custom functions as decision engines. Supports both sync and async functions.

**Features:**
- Wrap any function as a decision engine
- Automatic async/sync detection
- Full access to all decision parameters
- Maximum flexibility for custom logic

## Usage Examples

```python
from proactiveagent.decision_engines import (
    AIBasedDecisionEngine,
    SimpleDecisionEngine, 
    ThresholdDecisionEngine,
    FunctionBasedDecisionEngine
)

# Default AI-based engine
engine = AIBasedDecisionEngine(provider)

# Simple time-based engine  
engine = SimpleDecisionEngine()

# Threshold-based with custom thresholds
engine = ThresholdDecisionEngine({
    'urgent': 30,
    'high': 120,
    'medium': 300,
    'normal': 600,
    'default': 240
})

# Custom function-based engine
def my_decision_logic(messages, last_time, context, config, triggered):
    # Your custom logic here
    return should_respond, reason

engine = FunctionBasedDecisionEngine(my_decision_logic)
```

## Creating Custom Decision Engines

To create a custom decision engine, inherit from `DecisionEngine` and implement the `should_respond` method:

```python
from proactiveagent.decision_engines.base import DecisionEngine

class MyCustomEngine(DecisionEngine):
    async def should_respond(self, messages, last_user_message_time, context, config, triggered_by_user_message=False):
        # Your decision logic here
        return should_respond, reason
```

## Configuration Access

All decision engines receive the full configuration dictionary and should access values directly:

```python
min_interval = config.get('min_response_interval', 30)
max_interval = config.get('max_response_interval', 3600)
threshold = config.get('engagement_threshold', 0.5)
```

This approach ensures maximum flexibility and allows users to configure decision engines exactly as needed without being constrained by pre-defined instance variables.