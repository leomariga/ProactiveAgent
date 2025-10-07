*Large language models are reactive by default - they only respond when prompted. But what if your AI could initiate conversations, follow up on its own, and maintain engagement over time?*

## **The Problem That Motivated This Work**

Consider a typical scenario: you build a **Slack bot** that performs brilliantly during a demo, with users praising its human-like conversational abilities. But *24 hours later*, the conversation dies because the bot never initiates follow-ups or checks back in unless explicitly prompted.

This is the core issue with large language models - they're inherently ***reactive***. They wait for input rather than taking initiative. The challenge lies in embedding a time-based layer that gives agents temporal awareness - knowing not just *what* to say, but ***when*** to say it. In real-world applications, however, we need agents that can remember to follow up, initiate conversations, and maintain engagement over time.

Development teams have tried various workarounds:
- Scheduled cron jobs that often result in unwanted spam
- Aggressive polling that consumes excessive API resources
- Complex webhook architectures that become fragile when any component fails

None of these approaches felt like the right solution. This led me to explore a different approach: **what if we gave agents an internal sense of time and basic decision-making capabilities?**

## **The ProactiveAgent Library**

After experimenting a little bit I came up with:

**ProactiveAgent** - an open-source *Python framework* that adds time-awareness to large language models agents. It's built around a simple but effective loop: 

**wake → decide → respond → sleep**.

Here's the conceptual flow:


![ProactiveAgent flow](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/f2zy2bmnxsbu56wrthyr.png)

The agent wakes up according to a schedule, evaluates the conversation context, determines whether a response is appropriate, and generates one if needed. It then calculates an optimal sleep duration before the next cycle. *All components are designed to be interchangeable* - you can swap decision engines and sleep calculators without modifying your core application.

I intentionally kept the underlying implementation straightforward. *Simple, predictable code is much easier to debug during late-night troubleshooting sessions.*

### **Core Components**

- ***Agent***: The main orchestrator that manages the execution loop
- ***Decision Engines***: Components that determine response appropriateness *(if it should respond now)*
- ***Sleep Calculators***: Algorithms that determine optimal intervals between checks
- ***Providers***: Abstractions for different LLM APIs *(including OpenAI)*
- ***Callbacks***: Monitoring hooks for observing agent behavior and decisions

## **Building Your First Agent**

Let's move from theory to practice. Here's how to create a WhatsApp-style chatbot that maintains conversations proactively.

### **Installation**

```bash
pip install proactiveagent
```

### **Creating Your First Agent**

```python
import time
from proactiveagent import ProactiveAgent, OpenAIProvider

agent = ProactiveAgent(
    provider=OpenAIProvider(model="gpt-5-nano"),
    system_prompt="You are a casual young person which are bored and wants to talk in a WhatsApp chat. Use informal language, emojis, abbreviations, and speak like you're texting a friend. Keep responses short just a few words and conversational like real WhatsApp messages.",
    decision_config={
        'wake_up_pattern': "This is a normal whatsapp conversation, adapt your response frequency to the user's conversation.",
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

Your agent will now operate on a schedule, periodically evaluating whether to respond and maintaining natural conversation flow.

## **Understanding the Agent's Thought Process**

Want to see what's happening inside your agent's *"mind"*? You can add callbacks to observe the decision-making process in real-time:

```python
"""
Minimal callbacks example - response, sleep, and decision callbacks
"""
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
    system_prompt="You are a casual young person which are bored and wants to talk in a WhatsApp chat. Use informal language, emojis, abbreviations, and speak like you're texting a friend. Keep responses short just a few words and conversational like real WhatsApp messages.",
    decision_config={
        'wake_up_pattern': "This is a normal whatsapp conversation, adapt your response frequency to the user's conversation.",
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

This reveals the agent's internal reasoning - you'll see exactly why it chose to respond (or stay silent) and how it determined its sleep duration. It's like watching the agent think through its decisions.

## **Decision Engines**

The library's real flexibility comes from its *interchangeable decision engines*. Here are the available approaches:

- ***AI-based***: Let the model evaluate context and decide timing *(default)*
- ***Threshold***: Priority-based timing with different response times for different message types
- ***Function-based***: Custom logic using Python functions *(demonstrated below)*

Here's how to use a function-based decision engine with custom logic:

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

AI-powered decisions work surprisingly well as the default because large language models are excellent at evaluating conversation relevance and engagement levels. They can assess whether a response would be valuable, consider the user's current context and emotional state, and determine if the timing aligns with the conversation's natural flow - judgments that are difficult to codify in simple rules. This leads to more meaningful and contextually appropriate interventions.

## **Sleep Calculators**

Sleep calculators control the timing between agent wake cycles. By default, the agent lets the AI decide when to wake up based on context and conversation flow - this provides the most natural timing but can be less predictable in terms of cost and performance.

The library offers several approaches for when you need more control:

- ***AI-based***: Let the model decide timing based on context *(default)*
- ***Static***: Fixed intervals regardless of context
- ***Pattern-based***: Adjust timing based on conversation keywords
- ***Function-based***: Custom logic using Python functions

Here's a complete example using a static sleep calculator with fixed 2-minute intervals:

```python
"""
Minimal example using StaticSleepCalculator
"""
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

The rationale for the AI-based default is that LLMs are surprisingly good at understanding conversation rhythm and context. They can detect when a conversation is heating up, cooling down, or when it's an appropriate time to check back in. But feel free to use any other you want.


## **Configuration Management**

This example demonstrates key configuration options, though there are many more available. For comprehensive examples exploring all parameters, check the [`examples/configs/`](https://github.com/leomariga/ProactiveAgent/tree/main/examples/configs) directory on GitHub.

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

## **Key Lessons and Considerations**

### **Advantages:**
- Rule-based engines *(thresholds, functions)* offer predictable costs and behavior
- Start with longer sleep intervals when idle, then reduce timing after user engagement
- Comprehensive logging helps identify unusual decision patterns early

### **Important Considerations:**
- Some might characterize this as *"pseudo-proactive"* since scheduled wakeups still trigger model calls. This is a fair critique, but it represents a pragmatic approach given current LLM limitations.
- Token efficiency is crucial: maintain lean prompts and avoid redundant context
- Model drift occurs over time - strategies that work initially may need adjustment

### **When to Avoid This Approach:**
- Purely static workloads are better served by traditional cron jobs
- Long-running I/O operations typically require external orchestration systems
- Applications requiring absolute reliability *(models can occasionally be inconsistent)*

## **Future Development Plans**

I'm planning several enhancements:
- Support for additional LLM providers *(Anthropic, local models)*
- Improved conversation memory and persistence mechanisms

## **Links**
- ***Repository***: [leomariga/ProactiveAgent](https://github.com/leomariga/ProactiveAgent)
- ***Package***: [proactiveagent](https://pypi.org/project/proactiveagent/)

**Thanks for reading!** The library is intentionally *lightweight*, but achieving reliable proactive behavior with LLMs presents interesting technical challenges. If you've encountered similar issues in your own work, I'd love to hear about your solutions.

Feel free to reach out with questions, suggestions, or just to share your experiences building proactive AI agents. *Let's continue pushing the boundaries of what's possible with conversational AI!*
