"""AgriExpert — Admin Portal"""

import streamlit as st
import pandas as pd
from datetime import datetime
from data import (
    clean, gen_id, safe_update, add_credits,
    load_farms, load_farmers, load_scientists, load_reports,
    load_transactions, load_crop_types,
    CREDIT_PRICE_INR, FREE_CREDITS
)

ADMIN_PIN = st.secrets.get("admin", {}).get("pin", "admin123")


def show_admin():
    if st.button("Back to Home", key="admin_back"):
        st.session_state.role = None
        st.rerun()

    st.markdown("""
    <div class="ae-header">
        <div class="ae-header-nav">AgriExpert / Administrator</div>
        <div class="ae-header-title">Admin Portal</div>
        <div class="ae-header-sub">Platform management · Farms · Scientists · Credits</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ae-content">', unsafe_allow_html=True)
    pin = st.text_input("Administrator PIN", type="password",
                        placeholder="Enter PIN", label_visibility="visible",
                        key="admin_pin")
    st.markdown('</div>', unsafe_allow_html=True)

    if pin != ADMIN_PIN:
        if pin:
            st.error("Incorrect PIN.")
        return

    st.markdown("""
    <div style="background:#e8f5ed;border-top:3px solid #1a5c35;
                padding:0.6rem 1.4rem;font-size:0.8rem;color:#0f3320;
                font-weight:500;">
        Administrator access granted.
    </div>
    """, unsafe_allow_html=True)

    tab_ov, tab_farms, tab_sci, tab_credits, tab_crops = st.tabs([
        "Overview", "Farms", "Scientists", "Credits", "Crop Types"
    ])

    # ── OVERVIEW ──────────────────────────────────────────────────────────
    with tab_ov:
        farms_df   = load_farms()
        farmers_df = load_farmers()
        sci_df     = load_scientists()
        reports_df = load_reports()
        txn_df     = load_transactions()

        n_farms   = len(farms_df)   if not farms_df.empty   else 0
        n_farmers = len(farmers_df) if not farmers_df.empty else 0
        n_sci     = len(sci_df)     if not sci_df.empty     else 0
        n_rpts    = len(reports_df) if not reports_df.empty else 0
        n_pend    = len(reports_df[reports_df["Status"]=="Pending"]) if not reports_df.empty else 0
        n_crit    = len(reports_df[reports_df["AI_Severity"]=="Critical"]) if not reports_df.empty else 0

        st.markdown('<div class="ae-content">', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ae-metrics">
            <div class="ae-metric">
                <div class="ae-metric-val">{n_farms}</div>
                <div class="ae-metric-label">Farms</div>
            </div>
            <div class="ae-metric">
                <div class="ae-metric-val">{n_farmers}</div>
                <div class="ae-metric-label">Farmers</div>
            </div>
            <div class="ae-metric">
                <div class="ae-metric-val">{n_sci}</div>
                <div class="ae-metric-label">Scientists</div>
            </div>
        </div>
        <div class="ae-metrics">
            <div class="ae-metric">
                <div class="ae-metric-val">{n_rpts}</div>
                <div class="ae-metric-label">Reports</div>
            </div>
            <div class="ae-metric">
                <div class="ae-metric-val" style="color:#e65100;">{n_pend}</div>
                <div class="ae-metric-label">Pending</div>
            </div>
            <div class="ae-metric">
                <div class="ae-metric-val" style="color:#c62828;">{n_crit}</div>
                <div class="ae-metric-label">Critical</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Revenue summary
        if not txn_df.empty:
            paid = txn_df[txn_df["Type"] == "Credit"]
            total_credits_sold = paid["Credits"].astype(float).sum() if not paid.empty else 0
            total_revenue      = paid["Amount_INR"].astype(float).sum() if not paid.empty else 0

            st.markdown('<div class="ae-section">Revenue</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="ae-metrics">
                <div class="ae-metric">
                    <div class="ae-metric-val">{int(total_credits_sold)}</div>
                    <div class="ae-metric-label">Credits Sold</div>
                </div>
                <div class="ae-metric">
                    <div class="ae-metric-val" style="color:#1a5c35;">
                        &#8377;{total_revenue:,.0f}
                    </div>
                    <div class="ae-metric-label">Revenue</div>
                </div>
                <div class="ae-metric">
                    <div class="ae-metric-val">
                        &#8377;{CREDIT_PRICE_INR}
                    </div>
                    <div class="ae-metric-label">Per Credit</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Reports by crop
        if not reports_df.empty and "Crop_Type" in reports_df.columns:
            st.markdown('<div class="ae-section">Reports by Crop</div>',
                        unsafe_allow_html=True)
            st.bar_chart(
                reports_df["Crop_Type"].value_counts().rename("Reports"),
                height=160, color="#1a5c35"
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # ── FARMS ─────────────────────────────────────────────────────────────
    with tab_farms:
        farms_df   = load_farms()
        crop_types = load_crop_types()
        st.markdown('<div class="ae-content">', unsafe_allow_html=True)

        with st.expander("Register New Farm"):
            with st.form("add_farm", clear_on_submit=True):
                f1, f2 = st.columns(2)
                fn     = f1.text_input("Farm Name")
                owner  = f2.text_input("Owner Name")
                loc    = f1.text_input("Village / Location")
                dist   = f2.text_input("District")
                state  = f1.text_input("State", value="Kerala")
                crop   = f2.selectbox("Primary Crop", crop_types)
                acre   = f1.number_input("Acreage (acres)", min_value=0.0,
                                          step=0.1, format="%.2f")
                phone  = f2.text_input("Owner Phone")

                if st.form_submit_button("Register Farm", type="primary"):
                    if not fn.strip() or not owner.strip():
                        st.error("Farm name and owner name are required.")
                    else:
                        new_farm = pd.DataFrame([{
                            "Farm_ID":       gen_id("FARM", fn),
                            "Farm_Name":     fn.strip(),
                            "Owner_Name":    owner.strip(),
                            "Location":      loc.strip(),
                            "District":      dist.strip(),
                            "State":         state.strip(),
                            "Crop_Type":     crop,
                            "Acreage":       acre,
                            "Phone":         phone.strip(),
                            "Registered_At": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        }])
                        ok, err = safe_update(
                            "Farms",
                            pd.concat([farms_df, new_farm], ignore_index=True)
                        )
                        if ok:
                            st.success(f"{fn} registered.")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"Failed: {err}")

        if not farms_df.empty:
            st.markdown('<div class="ae-section">Registered Farms</div>',
                        unsafe_allow_html=True)
            cols = [c for c in ["Farm_Name","Owner_Name","Crop_Type","Location","Acreage"]
                    if c in farms_df.columns]
            st.dataframe(farms_df[cols], use_container_width=True, hide_index=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── SCIENTISTS ────────────────────────────────────────────────────────
    with tab_sci:
        sci_df     = load_scientists()
        crop_types = load_crop_types()
        st.markdown('<div class="ae-content">', unsafe_allow_html=True)

        with st.expander("Register Scientist"):
            with st.form("add_sci", clear_on_submit=True):
                s1, s2 = st.columns(2)
                s_name = s1.text_input("Full Name")
                s_qual = s2.text_input("Qualification", placeholder="PhD / MSc")
                s_spec = s1.text_input("Specialization", placeholder="Plant Pathology")
                s_inst = s2.text_input("Institution")
                s_crops= st.multiselect("Crops", crop_types)
                s_phone= s1.text_input("Phone Number")
                s_pin  = s2.text_input("Set Login PIN", max_chars=6,
                                        placeholder="6-digit PIN")

                if st.form_submit_button("Register Scientist", type="primary"):
                    if not s_name.strip() or not s_phone.strip() or not s_pin.strip():
                        st.error("Name, phone, and PIN are required.")
                    elif len(s_pin.strip()) < 4:
                        st.error("PIN must be at least 4 digits.")
                    else:
                        new_sci = pd.DataFrame([{
                            "Sci_ID":          gen_id("SCI", s_phone),
                            "Name":            s_name.strip(),
                            "Qualification":   s_qual.strip(),
                            "Specialization":  s_spec.strip(),
                            "Crops":           ", ".join(s_crops),
                            "Institution":     s_inst.strip(),
                            "Phone":           s_phone.strip(),
                            "PIN":             s_pin.strip(),
                            "Is_Active":       True,
                            "Reports_Reviewed":0,
                            "Registered_At":   datetime.now().strftime("%Y-%m-%d %H:%M"),
                        }])
                        ok, err = safe_update(
                            "Scientists",
                            pd.concat([sci_df, new_sci], ignore_index=True)
                        )
                        if ok:
                            st.success(f"{s_name} registered.")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"Failed: {err}")

        if not sci_df.empty:
            st.markdown('<div class="ae-section">Registered Scientists</div>',
                        unsafe_allow_html=True)
            cols = [c for c in ["Name","Specialization","Crops","Institution","Is_Active"]
                    if c in sci_df.columns]
            st.dataframe(sci_df[cols], use_container_width=True, hide_index=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── CREDITS ───────────────────────────────────────────────────────────
    with tab_credits:
        farmers_df = load_farmers()
        txn_df     = load_transactions()
        st.markdown('<div class="ae-content">', unsafe_allow_html=True)

        st.markdown('<div class="ae-section">Add Credits to Farmer</div>',
                    unsafe_allow_html=True)

        if not farmers_df.empty:
            farmer_names = farmers_df["Name"].tolist() if "Name" in farmers_df.columns else []
            with st.form("add_cred", clear_on_submit=True):
                sel_farmer = st.selectbox("Select Farmer", farmer_names)
                cr1, cr2   = st.columns(2)
                num_credits= cr1.number_input("Credits to Add", min_value=1,
                                               max_value=100, step=1, value=1)
                amount_paid= cr2.number_input(
                    f"Amount Received (Rs.)",
                    min_value=0.0, step=float(CREDIT_PRICE_INR),
                    value=float(num_credits * CREDIT_PRICE_INR),
                    format="%.0f"
                )
                cr_notes = st.text_input("Notes", value="Manual top-up")

                if st.form_submit_button("Add Credits", type="primary"):
                    farmer_row = farmers_df[farmers_df["Name"] == sel_farmer]
                    if farmer_row.empty:
                        st.error("Farmer not found.")
                    else:
                        fid  = clean(farmer_row.iloc[0].get("Farmer_ID"))
                        fname= clean(farmer_row.iloc[0].get("Name"))
                        ok   = add_credits(fid, fname, num_credits,
                                           amount_paid, cr_notes)
                        if ok:
                            st.success(f"{num_credits} credit(s) added to {fname}.")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error("Failed to add credits.")

            # Credit balances
            st.markdown('<div class="ae-section">Farmer Credit Balances</div>',
                        unsafe_allow_html=True)
            cols = [c for c in ["Name","Farm_Name","Credits","Phone"]
                    if c in farmers_df.columns]
            st.dataframe(
                farmers_df[cols].sort_values("Credits", ascending=True),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("No farmers registered yet.")

        # Transaction log
        if not txn_df.empty:
            st.markdown('<div class="ae-section">Transaction Log</div>',
                        unsafe_allow_html=True)
            cols = [c for c in ["Timestamp","Farmer_Name","Type","Credits",
                                 "Amount_INR","Notes"]
                    if c in txn_df.columns]
            st.dataframe(
                txn_df[cols].sort_values("Timestamp", ascending=False).head(50),
                use_container_width=True, hide_index=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # ── CROP TYPES ────────────────────────────────────────────────────────
    with tab_crops:
        crop_types = load_crop_types()
        st.markdown('<div class="ae-content">', unsafe_allow_html=True)
        st.markdown('<div class="ae-section">Registered Crop Types</div>',
                    unsafe_allow_html=True)
        for c in crop_types:
            st.markdown(f"""
            <div style="padding:0.5rem 0;border-bottom:1px solid #f0f4f1;
                        font-size:0.85rem;color:#1a1a1a;">{c}</div>
            """, unsafe_allow_html=True)

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        with st.form("add_crop", clear_on_submit=True):
            new_crop = st.text_input("Add New Crop Type")
            if st.form_submit_button("Add", type="primary"):
                if not new_crop.strip():
                    st.error("Enter crop name.")
                else:
                    try:
                        df = st.connection("gsheets").read(
                            spreadsheet=st.secrets["gsheets"]["spreadsheet"],
                            worksheet="Crop_Types", ttl=0
                        )
                        df.columns = df.columns.str.strip()
                    except:
                        df = pd.DataFrame(columns=["Crop_Name"])
                    ok, err = safe_update(
                        "Crop_Types",
                        pd.concat([df, pd.DataFrame([{"Crop_Name": new_crop.strip()}])],
                                  ignore_index=True)
                    )
                    if ok:
                        st.success(f"{new_crop} added.")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Failed: {err}")

        st.markdown('</div>', unsafe_allow_html=True)
