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
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background: #f5f5f0;
    color: #1a1a1a;
    -webkit-tap-highlight-color: transparent;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 !important;
    max-width: 480px !important;
    margin: 0 auto !important;
}

/* ── Landing ── */
.ae-landing {
    background: #0f2218;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    padding: 0;
}
.ae-landing-top {
    padding: 3.5rem 2.5rem 2rem;
    flex: 1;
}
.ae-wordmark {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    color: #5a9a6e;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.ae-headline {
    font-size: 2.4rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.15;
    letter-spacing: -0.5px;
    margin-bottom: 0.5rem;
}
.ae-headline span { color: #6fcf8d; }
.ae-subline {
    font-size: 0.9rem;
    color: #7aab8a;
    font-weight: 300;
    line-height: 1.5;
    margin-bottom: 0.3rem;
}

/* Divider line */
.ae-divider {
    height: 1px;
    background: linear-gradient(90deg, #2a4a36 0%, #1a3226 100%);
    margin: 2rem 0;
}

/* ── Role selector ── */
.ae-roles {
    padding: 0 2.5rem 3rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}
.ae-role {
    border: 1px solid #1e3628;
    border-radius: 4px;
    padding: 1.1rem 1.4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    transition: all 0.15s;
    background: #132018;
}
.ae-role:hover { border-color: #4a8a5e; background: #1a2e22; }
.ae-role-left {}
.ae-role-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #e8f0eb;
    margin-bottom: 2px;
}
.ae-role-sub {
    font-size: 0.72rem;
    color: #5a8a6e;
    font-weight: 300;
}

.ae-role-arrow {
    font-size: 0.9rem;
    color: #4a8a5e;
    font-family: 'IBM Plex Mono', monospace;
}

/* Credit badge on role */
.ae-credit-note {
    font-size: 0.65rem;
    font-family: 'IBM Plex Mono', monospace;
    background: #1e3a28;
    color: #6fcf8d;
    border: 1px solid #2a5038;
    border-radius: 2px;
    padding: 1px 5px;
    margin-top: 3px;
    display: inline-block;
}

/* ── Inner pages header ── */
.ae-header {
    background: #0f2218;
    padding: 1.1rem 1.4rem 1.3rem;
    border-bottom: 1px solid #1e3628;
}
.ae-header-nav {
    font-size: 0.72rem;
    color: #4a7a5a;
    margin-bottom: 0.5rem;
    cursor: pointer;
    letter-spacing: 0.05em;
}
.ae-header-nav:hover { color: #6fcf8d; }
.ae-header-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.3px;
}
.ae-header-sub {
    font-size: 0.75rem;
    color: #5a8a6e;
    margin-top: 2px;
    font-weight: 300;
}

/* ── Content wrapper ── */
.ae-content { padding: 1.2rem 1.4rem; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 3px !important;
    min-height: 48px !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    width: 100% !important;
    transition: all 0.15s !important;
}
.stButton > button[kind="primary"] {
    background: #1a5c35 !important;
    color: white !important;
}
.stButton > button[kind="primary"]:hover {
    background: #145028 !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #1a5c35 !important;
    border: 1px solid #c8d8cc !important;
}

/* ── Form inputs ── */
.stTextInput label, .stTextArea label, .stSelectbox label,
.stRadio label, .stNumberInput label, .stDateInput label,
.stFileUploader label {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #3a5a46 !important;
    letter-spacing: 0.03em !important;
    text-transform: uppercase !important;
}
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    border-radius: 3px !important;
    border-color: #d0d8d4 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}
div[data-baseweb="select"] {
    border-radius: 3px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff;
    border-radius: 0;
    padding: 0;
    gap: 0;
    border-bottom: 2px solid #e8ede9;
    margin: 0 0 1.2rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0 !important;
    font-weight: 500 !important;
    font-size: 0.8rem !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    letter-spacing: 0.04em !important;
    padding: 0.75rem 1rem !important;
    color: #6a8a76 !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
}
.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: #0f2218 !important;
    border-bottom: 2px solid #1a5c35 !important;
    font-weight: 600 !important;
}

/* ── Cards ── */
.ae-card {
    background: #ffffff;
    border: 1px solid #e0e8e3;
    border-radius: 4px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.6rem;
}
.ae-card-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #8aaa96;
    margin-bottom: 4px;
}
.ae-card-value {
    font-size: 0.88rem;
    color: #1a1a1a;
    font-weight: 500;
    line-height: 1.4;
}

