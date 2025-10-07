import time
from proactiveagent import ProactiveAgent, OpenAIProvider

agent = ProactiveAgent(
    provider=OpenAIProvider(model="gpt-5-nano"),
    system_prompt="You are a casual young person which are bored and wants to talk in a WhatsApp chat. Use informal language, emojis, abbreviations, and speak like you're texting a friend. Keep responses short just a few words and conversational like real WhatsApp messages.",
    decision_config={
        'wake_up_pattern': "This is a normal whatsapp conversation, adapt your response frequency to the user's conversation.",
    },
)

agent.add_callback(lambda response: print(f"🤖 AI: {response}"))
agent.start()

print("Chat started! Type your messages:")

while True:
    message = input("You: ").strip()
    if message.lower() == 'quit': break
    agent.send_message(message)
    time.sleep(3)

agent.stop()
print("Chat ended!")
