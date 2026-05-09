AI Research Copilot

An AI-powered multi-source research assistant that combines Groq LLMs, RAG (Retrieval-Augmented Generation), web search (Tavily), and YouTube intelligence to help users understand documents, explore the web, and learn from videos — all in one unified Streamlit interface.

Live Demo

https://your-streamlit-app-link.streamlit.app

Features:
PDF Intelligence (RAG)
Upload PDFs and chat with them
Context-aware answers using vector search
Source-based responses (citations supported)

Web Research Assistant
Real-time web search using Tavily API
AI-generated answers grounded in search results
Hybrid mode: PDF + Web reasoning

YouTube Learning Assistant
Search YouTube videos by topic
Fetch video transcripts (when available)
AI-powered video summarization
Metadata fallback when transcripts are unavailable

AI Chat Assistant
Powered by Groq LLMs (LLaMA / Mixtral)
Streaming responses

Multi-turn conversation support
Model Control Panel
Choose between multiple Groq models
Adjust temperature for creativity control

System Architecture
User Query
    ↓
Streamlit UI
    ↓
Route Decision (Chat / PDF / Web / YouTube)
    ↓
────────────────────────────
|  RAG Pipeline            |
|  Web Search (Tavily)     |
|  YouTube API + Transcript|
────────────────────────────
    ↓
Context Builder
    ↓
Groq LLM (LLaMA / Mixtral)
    ↓
Final Answer + Citations

Tech Stack
Frontend: Streamlit
LLM Provider: Groq (LLaMA 3 / Mixtral)
Framework: LangChain
Vector Store: FAISS (or equivalent)
Web Search: Tavily API
Video Intelligence: YouTube Data API + Transcript API
Language: Python


Main Dashboard

PDF Chat

Web Research

YouTube Assistant

Installation & Setup
1. Clone repository
git clone https://github.com/royaniruddha404-debug/AI-Research-Copilot.git
cd ai-research-copilot

2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

3. Install dependencies
pip install -r requirements.txt

4. Add environment variables
Create a .env file:
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
YOUTUBE_API_KEY=your_youtube_api_key

5. Run the app
streamlit run app.py


Key Design Highlights:
Some YouTube videos may not have transcripts (handled with fallback)
Modular tool-based architecture
Multi-source reasoning (PDF + Web + Video)
LLM routing system (hybrid intelligence)
Production-style Streamlit UI
Fallback handling for missing data

Future Improvements:
GitHub repository analyzer
Agent-based autonomous planning system
Memory-based long-term chat history
Advanced reranking for RAG

Author:
Aniruddha Roy

⭐ If you like this project

Give it a ⭐ on GitHub it helps a lot!
