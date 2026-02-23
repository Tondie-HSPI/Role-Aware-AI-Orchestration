"""
Role-Aware AI Orchestration Graph
----------------------------------

This module defines a minimal stateful agent using LangGraph.

Architecture:
START
  → Intake
  → Role Router
  → Role-Specific Tool
  → Output
  → END

This file represents the orchestration layer only.
UI is handled separately.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END


# -------------------------
# 1. Structured State Model
# -------------------------

class RoleState(TypedDict):
    role: Literal["student", "teacher", "parent"]
    title: str
    user_input: str
    next_action: str
    response: str


# -------------------------
# 2. Core Nodes
# -------------------------

def intake_node(state: RoleState):
    """Initial intake processing."""
    print("→ Intake Node")
    return state


def role_router_node(state: RoleState):
    """
    Determines which tool to invoke based on role.
    This is the decision boundary of the agent.
    """
    print("→ Role Router Node")

    role = state["role"]

    if role == "teacher":
        action = "teacher_tool"
    elif role == "student":
        action = "student_tool"
    elif role == "parent":
        action = "parent_tool"
    else:
        action = "fallback"

    return {**state, "next_action": action}


# -------------------------
# 3. Role-Specific Tool Nodes
# -------------------------

def teacher_tool(state: RoleState):
    print("→ Teacher Tool Node")
    response = f"[Knowledge Layer Applied] Curriculum support for '{state['title']}'."
    return {**state, "response": response}


def student_tool(state: RoleState):
    print("→ Student Tool Node")
    response = f"[Scaffold Applied] Expand your thinking about '{state['title']}'."
    return {**state, "response": response}


def parent_tool(state: RoleState):
    print("→ Parent Tool Node")
    response = f"[Conversation Support] Discuss themes in '{state['title']}' together."
    return {**state, "response": response}


def fallback_node(state: RoleState):
    print("→ Fallback Node")
    return {**state, "response": "No valid role detected."}


def output_node(state: RoleState):
    """Final output assembly."""
    print("→ Output Node")
    return state


# -------------------------
# 4. Graph Definition
# -------------------------

builder = StateGraph(RoleState)

builder.add_node("intake", intake_node)
builder.add_node("role_router", role_router_node)
builder.add_node("teacher_tool", teacher_tool)
builder.add_node("student_tool", student_tool)
builder.add_node("parent_tool", parent_tool)
builder.add_node("fallback", fallback_node)
builder.add_node("output", output_node)

builder.add_edge(START, "intake")
builder.add_edge("intake", "role_router")

builder.add_conditional_edges(
    "role_router",
    lambda state: state["next_action"],
    {
        "teacher_tool": "teacher_tool",
        "student_tool": "student_tool",
        "parent_tool": "parent_tool",
        "fallback": "fallback",
    }
)

builder.add_edge("teacher_tool", "output")
builder.add_edge("student_tool", "output")
builder.add_edge("parent_tool", "output")
builder.add_edge("fallback", "output")
builder.add_edge("output", END)

graph = builder.compile()


# -------------------------
# 5. Example Invocation
# -------------------------

if __name__ == "__main__":
    initial_state = {
        "role": "student",
        "title": "Charlotte's Web",
        "user_input": "I liked the friendship theme.",
        "next_action": "",
        "response": ""
    }

    result = graph.invoke(initial_state)

    print("\nFinal Response:")
    print(result["response"])
