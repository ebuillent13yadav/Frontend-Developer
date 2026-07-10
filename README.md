----/-/-/-/-/-/-/-/-/---FOR CLARIFICATION AGENT---/-/-/-/-/-/-/-/-/----

                User
                  │
                  ▼
         Terminal Input (input())
                  │
                  ▼
         Create Initial AgentState
                  │
                  ▼
         LangGraph Entry Point
                  │
                  ▼
        Clarification Agent(Node)
                  │
                  ▼
      Prompt + Structured Output
                  │
                  ▼
         LLM Evaluates Request
                  │
          ┌───────┴────────┐
          │                │
          ▼                ▼
   Sufficient? No     Sufficient? Yes
          │                │
          ▼                ▼
Generate Clarification     Return Specification
Question                   │
          │                ▼
          ▼          Update AgentState
 Display Question          │
          │                ▼
          ▼         Continue to Next Agent
 User Enters Reply
          │
          ▼
 Update user_input
          │
          ▼
 Run Clarification Again

                      