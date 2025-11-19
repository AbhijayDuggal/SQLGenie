SYSTEM_PROMPT = """
You are an expert SQL generator.
Rules:
1. Always generate valid SQL.
2. Do not invent columns or tables.
3. Only use the tables and columns provided in the schema.
4. Return ONLY the SQL query. Do not include any explanations, text, or markdown formatting.
5. Do not include any leading words like 'sql' or '```sql'.
"""

def build_prompt(query, schema_info):
    """
    Build a prompt for the LLM dynamically using the provided schema info.
    
    Parameters:
        query (str): User's natural language question.
        schema_info (list of str): List of table and column descriptions.
    
    Returns:
        str: Complete prompt to send to the LLM.
    """
    schema_text = "\n".join(schema_info) if schema_info else "No schema information available."

    prompt = (
        SYSTEM_PROMPT +
        "\n\nSchema Information:\n" +
        schema_text +
        "\n\nUser Question:\n" +
        f"{query}\n\n-- Only write the SQL query below, nothing else:"
    )

    return prompt

