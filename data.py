"""AgriExpert — Data Layer + Credit System + Knowledge Base"""

import streamlit as st
import pandas as pd
from datetime import datetime
import base64, hashlib, uuid, json, time
from streamlit_gsheets import GSheetsConnection
import gspread
from google.oauth2.service_account import Credentials

conn      = st.connection("gsheets", type=GSheetsConnection)
SHEET_URL = st.secrets["gsheets"]["spreadsheet"]

# ── Direct gspread client for reliable writes ─────────────────────────────
@st.cache_resource
def get_gspread_client():
    """
    Build a gspread client directly from secrets.
    st-gsheets-connection handles reads fine but writes need this for reliability.
    """
    creds_dict = {
        "type":                        st.secrets["gsheets"]["type"],
        "project_id":                  st.secrets["gsheets"]["project_id"],
        "private_key_id":              st.secrets["gsheets"]["private_key_id"],
        "private_key":                 st.secrets["gsheets"]["private_key"],
        "client_email":                st.secrets["gsheets"]["client_email"],
        "client_id":                   st.secrets["gsheets"]["client_id"],
        "auth_uri":                    st.secrets["gsheets"].get("auth_uri","https://accounts.google.com/o/oauth2/auth"),
        "token_uri":                   st.secrets["gsheets"].get("token_uri","https://oauth2.googleapis.com/token"),
        "auth_provider_x509_cert_url": st.secrets["gsheets"].get("auth_provider_x509_cert_url","https://www.googleapis.com/oauth2/v1/certs"),
        "client_x509_cert_url":        st.secrets["gsheets"].get("client_x509_cert_url",""),
        "universe_domain":             st.secrets["gsheets"].get("universe_domain","googleapis.com"),
    }
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds  = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return gspread.authorize(creds)

# ── Credit pricing ────────────────────────────────────────────────────────
CREDIT_PRICE_INR  = 99          # ₹99 per diagnostic credit
FREE_CREDITS      = 3           # credits given on signup
CREDITS_PER_QUERY = 1           # cost per diagnosis submission

CROP_TYPES_DEFAULT = [
    "Cardamom", "Black Pepper", "Coffee", "Tea",
    "Ginger", "Turmeric", "Vanilla", "Arecanut", "Other"
]

# Idukki District — Villages & Towns
# Source: Kerala local body directory — Idukki district
IDUKKI_VILLAGES = [
    # Devikulam Taluk
    "Munnar", "Devikulam", "Rajamala", "Marayoor", "Kanthalloor",
    "Anachal", "Pallivasal", "Vattavada", "Chinnakkanal", "Udumbanchola",
    "Pampadum Shola", "Mankulam", "Chinnakanal",
    # Idukki Taluk
    "Idukki", "Cheruthoni", "Thankamany", "Kattappana", "Kumily",
    "Vandiperiyar", "Upputhara", "Senapathy", "Murikkady", "Gandhinagar",
    "Elappara", "Moolamattom", "Nedumkandam", "Karimannoor",
    "Adimali", "Peermade", "Anakara",
    # Thodupuzha Taluk
    "Thodupuzha", "Kumaramangalam", "Kaliyar", "Vazhathoppu",
    "Pala", "Arakkulam", "Irattayar", "Vazhikadavu", "Manakkad",
    "Karimkunnam", "Nellimala", "Koovappally",
    # Udumbanchola Taluk
    "Azhutha", "Kuthumkal", "Pampadumpara", "Santhanpara",
    "Keezhillam", "Puliyanmala",
    # Peerumade Taluk
    "Peerumedu", "Painavu", "Thrikkovilvattom", "Vazhavara",
    "Mariyapuram", "Kallar", "Vagamon",
    # Other / Mixed
    "Iyyappancoil", "Kanjikuzhy", "Vaikom", "Other",
]
IDUKKI_VILLAGES = sorted(list(set(IDUKKI_VILLAGES)))

SEV_LEVELS  = ["Critical", "High", "Medium", "Low", "None"]
BADGE_CLASS = {
    "Critical":"critical","High":"high","Medium":"medium","Low":"low","None":"low"
}
STATUS_BADGE = {
    "Pending":"pending","Under Review":"review",
    "Responded":"done","Closed":"done"
}

