from langgraph.graph import StateGraph, END
from src.state import ProjectState

from src.agents.planner import planner_node
from src.agents.architect import architect_node
from src.agents.component import component_node
from src.agents.reviewer import reviewer_node

import subprocess
import re

def package_manager_and_writer_node(state: ProjectState) -> dict:
    print("\n [Package Manager Agent] Scanning finalized code for external libraries...")
    code = state["generated_code"]

    import_pattern = re.compile(r"from\s+['\"]([^'\".]+)['\"]")
    detected_packages = []

    for line in code.splitlines():
        match = import_pattern.search(line)
        if match:
            package_name = match.group(1)
            if package_name not in ["react", "react-dom"]:
                detected_packages.append(package_name)
    
    unique_packages = list(set(detected_packages))
    if unique_packages:
        print(f"Detected external dependencies: {unique_packages}")
        for pkg in unique_packages:
            print(f"Running: npm install {pkg}...")

            subprocess.run(["npm", "install", pkg], cwd="./my-generated-app", shell=True)
            print(f"Installed {pkg} successfully!")
    
    else:
        print("No external dependencies detected. Proceeding safely.")
    
    with open(state["file_layout"], "w", encoding="utf-8") as f:
        f.write(code)
    
    print("[Automation Node] Saved verified codebase to disk!")
    return {"final_code": code}

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
workflow.add_node("PackageManagerAndFileWriterNode", package_manager_and_writer_node)

workflow.set_entry_point("PlannerAgent")
workflow.add_edge("PlannerAgent", "ArchitectAgent")
workflow.add_edge("ArchitectAgent", "ComponentAgent")
workflow.add_edge("ComponentAgent", "ReviewerAgent")

workflow.add_conditional_edges(
    "ReviewerAgent",
    route_after_review,
    {
        "deploy": "PackageManagerAndFileWriterNode",
        "fix_code": "ComponentAgent"
    }
)

workflow.add_edge("PackageManagerAndFileWriterNode", END)

compiled_graph = workflow.compile()