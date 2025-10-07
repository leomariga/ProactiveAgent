"""
Minimal callbacks example - response, sleep, and decision callbacks
"""
import time
from proactiveagent import ProactiveAgent, OpenAIProvider


def on_response(response: str):
    """Called when AI sends a response"""
    print(f"🤖 AI: {response}")


def on_sleep(sleep_time: int, reasoning: str):
    """Called when AI calculates sleep time"""
    print(f"⏰ Sleep: {sleep_time}s - {reasoning}")


def on_decision(should_respond: bool, reasoning: str):
    """Called when AI makes a decision about whether to respond"""
    status = "RESPOND" if should_respond else "WAIT"
    print(f"🧠 {status} - {reasoning}")


agent = ProactiveAgent(
    provider=OpenAIProvider(model="gpt-5-nano"),
    system_prompt="You are a casual young person which are bored and wants to talk in a WhatsApp chat. Use informal language, emojis, abbreviations, and speak like you're texting a friend. Keep responses short just a few words and conversational like real WhatsApp messages.",
    decision_config={
        'wake_up_pattern': "This is a normal whatsapp conversation, adapt your response frequency to the user's conversation.",
    },
)

agent.add_callback(on_response)
agent.add_sleep_time_callback(on_sleep)
agent.add_decision_callback(on_decision)

agent.start()

print("Chat started! Type your messages:")

while True:
    message = input("You: ").strip()
    if message.lower() == 'quit': break
    agent.send_message(message)
    time.sleep(3)

agent.stop()
print("Chat ended!")
