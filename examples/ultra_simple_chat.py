"""
Ultra-simple synchronous chat example
"""
import time
from proactiveagent import ProactiveAgent, OpenAIProvider


def on_ai_response(response: str):
    """Called when AI sends a response"""
    print(f"🤖 AI: {response}")


def on_sleep_time_calculated(sleep_time: int, reasoning: str):
    """Called when AI calculates sleep time"""
    print(f"⏰ Sleep time: {sleep_time}s - {reasoning}")


def on_decision_made(should_respond: bool, reasoning: str):
    """Called when AI makes a decision about whether to respond"""
    decision = "✅ RESPOND" if should_respond else "❌ NO RESPONSE"
    print(f"🧠 Decision: {decision} - {reasoning}")


def main():
    # 1. Create provider with your OpenAI API key
    provider = OpenAIProvider(
        model="gpt-5-nano",
    )
    
    # 2. Create agent with simple settings
    agent = ProactiveAgent(
        provider=provider,
        system_prompt="You are a casual young person which are bored and wants to talk in a WhatsApp chat. Use informal language, emojis, abbreviations, and speak like you're texting a friend. Keep responses short just a few words and conversational like real WhatsApp messages.",
        decision_config={
            'wake_up_pattern': "This is a normal whatsapp conversation, adapt your response frequency to the user's conversation.",
        },
        #log_level="DEBUG"  # Enable debug logging to see what's happening
    )
    
    # 3. Add callbacks to handle AI responses and sleep time calculations
    agent.add_callback(on_ai_response)
    agent.add_sleep_time_callback(on_sleep_time_calculated)
    agent.add_decision_callback(on_decision_made)
    
    # 4. Start the agent
    agent.start()
    
    print("Chat started! Type your messages:")
    
    try:
        while True:
            # Get user input
            message = input("You: ").strip()
            
            if message.lower() == 'quit':
                break
                
            # Send to AI
            agent.send_message(message)
            
            # Wait a bit for AI response
            time.sleep(3)
    
    except KeyboardInterrupt:
        pass
    finally:
        agent.stop()
        print("Chat ended!")


if __name__ == "__main__":
    main()