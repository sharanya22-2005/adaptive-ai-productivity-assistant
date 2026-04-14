def chatbot(query):
    query = query.lower()

    if "what should i do" in query:
        return "You should follow your schedule."

    elif "productive" in query:
        return "You are most productive at night."

    return "I didn't understand."