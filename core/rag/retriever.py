def retrieve_docs(vectorstore, query):

    retriever = vectorstore.as_retriever()

    docs = retriever.invoke(query)

    return docs