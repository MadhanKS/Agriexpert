"""
AgriExpert — Crop Diagnostic Platform
Professional AI-powered plant health diagnostics connecting farmers with scientists.
"""

import streamlit as st

st.set_page_config(
    page_title="AgriExpert",
    page_icon="https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/leaflet.svg",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Noto+Sans+Tamil:wght@400;500;600&family=Noto+Sans+Malayalam:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin:0; padding:0; }

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #f7f8f5;
    color: #111;
    -webkit-tap-highlight-color: transparent;
    -webkit-font-smoothing: antialiased;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 0 !important;
    max-width: 430px !important;
    margin: 0 auto !important;
}

/* ═══════════════════════════════════════════
   LANDING PAGE
═══════════════════════════════════════════ */
.land-wrap {
    min-height: 100vh;
    background: #0a1f12;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
}
.land-wrap::before {
    content: '';
    position: absolute;
    width: 500px; height: 500px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(52,168,83,0.12) 0%, transparent 70%);
    top: -100px; right: -150px;
    pointer-events: none;
}
.land-wrap::after {
    content: '';
    position: absolute;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(52,168,83,0.07) 0%, transparent 70%);
    bottom: 100px; left: -80px;
    pointer-events: none;
}

.land-logo-bar {
    padding: 2rem 2rem 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.land-logo-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #34a853, #1a7a35);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}
.land-logo-text {
    font-size: 1.1rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.3px;
}
.land-logo-text span { color: #34a853; }

.land-hero {
    padding: 3rem 2rem 1.5rem;
    flex: 1;
    position: relative;
    z-index: 1;
}
.land-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(52,168,83,0.15);
    border: 1px solid rgba(52,168,83,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.7rem;
    font-weight: 600;
    color: #6fcf8d;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.land-h1 {
    font-size: 2.6rem;
    font-weight: 800;
    color: #fff;
    line-height: 1.1;
    letter-spacing: -1px;
    margin-bottom: 1rem;
}
.land-h1 em {
    font-style: normal;
    background: linear-gradient(135deg, #34a853, #6fcf8d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.land-sub {
    font-size: 0.88rem;
    color: #6a9a7a;
    line-height: 1.6;
    font-weight: 400;
    max-width: 300px;
}

.land-stats {
    display: flex;
    gap: 1rem;
    margin: 1.8rem 0 2rem;
}
.land-stat {
    flex: 1;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 0.8rem;
    text-align: center;
}
.land-stat-num {
    font-size: 1.4rem;
    font-weight: 800;
    color: #fff;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
}
.land-stat-label {
    font-size: 0.6rem;
    color: #5a8a6a;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 3px;
    font-weight: 600;
}

.land-cards {
    padding: 0 1.5rem 2.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    position: relative;
    z-index: 1;
}
.land-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    backdrop-filter: blur(10px);
    transition: border-color 0.2s, background 0.2s;
}
.land-card:hover {
    border-color: rgba(52,168,83,0.4);
    background: rgba(52,168,83,0.08);
}
.land-card-icon {
    width: 44px; height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
}
.lci-green { background: linear-gradient(135deg, #1a5c35, #34a853); }
.lci-blue  { background: linear-gradient(135deg, #1a3a6e, #2d6bc4); }
.lci-grey  { background: rgba(255,255,255,0.08); }
.land-card-body { flex: 1; }
.land-card-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: #e8f0eb;
    margin-bottom: 2px;
}
.land-card-desc {
    font-size: 0.7rem;
    color: #5a7a6a;
    font-weight: 400;
    line-height: 1.4;
}
.land-card-badge {
    font-size: 0.6rem;
    font-weight: 700;
    background: rgba(52,168,83,0.2);
    color: #6fcf8d;
    border: 1px solid rgba(52,168,83,0.3);
    border-radius: 4px;
    padding: 2px 6px;
    margin-top: 3px;
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.04em;
}
.land-card-arrow {
    color: rgba(255,255,255,0.2);
    font-size: 1rem;
    flex-shrink: 0;
}

.land-footer {
    padding: 1rem 2rem 1.5rem;
    text-align: center;
    font-size: 0.62rem;
    color: rgba(255,255,255,0.2);
    letter-spacing: 0.06em;
    font-family: 'JetBrains Mono', monospace;
    position: relative;
    z-index: 1;
}

/* Streamlit button overrides for landing */
section[data-testid="stVerticalBlock"] .stButton > button {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    height: auto !important;
    min-height: unset !important;
    color: transparent !important;
    font-size: 0 !important;
    position: absolute !important;
    inset: 0 !important;
    width: 100% !important;
    cursor: pointer !important;
    opacity: 0 !important;
}

/* ═══════════════════════════════════════════
   INNER PAGE HEADER
═══════════════════════════════════════════ */
.ae-header {
    background: linear-gradient(135deg, #0a1f12 0%, #0f2a18 100%);
    padding: 1rem 1.4rem 1.2rem;
    border-bottom: 1px solid rgba(52,168,83,0.15);
    position: sticky;
    top: 0;
    z-index: 100;
}
.ae-header-logo {
    font-size: 0.65rem;
    font-weight: 700;
    color: #34a853;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
    display: flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
}
.ae-header-logo::before {
    content: '←';
    font-size: 0.7rem;
    color: #2a7a45;
}
.ae-header-title {
    font-size: 1.4rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.5px;
    line-height: 1.2;
}
.ae-header-sub {
    font-size: 0.72rem;
    color: #4a7a5a;
    margin-top: 2px;
    font-weight: 400;
}

/* ═══════════════════════════════════════════
   CONTENT
═══════════════════════════════════════════ */
.ae-content { padding: 1.2rem 1.4rem; }
.ae-page { background: #f7f8f5; min-height: 100vh; }

/* ═══════════════════════════════════════════
   SECTION LABELS
═══════════════════════════════════════════ */
.ae-section {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8aaa96;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #e8ede9;
    margin: 1.4rem 0 0.9rem;
}

/* ═══════════════════════════════════════════
   CARDS
═══════════════════════════════════════════ */
.ae-card {
    background: #fff;
    border: 1px solid #e8ede9;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.6rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.ae-card-label {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #9ab0a0;
    margin-bottom: 4px;
}
.ae-card-value {
    font-size: 0.88rem;
    color: #1a1a1a;
    font-weight: 500;
    line-height: 1.5;
}

/* Report cards */
.rpt-card {
    background: #fff;
    border: 1px solid #e8ede9;
    border-radius: 12px;
    margin-bottom: 0.6rem;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    transition: box-shadow 0.2s;
}
.rpt-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08); }

/* ═══════════════════════════════════════════
   STATUS BADGES
═══════════════════════════════════════════ */
.badge {
    display: inline-flex;
    align-items: center;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    white-space: nowrap;
}
.badge-critical { background:#fde8e8; color:#c62828; }
.badge-high     { background:#fff0e0; color:#c25900; }
.badge-medium   { background:#fffbe0; color:#8a7000; }
.badge-low      { background:#e8f5ed; color:#1a6635; }
.badge-pending  { background:#fff0e0; color:#c25900; }
.badge-review   { background:#e8f0fe; color:#1a5c9a; }
.badge-done     { background:#e8f5ed; color:#1a6635; }

/* ═══════════════════════════════════════════
   METRICS
═══════════════════════════════════════════ */
.ae-metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    margin-bottom: 1.2rem;
}
.ae-metric {
    background: #fff;
    border: 1px solid #e8ede9;
    border-radius: 12px;
    padding: 1rem 0.6rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.ae-metric-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #0a1f12;
    line-height: 1;
}
.ae-metric-label {
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #9ab0a0;
    margin-top: 4px;
}

/* ═══════════════════════════════════════════
   BUTTONS
═══════════════════════════════════════════ */
.stButton > button {
    border-radius: 12px !important;
    min-height: 50px !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: 0.01em !important;
    width: 100% !important;
    transition: all 0.15s !important;
    border: none !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1a5c35, #2d8a52) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(26,92,53,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #145028, #256e42) !important;
    box-shadow: 0 6px 16px rgba(26,92,53,0.4) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: #fff !important;
    color: #1a5c35 !important;
    border: 1.5px solid #c8d8cc !important;
}

/* ═══════════════════════════════════════════
   INPUTS
═══════════════════════════════════════════ */
.stTextInput label, .stTextArea label, .stSelectbox label,
.stRadio label, .stNumberInput label, .stDateInput label,
.stFileUploader label {
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    color: #3a5a46 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    border-radius: 10px !important;
    border-color: #dce8e0 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
    background: #fff !important;
}
div[data-baseweb="input"] input:focus,
div[data-baseweb="textarea"] textarea:focus {
    border-color: #34a853 !important;
    box-shadow: 0 0 0 3px rgba(52,168,83,0.12) !important;
}
div[data-baseweb="select"] > div {
    border-radius: 10px !important;
    border-color: #dce8e0 !important;
    background: #fff !important;
}

/* ═══════════════════════════════════════════
   TABS
═══════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: #fff;
    border-radius: 0;
    padding: 0 1.4rem;
    gap: 0;
    border-bottom: 2px solid #e8ede9;
    margin: 0 0 1.2rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0 !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: 0.03em !important;
    padding: 0.8rem 1rem 0.8rem 0 !important;
    color: #8aaa96 !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #0a1f12 !important;
    border-bottom: 2px solid #34a853 !important;
    font-weight: 700 !important;
}

/* ═══════════════════════════════════════════
   ALERTS
═══════════════════════════════════════════ */
.ae-alert {
    background: #fde8e8;
    border-left: 3px solid #c62828;
    border-radius: 0 10px 10px 0;
    padding: 0.75rem 1rem;
    font-size: 0.82rem;
    color: #5a1515;
    margin-bottom: 0.8rem;
}
.ae-info {
    background: linear-gradient(135deg, #e8f5ed, #f0faf3);
    border: 1px solid #c8e8d4;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-size: 0.82rem;
    color: #0f3320;
    margin-bottom: 0.8rem;
}
.ae-warn {
    background: #fff8e0;
    border: 1px solid #f0d888;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-size: 0.82rem;
    color: #5a4000;
    margin-bottom: 0.8rem;
}
.ae-sep {
    height: 1px;
    background: #e8ede9;
    margin: 1.2rem 0;
}

/* ═══════════════════════════════════════════
   FARMER PROFILE STRIP
═══════════════════════════════════════════ */
.farmer-strip {
    background: linear-gradient(135deg, #0a1f12, #0f2a18);
    padding: 0.8rem 1.4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(52,168,83,0.15);
}
.farmer-strip-name {
    font-size: 0.9rem;
    font-weight: 700;
    color: #fff;
}
.farmer-strip-farm {
    font-size: 0.7rem;
    color: #4a7a5a;
    margin-top: 1px;
}
.farmer-strip-date {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #3a5a46;
}

/* ═══════════════════════════════════════════
   REPORT SUBMIT CONFIRMATION
═══════════════════════════════════════════ */
.submit-confirm {
    background: linear-gradient(135deg, #0a1f12, #1a3a22);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    margin: 1rem 0;
}
.submit-confirm-label {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #34a853;
    margin-bottom: 0.5rem;
}
.submit-confirm-id {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: 2px;
    margin-bottom: 0.6rem;
}
.submit-confirm-sub {
    font-size: 0.78rem;
    color: #4a7a5a;
    line-height: 1.5;
}

/* ═══════════════════════════════════════════
   WHATSAPP BUTTON
═══════════════════════════════════════════ */
.wa-btn {
    display: block;
    background: linear-gradient(135deg, #1ebe57, #25D366);
    color: white !important;
    text-align: center;
    padding: 0.9rem 1rem;
    border-radius: 12px;
    font-weight: 700;
    font-size: 0.88rem;
    text-decoration: none;
    letter-spacing: 0.02em;
    box-shadow: 0 4px 12px rgba(37,211,102,0.3);
    margin-top: 0.8rem;
    transition: all 0.15s;
}
.wa-btn:hover {
    box-shadow: 0 6px 16px rgba(37,211,102,0.4);
    transform: translateY(-1px);
    color: white !important;
}

/* ═══════════════════════════════════════════
   SCIENTIST REPORT CARD
═══════════════════════════════════════════ */
.sci-report {
    background: #fff;
    border: 1px solid #e8ede9;
    border-radius: 14px;
    overflow: hidden;
    margin: 0 0 0.8rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.sci-report-header {
    padding: 0.8rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid #f0f4f1;
}
.sci-report-name {
    font-size: 0.9rem;
    font-weight: 700;
    color: #111;
}
.sci-report-meta {
    font-size: 0.68rem;
    color: #8aaa96;
    margin-top: 2px;
    font-family: 'JetBrains Mono', monospace;
}
.sci-report-body { padding: 0.8rem 1rem; }

/* ═══════════════════════════════════════════
   KB REFERENCE PANEL
═══════════════════════════════════════════ */
.kb-panel {
    background: linear-gradient(135deg, #f0faf3, #e8f5ed);
    border: 1px solid #c8e8d4;
    border-radius: 12px;
    padding: 0.9rem 1rem;
    margin: 0.6rem 0;
}
.kb-source {
    font-size: 0.6rem;
    color: #6a9a7a;
    font-style: italic;
    margin-top: 0.5rem;
    border-top: 1px solid #d0e8d8;
    padding-top: 0.4rem;
}

/* ═══════════════════════════════════════════
   PRICE CARD
═══════════════════════════════════════════ */
.price-card {
    background: linear-gradient(135deg, #0a1f12, #1a3a22);
    border-radius: 16px;
    padding: 1.5rem;
    color: #fff;
    margin-bottom: 1rem;
}
.price-plan { font-size: 0.65rem; color: #34a853; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.3rem; }
.price-amount { font-family: 'JetBrains Mono', monospace; font-size: 2.5rem; font-weight: 700; line-height: 1; }
.price-unit { font-size: 0.75rem; color: #4a7a5a; margin-top: 3px; }
.price-feature { display: flex; justify-content: space-between; padding: 0.4rem 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 0.82rem; color: rgba(255,255,255,0.7); }
.price-check { color: #34a853; font-weight: 700; }

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-thumb { background: #c0d8c8; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────
for k, v in {
    "role":              None,
    "farmer_id":         None,
    "farmer_name":       None,
    "farm_id":           None,
    "farm_name":         None,
    "sci_id":            None,
    "sci_name":          None,
    "last_report":       None,
    "credits":           0,
    "sci_phone":         None,
    "pending_wa_url":    "",
    "pending_wa_farmer": "",
    "deep_report_id":    "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Landing ───────────────────────────────────────────────────────────────
if st.session_state.role is None:

    # Hero section — only safe CSS (no position:absolute, no webkit, no radial-gradient)
    st.markdown("""
    <div style="background:#0a1f12;padding:2.2rem 1.8rem 1.8rem;">

        <div style="display:flex;align-items:center;gap:8px;margin-bottom:1.8rem;">
            <div style="width:32px;height:32px;border-radius:8px;
                        background:#34a853;text-align:center;
                        line-height:32px;font-size:15px;">🌿</div>
            <div style="font-size:1rem;font-weight:800;color:#ffffff;letter-spacing:-0.3px;">
                Agri<span style="color:#34a853;">Expert</span>
            </div>
        </div>

        <div style="display:inline-block;background:#1a3a22;border:1px solid #2a5a32;
                    border-radius:20px;padding:4px 12px;font-size:0.65rem;font-weight:700;
                    color:#6fcf8d;letter-spacing:0.08em;text-transform:uppercase;
                    margin-bottom:1rem;">
            AI Crop Diagnostics
        </div>

        <div style="font-size:2.4rem;font-weight:800;color:#ffffff;line-height:1.1;
                    letter-spacing:-1px;margin-bottom:0.8rem;">
            Healthy crops.
        </div>
        <div style="font-size:2.4rem;font-weight:800;color:#34a853;line-height:1.1;
                    letter-spacing:-1px;margin-bottom:1rem;">
            Expert advice.
        </div>

        <div style="font-size:0.85rem;color:#6a9a7a;line-height:1.6;margin-bottom:1.8rem;">
            Photo to diagnosis in minutes.
            Reviewed by certified agronomists.
        </div>

        <div style="display:flex;gap:0.7rem;margin-bottom:0.5rem;">
            <div style="flex:1;background:#122a1a;border:1px solid #1e3a24;
                        border-radius:12px;padding:0.85rem 0.5rem;text-align:center;">
                <div style="font-size:1.6rem;font-weight:800;color:#ffffff;line-height:1;">100</div>
                <div style="font-size:0.58rem;color:#4a7a5a;text-transform:uppercase;
                            letter-spacing:0.08em;font-weight:700;margin-top:4px;">Farmers</div>
            </div>
            <div style="flex:1;background:#122a1a;border:1px solid #1e3a24;
                        border-radius:12px;padding:0.85rem 0.5rem;text-align:center;">
                <div style="font-size:1.6rem;font-weight:800;color:#ffffff;line-height:1;">10</div>
                <div style="font-size:0.58rem;color:#4a7a5a;text-transform:uppercase;
                            letter-spacing:0.08em;font-weight:700;margin-top:4px;">Scientists</div>
            </div>
            <div style="flex:1;background:#1a3a22;border:1px solid #2a5a32;
                        border-radius:12px;padding:0.85rem 0.5rem;text-align:center;">
                <div style="font-size:1.6rem;font-weight:800;color:#34a853;line-height:1;">AI</div>
                <div style="font-size:0.58rem;color:#4a7a5a;text-transform:uppercase;
                            letter-spacing:0.08em;font-weight:700;margin-top:4px;">Powered</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Role selector
    st.markdown("""
    <div style="background:#f7f8f5;padding:1.2rem 1.4rem 0.4rem;">
        <div style="font-size:0.62rem;font-weight:700;color:#8aaa96;
                    letter-spacing:0.12em;text-transform:uppercase;">
            Select your role
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Button styling — card look using Streamlit native
    st.markdown("""
    <style>
    [data-testid="stVerticalBlock"] [data-testid="stButton"] button {
        background: #fff !important;
        color: #111111 !important;
        border: 1.5px solid #e0e8e3 !important;
        border-radius: 14px !important;
        min-height: 64px !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    }
    [data-testid="stVerticalBlock"] [data-testid="stButton"]:first-of-type button {
        background: linear-gradient(135deg,#1a5c35,#2d8a52) !important;
        color: #fff !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(26,92,53,0.35) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding:0 1.4rem 1.4rem;background:#f7f8f5;">', unsafe_allow_html=True)

    if st.button("Farmer Portal  —  Submit photos, get recommendations",
                 key="go_farmer", type="primary", use_container_width=True):
        st.session_state.role = "farmer"
        st.rerun()
    st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)
    if st.button("Scientist Portal  —  Review reports, issue recommendations",
                 key="go_scientist", use_container_width=True):
        st.session_state.role = "scientist"
        st.rerun()
    st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)
    if st.button("Administrator  —  Manage platform, farms and users",
                 key="go_admin", use_container_width=True):
        st.session_state.role = "admin"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#f7f8f5;text-align:center;padding:1rem 0 1.5rem;
                font-size:0.6rem;color:#b0c8b8;letter-spacing:0.1em;">
        AGRIEXPERT.IN &nbsp;·&nbsp; IDUKKI, KERALA
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.role == "farmer":
    from pages.farmer import show_farmer
    show_farmer()

elif st.session_state.role == "scientist":
    from pages.scientist import show_scientist
    show_scientist()

elif st.session_state.role == "admin":
    from pages.admin import show_admin
    show_admin()
