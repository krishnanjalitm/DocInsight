import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def extract_topics(document_text):

    prompt = f"""
Analyze the following document.

Identify the main topics and their important subtopics.

Return ONLY valid JSON in exactly this format:

{{
    "topics": [
        {{
            "topic": "Main topic name",
            "subtopics": [
                "Subtopic 1",
                "Subtopic 2",
                "Subtopic 3"
            ]
        }}
    ]
}}

Do not include Markdown.
Do not include explanations.
Do not include ```json.
Return only the JSON object.

Document:
{document_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    return response.text