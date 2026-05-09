"""Octa Partner Network — Partner List & Detail View."""
import streamlit as st
from modules.auth import require_auth
from modules.sso import auto_login_from_url
from modules.ui_helpers import inject_css, sidebar_nav, page_header, section_label, DARK
from modules.database import get_all_partners, get_partner_by_id, get_contacts
from config import DARK as D, COLOR_FUNDED, COLOR_PROPOSAL

st.set_page_config(page_title="Partners — Octa Partner Network",
                   page_icon="🤝", layout="wide",
                   initial_sidebar_state="expanded")
inject_css()
auto_login_from_url()
require_auth()
sidebar_nav()

page_header("Partner Directory", "Search, browse and view all partners", "🤝")

partners = get_all_partners()

if not partners:
    st.info("No partners yet. Use **Add Partner** to get started.")
    st.stop()

# ── Search & filters ──────────────────────────────────────────────────────────
fc1, fc2, fc3 = st.columns(3)
with fc1:
    search = st.text_input("🔍 Search by name, country, type",
                            placeholder="Type to filter…", key="p_search")
with fc2:
    types = ["All types"] + sorted(set(p.get("partner_type","") for p in partners if p.get("partner_type")))
    f_type = st.selectbox("Partner type", types, key="p_type")
with fc3:
    countries = ["All countries"] + sorted(set(p.get("country","") for p in partners if p.get("country")))
    f_country = st.selectbox("Country", countries, key="p_country")

filtered = partners
if search:
    q = search.lower()
    filtered = [p for p in filtered if
        q in (p.get("full_name","") or "").lower() or
        q in (p.get("short_name","") or "").lower() or
        q in (p.get("country","") or "").lower() or
        q in (p.get("partner_type","") or "").lower()]
if f_type != "All types":
    filtered = [p for p in filtered if p.get("partner_type") == f_type]
if f_country != "All countries":
    filtered = [p for p in filtered if p.get("country") == f_country]

muted_c = D["muted"]
st.markdown(
    f"<p style='color:{muted_c};font-size:0.84rem'>"
    f"<strong style='color:{D['text']}'>{len(filtered)}</strong> of "
    f"{len(partners)} partners</p>",
    unsafe_allow_html=True
)

# Auto-open from map click
if "view_partner_id" in st.session_state:
    st.session_state["open_partner_id"] = st.session_state.pop("view_partner_id")

# ── Partner cards grid ────────────────────────────────────────────────────────
PTYPE_COLORS = {
    "HEI":                    D["accent"],
    "Business":               D["accent2"],
    "NGO":                    D["success"],
    "Governmental Institute": D["warning"],
    "Research Centre":        "#9b59b6",
    "Other":                  D["muted"],
}

