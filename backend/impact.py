def predict_impact(code_files, target_file):

    impacted_files = []

    for file in code_files:
        filename = file["file"]
        imports = file.get("imports", [])

        if target_file in imports:
            impacted_files.append(filename)

    return {
        "changed_file": target_file,
        "impacted_files": impacted_files
    }