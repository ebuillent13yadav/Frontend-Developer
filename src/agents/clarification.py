from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from state import ProjectState,Specifications

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
{user_prompt}
"""
)

llm = ChatOllama(model="qwen2.5:7b",temperature=0)
structured_llm = llm.with_structured_output(Evaluation)

def clarification_node(state: ProjectState):
    chain = prompt|structured_llm  ## Prompt ---> LLM

    result = chain.invoke({
        "user_prompt": state["user_prompt"]
    })

    return{
        "is_sufficient": result.is_sufficient,
        "missing_fields": result.missing_fields,
        "extracted_data": result.extracted_data,
        "clarification_question": result.clarification_question,
    }
  






