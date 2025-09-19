"""
Minimal example using FunctionBasedDecisionEngine
"""
import time
from proactiveagent import ProactiveAgent, OpenAIProvider
from proactiveagent.decision_engines import FunctionBasedDecisionEngine


def on_ai_response(response: str):
    print(f"🤖 AI: {response}")


def on_decision_made(should_respond: bool, reasoning: str):
    decision = "✅ RESPOND" if should_respond else "❌ WAIT"
    print(f"🧠 {decision}: {reasoning}")


def custom_decision_function(messages, last_user_message_time, context, config, triggered_by_user_message):
    """Simple custom decision logic"""
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


def main():
    provider = OpenAIProvider(
        model="gpt-5-nano",
    )
    
    # Use custom decision function
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
    
    agent.add_callback(on_ai_response)
    agent.add_decision_callback(on_decision_made)
    agent.start()
    
    print("=== Function-Based Decision Engine ===")
    print("Uses custom function to decide when to respond.")
    print("Type 'quit' to exit.\n")
    
    try:
        while True:
            message = input("You: ").strip()
            if message.lower() == 'quit':
                break
            agent.send_message(message)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        agent.stop()


if __name__ == "__main__":
    main()
