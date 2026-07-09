from langchain_ollama import ChatOllama
from src.state import ProjectState

llm = ChatOllama(model="qwen2.5:7b")

def reviewer_node(state: ProjectState) -> dict:
    print("[Reviewer Agent] Analyzing the code for runtime bugs or layout defects...")

    system_instruction = """You are an expert React Code Reviewer.
    Your task is to inspect the generated code for major flaws:
    1. Does it use raw HTML structures like <html>, <head>, or <body> instead of basic React layout tags?
    2. Did it forget to export the default component via 'export default App;'?
    3. Does it contain random floating string errors like "javascript;" or code-block backticks?
    4. Make sure it does not export external files from outside that are not part of basic react such as imports DarkThemeProvider and more that are not usually installedd inside a normal react file
    5. Make sure there exists export default App at the end

    CRITICAL OUTPUT FORMATTING:
    - If the code is perfect and ready to run, output EXACTLY the word: PASSED, say only PASSED do not include caution notes.
    - If the code has mistakes, write a clear, bulleted instruction guide listing exactly what needs to be fixed. Do NOT include code blocks in your review feedback, just text instructions.
    """

    full_prompt = f"{system_instruction}\n\nGenerated Code to Review:\n{state['generated_code']}"

    ai_message = llm.invoke(full_prompt)
    review_feedback = ai_message.content.strip()

    print(f"Review Verdict:\n{review_feedback}")

    return {"review_feedback": review_feedback}