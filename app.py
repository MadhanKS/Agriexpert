"""
Farmster — AI-Powered Crop Diagnostic Platform
===================================================
Standalone, multi-tenant, crop-agnostic diagnostic platform.
Any farmer submits a photo → AI pre-diagnoses → Scientist reviews → Farmer gets recommendation.

Architecture:
  - Streamlit multipage app (pages/ folder)
  - Google Sheets backend (6 worksheets)
  - Claude Vision API for AI diagnosis
  - Zero dependency on any farm-specific app

Sheets required (one Google Spreadsheet):
  Farms | Farmers | Scientists | Plant_Reports | Crop_Types | App_Config
"""

import streamlit as st

st.set_page_config(
    page_title="Farmster",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'DM Sans', 'Noto Sans Devanagari', sans-serif;
    background: #0d1f0f;
    color: #e8f5e9;
    -webkit-tap-highlight-color: transparent;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 0 !important;
    max-width: 480px !important;
    margin: 0 auto !important;
}

/* ── Hero ── */
.fd-hero {
    background: linear-gradient(160deg, #0a1a0c 0%, #1b4020 50%, #0d2e10 100%);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.fd-hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 30% 20%, rgba(76,175,80,0.15) 0%, transparent 60%),
                radial-gradient(ellipse at 70% 80%, rgba(27,94,32,0.2) 0%, transparent 50%);
}
.fd-logo {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -1px;
    line-height: 1;
    position: relative;
    z-index: 1;
}
.fd-logo span { color: #69f0ae; }
.fd-tagline {
    font-size: 1rem;
    color: #a5d6a7;
    margin-top: 0.5rem;
    position: relative;
    z-index: 1;
    font-weight: 300;
}
.fd-hi {
    font-family: 'Noto Sans Devanagari', sans-serif;
    font-size: 0.85rem;
    color: #4caf50;
    margin-top: 0.25rem;
    position: relative;
    z-index: 1;
}

/* ── Role cards ── */
.role-grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
    max-width: 340px;
    margin: 2.5rem auto 0;
    position: relative;
    z-index: 1;
}
.role-card {
    background: rgba(255,255,255,0.05);
    border: 1.5px solid rgba(105,240,174,0.2);
    border-radius: 20px;
    padding: 1.25rem 1.5rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    display: flex;
    align-items: center;
    gap: 1rem;
    backdrop-filter: blur(10px);
}
.role-card:hover {
    background: rgba(105,240,174,0.1);
    border-color: rgba(105,240,174,0.5);
    transform: translateY(-2px);
}
.role-icon {
    font-size: 2rem;
    flex-shrink: 0;
}
.role-en {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #fff;
}
.role-sub {
    font-size: 0.78rem;
    color: #81c784;
    margin-top: 2px;
}
.role-hi {
    font-family: 'Noto Sans Devanagari', sans-serif;
    font-size: 0.72rem;
    color: #4caf50;
    margin-top: 1px;
}
.role-arrow {
    margin-left: auto;
    color: #69f0ae;
    font-size: 1.2rem;
    flex-shrink: 0;
}

/* ── Inner pages ── */
.fd-page {
    background: #f0f7ee;
    min-height: 100vh;
    padding-bottom: 2rem;
}
.fd-header {
    background: linear-gradient(135deg, #1b5e20, #2e7d32);
    padding: 1rem 1.2rem 1.3rem;
    border-radius: 0 0 20px 20px;
    margin-bottom: 1.2rem;
    box-shadow: 0 6px 24px rgba(27,94,32,0.3);
}
.fd-header-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: #fff;
}
.fd-header-sub {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.75);
    margin-top: 2px;
}
.fd-header-back {
    font-size: 0.75rem;
    color: #a5d6a7;
    margin-bottom: 0.3rem;
    cursor: pointer;
}

