def chatbot(query):
    query = query.lower()

    if "what should i do" in query:
        return "Start your highest priority task now."

    elif "productive" in query:
        return "You are most productive at night."

    elif "schedule" in query:
        return "Check your generated schedule for optimal planning."

    elif "break" in query:
        return "Take a 10-15 minute break after long tasks."
    
    elif "tired" in query:
        return "Take a short break and relax."

    return "I'm your AI assistant. Ask me about your tasks or productivity!"