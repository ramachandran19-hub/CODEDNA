import ast

def analyze_structure(code_files):

    structure_data = []

    for file in code_files:
        filename = file["file"]
        content = file["content"]

        try:
            tree = ast.parse(content)

            functions = []
            classes = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)

                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)

            structure_data.append({
                "file": filename,
                "functions": functions,
                "classes": classes
            })

        except:
            structure_data.append({
                "file": filename,
                "functions": [],
                "classes": []
            })

    return structure_data