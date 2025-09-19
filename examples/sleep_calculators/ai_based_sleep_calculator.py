"""
Minimal example using AIBasedSleepCalculator (default behavior)
"""
import time
from proactiveagent import ProactiveAgent, OpenAIProvider


def on_ai_response(response: str):
    print(f"🤖 AI: {response}")


def on_sleep_time_calculated(sleep_time: int, reasoning: str):
    print(f"⏰ Sleep: {sleep_time}s - {reasoning}")


def main():
    provider = OpenAIProvider(
        model="gpt-5-nano",
    )
    
    # AI-based sleep calculator is used by default
    agent = ProactiveAgent(
        provider=provider,
        system_prompt="You are a helpful AI assistant.",
        decision_config={
            'wake_up_pattern': "Check every 2-3 minutes when active",
            'min_sleep_time': 30,
            'max_sleep_time': 300,
        }
    )
    
    agent.add_callback(on_ai_response)
    agent.add_sleep_time_callback(on_sleep_time_calculated)
    agent.start()
    
    print("=== AI-Based Sleep Calculator ===")
    print("AI decides when to wake up based on context.")
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
