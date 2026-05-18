import os


# =====================================
# 🧠 LIGHTWEIGHT CONTEXT BUILDER
# =====================================
def build_repo_context(repo_path, code_files, analysis):

    project_name = os.path.basename(repo_path)

    total_files = analysis.get("total_files", 0)
    total_functions = analysis.get("total_functions", 0)
    architecture = analysis.get("architecture", "Unknown")
    complexity = analysis.get("complexity", "Unknown")

    risky_files = analysis.get("risky_files", [])[:3]

    # =====================================
    # 📌 ONLY TOP 3 FILES
    # =====================================
    important_files = sorted(
        code_files,
        key=lambda x: len(x.get("imports", [])),
        reverse=True
    )[:3]

    modules = []

    for file in important_files:

        modules.append(file["file"])

    context = f"""
PROJECT: {project_name}

ARCHITECTURE: {architecture}

COMPLEXITY: {complexity}

FILES: {total_files}

FUNCTIONS: {total_functions}

IMPORTANT MODULES:
{modules}

RISKY FILES:
{risky_files}

PROJECT PURPOSE:
CodeDNA analyzes repositories,
detects architecture,
explains codebases,
and helps developer onboarding.
"""

    return context