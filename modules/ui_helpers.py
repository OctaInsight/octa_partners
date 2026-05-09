"""Octa Partner Network — UI helpers and dark-mode CSS."""
import streamlit as st
from config import DARK, APP_NAME, APP_VERSION

GLOBAL_CSS = f"""
<style>
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
[data-testid="block-container"] {{
    background-color: {DARK['bg']} !important;
    color: {DARK['text']} !important;
}}
[data-testid="stVerticalBlock"],[data-testid="stHorizontalBlock"],
[data-testid="column"],.element-container,.stMarkdown {{
    background: transparent !important;
}}
h1,h2,h3,h4 {{ color: {DARK['text']} !important; }}
p, li {{ color: {DARK['text']}; }}
label,.stTextInput label,.stSelectbox label,.stMultiselect label,
.stTextArea label,.stNumberInput label,.stDateInput label {{
    color: {DARK['muted']} !important; font-size: 0.85rem !important;
}}
[data-testid="stSidebar"] {{
    background: {DARK['sidebar']} !important;
    border-right: 3px solid {DARK['accent']} !important;
    box-shadow: 4px 0 20px rgba(0,188,212,0.1) !important;
}}
[data-testid="stSidebar"] * {{ color: {DARK['text']} !important; }}
[data-testid="stSidebarNav"] {{ display: none !important; }}
[data-testid="stSidebar"] .stButton > button {{
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important; width: 100% !important;
    color: {DARK['text']} !important; font-size: 0.87rem !important;
    text-align: left !important; margin-bottom: 2px !important;
    transition: all 0.18s !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: {DARK['accent']}22 !important;
    border-color: {DARK['accent']}66 !important;
    color: {DARK['accent']} !important;
}}
input,textarea {{
    background: {DARK['bg3']} !important;
    border: 1px solid {DARK['border']} !important;
    border-radius: 8px !important; color: {DARK['text']} !important;
}}
input::placeholder,textarea::placeholder {{ color: {DARK['muted']} !important; }}
div[data-baseweb="select"] > div {{
    background: {DARK['bg3']} !important;
    border-color: {DARK['border']} !important; color: {DARK['text']} !important;
}}
div[data-baseweb="select"] * {{ color: {DARK['text']} !important; }}
div[data-baseweb="popover"] {{
    background: {DARK['bg2']} !important;
    border: 1px solid {DARK['border']} !important;
}}
div[data-baseweb="popover"] li:hover {{ background: {DARK['bg3']} !important; }}
[data-testid="stTabs"] [role="tablist"] {{
    background: {DARK['bg2']}; border-radius: 10px;
    padding: 4px; border: 1px solid {DARK['border']};
}}
[data-testid="stTabs"] [role="tab"] {{ color: {DARK['muted']} !important; border-radius: 8px; }}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
    background: {DARK['accent']} !important; color: white !important;
}}
[data-testid="stButton"] > button {{
    background: {DARK['bg3']} !important;
    border: 1px solid {DARK['border']} !important;
    color: {DARK['text']} !important; border-radius: 8px !important;
    transition: all 0.2s !important;
}}
[data-testid="stButton"] > button:hover {{
    border-color: {DARK['accent']} !important; color: {DARK['accent']} !important;
}}
[data-testid="stButton"] > button[kind="primary"] {{
    background: linear-gradient(135deg,{DARK['accent']},#0097A7) !important;
    border: none !important; color: white !important; font-weight: 600 !important;
}}
[data-testid="stExpander"] {{
    background: {DARK['bg2']} !important;
    border: 1px solid {DARK['border']} !important; border-radius: 10px !important;
}}
[data-testid="stExpander"] summary {{ color: {DARK['text']} !important; }}
[data-testid="stAlert"] {{ border-radius: 10px !important; }}
hr {{ border-color: {DARK['border']} !important; }}
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: {DARK['bg']}; }}
::-webkit-scrollbar-thumb {{ background: {DARK['bg3']}; border-radius: 3px; }}
.page-header {{
    background: linear-gradient(135deg,{DARK['sidebar']} 0%,#2d4a7a 100%);
    padding: 1.4rem 2rem; border-radius: 12px;
    border-left: 4px solid {DARK['accent']};
    margin-bottom: 1.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}}
.page-header h1 {{ margin:0; font-size:1.7rem; font-weight:700; color:white !important; }}
.page-header p {{ margin:0.25rem 0 0; color:rgba(255,255,255,0.7) !important; font-size:0.92rem; }}
.section-label {{
    font-size:0.72rem; font-weight:600; letter-spacing:0.08em;
    text-transform:uppercase; color:{DARK['accent']};
    margin:1.2rem 0 0.5rem; padding-bottom:0.3rem;
    border-bottom:1px solid {DARK['border']};
}}
</style>
"""


