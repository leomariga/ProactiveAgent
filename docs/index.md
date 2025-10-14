---
title: ProactiveAgent - Time-Aware AI Framework for Python
description: Open-source Python framework for building time-aware AI agents that proactively initiate conversations and make intelligent timing decisions. Transform reactive AI into proactive engagement.
keywords: proactive, active, proactive AI agents, time-aware AI, AI scheduling framework, autonomous conversation initiation, AI wake-up patterns, intelligent timing decisions, LLM lifecycle management, AI agent scheduler
---

# ProactiveAgent Documentation
<figure markdown="span">
![Logo](logo_b.png#only-dark){ width="400" }
</figure>
<figure markdown="span">
![Logo](logo.png#only-light){ width="400" }
</figure>
---

## What is ProactiveAgent?

**ProactiveAgent** is an open-source Python library that adds **time-awareness** to your AI agents. Unlike traditional agents that only respond when prompted, ProactiveAgent creates AI agents that can **decide when to speak** based on intelligent timing and context analysis.

Your agents become truly conversational - they understand when to follow up, when to wait, and when to initiate conversations naturally.

## Key Features

- **Intelligent Decision Making** - Multi-factor decision engines that determine when to respond
- **Smart Timing** - Dynamic sleep calculators that adapt to conversation patterns
- **Fully Customizable** - Mix and match decision engines and sleep calculators
- **Production Ready** - Robust, tested, and ready for real-world applications
- **Easy Integration** - Simple API that works with any LLM provider


### How It Works

<img src="flow_gif.gif"/>

**The 3-Step Decision Cycle**: Wake → Decide → Respond → Sleep

## Quick Start

Get up and running in minutes:

### Installation

```bash
pip install proactiveagent
```

### Basic Usage

```python
import time
from proactiveagent import ProactiveAgent, OpenAIProvider

# Create a proactive agent
agent = ProactiveAgent(
    provider = OpenAIProvider(model="gpt-5-nano",),
    system_prompt = "You are a casual bored teenager. Answer like you're texting a friend",
    decision_config = {
        'wake_up_pattern': "Use the pace of a normal text chat",
    }
)

# Add response callback
agent.add_callback(lambda response: print(f"AI: {response}"))

agent.start()

# Chat with your proactive agent
while True:
    message = input("You: ").strip()
    if message.lower() == 'quit':
        break
    agent.send_message(message)
    time.sleep(1)

agent.stop()
```

**That's it!** Your agent now has intelligent timing and will respond naturally based on the conversation flow.




## Demo

<div align="center">
<video src="https://github.com/user-attachments/assets/b7e724e0-9590-4f73-bb78-478bf2fa3540" width="800" loop controls>
  <p>Your browser does not support the video tag.</p>
</video>
</div>

## Advanced Features

- **Runtime Configuration Updates** - Modify agent parameters dynamically without restarting
- **Comprehensive Monitoring** - Observe decision-making processes and timing patterns through callback mechanisms
- **Context Management System** - Programmatically manage conversation state and metadata
- **Provider-Agnostic Architecture** - Compatible with multiple LLM providers including OpenAI, Anthropic, and local models
- **Asynchronous Operations** - Native async/await support for high-performance concurrent applications

---

## Documentation

Ready to dive deeper? Check out our comprehensive documentation:

- **[Getting Started](getting-started.md)** - Complete guide with detailed examples
- **[Examples](examples.md)** - Code examples for different use cases
- **[API Reference](api-reference.md)** - Complete API documentation

## Contributing

We welcome contributions! Help us make ProactiveAgent even better:

- **Bug Reports** - [GitHub Issues](https://github.com/leomariga/ProactiveAgent/issues)
- **Feature Requests** - [GitHub Discussions](https://github.com/leomariga/ProactiveAgent/discussions)
- **Code Contributions** - [Contributing Guide](https://github.com/leomariga/ProactiveAgent/blob/main/CONTRIBUTING.md)

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](https://github.com/leomariga/ProactiveAgent/blob/main/LICENSE) file for details.

---

**Made by the community**

[Star on GitHub](https://github.com/leomariga/ProactiveAgent) •
[Report Issues](https://github.com/leomariga/ProactiveAgent/issues) •
[Read the Docs](https://leomariga.github.io/ProactiveAgent/)

**Maintained by [Leonardo Mariga](https://github.com/leomariga)**

