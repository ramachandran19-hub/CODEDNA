import os


def build_project_tree(repo_path):

    tree = {}

    for root, dirs, files in os.walk(repo_path):

        # 🚫 skip .git
        if ".git" in root:
            continue

        # relative path
        relative_path = os.path.relpath(root, repo_path)

        current = tree

        # build nested folders
        if relative_path != ".":
            parts = relative_path.split(os.sep)

            for part in parts:
                current = current.setdefault(part, {})

        # add files
        for file in files:

            if file.endswith(".py"):

                current[file] = "file"

    return tree