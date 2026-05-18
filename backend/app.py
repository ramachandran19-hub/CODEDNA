from fastapi import FastAPI
from backend.parser import load_code_files
from backend.analyzer import analyze_codebase
from backend.impact import predict_impact
from backend.flow import generate_flow
from backend.search import search_code
from backend.ast_parser import analyze_structure
from backend.groq_explainer import ai_explain_project
from backend.graph import generate_code_map
from backend.github_loader import clone_repo
from backend.tree import build_project_tree
from backend.file_reader import read_file_content
from backend.file_ai import explain_file
from backend.chatbot import ask_codebase_ai

app = FastAPI()

# =====================================
# 🚀 HOME
# =====================================
@app.get("/")
def home():

    return {
        "message": "CodeDNA Backend Running 🚀"
    }

# =====================================
# 📖 READ SAMPLE PROJECT
# =====================================
@app.get("/read")
def read_code():

    repo_path = "data/sample_project"

    code_files = load_code_files(repo_path)

    return {
        "files": code_files
    }

# =====================================
# 📊 ANALYZE SAMPLE PROJECT
# =====================================
@app.get("/analyze")
def analyze():

    repo_path = "data/sample_project"

    code_files = load_code_files(repo_path)

    structure = analyze_structure(code_files)

    report = analyze_codebase(
        code_files,
        structure
    )

    return {
        "CodeDNA Report": report
    }

# =====================================
# 🧠 AI EXPLAIN PROJECT
# =====================================
@app.get("/explain")
def explain():

    repo_path = "data/sample_project"

    code_files = load_code_files(repo_path)

    explanation = ai_explain_project(code_files)

    return {
        "Onboarding": explanation
    }

# =====================================
# ⚠ IMPACT ANALYSIS
# =====================================
@app.get("/impact")
def impact():

    repo_path = "data/sample_project"

    code_files = load_code_files(repo_path)

    target_file = "main.py"

    result = predict_impact(
        code_files,
        target_file
    )

    return {
        "Impact Analysis": result
    }

# =====================================
# 🔄 FLOW ANALYSIS
# =====================================
@app.get("/flow")
def flow():

    repo_path = "data/sample_project"

    code_files = load_code_files(repo_path)

    flow_data = generate_flow(code_files)

    return {
        "Code Flow": flow_data
    }

# =====================================
# 🔍 SEARCH CODEBASE
# =====================================
@app.get("/search")
def search(query: str):

    repo_path = "data/sample_project"

    code_files = load_code_files(repo_path)

    structure = analyze_structure(code_files)

    result = search_code(
        code_files,
        structure,
        query
    )

    return {
        "Search Result": result
    }

# =====================================
# 🏗 STRUCTURE
# =====================================
@app.get("/structure")
def structure():

    repo_path = "data/sample_project"

    code_files = load_code_files(repo_path)

    structure = analyze_structure(code_files)

    return {
        "Structure": structure
    }

# =====================================
# 🗺 CODE MAP
# =====================================
@app.get("/map")
def map_code():

    repo_path = "data/sample_project"

    code_files = load_code_files(repo_path)

    structure = analyze_structure(code_files)

    file_path = generate_code_map(
        code_files,
        structure
    )

    entry_file = next(
        (
            f["file"]
            for f in code_files
            if "main" in f["file"]
        ),
        code_files[0]["file"]
    )

    most_connected = max(
        code_files,
        key=lambda f: len(
            f.get("imports", [])
        )
    )

    return {

        "map": file_path,

        "insight": {

            "entry": entry_file,

            "critical": most_connected["file"]
        }
    }

# =====================================
# 🔗 ANALYZE GITHUB REPO
# =====================================
@app.get("/analyze-github")
def analyze_github(repo_url: str):

    try:

        print("🔗 Received URL:", repo_url)

        repo_path = clone_repo(repo_url)

        print("✅ Repo cloned at:", repo_path)

        return {

            "status": "success",

            "repo_path": repo_path,

            "message": "Repository cloned successfully"
        }

    except Exception as e:

        print("❌ Error:", str(e))

        return {

            "status": "error",

            "message": str(e)
        }

