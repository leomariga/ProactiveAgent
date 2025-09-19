# ProactiveAgent

<div align="center">

<!-- Logo placeholder -->
<img src="docs/logo.png" alt="ProactiveAgent Logo" width="200"/>

**Time-awareness for your AI Agent**

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/proactiveagent)](https://pypi.org/project/proactiveagent/)
[![License](https://img.shields.io/badge/license-BSD--3--Clause-green.svg)](LICENSE)

*Transform your AI from reactive to proactive with intelligent timing and context-aware wake-up patterns*

[Quick Start](#quick-start) • [Documentation](#documentation) • [Examples](#examples) • [Architecture](#architecture)

</div>

## What is ProactiveAgent?

**ProactiveAgent** is an open-source Python library that wraps AI models with intelligent **proactive behavior**. Unlike traditional agents that only respond when prompted, ProactiveAgent creates AI agents that:

- **Think before speaking** - Multi-factor decision engine determines *if* and *when* to respond
- **Sleep intelligently** - Dynamic timing system calculates smart response intervals  
- **Understand context** - Analyzes conversation flow, user engagement, and urgency
- **Stay flexible** - Fully customizable decision engines and sleep calculators

<!-- Demo GIF placeholder -->
<div align="center">
<img src="docs/demo.gif" alt="ProactiveAgent Demo" width="600"/>
</div>

## Quick Start

### Installation

```bash
pip install proactiveagent
```

### Basic Usage

```python
from proactiveagent import ProactiveAgent, OpenAIProvider

# Create a proactive agent
agent = ProactiveAgent(
    provider=OpenAIProvider(model="gpt-5-nano",),
    system_prompt="You are a casual bored teenager. Answer like you're texting a friend",

    # Define in natural language the frequency of response
    decision_config={
        'wake_up_pattern': "Use the pace of a normal text chat",
    }
)

# Add response callback
def on_response(response: str):
    print(f"🤖 AI: {response}")

agent.add_callback(on_response)


# Start the agent thread and chat
agent.start()
agent.send_message("Hey! whatsup?")
# You can add a loop to keep sending the agent more messages! see our examples.
```

## How It Works

ProactiveAgent operates on a **3-step decision cycle**:

<!-- Architecture diagram placeholder -->
<div align="center">
<img src="docs/architecture.png" alt="ProactiveAgent Architecture" width="800"/>
</div>

### 1. Decision Engine - "Should I Respond?"

The **Decision Engine** analyzes multiple factors to determine if the AI should respond. Our default engine:

- **Context Analysis**: Evaluates questions, urgency keywords, and conversation flow
- **Time Factors**: Considers elapsed time since the last user message
- **AI Reasoning**: Leverages native AI decision-making capabilities
- **Engagement Level**: Monitors user activity patterns and conversation intensity

We have other engines that you can choose TODO LINK. You can also define your own Engine like using our abstract class TODO LINK. (essa frase pode ficar com um design diferente no readme)
**TODO: See Multi-Factor Scoring for more info**:


### 2. Message Generation - "Respond"

When the decision engine determines a response is appropriate, the agent:
- Generates contextually appropriate responses
- Considers conversation history and timing
- Maintains natural conversation flow
- Triggers all registered response callbacks

### 3. Sleep Calculator - "How Long Should I Wait?"

Finally, the **Sleep Calculator** determines optimal wait time before the next decision cycle. There are different Sleep Calculator available, for example:

- **AI-Based** (default): Uses AI to interpret natural language patterns like *"Respond in a frequency of a normal internet chat"* or *"You are a anxious person"*
- **Pattern-Based**: Keyword matching for different conversation states
- **Function-Based**: Define your own function for adaptive timing
- **Static**: Fixed intervals for predictable behavior

You can also create your own SleepCalculator TODO LINK

<!-- Flow diagram placeholder -->
<div align="center">
<img src="docs/decision-flow.png" alt="Decision Flow" width="600"/>
</div>

## Customization & Flexibility

### Decision Engines

Choose or create your own decision-making logic:

```python
from proactiveagent import AIBasedDecisionEngine, SimpleDecisionEngine

# Option 1 - AI-powered decisions (default)
ai_engine = AIBasedDecisionEngine(provider)

# Option 2 - Simple time-based decisions
simple_engine = SimpleDecisionEngine()

# Option 3 - Your custom logic
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
You can also add your own config parameters for you customized engines and calculator. See example TODO link
## Examples

Explore our examples in the [`examples/`](examples/) directory:

### Getting Started
- **[`ultra_simple_chat.py`](examples/ultra_simple_chat.py)** - Minimal WhatsApp-style chat
- **[`all_config_parameters.py`](examples/configs/all_config_parameters.py)** - Complete configuration guide

### Decision Engines
- **[`ai_based_decision_engine.py`](examples/decision_engines/ai_based_decision_engine.py)** - AI-powered decisions
- **[`simple_decision_engine.py`](examples/decision_engines/simple_decision_engine.py)** - Time-based logic
- **[`custom_decision_engine.py`](examples/decision_engines/custom_decision_engine.py)** - Build your own

### Sleep Calculators
- **[`ai_based_sleep_calculator.py`](examples/sleep_calculators/ai_based_sleep_calculator.py)** - Natural language patterns
- **[`function_based_sleep_calculator.py`](examples/sleep_calculators/function_based_sleep_calculator.py)** - Adaptive timing
- **[`pattern_based_sleep_calculator.py`](examples/sleep_calculators/pattern_based_sleep_calculator.py)** - Keyword matching

### Monitoring & Callbacks
- **[`comprehensive_callbacks.py`](examples/callbacks/comprehensive_callbacks.py)** - Full callback system

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

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## Support

- **Star this repo** if ProactiveAgent helps your project!

<div align="center">

**Made with ❤️ by the internet**

Mainteiner: [Leonardo Mariga](https://github.com/leomariga) 

</div>
