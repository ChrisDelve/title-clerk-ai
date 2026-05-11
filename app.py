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
                    content = content.replace("\\", "\n")
                    content = content.replace("{", "")
                    content = content.replace("}", "")

                    # Reduce messy spacing from PDF/TXT extraction
                    content = " ".join(content.split())

                    # Add readable line breaks around common fee terms
                    content = content.replace("Electronic", "\nElectronic")
                    content = content.replace("Printed", "\nPrinted")
                    content = content.replace("Paper", "\nPaper")
                    content = content.replace("Fast Title", "\nFast Title")
                    content = content.replace("Transaction:", "\n\nTransaction:")
                    content = content.replace("TITLE:", "\n\nTITLE:")
                    content = content.replace("CATEGORY:", "\n\nCATEGORY:")
                    content = content.replace("RULE:", "\n\nRULE:")
                    content = content.replace("VERIFY:", "\n\nVERIFY:")
                    content = content.replace("ESCALATE IF:", "\n\nESCALATE IF:")

                    DOCUMENTS.append({
                        "name": file,
                        "content": content
                    })

            except Exception:
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
        doc_name_lower = doc["name"].lower()
        query_lower = query.lower()

        for word in query_words:
            if word in content_lower:
                score += 1

        # Boost fee documents when user asks about price/cost/fee
        fee_words = ["fee", "fees", "cost", "price", "how much", "amount"]
        if any(term in query_lower for term in fee_words):
            if "fees" in doc_name_lower or "fee" in doc_name_lower:
                score += 10

        # Boost duplicate title documents when asking duplicate title questions
        if "duplicate" in query_lower and "title" in query_lower:
            if "duplicate" in doc_name_lower:
                score += 8

        # Boost exact phrase matches
        if "duplicate title" in content_lower:
            score += 5

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
                    "content": f"""
You are a senior Florida dealership title clerk and compliance operations specialist.

Your job is to provide:
- operational answers
- procedural verification
- escalation warnings
- compliance risks
- dealership workflow guidance

DO NOT simply summarize documents.

You must:
- synthesize operational rules
- explain practical workflow
- identify missing information
- explain risks
- distinguish between title, registration, lien, ELT, and fee procedures

Always structure answers like this:

1. Direct Answer
2. Required Verification
3. Required Documents
4. Escalate If
5. Compliance Risk
6. Operational Notes

If the answer is uncertain or situation-dependent:
- explicitly say what determines the outcome

Use dealership operational language, not generic AI wording.

KNOWLEDGE BASE:
{combined_context}
"""
                },
                {
                    "role": "user",
                    "content": f"""
Question:
{user_question}

You must answer this operationally using the dealership knowledge base.

Requirements:
- Give a direct operational answer
- Explain dealership workflow
- Explain required verification
- Explain compliance concerns
- Explain required documents
- Explain escalation situations
- Use practical dealership terminology
- Do NOT ask the user to clarify unless absolutely necessary

Knowledge Base:
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

        st.markdown(ai_answer)

        st.divider()

        # ----------------------------
        # SOURCES USED
        # ----------------------------

        st.subheader("Sources Used")

        for result in results:

            with st.expander(result["name"]):

                st.caption(f"Match Score: {result['score']}")

                st.text(result["content"][:3000])