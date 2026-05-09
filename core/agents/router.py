def route_query(query):

    query = query.lower()

    web_keywords = [
        "latest",
        "news",
        "current",
        "today",
        "recent",
        "2025",
        "2026"
    ]

    pdf_keywords = [
        "document",
        "pdf",
        "according to",
        "in the file"
    ]

    use_web = any(
        word in query for word in web_keywords
    )

    use_pdf = any(
        word in query for word in pdf_keywords
    )

    if use_web and use_pdf:
        return "hybrid"

    elif use_web:
        return "web"

    elif use_pdf:
        return "pdf"

    else:
        return "general"