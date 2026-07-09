from src.graph import compiled_graph

if __name__ =="__main__":
    print("Initializing Multi-Agent Local Code Generation Pipeline...")

    initial_state = {
        "user_prompt": "Create a clean, dark-themed dashboard overview page with statistics widgets.",
        "project_plan": "",
        "file_layout": "",
        "generated_code": "",
        "final_code": "",
        "review_feedback": ""
    }
    compiled_graph.invoke(initial_state)