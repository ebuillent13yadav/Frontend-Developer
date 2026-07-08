from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5:7b")

system_prompt = system_prompt = """You are an automated code generation backend engine. You are NOT a conversational AI assistant.

CRITICAL INSTRUCTIONS FOR OUTPUT FORMATTING:
1. Output ONLY valid, executable JavaScript/React source code.
2. Do NOT write any introduction (e.g., "Sure, here is your component...").
3. Do NOT write any explanation or conclusion at the end.
4. Do NOT wrap the code inside markdown code blocks. Absolutely NO triple backticks (```jsx or ```).
5. Start your response directly with the first line of code (e.g., import React... or function App...).

TECHNICAL APP REQUIREMENT:
Generate a single-file React component using standard HTML elements and inline styles or Tailwind CSS utility classes. Ensure all variables and components are fully self-contained in this single output. Everything must export as default.
"""

user_request = user_request = """Create a gorgeous personal developer portfolio landing page. 
CRITICAL RULE: Use ONLY standard basic HTML layout tags: div, h1, h2, p, button, nav, a, section, footer. 
Do NOT use table tags, do NOT use the word 'import' for UI libraries, and do NOT use any external component packages. 
Style the sections beautifully using basic React inline styling, for example: style={{ backgroundColor: '#0f172a', color: '#f8fafc', padding: '40px', fontFamily: 'sans-serif' }}. 
Make sure it has a hero section, an 'About Me' section, and a 'Projects' section with cards made from divs."""

full_prompt = f"{system_prompt}\n\nUser request: {user_request}"

raw_react_code = llm.invoke(full_prompt)

with open(r"my-generated-app\src\App.jsx", "w") as f:
    f.write(raw_react_code)

print("Done")