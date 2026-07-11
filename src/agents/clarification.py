from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from src.state import ProjectState,Specifications

class Evaluation(BaseModel):
    is_sufficient: bool = Field(...,description = "True if all 4 parameters are present")    
    extracted_data: Specifications
    missing_fields: list[str] = Field(description = "List of required details that are missing")
    reasoning: str = Field(description = "Brief explanation of why the input is or is not sufficient")
    clarification_question: str = Field(description= "A natural language question asking for the missing details.")

    
prompt = ChatPromptTemplate.from_template("""
You are a Clarification Agent for an AI Website Generator.

Your task is to analyze the user's project request and determine whether it contains enough information to start website development.

The required specifications are:
1. Framework Preference (e.g., React, Next.js, Angular, Vue)
2. Styling Library (e.g., Tailwind CSS, Bootstrap, Shadcn UI)
3. Theme (e.g., Dark, Light, Minimalist)
4. Complexity (e.g., Landing Page, Portfolio, Dashboard, Admin Panel)

Instructions:
- Extract all specifications that are explicitly mentioned or can be confidently inferred from the user's wording.
- Interpret natural language and synonymous phrases correctly.
- The User Request may contain the original request followed by one or more clarification responses.
- Treat the entire User Request as a cumulative conversation.
- When the user provides additional clarification in later turns, combine it with the previously extracted information.
- Do not discard specifications that were extracted earlier.
- Do not ask about information that has already been provided.
- Only ask about fields that are still missing.
- If the user gives a clear answer that maps to one of the required specifications, extract it even if the wording is informal.

Examples:

- "React based frontend framework"
  -> framework_preference = "React"

- "I prefer React"
  -> framework_preference = "React"

- "Let's use Next.js"
  -> framework_preference = "Next.js"

- "Tailwind CSS styling would be preferred"
  -> styling_library = "Tailwind CSS"

- "Use Bootstrap for styling"
  -> styling_library = "Bootstrap"

- "Dark-themed website"
  -> theme = "Dark"

- "Minimalist dark interface"
  -> theme = "Minimalist Dark"

- "Dashboard overview page"
  -> complexity = "Dashboard"

- "Build me a landing page"
  -> complexity = "Landing Page"

Decision Rules:

- If all four specifications are present:
  - Set is_sufficient = true.
  - Return all extracted specifications.
  - Set missing_fields to an empty list.
  - Set clarification_question to an empty string.

- If one or more specifications are missing:
  - Set is_sufficient = false.
  - List ONLY the missing specifications in missing_fields.
  - Generate ONE natural clarification question asking ONLY for the missing specifications.
  - Never ask about specifications that have already been provided.

Return the response strictly according to the Evaluation schema.

User Request:
{user_prompt}
""")

llm = ChatOllama(model="qwen2.5:7b",temperature=0)
structured_llm = llm.with_structured_output(Evaluation)

def clarification_node(state: ProjectState):
    chain = prompt|structured_llm  ## Prompt ---> LLM
    print("\n===== USER PROMPT =====")
    print(state["user_prompt"])

    result = chain.invoke({
        "user_prompt": state["user_prompt"]
    })
    print("\n===RAW EVALUATION==")
    print(result.model_dump_json(indent=2))

    specs = result.extracted_data
    
    missing_fields = []
    if not specs.framework_preference:
        missing_fields.append("Framework Preference")
    if not specs.styling_library:
        missing_fields.append("Styling Library")
    if not specs.theme:
        missing_fields.append("Theme")
    if not specs.complexity:
        missing_fields.append("Complexity")

    is_sufficient = len(missing_fields) == 0
   
    return{
        "is_sufficient": is_sufficient,
        "missing_fields": missing_fields,
        "extracted_data": specs,
        "clarification_question": result.clarification_question,
    }
  






