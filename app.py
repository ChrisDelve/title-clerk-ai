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
    background-color: #161616;
    color: #EAEAEA;
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
/* PROFESSIONAL TYPOGRAPHY */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Entire App */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main Response Text */
.response-text {
    font-size: 18px;
    line-height: 1.75;
    color: #F5F5F5;
    padding-top: 10px;
}

/* Section Headers */
.response-text h1,
.response-text h2,
.response-text h3 {
    margin-top: 28px;
    margin-bottom: 14px;
    font-weight: 700;
    color: white;
}

/* Bullet Points */
.response-text li {
    margin-bottom: 10px;
}

/* Main Title */
.main-title {
    font-size: 52px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 8px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #CFCFCF;
    margin-bottom: 30px;
}

/* Operational Guidance Header */
.stSubheader {
    margin-top: 40px !important;
    margin-bottom: 20px !important;
}

/* Response Container */
.response-container {
    background-color: #111111;
    border: 1px solid rgba(255, 215, 0, 0.18);
    border-radius: 18px;
    padding: 28px;
    margin-top: 20px;
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
    # Force TL-33 / lien logic priority for ELT + unavailable lienholder questions
    lien_priority_terms = [
        "elt",
        "electronic lien",
        "electronic title",
        "lienholder out of business",
        "lien holder out of business",
        "lienholder unavailable",
        "lienholder unresponsive",
        "cannot get lien release",
        "can't get lien release",
        "active lien",
        "certified mail",
        "5 year",
        "5-year",
        "tl-33"
    ]

    if any(term in query.lower() for term in lien_priority_terms):
        priority_matches = [
            m for m in matches
            if (
                "tl_33" in m["name"].lower()
                or "tl-33" in m["name"].lower()
                or "lien_satisfactions" in m["name"].lower()
                or "lien_logic_map" in m["name"].lower()
                or "rejection_prevention_logic_map" in m["name"].lower()
                or "forms_required_logic_map" in m["name"].lower()
            )
        ]

        non_priority_matches = [
            m for m in matches
            if m not in priority_matches
        ]

        return (priority_matches + non_priority_matches)[:5]

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

    third_temp_words = [
        "third temporary tag",
        "third temp tag",
        "3rd temporary tag",
        "3rd temp tag",
        "regional dmv",
        "approval letter",
        "temporary tag approval"
    ]

    if any(term in query.lower() for term in third_temp_words):
        third_temp_matches = [
            m for m in matches
            if "third_temp_tag" in m["name"].lower()
            or "320.131" in m["name"].lower()
            or "registration_plate_and_insurance" in m["name"].lower()
            or "rejection_prevention_logic_map" in m["name"].lower()
            or "validation_logic_map" in m["name"].lower()
        ]

        non_third_temp_matches = [
            m for m in matches
            if m not in third_temp_matches
        ]

        return (third_temp_matches + non_third_temp_matches)[:5]
    spouse_plate_words = [
        "transfer a plate from their spouse",
        "transfer a plate from spouse",
        "transfer plate from spouse",
        "transfer tag from spouse",
        "plate from their spouse",
        "tag from their spouse",
        "spouse plate",
        "spouse tag",
        "wife plate",
        "wife tag",
        "wife's plate",
        "wife's tag",
        "husband plate",
        "husband tag",
        "husband's plate",
        "husband's tag",
        "use spouse plate",
        "use spouse tag"
        "insurance is in spouse's name",
        "insurance in spouse name",
        "insurance is in wife name",
        "insurance is in husband's name",
        "insurance in husband's name",
        "insurance in wife's name",
        "transfer tag but insurance is in spouse"
    ]

    if any(term in query.lower() for term in spouse_plate_words):
        spouse_plate_matches = [
            m for m in matches
            if "320.0609" in m["name"].lower()
            or "320.072" in m["name"].lower()
            or "registration_plate_and_insurance" in m["name"].lower()
            or "plate_registration_action_logic_map" in m["name"].lower()
            or "rejection_prevention_logic_map" in m["name"].lower()
            or "validation_logic_map" in m["name"].lower()
            or "320.02" in m["name"].lower()
        ]

        non_spouse_plate_matches = [
            m for m in matches
            if m not in spouse_plate_matches
        ]
    
        return (spouse_plate_matches + non_spouse_plate_matches)[:5]
    
    new_plate_to_transfer_words = [
        "changed from new plate to transfer tag",
        "new plate to transfer tag after delivery",
        "customer wants to switch from new plate to transfer tag",
        "issued new plate but customer has tag to transfer",
        "new plate was issued and customer wants transfer tag",
        "customer changed from new plate to transfer tag after delivery"
    ]

    if any(term in query.lower() for term in new_plate_to_transfer_words):
        new_plate_to_transfer_matches = [
            m for m in matches
            if "efs_01" in m["name"].lower()
            or "electronic_filing_system_efs" in m["name"].lower()
            or "320.0609" in m["name"].lower()
            or "registration_plate_and_insurance" in m["name"].lower()
            or "plate_registration_action_logic_map" in m["name"].lower()
            or "rejection_prevention_logic_map" in m["name"].lower()
            or "validation_logic_map" in m["name"].lower()
        ]

        non_new_plate_to_transfer_matches = [
            m for m in matches
            if m not in new_plate_to_transfer_matches
        ]

        return (new_plate_to_transfer_matches + non_new_plate_to_transfer_matches)[:5]
    insurance_words = [
        "insurance",
        "florida insurance",
        "proof of insurance",
        "no valid insurance",
        "no insurance",
        "invalid insurance"
    ]

    if any(term in query.lower() for term in insurance_words):
        insurance_matches = [
            m for m in matches
            if "320.02" in m["name"].lower()
            or "registration_plate_and_insurance" in m["name"].lower()
            or "validation_logic_map" in m["name"].lower()
            or "rejection_prevention_logic_map" in m["name"].lower()
        ]

        non_insurance_matches = [
            m for m in matches
            if m not in insurance_matches
        ]

        return (insurance_matches + non_insurance_matches)[:5]
    

    return matches[:5]

# ----------------------------
# USER INPUT
# ----------------------------


user_question = st.text_input(
    "Ask a question",
    placeholder="Example: What forms do I need for an out-of-state title transfer?"
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
- probate transfer
- registration transfer
- salvage title
- non-title transfer

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
STRICT TL-33 RESPONSE RULE:

When the user asks about:
- ELT
- active lien
- lienholder out of business
- lienholder unavailable
- lienholder unresponsive
- cannot get lien release
- paid off lien still showing

The answer must include a TL-33 review section with these exact operational checks:

1. Active ELT liens must normally be released electronically.
2. Alternate lien removal is not normally available for active ELT liens.
3. Certified mail proof may be required if lienholder is unavailable or unresponsive.
4. Certified letter must be mailed at least 20 days before application.
5. Payoff proof is required if using an alternate lien removal path.
6. If no sales contract and no payoff record exist, review the 5-year rule or court order requirement.
7. HSMV 82260 is not sufficient for an active ELT lien.
8. HSMV 82139 should only be discussed when lien assignment, successor lienholder, or lien reassignment is involved.
9. Escalate to title lead, tax collector, or FLHSMV before submission.

Do not make bonded title the main solution for active ELT lien problems.

If no sales contract or payoff proof exists, review the 5-year rule or court order requirement before proceeding.
If payoff proof, sales contract, cancelled checks, or lien satisfaction proof is missing, always mention the TL-33 5-year rule or court order review before allowing the transaction to proceed.
STRICT ODOMETER FORM RULE:

Do not call HSMV 82040 an odometer disclosure statement.

HSMV 82040 is a title application.

For odometer disclosure or mileage discrepancy questions, review HSMV 82993, HSMV 82994, HSMV 82995, HSMV 82996, TL-09, and the applicable title correction path.

Do not say one form alone fixes a mileage-unit discrepancy.

STRICT ODOMETER AGE EXEMPTION RULE:

Do not say odometer disclosure is generally required for vehicles less than 10 years old.

For model year 2011 and newer vehicles, odometer disclosure exemption applies after 20 years.

For model year 2010 and older vehicles, odometer disclosure exemption applies after 10 years.

If the model year is unknown, say to verify the model year before determining odometer disclosure exemption.

STRICT KILOMETER MILEAGE WORDING RULE:

Do not broadly state that every Florida title must show mileage in miles without review.

When a title or supporting document shows kilometers, say this is an odometer unit discrepancy that requires verification, supporting documentation, and title lead / tax collector / FLHSMV review before submission.

Do not guess the conversion from kilometers to miles.

STRICT MILEAGE BRAND RULE:

When a title is branded with incorrect miles, do not treat it as a simple correction.

Separate the issue into:
1. supported clerical error
2. mileage discrepancy
3. Not Actual Mileage brand
4. suspected rollback/tampering/fraud

Do not promise that a mileage brand can be removed or changed.

If supporting mileage documents are missing or conflicting, tell the clerk to hold and escalate to title lead, tax collector, or FLHSMV before submission.
STRICT PLATE TRANSFER RULE:

For transfer tag questions, focus on the registered owner of the plate, not only the title owner of the vehicle.

If the tag is not in the customer's name, do not process as a normal transfer tag.

A customer being the buyer/title applicant does not automatically make someone else's plate transferable to them.

If plate owner does not match customer and no valid statutory exception applies, tell the clerk to review new plate and IRF.

Do not say the tag can transfer merely because the new title will be in the customer's name.

STRICT IRF WORDING RULE:

Do not call IRF "IRP."

IRF means Initial Registration Fee.

IRP means International Registration Plan and should only be used for apportioned/commercial registration issues.

For plate owner mismatch or transfer tag not in customer name, say "new plate and IRF review" or "Initial Registration Fee review."

Do not say "Initial Registration Form."

STRICT AUDIT TRAIL RULE:

For missing audit trail questions, do not answer only as a lien issue.

Treat missing audit trail as a chain-of-ownership and document-support issue.

The answer must verify:
- title record
- current title or valid duplicate
- prior title if needed
- reassignment chain
- bill of sale or purchase agreement
- customer identity
- lien release or ELT status if applicable
- odometer disclosure if applicable
- power of attorney if used
- DLRDMV uploaded documents, rejection notes, and transaction history if applicable

If the audit trail cannot be reconstructed, tell the clerk to hold and escalate before submission.

STRICT GIFTED TRADE RULE:

For "gifted trade" or "third-party trade" questions, do not treat the issue only as a normal title transfer to dealer inventory.

Always identify three parties:
1. titled owner of the trade vehicle
2. buyer of the new vehicle
3. person receiving the trade credit

If the trade owner and buyer are not the same person, require documentation showing the trade owner authorizes the trade value or trade credit to be used for the buyer.

Do not assume sales tax trade credit applies. Tell the clerk to verify tax credit eligibility before applying trade credit/tax benefit.

Do not route to bonded title unless the title is missing, defective, or ownership cannot be proven.

STRICT FLORIDA INSURANCE RULE:

For questions about no insurance, invalid insurance, missing Florida insurance, proof of insurance, or customer has no valid Florida insurance, treat the issue as a registration/plate issuance block.

Use Florida registration law guidance, especially 320.02.

If valid Florida insurance proof is missing, do not complete registration, plate issuance, or transfer plate issuance.

A title-only transaction may be possible if no registration or license plate is being issued, but the answer must clearly separate title-only from registration/plate issuance.

Do not answer this primarily as a signature, trust, fee, OHV, or general title transfer issue.

STRICT THIRD TEMP TAG RULE:

For third temporary tag or 3rd temp tag questions, do not say it can be issued as a normal temporary tag.

A third temporary tag requires dealership approval first.

Required workflow:
1. Get General Manager or Controller approval.
2. Email the regional DMV office for the store's region requesting approval.
3. Include customer name, VIN, valid insurance, buyer's order or bill of sale, and reason the third temp tag is needed.
4. If regional DMV approves, send the approval letter to the agency.
5. Send the agency the customer name, VIN, insurance, buyer's order, and approval letter.
6. Agency processes the third temporary tag.

If approval letter is missing, tell the clerk not to proceed.

STRICT SPOUSE PLATE TRANSFER RULE:

For spouse plate transfer questions, do not say the plate can transfer automatically because the customer is married.

Always verify:
1. registered owner of the plate
2. titled owner/applicant of the new vehicle
3. who will be listed as registrant
4. whether the spouse is being added as owner or co-registrant
5. valid Florida insurance
6. signatures and ID for any party being added or relied on

If the spouse owns the plate but is not an owner or registrant on the new vehicle, tell the clerk to process as new plate and review IRF unless a valid exception or tax collector guidance applies.

STRICT NEW PLATE TO TRANSFER TAG AFTER DELIVERY RULE:

For questions where a customer was issued a new plate but later wants to change to a transfer tag after delivery, do not answer only as a normal plate transfer.

Treat this first as an EFS inventory and void workflow issue.

Required workflow:
1. Verify whether the new plate was issued.
2. Verify whether the plate was placed on the vehicle.
3. Verify whether the vehicle left the dealership.
4. If the plate was issued/placed after delivery, void the original EFS transaction.
5. Return the issued plate to the tax collector or license plate agency.
6. Verify the customer’s transfer plate eligibility.
7. Reprocess correctly as a transfer tag only if the plate is eligible.
8. If the transfer plate is not eligible, process as new plate and review IRF.
9. Escalate if EFS inventory status, returned plate status, or transfer eligibility is unclear.

Do not say this is only a normal plate transfer.

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

        st.subheader("Operational Guidance")

        ai_answer = ai_answer.replace("`", "")

        st.markdown(ai_answer.replace("`", ""), unsafe_allow_html=False)

        st.divider()

        # ----------------------------
        # SOURCES USED
        # ----------------------------

        st.subheader("Sources Used")

        for result in results:

            with st.expander(result["name"]):

                st.caption(f"Match Score: {result['score']}")

                st.text(result["content"][:3000])