# Decision Engines

Decision engines determine whether your AI agent should respond based on various factors like context, timing, and engagement.

## DecisionEngine (Base Class)

::: proactiveagent.decision_engines.base.DecisionEngine
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

## AIBasedDecisionEngine

Uses AI to make intelligent decisions about when to respond.

::: proactiveagent.decision_engines.ai_based.AIBasedDecisionEngine
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

## SimpleDecisionEngine

Simple time-based decision logic.

::: proactiveagent.decision_engines.simple.SimpleDecisionEngine
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

## ThresholdDecisionEngine

Priority-based timing with different response times for different message types.

::: proactiveagent.decision_engines.threshold_based.ThresholdDecisionEngine
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

## FunctionBasedDecisionEngine

Custom decision logic using Python functions.

::: proactiveagent.decision_engines.function_based.FunctionBasedDecisionEngine
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

