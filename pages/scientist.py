"""AgriExpert — Scientist Portal"""

import streamlit as st
import pandas as pd
from datetime import datetime
from data import (
    clean, safe_update, load_scientists, load_reports,
    BADGE_CLASS, STATUS_BADGE
)
from cardamom_kb import get_disease_kb, get_seasonal_advisory

def show_scientist():
    today = datetime.now().date()

    if st.button("Back to Home", key="sci_back"):
        st.session_state.role   = None
        st.session_state.sci_id = None
        st.rerun()

    st.markdown("""
    <div class="ae-header">
        <div class="ae-header-nav">AgriExpert / Scientist Portal</div>
        <div class="ae-header-title">Scientist Portal</div>
        <div class="ae-header-sub">Review diagnostic queue · Issue recommendations</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Auth ──────────────────────────────────────────────────────────────
    if not st.session_state.sci_id:
        scientists_df = load_scientists()
        st.markdown('<div class="ae-content">', unsafe_allow_html=True)

        phone = st.text_input("Registered Phone", key="sci_phone")
        pin   = st.text_input("PIN", type="password", max_chars=6, key="sci_pin")

        if st.button("Login", type="primary", key="sci_login"):
            if not phone.strip() or not pin.strip():
                st.error("Enter phone number and PIN.")
            elif not scientists_df.empty:
                match = scientists_df[
                    (scientists_df["Phone"].astype(str).str.strip() == phone.strip()) &
                    (scientists_df["PIN"].astype(str).str.strip() == pin.strip())
                ]
                if match.empty:
                    st.error("Invalid credentials.")
                elif clean(match.iloc[0].get("Is_Active","True")).lower() in ("false","0","no"):
                    st.error("Account inactive. Contact administrator.")
                else:
                    row = match.iloc[0]
                    st.session_state.sci_id   = clean(row.get("Sci_ID"))
                    st.session_state.sci_name = clean(row.get("Name"))
                    st.cache_data.clear()
                    st.rerun()
            else:
                st.error("No scientists registered.")

        st.markdown('</div>', unsafe_allow_html=True)
        return

    # ── Dashboard ─────────────────────────────────────────────────────────
    reports_df = load_reports()

    # Scientist info strip
    scientists_df = load_scientists()
    sci_row = scientists_df[scientists_df["Sci_ID"] == st.session_state.sci_id] \
              if not scientists_df.empty else pd.DataFrame()
    sci_spec = clean(sci_row.iloc[0].get("Specialization",""), "") if not sci_row.empty else ""
    sci_inst = clean(sci_row.iloc[0].get("Institution",""), "") if not sci_row.empty else ""

    st.markdown(f"""
    <div style="background:#0f2218;padding:0.7rem 1.4rem;
                border-bottom:1px solid #1e3628;
                display:flex;justify-content:space-between;align-items:center;">
        <div>
            <div style="font-size:0.88rem;font-weight:600;color:#e8f0eb;">
                {st.session_state.sci_name}
            </div>
            <div style="font-size:0.68rem;color:#5a8a6e;">
                {sci_spec}{"  ·  " + sci_inst if sci_inst else ""}
            </div>
        </div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.68rem;
                    color:#3a6a4e;">{today}</div>
    </div>
    """, unsafe_allow_html=True)

    tab_pending, tab_done = st.tabs(["Pending Review", "Completed"])

    # ── Shared render function ─────────────────────────────────────────────
    def render_reports(df, allow_response=True):
        if df.empty:
            st.markdown("""
            <div class="ae-content">
            <div style="text-align:center;padding:2rem;color:#8aaa96;
                        font-size:0.85rem;">No reports in this queue.</div>
            </div>""", unsafe_allow_html=True)
            return

        # KPIs
        total    = len(df)
        critical = len(df[df["AI_Severity"] == "Critical"])
        high     = len(df[df["AI_Severity"] == "High"])

        st.markdown(f"""
        <div class="ae-metrics" style="margin:1rem 1.4rem;">
            <div class="ae-metric">
                <div class="ae-metric-val">{total}</div>
                <div class="ae-metric-label">Total</div>
            </div>
            <div class="ae-metric">
                <div class="ae-metric-val" style="color:#c62828;">{critical}</div>
                <div class="ae-metric-label">Critical</div>
            </div>
            <div class="ae-metric">
                <div class="ae-metric-val" style="color:#e65100;">{high}</div>
                <div class="ae-metric-label">High</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Sort by severity
        sev_ord = {"Critical":0,"High":1,"Medium":2,"Low":3,"None":4}
        try:
            df = df.copy()
            df["_s"] = df["AI_Severity"].map(sev_ord).fillna(5)
            df = df.sort_values("_s")
        except: pass

        for _, rpt in df.iterrows():
            rid      = clean(rpt.get("Report_ID"), "—")
            farmer   = clean(rpt.get("Farmer_Name"), "—")
            farm     = clean(rpt.get("Farm_Name"), "—")
            crop     = clean(rpt.get("Crop_Type"), "—")
            part     = clean(rpt.get("Plant_Part"), "")
            ai_cond  = clean(rpt.get("AI_Condition"), "—")
            ai_sev   = clean(rpt.get("AI_Severity"), "Low")
            findings = clean(rpt.get("AI_Findings"), "")
            ai_treat = clean(rpt.get("AI_Treatment"), "")
            ai_note  = clean(rpt.get("AI_Expert_Note"), "")
            symptoms = clean(rpt.get("Symptoms"), "")
            sub_at   = clean(rpt.get("Submitted_At"), "")
            status   = clean(rpt.get("Status"), "Pending")
            sc       = {"Critical":"#c62828","High":"#e65100",
                        "Medium":"#f9a825","Low":"#1a5c35"}.get(ai_sev,"#6a8a76")
            badge    = BADGE_CLASS.get(ai_sev,"low")

            with st.expander(f"[{ai_sev.upper()}]  {rid}  —  {farm}  —  {ai_cond}"):
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;
                            align-items:flex-start;margin-bottom:0.8rem;">
                    <div>
                        <div style="font-size:0.95rem;font-weight:600;color:{sc};">
                            {ai_cond}
                        </div>
                        <div style="font-size:0.72rem;color:#8aaa96;
                                    font-family:'IBM Plex Mono',monospace;margin-top:2px;">
                            {crop} · {farm} · {farmer}
                            {" · " + part if part and part != "—" else ""}
                        </div>
                        <div style="font-size:0.68rem;color:#b0c8b8;
                                    font-family:'IBM Plex Mono',monospace;margin-top:1px;">
                            Submitted: {sub_at}
                        </div>
                    </div>
                    <span class="badge badge-{badge}">{ai_sev}</span>
                </div>
                """, unsafe_allow_html=True)

                # AI data cards
                for label, val in [
                    ("AI Findings", findings),
                    ("AI Treatment Suggestion", ai_treat),
                    ("Grower Observations", symptoms),
                ]:
                    if val and val not in ("—",""):
                        st.markdown(f"""
                        <div class="ae-card">
                            <div class="ae-card-label">{label}</div>
                            <div class="ae-card-value">{val}</div>
                        </div>
                        """, unsafe_allow_html=True)

                if ai_note and ai_note not in ("—",""):
                    st.markdown(f"""
                    <div class="ae-card" style="background:#e8f0fe;border-color:#b8d0f0;">
                        <div class="ae-card-label" style="color:#1a5c9a;">
                            For Specialist Review
                        </div>
                        <div class="ae-card-value" style="color:#1a3a6a;">
                            {ai_note}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # ── Knowledge Base Reference Panel ──────────────────────
                try:
                    from datetime import datetime as _dt
                    _month = _dt.now().month
                    _adv   = get_seasonal_advisory(_month)
                    _kb_name, _kb = get_disease_kb(ai_cond)

                    if _kb:
                        with st.expander(
                            f"Knowledge Base Reference — {_kb_name}",
                            expanded=True
                        ):
                            # Seasonal context
                            st.markdown(f"""
                            <div style="background:#fff8e0;border-left:3px solid #f9a825;
                                        padding:0.6rem 0.9rem;border-radius:0 4px 4px 0;
                                        margin-bottom:0.8rem;">
                                <div style="font-size:0.62rem;font-weight:600;
                                            letter-spacing:0.1em;text-transform:uppercase;
                                            color:#8a6000;margin-bottom:3px;">
                                    Seasonal Risk — This Month
                                </div>
                                <div style="font-size:0.8rem;color:#5a4000;font-weight:500;">
                                    {_adv.get('diseases','—')}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            # Disease profile
                            _fields = [
                                ("Causal Organism",    _kb.get("causal","—")),
                                ("Parts Affected",     _kb.get("parts","—")),
                                ("Peak Season",        _kb.get("season","—")),
                                ("Conditions",         _kb.get("conditions","—")),
                                ("Crop Loss",          _kb.get("severity","—")),
                                ("Distribution",       _kb.get("distribution","—")),
                            ]
                            for label, val in _fields:
                                if val and val != "—":
                                    st.markdown(f"""
                                    <div class="ae-card" style="margin-bottom:4px;padding:0.6rem 0.8rem;">
                                        <div class="ae-card-label">{label}</div>
                                        <div class="ae-card-value" style="font-size:0.82rem;">
                                            {val}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)

                            # Symptoms
                            _syms = _kb.get("symptoms",[])
                            if _syms:
                                st.markdown("""
                                <div style="font-size:0.62rem;font-weight:600;
                                            letter-spacing:0.1em;text-transform:uppercase;
                                            color:#8aaa96;margin:0.6rem 0 0.3rem;">
                                    Book-Referenced Symptoms
                                </div>
                                """, unsafe_allow_html=True)
                                for s in _syms:
                                    st.markdown(f"""
                                    <div style="padding:3px 0 3px 0.8rem;font-size:0.8rem;
                                                color:#2a2a2a;border-left:2px solid #c8d8cc;">
                                        {s}
                                    </div>
                                    """, unsafe_allow_html=True)

                            # Management
                            _mgmt = _kb.get("management",{})
                            _chem = _mgmt.get("chemical",[])
                            _bio  = _mgmt.get("biological",[])
                            _cult = _mgmt.get("cultural",[])

                            if _chem:
                                st.markdown("""
                                <div style="font-size:0.62rem;font-weight:600;
                                            letter-spacing:0.1em;text-transform:uppercase;
                                            color:#1a5c35;margin:0.7rem 0 0.3rem;">
                                    Chemical Management (Book Reference)
                                </div>
                                """, unsafe_allow_html=True)
                                for m in _chem:
                                    st.markdown(f"""
                                    <div style="padding:3px 0 3px 0.8rem;font-size:0.8rem;
                                                color:#1a3a26;border-left:2px solid #1a5c35;
                                                margin-bottom:2px;">
                                        {m}
                                    </div>
                                    """, unsafe_allow_html=True)

                            if _bio:
                                st.markdown("""
                                <div style="font-size:0.62rem;font-weight:600;
                                            letter-spacing:0.1em;text-transform:uppercase;
                                            color:#1a5c9a;margin:0.7rem 0 0.3rem;">
                                    Biological Control (Book Reference)
                                </div>
                                """, unsafe_allow_html=True)
                                for m in _bio:
                                    st.markdown(f"""
                                    <div style="padding:3px 0 3px 0.8rem;font-size:0.8rem;
                                                color:#1a3a6a;border-left:2px solid #1a5c9a;
                                                margin-bottom:2px;">
                                        {m}
                                    </div>
                                    """, unsafe_allow_html=True)

                            if _cult:
                                st.markdown("""
                                <div style="font-size:0.62rem;font-weight:600;
                                            letter-spacing:0.1em;text-transform:uppercase;
                                            color:#8a3a00;margin:0.7rem 0 0.3rem;">
                                    Cultural Practices
                                </div>
                                """, unsafe_allow_html=True)
                                for m in _cult:
                                    st.markdown(f"""
                                    <div style="padding:3px 0 3px 0.8rem;font-size:0.8rem;
                                                color:#5a2a00;border-left:2px solid #e65100;
                                                margin-bottom:2px;">
                                        {m}
                                    </div>
                                    """, unsafe_allow_html=True)

                            # Sources
                            _sources = _kb.get("sources",[])
                            if _sources:
                                st.markdown(f"""
                                <div style="font-size:0.65rem;color:#8aaa96;
                                            margin-top:0.6rem;font-style:italic;
                                            border-top:1px solid #e8ede9;padding-top:0.4rem;">
                                    Sources: {" · ".join(_sources)}
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        # No KB match — show seasonal advisory only
                        with st.expander("Seasonal Advisory", expanded=False):
                            st.markdown(f"""
                            <div class="ae-card">
                                <div class="ae-card-label">Current Month Disease Risk</div>
                                <div class="ae-card-value">{_adv.get('diseases','—')}</div>
                            </div>
                            <div class="ae-card">
                                <div class="ae-card-label">Recommended Activity</div>
                                <div class="ae-card-value">{_adv.get('activity','—')}</div>
                            </div>
                            """, unsafe_allow_html=True)
                except Exception as _kb_err:
                    st.caption(f"KB reference unavailable: {_kb_err}")

                # Response form
                if allow_response and status not in ("Responded","Closed"):
                    st.markdown('<div class="ae-sep"></div>', unsafe_allow_html=True)
                    st.markdown("""
                    <div style="font-size:0.65rem;font-weight:600;letter-spacing:0.12em;
                                text-transform:uppercase;color:#3a5a46;margin-bottom:0.6rem;">
                        Your Assessment
                    </div>
                    """, unsafe_allow_html=True)

                    with st.form(f"resp_{rid}", clear_on_submit=True):
                        confirmed = st.text_input(
                            "Confirmed Diagnosis",
                            value=ai_cond, key=f"c_{rid}"
                        )
                        recs = st.text_area(
                            "Recommendations",
                            placeholder="Provide detailed treatment recommendations...",
                            height=130, key=f"r_{rid}"
                        )
                        meds = st.text_area(
                            "Medicines (product name, dosage, frequency, duration)",
                            height=90, key=f"m_{rid}"
                        )
                        fc1, fc2 = st.columns(2)
                        followup = fc1.selectbox(
                            "Follow-up Required",
                            ["Not required","Monitor weekly","Site visit required"],
                            key=f"f_{rid}"
                        )
                        nxt = fc2.text_input(
                            "Next visit date",
                            key=f"n_{rid}"
                        )
                        notes = st.text_area(
                            "Additional notes for farmer",
                            height=60, key=f"an_{rid}"
                        )

                        if st.form_submit_button("Submit Assessment",
                                                 type="primary"):
                            if not confirmed.strip() or not recs.strip():
                                st.error("Confirmed diagnosis and recommendations are required.")
                            else:
                                existing = load_reports()
                                mask = existing["Report_ID"] == rid
                                existing.loc[mask, "Sci_Confirmed"]      = confirmed.strip()
                                existing.loc[mask, "Sci_Recommendations"]= recs.strip()
                                existing.loc[mask, "Sci_Medicines"]      = meds.strip()
                                existing.loc[mask, "Sci_Follow_Up"]      = followup
                                existing.loc[mask, "Sci_Next_Visit"]     = nxt.strip()
                                existing.loc[mask, "Additional_Notes"]   = notes.strip()
                                existing.loc[mask, "Status"]             = "Responded"
                                existing.loc[mask, "Reviewed_At"]        = datetime.now().strftime("%Y-%m-%d %H:%M")
                                existing.loc[mask, "Reviewed_By"]        = st.session_state.sci_name

                                ok, err = safe_update("Plant_Reports", existing)
                                if ok:
                                    st.success(f"Assessment submitted for {rid}")
                                    st.cache_data.clear()
                                    st.rerun()
                                else:
                                    st.error(f"Save failed: {err}")

                elif not allow_response:
                    rev_by  = clean(rpt.get("Reviewed_By"), "")
                    rev_at  = clean(rpt.get("Reviewed_At"), "")
                    recs_d  = clean(rpt.get("Sci_Recommendations"), "")
                    st.markdown(f"""
                    <div class="ae-sep"></div>
                    <div class="ae-info">
                        <strong>Assessment submitted</strong>
                        {" by " + rev_by if rev_by and rev_by != "—" else ""}
                        {" at " + rev_at if rev_at and rev_at != "—" else ""}
                        <br><span style="color:#2a5a36;">{recs_d[:150]}{"..." if len(recs_d)>150 else ""}</span>
                    </div>
                    """, unsafe_allow_html=True)

    with tab_pending:
        if st.button("Refresh Queue", key="sci_ref_p"):
            st.cache_data.clear()
            st.rerun()

        pending = pd.DataFrame()
        if not reports_df.empty:
            pending = reports_df[reports_df["Status"].isin(["Pending","Under Review"])]
        render_reports(pending, allow_response=True)

    with tab_done:
        if st.button("Refresh", key="sci_ref_d"):
            st.cache_data.clear()
            st.rerun()

        done = pd.DataFrame()
        if not reports_df.empty:
            done = reports_df[
                (reports_df["Status"].isin(["Responded","Closed"])) &
                (reports_df["Reviewed_By"].astype(str) == str(st.session_state.sci_name))
            ].sort_values("Reviewed_At", ascending=False)
        render_reports(done, allow_response=False)
