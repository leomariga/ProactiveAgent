# Sleep Time Calculators

Sleep time calculators determine how long the agent should wait before the next decision cycle.

## SleepTimeCalculator (Base Class)

::: proactiveagent.sleep_time_calculators.base.SleepTimeCalculator
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

## AIBasedSleepCalculator

Uses AI to interpret natural language patterns and determine optimal sleep time.

::: proactiveagent.sleep_time_calculators.ai_based.AIBasedSleepCalculator
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

## StaticSleepCalculator

Fixed sleep intervals regardless of context.

::: proactiveagent.sleep_time_calculators.static.StaticSleepCalculator
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

## PatternBasedSleepCalculator

Adjusts timing based on conversation keywords and patterns.

::: proactiveagent.sleep_time_calculators.pattern_based.PatternBasedSleepCalculator
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

## FunctionBasedSleepCalculator

Custom timing logic using Python functions.

::: proactiveagent.sleep_time_calculators.function_based.FunctionBasedSleepCalculator
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

