"""
Octa Partner Network — Main Landing Page
World map + Europe map + Partner type chart.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

from modules.auth import require_auth
from modules.sso import auto_login_from_url, set_token_in_url, get_token_from_url
from modules.ui_helpers import inject_css, sidebar_nav, page_header, section_label, DARK
from modules.database import get_all_partners, get_proposals_for_map
from config import COUNTRY_ISO, COLOR_FUNDED, COLOR_PROPOSAL, COLOR_NONE, DARK as D

st.set_page_config(page_title="Partner Network — Octa",
                   page_icon="🌐", layout="wide",
                   initial_sidebar_state="expanded")
inject_css()
auto_login_from_url()
require_auth()

token = st.session_state.get("sso_token","") or get_token_from_url()
if token:
    set_token_in_url(token)

sidebar_nav()
page_header("Partner Network", "Global overview of Octa's partner ecosystem", "🌐")

# ── Load data ─────────────────────────────────────────────────────────────────
partners  = get_all_partners()
proposals = get_proposals_for_map()

if not partners:
    st.info("No partners in the database yet. Use **Add Partner** in the sidebar to get started.")
    st.stop()

df_p = pd.DataFrame(partners)

# ── Build country involvement mapping ─────────────────────────────────────────
# Determine which partner names appear in funded vs unfunded proposals
funded_partner_names   = set()
proposal_partner_names = set()
FUNDED_STATUSES = {"Funded", "Ongoing", "funded", "ongoing"}

for prop in proposals:
    status = prop.get("status","")
    names  = []
    coord  = prop.get("coordinator","")
    if coord:
        names.append(coord.strip())
    plist = prop.get("partners_list") or []
    if isinstance(plist, str):
        try:    plist = json.loads(plist)
        except: plist = []
    names.extend([str(n).strip() for n in plist if n])

    if status in FUNDED_STATUSES:
        funded_partner_names.update(names)
    else:
        proposal_partner_names.update(names)

# Map each partner to their involvement level
def _partner_level(row):
    name  = str(row.get("full_name","")).strip()
    sname = str(row.get("short_name","")).strip()
    if name in funded_partner_names or sname in funded_partner_names:
        return "funded"
    if name in proposal_partner_names or sname in proposal_partner_names:
        return "proposal"
    return "none"

df_p["involvement"] = df_p.apply(_partner_level, axis=1)
df_p["iso"]         = df_p["country"].map(COUNTRY_ISO)
df_p["iso"]         = df_p["iso"].fillna("")

# Build country-level aggregation
country_data = {}
for _, row in df_p.iterrows():
    country = str(row.get("country","")).strip()
    iso     = str(row.get("iso","")).strip()
    if not country or not iso:
        continue
    inv = row["involvement"]
    if country not in country_data:
        country_data[country] = {"iso": iso, "level": inv, "partners": []}
    # Escalate level: funded > proposal > none
    existing = country_data[country]["level"]
    if inv == "funded" or (inv == "proposal" and existing == "none"):
        country_data[country]["level"] = inv
    country_data[country]["partners"].append(
        str(row.get("full_name","")) or str(row.get("short_name",""))
    )

if not country_data:
    st.warning("Partners have no country data. Please add country information to your partners.")
    st.stop()

# Build dataframe for choropleth
map_rows = []
for country, info in country_data.items():
    level = info["level"]
    color_val = 3 if level=="funded" else (2 if level=="proposal" else 1)
    partner_list = "<br>".join(f"• {p}" for p in info["partners"])
    map_rows.append({
        "country":      country,
        "iso":          info["iso"],
        "level":        level,
        "color_val":    color_val,
        "partner_list": partner_list,
        "n_partners":   len(info["partners"]),
    })
map_df = pd.DataFrame(map_rows)

color_discrete = {
    "funded":   COLOR_FUNDED,
    "proposal": COLOR_PROPOSAL,
    "none":     COLOR_NONE,
}

def _build_map(scope: str, height: int) -> go.Figure:
    fig = px.choropleth(
        map_df,
        locations="iso",
        locationmode="ISO-3",
        color="level",
        color_discrete_map=color_discrete,
        hover_name="country",
        hover_data={"iso": False, "color_val": False, "level": False,
                    "n_partners": True, "partner_list": True},
        labels={"n_partners": "Partners", "partner_list": "Partner list"},
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Partners: %{customdata[0]}<br>"
            "%{customdata[1]}<extra></extra>"
        )
    )
    fig.update_geos(
        scope=scope,
        showcoastlines=True,   coastlinecolor="rgba(255,255,255,0.2)",
        showborder=True,       bordercolor="rgba(255,255,255,0.15)",
        showland=True,         landcolor="#1a2235",
        showocean=True,        oceancolor="#0f1421",
        showlakes=True,        lakecolor="#0f1421",
        showframe=False,
        bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        font_color=D["text"],
    )
    return fig

# ── Legend ────────────────────────────────────────────────────────────────────
funded_c = COLOR_FUNDED; proposal_c = COLOR_PROPOSAL; none_c = COLOR_NONE
muted_c  = D["muted"]

st.markdown(f"""
<div style="display:flex;gap:2rem;flex-wrap:wrap;margin-bottom:1rem;
            padding:0.6rem 1rem;background:{D['bg2']};border-radius:8px;
            border:1px solid {D['border']};font-size:0.82rem">
    <span><span style="display:inline-block;width:12px;height:12px;
        background:{funded_c};border-radius:50%;margin-right:5px;vertical-align:middle">
    </span><strong style="color:{funded_c}">Funded project</strong></span>
    <span><span style="display:inline-block;width:12px;height:12px;
        background:{proposal_c};border-radius:50%;margin-right:5px;vertical-align:middle">
    </span><strong style="color:{proposal_c}">Proposals only (unfunded)</strong></span>
    <span><span style="display:inline-block;width:12px;height:12px;
        background:{none_c};border-radius:50%;margin-right:5px;vertical-align:middle">
    </span><strong style="color:{muted_c}">No proposal involvement</strong></span>
