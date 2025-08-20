import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import streamlit as st

from prompt import PROMPT
from regex import resolve_query_regex

load_dotenv()


# --------------------------
# LLM setup
# --------------------------
def get_response(input, provider="GROQ"):
    match provider:
        case "GROQ":
            llm = ChatGroq(
                api_key=os.getenv("GROQ_API_KEY"),
                model_name="llama3-8b-8192"
            )
            return llm.invoke(input)
        case _:
            st.error("Error: Unknown API Provider")
            return None


# --------------------------
# Helpers
# --------------------------
def compress_text(text: str, max_lines: int = 500) -> str:
    lines = text.strip().splitlines()
    return "\n".join(lines[:max_lines]) + ("\n#...truncated" if len(lines) > max_lines else "")

# --------------------------
# Sanitize SQL (T-SQL → MySQL)
# --------------------------
# def fix_tsql_to_mysql(sql: str) -> str:
#     if not sql:
#         return sql
#     sql = sql.replace("[", "`").replace("]", "`")  # Brackets → backticks
#     sql = sql.replace("TOP 1000", "LIMIT 1000")
#     sql = sql.replace("TOP (1000)", "LIMIT 1000")
#     return sql.strip()

# --------------------------
# SQL Generation (NL → SQL)
# --------------------------
def generate_sql_from_nl(nl_question: str, provider: str = "GROQ") -> str:
    try:
        with open("context/schema.sql") as f:
            schema_context = f.read()
    except FileNotFoundError:
        st.error("❌ schema.sql not found in /context directory")
        return ""

    prompt = PROMPT.format(
        compressed_schema=compress_text(schema_context),
        nl_question=nl_question
    )

    response = get_response([HumanMessage(content=prompt)], provider=provider)
    output = response.content.strip(" `-")

    return output   # ensure MySQL-compatible output

# --------------------------
# Handle NL Query (Regex or LLM)
# --------------------------
def handle_nl_query(nl_question: str, provider: str, mode: str = "llm") -> str:
    if mode == "regex":
        return resolve_query_regex(nl_question).strip()
    elif mode == "llm":
        return generate_sql_from_nl(nl_question, provider=provider)
    else:
        st.error("❌ Unknown query mode")
        return ""


# --------------------------
# Format results to NL
# --------------------------
def format_result_to_nl(question: str, result):
    if result.empty:
        return "🔍 I couldn't find any relevant data."

    value = result.values
    value = value.item() if value.size == 1 else value.tolist()
    return str(value)
