from src.graph import compiled_graph

if __name__ =="__main__":
    print("Initializing Multi-Agent Local Code Generation Pipeline...")

    initial_state = {
        "user_prompt": "Create a clean, dark-themed dashboard overview page with statistics widgets.",
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
    state = initial_state
    while True:
        state = compiled_graph.invoke(state) 
        if state["is_sufficient"]:
            break
        print(state["clarification_question"])
        reply = input("> ")
        state["user_prompt"] += "\n" + reply

        print(state["extracted_data"])