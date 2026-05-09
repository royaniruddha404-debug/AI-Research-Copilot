def format_sources(docs):

    sources = []

    for doc in docs:

        page = doc.metadata.get("page", "Unknown")

        source = {
            "page": page + 1,
            "content": doc.page_content[:300]
        }

        sources.append(source)

    return sources