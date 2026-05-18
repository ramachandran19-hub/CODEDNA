import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================
# ⚙ PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="CodeDNA",
    layout="wide"
)

# =====================================
# 🌐 BACKEND URL
# =====================================
BACKEND_URL = "https://codedna-backend.onrender.com"

# =====================================
# 🧠 SESSION STATE
# =====================================
if "repo_path" not in st.session_state:
    st.session_state.repo_path = None

if "selected_file" not in st.session_state:
    st.session_state.selected_file = None

if "selected_content" not in st.session_state:
    st.session_state.selected_content = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================
# 🎨 TITLE
# =====================================
st.title("🧬 CodeDNA - Software Intelligence Engine")

st.markdown("""
Analyze software architecture visually using:

- GitHub repository ingestion
- Dependency intelligence
- Interactive project exploration
- AI-assisted understanding
""")

# =====================================
# 🔗 GITHUB ANALYZER
# =====================================
st.markdown("---")
st.subheader("🔗 Analyze GitHub Repository")

repo_url = st.text_input(
    "Enter GitHub Repository URL",
    placeholder="https://github.com/pallets/flask"
)

# =====================================
# 🚀 ANALYZE
# =====================================
if st.button("🚀 Analyze Repository"):

    if repo_url:

        with st.spinner("Analyzing repository..."):

            try:

                res = requests.get(
                    f"{BACKEND_URL}/analyze-github",
                    params={
                        "repo_url": repo_url
                    }
                ).json()

                if res.get("status") == "success":

                    st.success("Repository analyzed successfully")

                    st.session_state.repo_path = res["repo_path"]

                    st.write(
                        "📂 Active Repository:",
                        st.session_state.repo_path
                    )

                    # =====================================
                    # 🧹 CLEAR OLD CHAT
                    # =====================================
                    st.session_state.messages = []

                else:

                    st.error(
                        res.get(
                            "message",
                            "Repository analysis failed"
                        )
                    )

            except Exception as e:

                st.error(str(e))

    else:

        st.warning("Please enter a repository URL")

# =====================================
# 🚫 STOP IF NO REPO
# =====================================
if not st.session_state.repo_path:

    st.info("Analyze a GitHub repository first")

    st.stop()

# =====================================
# 🧠 ACTIVE REPO
# =====================================
st.markdown("---")

st.success(
    f"📂 Active Repository: {st.session_state.repo_path}"
)

# =====================================
# 🧠 AI PIPELINE
# =====================================
st.markdown("---")
st.subheader("🧠 CodeDNA Intelligence Pipeline")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.info("""
    ### GitHub Repository

    User submits repository URL
    """)

with col2:

    st.info("""
    ### Repository Parsing

    Extract files and structure
    """)

with col3:

    st.info("""
    ### AI Analysis

    Detect architecture and risks
    """)

with col4:

    st.info("""
    ### Engineering Dashboard

    Generate analytics and metrics
    """)

with col5:

    st.success("""
    ### Developer Intelligence

    AI onboarding and understanding
    """)

# =====================================
# 📁 PROJECT EXPLORER
# =====================================
st.markdown("---")
st.subheader("📁 Intelligent Project Explorer")

left_col, right_col = st.columns([1, 2])

# =====================================
# 🌳 FILE TREE
# =====================================
with left_col:

    try:

        tree_res = requests.get(
            f"{BACKEND_URL}/project-tree",
            params={
                "repo_path": st.session_state.repo_path
            }
        ).json()

        tree = tree_res["tree"]

        def display_tree(tree, current_path=""):

            for key, value in tree.items():

                if value == "file":

                    button_key = f"{current_path}/{key}"

                    if st.button(
                        f"📄 {key}",
                        key=button_key
                    ):

                        file_path = (
                            current_path + "/" + key
                            if current_path
                            else key
                        )

                        file_res = requests.get(
                            f"{BACKEND_URL}/file-content",
                            params={
                                "repo_path": st.session_state.repo_path,
                                "file_path": file_path
                            }
                        ).json()

                        if "error" not in file_res:

                            st.session_state.selected_file = file_path

                            st.session_state.selected_content = (
                                file_res["content"]
                            )

                else:

                    with st.expander(f"📁 {key}"):

                        next_path = (
                            current_path + "/" + key
                            if current_path
                            else key
                        )

                        display_tree(
                            value,
                            next_path
                        )

        display_tree(tree)

    except Exception as e:

        st.error(str(e))

# =====================================
# 📄 FILE VIEWER
# =====================================
with right_col:

    if st.session_state.selected_file:

        st.subheader(
            f"📄 {st.session_state.selected_file}"
        )

        st.code(
            st.session_state.selected_content,
            language="python"
        )

        # =====================================
        # 🧠 FILE EXPLAINER
        # =====================================
        if st.button("🧠 Explain This File"):

            with st.spinner(
                "Analyzing file..."
            ):

                try:

                    response = requests.get(
                        f"{BACKEND_URL}/ai-file-explain",
                        params={
                            "repo_path": st.session_state.repo_path,
                            "file_path": st.session_state.selected_file
                        }
                    ).json()

                    if "explanation" in response:

                        st.success(
                            "AI Analysis Complete"
                        )

                        st.markdown(
                            response["explanation"]
                        )

                    else:

                        st.error(
                            response.get(
                                "error",
                                "AI failed"
                            )
                        )

                except Exception as e:

                    st.error(str(e))

    else:

        st.info(
            "Select a file from the explorer"
        )

# =====================================
# 💬 AI CHATBOT
# =====================================
st.markdown("---")
st.subheader("🧠 CodeDNA AI Assistant")

# =====================================
# 💬 DISPLAY CHAT
# =====================================
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =====================================
# 💬 USER INPUT
# =====================================
prompt = st.chat_input(
    "Ask anything about the repository..."
)

# =====================================
# 🚀 PROCESS CHAT
# =====================================
if prompt:

    # =====================================
    # 👤 USER MESSAGE
    # =====================================
    st.session_state.messages.append({

        "role": "user",

        "content": prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    # =====================================
    # 🤖 AI RESPONSE
    # =====================================
    with st.chat_message("assistant"):

        with st.spinner("Analyzing repository..."):

            try:

                response = requests.get(

                    f"{BACKEND_URL}/chat",

                    params={

                        "repo_path": st.session_state.repo_path,

                        "question": prompt
                    }

                ).json()

                if "answer" in response:

                    answer = response["answer"]

                    st.markdown(answer)

                    st.session_state.messages.append({

                        "role": "assistant",

                        "content": answer
                    })

                else:

                    error_msg = response.get(
                        "error",
                        "AI failed"
                    )

                    st.error(error_msg)

            except Exception as e:

                st.error(str(e))