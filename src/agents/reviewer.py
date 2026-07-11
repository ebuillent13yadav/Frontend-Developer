from langchain_ollama import ChatOllama
from src.state import ProjectState

llm = ChatOllama(model="qwen2.5:7b")

def reviewer_node(state: ProjectState) -> dict:
    print("[Reviewer Agent] Analyzing the code for runtime bugs or layout defects...")

    system_instruction = """
    You are an expert React Code Reviewer.

    Your task is to inspect the generated React code for major issues before deployment.

    Checklist:

    1. Ensure the code is a valid React component.
    2. Ensure there are NO <html>, <head>, or <body> tags.
    3. Ensure the component is exported using:
       export default App;
    4. Ensure there are no markdown code fences (```), random text like "javascript;", or explanations.
    5. Verify that all import statements are syntactically correct.
    6. Verify that imported packages are real npm packages. Reject invented package names such as:
       - @styled-components
       - @react-icons
       - @tailwindcss
    7. Ensure there are no imports from missing local files (./ or ../) unless they are guaranteed to exist.
    8. Ensure the generated code is self-contained and can compile successfully.
    9. Ensure there are no obvious JavaScript or JSX syntax errors.
    
    CRITICAL OUTPUT FORMAT:
    
    - If ALL checks pass, output EXACTLY:
    PASSED
    
    Do not output any other words, explanations, or caution notes.
    
    - Otherwise, output a concise bulleted list of the issues that must be fixed.
    Do not include code blocks or corrected code.
    Only describe the problems.
    """
    full_prompt = f"{system_instruction}\n\nGenerated Code to Review:\n{state['generated_code']}"

    ai_message = llm.invoke(full_prompt)
    review_feedback = ai_message.content.strip()

    print(f"Review Verdict:\n{review_feedback}")

    return {"review_feedback": review_feedback}