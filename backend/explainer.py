from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ==============================
# 🔹 CHUNK FUNCTION (NO LINE SKIPPED)
# ==============================
def chunk_code(content, chunk_size=800):
    return [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]


# ==============================
# 🔹 CHUNK SUMMARIZER
# ==============================
def summarize_chunk(file_name, chunk):

    prompt = f"""
    Analyze this code chunk.

    File: {file_name}

    Code:
    {chunk}

    Explain:
    - What this part does
    - Important logic
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ==============================
# 🔹 FILE SUMMARIZER
# ==============================
def summarize_file(file):

    chunks = chunk_code(file["content"])
    chunk_summaries = []

    for chunk in chunks:
        summary = summarize_chunk(file["file"], chunk)
        chunk_summaries.append(summary)

    combined = "\n".join(chunk_summaries)

    prompt = f"""
    Based on these summaries, explain this file:

    {combined}

    Give:
    - Purpose
    - Key logic
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ==============================
# 🔹 REDUCTION (AVOID OVERFLOW)
# ==============================
def reduce_summaries(summaries, batch_size=5):

    reduced = []

    for i in range(0, len(summaries), batch_size):
        batch = summaries[i:i + batch_size]

        combined = "\n\n".join(batch)

        prompt = f"""
        Combine these summaries into one:

        {combined}
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        reduced.append(response.choices[0].message.content)

    return reduced


# ==============================
# 🔥 MAIN AI FUNCTION (FULL CODEBASE)
# ==============================
def ai_explain_project(code_files):

    file_summaries = []

    # 🔥 Process ALL files (no skipping)
    for file in code_files:
        summary = summarize_file(file)
        file_summaries.append(summary)

    # 🔥 Reduce until safe size
    while len(file_summaries) > 5:
        file_summaries = reduce_summaries(file_summaries)

    final_combined = "\n\n".join(file_summaries)

    final_prompt = f"""
    You are a senior software architect.

    Based on full project analysis:

    {final_combined}

    Provide:
    - What the system does
    - Architecture
    - Key modules
    - Data flow
    - Risk areas
    - Where to start for a new developer
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": final_prompt}]
    )

    return response.choices[0].message.content


# ==============================
# 🔹 OLD FUNCTION (KEEP AS FALLBACK)
# ==============================
def explain_project(code_files, analysis, structure):

    entry_file = None

    for file in code_files:
        if "main" in file["file"]:
            entry_file = file["file"]
            break

    if not entry_file:
        entry_file = code_files[0]["file"]

    max_functions = 0
    complex_file = None

    for item in structure:
        if len(item["functions"]) > max_functions:
            max_functions = len(item["functions"])
            complex_file = item["file"]

    explanation = (
        "📘 Project Overview:\n\n"
        f"- Total Files: {analysis['total_files']}\n"
        f"- Total Functions: {analysis['total_functions']}\n"
        f"- Architecture: {analysis['architecture']}\n"
        f"- Complexity: {analysis['complexity']}\n\n"

        "🧠 How to Start:\n"
        f"- Begin with: {entry_file}\n\n"

        "⚙ Key Module:\n"
        f"- Most complex file: {complex_file}\n\n"

        "💡 Suggestion:\n"
        "- Start from main flow and explore dependent modules step-by-step."
    )

    return explanation