# ── Utilities ─────────────────────────────────────────────────────────────
def safe_update(worksheet_name, data, retries=3):
    """
    Write a DataFrame to a Google Sheet worksheet using gspread directly.
    Replaces the full sheet content (header + all rows).
    """
    for attempt in range(retries):
        try:
            gc  = get_gspread_client()
            # Extract sheet ID from URL — works regardless of URL format
            import re as _re
            _match = _re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', SHEET_URL)
            if not _match:
                return False, "Invalid spreadsheet URL in secrets."
            sheet_id    = _match.group(1)
            spreadsheet = gc.open_by_key(sheet_id)
            ws          = spreadsheet.worksheet(worksheet_name)

            # Convert DataFrame to list of lists (header + rows)
            df = data.copy()

            # Replace NaN/None with empty string for Sheets
            df = df.fillna("").astype(str)

            values = [df.columns.tolist()] + df.values.tolist()
            ws.clear()
            ws.update(values, value_input_option="RAW")
            return True, ""

        except gspread.exceptions.APIError as e:
            msg = str(e)
            if attempt < retries - 1:
                time.sleep(2 ** attempt * 2)
                continue
            if "403" in msg or "PERMISSION_DENIED" in msg:
                return False, "Permission denied — check service account has Editor access."
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                return False, "API quota exceeded. Wait 1 minute and retry."
            return False, f"Sheets API error: {msg[:200]}"
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            return False, f"Error: {str(e)[:200]}"
    return False, "Failed after all retries."

def clean(val, fallback="—"):
    if val is None: return fallback
    try:
        if pd.isna(val): return fallback
    except: pass
    s = str(val).strip()
    return s if s else fallback

def gen_id(prefix, seed=""):
    raw = f"{prefix}{seed}{datetime.now().isoformat()}{uuid.uuid4()}"
    return prefix + "-" + hashlib.md5(raw.encode()).hexdigest()[:8].upper()

# ── Loaders ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=600)
def load_farms():
    try:
        df = conn.read(spreadsheet=SHEET_URL, worksheet="Farms", ttl=600)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=[
            "Farm_ID","Farm_Name","Location","District","State",
            "Crop_Type","Acreage","Owner_Name","Phone","Registered_At"
        ])

@st.cache_data(ttl=300)
def load_farmers():
    try:
        df = conn.read(spreadsheet=SHEET_URL, worksheet="Farmers", ttl=300)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=[
            "Farmer_ID","Name","Phone","Farm_ID","Farm_Name",
            "Language","Credits","Registered_At"
        ])

@st.cache_data(ttl=300)
def load_scientists():
    try:
        df = conn.read(spreadsheet=SHEET_URL, worksheet="Scientists", ttl=300)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=[
            "Sci_ID","Name","Qualification","Specialization",
            "Crops","Institution","Phone","PIN","Is_Active",
            "Reports_Reviewed","Registered_At"
        ])

@st.cache_data(ttl=30)
def load_reports():
    try:
        df = conn.read(spreadsheet=SHEET_URL, worksheet="Plant_Reports", ttl=30)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=[
            "Report_ID","Submitted_At","Farmer_ID","Farmer_Name",
            "Farm_ID","Farm_Name","Crop_Type","Plant_Part","Symptoms",
            "AI_Condition","AI_Severity","AI_Confidence","AI_Findings",
            "AI_Treatment","AI_Spread_Risk","AI_Expert_Note","Status",
            "Sci_Confirmed","Sci_Recommendations","Sci_Medicines",
            "Sci_Follow_Up","Sci_Next_Visit","Reviewed_At","Reviewed_By",
            "Credits_Charged"
        ])

@st.cache_data(ttl=60)
def load_transactions():
    try:
        df = conn.read(spreadsheet=SHEET_URL, worksheet="Credit_Transactions", ttl=60)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=[
            "Txn_ID","Timestamp","Farmer_ID","Farmer_Name",
            "Type","Credits","Amount_INR","Notes","Report_ID"
        ])

@st.cache_data(ttl=3600)
def load_crop_types():
    try:
        df = conn.read(spreadsheet=SHEET_URL, worksheet="Crop_Types", ttl=3600)
        df.columns = df.columns.str.strip()
        if not df.empty and "Crop_Name" in df.columns:
            return df["Crop_Name"].dropna().tolist()
    except: pass
    return CROP_TYPES_DEFAULT

# ── Credit operations ──────────────────────────────────────────────────────
def get_farmer_credits(farmer_id):
    farmers_df = load_farmers()
    if farmers_df.empty: return 0
    row = farmers_df[farmers_df["Farmer_ID"] == farmer_id]
    if row.empty: return 0
    try:
        return int(float(clean(row.iloc[0].get("Credits"), "0")))
    except:
        return 0

