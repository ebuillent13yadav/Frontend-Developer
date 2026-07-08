from langgraph.graph import StateGraph, END
from src.state import ProjectState

from src.agents.planner import planner_node
from src.agents.architect import architect_node
from src.agents.component import component_node

def write_file_node(state: ProjectState) -> dict:
    """
    Software Engineering Automation Node: Writes the finalized code to disk.
    """
    print("[Automation Node] Saving finalized codebase to disk...")

    code = state["generated_code"]
    if "export default" not in code:
        code+="\n\nexport default App;"
    
    with open(state["file_layout"], "w", encoding="utf-8") as f:
        f.write(code)
    
    print("App.jsx updated successfully!")
    return {"final_code": code}

#--------------LangGraph Orchestration Setup---------

workflow = StateGraph(ProjectState)

workflow.add_node("PlannerAgent", planner_node)
workflow.add_node("ArchitectAgent", architect_node)
workflow.add_node("ComponentAgent", component_node)
workflow.add_node("FileWriterNode", write_file_node)

workflow.set_entry_point("PlannerAgent")
workflow.add_edge("PlannerAgent", "ArchitectAgent")
workflow.add_edge("ArchitectAgent", "ComponentAgent")
workflow.add_edge("ComponentAgent", "FileWriterNode")
workflow.add_edge("FileWriterNode", END)

compiled_graph = workflow.compile()