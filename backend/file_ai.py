from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def explain_file(file_name, content):

    try:

        content = content[:4000]

        prompt = f"""
You are a senior software architect.

Analyze this file and explain:

1. Purpose of the file
2. Important functions
3. Role in architecture
4. Complexity or risks
5. Developer onboarding guidance

File:
{file_name}

Code:
{content}
"""

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        return str(e)