/* ── Status badges ── */
.badge {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 2px;
    font-family: 'IBM Plex Mono', monospace;
}
.badge-pending  { background:#fff3e0; color:#c25900; border:1px solid #f0c888; }
.badge-review   { background:#e8f0fe; color:#1a5c9a; border:1px solid #b8d0f0; }
.badge-done     { background:#e8f5ed; color:#1a6635; border:1px solid #a8d8b8; }
.badge-critical { background:#fde8e8; color:#9a1a1a; border:1px solid #f0a8a8; }
.badge-high     { background:#fff0e0; color:#8a3a00; border:1px solid #f0c8a0; }
.badge-medium   { background:#fffbe0; color:#7a6000; border:1px solid #e8d888; }
.badge-low      { background:#e8f5ed; color:#1a6635; border:1px solid #a8d8b8; }

/* ── Severity bar ── */
.sev-bar {
    height: 3px;
    border-radius: 0;
    margin: 0.5rem 0;
}

/* ── Report card ── */
.rpt-card {
    background: #fff;
    border: 1px solid #e0e8e3;
    border-left: 3px solid #1a5c35;
    border-radius: 0 4px 4px 0;
    padding: 0.9rem 1rem;
    margin-bottom: 0.5rem;
}
.rpt-card.critical { border-left-color: #c62828; }
.rpt-card.high     { border-left-color: #e65100; }
.rpt-card.medium   { border-left-color: #f9a825; }
.rpt-card.low      { border-left-color: #2e7d32; }

/* ── Metric strip ── */
.ae-metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: #e0e8e3;
    border: 1px solid #e0e8e3;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 1.2rem;
}
.ae-metric {
    background: #fff;
    padding: 0.9rem 0.8rem;
    text-align: center;
}
.ae-metric-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.6rem;
    font-weight: 500;
    color: #0f2218;
    line-height: 1;
}
.ae-metric-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8aaa96;
    margin-top: 4px;
}

/* ── Credit display ── */
.credit-strip {
    background: #0f2218;
    color: #6fcf8d;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    padding: 0.6rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #1e3628;
}
.credit-count {
    font-size: 1.1rem;
    font-weight: 500;
}

/* ── Pricing card ── */
.price-card {
    background: #fff;
    border: 1px solid #e0e8e3;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 1rem;
}
.price-header {
    background: #0f2218;
    padding: 1rem 1.2rem;
    color: #fff;
}
.price-plan {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #5a9a6e;
    margin-bottom: 3px;
}
.price-amount {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2rem;
    font-weight: 500;
    color: #fff;
    line-height: 1;
}
.price-unit {
    font-size: 0.75rem;
    color: #6a9a78;
    margin-top: 3px;
}
.price-body { padding: 1rem 1.2rem; }
.price-feature {
    font-size: 0.82rem;
    color: #3a5a46;
    padding: 0.35rem 0;
    border-bottom: 1px solid #f0f4f1;
    display: flex;
    justify-content: space-between;
}
.price-check { color: #1a5c35; font-weight: 600; }

/* ── Divider ── */
.ae-sep {
    height: 1px;
    background: #e8ede9;
    margin: 1.2rem 0;
}

/* ── Alert box ── */
.ae-alert {
    border-left: 3px solid #c62828;
    background: #fde8e8;
    padding: 0.75rem 1rem;
    border-radius: 0 3px 3px 0;
    font-size: 0.82rem;
    color: #5a1515;
    margin-bottom: 0.8rem;
}
.ae-alert-hi {
    font-family: sans-serif;
    font-size: 0.75rem;
    color: #8a3030;
    margin-top: 2px;
}
.ae-info {
    border-left: 3px solid #1a5c35;
    background: #e8f5ed;
    padding: 0.75rem 1rem;
    border-radius: 0 3px 3px 0;
    font-size: 0.82rem;
    color: #0f3320;
    margin-bottom: 0.8rem;
}

/* ── Section title ── */
.ae-section {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8aaa96;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #e8ede9;
    margin: 1.2rem 0 0.8rem;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #c0d0c8; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────
for k, v in {
    "role":        None,
    "farmer_id":   None,
    "farmer_name": None,
    "farm_id":     None,
    "farm_name":   None,
    "sci_id":      None,
    "sci_name":    None,
    "last_report": None,
    "credits":     0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Landing ───────────────────────────────────────────────────────────────
if st.session_state.role is None:

    # Header block
    st.markdown("""
    <div style="background:#0f2218;padding:3rem 2rem 2rem;min-height:45vh;">
        <div style="font-size:0.72rem;font-weight:600;letter-spacing:0.2em;
                    color:#5a9a6e;text-transform:uppercase;margin-bottom:0.75rem;">
            AgriExpert
        </div>
        <div style="font-size:2.2rem;font-weight:700;color:#ffffff;
                    line-height:1.15;letter-spacing:-0.5px;margin-bottom:0.5rem;">
            Crop health<br>diagnostics.<br>
            <span style="color:#6fcf8d;">Expert advice.</span>
        </div>
        <div style="height:1px;background:linear-gradient(90deg,#2a4a36,#1a3226);
                    margin:1.5rem 0;"></div>
        <div style="font-size:0.88rem;color:#7aab8a;font-weight:300;line-height:1.5;">
            Submit a photo. Get an AI pre-diagnosis.<br>
            Receive recommendations from certified agronomists.
        </div>
        <div style="font-family:'IBM Plex Sans',sans-serif;font-size:0.8rem;
                    color:#4a7a5a;margin-top:4px;">
             AI  
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Role buttons — full width, clearly tappable
    st.markdown("""
    <div style="background:#0f2218;padding:0 1.5rem 0.5rem;">
        <div style="font-size:0.62rem;font-weight:600;letter-spacing:0.12em;
                    text-transform:uppercase;color:#3a6a4e;margin-bottom:0.6rem;">
            Select your role
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Override button style for landing page — dark theme full-width cards
    st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]:first-child .stButton > button,
    .landing-btn .stButton > button {
        background: #132018 !important;
        color: #e8f0eb !important;
        border: 1px solid #1e3628 !important;
        border-radius: 3px !important;
        min-height: 64px !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        text-align: left !important;
        padding: 0 1.2rem !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div style="background:#0f2218;padding:0 1.5rem 2rem;">', unsafe_allow_html=True)

    if st.button("Farmer Portal", key="go_farmer", type="primary",
                  use_container_width=True):
        st.session_state.role = "farmer"
        st.rerun()

    st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)

    if st.button("Scientist Portal", key="go_scientist",
                  use_container_width=True):
        st.session_state.role = "scientist"
        st.rerun()

    st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)

    if st.button("Administrator", key="go_admin", use_container_width=True):
        st.session_state.role = "admin"
        st.rerun()

    st.markdown("""
    </div>
    <div style="background:#0f2218;padding:0.8rem 1.5rem 1.5rem;
                font-size:0.65rem;color:#2a4a36;text-align:center;
                font-family:'IBM Plex Mono',monospace;letter-spacing:0.08em;">
        agriexpert.in  ·  Crop Diagnostics Platform  ·  Free during launch
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
