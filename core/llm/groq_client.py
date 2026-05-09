from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

def load_llm(model_name, temperature):

    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model=model_name,
        temperature=temperature
    )