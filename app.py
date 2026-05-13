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
/* INFO BOX COLOR */

div[data-testid="stAlert"] {
    background-color: #4A3B0A !important;
    border: 1px solid #C9A227 !important;
    color: #F5F5F5 !important;
}

/* INFO TEXT */

div[data-testid="stAlert"] p {
    color: #F5F5F5 !important;
    font-weight: 600;
}
/* INFO BOX SIZE */

div[data-testid="stAlert"] {
    padding: 0.15rem 0.65rem !important;
    min-height: 30px !important;
    border-radius: 8px !important;
}
/* CENTER ALERT TEXT */

div[data-testid="stAlert"] {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

div[data-testid="stAlert"] > div {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    min-height: 30px !important;
}

div[data-testid="stAlert"] p {
    text-align: center !important;
    width: 100% !important;
}
/* TEXT SPACING */

div[data-testid="stAlert"] p {
    margin: 0 !important;
    padding: 0 !important;
    font-size: 0.90rem !important;
    line-height: 1.1 !important;
    font-weight: 600 !important;
    text-align: center !important;
    width: 100% !important;
    position: relative !important;
    top: -6px !important;
}            
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

# ------------------------------
# LOAD DOCUMENTS
# ------------------------------

from pypdf import PdfReader

DOCUMENTS = []

docs_path = "docs"

for root, dirs, files in os.walk(docs_path):

    for file in files:

        filepath = os.path.join(root, file)

        # ---------------- TXT FILES ----------------

        if file.endswith(".txt"):

            try:
                with open(filepath, "r", encoding="utf-8") as f:

                    content = f.read()

                    # CLEANUP
                    content = content.replace("\\n", "\n")
                    content = content.replace("\\", "")
                    content = content.replace("{", "")
                    content = content.replace("}", "")

                    DOCUMENTS.append({
                        "name": file,
                        "content": content
                    })

            except Exception as e:
                print(f"Error loading TXT {file}: {e}")

        # ---------------- PDF FILES ----------------

        elif file.endswith(".pdf"):

            try:
                reader = PdfReader(filepath)

                pdf_text = ""

                for page in reader.pages:

                    text = page.extract_text()

                    if text:
                        pdf_text += text + "\n"

                DOCUMENTS.append({
                    "name": file,
                    "content": pdf_text
                })

            except Exception as e:
                print(f"Error loading PDF {file}: {e}")

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
        return (fee_matches + non_fee_matches)[:2]

    return matches[:2]

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

    status_box = st.empty()

    status_box.info("Classifying FLHSMV procedure scenario...")

    results = search_documents(user_question)

    if len(results) == 0:
        
        st.error("No matching operational documents found.")

    else:
        combined_context = ""

        for result in results:
            combined_context += f"""


    response = client.chat.completions.create(
SOURCE DOCUMENT:
{result['name']}

CONTENT:
{result['content'][:2500]}

==================================================
"""
    

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are Delve AI, a Florida dealership title and registration operational assistant.

Your primary purpose is to classify title and registration scenarios BEFORE providing procedural instructions.

CRITICAL BEHAVIOR RULES:

1. If the user's question is broad, vague, incomplete, or missing operational facts:
- DO NOT immediately provide full procedural instructions.
- FIRST enter INTAKE MODE.
- Ask targeted intake questions to classify the exact FLHSMV procedure scenario.

2. Examples of broad questions:
- dead owner
- duplicate title
- repo
- trust
- lien release
- bonded title
- out of state transfer
- divorce transfer
- title correction

3. In INTAKE MODE:
- Ask concise dealership-style operational intake questions.
- Determine:
    - ownership structure
    - Florida vs out-of-state
    - title availability
    - lien status
    - probate status
    - trust involvement
    - court documents
    - electronic title status
    - required authority/signers

4. DO NOT hallucinate missing facts.
Never assume:
- probate opened
- surviving spouse exists
- title available
- no liens
- valid signatures
- ownership conjunction

5. Only provide final procedural instructions AFTER enough facts are known to classify the scenario.

6. Always prioritize:
- FLHSMV operational procedures
- dealership workflow logic
- exact form requirements
- title authority rules
- lien verification
- ownership conjunction rules

7. Always mention exact HSMV forms when applicable.

8. Keep responses operational, procedural, and dealership-oriented.
Avoid generic legal disclaimers unless escalation is required.

9. Escalate situations involving:
- ownership disputes
- conflicting probate authority
- fraud concerns
- missing heirs
- invalid signatures
- unresolved liens
- court order ambiguity

10. Powers of attorney become void upon death unless specifically allowed by Florida procedure.

Your job is to behave like an experienced Florida title clerk performing procedural intake before processing.
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