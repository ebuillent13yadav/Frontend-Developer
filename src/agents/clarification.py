from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

user_input = input("Enter the Project you wanna Build: ")

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

class AgentState(TypedDict):
    user_input: str
    is_sufficient: bool
    missing_fields: list[str]
    extracted_data: Specifications|None # initially it clould be none

    
prompt = ChatPromptTemplate("""
You are a Clarification Agent.

Analyze the user's software request.

Determine whether these four parameters are present.

1. Framework
2. Styling Library
3. Theme
4. Complexity

Return output according to Evaluation schema.

User Request:

{user_input}
"""
)

llm = ChatOllama(model="qwen2.5:7b",temperature=0)




