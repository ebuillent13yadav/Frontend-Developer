from langchain_ollama import ChatOllama
from src.state import ProjectState
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="qwen2.5:7b")

def planner_node(state: ProjectState) -> dict:
    """
    Planner Agent: Analyzes user requirements and creates a conceptual roadmap.
    """
    print("\n [Planner Agent] Breaking down requirements...")

    system_instructions = (
        """
        You are an expert React Frontend Architect. Analyze the user request and output a
        high-level structure listing what functional components are required. Keep 
        your output clean and concise.
        """
    )
    user_input = state["user_prompt"]
    full_prompt = (
        SystemMessage(content=system_instructions),
        HumanMessage(content=user_input)
    )

    plan_output = llm.invoke(full_prompt)

    return {"project_plan": plan_output.content}