def deduct_credit(farmer_id, farmer_name, report_id):
    """Deduct 1 credit for a diagnosis. Returns (success, new_balance)."""
    farmers_df = load_farmers()
    if farmers_df.empty: return False, 0

    mask = farmers_df["Farmer_ID"] == farmer_id
    if not mask.any(): return False, 0

    current = 0
    try:
        current = int(float(clean(farmers_df.loc[mask, "Credits"].values[0], "0")))
    except: pass

    if current <= 0:
        return False, 0

    # Deduct
    farmers_df.loc[mask, "Credits"] = current - 1
    ok, err = safe_update("Farmers", farmers_df)
    if not ok: return False, current

    # Log transaction
    txn = pd.DataFrame([{
        "Txn_ID":      gen_id("TXN", farmer_id),
        "Timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Farmer_ID":   farmer_id,
        "Farmer_Name": farmer_name,
        "Type":        "Debit",
        "Credits":     -1,
        "Amount_INR":  0,   # 0 during free phase
        "Notes":       f"Diagnosis submitted — {report_id}",
        "Report_ID":   report_id,
    }])
    existing_txns = load_transactions()
    safe_update("Credit_Transactions",
                pd.concat([existing_txns, txn], ignore_index=True))

    st.cache_data.clear()
    return True, current - 1

def add_credits(farmer_id, farmer_name, credits, amount_inr, notes="Top-up"):
    """Add credits to a farmer account."""
    farmers_df = load_farmers()
    if farmers_df.empty: return False

    mask = farmers_df["Farmer_ID"] == farmer_id
    if not mask.any(): return False

    current = 0
    try:
        current = int(float(clean(farmers_df.loc[mask, "Credits"].values[0], "0")))
    except: pass

    farmers_df.loc[mask, "Credits"] = current + credits
    ok, _ = safe_update("Farmers", farmers_df)
    if not ok: return False

    txn = pd.DataFrame([{
        "Txn_ID":      gen_id("TXN", farmer_id),
        "Timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Farmer_ID":   farmer_id,
        "Farmer_Name": farmer_name,
        "Type":        "Credit",
        "Credits":     credits,
        "Amount_INR":  amount_inr,
        "Notes":       notes,
        "Report_ID":   "",
    }])
    existing = load_transactions()
    safe_update("Credit_Transactions",
                pd.concat([existing, txn], ignore_index=True))

    st.cache_data.clear()
    return True

# ── Knowledge Base ─────────────────────────────────────────────────────────
CROP_KB = {
    "Cardamom": {
        "diseases": {
            "Azhukal / Capsule Rot": {
                "causal":  "Phytophthora meadii, P. nicotianae",
                "season":  "SW monsoon June–Sep; peak at 320–400mm rainfall",
                "symptoms": [
                    "Water-soaked discoloured lesions on capsules or leaves",
                    "Capsules turn brownish, decay and drop with foul odour",
                    "Shredded leaf appearance; immature leaves fail to unfurl",
                    "Severe cases: entire panicle or pseudostem decays",
                ],
                "management": [
                    "Bordeaux mixture 1% — preventive spray before June onset",
                    "Metalaxyl (Ridomil) 0.25% — highly effective against Phytophthora",
                    "Copper oxychloride 0.25% — foliar spray or soil drench",
                    "Improve drainage; reduce shade density; remove infected material",
                ],
                "urgency": "High",
            },
            "Katte / Cardamom Mosaic Virus": {
                "causal":  "Cardamom Mosaic Virus (poty virus); vector: Pentalonia nigronervosa",
                "season":  "Year-round; aphid vector peaks November–May",
                "symptoms": [
                    "Mosaic chlorotic mottling on leaves — light and dark patches",
                    "Severe stunting; gradual plant decline and death",
                ],
                "management": [
                    "No chemical cure — rogue and destroy infected plants immediately",
                    "Control aphid vector with systemic insecticides",
                    "Use only certified disease-free planting material",
                    "Maintain 400m buffer from known infected areas",
                ],
                "urgency": "Critical",
            },
            "Rhizome Rot": {
                "causal":  "Pythium vexans, Rhizoctonia solani",
                "season":  "Peak July–August; waterlogged soils",
                "symptoms": [
                    "Collar region becomes soft, brown and brittle",
                    "Tillers detach at base with foul odour",
                    "Pale yellow foliage; premature leaf death",
                ],
                "management": [
                    "Copper oxychloride 0.25% or Bordeaux 1% soil drench",
                    "Trichoderma harzianum biocontrol in FYM",
                    "Ensure drainage; reduce plant density",
                ],
                "urgency": "High",
            },
            "Chenthal / Leaf Blight": {
                "causal":  "Colletotrichum gloeosporioides",
                "season":  "Post-monsoon October–January",
                "symptoms": [
                    "Yellowish-brown to orange-red elongate streaks on foliage",
                    "Two youngest leaves unaffected",
                    "Burnt appearance in severe cases",
                ],
                "management": [
                    "Carbendazim (Bavistin) 0.3% — 3 monthly sprays",
                    "Mancozeb 0.3% — 3 monthly sprays",
                ],
                "urgency": "Medium",
            },
        },
        "seasonal": {
            1:  "Late harvest rounds; Chenthal high risk; nematode pressure",
            2:  "Last harvest; soil conservation; pruning",
            3:  "Pre-monsoon irrigation; shade regulation; weeding",
            4:  "NPK fertiliser application; aphid pressure rising (Katte vector)",
            5:  "Preventive Azhukal spray — critical before monsoon onset",
            6:  "SW monsoon — Azhukal sprays; drainage management",
            7:  "Peak monsoon — Azhukal critical; Rhizome Rot critical",
            8:  "Harvest season begins; monitor capsules for Azhukal",
            9:  "Harvest ongoing; post-monsoon fertiliser",
            10: "Harvest peak; Leaf Blight onset; Chenthal onset",
            11: "Harvest peak; shade regulation; Chenthal high",
            12: "Late harvest; weeding; soil work",
        },
    },
    "Black Pepper": {
        "diseases": {
            "Phytophthora Foot Rot": {
                "causal":  "Phytophthora capsici",
                "season":  "Monsoon June–September",
                "symptoms": [
                    "Wilting from top of vine downward",
                    "Black lesions at collar / root region",
                    "Rapid defoliation; plant death within weeks",
                ],
                "management": [
                    "Bordeaux mixture 1% soil drench immediately",
                    "Metalaxyl + Mancozeb (Ridomil Gold) spray",
                    "Improve drainage; remove infected vines",
                ],
                "urgency": "Critical",
            },
        },
        "seasonal": {k: "Standard monitoring" for k in range(1, 13)},
    },
}

