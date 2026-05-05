"""AgriExpert — Farmer Portal"""

import streamlit as st
import pandas as pd
from datetime import datetime
from data import (
    clean, gen_id, safe_update,
    load_farms, load_farmers, load_reports, load_crop_types, load_transactions,
    get_farmer_credits, deduct_credit, run_ai_diagnosis,
    CREDIT_PRICE_INR, FREE_CREDITS, BADGE_CLASS, STATUS_BADGE,
    IDUKKI_VILLAGES
)

def show_farmer():
    today = datetime.now().date()

    if st.button("Back to Home", key="farmer_back"):
        st.session_state.role = None
        st.session_state.farmer_id = None
        st.rerun()

    st.markdown("""
    <div class="ae-header">
        <div class="ae-header-nav">AgriExpert / Farmer Portal</div>
        <div class="ae-header-title">Farmer Portal</div>
        <div class="ae-header-sub">Submit reports · Track recommendations</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Auth ──────────────────────────────────────────────────────────────
    if not st.session_state.farmer_id:
        farmers_df = load_farmers()
        farms_df   = load_farms()

        st.markdown('<div class="ae-content">', unsafe_allow_html=True)

        tab_login, tab_reg = st.tabs(["Login", "New Registration"])

        with tab_login:
            phone = st.text_input("Phone Number", placeholder="10-digit mobile number",
                                  key="fl_phone")
            if st.button("Continue", type="primary", key="fl_btn"):
                if not phone.strip():
                    st.error("Enter your phone number.")
                elif not farmers_df.empty and "Phone" in farmers_df.columns:
                    match = farmers_df[
                        farmers_df["Phone"].astype(str).str.strip() == phone.strip()
                    ]
                    if match.empty:
                        st.error("Phone number not registered. Please register first.")
                    else:
                        row = match.iloc[0]
                        st.session_state.farmer_id   = clean(row.get("Farmer_ID"))
                        st.session_state.farmer_name = clean(row.get("Name"))
                        st.session_state.farm_id     = clean(row.get("Farm_ID"))
                        st.session_state.farm_name   = clean(row.get("Farm_Name"))
                        st.session_state.credits     = get_farmer_credits(
                            st.session_state.farmer_id
                        )
                        st.cache_data.clear()
                        st.rerun()
                else:
                    st.error("No farmers registered yet.")

        with tab_reg:
            if farms_df.empty:
                st.markdown("""
                <div class="ae-info">
                    No farms registered yet. Contact your farm administrator
                    to register your farm before signing up.
                </div>
                """, unsafe_allow_html=True)
            else:
                farm_opts = farms_df["Farm_Name"].tolist() if "Farm_Name" in farms_df.columns else []
                with st.form("farmer_reg", clear_on_submit=True):
                    r_name  = st.text_input("Full Name")
                    r_phone = st.text_input("Phone Number")
                    r_farm  = st.selectbox("Your Farm", farm_opts)
                    r_village = st.selectbox(
                        "Village / Location *",
                        ["Select your village"] + IDUKKI_VILLAGES
                    )
                    r_lang  = st.selectbox("Preferred Language", [
                        "English", "Tamil", "Malayalam"
                    ])
                    if st.form_submit_button("Register", type="primary"):
                        if not r_name.strip():
                            st.error("Full name is required.")
                        elif not r_phone.strip():
                            st.error("Phone number is mandatory.")
                        elif len(r_phone.strip()) != 10 or not r_phone.strip().isdigit():
                            st.error("Enter a valid 10-digit phone number.")
                        elif r_village == "Select your village":
                            st.error("Please select your village.")
                        else:
                            if not farmers_df.empty and "Phone" in farmers_df.columns:
                                dup = farmers_df[
                                    farmers_df["Phone"].astype(str).str.strip() == r_phone.strip()
                                ]
                                if not dup.empty:
                                    st.error("This phone number is already registered.")
                                    st.stop()

                            farm_row = farms_df[farms_df["Farm_Name"] == r_farm]
                            farm_id  = clean(farm_row.iloc[0].get("Farm_ID")) if not farm_row.empty else ""

                            fid = gen_id("FMR", r_phone)
                            new = pd.DataFrame([{
                                "Farmer_ID":    fid,
                                "Name":         r_name.strip(),
                                "Phone":        r_phone.strip(),
                                "Village":      r_village,
                                "Farm_ID":      farm_id,
                                "Farm_Name":    r_farm,
                                "Language":     r_lang,
                                "Credits":      FREE_CREDITS,
                                "Registered_At":datetime.now().strftime("%Y-%m-%d %H:%M"),
                            }])
                            ok, err = safe_update(
                                "Farmers",
                                pd.concat([farmers_df, new], ignore_index=True)
                            )
                            if ok:
                                # Log the free credit grant
                                from data import add_credits
                                add_credits(fid, r_name.strip(),
                                            FREE_CREDITS, 0,
                                            f"Welcome — {FREE_CREDITS} free credits")
                                st.markdown(f"""
                                <div class="ae-info">
                                    Registration successful. You have been credited
                                    <strong>{FREE_CREDITS} free diagnostic credits</strong>.
                                    Login with your phone number.
                                </div>
                                """, unsafe_allow_html=True)
                                st.cache_data.clear()
                            else:
                                st.error(f"Registration failed: {err}")

        st.markdown('</div>', unsafe_allow_html=True)
        return

    # ── Logged-in ─────────────────────────────────────────────────────────
    farms_df   = load_farms()
    credits    = get_farmer_credits(st.session_state.farmer_id)

    # Resolve farm details
    farm_name  = clean(st.session_state.farm_name, "")
    crop_type  = "Cardamom"
    if st.session_state.farm_id and not farms_df.empty:
        fr = farms_df[farms_df["Farm_ID"] == st.session_state.farm_id]
        if not fr.empty:
            farm_name = clean(fr.iloc[0].get("Farm_Name"), farm_name)
            crop_type = clean(fr.iloc[0].get("Crop_Type"), "Cardamom")

    # Credit strip
    credit_color = "#c62828" if credits == 0 else ("#f9a825" if credits <= 1 else "#6fcf8d")
    st.markdown(f"""
    <div class="credit-strip">
        <div>
            <span style="opacity:0.6;font-size:0.68rem;letter-spacing:0.08em;">
                DIAGNOSTIC CREDITS
            </span>
        </div>
        <div class="credit-count" style="color:{credit_color};">
            {credits} credit{"s" if credits != 1 else ""} remaining
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_submit, tab_reports, tab_credits = st.tabs([
        "New Report", "My Reports", "Credits"
    ])

    # ── SUBMIT ────────────────────────────────────────────────────────────
    with tab_submit:
        st.markdown('<div class="ae-content">', unsafe_allow_html=True)

        # Farm context
        st.markdown(f"""
        <div class="ae-card">
            <div class="ae-card-label">Farm</div>
            <div class="ae-card-value">{farm_name}</div>
            <div class="ae-card-label" style="margin-top:6px;">Crop</div>
            <div class="ae-card-value">{crop_type}</div>
        </div>
        """, unsafe_allow_html=True)

        if credits <= 0:
            st.markdown(f"""
            <div class="ae-alert">
                You have no diagnostic credits remaining. Each report costs
                1 credit (&#8377;{CREDIT_PRICE_INR}). Purchase credits below
                in the Credits tab.
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            return

        st.markdown("""
        <div class="ae-section">Photograph</div>
        """, unsafe_allow_html=True)

        img_src = st.radio("Source", ["Camera", "Upload from Gallery"],
                           horizontal=True, label_visibility="collapsed")
        img = (st.camera_input(" ", label_visibility="collapsed")
               if img_src == "Camera"
               else st.file_uploader(
                   "Select image", type=["jpg","jpeg","png","webp"],
                   label_visibility="visible"
               ))

        if img:
            st.markdown('<div class="ae-section">Plant Details</div>',
                        unsafe_allow_html=True)
            plant_part = st.text_input(
                "Plant Part Affected",
                placeholder="e.g. Leaf / Capsule / Stem / Root"
            )
            symptoms = st.text_area(
                "Describe What You See",
                placeholder="When did you first notice this? Has it spread? Any recent weather events or chemical applications?",
                height=100
            )

            st.markdown(f"""
            <div class="ae-info" style="margin-top:0.8rem;">
                Submitting this report will use <strong>1 credit</strong>.
                You have <strong>{credits}</strong> remaining.
            </div>
            """, unsafe_allow_html=True)

            if st.button("Submit for Analysis", type="primary", key="submit_report"):
                with st.spinner("Running AI analysis — please wait..."):
                    try:
                        img_bytes  = img.getvalue()
                        fname      = getattr(img, 'name', 'img.jpg').lower()
                        media_type = ("image/png" if fname.endswith('.png')
                                      else "image/webp" if fname.endswith('.webp')
                                      else "image/jpeg")

                        result    = run_ai_diagnosis(
                            img_bytes, media_type, crop_type,
                            farm_name, st.session_state.farmer_name,
                            plant_part, symptoms, today.month
                        )
                        report_id = gen_id("RPT",
                                          f"{st.session_state.farmer_id}{today}")

                        new_rpt = pd.DataFrame([{
                            "Report_ID":       report_id,
                            "Submitted_At":    datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "Farmer_ID":       st.session_state.farmer_id,
                            "Farmer_Name":     st.session_state.farmer_name,
                            "Farm_ID":         st.session_state.farm_id or "",
                            "Farm_Name":       farm_name,
                            "Crop_Type":       crop_type,
                            "Plant_Part":      plant_part or "",
                            "Symptoms":        symptoms or "",
                            "AI_Condition":    result["condition"],
                            "AI_Severity":     result["severity"],
                            "AI_Confidence":   result["confidence"],
                            "AI_Findings":     result["observed"] + " " + result["cause"],
                            "AI_Treatment":    result["treatment"],
                            "AI_Spread_Risk":  result["spread"],
                            "AI_Expert_Note":  result["sci_note"],
                            "Status":          "Pending",
                            "Sci_Confirmed":   "",
                            "Sci_Recommendations": "",
                            "Sci_Medicines":   "",
                            "Sci_Follow_Up":   "",
                            "Sci_Next_Visit":  "",
                            "Reviewed_At":     "",
                            "Reviewed_By":     "",
                            "Credits_Charged": 1,
                        }])

                        existing = load_reports()
                        ok, err  = safe_update(
                            "Plant_Reports",
                            pd.concat([existing, new_rpt], ignore_index=True)
                        )
                        if ok:
                            deduct_credit(st.session_state.farmer_id,
                                          st.session_state.farmer_name,
                                          report_id)
                            st.session_state.last_report = {"id": report_id, **result}
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"Submission failed: {err}")

                    except Exception as e:
                        st.error(f"Analysis error: {e}")

        # Show last result
        if st.session_state.last_report:
            r  = st.session_state.last_report
            sc = {
                "Critical":"#c62828","High":"#e65100",
                "Medium":"#f9a825","Low":"#1a5c35"
            }.get(r.get("severity","Low"), "#6a8a76")
            badge = BADGE_CLASS.get(r.get("severity","Low"),"low")

            st.markdown(f"""
            <div class="ae-sep"></div>

            <div style="font-family:'IBM Plex Mono',monospace;font-size:0.68rem;
                        color:#8aaa96;letter-spacing:0.1em;margin-bottom:4px;">
                REPORT ID
            </div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:1.4rem;
                        font-weight:500;color:#0f2218;letter-spacing:1px;
                        margin-bottom:1.2rem;">
                {r.get('id','—')}
            </div>

            <div style="border:1px solid #e0e8e3;border-radius:4px;overflow:hidden;
                        margin-bottom:1rem;">
                <div style="background:{sc};padding:0.75rem 1rem;">
                    <div style="font-size:0.65rem;font-weight:600;letter-spacing:0.1em;
                                text-transform:uppercase;color:rgba(255,255,255,0.7);
                                margin-bottom:3px;">
                        AI ASSESSMENT — {r.get('confidence','')} CONFIDENCE
                    </div>
                    <div style="font-size:1.05rem;font-weight:600;color:#fff;">
                        {r.get('condition','—')}
                    </div>
                </div>
                <div style="padding:0.85rem 1rem;border-bottom:1px solid #f0f4f1;">
                    <div style="font-size:0.62rem;font-weight:600;letter-spacing:0.1em;
                                text-transform:uppercase;color:#8aaa96;margin-bottom:4px;">
                        OBSERVED
                    </div>
                    <div style="font-size:0.85rem;color:#2a2a2a;line-height:1.5;">
                        {r.get('observed','—')}
                    </div>
                </div>
                <div style="padding:0.85rem 1rem;border-bottom:1px solid #f0f4f1;
                            background:#fafcfb;">
                    <div style="font-size:0.62rem;font-weight:600;letter-spacing:0.1em;
                                text-transform:uppercase;color:#8aaa96;margin-bottom:4px;">
                        IMMEDIATE ACTION
                    </div>
                    <div style="font-size:0.9rem;font-weight:600;color:{sc};
                                line-height:1.4;">
                        {r.get('action','—')}
                    </div>
                </div>
                <div style="padding:0.85rem 1rem;">
                    <div style="font-size:0.62rem;font-weight:600;letter-spacing:0.1em;
                                text-transform:uppercase;color:#8aaa96;margin-bottom:4px;">
                        AI TREATMENT SUGGESTION
                    </div>
                    <div style="font-size:0.85rem;color:#1a3a26;font-weight:500;
                                line-height:1.5;">
                        {r.get('treatment','—')}
                    </div>
                </div>
            </div>

            <div class="ae-info">
                Report submitted to specialist queue. Check <strong>My Reports</strong>
                for expert recommendations.
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── MY REPORTS ────────────────────────────────────────────────────────
    with tab_reports:
        st.markdown('<div class="ae-content">', unsafe_allow_html=True)

        if st.button("Refresh", key="farmer_refresh"):
            st.cache_data.clear()
            st.rerun()

        reports_df = load_reports()
        if reports_df.empty:
            st.info("No reports submitted yet.")
        else:
            my = reports_df[
                reports_df["Farmer_ID"].astype(str) == str(st.session_state.farmer_id)
            ].sort_values("Submitted_At", ascending=False)

            if my.empty:
                st.info("You have not submitted any reports yet.")
            else:
                for _, rpt in my.iterrows():
                    rid     = clean(rpt.get("Report_ID"), "—")
                    ai_cond = clean(rpt.get("AI_Condition"), "—")
                    ai_sev  = clean(rpt.get("AI_Severity"), "Low")
                    status  = clean(rpt.get("Status"), "Pending")
                    sub_at  = clean(rpt.get("Submitted_At"), "—")
                    sc      = {"Critical":"#c62828","High":"#e65100",
                               "Medium":"#f9a825","Low":"#1a5c35"}.get(ai_sev,"#6a8a76")
                    badge   = BADGE_CLASS.get(ai_sev,"low")
                    st_badge= STATUS_BADGE.get(status,"pending")

                    with st.expander(f"{rid}  —  {ai_cond}  [{status}]"):
                        st.markdown(f"""
                        <div style="display:flex;justify-content:space-between;
                                    align-items:flex-start;margin-bottom:0.6rem;">
                            <div>
                                <div style="font-size:0.95rem;font-weight:600;
                                            color:{sc};">{ai_cond}</div>
                                <div style="font-size:0.7rem;color:#8aaa96;
                                            font-family:'IBM Plex Mono',monospace;
                                            margin-top:2px;">{sub_at}</div>
                            </div>
                            <div>
                                <span class="badge badge-{badge}">{ai_sev}</span>
                                &nbsp;
                                <span class="badge badge-{st_badge}">{status}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        ai_treat = clean(rpt.get("AI_Treatment"), "")
                        if ai_treat and ai_treat != "—":
                            st.markdown(f"""
                            <div class="ae-card">
                                <div class="ae-card-label">AI Treatment Suggestion</div>
                                <div class="ae-card-value">{ai_treat}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        # Scientist response
                        if status in ("Responded", "Closed"):
                            sci_by   = clean(rpt.get("Reviewed_By"), "Specialist")
                            rev_at   = clean(rpt.get("Reviewed_At"), "")
                            confirmed= clean(rpt.get("Sci_Confirmed"), "—")
                            recs     = clean(rpt.get("Sci_Recommendations"), "—")
                            meds     = clean(rpt.get("Sci_Medicines"), "")
                            followup = clean(rpt.get("Sci_Follow_Up"), "")
                            nxt      = clean(rpt.get("Sci_Next_Visit"), "")

                            st.markdown(f"""
                            <div class="ae-sep"></div>
                            <div style="font-size:0.62rem;font-weight:600;
                                        letter-spacing:0.1em;text-transform:uppercase;
                                        color:#1a5c35;margin-bottom:0.5rem;">
                                Specialist Response — {sci_by}
                                <span style="color:#8aaa96;font-weight:400;">
                                  &nbsp;{rev_at}
                                </span>
                            </div>
                            <div class="ae-card" style="border-left:3px solid #1a5c35;">
                                <div class="ae-card-label">Confirmed Diagnosis</div>
                                <div class="ae-card-value">{confirmed}</div>
                            </div>
                            <div class="ae-card">
                                <div class="ae-card-label">Recommendations</div>
                                <div class="ae-card-value">{recs}</div>
                            </div>
                            {"<div class='ae-card'><div class='ae-card-label'>Medicines</div><div class='ae-card-value'>" + meds + "</div></div>" if meds and meds != "—" else ""}
                            {"<div class='ae-card'><div class='ae-card-label'>Follow-up</div><div class='ae-card-value'>" + followup + (" — Next visit: " + nxt if nxt and nxt != "—" else "") + "</div></div>" if followup and followup != "—" else ""}
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="background:#fff8e8;border:1px solid #e8d888;
                                        border-radius:3px;padding:0.75rem 1rem;
                                        font-size:0.82rem;color:#7a6000;
                                        margin-top:0.4rem;">
                                Awaiting specialist review. Reports are typically
                                reviewed within 24 hours.
                            </div>
                            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── CREDITS ───────────────────────────────────────────────────────────
    with tab_credits:
        st.markdown('<div class="ae-content">', unsafe_allow_html=True)

        current_credits = get_farmer_credits(st.session_state.farmer_id)

        # Current balance
        bal_color = "#c62828" if current_credits == 0 else (
                    "#f9a825" if current_credits <= 2 else "#1a5c35")
        st.markdown(f"""
        <div style="text-align:center;padding:2rem 1rem;background:#fff;
                    border:1px solid #e0e8e3;border-radius:4px;margin-bottom:1.2rem;">
            <div style="font-size:0.65rem;font-weight:600;letter-spacing:0.12em;
                        text-transform:uppercase;color:#8aaa96;margin-bottom:6px;">
                Current Balance
            </div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:3rem;
                        font-weight:500;color:{bal_color};line-height:1;">
                {current_credits}
            </div>
            <div style="font-size:0.75rem;color:#8aaa96;margin-top:4px;">
                diagnostic credit{"s" if current_credits != 1 else ""}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Pricing (currently free tier note)
        st.markdown("""
        <div style="background:#e8f5ed;border:1px solid #a8d8b8;border-radius:4px;
                    padding:0.9rem 1rem;margin-bottom:1.2rem;">
            <div style="font-size:0.72rem;font-weight:600;letter-spacing:0.08em;
                        text-transform:uppercase;color:#1a5c35;margin-bottom:4px;">
                Currently Free
            </div>
            <div style="font-size:0.82rem;color:#1a3a26;line-height:1.5;">
                AgriExpert is currently free during our launch phase.
                Each new registration receives 3 free credits.
                Additional credits will be available at
                &#8377;99 per credit when paid tier launches.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Pricing card (visible, purchase disabled in free phase)
        st.markdown(f"""
        <div class="price-card">
            <div class="price-header">
                <div class="price-plan">Diagnostic Credit</div>
                <div class="price-amount">&#8377;{CREDIT_PRICE_INR}</div>
                <div class="price-unit">per diagnostic report</div>
            </div>
            <div class="price-body">
                <div class="price-feature">
                    AI image analysis
                    <span class="price-check">Included</span>
                </div>
                <div class="price-feature">
                    Specialist review
                    <span class="price-check">Included</span>
                </div>
                <div class="price-feature">
                    Written recommendations
                    <span class="price-check">Included</span>
                </div>
                <div class="price-feature">
                    Medicine guidance
                    <span class="price-check">Included</span>
                </div>
                <div class="price-feature">
                    Report stored permanently
                    <span class="price-check">Included</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.button("Purchase Credits — Coming Soon",
                  key="buy_credits", disabled=True)

        # Transaction history
        txn_df = load_transactions()
        if not txn_df.empty:
            my_txns = txn_df[
                txn_df["Farmer_ID"].astype(str) == str(st.session_state.farmer_id)
            ].sort_values("Timestamp", ascending=False)

            if not my_txns.empty:
                st.markdown('<div class="ae-section">Transaction History</div>',
                            unsafe_allow_html=True)
                for _, t in my_txns.head(10).iterrows():
                    txn_type = clean(t.get("Type"), "—")
                    credits  = clean(t.get("Credits"), "0")
                    ts       = clean(t.get("Timestamp"), "—")
                    notes    = clean(t.get("Notes"), "—")
                    color    = "#1a5c35" if txn_type == "Credit" else "#c25900"
                    sign     = "+" if txn_type == "Credit" else ""
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;
                                align-items:center;padding:0.6rem 0;
                                border-bottom:1px solid #f0f4f1;font-size:0.82rem;">
                        <div>
                            <div style="color:#1a1a1a;font-weight:500;">{notes}</div>
                            <div style="color:#8aaa96;font-size:0.68rem;
                                        font-family:'IBM Plex Mono',monospace;">
                                {ts}
                            </div>
                        </div>
                        <div style="font-family:'IBM Plex Mono',monospace;
                                    font-weight:600;color:{color};">
                            {sign}{credits}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
