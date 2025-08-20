import re

def resolve_query_regex(nl_question: str) -> str | None:
    """
    Maps natural language questions to SQL queries for the Hotel_Room_Booking schema.
    Falls back to LLM if no regex matches.
    """
    q = re.sub(r"\s+", " ", nl_question.lower()).strip()

    # Show all tables
    if re.search(r"\b(show|list|get|display)\b.*\btables?\b", q):
        return "SHOW TABLES;"

    # Count hotels
    if re.search(r"\bhow many\b.*\bhotels?\b", q):
        return "SELECT COUNT(*) FROM Hotel;"

    # List hotels
    if re.search(r"\b(list|show|get|display)\b.*\bhotels?\b", q):
        return "SELECT Hotel_id, Hotel_Name, Hotel_type, Pincode FROM Hotel LIMIT 20;"

    # Count rooms
    if re.search(r"\bhow many\b.*\brooms?\b", q):
        return "SELECT COUNT(*) FROM Room;"

    # List available rooms
    if re.search(r"\b(show|list|get|display)\b.*\bavailable\b.*\brooms?\b", q):
        return "SELECT Room_id, Room_no, Room_type, Hotel_id FROM Room WHERE Availability = 'Yes' LIMIT 20;"

    # Count customers
    if re.search(r"\bhow many\b.*\bcustomers?\b", q):
        return "SELECT COUNT(*) FROM Customer;"

    # List customers
    if re.search(r"\b(list|show|get|display)\b.*\bcustomers?\b", q):
        return "SELECT Customer_id, Customer_name, Email, Pincode FROM Customer LIMIT 20;"

    # List bookings
    if re.search(r"\b(list|show|get|display)\b.*\bbookings?\b", q):
        return """SELECT Booking_id, Booking_title, Booking_date, Check_in_date, Check_out_date, Room_id, Customer_id
                  FROM Booking LIMIT 20;"""

    # Count bookings
    if re.search(r"\bhow many\b.*\bbookings?\b", q):
        return "SELECT COUNT(*) FROM Booking;"

    # List payments
    if re.search(r"\b(list|show|get|display)\b.*\bpayments?\b", q):
        return "SELECT Payment_id, Booking_id, Date, Amount FROM Payment LIMIT 20;"

    # Fallback: let the LLM handle it
    return None
