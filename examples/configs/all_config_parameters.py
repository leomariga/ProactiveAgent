"""
Minimal example showing all configuration parameters
"""
import time
from proactiveagent import ProactiveAgent, OpenAIProvider


def on_ai_response(response: str):
    """Callback triggered when the AI generates a response."""
    print(f"🤖 AI: {response}")


def on_sleep_time_calculated(sleep_time: int, reasoning: str):
    """Callback triggered when the agent calculates how long to sleep."""
    print(f"⏰ Sleep: {sleep_time}s - {reasoning}")


def on_decision_made(should_respond: bool, reasoning: str):
    """Callback triggered when the agent makes a decision about whether to respond."""
    decision = "✅ RESPOND" if should_respond else "❌ WAIT"
    print(f"🧠 {decision}: {reasoning}")


def main():
    # Initialize the AI provider - this determines which AI model to use
    provider = OpenAIProvider(
        model="gpt-5-nano",  # The AI model to use for generating responses
    )
    
    # Create ProactiveAgent with all available configuration parameters
    agent = ProactiveAgent(
        # Core configuration
        provider=provider,  # The AI provider instance (required)
        system_prompt="You are a helpful AI assistant.",  # Instructions for the AI's behavior
        
        # Decision configuration - controls when and how the agent decides to respond
        decision_config={
            # === RESPONSE TIMING PARAMETERS ===
            # These control the minimum and maximum time between responses
            'min_response_interval': 30,  # Minimum seconds between responses (prevents spam)
            'max_response_interval': 600,  # Maximum seconds between responses (prevents abandonment)
            
            # === ENGAGEMENT THRESHOLD PARAMETERS ===
            # These control the final decision threshold and engagement level calculation
            'engagement_threshold': 0.5,  # Final decision threshold (0.0-1.0) - combined score must exceed this to respond
            'engagement_high_threshold': 10,  # User messages ≥10 in last hour = "high" engagement level
            'engagement_medium_threshold': 3,  # User messages ≥3 in last hour = "medium" engagement level
            
            # === DECISION WEIGHT PARAMETERS ===
            # These weights combine three factors into a final decision score (must sum to 1.0)
            'context_relevance_weight': 0.4,  # Weight for context factors (questions, urgency, follow-up needs)
            'time_weight': 0.3,  # Weight for time-based factor (how long since last user message)
            'probability_weight': 0.3,  # Weight for AI's own decision 
            
            # === SLEEP CALCULATION PARAMETERS ===
            # These control how the agent determines when to "sleep" (pause activity)
            'wake_up_pattern': "Check every 2-3 minutes when active",  # Human-readable sleep pattern description
            'min_sleep_time': 30,  # Minimum seconds to sleep (prevents excessive checking)
            'max_sleep_time': 600,  # Maximum seconds to sleep (prevents long inactivity)
        },
        
        # Logging configuration
        log_level="INFO"  # Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    )
    
    # === CALLBACK REGISTRATION ===
    # Register different types of callbacks to monitor agent behavior
    
    # Response callback - triggered when AI generates a response
    agent.add_callback(on_ai_response)
    
    # Sleep time callback - triggered when agent calculates sleep duration
    agent.add_sleep_time_callback(on_sleep_time_calculated)
    
    # Decision callback - triggered when agent decides whether to respond
    agent.add_decision_callback(on_decision_made)
    
    # Start the agent - begins the proactive monitoring and decision-making process
    agent.start()
    
    print("=== All Configuration Parameters Demo ===")
    print("This example demonstrates every available configuration option.")
    print("Watch the callbacks to see how each parameter affects behavior.")
    print("Type 'quit' to exit.\n")
    
    try:
        # Main interaction loop
        while True:
            message = input("You: ").strip()
            if message.lower() == 'quit':
                break
            
            # Send message to agent - triggers decision-making process
            agent.send_message(message)
            
            # Brief pause to prevent overwhelming the system
            time.sleep(1)
            
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        pass
    finally:
        # Always stop the agent to clean up resources
        agent.stop()


if __name__ == "__main__":
    main()