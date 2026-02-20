# Constraint Hierarchy

## Overview

The orchestration framework enforces constraints hierarchically to prevent generative drift, role overreach, and uncontrolled output generation.

Constraints are applied in strict order of precedence.

---

## 1. Safety Constraints (Highest Priority)

Safety rules override all downstream behavior.

Examples:
- Refusal logic
- Harm detection
- Authority boundaries
- Role-based access restrictions

No output may bypass this layer.

---

## 2. Knowledge Alignment Constraints

Outputs must remain grounded in defined domain scaffolds.

This layer ensures:
- Context-aware generation
- Controlled interpretation
- Restricted inference scope
- Structured output validation

This layer prevents hallucinated authority.

---

## 3. Engagement Constraints (Lowest Priority)

This layer governs interaction style.

Examples:
- Guided scaffolding
- Reflective prompting
- Question-based support
- Structured assistance without substitution

Engagement rules may never override Safety or Knowledge constraints.

---

## Enforcement Model

Constraint layers are applied sequentially:

Safety → Knowledge Alignment → Engagement

If a violation occurs at any stage, execution halts or reroutes.

This guarantees predictable system behavior.