cols = st.columns(3)
for i, p in enumerate(filtered):
    pid    = p["id"]
    name   = p.get("full_name","") or p.get("short_name","")
    sname  = p.get("short_name","")
    ptype  = p.get("partner_type","")
    country= p.get("country","")
    logo   = p.get("logo_url","")
    website= p.get("website","")
    color  = PTYPE_COLORS.get(ptype, D["muted"])
    bg2    = D["bg2"]; border = D["border"]

    with cols[i % 3]:
        st.markdown(
            f"<div style='background:{bg2};border:1px solid {border};"
            f"border-top:3px solid {color};border-radius:12px;"
            f"padding:1rem;margin-bottom:0.6rem;min-height:120px'>"
            + (f"<img src='{logo}' style='height:40px;margin-bottom:0.5rem;"
               f"object-fit:contain;display:block'>" if logo else "")
            + f"<div style='font-weight:700;color:{D['text']};font-size:0.95rem'>{name}</div>"
            f"<div style='color:{muted_c};font-size:0.78rem;margin-top:0.2rem'>"
            f"{sname + ' · ' if sname and sname != name else ''}{country}</div>"
            f"<span style='background:{color}22;color:{color};border:1px solid {color}44;"
            f"padding:2px 8px;border-radius:10px;font-size:0.72rem;font-weight:600;"
            f"display:inline-block;margin-top:0.4rem'>{ptype}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
        if st.button("👁 View Details", key=f"view_{pid}", use_container_width=True):
            st.session_state["open_partner_id"] = pid
            st.rerun()

# ── Partner detail panel ──────────────────────────────────────────────────────
open_id = st.session_state.get("open_partner_id")
if open_id:
    p = get_partner_by_id(open_id)
    if not p:
        st.warning("Partner not found.")
        st.session_state.pop("open_partner_id", None)
    else:
        st.markdown("---")
        name   = p.get("full_name","") or p.get("short_name","")
        ptype  = p.get("partner_type","")
        color  = PTYPE_COLORS.get(ptype, D["muted"])
        logo   = p.get("logo_url","")
        accent = D["accent"]

        # Header
        hc1, hc2 = st.columns([5,1])
        with hc1:
            st.markdown(
                f"<h2 style='color:{D['text']};margin-bottom:0.2rem'>"
                + (f"<img src='{logo}' style='height:50px;vertical-align:middle;"
                   f"margin-right:0.8rem;object-fit:contain'>" if logo else "")
                + f"{name}</h2>"
                f"<span style='background:{color}22;color:{color};border:1px solid {color}44;"
                f"padding:3px 12px;border-radius:12px;font-size:0.82rem;font-weight:600'>"
                f"{ptype}</span>"
                f"{p.get('country','')}</span>",
                unsafe_allow_html=True
            )
        with hc2:
            if st.button("✏️ Edit Partner", key="det_edit", type="primary"):
                st.session_state["edit_partner_id"] = open_id
                st.switch_page("pages/partner_form.py")
            if st.button("✖ Close", key="det_close"):
                st.session_state.pop("open_partner_id", None)
                st.rerun()

        tab_info, tab_bank, tab_social, tab_contacts = st.tabs(
            ["📋 General Info", "🏦 Bank Details", "📱 Social Media", "👥 Contacts"]
        )

        with tab_info:
            r1,r2,r3 = st.columns(3)
            r1.markdown(f"**Full Name:** {p.get('full_name','—')}")
            r2.markdown(f"**Short Name:** {p.get('short_name','—')}")
            r3.markdown(f"**Type:** {ptype}")
            r1.markdown(f"**Country:** {p.get('country','—')}")
            r2.markdown(f"**Status:** {p.get('status','—')}")
            if p.get("website"):
                r3.markdown(f"**Website:** [{p['website']}]({p['website']})")
            if p.get("email"):
                r1.markdown(f"**Email:** {p['email']}")
            if p.get("phone"):
                r2.markdown(f"**Phone:** {p['phone']}")
            if p.get("address"):
                st.markdown(f"**Address:** {p['address']}")
            if p.get("description"):
                section_label("Description")
                st.markdown(p["description"])

        with tab_bank:
            has_bank = any(p.get(f) for f in ["bank_name","bank_account","iban","bic","swift"])
            if not has_bank:
                st.info("No bank details recorded.")
            else:
                b1,b2,b3 = st.columns(3)
                b1.markdown(f"**Bank Name:** {p.get('bank_name','—')}")
                b2.markdown(f"**Account:** {p.get('bank_account','—')}")
                b3.markdown(f"**IBAN:** {p.get('iban','—')}")
                b1.markdown(f"**BIC:** {p.get('bic','—')}")
                b2.markdown(f"**SWIFT:** {p.get('swift','—')}")

        with tab_social:
            socials = [
                ("Facebook",  "facebook",  "https://facebook.com/"),
                ("LinkedIn",  "linkedin",  "https://linkedin.com/company/"),
                ("Twitter/X", "twitter",   "https://twitter.com/"),
                ("YouTube",   "youtube",   "https://youtube.com/@"),
                ("Instagram", "instagram", "https://instagram.com/"),
            ]
            has_social = any(p.get(k) for _,k,_ in socials)
            if not has_social:
                st.info("No social media accounts recorded.")
            else:
                for label, key, base_url in socials:
                    handle = p.get(key,"")
                    if handle:
                        clean = handle.lstrip("@")
                        url   = base_url + clean
                        acc   = D["accent"]
                        st.markdown(
                            f"**{label}:** "
                            f"[{handle}]({url})",
                            unsafe_allow_html=False
                        )

        with tab_contacts:
            contacts = get_contacts(open_id)
            if not contacts:
                st.info("No contacts recorded for this partner.")
            else:
                for c in contacts:
                    full    = f"{c.get('first_name','')} {c.get('last_name','')}".strip()
                    pos     = c.get("position","")
                    _muted  = D["muted"]
                    _txt    = D["text"]
                    _acc    = D["accent"]
                    _bg2    = D["bg2"]
                    _border = D["border"]
                    _li_url  = f"https://linkedin.com/in/{c.get('linkedin','').lstrip('@')}"
                    _li_html = (f"  <a href='{_li_url}' target='_blank' "
                                f"style='color:{_acc};font-size:0.8rem'>LinkedIn</a>"
                                if c.get("linkedin") else "")
                    _pos_html = (f" · <span style='color:{_muted};"
                                 f"font-size:0.85rem'>{pos}</span>" if pos else "")
                    _sub = (("📧 " + c.get("email","") + "  ") if c.get("email") else "") + \
                           (("📱 " + c.get("mobile","")) if c.get("mobile") else "")
                    st.markdown(
                        f"<div style='background:{_bg2};border:1px solid {_border};"
                        f"border-radius:10px;padding:0.8rem 1rem;margin-bottom:0.5rem'>"
                        f"<strong style='color:{_txt}'>{full}</strong>{_pos_html}"
                        f"<br><span style='color:{_muted};font-size:0.82rem'>{_sub}</span>"
                        f"{_li_html}</div>",
                        unsafe_allow_html=True
                    )
