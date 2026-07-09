from langgraph.graph import StateGraph, END
from src.state import ProjectState

from src.agents.planner import planner_node
from src.agents.architect import architect_node
from src.agents.component import component_node
from src.agents.reviewer import reviewer_node

def write_file_node(state: ProjectState) -> dict:
    """
    Software Engineering Automation Node: Writes the finalized code to disk.
    """
    print("[Automation Node] Saving finalized codebase to disk...")
    
    with open(state["file_layout"], "w", encoding="utf-8") as f:
        f.write(state["generated_code"])
    
    print("App.jsx updated successfully!")
    return {"final_code": state["generated_code"]}

def route_after_review(state: ProjectState):
    feedback = state.get("review_feedback","").upper()
    if "PASSED" in feedback:
        print("Code Passed Inspection! Moving to file deployment.")
        return "deploy"
    else:
        print("Code Rejected. Sending back to ComponentAgent for revisions.")
        return "fix_code"

#--------------LangGraph Orchestration Setup---------

workflow = StateGraph(ProjectState)

workflow.add_node("PlannerAgent", planner_node)
workflow.add_node("ArchitectAgent", architect_node)
workflow.add_node("ComponentAgent", component_node)
workflow.add_node("ReviewerAgent", reviewer_node)
workflow.add_node("FileWriterNode", write_file_node)

workflow.set_entry_point("PlannerAgent")
workflow.add_edge("PlannerAgent", "ArchitectAgent")
workflow.add_edge("ArchitectAgent", "ComponentAgent")
workflow.add_edge("ComponentAgent", "ReviewerAgent")

workflow.add_conditional_edges(
    "ReviewerAgent",
    route_after_review,
    {
        "deploy": "FileWriterNode",
        "fix_code": "ComponentAgent"
    }
)

workflow.add_edge("FileWriterNode", END)

compiled_graph = workflow.compile()