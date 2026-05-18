import os


def read_file_content(repo_path, file_path):

    full_path = os.path.join(repo_path, file_path)

    # 🔥 Normalize path
    full_path = os.path.normpath(full_path)

    # 🚫 Security check
    if not full_path.startswith(os.path.normpath(repo_path)):
        return None

    try:

        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:

            content = f.read()

        return content

    except Exception:

        return None