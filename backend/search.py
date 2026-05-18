def search_code(code_files, structure, query):

    results = []
    query = query.lower()

    for file, struct in zip(code_files, structure):
        filename = file["file"]
        content = file["content"].lower()

        score = 0

        # 🔍 Match in content
        if query in content:
            score += 2

        # 🔍 Match in function names
        for func in struct["functions"]:
            if query in func.lower():
                score += 3

        # 🔍 Match in file name
        if query in filename.lower():
            score += 2

        if score > 0:
            results.append({
                "file": filename,
                "score": score
            })

    # sort by relevance
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return {
        "query": query,
        "results": results
    }