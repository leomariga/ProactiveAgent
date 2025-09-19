"""
Minimal example using SimpleDecisionEngine
"""
import time
from proactiveagent import ProactiveAgent, OpenAIProvider
from proactiveagent.decision_engines import SimpleDecisionEngine


def on_ai_response(response: str):
    print(f"🤖 AI: {response}")


def on_decision_made(should_respond: bool, reasoning: str):
    decision = "✅ RESPOND" if should_respond else "❌ WAIT"
    print(f"🧠 {decision}: {reasoning}")


def main():
    provider = OpenAIProvider(
        model="gpt-5-nano",
    )
    
    # Use simple time-based decision engine
    decision_engine = SimpleDecisionEngine()
    
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
    
    print("=== Simple Decision Engine ===")
    print("Uses simple time-based rules to decide when to respond.")
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
