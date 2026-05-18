def analyze_codebase(code_files, structure_data):

    total_files = len(code_files)

    total_lines = 0
    total_functions = 0
    total_classes = 0

    risky_files = []

    for file, struct in zip(code_files, structure_data):
        lines = len(file["content"].split("\n"))
        total_lines += lines

        func_count = len(struct["functions"])
        class_count = len(struct["classes"])

        total_functions += func_count
        total_classes += class_count

        # 🔥 Risk logic (simple)
        if func_count > 5 or lines > 50:
            risky_files.append(file["file"])

    # 🔥 Complexity based on structure
    if total_functions < 5:
        complexity = "Low"
    elif total_functions < 15:
        complexity = "Medium"
    else:
        complexity = "High"

    # 🔥 Architecture
    if total_files == 1:
        architecture = "Monolithic"
    else:
        architecture = "Modular"

    return {
        "total_files": total_files,
        "total_lines": total_lines,
        "total_functions": total_functions,
        "total_classes": total_classes,
        "complexity": complexity,
        "architecture": architecture,
        "risky_files": risky_files
    }