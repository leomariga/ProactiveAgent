"""
Minimal example using PatternBasedSleepCalculator
"""
import time
from proactiveagent import ProactiveAgent, OpenAIProvider
from proactiveagent.sleep_time_calculators import PatternBasedSleepCalculator


def on_ai_response(response: str):
    print(f"🤖 AI: {response}")


def on_sleep_time_calculated(sleep_time: int, reasoning: str):
    print(f"⏰ Sleep: {sleep_time}s - {reasoning}")


def main():
    provider = OpenAIProvider(
        model="gpt-5-nano",
    )
    
    # Configure pattern mappings
    patterns = {
        'urgent': 30,
        'active': 60,
        'normal': 120,
        'slow': 180,
        'default': 120
    }
    sleep_calculator = PatternBasedSleepCalculator(patterns)
    
    agent = ProactiveAgent(
        provider=provider,
        system_prompt="You are a helpful AI assistant.",
        decision_config={
            'wake_up_pattern': "Monitor conversation with normal frequency",
            'min_sleep_time': 30,
            'max_sleep_time': 300,
        }
    )
    
    # Override the default sleep calculator
    agent.scheduler.sleep_calculator = sleep_calculator
    
    agent.add_callback(on_ai_response)
    agent.add_sleep_time_callback(on_sleep_time_calculated)
    agent.start()
    
    print("=== Pattern-Based Sleep Calculator ===")
    print("Analyzes wake_up_pattern keywords for timing.")
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
