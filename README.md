<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/logo_b.png" width="400">
  <source media="(prefers-color-scheme: light)" srcset="docs/logo.png" width="400">
  <img alt="ProactiveAgent logo." src="docs/logo.png" width="400">
</picture>

<!-- <img src="docs/logo.png" alt="ProactiveAgent Logo" width="400"/> -->

**Time-awareness for your AI Agent**

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/proactiveagent)](https://pypi.org/project/proactiveagent/)
[![License](https://img.shields.io/badge/license-BSD--3--Clause-green.svg)](LICENSE)

*Transform your AI from reactive to proactive with intelligent timing and context-aware wake-up patterns*

[Quick Start](#quick-start) • [Documentation](https://leomariga.github.io/ProactiveAgent/) • [Examples](#examples)

</div>

## What is ProactiveAgent?

**ProactiveAgent** is an open-source Python library that packs any AI agents with intelligent **proactive behavior**. Unlike traditional agents that only respond when prompted, ProactiveAgent creates AI agents that can respond on their own. The agents are able to:

- **Decide when to speak** - Multi-factor decision engine determines *if* and *when* to respond
- **Sleep intelligently** - Dynamic timing system calculates the response intervals  
- **Understand context** - Analyzes conversation flow, user engagement, and urgency
- **Stay flexible** - Fully customizable decision engines and sleep calculators

<div align="center">
<img src="docs/flow_gif.gif"/>
</div>

## Quick Start

### Installation

```bash
pip install proactiveagent
```

### Basic Usage

```python
import time
from proactiveagent import ProactiveAgent, OpenAIProvider

# Create a proactive agent: Define in natural language the frequency of response
agent = ProactiveAgent(
    provider = OpenAIProvider(model="gpt-5-nano",),
    system_prompt = "You are a casual bored teenager. Answer like you're texting a friend",
    decision_config = {
        'wake_up_pattern': "Use the pace of a normal text chat",
    }
)

# Add response callback and start agent thread
def on_response(response: str): 
    print(f"🤖 AI: {response}")

agent.add_callback(on_response)
agent.start()
while True:
    message = input("You: ").strip()
    if message.lower() == 'quit': break
    agent.send_message(message)
    time.sleep(3)

agent.stop()
```

<div align="center">
<video src="https://github.com/user-attachments/assets/b7e724e0-9590-4f73-bb78-478bf2fa3540" width="800" loop>
</video>
</div>

## How It Works

ProactiveAgent operates on a **3-step decision cycle**:

<!-- Architecture diagram placeholder -->
<!-- <div align="center">
<img src="docs/architecture.png" alt="ProactiveAgent Architecture" width="800"/>
</div> -->

### 1. Decision Engine - "Should I Respond?"

Evaluates multiple factors to determine if the AI should respond:

- **Context Analysis**: Checks for questions, urgency keywords, and conversation flow
- **Timing**: Considers elapsed time since the last user message
- **AI Reasoning**: Uses native AI capabilities for intelligent decision-making
- **Engagement**: Monitors user activity patterns and conversation intensity

> We have other engines you can choose from and you can also define your own engine using our abstract base class. See the [Decision Engines](#decision-engines) section for details and examples. 

### 2. Message Generation - "Respond"

Generates appropriate responses considering conversation history and timing.

### 3. Sleep Calculator - "How Long Should I Wait?"

Determines the best wait time before the next decision cycle. Available options:

- **AI-Based** (default): Interprets natural language patterns like *"Respond like a normal chat"*
- **Pattern-Based**: Keyword matching for different conversation states  
- **Function-Based**: Custom timing functions
- **Static**: Fixed intervals

> You can also create your own SleepCalculator. See the [Sleep Calculators](#sleep-calculators) section for details and examples.

<!-- Flow diagram placeholder -->
<!-- <div align="center">
<img src="docs/decision-flow.png" alt="Decision Flow" width="600"/>
</div> -->

## Customization & Flexibility

### Decision Engines

Choose or create your own decision-making logic:

```python
from proactiveagent import DecisionEngine

# Your custom logic
class MyDecisionEngine(DecisionEngine):
    async def should_respond(self, messages, last_time, context, config, triggered_by_user):
        # Your custom decision logic here
        return should_respond, "reasoning"

agent = ProactiveAgent(provider=provider, decision_engine=MyDecisionEngine())
```

### Sleep Time Calculators

Control when your agent "wakes up" to make decisions:

```python
from proactiveagent import AIBasedSleepCalculator, StaticSleepCalculator

# Option 1 - AI interprets natural language patterns (default)
ai_calc = AIBasedSleepCalculator(provider)

# Option 2 - Fixed intervals
static_calc = StaticSleepCalculator(sleep_time=120)  # Every 2 minutes

# Option 3 - Your own custom adaptive logic
class SmartCalculator(SleepTimeCalculator):
    async def calculate_sleep_time(self, config, context):
        engagement = context.get('user_engagement', 'medium')
        if engagement == 'high':
            return 30, "High engagement - checking frequently"
        elif engagement == 'low':
            return 300, "Low engagement - checking less often"
        return 120, "Medium engagement - standard interval"

agent.scheduler.set_sleep_time_calculator(SmartCalculator())
```

### Real-Time Monitoring

Track your agent's behavior with callbacks:

```python
def on_response(response: str):
    print(f"Response: {response}")

def on_decision(should_respond: bool, reasoning: str):
    status = "RESPOND" if should_respond else "WAIT"
    print(f"Decision: {status} - {reasoning}")

def on_sleep_time(sleep_time: int, reasoning: str):
    print(f"Sleeping {sleep_time}s - {reasoning}")

# Register callbacks
agent.add_callback(on_response)
agent.add_decision_callback(on_decision)
agent.add_sleep_time_callback(on_sleep_time)
```

## Configuration Options

Fine-tune your agent's behavior with comprehensive configuration:

```python
agent = ProactiveAgent(
    provider=provider,
    decision_config={
        # Response timing bounds
        'min_response_interval': 30,      # Minimum seconds between responses
        'max_response_interval': 600,     # Maximum seconds before forced response
        'probability_weight': 0.3,        # AI decision weight
        
        # Sleep calculation
        'wake_up_pattern': "Check around 2-3 minutes when user is active",
        'min_sleep_time': 30,             # Minimum sleep seconds
        'max_sleep_time': 600,            # Maximum sleep seconds
    }
)
```
<!-- You can also add your own config parameters for you customized engines and calculator. See example TODO link -->
## Examples

Explore our examples in the [`examples/`](examples/) directory:

### Getting Started
- **[`minimal_chat.py`](examples/minimal_chat.py)** - Ultra-simple chat
- **[`minimal_callbacks.py`](examples/callbacks/minimal_callbacks.py)** - Minimal chat with thought process

### Decision Engines
- **[`ai_based_decision_engine.py`](examples/decision_engines/ai_based_decision_engine.py)** - AI-powered decisions
- **[`simple_decision_engine.py`](examples/decision_engines/simple_decision_engine.py)** - Time-based logic
- **[`custom_decision_engine.py`](examples/decision_engines/custom_decision_engine.py)** - Build your own

### Sleep Calculators
- **[`ai_based_sleep_calculator.py`](examples/sleep_calculators/ai_based_sleep_calculator.py)** - Natural language patterns
- **[`function_based_sleep_calculator.py`](examples/sleep_calculators/function_based_sleep_calculator.py)** - Adaptive timing
- **[`pattern_based_sleep_calculator.py`](examples/sleep_calculators/pattern_based_sleep_calculator.py)** - Keyword matching

### Monitoring & Callbacks
- **[`minimal_callbacks.py`](examples/callbacks/minimal_callbacks.py)** - Full callback system

### Configuration
- **[`all_config_parameters.py`](examples/configs/all_config_parameters.py)** - Complete configuration guide
## Advanced Features

### Context Management
```python
# Set conversation context
agent.set_context('user_mood', 'excited')
agent.set_context('topic_urgency', 'high')

# Context automatically influences decisions
mood = agent.get_context('user_mood')
```

### Runtime Configuration
```python
# Update configuration while running
agent.update_config({
    'min_response_interval': 5,  # Respond faster
    'engagement_threshold': 0.3   # Lower threshold
})
```

## Contributing

We welcome contributions! This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

**Quick setup:**
```bash
pip install uv
uv sync --dev  # Install dependencies including dev tools
```

Please see our [Contributing Guide](CONTRIBUTING.md) for detailed instructions.

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## Support

**Made with ❤️ by the internet**

Mainteiner: [Leonardo Mariga](https://github.com/leomariga) 
