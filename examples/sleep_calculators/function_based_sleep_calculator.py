"""
Minimal example using FunctionBasedSleepCalculator
"""
import time
from proactiveagent import ProactiveAgent, OpenAIProvider
from proactiveagent.sleep_time_calculators import FunctionBasedSleepCalculator


def on_ai_response(response: str):
    print(f"🤖 AI: {response}")


def on_sleep_time_calculated(sleep_time: int, reasoning: str):
    print(f"⏰ Sleep: {sleep_time}s - {reasoning}")


def custom_sleep_function(config, context):
    """Simple custom sleep calculation"""
    user_engagement = context.get('user_engagement', 'low')
    
    if user_engagement == 'high':
        return 60, "High engagement - check every minute"
    elif user_engagement == 'medium':
        return 120, "Medium engagement - check every 2 minutes"
    else:
        return 180, "Low engagement - check every 3 minutes"


def main():
    provider = OpenAIProvider(
        model="gpt-5-nano",
    )
    
    # Use custom sleep function
    sleep_calculator = FunctionBasedSleepCalculator(custom_sleep_function)
    
    agent = ProactiveAgent(
        provider=provider,
        system_prompt="You are a helpful AI assistant.",
        decision_config={
            'min_sleep_time': 30,
            'max_sleep_time': 300,
        }
    )
    
    # Override the default sleep calculator
    agent.scheduler.sleep_calculator = sleep_calculator
    
    agent.add_callback(on_ai_response)
    agent.add_sleep_time_callback(on_sleep_time_calculated)
    agent.start()
    
    print("=== Function-Based Sleep Calculator ===")
    print("Uses custom logic based on engagement level.")
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
