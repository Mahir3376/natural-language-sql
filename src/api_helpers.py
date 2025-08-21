import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import streamlit as st

from prompt import PROMPT

load_dotenv()


# LLM setup
def get_response(input_messages, provider="GROQ"):
    if provider == "GROQ":
        llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama3-8b-8192"
        )
        return llm.invoke(input_messages)
    else:
        st.error(f"Unknown API provider: {provider}")
        return None


# Helpers
def compress_text(text: str, max_lines: int = 500) -> str:
    lines = text.strip().splitlines()
    return "\n".join(lines[:max_lines]) + ("\n#...truncated" if len(lines) > max_lines else "")

@st.cache_data
def load_schema(path="context/schema.sql") -> str:
    with open(path) as f:
        return f.read()

# SQL Generation (NL → SQL)
def generate_sql_from_nl(nl_question: str, provider: str = "GROQ") -> str:
    try:
        schema_context = load_schema()
    except FileNotFoundError:
        st.error("schema.sql not found in /context directory")
        return ""

    prompt = PROMPT.format(
        compressed_schema=compress_text(schema_context),
        nl_question=nl_question
    )

    response = get_response([HumanMessage(content=prompt)], provider=provider)
    if response and hasattr(response, "content"):
        return response.content.strip(" `-")
    return ""


# To handle NL Query
def handle_nl_query(nl_question: str, source: str = "GROQ") -> str:
    if source not in ["GROQ", "OpenAI"]:
        st.error(f"Unknown provider: {source}")
        return ""
    sql_query = generate_sql_from_nl(nl_question, provider=source)
    return sql_query.strip() if sql_query else ""

# Format results to NL
def format_result_to_nl(question: str, result) -> str:
    if result.empty:
        return "I couldn't find any relevant data."

    value = result.values
    return str(value.item() if value.size == 1 else value.tolist())