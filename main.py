from src.graph import compiled_graph

if __name__ =="__main__":
    print("Initializing Multi-Agent Local Code Generation Pipeline...")
    
    user_prompt = input("Enter the project you want to build:\n>")
    initial_state = {
        "user_prompt": user_prompt,
        "is_sufficient": False,
        "missing_fields": [],
        "extracted_data": None,
        "clarification_question": "",
        "project_plan": "",
        "file_layout": "",
        "generated_code": "",
        "final_code": "",
        "review_feedback": ""
    }
    
    while True:
        initial_state = compiled_graph.invoke(initial_state) 
        if initial_state["is_sufficient"]:
            break
        print(initial_state["clarification_question"])
        reply = input("> ")
        initial_state["user_prompt"] += "\n" + reply

        print(initial_state["extracted_data"])