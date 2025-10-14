---
title: Getting Started with ProactiveAgent
description: Learn how to build your first proactive AI agent with ProactiveAgent. Step-by-step guide covering installation, configuration, decision engines, and sleep calculators.
keywords: proactive agent tutorial, thread, AI timing configuration, decision engine setup, sleep calculator configuration, autonomous AI agent, wake-up pattern configuration, AI scheduling tutorial
---

# Getting Started

This guide will walk you through creating your first proactive AI agent. By the end, you'll understand how to build agents that can initiate conversations, make timing decisions, and maintain engagement autonomously.

## Installation

Install ProactiveAgent using pip:

```bash
pip install proactiveagent
```

You might also need an API key from a provider. For example, using OpenAI, set it as an environment variable:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Quick Start

Here's a minimal example to get you started:

```python
import time
from proactiveagent import ProactiveAgent, OpenAIProvider

agent = ProactiveAgent(
    provider=OpenAIProvider(model="gpt-5-nano"),
    system_prompt="ou are a casual bored teenager. Answer like you're texting a friend.",
    decision_config={
        'wake_up_pattern': "Use the pace of a normal text chat",
    },
)

agent.add_callback(lambda response: print(f"🤖 AI: {response}"))
agent.start()

print("Chat started! Type your messages:")

while True:
    message = input("You: ").strip()
    if message.lower() == 'quit': break
    agent.send_message(message)
    time.sleep(3)

agent.stop()
print("Chat ended!")
```

This creates a conversational agent that:

- Operates on an autonomous schedule
- Decides when to respond based on conversation context
- Maintains natural conversation flow over time

**Key Parameters:**

- `provider` - Choose which provider you want to use.
- `decision_config` - Configuration dictionary that controls the agent's behavior
- `wake_up_pattern` - Define in natural language how to determine sleep intervals between wake cycles (used by the default AI-based sleep calculator)

## Core Concepts

ProactiveAgent operates on a simple cycle:

**wake → decide → respond → sleep**

1. **Wake**: The agent wakes up at scheduled intervals
2. **Decide**: Evaluates whether to respond based on conversation state
3. **Respond**: Generates and sends a message if appropriate
4. **Sleep**: Calculates the next wake time and goes dormant

This cycle enables time-aware behavior without requiring constant polling or external triggers.

## Callbacks

Use callbacks to observe the agent's decision-making process:

```python
import time
from proactiveagent import ProactiveAgent, OpenAIProvider


def on_response(response: str):
    """Called when AI sends a response"""
    print(f"🤖 AI: {response}")


def on_sleep(sleep_time: int, reasoning: str):
    """Called when AI calculates sleep time"""
    print(f"⏰ Sleep: {sleep_time}s - {reasoning}")


def on_decision(should_respond: bool, reasoning: str):
    """Called when AI makes a decision about whether to respond"""
    status = "RESPOND" if should_respond else "WAIT"
    print(f"🧠 {status} - {reasoning}")


agent = ProactiveAgent(
    provider=OpenAIProvider(model="gpt-5-nano"),
    system_prompt="ou are a casual bored teenager. Answer like you're texting a friend.",
    decision_config={
        'wake_up_pattern': "Use the pace of a normal text chat",
    },
)

agent.add_callback(on_response)
agent.add_sleep_time_callback(on_sleep)
agent.add_decision_callback(on_decision)

agent.start()

print("Chat started! Type your messages:")

while True:
    message = input("You: ").strip()
    if message.lower() == 'quit': break
    agent.send_message(message)
    time.sleep(3)

agent.stop()
print("Chat ended!")
```

Callbacks are useful for debugging, logging, and integrating with external systems.

## Decision Engines

Decision engines determine whether the agent should respond. ProactiveAgent supports multiple strategies:

| Engine | Description | Use Case |
|--------|-------------|----------|
| **AI-based** (default) | LLM evaluates context and decides | Natural, context-aware responses |
| **Threshold** | Priority-based rules | Predictable, cost-effective |
| **Function-based** | Custom Python logic | Full control over behavior |

### Custom Decision Logic

Use `FunctionBasedDecisionEngine` for complete control:

```python
from proactiveagent import ProactiveAgent, OpenAIProvider
from proactiveagent.decision_engines import FunctionBasedDecisionEngine

def custom_decision_function(messages, last_user_message_time, context, config, triggered_by_user_message):
    """Custom decision logic with specific timing rules"""
    import time
    current_time = time.time()
    elapsed_time = int(current_time - last_user_message_time)

    # Respond immediately to new user messages
    if triggered_by_user_message:
        return True, "User just sent a message"

    # Wait at least 60 seconds between responses
    if elapsed_time < 60:
        return False, f"Too soon - wait {60 - elapsed_time}s more"

    # Respond if we've been quiet for more than 2 minutes
    if elapsed_time > 120:
        return True, f"Been quiet for {elapsed_time}s - time to respond"

    return False, "Waiting for good timing"

provider = OpenAIProvider(model="gpt-5-nano")
decision_engine = FunctionBasedDecisionEngine(custom_decision_function)

agent = ProactiveAgent(
    provider=provider,
    decision_engine=decision_engine,
    system_prompt="You are a helpful AI assistant.",
    decision_config={
        'min_response_interval': 60,
        'max_response_interval': 300,
    }
)
```

