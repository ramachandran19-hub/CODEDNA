def ai_explain_project(code_files):

    try:
        # 🔥 Step 1: rank files by importance
        sorted_files = sorted(
            code_files,
            key=lambda f: len(f.get("imports", [])),
            reverse=True
        )

        # 🔥 Step 2: pick top important files
        selected_files = sorted_files[:8]

        combined_code = ""

        for file in selected_files:
            combined_code += f"\n# File: {file['file']}\n"
            combined_code += file["content"][:400]

        # 🔥 Step 3: structured prompt
        prompt = f"""
        You are a senior software architect analyzing a real-world project.

        Based on the following important parts of the codebase, provide:

        1. What the project does (in simple terms)
        2. Architecture style (monolith, modular, layered, etc.)
        3. Key modules and their roles
        4. How data flows through the system
        5. Where a new developer should start
        6. Any risky or complex areas

        Code:
        {combined_code}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            timeout=30
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"