/* ── Cards ── */
.fd-card {
    background: #fff;
    border-radius: 16px;
    padding: 1rem 1.1rem;
    margin: 0 0.75rem 0.7rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
}
.fd-card-green { border-left: 5px solid #43a047; }
.fd-card-amber { border-left: 5px solid #fbc02d; }
.fd-card-red   { border-left: 5px solid #c62828; }
.fd-card-blue  { border-left: 5px solid #1565c0; }

/* ── Status pill ── */
.status-pill {
    display: inline-block;
    border-radius: 12px;
    padding: 3px 10px;
    font-size: 0.68rem;
    font-weight: 700;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 14px !important;
    min-height: 52px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    font-family: 'DM Sans', sans-serif !important;
    border: none !important;
    width: 100% !important;
    transition: all 0.15s !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1b5e20, #2e7d32) !important;
    color: white !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(27,94,32,0.08) !important;
    color: #1b5e20 !important;
    border: 1.5px solid #a5d6a7 !important;
}

/* ── Form inputs ── */
.stTextInput label, .stTextArea label, .stSelectbox label,
.stRadio label, .stNumberInput label, .stDateInput label {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #1b5e20 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #fff;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin: 0 0.75rem 0.8rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1b5e20, #2e7d32) !important;
    color: white !important;
}

/* ── Metric ── */
.fd-metric {
    background: #fff;
    border-radius: 14px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border-top: 4px solid #43a047;
}
.fd-metric-val { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800; color: #1b5e20; }
.fd-metric-label { font-size: 0.72rem; color: #9e9e9e; margin-top: 2px; font-weight: 600; }

/* ── Report card ── */
.report-card {
    background: #fff;
    border-radius: 14px;
    margin: 0 0.75rem 0.6rem;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    border: 1.5px solid #e8f5e9;
}
.report-header {
    padding: 0.7rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #f5f5f5;
}
.report-body { padding: 0.7rem 1rem; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #a5d6a7; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────
for k, v in {
    "role":        None,    # "farmer" | "scientist" | "admin"
    "farmer_id":   None,
    "farmer_name": None,
    "farm_id":     None,
    "sci_id":      None,
    "sci_name":    None,
    "page":        "home",  # "home" | "farmer_register" | ...
    "last_report": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Landing page ───────────────────────────────────────────────────────────
if st.session_state.role is None:
    st.markdown("""
    <div class="fd-hero">
        <div class="fd-logo">Farm<span>Diagnose</span></div>
        <div class="fd-tagline">AI-Powered Crop Diagnostic Platform</div>
        <div class="fd-hi">कृषि स्वास्थ्य — AI से जाँच</div>
        <div class="role-grid">
            <div class="role-card" id="farmer-card">
                <div class="role-icon">👨‍🌾</div>
                <div>
                    <div class="role-en">I am a Farmer</div>
                    <div class="role-sub">Submit plant photos, get expert advice</div>
                    <div class="role-hi">किसान हूँ — पौधा जाँचवाना है</div>
                </div>
                <div class="role-arrow">›</div>
            </div>
            <div class="role-card" id="scientist-card">
                <div class="role-icon">👨‍🔬</div>
                <div>
                    <div class="role-en">I am a Scientist</div>
                    <div class="role-sub">Review reports, give recommendations</div>
                    <div class="role-hi">वैज्ञानिक हूँ — किसानों की मदद करनी है</div>
                </div>
                <div class="role-arrow">›</div>
            </div>
            <div class="role-card" id="admin-card">
                <div class="role-icon">⚙️</div>
                <div>
                    <div class="role-en">Admin</div>
                    <div class="role-sub">Manage platform, farms, and users</div>
                    <div class="role-hi">व्यवस्थापक</div>
                </div>
                <div class="role-arrow">›</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("👨‍🌾 Farmer", key="go_farmer", type="primary"):
            st.session_state.role = "farmer"
            st.rerun()
    with c2:
        if st.button("👨‍🔬 Scientist", key="go_scientist"):
            st.session_state.role = "scientist"
            st.rerun()
    with c3:
        if st.button("⚙️ Admin", key="go_admin"):
            st.session_state.role = "admin"
            st.rerun()

elif st.session_state.role == "farmer":
    from pages.farmer import show_farmer
    show_farmer()

elif st.session_state.role == "scientist":
    from pages.scientist import show_scientist
    show_scientist()

elif st.session_state.role == "admin":
    from pages.admin import show_admin
