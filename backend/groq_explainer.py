from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ai_explain_project(code_files):

    try:
        combined_code = ""

        for file in code_files:
            combined_code += f"\n# File: {file['file']}\n"
            combined_code += file["content"][:500]

        prompt = f"""
        You are a software architect.

        Analyze this codebase and explain:
        - What this project does
        - Architecture style
        - Key components
        - Where a new developer should start

        Code:
        {combined_code}
        """
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"