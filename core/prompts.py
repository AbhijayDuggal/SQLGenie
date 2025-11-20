SYSTEM_PROMPT = """
You are an expert SQL generator.

Rules:
1. Always generate valid SQL.
2. Do not invent columns or tables.
3. Only use the tables and columns provided in the schema.
4. Use context from the conversation history to understand follow-up questions.
5. Return ONLY the SQL query. No explanations, no extra text, no markdown.
6. Do NOT include ``` blocks or any prefix like 'sql'.
7. Output must contain SQL only, nothing else.
"""

def build_prompt(query, schema_info, chat_history=None, db_type="sqlite"):
    """
    Build an LLM prompt using:
    - User query
    - Schema info
    - Chat history (for follow-up questions)
    - Database type (sqlite or mysql)

    Parameters:
        query (str): New user question.
        schema_info (list of str): Database schema info.
        chat_history (list): List of (role, message) tuples.
        db_type (str): Type of database to generate SQL for ("sqlite" or "mysql").

    Returns:
        str: Final prompt.
    """

    schema_text = "\n".join(schema_info) if schema_info else "No schema information available."

    # Build conversation transcript
    history_text = ""
    if chat_history:
        for role, message in chat_history:
            history_text += f"{role}: {message}\n"

    prompt = (
        SYSTEM_PROMPT
        + f"\n\nDatabase Type: {db_type}\n"
        + "Schema Information:\n"
        + schema_text
        + "\n\nConversation History:\n"
        + history_text
        + "\nUser:\n"
        + query
        + "\n\n-- Write ONLY the SQL query below, compatible with the specified database:\n"
    )

    return prompt