# =====================================
# 🗺 GENERATE GRAPH
# =====================================
@app.get("/generate-graph")
def generate_graph(repo_path: str):

    try:

        print("🗺 Generating graph for:", repo_path)

        code_files = load_code_files(repo_path)

        if not code_files:

            return {
                "error": "No Python files found"
            }

        structure = analyze_structure(code_files)

        graph_path = generate_code_map(
            code_files,
            structure
        )

        print("✅ Graph generated")

        return {

            "status": "success",

            "graph": graph_path
        }

    except Exception as e:

        print("❌ Graph Error:", str(e))

        return {
            "error": str(e)
        }

# =====================================
# 📁 PROJECT TREE
# =====================================
@app.get("/project-tree")
def project_tree(repo_path: str):

    try:

        print("📁 Building project tree...")

        tree = build_project_tree(repo_path)

        return {

            "status": "success",

            "tree": tree
        }

    except Exception as e:

        print("❌ Tree Error:", str(e))

        return {
            "error": str(e)
        }

# =====================================
# 📄 FILE CONTENT
# =====================================
@app.get("/file-content")
def file_content(repo_path: str, file_path: str):

    try:

        print("📄 Reading file:", file_path)

        content = read_file_content(
            repo_path,
            file_path
        )

        if content is None:

            return {
                "error": "Could not read file"
            }

        return {

            "status": "success",

            "file": file_path,

            "content": content
        }

    except Exception as e:

        print("❌ File Read Error:", str(e))

        return {
            "error": str(e)
        }

# =====================================
# 🧠 AI FILE EXPLAINER
# =====================================
@app.get("/ai-file-explain")
def ai_file_explain(repo_path: str, file_path: str):

    try:

        content = read_file_content(
            repo_path,
            file_path
        )

        if not content:

            return {
                "error": "Could not read file"
            }

        explanation = explain_file(
            file_path,
            content
        )

        return {
            "explanation": explanation
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# =====================================
# 🤖 CODEBASE CHATBOT
# =====================================
# =====================================
# 🤖 CODEBASE CHATBOT
# =====================================
# =====================================
# 🤖 CODEBASE CHATBOT
# =====================================
@app.get("/chat")
def chat(repo_path: str, question: str):

    try:

        print("\n==============================")
        print("🧠 CHAT REQUEST RECEIVED")
        print("📂 REPO PATH:", repo_path)

        # =====================================
        # 📂 LOAD CODE FILES
        # =====================================
        code_files = load_code_files(repo_path)

        print("📄 FILES LOADED:", len(code_files))

        # DEBUG FILES
        for file in code_files[:10]:

            print("➡", file["file"])

        # =====================================
        # ❌ NO FILES
        # =====================================
        if not code_files:

            return {
                "error": "No Python files found"
            }

        # =====================================
        # 🧠 ANALYZE STRUCTURE
        # =====================================
        structure = analyze_structure(
            code_files
        )

        # =====================================
        # 📊 ANALYZE CODEBASE
        # =====================================
        analysis = analyze_codebase(
            code_files,
            structure
        )

        print("🏗 ARCHITECTURE:",
              analysis["architecture"])

        print("📄 TOTAL FILES:",
              analysis["total_files"])

        # =====================================
        # 🤖 AI RESPONSE
        # =====================================
        answer = ask_codebase_ai(
            question,
            code_files
        )

        print("✅ AI RESPONSE GENERATED")

        return {

            "answer": answer,

            "stats": {

                "files": analysis["total_files"],

                "functions": analysis["total_functions"],

                "classes": analysis["total_classes"],

                "architecture": analysis["architecture"]
            }
        }

    except Exception as e:

        print("❌ CHAT ERROR:", str(e))

        return {
            "error": str(e)
        }