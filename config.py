"""Octa Partner Network — Configuration."""

APP_NAME    = "Partner Network"
APP_ICON    = "🌐"
APP_VERSION = "1.0.0"

DARK = {
    "bg":      "#0f1421",
    "bg2":     "#1a2235",
    "bg3":     "#232f45",
    "border":  "rgba(255,255,255,0.09)",
    "text":    "#e2e8f0",
    "muted":   "#8899b0",
    "accent":  "#00BCD4",
    "accent2": "#FF6B35",
    "sidebar": "#1B2A4A",
    "success": "#6fcf97",
    "warning": "#f6cc52",
    "danger":  "#fc8181",
}

PARTNER_TYPES = ["HEI", "Business", "NGO", "Governmental Institute", "Research Centre", "Other"]

# Map colour logic
COLOR_FUNDED    = "#28a745"   # green  — in a funded project
COLOR_PROPOSAL  = "#f6ad55"   # amber  — only in unfunded proposals
COLOR_NONE      = "#2d4a7a"   # dark blue — not involved

# Country name → ISO alpha-3 for Plotly choropleth
COUNTRY_ISO = {
    "Afghanistan": "AFG", "Albania": "ALB", "Algeria": "DZA",
    "Argentina": "ARG", "Armenia": "ARM", "Australia": "AUS",
    "Austria": "AUT", "Azerbaijan": "AZE", "Bangladesh": "BGD",
    "Belarus": "BLR", "Belgium": "BEL", "Bolivia": "BOL",
    "Bosnia and Herzegovina": "BIH", "Brazil": "BRA", "Bulgaria": "BGR",
    "Cambodia": "KHM", "Canada": "CAN", "Chile": "CHL",
    "China": "CHN", "Colombia": "COL", "Croatia": "HRV",
    "Cyprus": "CYP", "Czech Republic": "CZE", "Denmark": "DNK",
    "Ecuador": "ECU", "Egypt": "EGY", "Estonia": "EST",
    "Ethiopia": "ETH", "Finland": "FIN", "France": "FRA",
    "Georgia": "GEO", "Germany": "DEU", "Ghana": "GHA",
    "Greece": "GRC", "Guatemala": "GTM", "Honduras": "HND",
    "Hungary": "HUN", "Iceland": "ISL", "India": "IND",
    "Indonesia": "IDN", "Iran": "IRN", "Iraq": "IRQ",
    "Ireland": "IRL", "Israel": "ISR", "Italy": "ITA",
    "Japan": "JPN", "Jordan": "JOR", "Kazakhstan": "KAZ",
    "Kenya": "KEN", "Kosovo": "XKX", "Kuwait": "KWT",
    "Kyrgyzstan": "KGZ", "Latvia": "LVA", "Lebanon": "LBN",
    "Libya": "LBY", "Lithuania": "LTU", "Luxembourg": "LUX",
    "Malaysia": "MYS", "Malta": "MLT", "Mexico": "MEX",
    "Moldova": "MDA", "Montenegro": "MNE", "Morocco": "MAR",
    "Netherlands": "NLD", "New Zealand": "NZL", "Nigeria": "NGA",
    "North Macedonia": "MKD", "Norway": "NOR", "Pakistan": "PAK",
    "Palestine": "PSE", "Panama": "PAN", "Paraguay": "PRY",
    "Peru": "PER", "Philippines": "PHL", "Poland": "POL",
    "Portugal": "PRT", "Romania": "ROU", "Russia": "RUS",
    "Saudi Arabia": "SAU", "Senegal": "SEN", "Serbia": "SRB",
    "Slovakia": "SVK", "Slovenia": "SVN", "South Africa": "ZAF",
    "South Korea": "KOR", "Spain": "ESP", "Sri Lanka": "LKA",
    "Sweden": "SWE", "Switzerland": "CHE", "Syria": "SYR",
    "Tajikistan": "TJK", "Thailand": "THA", "Tunisia": "TUN",
    "Turkey": "TUR", "Turkmenistan": "TKM", "Uganda": "UGA",
    "Ukraine": "UKR", "United Arab Emirates": "ARE",
    "United Kingdom": "GBR", "United States": "USA",
    "Uruguay": "URY", "Uzbekistan": "UZB", "Venezuela": "VEN",
    "Vietnam": "VNM", "Yemen": "YEM", "Zimbabwe": "ZWE",
    "Norway": "NOR", "Iceland": "ISL", "Liechtenstein": "LIE",
    "Kosovo": "XKX", "North Macedonia": "MKD",
}

# Sorted list of countries for dropdowns
COUNTRIES = sorted(COUNTRY_ISO.keys())
