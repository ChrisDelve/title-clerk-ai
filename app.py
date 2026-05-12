import streamlit as st
from openai import OpenAI
import os

# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="Delve AI",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
/* App background */
.stApp {
    background-color: #0E0E0E;
    color: #F5F5F5;
}

/* Hide Streamlit header/footer/menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main content width and spacing */
.block-container {
    max-width: 900px;
    padding-top: 0rem;
    padding-bottom: 4rem;
}

/* Text */
h1, h2, h3, h4, h5, h6, p, label, span {
    color: #F5F5F5 !important;
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Muted subtitle text */
.subtext {
    color: #9A9A9A !important;
    font-size: 0.98rem;
    text-align: center;
    max-width: 760px;
    margin: 0 auto 1.5rem auto;
    line-height: 1.75;
    font-weight: 300;
    letter-spacing: 0.2px;
}

/* Logo container */
..logo-wrap {
    display: flex;
    justify-content: center;
    margin-bottom: 0.4rem;
}

/* Logo sizing */
.logo-wrap img {
    max-width: 620px;
    width: 80%;

    filter: drop-shadow(0 0 12px rgba(212,175,55,0.12));
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #2A2A2A;
    margin: 2rem 0;
}

/* Input box */
.stTextInput input {
    background: rgba(17,17,17,0.92) !important;
    color: #F5F5F5 !important;

    border: 1px solid rgba(212,175,55,0.22) !important;
    border-radius: 14px !important;

    height: 48px !important;
min-height: 48px !important;
line-height: 48px !important;

padding: 0 1rem !important;

    font-size: 0.95rem !important;
    font-weight: 400 !important;
    line-height: normal !important;

    box-shadow: none !important;
    transition: all 0.2s ease !important;
}
.stTextInput input::placeholder {
    color: #7A7A7A !important;
    opacity: 1 !important;
    font-weight: 400 !important;
}
.stTextInput input:focus {
    border: 1px solid #C8A96B !important;
    box-shadow: 0 0 10px rgba(200,169,107,0.25) !important;
}
/* Text area if used */
.stTextArea textarea {
    background-color: #171717 !important;
    color: #F5F5F5 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 14px !important;
    padding: 1rem !important;
    font-size: 1rem !important;
}

/* Buttons */
.stButton button {
    background-color: #C8A96B !important;
    color: #0E0E0E !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: 700 !important;
    padding: 0.65rem 1.25rem !important;
}

/* Response card */
.response-card {
    background-color: #171717;
    border: 1px solid #2A2A2A;
    border-radius: 18px;
    padding: 1.5rem;
    margin-top: 1.5rem;
}

/* Small helper text */
.helper {
    color: #A1A1A1 !important;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)
# ----------------------------
# OPENAI CLIENT
# ----------------------------

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# ----------------------------
# SIDEBAR
# ----------------------------

# ----------------------------
# HEADER / LOGO
# ----------------------------

st.markdown('<div class="logo-wrap">', unsafe_allow_html=True)
st.image("logo.png", width=700)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <h1 style='
        text-align:center;
        font-size:2.5rem;
        font-weight:700;
        letter-spacing:-1px;
        line-height:1.1;
        margin-bottom:0.8rem;
        font-family: Inter, sans-serif;
        color:white;
    '>
        Instant Title & Registration Assistant
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class='subtext' style='text-align:center; max-width:700px; margin:auto; line-height:1.8;'>
    Ask about duplicate titles, ELT, lien releases, registration transfers, fees, & title procedures.
    </p>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style="
        width: 320px;
        height: 1px;
        margin: 2rem auto 2.2rem auto;
        background: linear-gradient(
            to right,
            transparent,
            rgba(212,175,55,0.9),
            transparent
        );
        position: relative;
    ">
        <div style="
            width: 10px;
            height: 10px;
            background: #D4AF37;
            border-radius: 50%;
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            box-shadow: 0 0 10px rgba(212,175,55,0.5);
        "></div>
    </div>
    """,
    unsafe_allow_html=True
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
                    content = content.replace("*", "")
                    content = content.replace("_", " ")
                    content = content.replace("•", "-")
                    content = content.replace("{", "")
                    content = content.replace("}", "")

                    # PRESERVE LINE BREAKS
                    content = "\n".join(
                        line.strip()
                        for line in content.splitlines()
                        if line.strip()
                    )

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

    # If question is about fees/cost/pricing, force fee documents to the top
    fee_words = ["fee", "fees", "cost", "price", "how much", "amount"]

    if any(term in query.lower() for term in fee_words):
        fee_matches = [
            m for m in matches
            if "fee" in m["name"].lower() or "fees" in m["name"].lower()
        ]
        non_fee_matches = [
            m for m in matches
            if m not in fee_matches
        ]
        return (fee_matches + non_fee_matches)[:5]

    return matches[:5]

# ----------------------------
# USER INPUT
# ----------------------------


user_question = st.text_input(
    "",
    placeholder="Ask your title clerk question here..."
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

When providing fees:
- Use clean plain text.
- Do not italicize fee amounts.
- Do not merge multiple fee amounts into one sentence.
- Use bullet points for fee amounts.
- If fee amounts vary by lien, paper/electronic title, fast title, vessel, or for-hire status, separate them clearly.

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
- Use clean plain text formatting
- Do NOT use italic formatting
- Do NOT merge fee amounts together

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