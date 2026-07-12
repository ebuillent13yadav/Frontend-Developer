from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import ProjectState

llm = ChatOllama(model="qwen2.5:7b")


def reviewer_node(state: ProjectState) -> dict:
    print("[Reviewer Agent] Analyzing the code for runtime bugs or layout defects...")

    system_instruction = """
    You are an expert React Code Reviewer.

    Your task is to inspect the generated React code before deployment.

    Carefully verify the following:

    1. React Structure
    - The code defines exactly one React component named App.
    - The component is exported using:
      export default App;
    - The component returns exactly one root JSX element.

    2. JSX Validation
    - No JSX syntax errors.
    - Every opening tag has a matching closing tag.
    - No adjacent JSX elements without a wrapper.
    - No invalid JSX nesting.

    3. React Best Practices
    - No deprecated React APIs.
    - Hooks are used correctly.
    - No undefined variables.
    - No duplicate declarations.
    - No obvious runtime errors.

    4. Imports
    - Every imported module is actually used.
    - Every used hook or component is imported.
    - Import statements are syntactically valid.
    - No imports from missing local files (./ or ../) unless they are guaranteed to exist.
    - Every external package must exist on npm.
    - Reject invented package names.
    - Reject any package that is not an official npm package.

    Examples of invalid packages:
    - @tailwindcss/react
    - @styled-components
    - @react-icons

    If any imported package is not known to exist on npm, DO NOT output PASSED.

    5. Routing (if React Router is used)
    - BrowserRouter is imported correctly.
    - Every Route is inside a Routes component.
    - Every Route uses:
      element={<Component />}
    - No JSX is placed directly inside a Route.

    6. Output Cleanliness
    - No markdown code fences.
    - No explanations.
    - No comments outside the code.
    - No random strings such as "javascript;".
    - No HTML document tags such as:
      <html>
      <head>
      <body>

    7. Build Readiness
    - The code should compile successfully in a fresh Vite + React project.
    - There should be no obvious JavaScript or JSX syntax errors.
     Reject any package that is not an official npm package.

    Examples of invalid packages:
    - @tailwindcss/react
    - @styled-components
    - @react-icons

    If any imported package is not known to exist on npm, DO NOT output PASSED.
    Decision Rules:

    - If ANY issue is found, DO NOT output PASSED.
    - List ONLY the issues that must be fixed.
    - Keep each issue short and actionable.
    - Do not rewrite the code.
    - Do not suggest UI improvements.
    - Only report correctness issues.

    CRITICAL OUTPUT FORMAT

    If every check passes, output EXACTLY:

    PASSED

    Otherwise, output ONLY a concise bulleted list describing the issues to fix.

    Do NOT:
    - Use markdown code fences.
    - Use ``` or ```plaintext.
    - Include explanations.
    - Include introductory phrases such as "Here are the issues to fix".
    - Include corrected code.
    """

    ai_message = llm.invoke([
        SystemMessage(content=system_instruction),
        HumanMessage(content=state["generated_code"])
    ])

    review_feedback = ai_message.content.strip()

    # Prevent accidental "PASSED" appearing together with issues
    if review_feedback != "PASSED" and "PASSED" in review_feedback:
        review_feedback = review_feedback.replace("PASSED", "").strip()

    print(f"Review Verdict:\n{review_feedback}")

    return {
        "review_feedback": review_feedback
    }