The function receives conversation state and returns a tuple: `(should_respond: bool, reasoning: str)`.

**Why AI-based is the default:** LLMs excel at evaluating conversation context, engagement levels, and timing appropriateness—judgments that are difficult to encode in simple rules.

## Sleep Calculators

Sleep calculators control how long the agent waits before waking up again. Available options:

| Calculator | Behavior | Best For |
|------------|----------|----------|
| **AI-based** (default) | Context-aware timing | Natural conversation flow |
| **Static** | Fixed intervals | Predictable costs |
| **Pattern-based** | Keyword-driven timing | Specific use cases |
| **Function-based** | Custom logic | Complex timing rules |

### Static Sleep Example

```python
import time
from proactiveagent import ProactiveAgent, OpenAIProvider
from proactiveagent.sleep_time_calculators import StaticSleepCalculator


def on_ai_response(response: str):
    print(f"🤖 AI: {response}")


def on_sleep_time_calculated(sleep_time: int, reasoning: str):
    print(f"⏰ Sleep: {sleep_time}s - {reasoning}")


def main():
    provider = OpenAIProvider(model="gpt-5-nano")

    # Use static sleep calculator with fixed 2-minute intervals
    sleep_calculator = StaticSleepCalculator(120, "Fixed 2-minute intervals")

    agent = ProactiveAgent(
        provider=provider,
        system_prompt="You are a helpful AI assistant.",
        decision_config={
            'min_sleep_time': 60,
            'max_sleep_time': 300,
        }
    )

    # Override the default sleep calculator
    agent.scheduler.sleep_calculator = sleep_calculator

    agent.add_callback(on_ai_response)
    agent.add_sleep_time_callback(on_sleep_time_calculated)
    agent.start()

    print("=== Static Sleep Calculator ===")
    print("Always sleeps for 2 minutes between checks.")
    print("Type 'quit' to exit.\n")

    while True:
        message = input("You: ").strip()
        if message.lower() == 'quit': break
        agent.send_message(message)
        time.sleep(1)

    agent.stop()


if __name__ == "__main__":
    main()
```

## Configuration

Configure agent behavior through the `decision_config` dictionary:

```python
agent = ProactiveAgent(
    provider=provider,
    system_prompt="You are a helpful AI assistant.",
    decision_config={
        # Response timing parameters
        "min_response_interval": 30,
        "max_response_interval": 600,
        # Decision-making weights and thresholds
        "engagement_threshold": 0.5,
        "engagement_high_threshold": 10,
        "engagement_medium_threshold": 3,
        "context_relevance_weight": 0.4,
        "time_weight": 0.3,
        "probability_weight": 0.3,
        # Sleep calculation parameters
        "wake_up_pattern": "Check every 2-3 minutes when active",
        "min_sleep_time": 30,
        "max_sleep_time": 600,
    },
)
```

For comprehensive configuration examples, see the [`examples/configs/`](https://github.com/leomariga/ProactiveAgent/tree/main/examples/configs) directory.

## Best Practices

**Cost Management**

- Use rule-based engines (threshold, function) for predictable costs
- Start with longer sleep intervals and reduce after user engagement
- Keep system prompts concise to reduce token usage

**Reliability**

- Implement comprehensive logging with callbacks
- Monitor decision patterns for unexpected behavior
- Consider fallback logic for critical applications

**When to Use**

- ✅ Conversational agents that maintain engagement over time
- ✅ Notification systems with intelligent timing
- ✅ Monitoring agents that respond to changes

**When Not to Use**

- ❌ Mission-critical systems requiring guaranteed reliability
- ❌ High-frequency real-time applications

## Next Steps

Now that you understand the basics, explore:

- **[API Reference](api-reference.md)** - Detailed API documentation
- **[Examples](examples.md)** - More advanced usage patterns
- **[GitHub Repository](https://github.com/leomariga/ProactiveAgent)** - Source code and examples

## Resources

- **Repository**: [leomariga/ProactiveAgent](https://github.com/leomariga/ProactiveAgent)
- **PyPI Package**: [proactiveagent](https://pypi.org/project/proactiveagent/)
- **Issue Tracker**: [GitHub Issues](https://github.com/leomariga/ProactiveAgent/issues)