def get_kb(crop_type):
    return CROP_KB.get(crop_type, {})

def seasonal_advisory(crop_type, month):
    return get_kb(crop_type).get("seasonal", {}).get(month, "Standard monitoring.")

def build_prompt(crop, farm, farmer, part, notes, month):
    kb  = get_kb(crop)
    dis = kb.get("diseases", {})
    disease_ctx = "\n".join([
        f"- {n}: {'; '.join(v.get('symptoms',[])[:2])}. "
        f"Urgency: {v.get('urgency')}. Mgmt: {'; '.join(v.get('management',[])[:2])}."
        for n, v in dis.items()
    ])
    risk = seasonal_advisory(crop, month)
    return (
        f"You are a senior plant pathologist specialising in {crop}. "
        f"Farm: {farm}. Grower: {farmer}. Current month risk: {risk}.\n\n"
        f"Known {crop} diseases:\n{disease_ctx}\n\n"
        "Analyze the submitted image. Respond EXACTLY in this format with no preamble:\n"
        "CONDITION: [disease name or Healthy or Inconclusive]\n"
        "CONFIDENCE: [High/Medium/Low]\n"
        "TYPE: [Fungal/Viral/Bacterial/Pest/Nutrient/Healthy/Inconclusive]\n"
        "SEVERITY: [Critical/High/Medium/Low/None]\n"
        "OBSERVED:\n[2-3 precise sentences describing visible symptoms]\n"
        "CAUSE:\n[specific pathogen or condition and reasoning]\n"
        "ACTION:\n[single most urgent step in next 24-48 hours]\n"
        "TREATMENT:\n[specific products, dosage, method, frequency]\n"
        "SPREAD:\n[contagion risk and rate of spread if left untreated]\n"
        "SCIENTIST_NOTE:\n[specific questions or areas for specialist to verify]"
    )

def parse_ai(raw):
    def ef(f):
        for l in raw.split('\n'):
            if l.startswith(f + ':'):
                return l.split(':', 1)[1].strip()
        return ""
    def eb(f):
        FIELDS = ['CONDITION','CONFIDENCE','TYPE','SEVERITY',
                  'OBSERVED','CAUSE','ACTION','TREATMENT','SPREAD','SCIENTIST_NOTE']
        lines, cap, res = raw.split('\n'), False, []
        for l in lines:
            if l.startswith(f + ':'):
                cap = True
                a = l.split(':', 1)[1].strip()
                if a: res.append(a)
                continue
            if cap:
                if any(l.startswith(x + ':') for x in FIELDS): break
                res.append(l)
        return ' '.join(res).strip()

    return {
        "condition":  ef('CONDITION'),
        "confidence": ef('CONFIDENCE'),
        "dtype":      ef('TYPE'),
        "severity":   ef('SEVERITY'),
        "observed":   eb('OBSERVED'),
        "cause":      eb('CAUSE'),
        "action":     eb('ACTION'),
        "treatment":  eb('TREATMENT'),
        "spread":     eb('SPREAD'),
        "sci_note":   eb('SCIENTIST_NOTE'),
    }

