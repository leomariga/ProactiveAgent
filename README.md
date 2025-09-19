# Proactive AI Agents

A Python library for creating proactive AI agents that actively engage users instead of waiting for input. The agents use configurable wake-up patterns and intelligent decision-making to determine when and how to respond.

## Features

- **Proactive Communication**: AI agents actively initiate conversations
- **Configurable Wake-up Patterns**: Define custom timing patterns for agent activity
- **Time-Aware Responses**: Agents receive elapsed time information for contextual decisions
- **Multi-Provider Support**: Extensible architecture (currently supports OpenAI)
- **Thread-Based Operation**: Non-blocking execution in separate threads
- **Callback System**: Flexible response handling through user-defined callbacks

## Installation

```bash
pip install proactive-agent
```

## Super Simple Example

**Just 10 lines to get started:**

```python
from proactiveagent import ProactiveAgent, OpenAIProvider
import time

# Create provider and agent
provider = OpenAIProvider(api_key="your-openai-api-key-here")
agent = ProactiveAgent(provider, max_sleep_time="30 seconds")

# Add response handler and start
agent.add_callback(lambda response: print(f"AI: {response}"))
agent.start()

# Send message and wait for proactive response
agent.send_message("Hello! Tell me about AI agents.")
time.sleep(5)  # Wait for AI response

agent.stop()
```

**Interactive chat:**

```python
from proactiveagent import ProactiveAgent, OpenAIProvider
import time

def on_ai_response(response: str):
    print(f"🤖 AI: {response}")

# Setup
provider = OpenAIProvider(api_key="your-openai-api-key-here")
agent = ProactiveAgent(provider, max_sleep_time="1 minute")
agent.add_callback(on_ai_response)
agent.start()

# Chat loop
while True:
    message = input("You: ").strip()
    if message.lower() == 'quit': break
    agent.send_message(message)
    time.sleep(3)  # Wait for response

agent.stop()
```

## Quick Start

```python
import os
from proactiveagent import ProactiveAgent, OpenAIProvider

# Initialize provider with your API key
provider = OpenAIProvider(
    model="gpt-3.5-turbo",
    api_key="your_openai_api_key_here",  # Replace with your actual API key
    temperature=0.7,
    max_tokens=150
)

# Create agent with custom configuration
agent = ProactiveAgent(
    provider=provider,
    wake_up_pattern="Check every 2-5 minutes if user seems busy, every 30 seconds if engaged",
    max_sleep_time="10 minutes",
    callbacks=[lambda response: print(f"AI: {response}")],
    log_level="INFO"
)

# Start the agent
agent.start()

# Send a message to begin conversation
agent.send_message("Hello! How are you today?")

# The agent will now actively participate in the conversation
# Stop when done
agent.stop()
```

## Configuration

You can set your OpenAI API key in several ways:

**Option 1: Direct in code (simple)**
```python
provider = OpenAIProvider(
    model="gpt-3.5-turbo",
    api_key="your_actual_api_key_here"
)
```

**Option 2: Environment variable**
```python
import os
provider = OpenAIProvider(
    model="gpt-3.5-turbo",
    api_key=os.getenv('OPENAI_API_KEY')
)
```

**Option 3: System environment variable**
```bash
# On Windows
set OPENAI_API_KEY=your_openai_api_key_here

# On macOS/Linux
export OPENAI_API_KEY=your_openai_api_key_here
```

## API Reference

### ProactiveAgent

Main class for creating proactive AI agents.

#### Parameters

- `provider`: AI provider instance (e.g., OpenAIProvider)
- `wake_up_pattern`: Description of when agent should wake up
- `max_sleep_time`: Maximum time to sleep between wake-ups (int seconds or string like "10 minutes")
- `callbacks`: List of callback functions for receiving responses
- `decision_config`: Optional configuration dict for decision engine behavior
- `system_prompt`: Optional system prompt for the AI
- `log_level`: Logging level (DEBUG, INFO, WARNING, ERROR)

#### Methods

- `start()`: Start the agent in a separate thread
- `stop()`: Stop the agent
- `send_message(message, role="user")`: Send a message to the conversation
- `add_callback(callback)`: Add a response callback function
- `update_wake_up_pattern(pattern)`: Update the wake-up pattern
- `get_conversation_history()`: Get full conversation history

### OpenAIProvider

OpenAI implementation of the AI provider interface.

#### Parameters

- `model`: OpenAI model name (default: "gpt-3.5-turbo")
- `api_key`: OpenAI API key (optional, can be set via environment)
- `temperature`: Response randomness (default: 0.7)
- `max_tokens`: Maximum response length (default: 150)

## Wake-up Patterns

You can define custom wake-up patterns using natural language:

```python
# Examples
agent.update_wake_up_pattern("Check every 30 seconds if user is active")
agent.update_wake_up_pattern("Respond quickly during business hours, slower in evening")
agent.update_wake_up_pattern("Be more active if conversation involves urgent topics")
```

## Callbacks

Define custom callback functions to handle AI responses:

```python
def log_response(response):
    print(f"[{time.time()}] AI: {response}")

def save_to_file(response):
    with open("conversation.txt", "a") as f:
        f.write(f"AI: {response}\n")

agent = ProactiveAgent(
    provider=provider,
    callbacks=[log_response, save_to_file]
)
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.