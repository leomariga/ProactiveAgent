"""
Minimal example using ThresholdDecisionEngine
"""
import time
from proactiveagent import ProactiveAgent, OpenAIProvider
from proactiveagent.decision_engines import ThresholdDecisionEngine


def on_ai_response(response: str):
    print(f"🤖 AI: {response}")


def on_decision_made(should_respond: bool, reasoning: str):
    decision = "✅ RESPOND" if should_respond else "❌ WAIT"
    print(f"🧠 {decision}: {reasoning}")


def main():
    provider = OpenAIProvider(
        model="gpt-5-nano",
    )
    
    # Configure threshold-based decision engine
    thresholds = {
        'urgent': 30,
        'high': 60,
        'medium': 120,
        'normal': 180,
        'default': 120
    }
    decision_engine = ThresholdDecisionEngine(thresholds)
    
    agent = ProactiveAgent(
        provider=provider,
        decision_engine=decision_engine,
        system_prompt="You are a helpful AI assistant.",
        decision_config={
            'min_response_interval': 30,
            'max_response_interval': 300,
        }
    )
    
    agent.add_callback(on_ai_response)
    agent.add_decision_callback(on_decision_made)
    agent.start()
    
    print("=== Threshold Decision Engine ===")
    print("Uses priority thresholds to decide response timing.")
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
