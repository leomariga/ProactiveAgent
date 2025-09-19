"""
Minimal example of custom sleep calculator
"""
import time
from typing import Dict, Any
from proactiveagent import ProactiveAgent, OpenAIProvider
from proactiveagent.sleep_time_calculators import SleepTimeCalculator


class MyCustomSleepCalculator(SleepTimeCalculator):
    """Simple custom sleep calculator"""
    
    async def calculate_sleep_time(self, config: Dict[str, Any], context: Dict[str, Any]) -> tuple[int, str]:
        # Simple logic: sleep longer at night, shorter during day
        hour = time.localtime().tm_hour
        
        if 9 <= hour <= 17:  # Business hours
            return 60, "Daytime - check every minute"
        else:  # Off hours
            return 180, "Nighttime - check every 3 minutes"


def on_ai_response(response: str):
    print(f"🤖 AI: {response}")


def on_sleep_time_calculated(sleep_time: int, reasoning: str):
    print(f"⏰ Sleep: {sleep_time}s - {reasoning}")


def main():
    provider = OpenAIProvider(
        model="gpt-5-nano",
    )
    
    # Use custom sleep calculator
    custom_calculator = MyCustomSleepCalculator()
    
    agent = ProactiveAgent(
        provider=provider,
        system_prompt="You are a helpful AI assistant.",
        decision_config={
            'min_sleep_time': 30,
            'max_sleep_time': 300,
        }
    )
    
    # Replace default calculator
    agent.scheduler.sleep_calculator = custom_calculator
    
    agent.add_callback(on_ai_response)
    agent.add_sleep_time_callback(on_sleep_time_calculated)
    agent.start()
    
    print("=== Custom Sleep Calculator ===")
    print("Uses time of day to determine sleep intervals.")
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
