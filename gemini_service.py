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
# ----------------------------------------------------------
def extract_subtopic_info(document_text, subtopic):

    prompt = f"""
Use only the information available in the document.

Explain the following subtopic clearly:
{subtopic}

If the document does not contain relevant information,
say so. Do not invent facts.

Document:
{document_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def summarize_document(document_text):
    prompt = f"""
Summarize the following document in simple language.

Include:
1. Main idea
2. Important points
3. Conclusion

Use only information from the document.
Do not invent facts.

Document:
{document_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def compare_documents(document1_text, document2_text):
    prompt = f"""
Compare the following two documents.

Explain:
1. Main topic of each document
2. Similarities
3. Important differences
4. Key points unique to each document

Use only the information in the documents.
Do not invent facts.

DOCUMENT 1:
{document1_text}

DOCUMENT 2:
{document2_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

#----------- COMPARE TWO DOCUMENTS FUNCTION----------------------------

# def compare_documents(document1_text, document2_text):
#     prompt = f"""
# Compare these two documents.

# 1. Main topic of each document
# 2. Similarities
# 3. Important differences
# 4. Key points unique to each document

# Use only the information in the documents.
# Do not invent facts.

# DOCUMENT 1:
# {document1_text}

# DOCUMENT 2:
# {document2_text}
# """

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text