def inject_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", icon: str = ""):
    st.markdown(f"""
    <div class="page-header">
        <h1>{icon + ' ' if icon else ''}{title}</h1>
        {'<p>' + subtitle + '</p>' if subtitle else ''}
    </div>""", unsafe_allow_html=True)


def section_label(text: str):
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


def _hr():
    st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.12);margin:0.5rem 0'>",
                unsafe_allow_html=True)


def _section_title(text):
    muted = DARK["muted"]
    st.markdown(
        f"<div style='font-size:0.68rem;font-weight:600;letter-spacing:0.1em;"
        f"text-transform:uppercase;color:{muted};margin-bottom:0.3rem'>{text}</div>",
        unsafe_allow_html=True
    )


def sidebar_nav():
    is_auth       = st.session_state.get("authenticated", False)
    is_admin_user = st.session_state.get("role") == "admin"
    uname         = st.session_state.get("first_name") or st.session_state.get("username","")

    with st.sidebar:
        # Logo / App name
        txt = DARK["text"]; muted = DARK["muted"]
        st.markdown(f"""
<div style="text-align:center;padding:1rem 0 0.8rem">
<div style="font-size:2rem">🌐</div>
<div style="font-weight:700;font-size:1rem;color:{txt}">{APP_NAME}</div>
<div style="color:{muted};font-size:0.68rem">v{APP_VERSION}</div>
</div>""", unsafe_allow_html=True)

        # User badge
        if is_auth and uname:
            st.markdown(
                f"<div style='background:rgba(255,255,255,0.07);"
                f"border:1px solid rgba(255,255,255,0.12);border-radius:8px;"
                f"padding:0.4rem 0.8rem;font-size:0.82rem;margin-bottom:0.4rem'>"
                f"👤 <strong style='color:{txt}'>{uname}</strong></div>",
                unsafe_allow_html=True
            )

        _hr()

        # ── Frame 1: Partners ─────────────────────────────────────────────────
        _section_title("Partners")
        if st.button("🏠  Home / Maps",     key="nav_home",   use_container_width=True):
            st.switch_page("app.py")
        if st.button("🔍  Search Partners", key="nav_search", use_container_width=True):
            st.switch_page("pages/partner_list.py")
        if st.button("➕  Add Partner",     key="nav_add",    use_container_width=True):
            st.session_state.pop("edit_partner_id", None)
            st.switch_page("pages/partner_form.py")

        _hr()

        # ── Frame 2: Tasks ────────────────────────────────────────────────────
        _section_title("Tasks")
        if st.button("📌  Assign Task", key="nav_assign", use_container_width=True):
            st.switch_page("pages/assign_task.py")
        if st.button("✅  My Tasks",    key="nav_tasks",  use_container_width=True):
            st.switch_page("pages/my_tasks.py")

        _hr()

        # ── Frame 3: Admin ────────────────────────────────────────────────────
        if is_admin_user:
            _section_title("Administration")
            if st.button("🛡️  Admin Panel", key="nav_admin", use_container_width=True):
                st.switch_page("pages/admin.py")
            _hr()

        # ── Frame 4: Account ──────────────────────────────────────────────────
        _section_title("Account")
        if is_auth:
            if st.button("🚪  Sign Out", use_container_width=True, key="nav_signout"):
                from modules.sso import logout
                logout()
                st.switch_page("pages/login.py")
        else:
            if st.button("🔑  Login / Register", use_container_width=True, key="nav_login"):
                st.switch_page("pages/login.py")

        st.markdown(
            f"<div style='color:{muted};font-size:0.65rem;text-align:center;margin-top:1.5rem'>"
            f"Octa Platform · {__import__('datetime').date.today().year}</div>",
            unsafe_allow_html=True
        )
