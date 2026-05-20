from annotated_types import doc
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

.scope-note {
    max-width: 900px;
    margin: 1.25rem auto 1.2rem auto;
    padding: 0.85rem 1rem;
    border: 1px solid rgba(255, 204, 64, 0.28);
    border-radius: 10px;
    background: rgba(255, 204, 64, 0.06);
    color: rgba(255, 255, 255, 0.72);
    font-size: 0.86rem;
    line-height: 1.45;
    text-align: left;
}

.scope-note strong {
    color: rgba(255, 218, 95, 0.95);
    font-weight: 700;
}

.app-subtext {
    max-width: 900px;
    margin: 1.15rem auto 0.25rem auto;
    padding: 0 0.15rem;
    color: rgba(255, 255, 255, 1);
    font-size: 1.65rem;
    font-weight: 900;
    line-height: 1.32;
    letter-spacing: -0.35px;
    text-align: center;
    text-shadow: 0 1px 10px rgba(0, 0, 0, 0.35);
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
.logo-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 0.5rem;
    margin-bottom: 1.1rem;
    transform: translateX(70px);
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
st.image("logo.png", width=850)
st.markdown('</div>', unsafe_allow_html=True)


st.markdown(
    """
    <div class="scope-note">
        <strong>Scope Note:</strong> This assistant provides dealership title and registration workflow guidance
        based on uploaded Florida statutes, FLHSMV procedures, and internal operational notes.
        It is not legal advice and does not replace FLHSMV, tax collector, lender, controller,
        management, or compliance approval. When ownership, lien, odometer, fraud, legal authority,
        or registration issues are unclear, hold and escalate before submission.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class="app-subtext">
        Ask about duplicate titles, ELT, lien releases, registrations, fees, title procedures, and rejection prevention.
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

EXCLUDED_SOURCE_FILES = {
    "passed_issue_tests.txt",
    "demo_question_list.txt",
}

for root, dirs, files in os.walk(docs_path):

    for file in files:

        if file in EXCLUDED_SOURCE_FILES:
            continue

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
                        "path": filepath,
                        "content": content
                    })

            except Exception as e:
                print(f"Error loading TXT {file}: {e}")

        # ---------------- PDF FILES ----------------


# ----------------------------
# SEARCH FUNCTION
# ----------------------------

def clean_source_name(filename):
    """
    Converts internal TXT file names into cleaner display names for the app UI.
    This does NOT rename the actual files. It only changes how sources appear to users.
    """

    source_labels = {
        # Core logic maps
        "rejection_prevention_logic_map.txt": "Rejection Prevention Logic Map",
        "validation_logic_map.txt": "Validation Logic Map",
        "plate_registration_action_logic_map.txt": "Plate / Registration Action Logic Map",
        "forms_required_logic_map.txt": "Required Forms Logic Map",
        "lien_logic_map.txt": "Lien Logic Map",

        # Registration / plates / insurance
        "fl_registration_plate_and_insurance_law_notes.txt": "Registration / Plate / Insurance Law Notes",
        "320.02_Operational_Notes.txt": "Florida Statute 320.02 — Registration / Insurance Requirements",
        "320.0609_Operational_Notes.txt": "Florida Statute 320.0609 — Plate Transfer / Plate Owner Rules",
        "320.131_Operational_Notes.txt": "Florida Statute 320.131 — Temporary Tags",
        "320.072_Operational_Notes.txt": "Florida Statute 320.072 — Initial Registration Fee",
        "320.07_Operational_Notes.txt": "Florida Statute 320.07 — Expiration / Delinquent Registration",
        "320.03_Operational_Notes.txt": "Florida Statute 320.03 — Tax Collector / Registration Processing",

        # Title ownership / transfer
        "fl_title_ownership_and_transfer_law_notes.txt": "Title Ownership / Transfer Law Notes",
        "fl_tl_11_transfer_of_florida_certificate_of_title_operational_notes.txt": "TL-11 — Transfer of Florida Certificate of Title",
        "fl_tl_01_signature_requirements_operational_notes.txt": "TL-01 — Signature Requirements",
        "fl_tl_05_duplicate_titles_operational_notes.txt": "TL-05 — Duplicate Titles",
        "fl_tl_18_deceased_owner_workflow_notes.txt": "TL-18 — Deceased Owner Workflow",
        "fl_tl_52_mark_title_sold_notes.txt": "TL-52 — Mark Title Sold / Dealer Trade Workflow",

        # Title statutes
        "319.20_Operational_Notes.txt": "Florida Statute 319.20 — Title Requirements",
        "319.21_Operational_Notes.txt": "Florida Statute 319.21 — Certificate of Origin / Owner Name",
        "319.22_Operational_Notes.txt": "Florida Statute 319.22 — Transfer of Title / Ownership",
        "319.23_Operational_Notes.txt": "Florida Statute 319.23 — Application for Title",
        "319.24_Operational_Notes.txt": "Florida Statute 319.24 — Title Delivery / Lien Delivery",
        "319.27_Operational_Notes.txt": "Florida Statute 319.27 — Liens",
        "319.28_Operational_Notes.txt": "Florida Statute 319.28 — Operation of Law / Deceased / Repossession",
        "319.29_Operational_Notes.txt": "Florida Statute 319.29 — Duplicate Title",
        "319.33_Operational_Notes.txt": "Florida Statute 319.33 — Fraud / False Statements / VIN Offenses",
        "319.34_Operational_Notes.txt": "Florida Statute 319.34 — Transfer Without Title Delivery",
        "319.235_Operational_Notes.txt": "Florida Statute 319.235 — Encumbrances / Liens",

        # Odometer / mileage
        "fl_odometer_and_mileage_law_notes.txt": "Odometer / Mileage Law Notes",
        "319.225_Operational_Notes.txt": "Florida Statute 319.225 — Odometer Disclosure",
        "319.23_Odometer_Operational_Notes.txt": "Florida Statute 319.23 — Odometer / Title Application",
        "319.24_Odometer_Operational_Notes.txt": "Florida Statute 319.24 — Odometer / Title Delivery",
        "319.324_Operational_Notes.txt": "Florida Statute 319.324 — Odometer Verification",
        "319.35_Operational_Notes.txt": "Florida Statute 319.35 — Odometer / Title Certificates",

        # Liens / ELT
        "fl_lien_and_lien_satisfaction_law_notes.txt": "Lien / Lien Satisfaction Law Notes",
        "fl_tl_33_lien_satisfactions_and_alternate_methods_of_removal_of_recorded_liens_notes.txt": "TL-33 — Lien Satisfaction / Alternate Lien Removal",
        "319.241_Operational_Notes.txt": "Florida Statute 319.241 — Electronic Liens / ELT",

        # EFS
        "fl_efs_01_electronic_filing_system_inventory_notes.txt": "EFS-01 — Electronic Filing System Inventory",
        "fl_efs_02_electronic_filing_system_records_retention_notes.txt": "EFS-02 — EFS Records Retention",
        "fl_electronic_filing_system_efs_law_notes.txt": "Electronic Filing System / EFS Master Notes",
        "third_temp_tag_regional_dmv_office_lookup_notes.txt": "Third Temp Tag — Regional DMV Office Lookup",

        # Passport / registration ID
        "fl_info_24_023_rule_15c_1_015_valid_passport_registration_notes.txt": "INFO 24-023 / Rule 15C-1.015 — Valid Passport for Registration",

        # Fees
        "fl_fees_01_schedule_of_title_and_lien_fees_notes.txt": "FEES-01 — Schedule of Title and Lien Fees",
        "fl_fees01_Raw_Fee_Table .txt": "FEES-01 — Raw Title / Lien Fee Table",
        "fees-01_AI_Logic_Map.txt": "FEES-01 — Title / Lien Fee Logic Map",
        "fees-02_AI_Logic_Map.txt": "FEES-02 — Registration Fee Logic Map",
        "fees-03_AI_Logic_Map.txt": "FEES-03 — Motor Vehicle Class Code / Fee Chart",
        "fees-04_AI_Logic_Map.txt": "FEES-04 — Vessel Registration Fee Chart",

        # Forms
        "HSMV-82040_Operational_Notes.txt": "HSMV 82040 — Application for Certificate of Title With/Without Registration",
    }

    return source_labels.get(filename, filename)

def search_documents(query):

    query_lower = query.lower()
    query_words = query_lower.split()

    matches = []

    out_of_state_customer_keywords = [
        "title in",
        "register in",
        "customer wants to title in",
        "customer wants to register in",
        "out of state customer",
        "out-of-state customer",
        "customer from",
        "what do i need to title this customer in",
        "what do i need to register this customer in",
    ]

    for doc in DOCUMENTS:

        score = 0

        content_lower = doc["content"].lower()
        doc_name_lower = doc["name"].lower()
        doc_path_lower = doc.get("path", "").lower()

        doc_identity_lower = (
            doc_name_lower
            + " "
            + doc_path_lower
            + " "
            + content_lower[:800]
        )

        plate_only_fee_question = (
            (
                "new plate" in query_lower
                or "new tag" in query_lower
                or "license plate" in query_lower
                or "how much is a new plate" in query_lower
                or "how much is a new tag" in query_lower
            )
            and "duplicate title" not in query_lower
            and "transfer title" not in query_lower
            and "original title" not in query_lower
        )

        if (
            "advanced replacement" not in query_lower
            and "advance replacement" not in query_lower
            and "replacement plate" not in query_lower
            and "replace plate" not in query_lower
            and "replacement tag" not in query_lower
            and (
                "fl_rs_42" in doc_identity_lower
                or "advanced_replacement" in doc_identity_lower
                or "advance_replacement" in doc_identity_lower
            )
        ):
            continue

        if plate_only_fee_question and (
            "fees-01" in doc_identity_lower
            or "fees_01" in doc_identity_lower
            or "fl_fees_01" in doc_identity_lower
            or "fl_fees01" in doc_identity_lower
            or "raw title" in doc_identity_lower
            or "raw_title" in doc_identity_lower
            or "title / lien" in doc_identity_lower
            or "title and lien" in doc_identity_lower
            or "title_and_lien" in doc_identity_lower
            or "schedule of title and lien" in doc_identity_lower
        ):
            continue

        if plate_only_fee_question and (
            "fl_rs_35" in doc_identity_lower
            or "delinquent registration" in doc_identity_lower
            or "delinquent_registration" in doc_identity_lower
        ):
            continue

        # ------------------------------------------------------------
        # GOLF CART / LOW-SPEED VEHICLE ROUTING
        # ------------------------------------------------------------

        golf_cart_keywords = [
            "golf cart",
            "golfcart",
            "low speed vehicle",
            "low-speed vehicle",
            "lsv",
            "converted golf cart",
            "street legal golf cart",
            "street-legal golf cart",
            "hsmv 86064",
            "hsmv 84490",
        ]

        golf_cart_question = any(phrase in query_lower for phrase in golf_cart_keywords)

        if golf_cart_question:
            if "fl_golf_cart_low_speed_vehicle_lsv_notes" in doc_name_lower:
                score += 300

            if "import_export_vehicle_logic_map" in doc_name_lower:
                score -= 150

            if "us_cbp_" in doc_name_lower:
                score -= 200

            if "canada_cbsa" in doc_name_lower:
                score -= 200

            if "customer_titling_requirements_notes" in doc_name_lower:
                score -= 150

            if "out_of_state_customer_title_notes" in doc_path_lower:
                score -= 150

            if "mississippi" in doc_name_lower or "west_virginia" in doc_name_lower:
                score -= 200
            
        if (
            "off highway" not in query_lower
            and "off-highway" not in query_lower
            and "ohv" not in query_lower
            and "atv" not in query_lower
            and "dirt bike" not in query_lower
            and "all-terrain" not in query_lower
            and (
                "off_highway" in doc_name_lower
                or "ohv" in doc_name_lower
            )
        ):
            continue

        if (
            "export" not in query_lower
            and "exporting" not in query_lower
            and "ship out" not in query_lower
            and "shipping out" not in query_lower
            and "out of the country" not in query_lower
            and "leaving the united states" not in query_lower
            and "leaving the u.s." not in query_lower
            and "port of export" not in query_lower
            and "cbp" not in query_lower
            and "customs" not in query_lower
            and "canada" not in query_lower
            and "canadian" not in query_lower
            and "us_cbp_exporting_motor_vehicle_notes" in doc_name_lower
        ):
            continue

        if (
            "power of attorney" not in query_lower
            and "poa" not in query_lower
            and (
                "power_of_attorney" in doc_name_lower
                or "tl_02" in doc_name_lower
            )
        ):
            continue

        if (
            "canada" not in query_lower
            and "canadian" not in query_lower
            and "cbsa" not in query_lower
            and "riv" not in query_lower
            and "transport canada" not in query_lower
            and "canada_cbsa" in doc_name_lower
        ):
            continue

        if "trust" not in query_lower and "trust" in doc_name_lower:
            continue

        if "guardian" not in query_lower and "guardianship" in doc_name_lower:
            continue

        if "replevin" not in query_lower and "repossession" not in query_lower and "replevin" in doc_name_lower:
            continue

        if "bonded" not in query_lower and "bond" not in query_lower and "bonded" in doc_name_lower:
            continue

        if (
            "duplicate" not in query_lower
            and "lost title" not in query_lower
            and "replacement title" not in query_lower
            and "lost-in-transit" not in query_lower
            and "lost in transit" not in query_lower
            and (
                "duplicate" in doc_name_lower
                or "tl_05" in doc_name_lower
            )
        ):
            continue

        if (
            "mobile home" not in query_lower
            and "mobilehome" not in query_lower
            and "manufactured home" not in query_lower
            and (
                "mobile_home" in doc_name_lower
                or "tl_39" in doc_name_lower
            )
        ):
            continue

        if (
            "vessel" not in query_lower
            and "boat" not in query_lower
            and "watercraft" not in query_lower
            and "fl_fees_04_vessel" in doc_name_lower
        ):
            continue

        if (
            "refund" not in query_lower
            and "refunds" not in query_lower
            and "fl_rs_65_refunds" in doc_name_lower
        ):
            continue

        if (
            "delinquent" not in query_lower
            and "late" not in query_lower
            and "expired" not in query_lower
            and "expiration" not in query_lower
            and "penalty" not in query_lower
            and "renewal" not in query_lower
            and "renew" not in query_lower
            and (
                "fl_rs_35" in doc_name_lower
                or "delinquent_registration" in doc_name_lower
                or "delinquent" in doc_name_lower
            )
        ):
            continue

        fee_question_keywords = [
            "fee",
            "fees",
            "cost",
            "how much",
            "price",
            "charge",
            "pay",
            "amount",
        ]

        fee_question = any(phrase in query_lower for phrase in fee_question_keywords)

        if not fee_question:
            if "fees" in doc_path_lower or "fees" in doc_name_lower or "fees-" in doc_name_lower or "fees_" in doc_name_lower:
                score -= 100

        if (
            "divorce" not in query_lower
            and "dissolution" not in query_lower
            and "marriage" not in query_lower
            and (
                "dissolution_of_marriage" in doc_name_lower
                or "tl_17" in doc_name_lower
            )
        ):
            continue

        if (
            "pawn" not in query_lower
            and "pawnbroker" not in query_lower
            and "title pledge" not in query_lower
            and (
                "pawnbroker" in doc_name_lower
                or "pawnbrokers" in doc_name_lower
                or "tl_47" in doc_name_lower
            )
        ):
            continue
        
        if (
            "antique" not in query_lower
            and "ancient" not in query_lower
            and "vessel" not in query_lower
            and (
                "antique" in doc_name_lower
                or "ancient" in doc_name_lower
            )
        ):
            continue

        if (
            "rebuilt" not in query_lower
            and "rebuild" not in query_lower
            and "salvage" not in query_lower
            and "branded" not in query_lower
            and "total loss" not in query_lower
            and "rebuilt_vehicle" in doc_name_lower
        ):
            continue

        if (
            "total loss" not in query_lower
            and "derelict" not in query_lower
            and "junk" not in query_lower
            and "salvage" not in query_lower
            and (
                "total_loss" in doc_name_lower
                or "derelict" in doc_name_lower
                or "junked" in doc_name_lower
            )
        ):
            continue

        if "title loan" not in query_lower and "title_loan" in doc_name_lower:
            continue

        # ------------------------------------------------------------
        # IMPORT / EXPORT / CANADA ROUTING
        # ------------------------------------------------------------

        foreign_import_keywords = [
            "from another country",
            "out of country",
            "out-of-country",
            "foreign vehicle",
            "foreign title",
            "foreign registration",
            "customs",
            "cbp",
            "epa form",
            "3520-1",
            "dot form",
            "hs-7",
            "port of entry",
            "import documents",
            "nonconforming vehicle",
            "not manufactured for u.s.",
            "not manufactured for us",
            "imported from canada",
            "imported from mexico",
            "imported from overseas",
            "imported into the united states",
        ]

        florida_import_keywords = [
            "importing a vehicle into florida",
            "import vehicle into florida",
            "bringing a vehicle into florida",
            "bring vehicle into florida",
            "out of state title into florida",
            "out-of-state title into florida",
            "title an out of state vehicle in florida",
            "title an out-of-state vehicle in florida",
            "register an out of state vehicle in florida",
            "register an out-of-state vehicle in florida",
            "vehicle coming into florida",
            "customer moved to florida",
        ]

        export_keywords = [
            "export vehicle",
            "exporting a vehicle",
            "exporting vehicle",
            "shipping vehicle out of the country",
            "ship vehicle out of the country",
            "vehicle leaving the united states",
            "vehicle leaving the u.s.",
            "foreign buyer shipping vehicle",
            "cbp export",
            "customs export",
            "72 hours prior to export",
            "present vehicle to customs",
            "port of export",
            "export documents",
        ]

        canada_keywords = [
            "canada",
            "canadian",
            "cbsa",
            "transport canada",
            "riv",
            "registrar of imported vehicles",
            "cmvss",
            "import into canada",
            "export to canada",
            "taking vehicle to canada",
            "shipping vehicle to canada",
            "canadian customer",
        ]

        foreign_import_question = (
            any(phrase in query_lower for phrase in foreign_import_keywords)
            or (
                "import" in query_lower
                and any(word in query_lower for word in ["country", "foreign", "customs", "cbp", "epa", "dot", "hs-7", "3520"])
            )
        )

        florida_import_question = (
            any(phrase in query_lower for phrase in florida_import_keywords)
            and not foreign_import_question
        )

        export_question = any(phrase in query_lower for phrase in export_keywords)

        canada_question = any(phrase in query_lower for phrase in canada_keywords)

        if (
            "import" in query_lower
            or "export" in query_lower
            or "canada" in query_lower
            or "canadian" in query_lower
            or "foreign" in query_lower
            or "customs" in query_lower
            or "cbp" in query_lower
        ):
            if "import_export_vehicle_logic_map" in doc_name_lower:
                score += 200

        # ------------------------------------------------------------
        # FLORIDA PLATE / TAG TRANSFER ROUTING
        # ------------------------------------------------------------

        plate_transfer_keywords = [
            "transfer tag",
            "transfer plate",
            "tag transfer",
            "plate transfer",
            "tag is not in customer",
            "plate is not in customer",
            "tag not in customer",
            "plate not in customer",
            "not in customer's name",
            "not in customers name",
            "new plate",
            "initial registration fee",
            "irf",
            "new tag",
            "how much is a new tag",
            "original plate",
        ]

        plate_transfer_question = any(phrase in query_lower for phrase in plate_transfer_keywords)

        if plate_transfer_question:
            if "out_of_state_customer_title_notes" in doc_path_lower:
                score -= 200

            if "customer_titling_requirements_notes" in doc_name_lower:
                score -= 200

            if "fees-01" in doc_name_lower or "fl_fees_01" in doc_name_lower:
                score -= 200

            if "title_and_lien" in doc_name_lower or "title_lien" in doc_name_lower:
                score -= 200    

            if "mobile_home" in doc_name_lower or "tl_39" in doc_name_lower:
                score -= 200

            if "registration" in doc_name_lower:
                score += 60

            if "initial_registration" in doc_name_lower:
                score += 80

            if "license_plate" in doc_name_lower or "plate" in doc_name_lower:
                score += 80

            if "rejection_prevention" in doc_name_lower:
                score += 40

            if "fl_fees_02_registration_fees_notes" in doc_name_lower:
                score += 120

            if "fl_rs_30_initial_registration_fee_notes" in doc_name_lower:
                score += 120

            if "plate_registration_action_logic" in doc_name_lower or "registration_action_logic" in doc_name_lower:
                score += 80

            if "registration" in doc_name_lower and "plate" in doc_name_lower:
                score += 60

            if (
                "fees-01" in doc_name_lower
                or "fees_01" in doc_name_lower
                or "fl_fees_01" in doc_name_lower
                or "raw_title" in doc_name_lower
                or "title_lien" in doc_name_lower
                or "title_and_lien" in doc_name_lower
                or "schedule_of_title_and_lien" in doc_name_lower
            ):
                score -= 500    

        # Canadian customer / Canada import routing
        if canada_question:
            if "canada_cbsa_importing_vehicle_notes" in doc_name_lower:
                score += 250

            if "us_cbp_exporting_motor_vehicle_notes" in doc_name_lower:
                score += 120

            if "us_cbp_importing_motor_vehicle_notes" in doc_name_lower:
                score -= 50

            if "customer_titling_requirements_notes" in doc_name_lower:
                score -= 75

            if "out_of_state_customer_title_notes" in doc_path_lower:
                score -= 75

        # Vehicle exported out of the United States
        if export_question and not canada_question:
            if "us_cbp_exporting_motor_vehicle_notes" in doc_name_lower:
                score += 250

            if "us_cbp_importing_motor_vehicle_notes" in doc_name_lower:
                score -= 50

            if "canada_cbsa_importing_vehicle_notes" in doc_name_lower:
                score -= 50

            if "customer_titling_requirements_notes" in doc_name_lower:
                score -= 75

            if "out_of_state_customer_title_notes" in doc_path_lower:
                score -= 75

            if "fees" in doc_path_lower or "fees" in doc_name_lower:
                score -= 100

            if "customer_service_center" in doc_name_lower or "title_support" in doc_name_lower:
                score -= 100

        # Vehicle imported from another country into the U.S. / Florida
        if foreign_import_question and not canada_question:
            if "us_cbp_importing_motor_vehicle_notes" in doc_name_lower:
                score += 250

            if "fl_tl_10" in doc_name_lower:
                score += 80

            if "original_certificate_of_title_operational_notes" in doc_name_lower:
                score += 100

            if "82040" in content_lower:
                score += 40

            if "82042" in content_lower:
                score += 40

            if "canada_cbsa_importing_vehicle_notes" in doc_name_lower:
                score -= 50    

            if "customer_titling_requirements_notes" in doc_name_lower:
                score -= 75

            if "out_of_state_customer_title_notes" in doc_path_lower:
                score -= 75

        # Normal U.S. out-of-state vehicle coming into Florida
        if florida_import_question:
            if "out_of_state_customer_title_notes" in doc_path_lower:
                score -= 150

            if "customer_titling_requirements_notes" in doc_name_lower:
                score -= 150

            if "us_cbp_importing_motor_vehicle_notes" in doc_name_lower:
                score -= 50

            if "us_cbp_exporting_motor_vehicle_notes" in doc_name_lower:
                score -= 50

            if "canada_cbsa_importing_vehicle_notes" in doc_name_lower:
                score -= 50

            if "fl_tl_10" in doc_name_lower:
                score += 80

            if "original_certificate_of_title_operational_notes" in doc_name_lower:
                score += 100 

            if "original" in doc_name_lower and "title" in doc_name_lower:
                score += 50

            if "vin" in doc_name_lower:
                score += 50

            if "82042" in content_lower:
                score += 50

            if "82040" in content_lower:
                score += 50

            if "odometer" in doc_name_lower:
                score += 30

            if "electronic_lien" in doc_name_lower or "elt" in doc_name_lower:
                score += 20
        
        state_names = [
            "alabama", "alaska", "arizona", "arkansas", "california",
            "colorado", "delaware", "georgia", "hawaii", "idaho",
            "illinois", "indiana", "iowa", "kansas", "kentucky",
            "louisiana", "maine", "maryland", "massachusetts", "michigan",
            "minnesota", "mississippi", "missouri", "montana", "nebraska",
            "nevada", "new hampshire", "new jersey", "new mexico",
            "new york", "north carolina", "north dakota", "ohio",
            "oklahoma", "oregon", "pennsylvania", "rhode island",
            "south carolina", "south dakota", "tennessee", "texas",
            "utah", "vermont", "virginia", "washington",
            "west virginia", "wisconsin", "wyoming"
        ]

        matched_states = [state for state in state_names if state in query_lower]

        for state in matched_states:
            state_file_name = state.replace(" ", "_") + "_customer_titling_requirements_notes"

            if state_file_name in doc_name_lower:
                score += 200

            elif "customer_titling_requirements_notes" in doc_name_lower:
                score -= 50

        # Strongly route out-of-state customer titling questions to state-specific notes
        if any(phrase in query_lower for phrase in out_of_state_customer_keywords):
            if "out_of_state_customer_title_notes" in doc.get("path", "").lower():
                score += 20
            if "customer_titling_requirements_notes" in doc_name_lower:
                score += 20
            if "out_of_state_customer_title_master_logic_map" in doc_name_lower:
                score += 15
            if "fl_motor_vehicle_sales_tax_rates_by_state" in doc_name_lower:
                score += 10
            if "fl_nonresident_motor_vehicle_sales_tax_logic_map" in doc_name_lower:
                score += 10

        

        # Penalize general Florida-only title law sources for this question type
            if "florida statute 319" in doc_name_lower:
                score -= 10

            if "title ownership" in doc_name_lower:
                score -= 8

            if "florida statute 319" in doc_name_lower:
                score -= 10

            if "trust" not in query_lower and "trust" in doc_name_lower:
                score -= 200

        if "title ownership" in doc_name_lower:
            score -= 8    
        if "passed_issue_tests" in doc_name_lower:
            score -= 100
        if "demo_question_list" in doc_name_lower:
            score -= 100
        
        
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
    duplicate_title_fee_words = [
        "how much is a duplicate title",
        "how much is duplicate title",
        "duplicate title fee",
        "lost title fee",
        "replacement title fee",
        "how much for duplicate title",
        "cost of duplicate title",
        "fee for duplicate title"
    ]

    if any(term in query.lower() for term in duplicate_title_fee_words):
        priority_names = [
            "fees01_raw_fee_table",
            "fees-01_ai_logic_map",
            "fees_01_schedule",
            "tl_05",
            "319.29",
            "rejection_prevention_logic_map",
            "validation_logic_map"
        ]

        duplicate_title_fee_matches = [
            m for name in priority_names
            for m in matches
            if name in m["name"].lower().replace(" ", "_")
        ]

        unique_duplicate_title_fee_matches = []
        seen_names = set()

        for m in duplicate_title_fee_matches:
            if m["name"] not in seen_names:
                unique_duplicate_title_fee_matches.append(m)
                seen_names.add(m["name"])

        non_duplicate_title_fee_matches = [
            m for m in matches
            if m["name"] not in seen_names
        ]

        return (unique_duplicate_title_fee_matches + non_duplicate_title_fee_matches)[:5]
    
    out_of_state_original_title_fee_words = [
        "how much is an original title from out of state",
        "original title from out of state fee",
        "out of state original title fee",
        "out-of-state original title fee",
        "how much to title an out of state vehicle",
        "how much to title an out-of-state vehicle",
        "previously titled in another state fee",
        "previously registered in another state fee",
        "original title previously titled in another state",
        "original title previously registered in another state"
    ]

    if any(term in query.lower() for term in out_of_state_original_title_fee_words):
        priority_names = [
            "fees01_raw_fee_table",
            "fees-01_ai_logic_map",
            "fees_01_schedule",
            "319.23",
            "registration_plate_and_insurance",
            "320.02",
            "validation_logic_map",
            "rejection_prevention_logic_map"
        ]

        out_of_state_original_title_fee_matches = [
            m for name in priority_names
            for m in matches
            if name in m["name"].lower().replace(" ", "_")
        ]

        unique_out_of_state_original_title_fee_matches = []
        seen_names = set()

        for m in out_of_state_original_title_fee_matches:
            if m["name"] not in seen_names:
                unique_out_of_state_original_title_fee_matches.append(m)
                seen_names.add(m["name"])

        non_out_of_state_original_title_fee_matches = [
            m for m in matches
            if m["name"] not in seen_names
        ]

        return (unique_out_of_state_original_title_fee_matches + non_out_of_state_original_title_fee_matches)[:5]

    transfer_title_fee_words = [
        "how much is a transfer title",
        "transfer title fee",
        "title transfer fee",
        "how much to transfer title",
        "fee to transfer title",
        "cost of transfer title",
        "how much is title transfer"
    ]

    if any(term in query.lower() for term in transfer_title_fee_words):
        priority_names = [
            "fees01_raw_fee_table",
            "fees-01_ai_logic_map",
            "fees_01_schedule",
            "tl_11",
            "319.22",
            "rejection_prevention_logic_map",
            "validation_logic_map"
        ]

        transfer_title_fee_matches = [
            m for name in priority_names
            for m in matches
            if name in m["name"].lower().replace(" ", "_")
        ]

        unique_transfer_title_fee_matches = []
        seen_names = set()

        for m in transfer_title_fee_matches:
            if m["name"] not in seen_names:
                unique_transfer_title_fee_matches.append(m)
                seen_names.add(m["name"])

        non_transfer_title_fee_matches = [
            m for m in matches
            if m["name"] not in seen_names
        ]

        return (unique_transfer_title_fee_matches + non_transfer_title_fee_matches)[:5]

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
    
    blank_odometer_words = [
        "odometer disclosure is blank on the title",
        "blank odometer disclosure",
        "odometer left blank",
        "mileage blank on title",
        "seller left odometer blank",
        "title missing odometer",
        "odometer disclosure blank"
    ]

    if any(term in query.lower() for term in blank_odometer_words):
        priority_names = [
            "odometer_and_mileage_law_notes",
            "319.225",
            "319.23_odometer",
            "validation_logic_map",
            "rejection_prevention_logic_map",
            "tl_11",
            "tl_01"
        ]

        blank_odometer_matches = [
            m for name in priority_names
            for m in matches
            if name in m["name"].lower()
        ]

        unique_blank_odometer_matches = []
        seen_names = set()

        for m in blank_odometer_matches:
            if m["name"] not in seen_names:
                unique_blank_odometer_matches.append(m)
                seen_names.add(m["name"])

        non_blank_odometer_matches = [
            m for m in matches
            if m["name"] not in seen_names
        ]

        return (unique_blank_odometer_matches + non_blank_odometer_matches)[:5]

    wrong_signature_area_words = [
        "seller signed the wrong area on the title",
        "seller signed wrong spot on title",
        "seller signed in wrong place",
        "signature in wrong area on title",
        "seller signed buyer section",
        "seller signed wrong box",
        "seller signature wrong area",
        "seller signed wrong area"
    ]

    if any(term in query.lower() for term in wrong_signature_area_words):
        priority_names = [
            "tl_11",
            "tl_01",
            "title_ownership_and_transfer",
            "validation_logic_map",
            "rejection_prevention_logic_map",
            "tl_05"
        ]

        wrong_signature_area_matches = [
            m for name in priority_names
            for m in matches
            if name in m["name"].lower()
        ]

        unique_wrong_signature_area_matches = []
        seen_names = set()

        for m in wrong_signature_area_matches:
            if m["name"] not in seen_names:
                unique_wrong_signature_area_matches.append(m)
                seen_names.add(m["name"])

        non_wrong_signature_area_matches = [
            m for m in matches
            if m["name"] not in seen_names
        ]

        return (unique_wrong_signature_area_matches + non_wrong_signature_area_matches)[:5]
    
    and_ownership_signature_words = [
        "florida title shows and between owners but only one owner signed",
        "and title only one owner signed",
        "title says and but one owner signed",
        "only one owner signed and title says and",
        "joint owners and only one signature",
        "missing owner signature and title",
        "and ownership only one signature",
        "and ownership missing signature"
    ]

    if any(term in query.lower() for term in and_ownership_signature_words):
        priority_names = [
            "tl_11",
            "tl_01",
            "title_ownership_and_transfer",
            "validation_logic_map",
            "rejection_prevention_logic_map"
        ]

        and_ownership_signature_matches = [
            m for name in priority_names
            for m in matches
            if name in m["name"].lower()
        ]

        unique_and_ownership_signature_matches = []
        seen_names = set()

        for m in and_ownership_signature_matches:
            if m["name"] not in seen_names:
                unique_and_ownership_signature_matches.append(m)
                seen_names.add(m["name"])

        non_and_ownership_signature_matches = [
            m for m in matches
            if m["name"] not in seen_names
        ]

        return (unique_and_ownership_signature_matches + non_and_ownership_signature_matches)[:5]

    seller_title_transfer_tag_words = [
        "transfer tag but title is still in seller's name",
        "transfer tag but title is still in seller’s name",
        "transfer plate but title is still in seller's name",
        "transfer plate but title is still in seller’s name",
        "title still in seller's name",
        "title still in seller’s name",
        "title still in sellers name",
        "seller name on title but customer wants tag transfer",
        "seller's name on title but customer wants tag transfer",
        "seller’s name on title but customer wants tag transfer",
        "customer wants to transfer tag before title transfer",
        "tag transfer before title is in customer name",
        "title not in customer's name but wants transfer tag",
        "title not in customer’s name but wants transfer tag",
        "title not in customer name transfer tag",
        "title still in seller name transfer tag"
    ]

    if any(term in query.lower() for term in seller_title_transfer_tag_words):
        seller_title_transfer_tag_matches = [
            m for m in matches
            if "title_ownership_and_transfer" in m["name"].lower()
            or "tl_11" in m["name"].lower()
            or "320.0609" in m["name"].lower()
            or "registration_plate_and_insurance" in m["name"].lower()
            or "plate_registration_action_logic_map" in m["name"].lower()
            or "rejection_prevention_logic_map" in m["name"].lower()
            or "validation_logic_map" in m["name"].lower()
            or "tl_01" in m["name"].lower()
        ]

        non_seller_title_transfer_tag_matches = [
            m for m in matches
            if m not in seller_title_transfer_tag_matches
        ]

        return (seller_title_transfer_tag_matches + non_seller_title_transfer_tag_matches)[:5]
    
    expired_registration_transfer_tag_words = [
        "transfer tag but registration is expired",
        "transfer plate but registration is expired",
        "expired registration transfer tag",
        "expired registration transfer plate",
        "expired tag transfer",
        "expired plate transfer",
        "customer wants to transfer expired tag",
        "customer wants to transfer expired plate",
        "customer has expired registration but wants to transfer plate",
        "customer has expired registration but wants to transfer tag",
        "registration expired but wants transfer tag",
        "registration expired but wants transfer plate"
    ]

    if any(term in query.lower() for term in expired_registration_transfer_tag_words):
        priority_names = [
            "registration_plate_and_insurance",
            "320.0609",
            "320.02",
            "plate_registration_action_logic_map",
            "rejection_prevention_logic_map",
            "fees_01",
            "validation_logic_map",
            "title_ownership_and_transfer"
        ]

        expired_registration_transfer_tag_matches = [
            m for name in priority_names
            for m in matches
            if name in m["name"].lower()
        ]

        unique_expired_registration_transfer_tag_matches = []
        seen_names = set()

        for m in expired_registration_transfer_tag_matches:
            if m["name"] not in seen_names:
                unique_expired_registration_transfer_tag_matches.append(m)
                seen_names.add(m["name"])

        non_expired_registration_transfer_tag_matches = [
            m for m in matches
            if m["name"] not in seen_names
        ]

        return (unique_expired_registration_transfer_tag_matches + non_expired_registration_transfer_tag_matches)[:5]
    
    registration_stop_words = [
        "customer has a registration stop and wants the dealer to submit anyway",
        "registration stop submit anyway",
        "customer has registration stop",
        "registration hold wants dealer to submit",
        "registration block wants dealer to submit",
        "customer wants dealer to bypass registration stop",
        "submit with registration stop",
        "registration stop",
        "registration hold",
        "registration block"
    ]

    if any(term in query.lower() for term in registration_stop_words):
        priority_names = [
            "registration_plate_and_insurance",
            "320.02",
            "plate_registration_action_logic_map",
            "rejection_prevention_logic_map",
            "validation_logic_map",
            "title_ownership_and_transfer"
        ]

        registration_stop_matches = [
            m for name in priority_names
            for m in matches
            if name in m["name"].lower()
        ]

        unique_registration_stop_matches = []
        seen_names = set()

        for m in registration_stop_matches:
            if m["name"] not in seen_names:
                unique_registration_stop_matches.append(m)
                seen_names.add(m["name"])

        non_registration_stop_matches = [
            m for m in matches
            if m["name"] not in seen_names
        ]

        return (unique_registration_stop_matches + non_registration_stop_matches)[:5]

    dealer_title_only_words = [
        "customer wants title-only",
        "customer wants title only",
        "customer does not want to register",
        "title only no registration",
        "title-only transaction",
        "customer wants title only and no plate",
        "dealer title only",
        "no registration title only",
        "title only no plate"
    ]

    if any(term in query.lower() for term in dealer_title_only_words):
        priority_names = [
            "registration_plate_and_insurance",
            "320.02",
            "title_ownership_and_transfer",
            "rejection_prevention_logic_map",
            "validation_logic_map",
            "tl_11",
            "319.23",
            "lien_and_lien_satisfaction"
        ]

        dealer_title_only_matches = [
            m for name in priority_names
            for m in matches
            if name in m["name"].lower()
        ]

        unique_dealer_title_only_matches = []
        seen_names = set()

        for m in dealer_title_only_matches:
            if m["name"] not in seen_names:
                unique_dealer_title_only_matches.append(m)
                seen_names.add(m["name"])

        non_dealer_title_only_matches = [
            m for m in matches
            if m["name"] not in seen_names
        ]

        return (unique_dealer_title_only_matches + non_dealer_title_only_matches)[:5]

    out_of_state_title_florida_tag_words = [
        "out-of-state title and wants to transfer their florida tag",
        "out of state title and wants to transfer their florida tag",
        "out-of-state title transfer florida tag",
        "out of state title transfer florida plate",
        "customer has out-of-state title and florida tag",
        "customer has out of state title and florida tag",
        "transfer florida tag with out-of-state title",
        "transfer florida tag with out of state title",
        "florida tag transfer with out-of-state title",
        "florida tag transfer with out of state title"
    ]

    if any(term in query.lower() for term in out_of_state_title_florida_tag_words):
        priority_names = [
            "registration_plate_and_insurance",
            "320.0609",
            "320.02",
            "319.23",
            "plate_registration_action_logic_map",
            "rejection_prevention_logic_map",
            "validation_logic_map",
            "title_ownership_and_transfer",
            "tl_11",
            "tl_01"
        ]

        out_of_state_title_florida_tag_matches = [
            m for name in priority_names
            for m in matches
            if name in m["name"].lower()
        ]

        unique_out_of_state_title_florida_tag_matches = []
        seen_names = set()

        for m in out_of_state_title_florida_tag_matches:
            if m["name"] not in seen_names:
                unique_out_of_state_title_florida_tag_matches.append(m)
                seen_names.add(m["name"])

        non_out_of_state_title_florida_tag_matches = [
            m for m in matches
            if m["name"] not in seen_names
        ]

        return (unique_out_of_state_title_florida_tag_matches + non_out_of_state_title_florida_tag_matches)[:5]

    out_of_state_no_vin_words = [
        "out-of-state title but no vin verification",
        "out of state title but no vin verification",
        "out-of-state title no vin verification",
        "out of state title no vin verification",
        "customer has out-of-state title but no vin verification",
        "customer has out of state title but no vin verification",
        "missing vin verification",
        "vin verification missing",
        "no vin verification"
    ]

    if any(term in query.lower() for term in out_of_state_no_vin_words):
        priority_names = [
            "319.23_operational_notes",
            "320.02",
            "registration_plate_and_insurance",
            "validation_logic_map",
            "rejection_prevention_logic_map",
            "title_ownership_and_transfer",
            "tl_01"
        ]

        out_of_state_no_vin_matches = [
            m for name in priority_names
            for m in matches
            if name in m["name"].lower()
        ]

        unique_out_of_state_no_vin_matches = []
        seen_names = set()

        for m in out_of_state_no_vin_matches:
            if m["name"] not in seen_names:
                unique_out_of_state_no_vin_matches.append(m)
                seen_names.add(m["name"])

        non_out_of_state_no_vin_matches = [
            m for m in matches
            if m["name"] not in seen_names
        ]

        return (unique_out_of_state_no_vin_matches + non_out_of_state_no_vin_matches)[:5]
    
    
    out_of_state_lien_paid_words = [
        "out-of-state title with a lien showing but says it is paid off",
        "out of state title with a lien showing but says it is paid off",
        "out-of-state title shows lien but customer says paid",
        "out of state title shows lien but customer says paid",
        "title has lien showing but customer says paid off",
        "lien showing on out-of-state title",
        "lien showing on out of state title",
        "out-of-state title lien paid off",
        "out of state title lien paid off"
    ]

    if any(term in query.lower() for term in out_of_state_lien_paid_words):
        priority_names = [
            "lien_and_lien_satisfaction",
            "tl_33",
            "319.24",
            "319.27",
            "title_ownership_and_transfer",
            "rejection_prevention_logic_map",
            "validation_logic_map",
            "registration_plate_and_insurance",
            "320.02"
        ]

        out_of_state_lien_paid_matches = [
            m for name in priority_names
            for m in matches
            if name in m["name"].lower()
        ]

        unique_out_of_state_lien_paid_matches = []
        seen_names = set()

        for m in out_of_state_lien_paid_matches:
            if m["name"] not in seen_names:
                unique_out_of_state_lien_paid_matches.append(m)
                seen_names.add(m["name"])

        non_out_of_state_lien_paid_matches = [
            m for m in matches
            if m["name"] not in seen_names
        ]

        return (unique_out_of_state_lien_paid_matches + non_out_of_state_lien_paid_matches)[:5]

    out_of_state_customer_keywords = [
        "title in",
        "register in",
        "customer wants to title in",
        "customer wants to register in",
        "out of state customer",
        "out-of-state customer",
        "customer from",
        "what do i need to title this customer in",
        "what do i need to register this customer in",
    ]

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
    
    deceased_spouse_plate_words = [
        "transfer tag from deceased spouse",
        "transfer plate from deceased spouse",
        "deceased spouse tag",
        "deceased spouse plate",
        "husband passed away transfer tag",
        "wife passed away transfer tag",
        "spouse died and customer wants to use tag",
        "spouse died transfer plate",
        "spouse passed away transfer plate"
    ]

    if any(term in query.lower() for term in deceased_spouse_plate_words):
        deceased_spouse_plate_matches = [
            m for m in matches
            if "deceased_owner" in m["name"].lower()
            or "320.0609" in m["name"].lower()
            or "registration_plate_and_insurance" in m["name"].lower()
            or "plate_registration_action_logic_map" in m["name"].lower()
            or "rejection_prevention_logic_map" in m["name"].lower()
            or "validation_logic_map" in m["name"].lower()
            or "title_ownership_and_transfer" in m["name"].lower()
        ]

        non_deceased_spouse_plate_matches = [
            m for m in matches
            if m not in deceased_spouse_plate_matches
        ]

        return (deceased_spouse_plate_matches + non_deceased_spouse_plate_matches)[:5]
    
    deceased_parent_plate_words = [
        "use deceased parent's tag",
        "use deceased parents tag",
        "transfer deceased parent's tag",
        "transfer tag from deceased parent",
        "deceased parent tag",
        "deceased parent's plate",
        "father passed away use his tag",
        "mother passed away use her tag",
        "parent died and customer wants to use tag",
        "dad passed away use his tag",
        "mom passed away use her tag"
    ]

    if any(term in query.lower() for term in deceased_parent_plate_words):
        deceased_parent_plate_matches = [
            m for m in matches
            if "deceased_owner" in m["name"].lower()
            or "320.0609" in m["name"].lower()
            or "registration_plate_and_insurance" in m["name"].lower()
            or "plate_registration_action_logic_map" in m["name"].lower()
            or "rejection_prevention_logic_map" in m["name"].lower()
            or "validation_logic_map" in m["name"].lower()
            or "title_ownership_and_transfer" in m["name"].lower()
        ]

        non_deceased_parent_plate_matches = [
            m for m in matches
            if m not in deceased_parent_plate_matches
        ]

        return (deceased_parent_plate_matches + non_deceased_parent_plate_matches)[:5]
    
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
    efs_initial_status_words = [
        "efs transaction stuck in initial status",
        "transaction stuck in initial status",
        "efs stuck in initial",
        "cannot advance efs transaction to complete",
        "efs transaction will not complete",
        "initial status cannot complete",
        "stuck in initial status"
    ]

    if any(term in query.lower() for term in efs_initial_status_words):
        efs_initial_status_matches = [
            m for m in matches
            if "efs_01" in m["name"].lower()
            or "electronic_filing_system_efs" in m["name"].lower()
            or "registration_plate_and_insurance" in m["name"].lower()
            or "rejection_prevention_logic_map" in m["name"].lower()
            or "validation_logic_map" in m["name"].lower()
        ]

        non_efs_initial_status_matches = [
            m for m in matches
            if m not in efs_initial_status_matches
        ]

        return (efs_initial_status_matches + non_efs_initial_status_matches)[:5]
    
    financing_fell_through_words = [
        "buyer took delivery but financing fell through after plate was issued",
        "financing fell through after plate was issued",
        "buyer could not obtain financing after delivery",
        "customer took delivery then financing fell through",
        "plate issued then financing fell through",
        "spot delivery financing fell through after plate issued"
    ]

    if any(term in query.lower() for term in financing_fell_through_words):
        financing_fell_through_matches = [
            m for m in matches
            if "efs_01" in m["name"].lower()
            or "electronic_filing_system_efs" in m["name"].lower()
            or "registration_plate_and_insurance" in m["name"].lower()
            or "rejection_prevention_logic_map" in m["name"].lower()
            or "validation_logic_map" in m["name"].lower()
        ]

        non_financing_fell_through_matches = [
            m for m in matches
            if m not in financing_fell_through_matches
        ]

        return (financing_fell_through_matches + non_financing_fell_through_matches)[:5]
    
    buyer_never_possession_words = [
        "buyer never took possession but new plate was issued",
        "buyer never took possession",
        "customer never took possession but plate was issued",
        "new plate issued but buyer never took possession",
        "plate issued but customer never took delivery",
        "vehicle never left dealership but plate was issued",
        "never took delivery but plate was issued"
    ]

    if any(term in query.lower() for term in buyer_never_possession_words):
        buyer_never_possession_matches = [
            m for m in matches
            if "efs_01" in m["name"].lower()
            or "electronic_filing_system_efs" in m["name"].lower()
            or "registration_plate_and_insurance" in m["name"].lower()
            or "rejection_prevention_logic_map" in m["name"].lower()
            or "validation_logic_map" in m["name"].lower()
        ]

        non_buyer_never_possession_matches = [
            m for m in matches
            if m not in buyer_never_possession_matches
        ]

        return (buyer_never_possession_matches + non_buyer_never_possession_matches)[:5]
    
    passport_registration_words = [
        "foreign passport and wants to register",
        "only has a foreign passport",
        "customer only has a foreign passport",
        "customer has a foreign passport",
        "foreign passport registration",
        "can customer register with foreign passport",
        "passport but no florida id",
        "passport but no driver license",
        "valid passport for registration",
        "customer only has passport",
        "customer has passport and wants to register",
        "i-94",
        "permanent resident card",
        "immigrant visa",
        "lawful presence"
    ]

    if any(term in query.lower() for term in passport_registration_words):
        priority_names = [
            "info_24_023",
            "15c_1_015",
            "passport_registration",
            "320.02",
            "registration_plate_and_insurance",
            "validation_logic_map",
            "rejection_prevention_logic_map"
        ]

        passport_registration_matches = [
            m for name in priority_names
            for m in matches
            if name in m["name"].lower()
        ]

        unique_passport_registration_matches = []
        seen_names = set()

        for m in passport_registration_matches:
            if m["name"] not in seen_names:
                unique_passport_registration_matches.append(m)
                seen_names.add(m["name"])

        non_passport_registration_matches = [
            m for m in matches
            if m["name"] not in seen_names
        ]

        return (unique_passport_registration_matches + non_passport_registration_matches)[:5]

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

CANADIAN CUSTOMER / EXPORT TO CANADA HARD RULE:
If the user asks about a Canadian customer, taking a vehicle to Canada, exporting to Canada, importing into Canada, CBSA, RIV, or Transport Canada:

Do NOT default to saying:
- Complete Florida title application HSMV 82040
- Process the Florida title application as usual
- Process the title transfer through EFS as usual
- Submit to the Florida tax collector as the default workflow

Instead say:
- Prepare the dealership ownership/export package.
- Do not default to Florida title application, Florida registration, or Florida plate issuance unless the customer is actually titling/registering the vehicle in Florida.
- The package should include MSO/MCO or properly assigned title, buyer’s order/bill of sale, odometer disclosure/statement if applicable, lienholder information or lien release if financed, and any dealership-required POA/wet-signature documents if applicable.
- Because the vehicle is leaving the United States, U.S. CBP export requirements should be reviewed.
- Required export documentation must be submitted to CBP at least 72 hours prior to export, and the vehicle must be presented to CBP at the port of export.
- Because the vehicle is entering Canada, CBSA / Transport Canada / RIV requirements must be reviewed.
- Not every U.S. vehicle is admissible into Canada.
- Escalate to title lead, controller, lienholder, CBP, CBSA, RIV, export broker, freight forwarder, or Canadian provincial authority if title, lien, export, import, tax/duty, or admissibility is unclear.

GOLF CART / LOW-SPEED VEHICLE HARD RULE:
If the user asks about a golf cart, low-speed vehicle, LSV, converted golf cart, street-legal golf cart, HSMV 86064, or HSMV 84490:

Do NOT answer as if all golf carts are title/register eligible.

Always start by distinguishing:
- Standard golf cart
- Existing low-speed vehicle / LSV
- Golf cart converted to a low-speed vehicle

Use this wording:
- A standard golf cart is not the same as an LSV.
- A standard golf cart is not processed like a normal titled/registered motor vehicle.
- An LSV or converted golf cart may require title/registration if it meets LSV requirements.
- For a converted golf cart, Regional Office inspection and VIN assignment are required before title/registration.

Do NOT soften converted golf cart VIN assignment by saying:
- “if VIN assignment is needed”
- “VIN verification or assignment if applicable”
- “coordinate with Regional Office if needed”

For converted golf carts, say clearly:
- Regional Office inspection and VIN assignment are required before title/registration.

Escalate if classification, top speed, VIN, street-legal status, HSMV 86064, HSMV 84490, conversion receipts, certified weight slip, or insurance is unclear.

CALIFORNIA CUSTOMER TITLING HARD RULE:
If the user asks about a customer titling or registering a vehicle in California, California customer, title in California, register in California, or Florida dealer sale to California customer:

Use these California form labels exactly:
- REG 343 = Application for Title or Registration
- REG 227 = Application for Replacement or Transfer of Title
- REG 262 = Vehicle/Vessel Transfer and Reassignment
- REG 256 = Statement of Facts
- REG 139 = Vehicle Emission System Statement
- REG 4008 = Declaration of Gross Vehicle Weight / Combined Gross Vehicle Weight, commercial vehicles only

Do NOT say:
- REG 139 is a Power of Attorney
- REG 256 is a Power of Attorney
- REG 227 is a Statement of Facts
- REG 4008 is required for non-commercial vehicles

If power of attorney is needed, describe it generically as power of attorney documentation required by dealership/vendor workflow. Do not assign a California REG number to power of attorney unless the source explicitly supports it.

For odometer wording, say:
- Odometer disclosure/statement is required if applicable based on the vehicle’s model year and exemption status.

Do NOT say:
- California requires odometer disclosure only for vehicles less than 10 years old.

Only mention HSMV 82040 if the customer is actually applying for Florida title/registration.

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

STRICT EFS INITIAL STATUS RULE:

For EFS transactions stuck in initial status, do not answer as only a generic title, lien, or audit trail issue.

Treat this first as an EFS inventory/manual processing issue.

Required workflow:
1. Confirm the transaction is stuck in initial status.
2. Identify why it cannot advance to complete status.
3. Check for vehicle, customer, registration, or stop issues.
4. Determine whether a plate was issued or placed on the vehicle.
5. If a plate was issued/placed and the transaction cannot complete, do not reuse the plate as available inventory.
6. Use the Return Voided Inventory to Tax Collector workflow.
7. Inventory should move to RT.
8. Once the tax collector or agency receives the returned inventory, status should move to RR.
9. If a void error occurs or inventory status does not update, contact the tax collector office for Department assistance.

For EFS inventory status, do not say RS means issued. RS means re-issuable. IS means issued. RT means EFS returned. RR means return received.

STRICT BUYER NEVER TOOK POSSESSION / NEW PLATE ISSUED RULE:

For questions where a buyer never took possession but a new plate was issued, do not answer as a normal plate transfer or generic title issue.

Treat this first as an EFS inventory void issue.

Required workflow:
1. Verify whether the buyer truly never took possession.
2. Verify whether the vehicle ever left the dealership.
3. Verify whether the new plate was physically placed on the vehicle.
4. If the buyer never took possession and the plate was not placed on the vehicle, void the EFS transaction and set inventory to available.
5. Inventory should become RS / re-issuable.
6. If the plate was placed on the vehicle or the vehicle left the dealership, do not reuse the plate as available inventory.
7. In that case, use the return-voided-inventory-to-tax-collector workflow.
8. Document possession status, plate placement, void reason, and inventory status.
9. Escalate if the void fails or inventory status does not update.

STRICT FINANCING FELL THROUGH AFTER DELIVERY / PLATE ISSUED RULE:

For questions where the buyer took delivery and financing later fell through after a plate was issued, do not answer as a generic title transfer, bonded title, or normal plate transfer issue.

Treat this first as an EFS inventory void and return issue.

Required workflow:
1. Verify the buyer took possession.
2. Verify the vehicle left the dealership.
3. Verify the plate was issued or placed on the vehicle.
4. If buyer took delivery and the plate was issued/placed, do not set inventory to RS/re-issuable.
5. Void the EFS transaction.
6. Return the issued plate to the tax collector or license plate agency.
7. Inventory should move to RT.
8. Once the tax collector/license plate agency receives the returned inventory, status should move to RR.
9. Escalate if the plate cannot be recovered, the void fails, or inventory status does not update.

STRICT DECEASED SPOUSE PLATE TRANSFER RULE:

For questions where a customer wants to transfer a tag or plate from a deceased spouse, do not answer as a normal spouse plate transfer only.

Required workflow:
1. Verify the registered owner of the plate.
2. Confirm the spouse is deceased.
3. Obtain/review death certificate requirements.
4. Review deceased owner title workflow and surviving spouse authority.
5. Do not accept power of attorney as authority after death unless a specific lawful exception applies.
6. Verify whether the surviving spouse is legally allowed to transfer/use the plate.
7. If authority, probate, estate, or ownership status is unclear, hold and escalate.
8. If the plate cannot legally transfer, process as new plate and review IRF.

STRICT DECEASED PARENT TAG RULE:

For questions where a customer wants to use or transfer a deceased parent’s tag, do not answer as a normal family transfer, spouse transfer, or generic estate issue.

Required workflow:
1. Verify the registered owner of the plate.
2. Confirm the parent is deceased and obtain death certificate requirements.
3. Review deceased owner title workflow.
4. Do not accept power of attorney as authority after death unless a specific lawful exception applies.
5. Do not assume a child or relative can use the deceased parent’s tag.
6. Verify estate authority, court order, surviving spouse authority, or tax collector/FLHSMV-approved authority.
7. If authority is unclear, hold and escalate.
8. If the tag cannot legally transfer, process as new plate and review IRF.

STRICT TITLE STILL IN SELLER'S NAME / TRANSFER TAG RULE:

For questions where a customer wants to transfer a tag but the vehicle title is still in the seller’s name, do not answer as a normal plate transfer only.

Required workflow:
1. Verify whether the title has been properly assigned from seller to customer.
2. Verify seller and buyer signatures, printed names, odometer disclosure if required, and lien status.
3. Verify the registered owner of the plate being transferred.
4. Do not process a normal transfer tag until customer ownership and plate eligibility are established.
5. If the title is open, incomplete, unsigned, or still in seller’s name without proper assignment, hold before submission.
6. If the plate is not registered to the customer and no valid exception applies, process as new plate with IRF review.
7. Escalate if title ownership, signatures, liens, or plate ownership are unclear.

STRICT OUT-OF-STATE TITLE WITH FLORIDA TAG TRANSFER RULE:

For questions where a customer has an out-of-state title and wants to transfer a Florida tag, do not answer as a trust, bankruptcy, bonded title, or generic title-only issue.

Treat this as:
1. Florida title application from an out-of-state title, and
2. Florida plate transfer eligibility.

Required workflow:
1. Verify original out-of-state title is available.
2. Verify title is properly assigned to the customer.
3. Verify seller/buyer signatures and odometer disclosure if required.
4. Verify VIN verification requirement for Florida title/registration.
5. Verify valid Florida insurance.
6. Verify the Florida plate is registered to the customer.
7. If the Florida plate is not registered to the customer, process as new plate and review IRF.
8. If the out-of-state title shows lien or ELT issues, review lien release/TL-33 logic.
9. Do not make TL-33 the primary answer unless lien or ELT issue is present.
10. Hold and escalate if title assignment, VIN verification, lien status, insurance, or plate ownership is unclear.

STRICT FOREIGN PASSPORT REGISTRATION RULE:

For questions where a customer only has a foreign passport and wants to register a vehicle, do not answer as a generic title, fee, odometer, trust, or general ID issue.

Use Rule 15C-1.015 / INFO 24-023.

Required answer:
1. Determine whether registration or plate issuance is involved.
2. A foreign passport alone is not enough for registration.
3. The foreign passport must be unexpired.
4. The customer must also provide lawful-presence documentation:
   - DHS stamp or mark showing lawful presence, OR
   - unexpired I-94, OR
   - current permanent resident card, OR
   - unexpired immigrant visa.
5. If required lawful-presence documentation is missing, hold the registration application.
6. This rule applies to vehicle registration applications, not title-only applications.
7. Do not suggest consular ID, utility bills, lease agreements, or foreign driver license as substitutes for the Rule 15C-1.015 valid passport requirement unless a separate FLHSMV procedure specifically supports that issue.

STRICT OUT-OF-STATE TITLE / VIN VERIFICATION RULE:

For questions where a customer has an out-of-state title but no VIN verification, do not answer as a bonded title, trust, bankruptcy, or generic title issue.

Required workflow:
1. Verify the original out-of-state title is available.
2. Verify the title is properly assigned to the customer.
3. Verify seller/buyer signatures and odometer disclosure if required.
4. Require VIN verification before Florida title/registration submission.
5. Use HSMV 82042 or another authorized VIN verification method.
6. If VIN verification is missing, hold before submission.
7. If VIN does not match the title or appears altered/tampered with, escalate before proceeding.
8. If registration or plate issuance is involved, verify valid Florida insurance.

STRICT OUT-OF-STATE TITLE LIEN SHOWING RULE:

For questions where an out-of-state title shows a lien but the customer says it is paid off, do not accept the customer’s verbal statement as proof of lien satisfaction.

Required workflow:
1. Verify the original out-of-state title and lienholder shown.
2. Require acceptable lien release or lien satisfaction documentation.
3. Verify the lienholder name matches the title/record.
4. Verify title assignment and ownership chain.
5. If lien release is missing, unclear, electronic, out-of-state, or cannot be verified, hold and escalate.
6. Do not automatically say Florida ELT release is required unless the issue involves a Florida ELT or active Florida electronic lien.
7. Use TL-33 only when lien release/removal, unavailable lienholder, ELT issue, certified mail, 5-year rule, or court order review is actually involved.

STRICT LOST TRADE TITLE WORDING RULE:

For questions where a customer traded a vehicle but lost the title, do not say the dealership cannot physically accept the vehicle at all.

Say the dealership should not complete the trade title transfer, submit the title work, or treat the trade as title-ready until valid title authority is resolved.

Valid title authority may include:
1. original title,
2. duplicate title,
3. electronic title release/reassignment,
4. lien release,
5. authorized reassignment or other approved title documentation.

If the title is missing and ownership/lien authority cannot be verified, hold and escalate before submission.

STRICT WRONG SIGNATURE AREA ON TITLE RULE:

For questions where a seller signed the wrong area on the title, do not automatically say a duplicate title is required.

Required workflow:
1. Do not submit the title as-is until reviewed.
2. Identify exactly where the seller signed.
3. Verify the correct assignment section, printed name, buyer section, odometer disclosure, lien section, and any alterations.
4. If the seller is available and the correct assignment can still be completed, review proper re-signature or correction documentation.
5. If the error affects ownership transfer, odometer disclosure, or cannot be corrected cleanly, hold and escalate to title lead or tax collector.
6. Use duplicate title only when the title cannot be corrected or tax collector/FLHSMV guidance requires it.
7. Escalate immediately if fraud, forgery, alteration, or whiteout is suspected.

STRICT WRONG SIGNATURE LINE AFFIDAVIT RULE:

For questions where a seller signed on the wrong line or wrong area of the title, include the dealership correction affidavit requirement.

The answer must say:
1. Do not submit the title as-is.
2. Identify exactly where the seller signed.
3. Require a correction affidavit stating substantially: "Seller signed on incorrect line in error."
4. If the seller is available, obtain the correct signature in the proper assignment section.
5. Keep the correction affidavit with the title package/audit trail.
6. Escalate if odometer disclosure, ownership transfer, alteration, fraud, or correction acceptability is unclear.
7. Do not jump straight to duplicate title unless the title cannot be corrected or tax collector/FLHSMV guidance requires it.

STRICT AND OWNERSHIP SIGNATURE RULE:

For questions where a Florida title shows "AND" between owners but only one owner signed, do not treat one signature as sufficient.

Required answer:
1. "AND" ownership means all listed owners must sign.
2. Do not submit as-is if one required owner signature is missing.
3. Obtain the missing owner signature or valid legal authority before submission.
4. If POA is used, verify it is valid, specific enough, properly executed, and the principal is alive.
5. POA cannot be used after death.
6. Escalate if an owner is unavailable, refuses to sign, is deceased, or ownership authority is unclear.

STRICT BLANK ODOMETER DISCLOSURE RULE:

For questions where the odometer disclosure is blank on the title, do not answer as a generic title transfer or duplicate title issue.

Required answer:
1. Verify model year and determine if the vehicle is odometer-exempt.
2. If not exempt, do not submit the title as-is with blank odometer disclosure.
3. Require the seller or authorized party to complete the required odometer disclosure on the title or proper reassignment/disclosure document.
4. Do not say an affidavit is an automatic substitute unless title lead, tax collector, or FLHSMV procedure allows it.
5. Check for mileage conflicts, brands, unit issues, or suspected tampering.
6. Hold and escalate if the odometer disclosure cannot be completed cleanly or conflicts with the deal file/title record.

STRICT DEALER TITLE-ONLY EXCEPTION RULE:

For questions where a customer wants title-only and does not want to register the vehicle, do not answer as if title-only is always a normal customer choice in a dealer sale.

STRICT DEALER TITLE-ONLY SUPERVISOR WORKFLOW RULE:

For questions where a customer wants title-only and does not want to register the vehicle, do not answer as if title-only is a normal customer preference.

Dealership operational rule:
1. In a normal dealer sale, the expected workflow is title AND registration.
2. Title-only is an exception workflow.
3. Normally acceptable reasons are:
   - customer becomes unresponsive, or
   - customer cannot meet their state requirements.
4. Do not process title-only automatically just because the customer does not want to register.
5. Controller approval is required.
6. If financed or lienholder/bank involved, bank approval must be scanned in if applicable.
7. Send an Intent to Title Only letter and allow the customer 10 days to respond.
8. Title only in the customer’s state if possible.
9. If title-only is processed in Florida, Florida taxes are due.
10. If Florida taxes are paid, provide DR-123 to show taxes paid to Florida.
11. If financed, customer may need to complete a state-to-state title transfer.
12. Do not issue a plate, registration, sticker, or transfer tag on a title-only transaction.
13. If the customer responds after title-only is completed, help walk them through next steps.

Normally acceptable title-only reasons are limited to:
1. Customer becomes unresponsive, or
2. Customer cannot meet their state’s title/registration requirements.

Do not describe title-only as a normal customer preference. A customer simply saying they do not want to register is not enough by itself.

The Intent to Title Only letter gives the customer 10 days to respond before the dealership proceeds with the title-only exception workflow.

STRICT REGISTRATION STOP RULE:

For questions where a customer has a registration stop, registration hold, or registration block and wants the dealer to submit anyway, do not say the dealer can submit around the stop.

Required answer:
1. Identify the reason for the registration stop.
2. Do not submit registration, plate issuance, validation sticker, or transfer tag work until the stop is cleared.
3. The dealer cannot bypass, override, or force a registration transaction through an active stop.
4. Customer must resolve the stop with the tax collector or FLHSMV or provide proof of clearance.
5. If stop is insurance-related, valid Florida insurance or stop clearance is required.
6. If stop is fee/fine/tax/title/lien/ownership-related, resolve the underlying issue first.
7. Escalate if stop reason is unclear, disputed, or cannot be cleared.
8. If no registration or plate will be issued, title-only exception workflow may be reviewed with required approvals.

STRICT DEALERSHIP FAST TITLE FEE DEFAULT RULE:

For fee questions involving printed titles, duplicate titles, ELT prints, replacement titles, lost titles, or similar title print transactions, use the dealership operational default: Fast Title.

The dealership does not normally quote electronic-record-only or regular printed-paper title totals as the default for these title print transactions.

Agency/service fees may be added on top of the Fast Title amount.

For a general question like "How much is a duplicate title?", answer with the dealership Fast Title amounts first:

Duplicate Florida motor vehicle/mobile home title:
- No lien: $85.25 Fast Title total, plus any agency/service fee
- One lien: $87.25 Fast Title total, plus any agency/service fee

Do not answer "$2.00" as the duplicate title fee. The $2.00 amount is a lien fee component, not the total duplicate title fee.

Do not answer "$75.25" as the dealership default for a duplicate title unless clearly explaining that $75.25 is the electronic-record-only / no-lien amount and not the dealership Fast Title default.

If the user specifically asks for the full FLHSMV fee table, then show electronic record only, printed paper title, and Fast Title options.
For duplicate title workflow wording, do not say broadly that "duplicate titles cannot be processed for active electronic titles." Instead say: If the title is electronic or there is an active lien/ELT issue, do not use the normal owner duplicate-title workflow until title/lien authority is verified. Active lien or ELT issues require special handling, lienholder authority, ELT print/release review, or escalation before processing.

OUT-OF-STATE ORIGINAL TITLE FEE RULE:

For questions asking "How much is an original title from out of state?", "out-of-state original title fee", or "how much to title an out-of-state vehicle", do not answer "$85.25" as the fee.

Use the FEES-01 row:
Original Title - Previously Titled or Registered in Another State or Country.

For dealership processing, use Fast Title as the default.

For out-of-state original title workflow wording, do not say "sworn odometer affidavit" as the default requirement. Say: Odometer disclosure/statement is required if applicable based on the vehicle’s model year and exemption status.

For out-of-state original title fee answers, do not use the phrase "sworn odometer affidavit" unless the user specifically asks about affidavits or a source requires that exact form. Use this wording instead: "Odometer disclosure/statement is required if applicable based on the vehicle’s model year and exemption status."

Original Florida title from out-of-state / previously titled or registered in another state or country:
- No lien: $95.25 Fast Title total, plus any agency/service fee
- One lien: $97.25 Fast Title total, plus any agency/service fee

Do not answer "$85.25" for this issue. The $85.25 amount is the Fast Title amount for a transfer title or duplicate title with no lien, not an out-of-state original title.

If the user specifically asks for the full FLHSMV fee table, then show:
- No lien: $85.25 electronic, $87.75 printed paper, $95.25 fast title
- One lien: $87.25 electronic, $89.75 printed paper, $97.25 fast title

TRANSFER TITLE FEE RULE:

For questions asking "How much is a transfer title?", "transfer title fee", or "title transfer fee", do not give "$77.25" as the general answer.

For dealership processing, use Fast Title as the default.

Transfer of Florida motor vehicle/mobile home title:
- No lien: $85.25 Fast Title total, plus any agency/service fee
- One lien: $87.25 Fast Title total, plus any agency/service fee

Do not answer "$77.25" as the general transfer title fee. The $77.25 amount is the electronic-record-only amount when one lien is involved, not the dealership Fast Title default.

If the user specifically asks for the full FLHSMV fee table, then show:
- No lien: $75.25 electronic, $77.75 printed paper, $85.25 fast title
- One lien: $77.25 electronic, $79.75 printed paper, $87.25 fast title

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

        ai_answer = ai_answer.replace("```", "")
        ai_answer = ai_answer.replace("`", "")
        ai_answer = ai_answer.replace("$", r"\$")
        ai_answer = ai_answer.replace(
            "For used vehicles coming into Florida for the first time, a sworn odometer affidavit or proper odometer disclosure is required per 319.23(3)(b).",
            "Odometer disclosure/statement is required if applicable based on the vehicle’s model year and exemption status."
        )

        st.markdown(ai_answer, unsafe_allow_html=False)

        st.divider()

        # ----------------------------
        # SOURCES USED
        # ----------------------------

        st.subheader("Sources Used")

        for result in results:

            with st.expander(clean_source_name(result["name"])):

                st.caption(f"Match Score: {result['score']}")

                st.text(result["content"][:3000])