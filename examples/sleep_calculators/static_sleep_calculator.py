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
    provider = OpenAIProvider(
        model="gpt-5-nano",
    )
    
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