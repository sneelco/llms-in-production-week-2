PROMPT = """
Generate a valid SQL query for the following natural language instruction:

If asked for a count use a descriptive alias in your SQL query.

Only generate SQL code as a plain text string on a single line with no formatting or markdown.

Query: ${query}

${gr.complete_json_suffix_v3}
"""
