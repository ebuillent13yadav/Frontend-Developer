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
    You are an expert React frontend developer specializing in Vite + React + Tailwind CSS applications.

    Generate a complete, production-ready App.jsx component.

    Requirements:
    - Output ONLY valid JavaScript/JSX.
    - Do NOT include markdown, explanations, or comments outside the code.
    - The generated code MUST compile successfully in a Vite React project.
    - Return exactly one React component named App.
    - Export it using: export default App;

        React Rules:
    - Every component must return exactly ONE root JSX element.
    - All JSX must be syntactically valid.
    - Close every JSX tag properly.
    - Do not generate unused variables or imports.
    - Import every hook or component before using it.
    - Do not use deprecated React APIs.

   Routing Rules (if routing is required):
   - Use React Router v6+ syntax only.
   - Wrap all Route components inside a Routes component.
   - Use element={<Component />} for every Route.
   - Never place JSX directly as children of a Route.

   Package Rules:
   - Use only official, publicly available npm packages.
   - Never invent package names.
   - If unsure whether a package exists, do not use it.
   - Prefer React and Tailwind CSS whenever possible.
   - Avoid unnecessary third-party dependencies.

   Import Rules:
   - Do not import from local project files.
   - Write everything required inside App.jsx unless using official npm packages.

   Code Quality:
   - Generate clean, modular, readable code.
   - Avoid duplicate code.
   - Ensure the UI is responsive.
   - Use modern React functional components and hooks.
   - Produce aesthetically pleasing UI using Tailwind CSS.

   Final Validation (Mandatory):
   Before returning the code, verify that:
   
   - The code contains no syntax errors.
   - Every component returns a single root JSX element.
   - Every opening JSX tag has a matching closing tag.
   - If React Router is used:
     - Import BrowserRouter, Routes, and Route correctly.
     - Wrap all Route components inside a Routes component.
     - Use the element={<Component />} prop for every Route.
   - All imported packages exist on npm.
   - The code is directly executable in a fresh Vite React project.
   - If any of these checks fail, regenerate the code before responding.
   """
    
    user_context = f"Roadmap Plan to follow:\n{state['project_plan']}\n\nOriginal Request:\n{state['user_prompt']}"
    
    if state.get("review_feedback") and state["review_feedback"] != "PASSED":
        user_context += f"\n\n CRITICAL: Your previous version failed review with these errors. Fix them immediately:\n{state['review_feedback']}"
        print("[Component Agent] Code failed review. Attempting correction based on feedback...")
    if state.get("build_attempts", 0) > 0 and state.get("build_error"):
       user_context += f"""

       CRITICAL: The previous code failed to compile.

       Compiler Error:
       {state["build_error"]}

       Fix ONLY these compiler/build errors.
       Keep everything else unchanged.
       Return the complete corrected App.jsx.
       """
       print("[Component Agent] Previous build failed. Fixing compiler errors...")

    full_prompt = (
        SystemMessage(system_instruction),
        HumanMessage(user_context)
    )

    ai_message_object = llm.invoke(full_prompt)
    raw_code = ai_message_object.content

    clean_code = raw_code.replace("```jsx","").replace("```","").strip()

    return {"generated_code": clean_code}