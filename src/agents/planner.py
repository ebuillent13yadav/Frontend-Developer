from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import ProjectState

llm = ChatOllama(model="qwen2.5:7b")


def planner_node(state: ProjectState) -> dict:
    print("\n[Planner Agent] Breaking down requirements...")

    system_instruction = """
    You are an expert React Frontend Architect.

    Create a high-level implementation plan for the application.

    Include:
    - Overall page structure
    - Major React components
    - Layout hierarchy
    - UI sections
    - Any reusable components
    - Suggested external libraries (only if necessary)

    Do not generate code.
    Return only the implementation plan.
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