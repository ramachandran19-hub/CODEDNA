import os
import ast

# =====================================
# 📂 LOAD ALL PYTHON FILES
# =====================================
def load_code_files(repo_path):

    code_files = []

    for root, dirs, files in os.walk(repo_path):

        # skip virtual env / git
        dirs[:] = [

            d for d in dirs

            if d not in [
                "__pycache__",
                ".git",
                "venv",
                "env",
                "node_modules"
            ]
        ]

        for file in files:

            if file.endswith(".py"):

                try:

                    full_path = os.path.join(root, file)

                    relative_path = os.path.relpath(
                        full_path,
                        repo_path
                    )

                    with open(
                        full_path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        content = f.read()

                    tree = ast.parse(content)

                    imports = []
                    functions = []
                    classes = []

                    for node in ast.walk(tree):

                        # imports
                        if isinstance(node, ast.Import):

                            for n in node.names:
                                imports.append(n.name)

                        elif isinstance(node, ast.ImportFrom):

                            if node.module:
                                imports.append(node.module)

                        # functions
                        elif isinstance(node, ast.FunctionDef):

                            functions.append(node.name)

                        # classes
                        elif isinstance(node, ast.ClassDef):

                            classes.append(node.name)

                    code_files.append({

                        "file": relative_path,

                        "content": content[:4000],

                        "imports": imports,

                        "functions": functions,

                        "classes": classes
                    })

                except Exception:

                    pass

    return code_files