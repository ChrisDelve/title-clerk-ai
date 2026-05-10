import streamlit as st
from openai import OpenAI
import os

# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="Florida Title Clerk AI",
    page_icon="🚗",
    layout="wide"
)

# ----------------------------
# OPENAI CLIENT
# ----------------------------

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# ----------------------------
# TITLE / HEADER
# ----------------------------

st.title("🚗 Florida Title Clerk AI")
st.caption("Internal Operations Knowledge Assistant")

st.divider()

# ----------------------------
# SIDEBAR
# ----------------------------

with st.sidebar:
    st.header("Operational Categories")

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

    st.divider()

    st.info(
        "Internal prototype AI assistant for dealership title and registration operations."
    )

# ----------------------------
# LOAD DOCUMENTS
# ----------------------------

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
                    content = content.replace("\\", "")
                    content = content.replace("{", "")
                    content = content.replace("}", "")

                    DOCUMENTS.append({
                        "name": file,
                        "content": content
                    })

            except:
                pass

# ----------------------------
# SEARCH FUNCTION
# ----------------------------

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

    matches = sorted(matches, key=lambda x: x["score"], reverse=True)

    return matches[:5]

# ----------------------------
# USER INPUT
# ----------------------------

st.header("Ask an Operational Question")

user_question = st.text_input(
    "Example: duplicate title, lien release, registration transfer..."
)

# ----------------------------
# AI RESPONSE
# ----------------------------

if user_question:

    st.info("Searching Florida operational knowledge base...")

    results = search_documents(user_question)

    if len(results) == 0:
        st.error("No matching operational documents found.")

    else:

        st.success(f"Found {len(results)} matching operational documents")

        combined_context = ""

        for result in results:
            combined_context += f"""

SOURCE DOCUMENT:
{result['name']}

CONTENT:
{result['content']}

==================================================
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a professional Florida dealership title clerk operations assistant.

Your purpose:
- Answer dealership operational questions
- Explain title and registration procedures
- Explain lien release handling
- Explain escalation risks
- Explain documentation requirements

Rules:
- Be concise but professional
- Use bullet points when helpful
- Explain operational risk areas
- Mention verification steps
- Mention escalation situations
- NEVER invent laws
- ONLY use provided operational context
"""
                },
                {
                    "role": "user",
                    "content": f"""
QUESTION:
{user_question}

KNOWLEDGE BASE:
{combined_context}
"""
                }
            ],
            temperature=0.2
        )

        ai_answer = response.choices[0].message.content

        # ----------------------------
        # DISPLAY ANSWER
        # ----------------------------

        st.subheader("AI Operational Response")

        st.write(ai_answer)

        st.divider()

        # ----------------------------
        # SOURCES USED
        # ----------------------------

        st.subheader("Sources Used")

        for result in results:

            with st.expander(result["name"]):

                st.caption(f"Match Score: {result['score']}")

                st.text(result["content"][:3000])