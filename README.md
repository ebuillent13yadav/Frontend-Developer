----/-/-/-/-/-/-/-/-/---FOR CLARIFICATION AGENT---/-/-/-/-/-/-/-/-/----

                  User
                    │
                    ▼
        Terminal (input())
                    │
                    ▼
            Initial AgentState
                    │
                    ▼
         LangGraph Entry Point
                    │
                    ▼
        Clarification Agent(Node)
                    │
        ┌───────────┴────────────┐
        │                        │
        ▼                        ▼
 Information              Information
 Insufficient             Sufficient
        │                        │
        ▼                        ▼
Ask Clarification       Extract Specifications
Questions                     │
        │                      ▼
        └──────────────► Evaluation
                               │
                               ▼
                      Updated AgentState
                               │
                               ▼
                      Return to Terminal

                      