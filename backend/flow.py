def generate_flow(code_files):

    flow_map = []

    for file in code_files:
        source = file["file"]
        imports = file.get("imports", [])

        for imp in imports:
            flow_map.append({
                "from": source,
                "to": imp
            })

    return flow_map