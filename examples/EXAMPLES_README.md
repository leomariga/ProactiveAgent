# ProactiveAgent Examples

This directory contains comprehensive examples demonstrating all features of the ProactiveAgent library. All examples are based on the `ultra_simple_chat.py` but focus on specific aspects of the library functionality.

## Quick Start

Before running any examples, make sure to:
1. Install the ProactiveAgent library: `pip install ProactiveAgent`
2. Set your OpenAI API key in each example file
3. Run any example: `python example_name.py`

## Examples Overview

### Configuration Examples

- **`all_config_parameters.py`** - Demonstrates all available configuration parameters with detailed explanations

### Sleep Time Calculator Examples

- **`ai_based_sleep_calculator.py`** - Uses AI provider to calculate sleep timing (default behavior)
- **`static_sleep_calculator.py`** - Fixed sleep intervals for consistent timing
- **`function_based_sleep_calculator.py`** - Custom function with adaptive logic based on engagement
- **`pattern_based_sleep_calculator.py`** - Keyword-based pattern matching for sleep timing

### Decision Engine Examples

- **`ai_based_decision_engine.py`** - AI-powered decision making (default behavior)
- **`simple_decision_engine.py`** - Simple time-based decision logic
- **`threshold_decision_engine.py`** - Threshold-based decisions with priority levels
- **`function_based_decision_engine.py`** - Custom decision function with sophisticated logic

### Custom Implementation Examples

- **`custom_sleep_calculator.py`** - Complete custom sleep calculator with machine learning-like adaptation
- **`custom_decision_engine.py`** - Complete custom decision engine with sentiment analysis and momentum tracking

### Callback Examples

- **`comprehensive_callbacks.py`** - Demonstrates all callback types with logging, analysis, and metrics

## Key Features Demonstrated

### Sleep Time Calculators
1. **AIBasedSleepCalculator** - Uses AI provider to determine optimal wake-up timing
2. **StaticSleepCalculator** - Fixed intervals for predictable behavior
3. **FunctionBasedSleepCalculator** - Custom functions for adaptive timing
4. **PatternBasedSleepCalculator** - Keyword pattern matching for timing decisions

### Decision Engines
1. **AIBasedDecisionEngine** - Intelligent context-aware decision making
2. **SimpleDecisionEngine** - Basic time-based response decisions
3. **ThresholdDecisionEngine** - Priority-based response thresholds
4. **FunctionBasedDecisionEngine** - Custom decision logic functions

### Configuration Parameters

All examples show how to configure:
- `min_response_interval` - Minimum time between responses
- `max_response_interval` - Maximum time before forced response
- `engagement_threshold` - Overall engagement threshold (0.0-1.0)
- `engagement_high_threshold` - Message count for "high" engagement
- `engagement_medium_threshold` - Message count for "medium" engagement  
- `context_relevance_weight` - Weight for context in decisions
- `time_weight` - Weight for time-based factors
- `probability_weight` - Weight for probabilistic factors
- `wake_up_pattern` - Pattern description for sleep calculations
- `min_sleep_time` - Minimum sleep duration in seconds
- `max_sleep_time` - Maximum sleep duration in seconds

### Callback Types

Three types of callbacks are demonstrated:

1. **Response Callbacks** - Called when AI generates a response
   ```python
   def on_ai_response(response: str):
       print(f"AI: {response}")
   agent.add_callback(on_ai_response)
   ```

2. **Sleep Time Callbacks** - Called when sleep time is calculated
   ```python
   def on_sleep_time_calculated(sleep_time: int, reasoning: str):
       print(f"Sleep: {sleep_time}s - {reasoning}")
   agent.add_sleep_time_callback(on_sleep_time_calculated)
   ```

3. **Decision Callbacks** - Called when response decision is made
   ```python
   def on_decision_made(should_respond: bool, reasoning: str):
       decision = "RESPOND" if should_respond else "WAIT"
       print(f"Decision: {decision} - {reasoning}")
   agent.add_decision_callback(on_decision_made)
   ```

## Running Examples

Each example is self-contained and can be run independently:

```bash
# Basic configuration example
python all_config_parameters.py

# Sleep calculator examples
python ai_based_sleep_calculator.py
python static_sleep_calculator.py
python function_based_sleep_calculator.py
python pattern_based_sleep_calculator.py

# Decision engine examples  
python ai_based_decision_engine.py
python simple_decision_engine.py
python threshold_decision_engine.py
python function_based_decision_engine.py

# Custom implementation examples
python custom_sleep_calculator.py
python custom_decision_engine.py

# Callback examples
python comprehensive_callbacks.py
```

## Learning Path

Recommended order for learning the library:

1. **Start with** `all_config_parameters.py` to understand basic configuration
2. **Try sleep calculators** in order: AI-based → Static → Function-based → Pattern-based
3. **Try decision engines** in order: AI-based → Simple → Threshold → Function-based
4. **Explore callbacks** with `comprehensive_callbacks.py`
5. **Build custom implementations** using the custom examples as templates

## Tips for Development

- **API Key**: Replace `"your-openai-api-key-here"` with your actual OpenAI API key
- **Logging**: Set `log_level="DEBUG"` in agent configuration to see detailed operation logs
- **Experimentation**: Modify configuration values to see how they affect behavior
- **Custom Logic**: Use the custom implementation examples as starting points for your own logic
- **Monitoring**: Use callbacks to monitor and analyze agent behavior in real-time

## Example Output

When running examples, you'll see output like:

```
🤖 AI: Hello! How can I help you today?
⏰ Sleep time: 120s - Medium engagement detected, checking every 2 minutes
🧠 Decision: ✅ RESPOND - User asked a question - immediate response
📝 Logged response #1
📊 Response Analysis: 8 words, positive sentiment
```

This shows the integration of AI responses, sleep calculations, decision making, and callback monitoring.

## Support

If you have questions about the examples or need help customizing them for your use case, please refer to the main ProactiveAgent documentation or create an issue in the repository.
