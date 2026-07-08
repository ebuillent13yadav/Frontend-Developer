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
    You are an automated React code generation engine.

    CRITICAL STRUCTURAL RULES:
    1. Output ONLY a valid, executable single-file React JavaScript component named App.
    2. Absolutely DO NOT include HTML wrappers like <!DOCTYPE html>, <html>, <head>, <body>, or <style> tags.
    3. If you want to use styles, use inline React style objects.
    4. Ensure the file structure defines a clear functional module (e.g., function App() { return (...) }).
    5. Output ONLY raw source code. No explanations, no markdown blocks, no filler.

    🌟 MANDATORY SINGLE-FILE RULE:
    - Do NOT try to import other local components using relative paths (e.g., DO NOT use import Header from "./Header" or import Sidebar from "./Sidebar").
    - Every single sub-component, layout card, icon mapping, or sub-widget MUST be written directly inside this single file. You can declare multiple helper functions in this file, but they must all live under or alongside 'function App()'.
    """
    
    user_context = f"Roadmap Plan to follow:\n{state['project_plan']}\n\nOriginal Request:\n{state['user_prompt']}"
    full_prompt = (
        SystemMessage(system_instruction),
        HumanMessage(user_context)
    )

    ai_message_object = llm.invoke(full_prompt)
    raw_code = ai_message_object.content

    clean_code = raw_code.replace("```jsx","").replace("```","").strip()

    return {"generated_code": clean_code}