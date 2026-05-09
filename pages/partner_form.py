"""Octa Partner Network — Add / Edit Partner Form."""
import streamlit as st
from datetime import datetime
from modules.auth import require_auth
from modules.sso import auto_login_from_url
from modules.ui_helpers import inject_css, sidebar_nav, page_header, section_label, DARK
from modules.database import (get_partner_by_id, upsert_partner,
                               get_contacts, upsert_contact, delete_contact)
from config import COUNTRIES, PARTNER_TYPES, DARK as D

st.set_page_config(page_title="Partner Form — Octa",
                   page_icon="✏️", layout="wide",
                   initial_sidebar_state="expanded")
inject_css()
auto_login_from_url()
require_auth()
sidebar_nav()

# ── Load existing partner if editing ─────────────────────────────────────────
edit_id = st.session_state.get("edit_partner_id")
p = get_partner_by_id(edit_id) if edit_id else {}
is_edit = bool(p)

page_header(
    "Edit Partner" if is_edit else "Add New Partner",
    p.get("full_name","") if is_edit else "Fill in all available information",
    "✏️" if is_edit else "➕"
)

if st.button("← Back to Partners"):
    st.switch_page("pages/partner_list.py")

def _v(field, default=""):
    return p.get(field, default) if p else default

# ═════════════════════════════════════════════════════════════════════════════
# TABS
# ═════════════════════════════════════════════════════════════════════════════
tab_general, tab_bank, tab_social, tab_contacts = st.tabs(
    ["📋 General Info", "🏦 Bank Details", "📱 Social Media", "👥 Contacts"]
)

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — General Info
# ════════════════════════════════════════════════════════════════════════════
with tab_general:
    section_label("Basic Information")
    g1, g2 = st.columns(2)
    with g1:
        full_name  = st.text_input("Full Name *", value=_v("full_name"),
                                    placeholder="University of Rome La Sapienza",
                                    key="f_fullname")
    with g2:
        short_name = st.text_input("Short Name / Acronym",
                                    value=_v("short_name"),
                                    placeholder="UniRomeSap",
                                    key="f_shortname")

    g3, g4 = st.columns(2)
    with g3:
        # Country dropdown
        current_country = _v("country","")
        country_idx = COUNTRIES.index(current_country) if current_country in COUNTRIES else 0
        country = st.selectbox("Country *", COUNTRIES, index=country_idx, key="f_country")
    with g4:
        current_type = _v("partner_type","Other")
        type_idx = PARTNER_TYPES.index(current_type) if current_type in PARTNER_TYPES else len(PARTNER_TYPES)-1
        partner_type = st.selectbox("Partner Type *", PARTNER_TYPES,
                                     index=type_idx, key="f_type")

    g5, g6, g7 = st.columns(3)
    with g5:
        website = st.text_input("Website", value=_v("website"),
                                 placeholder="https://www.example.com", key="f_web")
    with g6:
        email   = st.text_input("General Email", value=_v("email"),
                                 placeholder="contact@example.com", key="f_email")
    with g7:
        phone   = st.text_input("Phone", value=_v("phone"),
                                 placeholder="+39 06 1234567", key="f_phone")

    address = st.text_input("Address", value=_v("address"),
                              placeholder="Via Example 1, Rome, Italy", key="f_address")

    section_label("Logo")
    st.caption("Paste a public URL to the partner's logo (Google Drive, website, etc.)")
    logo_url = st.text_input("Logo URL", value=_v("logo_url"),
                               placeholder="https://drive.google.com/...", key="f_logo")
    if logo_url:
        try:
            st.image(logo_url, width=150)
        except Exception:
            st.caption("⚠️ Could not preview image — URL may not be publicly accessible.")

    section_label("Description / Notes")
    description = st.text_area("Notes", value=_v("description"), height=100,
                                placeholder="Any additional notes about this partner…",
                                key="f_desc")

    status_opts = ["active","inactive","prospect"]
    cur_status  = _v("status","active")
    status_idx  = status_opts.index(cur_status) if cur_status in status_opts else 0
    status = st.selectbox("Status", status_opts, index=status_idx, key="f_status")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Save General Info", type="primary", key="save_general"):
        if not full_name.strip():
            st.error("❌ Full name is required.")
        else:
            data = {
                "full_name":    full_name.strip(),
                "short_name":   short_name.strip(),
                "country":      country,
                "partner_type": partner_type,
                "website":      website.strip(),
                "email":        email.strip(),
                "phone":        phone.strip(),
                "address":      address.strip(),
                "logo_url":     logo_url.strip(),
                "description":  description.strip(),
                "status":       status,
            }
            if edit_id:
                data["id"] = edit_id
            ok, result = upsert_partner(data)
            if ok:
                st.success("✅ Partner saved!")
                if not edit_id:
                    st.session_state["edit_partner_id"] = result
                    st.rerun()
            else:
                st.error(f"❌ {result}")

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — Bank Details
# ════════════════════════════════════════════════════════════════════════════
with tab_bank:
    if not edit_id:
        st.info("💡 Save General Info first, then you can add bank details.")
    else:
        section_label("Banking Information")
        st.caption("This information is confidential — only accessible to authorised users.")
        b1, b2 = st.columns(2)
        with b1:
            bank_name    = st.text_input("Bank Name", value=_v("bank_name"),
                                          placeholder="Deutsche Bank", key="b_bankname")
            bank_account = st.text_input("Account Number", value=_v("bank_account"),
                                          key="b_account")
        with b2:
            iban = st.text_input("IBAN", value=_v("iban"),
                                  placeholder="DE12 3456 7890 1234 5678 90", key="b_iban")
            bic  = st.text_input("BIC / SWIFT", value=_v("bic"),
                                  placeholder="DEUTDEDB", key="b_bic")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Save Bank Details", type="primary", key="save_bank"):
            ok, result = upsert_partner({
                "id": edit_id,
                "bank_name":    bank_name.strip(),
                "bank_account": bank_account.strip(),
                "iban":         iban.strip(),
                "bic":          bic.strip(),
            })
            if ok: st.success("✅ Bank details saved!")
            else:  st.error(f"❌ {result}")

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — Social Media
# ════════════════════════════════════════════════════════════════════════════
with tab_social:
    if not edit_id:
        st.info("💡 Save General Info first, then you can add social media accounts.")
    else:
        section_label("Social Media Handles")
        st.caption("Enter handles as @handle — used to tag the partner when posting on social media.")

        SOCIALS = [
            ("Facebook",  "facebook",  "📘", "@FacebookPageName"),
            ("LinkedIn",  "linkedin",  "💼", "@LinkedInCompany"),
            ("Twitter/X", "twitter",   "🐦", "@TwitterHandle"),
            ("YouTube",   "youtube",   "▶️", "@YouTubeChannel"),
            ("Instagram", "instagram", "📸", "@InstagramHandle"),
        ]

        social_vals = {}
        sc1, sc2 = st.columns(2)
        for i, (label, key, icon, placeholder) in enumerate(SOCIALS):
            col = sc1 if i % 2 == 0 else sc2
            with col:
                social_vals[key] = st.text_input(
                    f"{icon} {label}", value=_v(key),
                    placeholder=placeholder, key=f"s_{key}"
                )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Save Social Media", type="primary", key="save_social"):
            data = {"id": edit_id}
            data.update({k: v.strip() for k, v in social_vals.items()})
            ok, result = upsert_partner(data)
            if ok: st.success("✅ Social media accounts saved!")
            else:  st.error(f"❌ {result}")

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — Contacts
# ════════════════════════════════════════════════════════════════════════════
with tab_contacts:
    if not edit_id:
        st.info("💡 Save General Info first, then you can add contacts.")
    else:
        contacts = get_contacts(edit_id)
        section_label(f"Contacts ({len(contacts)})")

        # Existing contacts
        for c in contacts:
            cid   = c["id"]
            cname = f"{c.get('first_name','')} {c.get('last_name','')}".strip()
            cpos  = c.get("position","")
            bg2   = D["bg2"]; border = D["border"]; muted_c = D["muted"]

            with st.expander(f"👤 {cname}" + (f" — {cpos}" if cpos else ""), expanded=False):
                cc1,cc2,cc3 = st.columns(3)
                fn = cc1.text_input("First Name", value=c.get("first_name",""), key=f"c_fn_{cid}")
                ln = cc2.text_input("Last Name",  value=c.get("last_name",""),  key=f"c_ln_{cid}")
                ps = cc3.text_input("Position",   value=c.get("position",""),   key=f"c_ps_{cid}")
                cc4,cc5 = st.columns(2)
                em = cc4.text_input("Email",  value=c.get("email",""),  key=f"c_em_{cid}")
                mo = cc5.text_input("Mobile", value=c.get("mobile",""), key=f"c_mo_{cid}")

                st.markdown("**Social media handles:**")
                sc1c,sc2c,sc3c = st.columns(3)
                li = sc1c.text_input("LinkedIn",  value=c.get("linkedin",""),  key=f"c_li_{cid}", placeholder="@handle")
                tw = sc2c.text_input("Twitter",   value=c.get("twitter",""),   key=f"c_tw_{cid}", placeholder="@handle")
                fb = sc3c.text_input("Facebook",  value=c.get("facebook",""),  key=f"c_fb_{cid}", placeholder="@handle")

                no = st.text_input("Notes", value=c.get("notes",""), key=f"c_no_{cid}")

                ba1,ba2,_ = st.columns([1,1,4])
                with ba1:
                    if st.button("💾 Save", key=f"c_save_{cid}", type="primary",
                                 use_container_width=True):
                        ok, res = upsert_contact({
                            "id": cid, "partner_id": edit_id,
                            "first_name": fn.strip(), "last_name": ln.strip(),
                            "position": ps.strip(), "email": em.strip(),
                            "mobile": mo.strip(), "linkedin": li.strip(),
                            "twitter": tw.strip(), "facebook": fb.strip(),
                            "notes": no.strip(),
                        })
                        if ok: st.success("Saved!")
                        else:  st.error(f"Error: {res}")
                with ba2:
                    if st.button("🗑 Delete", key=f"c_del_{cid}", use_container_width=True):
                        ok, msg = delete_contact(cid)
                        if ok:
                            st.success("Deleted.")
                            st.rerun()
                        else:
                            st.error(msg)

        # ── Add new contact ───────────────────────────────────────────────────
        section_label("➕ Add New Contact")
        with st.expander("New contact", expanded=False):
            na1,na2,na3 = st.columns(3)
            n_fn = na1.text_input("First Name *", key="nc_fn")
            n_ln = na2.text_input("Last Name *",  key="nc_ln")
            n_ps = na3.text_input("Position",     key="nc_ps")
            na4,na5 = st.columns(2)
            n_em = na4.text_input("Email",  key="nc_em")
            n_mo = na5.text_input("Mobile", key="nc_mo")

            st.markdown("**Social media:**")
            ns1,ns2,ns3 = st.columns(3)
            n_li = ns1.text_input("LinkedIn",  key="nc_li", placeholder="@handle")
            n_tw = ns2.text_input("Twitter",   key="nc_tw", placeholder="@handle")
            n_fb = ns3.text_input("Facebook",  key="nc_fb", placeholder="@handle")
            n_no = st.text_input("Notes", key="nc_no")

            if st.button("➕ Add Contact", type="primary", key="nc_add"):
                if not n_fn.strip() and not n_ln.strip():
                    st.error("❌ Please enter at least a first or last name.")
                else:
                    ok, res = upsert_contact({
                        "partner_id": edit_id,
                        "first_name": n_fn.strip(), "last_name": n_ln.strip(),
                        "position":   n_ps.strip(), "email":     n_em.strip(),
                        "mobile":     n_mo.strip(), "linkedin":  n_li.strip(),
                        "twitter":    n_tw.strip(), "facebook":  n_fb.strip(),
                        "notes":      n_no.strip(),
                    })
                    if ok:
                        st.success("✅ Contact added!")
                        st.rerun()
                    else:
                        st.error(f"❌ {res}")
