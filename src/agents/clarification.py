from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END


class Specifications(BaseModel):
    framework_preference: str | None = Field(None,description = "React, Next.js, TypeScript, etc.")
    styling_library: str | None = Field(None,description = "Tailwind CSS,Shaden UI,Bootstrap, etc.")
    theme: str | None = Field(None,description = "Dark Mode,Minimalist Dark Mode, etc.")
    complexity: str | None = Field(None,description = "Dashboard, Landing Page, Custom UI, etc.")

class Evaluation(BaseModel):
    is_sufficient: bool = Field(...,description = "True if all 4 parameters are present")    
    extracted_data: Specifications
    missing_fields: list[str] = Field(description = "List of required details that are missing")
    reasoning: str = Field(description = "Brief explanation of why the input is or is not sufficient")
    clarification_question: str = Field(description= "A natural language question asking for the missing details.")

class AgentState(TypedDict):
    user_input: str
    is_sufficient: bool
    missing_fields: list[str]
    extracted_data: Specifications|None # initially it clould be none
    clarification_question: str

    
prompt = ChatPromptTemplate.from_template("""
You are a Clarification Agent for an AI Website Generator.

Your task is to analyze the user's project request and determine whether it contains enough information to start website development.

The required specifications are:
1. Framework Preference (e.g., React, Next.js, Angular, Vue)
2. Styling Library (e.g., Tailwind CSS, Bootstrap, Shadcn UI)
3. Theme (e.g., Dark, Light, Minimalist)
4. Complexity (e.g., Landing Page, Portfolio, Dashboard, Admin Panel)

Instructions:
- Extract all specifications that are explicitly mentioned.
- If all four specifications are present:
  - Set is_sufficient = true.
  - Return the extracted specifications.
  - Set missing_fields to an empty list.
  - Set clarification_question to an empty string.
- If one or more specifications are missing:
  - Set is_sufficient = false.
  - List only the missing specifications in missing_fields.
  - Generate one natural clarification question asking only for the missing specifications.
- Do not ask about information that has already been provided.
- Return the response according to the Evaluation schema.

User Request:
{user_input}
"""
)

llm = ChatOllama(model="qwen2.5:7b",temperature=0)
structured_llm = llm.with_structured_output(Evaluation)

def clarification_node(state: AgentState):
    chain = prompt|structured_llm  ## Prompt ---> LLM

    result = chain.invoke({
        "user_input": state["user_input"]
    })

    state["is_sufficient"] = result.is_sufficient
    state["missing_fields"] = result.missing_fields
    state["extracted_data"] = result.extracted_data
    state["clarification_question"] = result.clarification_question

    return state

##-----##----Graph----##-----##

builder = StateGraph(AgentState)

builder.add_node("clarification",clarification_node)
builder.set_entry_point("clarification")
builder.add_edge("clarification",END)

graph = builder.compile()

user = input("Enter the Project you wanna Build:\n ")

initial_state: AgentState = {
    "user_input": user,
    "is_sufficient": False,
    "missing_fields": [],
    "extracted_data": None,
    "clarification_question": ""
}

result = graph.invoke(initial_state)

print("\nEvaluation\n")

while not result["is_sufficient"]:
    print(result["clarification_question"])
    reply = input("> ")
    result["user_input"] += "\n" + reply

    result = graph.invoke(result) ## result gets updated after each iteration 
    
print(result["extracted_data"])    