def run_ai_diagnosis(image_bytes, media_type, crop, farm,
                     farmer, part, notes, month):
    import anthropic
    api_key = st.secrets.get("anthropic", {}).get("api_key", "")
    client  = anthropic.Anthropic(api_key=api_key)
    img_b64 = base64.b64encode(image_bytes).decode("utf-8")
    resp    = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1200,
        system=build_prompt(crop, farm, farmer, part, notes, month),
        messages=[{
            "role": "user",
            "content": [
                {"type": "image",
                 "source": {"type": "base64",
                            "media_type": media_type, "data": img_b64}},
                {"type": "text",
                 "text": (f"Crop: {crop}. Part observed: {part or 'unspecified'}. "
                          f"Notes from grower: {notes or 'none'}.")}
            ]
        }]
    )
    return parse_ai(resp.content[0].text)


# ── UI Translations ──────────────────────────────────────────────────────
UI_TRANSLATIONS = {'Tamil': {'Farmer Portal': 'விவசாயி போர்டல்', 'Scientist Portal': 'விஞ்ஞானி போர்டல்', 'Administrator': 'நிர்வாகி', 'Submit plant photos': 'தாவர புகைப்படங்களை சமர்ப்பிக்கவும்', 'Track reports': 'அறிக்கைகளை கண்காணிக்கவும்', 'Get recommendations': 'பரிந்துரைகளை பெறவும்', 'Login': 'உள்நுழை', 'Register': 'பதிவு செய்க', 'Phone Number': 'தொலைபேசி எண்', 'Full Name': 'முழு பெயர்', 'Your Farm': 'உங்கள் பண்ணை', 'New Report': 'புதிய அறிக்கை', 'My Reports': 'என் அறிக்கைகள்', 'Credits': 'கிரெடிட்கள்', 'Submit for Analysis': 'பகுப்பாய்வுக்கு சமர்ப்பிக்கவும்', 'Pending Review': 'நிலுவையில் உள்ள மதிப்பாய்வு', 'Completed': 'முடிந்தது', 'Refresh': 'புதுப்பிக்கவும்', 'Back to Home': 'முகப்புக்கு திரும்பு', '3 FREE credits on signup': 'பதிவில் 3 இலவச கிரெடிட்கள்'}, 'Malayalam': {'Farmer Portal': 'കർഷക പോർട്ടൽ', 'Scientist Portal': 'ശാസ്ത്രജ്ഞ പോർട്ടൽ', 'Administrator': 'അഡ്മിനിസ്ട്രേറ്റർ', 'Submit plant photos': 'സസ്യ ഫോട്ടോകൾ സമർപ്പിക്കുക', 'Track reports': 'റിപ്പോർട്ടുകൾ ട്രാക്ക് ചെയ്യുക', 'Get recommendations': 'ശുപാർശകൾ നേടുക', 'Login': 'ലോഗിൻ', 'Register': 'രജിസ്റ്റർ ചെയ്യുക', 'Phone Number': 'ഫോൺ നമ്പർ', 'Full Name': 'പൂർണ്ണ നാമം', 'Your Farm': 'നിങ്ങളുടെ ഫാം', 'New Report': 'പുതിയ റിപ്പോർട്ട്', 'My Reports': 'എന്റെ റിപ്പോർട്ടുകൾ', 'Credits': 'ക്രെഡിറ്റുകൾ', 'Submit for Analysis': 'വിശകലനത്തിനായി സമർപ്പിക്കുക', 'Pending Review': 'അവലോകനം ബാക്കി', 'Completed': 'പൂർത്തിയായി', 'Refresh': 'പുതുക്കുക', 'Back to Home': 'ഹോമിലേക്ക് തിരിച്ചു', '3 FREE credits on signup': 'സൈൻ അപ്പിൽ 3 സൗജന്യ ക്രെഡിറ്റുകൾ'}}

def t(key, lang='English'):
    """Translate a UI key to the farmer's preferred language.
    Falls back to English if translation not found."""
    if lang == 'English' or not lang:
        return key
    return UI_TRANSLATIONS.get(lang, {}).get(key, key)
