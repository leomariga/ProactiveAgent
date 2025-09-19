"""
Minimal example showing all configuration parameters
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


def main():
    provider = OpenAIProvider(
        model="gpt-5-nano",
    )
    
    # All configuration parameters
    agent = ProactiveAgent(
        provider=provider,
        system_prompt="You are a helpful AI assistant.",
        decision_config={
            # Response timing
            'min_response_interval': 30,
            'max_response_interval': 600,
            
            # Engagement thresholds  
            'engagement_threshold': 0.5,
            'engagement_high_threshold': 10,
            'engagement_medium_threshold': 3,
            
            # Decision weights
            'context_relevance_weight': 0.4,
            'time_weight': 0.3,
            'probability_weight': 0.3,
            
            # Sleep calculation
            'wake_up_pattern': "Check every 2-3 minutes when active",
            'min_sleep_time': 30,
            'max_sleep_time': 600,
        },
        log_level="INFO"
    )
    
    # All callback types
    agent.add_callback(on_ai_response)
    agent.add_sleep_time_callback(on_sleep_time_calculated)
    agent.add_decision_callback(on_decision_made)
    agent.start()
    
    print("=== All Configuration Parameters ===")
    print("Shows all available configuration options.")
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