from langchain_ollama import ChatOllama
from src.state import ProjectState
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="qwen2.5:7b")

def component_node(state: ProjectState) -> dict:
    """
    Component Agent: Consumes the planner's architecture roadmap and outputs clean,
    executable react code.
    """
    print("[Component Agent] Writing core React applications code...")

    system_instruction = """
      You are an expert React frontend developer.

      Generate a complete App.jsx component.

      Rules:
      - Output only JavaScript/JSX.
      - No markdown.
      - No explanations.
      - No local imports.
      - Use only official npm packages.
      - Never invent package names.
      - If you are unsure whether a package exists, do not use it.
      - Prefer pure React and Tailwind CSS whenever possible.
     """
    
    user_context = f"Roadmap Plan to follow:\n{state['project_plan']}\n\nOriginal Request:\n{state['user_prompt']}"
    
    if state.get("review_feedback") and state["review_feedback"] != "PASSED":
        user_context += f"\n\n CRITICAL: Your previous version failed review with these errors. Fix them immediately:\n{state['review_feedback']}"
        print("[Component Agent] Code failed review. Attempting correction based on feedback...")
    
    full_prompt = (
        SystemMessage(system_instruction),
        HumanMessage(user_context)
    )

    ai_message_object = llm.invoke(full_prompt)
    raw_code = ai_message_object.content

    clean_code = raw_code.replace("```jsx","").replace("```","").strip()

    return {"generated_code": clean_code}