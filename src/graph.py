from langgraph.graph import StateGraph, END
from src.state import ProjectState
import shutil
from src.agents.clarification import clarification_node
from src.agents.planner import planner_node
from src.agents.architect import architect_node
from src.agents.component import component_node
from src.agents.reviewer import reviewer_node
from src.agents.build_verifier import build_verifier_node
import os
import subprocess
import re

def package_manager_and_writer_node(state: ProjectState) -> dict:
    print("\n [Package Manager Agent] Scanning finalized code for external libraries...")
    code = state["generated_code"]

    import_pattern = re.compile(
    r'import\s+(?:.*?\s+from\s+)?["\']([^"\']+)["\']'
    )
    detected_packages = []

    for line in code.splitlines():
        match = import_pattern.search(line)
        if match:
            package_name = match.group(1)

            if(
                package_name.startswith("./")
                or package_name.startswith("../")
                or package_name.startswith("@/")
            ):
                continue
            
            if package_name.startswith("@"):
                package_name = "/".join(package_name.split("/")[:2])
            else:
                package_name = package_name.split("/")[0]

            if package_name not in ["react", "react-dom"]:
                detected_packages.append(package_name)
    
    unique_packages = list(set(detected_packages))
    if unique_packages:
        print(f"Detected external dependencies: {unique_packages}")
        print("cwd:", os.getcwd())
        print("app exists:", os.path.exists("./my-generated-app"))
        print("npm:", shutil.which("npm"))
        print("npm.cmd:", shutil.which("npm.cmd"))
        for pkg in unique_packages:
            print(f"Package: {repr(pkg)}")
            print(f"Running: npm install {pkg}...")

            result = subprocess.run(
                [r"C:\Program Files\nodejs\npm.cmd",
                 "install", 
                 pkg,
                ],
                cwd="./my-generated-app", 
                # shell=True,
                capture_output=True,
                text=True
                )
            if result.returncode == 0:
                print(f"Installed {pkg} successfully!")
            else:
                print(f"Failed to install {pkg}")
                print(result.stderr)
    else:
        print("No external dependencies detected. Proceeding safely.")
    
    with open(state["file_layout"], "w", encoding="utf-8") as f:
        f.write(code)
    
    print("[Automation Node] Saved verified codebase to disk!")
    return {"final_code": code}

def route_after_clarification(state: ProjectState):
    if state["is_sufficient"]:
        print("Specifications Complete. Moving to Planner Agent.")
        return "planner"
    print("More Information required from user")
    return "end"

def route_after_review(state: ProjectState):
    feedback = state.get("review_feedback","").strip()
    if feedback == "PASSED":
        print("Code Passed Inspection! Moving to file deployment.")
        return "deploy"
    else:
        print("Code Rejected. Sending back to ComponentAgent for revisions.")
        return "fix_code"
    
def route_after_build(state: ProjectState):
    if state["build_passed"]:
        return "deploy"

    if state["build_attempts"] >= 3:
        return "end"

    return "fix"
#--------------LangGraph Orchestration Setup---------#

workflow = StateGraph(ProjectState)

workflow.add_node("ClarificationAgent",clarification_node)
workflow.add_node("PlannerAgent", planner_node)
workflow.add_node("ArchitectAgent", architect_node)
workflow.add_node("ComponentAgent", component_node)
workflow.add_node("ReviewerAgent", reviewer_node)
workflow.add_node("BuildVerifier", build_verifier_node)
workflow.add_node("PackageManagerAndFileWriterNode", package_manager_and_writer_node)

workflow.set_entry_point("ClarificationAgent")

workflow.add_conditional_edges(
    "ClarificationAgent",
    route_after_clarification,
    {
        "planner": "PlannerAgent",
        "end":END,
    },
)

workflow.add_edge("PlannerAgent", "ArchitectAgent")
workflow.add_edge("ArchitectAgent", "ComponentAgent")
workflow.add_edge("ComponentAgent", "ReviewerAgent")

workflow.add_conditional_edges(
    "ReviewerAgent",
    route_after_review,
    {
        "deploy": "PackageManagerAndFileWriterNode",
        "fix_code": "ComponentAgent",
    },
)

workflow.add_edge("PackageManagerAndFileWriterNode", "BuildVerifier")
workflow.add_conditional_edges(
    "BuildVerifier",
    route_after_build,
    {
        "deploy": END,
        "fix": "ComponentAgent",
        "end": END,
    },
)

compiled_graph = workflow.compile()