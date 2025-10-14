---
title: Examples - ProactiveAgent Use Cases and Tutorials
description: Comprehensive examples and tutorials for ProactiveAgent including chat applications, custom decision engines, sleep calculators, and advanced configurations.
keywords: proactive agent examples, decision engine examples, sleep calculator tutorials, AI scheduling examples, autonomous conversation patterns, wake-up pattern examples, timing decision examples
---

# Examples

Practical examples demonstrating ProactiveAgent features. All source code is available in the [examples directory](https://github.com/leomariga/ProactiveAgent/tree/main/examples).

## Basic Usage

| Example | Description |
|---------|-------------|
| [minimal_chat.py](https://github.com/leomariga/ProactiveAgent/blob/main/examples/minimal_chat.py) | Minimal implementation demonstrating core agent initialization, message handling, and default AI-based decision making. |
| [beautiful_chat.py](https://github.com/leomariga/ProactiveAgent/blob/main/examples/beautiful_chat/beautiful_chat.py) | Terminal interface with rich formatting, colored output, and visual feedback for agent decisions. |
| [minimal_callbacks.py](https://github.com/leomariga/ProactiveAgent/blob/main/examples/callbacks/minimal_callbacks.py) | Complete callback implementation showing response, sleep time, and decision callbacks for monitoring agent behavior. |

## Configuration

| Example | Description |
|---------|-------------|
| [all_config_parameters.py](https://github.com/leomariga/ProactiveAgent/blob/main/examples/configs/all_config_parameters.py) | Comprehensive reference documenting all available configuration parameters with inline explanations and default values. |

## Decision Engines

Decision engines evaluate conversation state and determine whether the agent should respond.

| Example | Implementation |
|---------|----------------|
| [ai_based_decision_engine.py](https://github.com/leomariga/ProactiveAgent/blob/main/examples/decision_engines/ai_based_decision_engine.py) | LLM-powered decision making that evaluates context, engagement, and conversation flow. |
| [threshold_decision_engine.py](https://github.com/leomariga/ProactiveAgent/blob/main/examples/decision_engines/threshold_decision_engine.py) | Rule-based system using configurable thresholds for priority levels and engagement metrics. |
| [function_based_decision_engine.py](https://github.com/leomariga/ProactiveAgent/blob/main/examples/decision_engines/function_based_decision_engine.py) | Custom decision logic implemented as a Python function with access to message history and context. |
| [simple_decision_engine.py](https://github.com/leomariga/ProactiveAgent/blob/main/examples/decision_engines/simple_decision_engine.py) | Always-respond implementation useful for testing and debugging agent responses. |
| [custom_decision_engine.py](https://github.com/leomariga/ProactiveAgent/blob/main/examples/decision_engines/custom_decision_engine.py) | Full custom implementation extending the base `DecisionEngine` class for complex logic requiring state management. |

## Sleep Calculators

Sleep calculators determine wait duration between agent wake cycles.

| Example | Implementation |
|---------|----------------|
| [ai_based_sleep_calculator.py](https://github.com/leomariga/ProactiveAgent/blob/main/examples/sleep_calculators/ai_based_sleep_calculator.py) | LLM-driven calculation adapting sleep time based on conversation dynamics and engagement patterns. |
| [static_sleep_calculator.py](https://github.com/leomariga/ProactiveAgent/blob/main/examples/sleep_calculators/static_sleep_calculator.py) | Fixed-interval implementation providing consistent timing regardless of conversation state. |
| [pattern_based_sleep_calculator.py](https://github.com/leomariga/ProactiveAgent/blob/main/examples/sleep_calculators/pattern_based_sleep_calculator.py) | Keyword-driven timing adjustments based on conversation content and detected patterns. |
| [function_based_sleep_calculator.py](https://github.com/leomariga/ProactiveAgent/blob/main/examples/sleep_calculators/function_based_sleep_calculator.py) | Custom calculation logic implemented as a Python function with access to configuration and context. |
| [custom_sleep_calculator.py](https://github.com/leomariga/ProactiveAgent/blob/main/examples/sleep_calculators/custom_sleep_calculator.py) | Full custom implementation extending the base `SleepTimeCalculator` class for advanced timing strategies. |

## Running Examples

```bash
git clone https://github.com/leomariga/ProactiveAgent.git
cd ProactiveAgent
uv sync

export OPENAI_API_KEY='your-api-key-here'
uv run python examples/minimal_chat.py
```

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](https://github.com/leomariga/ProactiveAgent/blob/main/CONTRIBUTING.md) for guidelines.
