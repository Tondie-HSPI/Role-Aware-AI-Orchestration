"""
Literacy-Oriented Role-Aware Orchestration Example

This example demonstrates:
- Structured state
- Role-based routing (Student / Teacher / Parent)
- Hierarchical constraint enforcement
- Cognitive-preservation logic

This mirrors the Tag-Along Reader implementation model.
"""

from typing import TypedDict


# ----------------------------
# Structured State Definition
# ----------------------------

class State(TypedDict):
    role: str
    reflection_text: str
    evidence_provided: bool
    safety_passed: bool
    output: str


# ----------------------------
# Safety Constraint
# ----------------------------

def safety_check(state: State) -> State:
    """
    Blocks unsafe or inappropriate content.
    """
    if "harm" in state["reflection_text"].lower():
        state["safety_passed"] = False
        state["output"] = "Content flagged for review."
    else:
        state["safety_passed"] = True
    return state


# ----------------------------
# Literacy-Specific Constraint
# ----------------------------

def evidence_requirement(state: State) -> State:
    """
    Enforces evidence-based reflection.
    Student must reference the text.
    """

    if "because" in state["reflection_text"].lower():
        state["evidence_provided"] = True
    else:
        state["evidence_provided"] = False
        state["output"] = "Please explain your thinking using evidence from the text."

    return state


# ----------------------------
# Role-Specific Processing
# ----------------------------

def process_student(state: State) -> State:
    state = evidence_requirement(state)

    if state["evidence_provided"]:
        state["output"] = "Reflection accepted. Consider expanding your reasoning."
    
    return state


def process_teacher(state: State) -> State:
    state["output"] = "Display structured student reflection for review."
    return state


def process_parent(state: State) -> State:
    state["output"] = "Display read-only reflection summary."
    return state


# ----------------------------
# Orchestration Engine
# ----------------------------

def orchestrate(state: State) -> State:
    """
    Governance-first execution order:
    1. Safety
    2. Role routing
    """

    # 1. Safety
    state = safety_check(state)
    if not state["safety_passed"]:
        return state

    # 2. Role Routing
    if state["role"] == "student":
        return process_student(state)

    elif state["role"] == "teacher":
        return process_teacher(state)

    elif state["role"] == "parent":
        return process_parent(state)

    else:
        state["output"] = "Unknown role."
        return state


# ----------------------------
# Example Run
# ----------------------------

if __name__ == "__main__":
    example_state: State = {
        "role": "student",
        "reflection_text": "I think the character changed because he learned from his mistake.",
        "evidence_provided": False,
        "safety_passed": False,
        "output": ""
    }

    result = orchestrate(example_state)
    print(result)


