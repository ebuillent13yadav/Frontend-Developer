from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import ProjectState

llm = ChatOllama(model="qwen2.5:7b")


def planner_node(state: ProjectState) -> dict:
    print("\n[Planner Agent] Breaking down requirements...")

    system_instruction = """
    You are an expert React Frontend Architect.

    Your task is to analyze the project requirements and create a high-level implementation plan for a React application.

    Requirements:
    - Do NOT generate any code.
    - Return ONLY the implementation plan.
    - Base the plan strictly on the provided user requirements and extracted specifications.
    - Do not introduce frameworks, libraries, or features that were not requested.
    - Suggest external libraries only if they are genuinely required.
    
    The implementation plan should include:
    
    1. Application Overview
       - Purpose of the application
       - Primary user workflow

    2. Overall Page Structure
       - Main pages or views
       - Navigation flow
       - Routing requirements (if applicable)

    3. Component Hierarchy
       - Parent components
       - Child components
       - Reusable UI components

    4. Layout Structure
       - Header
       - Sidebar
       - Main content
       - Footer
       - Responsive layout strategy

    5. UI Sections
       - Cards
       - Forms
       - Tables
       - Charts
       - Navigation
       - Modals
       - Any additional UI sections

    6. State Management
       - Local component state
       - Shared/global state (only if necessary)

    7. External Libraries
       - Recommend only official npm packages.
       - Do not invent package names.
       - If Tailwind CSS is specified, prefer Tailwind utilities over additional UI libraries unless explicitly requested.

    8. Implementation Order
       - List the recommended order for building the application.

    Rules:
    - Keep the plan concise but complete.
    - Do not generate JSX or JavaScript.
    - Do not include explanations outside the implementation plan.
    - Ensure the plan is compatible with a standard Vite + React project.
    """

    specs = state["extracted_data"]
    if specs is None:
        raise ValueError("Planner Agent requires extracted specifications.")

    user_input = f"""
    Original User Request:
    {state["user_prompt"]}

    Extracted Specifications:
    {specs.model_dump()}
    """

    response = llm.invoke([
        SystemMessage(content=system_instruction),
        HumanMessage(content=user_input)
    ])

    return {
        "project_plan": response.content
    }