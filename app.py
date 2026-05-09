import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os
from core.llm.groq_client import load_llm

from core.tools.web_search import (
    web_search,
    format_web_results
)

from core.agents.router import route_query

from core.tools.query_generator import (
    generate_search_query
)

from core.tools.youtube_tool import (
    search_youtube,
    get_transcript,
    summarize_video
)



load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


st.set_page_config(
    page_title="AI Research Copilot",
    layout="wide"
)

use_web = st.sidebar.checkbox(
    "Enable Web Search",
    value=True
)

if "summary" not in st.session_state:
    st.session_state.summary = None

if "active_video" not in st.session_state:
    st.session_state.active_video = None



with st.sidebar:

    st.title("AI Research Copilot")

    uploaded_file = st.sidebar.file_uploader(
        "Upload PDF",
        type="pdf"
    )

    model_name = st.selectbox(
        "Select Model",
        [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
        ]
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    st.divider()

    st.markdown("### Features")
    st.markdown("- 💬 Chat")
    st.markdown("- 📄 PDF RAG")
    st.markdown("- 🌐 Web Search")
    st.markdown("- 🎥 YouTube Summarizer")
    st.markdown("- 💻 GitHub Analyzer (Coming Soon)")


if uploaded_file:

    from core.rag.pdf_loader import load_pdf
    from core.rag.chunking import chunk_documents
    from core.rag.vectorstore import create_vectorstore

    documents = load_pdf(uploaded_file)

    chunks = chunk_documents(documents)

    vectorstore = create_vectorstore(chunks)

    st.session_state.vectorstore = vectorstore

    st.success("PDF processed successfully!")


llm = load_llm(model_name, temperature)

#Code assistant
st.header("Code Assistant")

code_input = st.text_area("Paste your code here")

task = st.selectbox(
    "Task",
    ["explain", "debug", "optimize", "convert"]
)

if st.button("Run Code Assistant"):

    from core.tools.code_tool import analyze_code

    result = analyze_code(llm, code_input, task)

    st.write(result)

#Youtube assistant
st.header("YouTube Learning Assistant")

if "summary" not in st.session_state:
    st.session_state.summary = None

if "active_video" not in st.session_state:
    st.session_state.active_video = None


query = st.text_input("Search topic")

if st.button("Search Videos"):

    if not query:
        st.warning("Enter a topic")

    else:
        st.session_state.videos = search_youtube(query)
        st.session_state.summary = None  # reset old summary


if "videos" in st.session_state:

    for v in st.session_state.videos:

        st.image(v["thumbnail"], width=250)

        st.markdown(f"### {v['title']}")
        st.write(v["channel"])
        st.write(v["link"])

        
        if st.button(
            f"Summarize this video",
            key=f"sum_{v['video_id']}"
        ):

            st.session_state.active_video = v["video_id"]

            transcript = get_transcript(v["video_id"])

            if transcript:

                summary = summarize_video(llm, transcript)

            else:

                fallback = f"""
                Video Title: {v['title']}
                Channel: {v['channel']}
                URL: {v['link']}
                """

                summary = llm.invoke(f"""
                You are a study assistant.

                Summarize this YouTube video based on its metadata.
                Explain what the video is likely about and what a learner can expect.

                {fallback}
                """).content

            st.session_state.summary = summary


if st.session_state.summary:

    st.success("Summary")

    st.write(st.session_state.summary)




if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("AI Research Copilot")

st.caption("Powered by Groq + LangChain")


for message in st.session_state.messages:

    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)

    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)


user_input = st.chat_input("Ask anything...")

if user_input:

  
    st.session_state.messages.append(HumanMessage(content=user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        full_response = ""

    try:

        route = route_query(user_input)
        st.write(f"Route: {route}")

        pdf_context = ""
        web_context = ""

        sources = []
        web_results = []

    

        if route in ["pdf", "hybrid"] and \
        "vectorstore" in st.session_state:

            from core.rag.retriever import retrieve_docs
            from core.rag.citations import format_sources

            docs = retrieve_docs(
                st.session_state.vectorstore,
                user_input
            )

            sources = format_sources(docs)

            pdf_context = "\n\n".join(
                [doc.page_content for doc in docs]
            )

        web_results = []
        web_context = ""

        if use_web and route in ["web", "hybrid"]:

            search_query = generate_search_query(
                llm,
                user_input,
                pdf_context
            )

            st.write(search_query)

            web_results = web_search(search_query)

            web_context = format_web_results(
                web_results
            )

        prompt = f"""
    You are an AI research assistant.

    Answer the question using the provided contexts.

    PDF Context:
    {pdf_context}

    Web Context:
    {web_context}

    Question:
    {user_input}

    Provide a detailed and accurate answer.
    """

        

        response = llm.stream(prompt)

        for chunk in response:

            if chunk.content:

                full_response += chunk.content

                response_placeholder.markdown(
                    full_response + "▌"
                )

        response_placeholder.markdown(full_response)


        if sources:

            with st.expander("PDF Sources"):

                for i, source in enumerate(sources):

                    st.markdown(
                        f"### Source {i+1}"
                    )

                    st.markdown(
                        f"**Page:** {source['page']}"
                    )

                    st.write(source["content"])

    
        if web_results:

            with st.expander("Web Sources"):

                for result in web_results:

                    st.markdown(
                        f"### {result['title']}"
                    )

                    st.write(result["url"])

    except Exception as e:

        st.error(f"Error: {e}")

  
    st.session_state.messages.append(
        AIMessage(content=full_response)
    )