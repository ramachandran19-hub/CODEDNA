from git import Repo
import os
import shutil

def clone_repo(repo_url):

    repo_name = repo_url.split("/")[-1].replace(".git", "")

    base_path = "data/repos"

    local_path = os.path.join(
        base_path,
        repo_name
    )

    os.makedirs(base_path, exist_ok=True)

    # =====================================
    # 🔥 DELETE OLD REPO
    # =====================================
    if os.path.exists(local_path):

        try:

            shutil.rmtree(
                local_path,
                ignore_errors=True
            )

            print("🗑 Old repo deleted")

        except Exception as e:

            print("Delete error:", str(e))

    # =====================================
    # ⬇ CLONE REPO
    # =====================================
    print("⬇ Cloning repository...")

    Repo.clone_from(
        repo_url,
        local_path,
        depth=1
    )

    print("✅ Clone complete")

    return local_path