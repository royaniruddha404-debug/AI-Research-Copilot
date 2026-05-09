def generate_search_query(
    llm,
    user_question,
    pdf_context
):

    prompt = f"""
You are a search query generator.

Based on the user question and the document context,
generate a SHORT and EFFECTIVE web search query.

User Question:
{user_question}

Document Context:
{pdf_context[:1000]}

Only return the search query.
"""

    response = llm.invoke(prompt)

    return response.content.strip()