# Unless you want to explicitly use pre-defined queries in case of large scale db, don't uncomment this code

# import re

# def resolve_query_regex(nl_question: str) -> str | None:
#     """
#     Maps natural language questions to SQL queries for the Hotel_Room_Booking schema.
#     Falls back to LLM if no regex matches.
#     """
#     q = re.sub(r"\s+", " ", nl_question.lower()).strip()

#     # Show all tables
#     if re.search(r"\b(show|list|get|display)\b.*\btables?\b", q):
#         return "SHOW TABLES;"

#     # -------------------
#     # Hotel
#     # -------------------
#     if re.search(r"\bhow many\b.*\bhotels?\b", q):
#         return "SELECT COUNT(*) FROM `Hotel`;"
#     if re.search(r"\b(list|show|get|display)\b.*\bhotels?\b", q):
#         return "SELECT `Hotel_id`, `Hotel_Name`, `Hotel_type`, `Pincode` FROM `Hotel` LIMIT 20;"

#     # -------------------
#     # Rooms
#     # -------------------
#     if re.search(r"\bhow many\b.*\brooms?\b", q):
#         return "SELECT COUNT(*) FROM `Room`;"
#     if re.search(r"\b(show|list|get|display)\b.*\bavailable\b.*\brooms?\b", q):
#         return "SELECT `Room_id`, `Room_no`, `Room_type`, `Hotel_id` FROM `Room` WHERE `Availability` = 'Yes' LIMIT 20;"
#     if re.search(r"\b(list|show|get|display)\b.*\brooms?\b", q):
#         return "SELECT `Room_id`, `Room_no`, `Room_type`, `Availability`, `Hotel_id` FROM `Room` LIMIT 20;"

#     # -------------------
#     # Customers & Guests
#     # -------------------
#     if re.search(r"\bhow many\b.*\bcustomers?\b", q):
#         return "SELECT COUNT(*) FROM `Customer`;"
#     if re.search(r"\b(list|show|get|display)\b.*\bcustomers?\b", q):
#         return "SELECT `Customer_id`, `Customer_name`, `Email`, `Pincode` FROM `Customer` LIMIT 20;"
#     if re.search(r"\b(list|show|get|display)\b.*\bguests?\b", q):
#         return "SELECT g.`Customer_id`, c.`Customer_name`, g.`Guest_type`, g.`Preferred_roomtype` FROM `Guest` g JOIN `Customer` c ON g.`Customer_id` = c.`Customer_id` LIMIT 20;"

#     # -------------------
#     # Customer contacts
#     # -------------------
#     if re.search(r"\b(list|show|get|display)\b.*\bcontacts?\b.*\bcustomers?\b", q):
#         return "SELECT `Customer_id`, `Contact_num` FROM `CustomerContact` LIMIT 20;"

#     # -------------------
#     # Bookings
#     # -------------------
#     if re.search(r"\bhow many\b.*\bbookings?\b", q):
#         return "SELECT COUNT(*) FROM `Booking`;"
#     if re.search(r"\b(list|show|get|display)\b.*\bbookings?\b", q):
#         return """SELECT b.`Booking_id`, b.`Booking_title`, b.`Booking_date`, b.`Check_in_date`, b.`Check_out_date`,
#                           c.`Customer_name`, r.`Room_no`, h.`Hotel_Name`
#                    FROM `Booking` b
#                    JOIN `Customer` c ON b.`Customer_id` = c.`Customer_id`
#                    JOIN `Room` r ON b.`Room_id` = r.`Room_id`
#                    JOIN `Hotel` h ON r.`Hotel_id` = h.`Hotel_id`
#                    LIMIT 20;"""

#     # -------------------
#     # Payments
#     # -------------------
#     if re.search(r"\bhow many\b.*\bpayments?\b", q):
#         return "SELECT COUNT(*) FROM `Payment`;"
#     if re.search(r"\b(list|show|get|display)\b.*\bpayments?\b", q):
#         return "SELECT `Payment_id`, `Booking_id`, `Date`, `Amount` FROM `Payment` LIMIT 20;"

#     # -------------------
#     # Services & Offers
#     # -------------------
#     if re.search(r"\b(list|show|get|display)\b.*\bservices?\b", q):
#         return "SELECT `Service_id`, `Service_name`, `Service_type` FROM `Service` LIMIT 20;"
#     if re.search(r"\bwhat\b.*\bservices?\b.*\b(hotel|hotels)\b", q) or re.search(r"\bservices?\b.*\boffered\b", q):
#         return """SELECT h.`Hotel_Name`, s.`Service_name`, o.`Price`
#                   FROM `Offers` o
#                   JOIN `Hotel` h ON o.`Hotel_id` = h.`Hotel_id`
#                   JOIN `Service` s ON o.`Service_id` = s.`Service_id`
#                   LIMIT 20;"""

#     # -------------------
#     # Pincode / location
#     # -------------------
#     if re.search(r"\b(list|show|get|display)\b.*\bhotels?\b.*\b(city|state)\b", q):
#         return """SELECT h.`Hotel_Name`, p.`City`, p.`State`
#                   FROM `Hotel` h
#                   JOIN `Pincode` p ON h.`Pincode` = p.`Pincode`
#                   LIMIT 20;"""

#     # -------------------
#     # Fallback
#     # -------------------
#     return None