</div>
""", unsafe_allow_html=True)

# ── Maps side by side ─────────────────────────────────────────────────────────
mc1, mc2 = st.columns(2)
with mc1:
    st.markdown(f"<h4 style='color:{D['text']};margin-bottom:0.3rem'>🌍 World Map</h4>",
                unsafe_allow_html=True)
    st.plotly_chart(_build_map("world", 380), use_container_width=True)

with mc2:
    st.markdown(f"<h4 style='color:{D['text']};margin-bottom:0.3rem'>🇪🇺 Europe Map</h4>",
                unsafe_allow_html=True)
    st.plotly_chart(_build_map("europe", 380), use_container_width=True)

# ── Country click → partner list ──────────────────────────────────────────────
section_label("🔍 Filter by Country")
country_options = ["All countries"] + sorted(country_data.keys())
sel_country = st.selectbox("Select a country to see its partners",
                            country_options, key="map_country_filter")

filtered_partners = partners if sel_country == "All countries" else \
    [p for p in partners if str(p.get("country","")).strip() == sel_country]

if sel_country != "All countries":
    info = country_data.get(sel_country,{})
    level = info.get("level","none")
    level_color = COLOR_FUNDED if level=="funded" else \
                  (COLOR_PROPOSAL if level=="proposal" else D["muted"])
    level_label = "Funded project" if level=="funded" else \
                  ("Proposals only" if level=="proposal" else "No involvement")
    n_p = len(filtered_partners)
    st.markdown(
        f"<p style='color:{muted_c};font-size:0.85rem'>"
        f"<strong style='color:{D['text']}'>{n_p}</strong> partner{'s' if n_p!=1 else ''} "
        f"in <strong style='color:{D['text']}'>{sel_country}</strong> · "
        f"<span style='color:{level_color}'>{level_label}</span></p>",
        unsafe_allow_html=True
    )

# Show partner cards
_cols = st.columns(3)
for i, p in enumerate(filtered_partners[:12]):
    with _cols[i % 3]:
        name  = p.get("full_name","") or p.get("short_name","")
        ptype = p.get("partner_type","")
        pid   = p["id"]
        logo  = p.get("logo_url","")
        bg2   = D["bg2"]; border = D["border"]; accent = D["accent"]

        st.markdown(
            f"<div style='background:{bg2};border:1px solid {border};"
            f"border-radius:10px;padding:0.9rem;margin-bottom:0.5rem'>"
            + (f"<img src='{logo}' style='height:36px;margin-bottom:0.4rem;object-fit:contain'><br>"
               if logo else "")
            + f"<strong style='color:{D['text']}'>{name}</strong><br>"
            f"<span style='color:{muted_c};font-size:0.8rem'>{ptype} · {p.get('country','')}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
        if st.button("View Details", key=f"view_{pid}_{i}", use_container_width=True):
            st.session_state["view_partner_id"] = pid
            st.switch_page("pages/partner_list.py")

# ── Partner type chart ────────────────────────────────────────────────────────
section_label("📊 Partners by Type")
type_counts = df_p.groupby("partner_type").size().reset_index(name="count")
type_counts = type_counts.sort_values("count", ascending=False)

COLORS = [D["accent"], D["accent2"], D["success"], D["warning"], D["danger"], D["muted"]]

fig_type = px.bar(
    type_counts,
    x="partner_type", y="count",
    color="partner_type",
    color_discrete_sequence=COLORS,
    labels={"partner_type":"Partner Type","count":"Number of Partners"},
    text="count",
)
fig_type.update_traces(textposition="outside", marker_line_width=0)
fig_type.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    height=300, margin=dict(l=0,r=0,t=20,b=0),
    font_color=D["text"], showlegend=False,
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
)
st.plotly_chart(fig_type, use_container_width=True)

# ── Summary KPIs ──────────────────────────────────────────────────────────────
section_label("📈 Summary")
k1,k2,k3,k4 = st.columns(4)
for col, label, val, color in [
    (k1, "Total Partners",    len(partners),                                     D["accent"]),
    (k2, "Countries",         df_p["country"].nunique(),                         D["accent2"]),
    (k3, "In Funded Projects",df_p[df_p["involvement"]=="funded"]["id"].count(), D["success"]),
    (k4, "In Proposals Only", df_p[df_p["involvement"]=="proposal"]["id"].count(),D["warning"]),
]:
    bg2 = D["bg2"]
    col.markdown(
        f"<div style='background:{bg2};border-top:3px solid {color};"
        f"border:1px solid {color}44;border-radius:10px;"
        f"padding:0.9rem;text-align:center'>"
        f"<div style='font-size:1.8rem;font-weight:700;color:{color}'>{val}</div>"
        f"<div style='font-size:0.78rem;color:{muted_c}'>{label}</div></div>",
        unsafe_allow_html=True
    )
