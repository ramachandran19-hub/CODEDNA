from groq import Groq
from dotenv import load_dotenv
import os

from backend.analyzer import analyze_codebase
from backend.ast_parser import analyze_structure

load_dotenv()

# =====================================
# 🔑 GROQ CLIENT
# =====================================
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =====================================
# 🧠 CODEBASE AI CHATBOT
# =====================================
def ask_codebase_ai(question, code_files):

    try:

        # =====================================
        # 🚫 NO FILES
        # =====================================
        if not code_files:

            return "No repository files found."

        # =====================================
        # 🧠 ANALYZE CODEBASE
        # =====================================
        structure = analyze_structure(code_files)

        analysis = analyze_codebase(
            code_files,
            structure
        )

        # =====================================
        # 🧠 DETECT PROJECT NAME
        # =====================================
        project_name = "Repository"

        try:

            first_file = code_files[0]["file"]

            normalized = first_file.replace("\\", "/")

            parts = normalized.split("/")

            if len(parts) > 1:

                project_name = parts[1]

        except Exception:

            pass

        # =====================================
        # 📌 IMPORTANT FILES
        # =====================================
        important_files = sorted(
            code_files,
            key=lambda x: len(
                x.get("imports", [])
            ),
            reverse=True
        )[:6]

        important_code = ""

        for file in important_files:

            content_preview = file.get(
                "content",
                ""
            )[:1500]

            important_code += f"""

FILE: {file['file']}

CODE:
{content_preview}

==================================================
"""

        # =====================================
        # 📊 REAL STATS
        # =====================================
        stats = f"""
Total Files: {analysis['total_files']}
Total Functions: {analysis['total_functions']}
Total Classes: {analysis['total_classes']}
Architecture: {analysis['architecture']}
"""

        # =====================================
        # 🧠 FINAL PROMPT
        # =====================================
        prompt = f"""
You are an expert software repository analyst.

Analyze ONLY the uploaded repository.

STRICT RULES:
- Never mention CodeDNA
- Never assume this is a repository analysis tool
- Never hallucinate features
- Never invent project purpose
- Use ONLY the actual source code
- Mention actual filenames when useful
- If unsure, say "not clearly defined in repository"

PROJECT NAME:
{project_name}

REPOSITORY STATS:
{stats}

SOURCE CODE:
{important_code}

USER QUESTION:
{question}

RESPONSE STYLE:
- concise
- technical
- repository specific
- natural ChatGPT style
- maximum 6 lines
"""

        # =====================================
        # 🚀 AI CALL
        # =====================================
        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "system",
                    "content": """
You are a professional repository analysis assistant.

You explain repositories ONLY from actual code.

Never mention CodeDNA unless it exists in the repository.

Never hallucinate project purpose.
"""
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.1,

            max_tokens=250
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Chatbot Error: {str(e)}"