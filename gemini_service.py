import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def extract_topics(document_text):

    prompt = f"""
You are analyzing a document.

Read the following document and identify its main topics and important subtopics.

Return the answer in a simple structured format.

Document:
{document_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text