import json

from database import get_db_connection
from gemini_service import extract_topics


connection = get_db_connection()

document = connection.execute(
    """
    SELECT document_id, filename, extracted_text
    FROM documents
    ORDER BY document_id DESC
    LIMIT 1
    """
).fetchone()

connection.close()


if document and document["extracted_text"]:

    print("Analyzing:", document["filename"])
    print("\nGemini is analyzing the document...\n")

    result = extract_topics(document["extracted_text"])

    try:
        topics = json.loads(result)

        print("----- JSON Result -----")
        print(topics)

    except json.JSONDecodeError:
        print("Gemini did not return valid JSON.")
        print(result)

else:
    print("No document or extracted text found.")