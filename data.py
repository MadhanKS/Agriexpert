"""
Farmster — Shared Data Layer
All Google Sheets read/write operations, KB, and utilities
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import base64
import hashlib
import uuid

# ── Connection ────────────────────────────────────────────────────────────
from streamlit_gsheets import GSheetsConnection
conn = st.connection("gsheets", type=GSheetsConnection)
SHEET_URL = st.secrets["gsheets"]["spreadsheet"]

CROP_TYPES_DEFAULT = [
    "Cardamom", "Black Pepper", "Coffee", "Tea",
    "Ginger", "Turmeric", "Vanilla", "Arecanut", "Other"
]

SEV_COLORS = {
    "Critical": "#c62828", "High": "#e65100",
    "Medium":   "#fbc02d", "Low":  "#2e7d32", "None": "#2e7d32"
}
SEV_ICONS = {
    "Critical":"🔴","High":"🟠","Medium":"🟡","Low":"🟢","None":"🟢"
}
STATUS_COLORS = {
    "Pending":      "#e65100",
    "Under Review": "#fbc02d",
    "Responded":    "#2e7d32",
    "Closed":       "#1565c0",
}

# ── Safe write wrapper ────────────────────────────────────────────────────
def safe_update(worksheet, data, retries=3):
    import time
    import gspread
    for attempt in range(retries):
        try:
            conn.update(spreadsheet=SHEET_URL, worksheet=worksheet, data=data)
            return True, ""
        except gspread.exceptions.APIError as e:
            msg = str(e)
            if attempt < retries - 1:
                time.sleep(2 ** attempt * 2)
            else:
                if "403" in msg: return False, "Permission denied — check service account access."
                if "429" in msg: return False, "API quota exceeded — wait 1 minute and retry."
                return False, msg[:200]
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return False, str(e)[:200]
    return False, "Failed after retries."

def clean(val, fallback="—"):
    if val is None: return fallback
    try:
        if pd.isna(val): return fallback
    except: pass
    s = str(val).strip()
    return s if s else fallback

def gen_id(prefix, seed=""):
    raw = f"{prefix}{seed}{datetime.now().isoformat()}"
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
            "Farmer_ID","Name","Phone","Farm_ID","Language","Registered_At"
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
            "Crops","Institution","Phone","PIN","Is_Active","Registered_At"
        ])

@st.cache_data(ttl=30)
def load_reports():
    try:
        df = conn.read(spreadsheet=SHEET_URL, worksheet="Plant_Reports", ttl=30)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=[
            "Report_ID","Submitted_At","Farmer_ID","Farmer_Name","Farm_ID",
            "Farm_Name","Crop_Type","Plant_Part","Symptoms","AI_Condition",
            "AI_Severity","AI_Confidence","AI_Findings","AI_Treatment",
            "AI_Spread_Risk","AI_Expert_Note","Status","Assigned_To",
            "Sci_Confirmed","Sci_Recommendations","Sci_Medicines",
            "Sci_Follow_Up","Sci_Next_Visit","Reviewed_At","Reviewed_By"
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

# ── Cardamom Knowledge Base (inline) ─────────────────────────────────────
CROP_KB = {
    "Cardamom": {
        "diseases": {
            "Azhukal / Capsule Rot": {
                "causal": "Phytophthora meadii, P. nicotianae",
                "season": "SW monsoon June–Sep; peak 320–400mm rainfall",
                "symptoms": [
                    "Water-soaked lesions on capsules or leaves",
                    "Capsules turn brownish, decay, drop with foul smell",
                    "Shredded leaf appearance; immature leaves fail to unfurl",
                ],
                "management": [
                    "Bordeaux mixture 1% — preventive spray before June",
                    "Metalaxyl (Ridomil) 0.25% — highly effective",
                    "Copper oxychloride 0.25% — foliar or drench",
                    "Improve drainage; reduce shade; remove infected material",
                ],
                "urgency": "High",
            },
            "Katte / Cardamom Mosaic Virus": {
                "causal": "Cardamom Mosaic Virus — aphid vector Pentalonia nigronervosa",
                "season": "Year-round; aphid peak Nov–May",
                "symptoms": [
                    "Mosaic chlorotic mottling on leaves",
                    "Light and dark green alternating patches",
                    "Severe stunting; progressive plant death",
                ],
                "management": [
                    "NO chemical cure — ROGUE infected plant IMMEDIATELY",
                    "Control aphid vector with systemic insecticides",
                    "Plant only certified disease-free planting material",
                    "400m buffer from known infected areas",
                ],
                "urgency": "Critical",
            },
            "Rhizome Rot / Clump Rot": {
                "causal": "Pythium vexans, Rhizoctonia solani",
                "season": "SW monsoon July–August",
                "symptoms": [
                    "Collar region of shoots turns soft, brown, brittle",
                    "Tillers fall off at base with foul smell",
                    "Pale yellow foliage, premature leaf death",
                ],
                "management": [
                    "Copper oxychloride 0.25% soil drench",
                    "Bordeaux mixture 1% soil drench",
                    "Trichoderma harzianum — biocontrol in FYM",
                    "Remove crowding; ensure drainage",
                ],
                "urgency": "High",
            },
            "Chenthal / Leaf Blight": {
                "causal": "Colletotrichum gloeosporioides",
                "season": "Post-monsoon; severe in summer",
                "symptoms": [
                    "Yellowish-brown to orange-red elongate streaks on leaves",
                    "Two youngest leaves NOT affected",
                    "Burnt appearance in severe cases",
                ],
                "management": [
                    "Carbendazim 0.3% — 3 sprays at monthly intervals",
                    "Mancozeb 0.3% — 3 sprays at monthly intervals",
                ],
                "urgency": "Medium",
            },
        },
        "seasonal": {
            1:  "Harvest late rounds; Chenthal HIGH; Nematode HIGH",
            2:  "Last harvest; soil conservation work",
            3:  "Pre-monsoon irrigation; shade regulation; weeding",
            4:  "Fertilizer application (NPK); aphid peak — Katte vector",
            5:  "Preventive Azhukal spray CRITICAL; pre-monsoon prep",
            6:  "SW monsoon — Azhukal sprays ongoing; drain management",
            7:  "Peak monsoon — Azhukal CRITICAL; Rhizome Rot CRITICAL",
            8:  "Harvest begins; monitor Azhukal on capsules",
            9:  "Harvest; NE monsoon; nematode build-up",
            10: "Harvest peak; Phytophthora Leaf Blight onset; Chenthal onset",
            11: "Harvest peak; shade regulation; Chenthal HIGH",
            12: "Late harvest; weeding; soil work; Chenthal ongoing",
        },
    },
    "Black Pepper": {
        "diseases": {
            "Phytophthora Foot Rot": {
                "causal": "Phytophthora capsici",
                "season": "Monsoon June–September",
                "symptoms": [
                    "Wilting of leaves starting from top",
                    "Black lesions at collar region / roots",
                    "Defoliation; plant death within weeks",
                ],
                "management": [
                    "Bordeaux mixture 1% soil drench",
                    "Metalaxyl + Mancozeb (Ridomil Gold) spray",
                    "Improve drainage urgently",
                ],
                "urgency": "Critical",
            },
            "Pollu Beetle": {
                "causal": "Longitarsus nigripennis (insect pest)",
                "season": "June–November",
                "symptoms": [
                    "Shot-hole appearance on berries",
                    "Premature berry drop; affected berries are hollow",
                ],
                "management": [
                    "Carbaryl 0.1% spray on spikes",
                    "Repeat at 2-week intervals during monsoon",
                ],
                "urgency": "High",
            },
        },
        "seasonal": {
            k: "General monitoring" for k in range(1, 13)
        }
    },
}

def get_kb_for_crop(crop_type):
    return CROP_KB.get(crop_type, {})

def get_seasonal_risk(crop_type, month):
    kb = get_kb_for_crop(crop_type)
    return kb.get("seasonal", {}).get(month, "Standard monitoring")

def get_disease_list(crop_type):
    kb = get_kb_for_crop(crop_type)
    return list(kb.get("diseases", {}).keys())

# ── AI Diagnosis ──────────────────────────────────────────────────────────
def build_system_prompt(crop_type, farm_name, farmer_name, month):
    kb    = get_kb_for_crop(crop_type)
    dis   = kb.get("diseases", {})
    risk  = get_seasonal_risk(crop_type, month)

    disease_ctx = "\n".join([
        f"- {n}: Causal: {v.get('causal','')}. "
        f"Symptoms: {'; '.join(v.get('symptoms',[])[:2])}. "
        f"Urgency: {v.get('urgency','Medium')}."
        for n, v in dis.items()
    ])

    return (
        f"You are an expert plant pathologist specializing in {crop_type} cultivation. "
        f"Farm: {farm_name}. Farmer: {farmer_name}. Month: {month}.\n"
        f"Current seasonal disease risk: {risk}\n\n"
        f"Known diseases for {crop_type}:\n{disease_ctx}\n\n"
        "Analyze the image. Respond EXACTLY in this format:\n"
        "CONDITION: [name or Healthy or Inconclusive]\n"
        "CONFIDENCE: [High/Medium/Low]\n"
        "TYPE: [Fungal/Viral/Bacterial/Pest/Nutrient/Healthy/Inconclusive]\n"
        "SEVERITY: [Critical/High/Medium/Low/None]\n"
        "OBSERVED:\n[2-3 sentences describing visible symptoms]\n"
        "CAUSE:\n[specific disease/pest and why]\n"
        "ACTION:\n[most urgent step in next 24-48 hours]\n"
        "TREATMENT:\n[specific chemicals/biologicals, dosage, method]\n"
        "SPREAD:\n[contagion risk and speed]\n"
        "SCIENTIST_NOTE:\n[what expert should verify/investigate]"
    )

def parse_diagnosis(raw):
    def ef(field):
        for l in raw.split('\n'):
            if l.startswith(field + ':'):
                return l.split(':', 1)[1].strip()
        return ""

    def eb(field):
        FIELDS = ['CONDITION','CONFIDENCE','TYPE','SEVERITY',
                  'OBSERVED','CAUSE','ACTION','TREATMENT','SPREAD','SCIENTIST_NOTE']
        lines   = raw.split('\n')
        cap, res = False, []
        for l in lines:
            if l.startswith(field + ':'):
                cap = True
                after = l.split(':', 1)[1].strip()
                if after: res.append(after)
                continue
            if cap:
                if any(l.startswith(f + ':') for f in FIELDS): break
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

def run_diagnosis(image_bytes, media_type, crop_type, farm_name,
                  farmer_name, plant_part, notes, month):
    import anthropic
    api_key = st.secrets.get("anthropic", {}).get("api_key", "")
    client  = anthropic.Anthropic(api_key=api_key)

    system  = build_system_prompt(crop_type, farm_name, farmer_name, month)
    img_b64 = base64.b64encode(image_bytes).decode("utf-8")

    resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1200,
        system=system,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image",
                 "source": {"type": "base64",
                            "media_type": media_type,
                            "data": img_b64}},
                {"type": "text",
                 "text": (f"Crop: {crop_type}. Plant part: {plant_part or 'not specified'}. "
                          f"Farmer notes: {notes or 'none'}.")}
            ]
        }]
    )
    return parse_diagnosis(resp.content[0].text)
