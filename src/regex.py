import re

def resolve_query_regex(nl_question: str) -> str | None:
    """
    Maps common natural language patterns to simple MySQL queries.
    If no regex matches, return None so the LLM can handle it.
    """
    q = re.sub(r"\s+", " ", nl_question.lower()).strip()

    # Show all tables
    if re.search(r"\b(show|list|get|display)\b.*\btables?\b", q):
        return "SHOW TABLES;"

    # Count rows in a specific table
    m = re.search(r"how many (rows|records|entries) (are in|in) (\w+)", q)
    if m:
        table = m.group(3)
        return f"SELECT COUNT(*) FROM `{table}`;"

    # Show all rows in a table (limit to 20 for safety)
    m = re.search(r"(show|list|get|display).*(all )?(rows|records|entries|data).*from (\w+)", q)
    if m:
        table = m.group(4)
        return f"SELECT * FROM `{table}` LIMIT 20;"

    # Select specific columns from a table
    m = re.search(r"show (.+) from (\w+)", q)
    if m:
        cols = ", ".join([c.strip() for c in m.group(1).split(",")])
        table = m.group(2)
        return f"SELECT {cols} FROM `{table}` LIMIT 20;"

    # Default: let the LLM handle it
    return None
