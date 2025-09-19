"""
Minimal example showing all callback types
"""
import time
from proactiveagent import ProactiveAgent, OpenAIProvider


def on_ai_response(response: str):
    print(f"🤖 AI: {response}")


def on_sleep_time_calculated(sleep_time: int, reasoning: str):
    print(f"⏰ Sleep: {sleep_time}s - {reasoning}")


def on_decision_made(should_respond: bool, reasoning: str):
    decision = "✅ RESPOND" if should_respond else "❌ WAIT"
    print(f"🧠 {decision}: {reasoning}")


# Additional callback examples
def response_logger(response: str):
    print(f"📝 Logged: {len(response)} characters")


def sleep_monitor(sleep_time: int, reasoning: str):
    urgency = "🔥" if sleep_time < 60 else "😴"
    print(f"{urgency} Timing: {sleep_time}s")


def decision_tracker(should_respond: bool, reasoning: str):
    print(f"📊 Decision tracked: {should_respond}")


def main():
    provider = OpenAIProvider(
        model="gpt-5-nano",
    )
    
    agent = ProactiveAgent(
        provider=provider,
        system_prompt="You are a helpful AI assistant.",
        decision_config={
            'min_response_interval': 30,
            'max_response_interval': 300,
        }
    )
    
    # Add multiple callbacks of each type
    agent.add_callback(on_ai_response)
    agent.add_callback(response_logger)
    
    agent.add_sleep_time_callback(on_sleep_time_calculated)
    agent.add_sleep_time_callback(sleep_monitor)
    
    agent.add_decision_callback(on_decision_made)
    agent.add_decision_callback(decision_tracker)
    
    agent.start()
    
    print("=== Multiple Callbacks Example ===")
    print("Shows how to use multiple callbacks for monitoring.")
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