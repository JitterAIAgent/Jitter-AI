def print_being_details(being):
    print("\n" + "="*50)
    print("             BEING CONFIGURATION")
    print("="*50)
    
    print("\n" + "-"*20 + " PROVIDER " + "-"*20)
    print(f"Model Provider: {being['modelProvider']}")
    print(f"System Prompt: {being['system']}")
    
    print("\n" + "-"*20 + " CHARACTER " + "-"*20)
    print(f"Name: {being['name']}")
    print(f"Bio: {being['bio']}")
    print(f"Personality: {being['personality']}")
    print(f"Context ID: {being['contextId']}")
    
    print("\n" + "-"*20 + " KNOWLEDGE " + "-"*20)
    print(f"Knowledge Documents: {len(being['knowledge'])}")
    print(f"Example Responses: {len(being['exampleResponses'])}")
    print("\n" + "="*50 + "\n")