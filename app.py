import streamlit as st
import os
from openai import OpenAI

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Delve AI",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    div[data-testid="stVerticalBlock"] > div:has(img) {
        margin-bottom: -40px;
    }

    .stTextInput input {
        border-radius: 12px;
        padding: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# OPENAI
# ==================================================

api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("### Operational Categories")

    st.markdown("""
    - Title Transfers
    - Registration
    - Liens / ELT
    - Duplicate Titles
    - Fees
    - VIN Verification
    - Dealer Processing
    - Escalation Procedures
    """)

    st.info(
        "Internal dealership operations assistant designed to support title, registration, lien, and compliance workflows."
    )

# ==================================================
# LOGO
# ==================================================

st.image("logo.png", width=475)

# ==================================================
# HEADER
# ==================================================

st.markdown("## Instant Title & Registration Assistant")

st.caption(
    "Ask about duplicate titles • ELT • lien releases • registration transfers"
)

# ==================================================
# SEARCH BOX
# ==================================================

with st.container(border=True):

    user_question = st.text_input(
        "",
        placeholder="Ask your title clerk question here..."
    )

# ==================================================
# LOAD DOCUMENTS
# ==================================================

DOCUMENTS = []

docs_path = "docs"

for root, dirs, files in os.walk(docs_path):

    for file in files:

        if file.endswith(".txt"):

            filepath = os.path.join(root, file)

            try:

                with open(filepath, "r", encoding="utf-8") as f:

                    content = f.read()

                    # CLEANUP
                    content = content.replace("\\", "\n")
                    content = content.replace("{", "")
                    content = content.replace("}", "")

                    DOCUMENTS.append({
                        "name": file,
                        "content": content
                    })

            except:
                pass

# ==================================================
# SEARCH FUNCTION
# ==================================================

def search_documents(query):

    query_words = query.lower().split()

    matches = []

    for doc in DOCUMENTS:

        score = 0

        content_lower = doc["content"].lower()

        for word in query_words:

            if word in content_lower:
                score += 1

        if score > 0:

            matches.append({
                "name": doc["name"],
                "content": doc["content"],
                "score": score
            })

    matches = sorted(
        matches,
        key=lambda x: x["score"],
        reverse=True
    )

    return matches[:5]

# ==================================================
# AI RESPONSE
# ==================================================

if user_question:

    st.info("Searching Florida operational knowledge base...")

    results = search_documents(user_question)

    st.success(f"Found {len(results)} matching operational documents")

    combined_context = ""

    for result in results:

        combined_context += f"""

DOCUMENT NAME:
{result['name']}

DOCUMENT CONTENT:
{result['content']}

"""

    system_prompt = f"""
You are an expert Florida dealership title clerk operations assistant.

You ONLY answer using the operational knowledge provided.

Structure responses professionally.

Use:
1. Direct Answer
2. Required Verification
3. Required Documents
4. Escalate If
5. Compliance Risk
6. Operational Notes

Be operationally precise.
"""

    user_prompt = f"""
QUESTION:
{user_question}

KNOWLEDGE BASE:
{combined_context}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2
    )

    ai_answer = response.choices[0].message.content

    # ==================================================
    # DISPLAY RESPONSE
    # ==================================================

    st.markdown("---")

    st.markdown("## AI Operational Response")

    st.markdown(ai_answer)

    # ==================================================
    # SOURCES
    # ==================================================

    st.markdown("---")

    st.markdown("### Sources Used")

    for result in results:

        with st.expander(result["name"]):

            st.caption(f"Match Score: {result['score']}")

            st.text(result["content"][:3000])