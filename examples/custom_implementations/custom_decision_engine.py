"""
Minimal example of custom decision engine
"""
import time
from typing import List, Dict, Any
from proactiveagent import ProactiveAgent, OpenAIProvider
from proactiveagent.decision_engines import DecisionEngine


class MyCustomDecisionEngine(DecisionEngine):
    """Simple custom decision engine"""
    
    async def should_respond(
        self,
        messages: List[Dict[str, str]],
        last_user_message_time: float,
        context: Dict[str, Any],
        config: Dict[str, Any],
        triggered_by_user_message: bool = False
    ) -> tuple[bool, str]:
        # Simple logic: respond to questions immediately, otherwise wait
        if triggered_by_user_message:
            recent_content = messages[-1].get('content', '').lower() if messages else ''
            if '?' in recent_content:
                return True, "Question detected - immediate response"
            else:
                return True, "New user message - respond"
        
        # For periodic checks, wait at least 2 minutes
        elapsed = int(time.time() - last_user_message_time)
        if elapsed > 120:
            return True, f"Been quiet for {elapsed}s - time to respond"
        
        return False, f"Wait {120 - elapsed}s more"


def on_ai_response(response: str):
    print(f"🤖 AI: {response}")


def on_decision_made(should_respond: bool, reasoning: str):
    decision = "✅ RESPOND" if should_respond else "❌ WAIT"
    print(f"🧠 {decision}: {reasoning}")


def main():
    provider = OpenAIProvider(
        model="gpt-5-nano",
    )
    
    # Use custom decision engine
    custom_engine = MyCustomDecisionEngine()
    
    agent = ProactiveAgent(
        provider=provider,
        decision_engine=custom_engine,
        system_prompt="You are a helpful AI assistant.",
        decision_config={
            'min_response_interval': 30,
            'max_response_interval': 300,
        }
    )
    
    agent.add_callback(on_ai_response)
    agent.add_decision_callback(on_decision_made)
    agent.start()
    
    print("=== Custom Decision Engine ===")
    print("Responds immediately to questions, waits 2 minutes otherwise.")
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
