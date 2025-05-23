# =============================================================================
# GMBLERS Analytics Dashboard - Optimized Version
# 
# OPTIMIZATIONS COMPLETED:
# - Removed unused imports: datetime, matplotlib.pyplot, seaborn
# - All functions are actively used except create_threat_card and format_time_diff
# - CSS and styling have been kept minimal and functional
# =============================================================================

import streamlit as st
import pandas as pd
import pymongo
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Determine page icon - use logo if available, otherwise emoji
page_icon = "🎮"  # Default fallback
try:
    import os
    if os.path.exists("logo.png"):
        page_icon = "logo.png"
except:
    pass

# Page configuration
st.set_page_config(
    page_title="GMBLERS Analytics", 
    page_icon=page_icon, 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Authentication function
def check_password():
    """Returns True if password is correct"""
    # If already authenticated, just return True
    if st.session_state.authenticated:
        return True
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["auth"]["password"]:
            st.session_state["authenticated"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["authenticated"] = False

    # Login form styling
    st.markdown("""
    <style>
        .login-container {
            background: linear-gradient(135deg, #0f172a 0%, #1a2332 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .login-card {
            background: rgba(51, 65, 85, 0.3);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
            text-align: center;
            max-width: 450px;
            width: 100%;
        }
        
        .login-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .login-text {
            text-align: left;
        }
        
        .login-logo {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            border: 3px solid #3b82f6;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
            flex-shrink: 0;
        }
        
        .login-title {
            background: linear-gradient(135deg, #3b82f6, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0 0 0.5rem 0;
            line-height: 1.1;
        }
        
        .login-subtitle {
            color: #94a3b8;
            margin: 0;
            font-size: 1.1rem;
        }
        
        .stTextInput > div > div > input {
            background-color: rgba(51, 65, 85, 0.5) !important;
            border: 1px solid #475569 !important;
            border-radius: 12px !important;
            color: #f8fafc !important;
            padding: 1rem !important;
            font-size: 1rem !important;
            text-align: center !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Load logo
    logo_base64 = ""
    try:
        if __import__('os').path.exists("logo.png"):
            logo_base64 = __import__('base64').b64encode(open("logo.png", "rb").read()).decode()
    except:
        pass

    # Login form
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if logo_base64:
                st.markdown(f"""
                <div class="login-card">
                    <div class="login-header">
                        <div class="login-text">
                            <h1 class="login-title">GMBLERS</h1>
                            <p class="login-subtitle">Analytics Dashboard</p>
                        </div>
                        <img src="data:image/png;base64,{logo_base64}" class="login-logo">
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="login-card">
                    <div class="login-header">
                        <div class="login-text">
                            <h1 class="login-title">GMBLERS</h1>
                            <p class="login-subtitle">Analytics Dashboard</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.text_input("Enter Password", type="password", key="password", on_change=password_entered, placeholder="Password required...")
            
            if "password" in st.session_state and st.session_state.get("password"):
                if not st.session_state.authenticated:
                    st.error("❌ Incorrect password. Try again.")

    return st.session_state.authenticated

# Main application logic - only run if authenticated
if not check_password():
    st.stop()

# Modern CSS for contemporary aesthetics (with reduced hover effects)
st.markdown("""
<style>
    /* CSS Variables for consistent theming */
    :root {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-card: #334155;
        --accent-primary: #3b82f6;
        --accent-secondary: #60a5fa;
        --accent-tertiary: #2563eb;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --border: #475569;
        --shadow: rgba(0, 0, 0, 0.25);
    }

    /* Global Styles */
    .main {
        background: linear-gradient(135deg, var(--bg-primary) 0%, #1a2332 100%);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Modern Typography */
    h1, h2, h3, h4 {
        color: var(--text-primary);
        font-weight: 700;
        line-height: 1.2;
        letter-spacing: -0.025em;
    }
    
    h1 {
        text-align: center;
        font-size: clamp(2rem, 4vw, 3rem);
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding-bottom: 2rem;
        margin-bottom: 3rem;
        position: relative;
    }
    
    h1::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
        border-radius: 2px;
    }
    
    h2 {
        font-size: 1.75rem;
        color: var(--accent-secondary);
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid var(--border);
        position: relative;
    }
    
    h3 {
        font-size: 1.5rem;
        color: var(--text-primary);
        margin: 2rem 0 1rem 0;
    }
    
    /* Glass Morphism Cards (without hover effects) */
    .stat-card, .modern-card {
        background: rgba(51, 65, 85, 0.3);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px var(--shadow);
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
    }
    
    /* Enhanced Team Colors */
    .gmb-blue {
        color: var(--accent-primary) !important;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
    }
    
    .opponent-red {
        color: var(--danger) !important;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
    }
    
    .win {
        color: var(--success) !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
    }
    
    .loss {
        color: var(--danger) !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
    }
    
    /* Modern Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
        border-right: 1px solid var(--border);
    }
    
    .css-1d391kg .css-17eq0hr, [data-testid="stSidebar"] .css-17eq0hr {
        background: rgba(51, 65, 85, 0.3);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Enhanced Dataframes */
    .dataframe-container {
        background: rgba(51, 65, 85, 0.2);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        overflow: hidden;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px var(--shadow);
    }
    
    /* Modern Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-tertiary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.025em !important;
    }
    
    /* Enhanced Form Elements */
    .stSelectbox > div > div > div, .stTextInput > div > div > input {
        background-color: rgba(51, 65, 85, 0.5) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div > div:focus, .stTextInput > div > div > input:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Modern Radio Buttons */
    .stRadio > div {
        background: rgba(51, 65, 85, 0.3) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Enhanced Progress Bars */
    .stProgress > div {
        background-color: rgba(51, 65, 85, 0.3) !important;
        border-radius: 20px !important;
        height: 12px !important;
        overflow: hidden !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent-tertiary), var(--accent-primary)) !important;
        border-radius: 20px !important;
        transition: all 0.5s ease !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Champion Icons Enhancement */
    .champion-icon {
        border: 3px solid var(--accent-primary);
        border-radius: 50%;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
    }
    
    /* Alert Boxes */
    .stAlert {
        background: rgba(51, 65, 85, 0.4) !important;
        border: 1px solid var(--accent-primary) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(15px) !important;
    }
    
    /* Tables */
    .dataframe th {
        background: linear-gradient(135deg, var(--bg-card), var(--bg-secondary)) !important;
        color: var(--accent-secondary) !important;
        text-transform: uppercase !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        border-bottom: 2px solid var(--accent-primary) !important;
    }
    
    .dataframe td {
        background: rgba(30, 41, 59, 0.7) !important;
        border-bottom: 1px solid var(--border) !important;
    }
    
    /* Metric Cards Enhancement */
    .metric-value {
        font-size: 2.25rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, var(--accent-secondary), var(--accent-primary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0 !important;
    }
    
    .metric-label {
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 0.25rem !important;
    }
    
    .metric-delta {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        margin-top: 0.5rem !important;
    }
    
    /* Player Cards */
    .player-card {
        display: flex;
        align-items: center;
        background: rgba(51, 65, 85, 0.3);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px var(--shadow);
    }
    
    /* Player Items Layout - New improved layout */
    .player-items-row {
        background: rgba(51, 65, 85, 0.3);
        backdrop-filter: blur(15px);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .champion-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        min-width: 80px;
    }
    
    .items-section {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    
    .player-info-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 0.5rem;
    }
    
    .player-name {
        font-weight: 600;
        font-size: 0.9rem;
        color: var(--text-primary);
        margin: 0;
        text-align: center;
    }
    
    .player-score {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin: 0.25rem 0 0 0;
        text-align: center;
    }
    
    /* Logo and header styling */
    .sidebar-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        padding: 1rem 0 2rem 0;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent-primary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-secondary);
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .stat-card, .modern-card {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Enhanced metric cards function
def styled_metric(label, value, delta=None, delta_color="normal"):
    html = f"""
    <div class="stat-card">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <p class="metric-label">{label}</p>
        </div>
        <p class="metric-value">{value}</p>
    """
    
    if delta:
        color_class = "gmb-blue" if delta_color == "blue" else "win" if delta_color == "good" else "loss" if delta_color == "bad" else ""
        html += f'<p class="metric-delta {color_class}">{delta}</p>'
    
    html += "</div>"
    return st.markdown(html, unsafe_allow_html=True)

# Connect to MongoDB Atlas
@st.cache_resource
def get_db():
    connection_string = st.secrets["database"]["mongodb_connection_string"]
    client = pymongo.MongoClient(connection_string)
    return client.GMBLERS

# Get champion data
@st.cache_data(ttl=3600)
def get_champion_data():
    versions = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()
    latest = versions[0]
    champs = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{latest}/data/en_US/champion.json").json()
    
    champ_mapping = {}
    for key, data in champs["data"].items():
        champ_name = data["name"]
        champ_mapping[champ_name.lower()] = key
        champ_mapping[champ_name.lower().replace(" ", "")] = key
        champ_mapping[champ_name.lower().replace("'", "")] = key
        champ_mapping[champ_name.lower().replace(" ", "").replace("'", "")] = key
        
        if champ_name == "Wukong":
            champ_mapping["monkeyking"] = key
        elif champ_name == "Nunu & Willump":
            champ_mapping["nunu"] = key
        
    return champs["data"], latest, champ_mapping

# Helper function to find champion key with improved matching
def find_champion_key(champion_name, champion_data, champ_mapping):
    if not champion_name:
        return None
    
    champ_key = next((k for k, v in champion_data.items() if v["name"] == champion_name), None)
    if champ_key:
        return champ_key
    
    normalized_name = champion_name.lower().replace(" ", "").replace("'", "")
    if normalized_name in champ_mapping:
        return champ_mapping[normalized_name]
    
    for key, data in champion_data.items():
        if champion_name.lower() in data["name"].lower() or data["name"].lower() in champion_name.lower():
            return key
    
    if champion_name in champion_data:
        return champion_name
    
    return None

# Load games from MongoDB Atlas
@st.cache_data(ttl=300)
def load_games():
    db = get_db()
    return list(db.GMB_Games.find().sort("date", -1))

@st.cache_data(ttl=300)
def load_players():
    db = get_db()
    return list(db.GMB_Players.find())

# Format time difference for readability
def format_time_diff(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"

# Enhanced sidebar with modern design
with st.sidebar:
    # Header with logo and text inline
    st.markdown("""
    <div class="sidebar-header">
        <img src="data:image/png;base64,{}" width="40" style="border-radius: 50%;">
        <div>
            <h1 style="font-size: 1.8rem; margin: 0; background: linear-gradient(135deg, #3b82f6, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                GMBLERS
            </h1>
            <p style="color: #94a3b8; font-size: 0.9rem; margin: 0;">Analytics Dashboard</p>
        </div>
    </div>
    """.format(
        # Try to load logo and convert to base64, or use empty string if it fails
        __import__('base64').b64encode(open("logo.png", "rb").read()).decode() if __import__('os').path.exists("logo.png") else ""
    ), unsafe_allow_html=True)
    
    # Modern navigation
    page = st.radio(
        "Navigation",
        ["Scrims", "Team Stats", "Player Stats", "Champion Analysis"]
    )
    
    # Add some stats in sidebar
    st.markdown("---")
    
    # Quick stats
    games = load_games()
    if games:
        total_games = len(games)
        wins = sum(1 for game in games if game.get("win"))
        win_rate = (wins / total_games * 100) if total_games > 0 else 0
        
        st.markdown(f"""
        <div class="modern-card" style="padding: 1rem; margin: 1rem 0;">
            <h4 style="margin: 0 0 0.5rem 0; color: #60a5fa;">Quick Stats</h4>
            <p style="margin: 0.25rem 0; font-size: 0.9rem;"><strong>{total_games}</strong> Total Games</p>
            <p style="margin: 0.25rem 0; font-size: 0.9rem;"><strong>{wins}W - {total_games-wins}L</strong></p>
            <p style="margin: 0.25rem 0; font-size: 0.9rem; color: {'#10b981' if win_rate >= 50 else '#ef4444'};">
                <strong>{win_rate:.1f}%</strong> Win Rate
            </p>
        </div>
        """, unsafe_allow_html=True)

# Load data
games = load_games()
players_db = load_players()
champion_data, ddragon_version, champ_mapping = get_champion_data()

# Helper functions for the enhanced Champion Analysis page
def create_champion_card(champ_data, role_color, champion_data, champ_mapping, ddragon_version):
    """Create a simple champion card with clear separation using only native Streamlit components"""
    champion_name = champ_data["champion"]
    win_rate = champ_data["win_rate"]
    games = champ_data["games"]
    wins = champ_data["wins"]
    losses = champ_data["losses"]
    
    # Get champion key for image
    champ_key = find_champion_key(champion_name, champion_data, champ_mapping)
    
    # Determine win rate status
    if win_rate >= 70:
        wr_status = "Excellent"
    elif win_rate >= 50:
        wr_status = "Good"
    else:
        wr_status = "Needs Work"
    
    # Champion icon centered
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if champ_key:
            st.image(
                f"https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/img/champion/{champ_key}.png",
                width=100
            )
        else:
            st.write("❓")
    
    # Champion name centered
    st.markdown(f"### {champion_name}")
    
    # Win rate as main metric
    st.metric(label="Win Rate", value=f"{win_rate:.1f}%", delta=wr_status)
    
    # Stats in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Wins", wins)
    with col2:
        st.metric("Games", games)
    with col3:
        st.metric("Losses", losses)
    
    # Extra spacing
    st.write("")

def create_champion_row(champ_data, role_color, champion_data, champ_mapping, ddragon_version):
    """Create a compact champion row for detailed view"""
    champion_name = champ_data["champion"]
    win_rate = champ_data["win_rate"]
    games = champ_data["games"]
    wins = champ_data["wins"]
    losses = champ_data["losses"]
    
    champ_key = find_champion_key(champion_name, champion_data, champ_mapping)
    wr_color = "#10b981" if win_rate >= 60 else "#f59e0b" if win_rate >= 40 else "#ef4444"
    
    col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
    
    with col1:
        if champ_key:
            st.image(f"https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/img/champion/{champ_key}.png", width=50)
        else:
            st.markdown(f"""
            <div style="width: 50px; height: 50px; background: #334155; border-radius: 8px; 
                        display: flex; align-items: center; justify-content: center; border: 2px solid {role_color};">
                <span style="color: white;">?</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"**{champion_name}**")
    
    with col3:
        st.metric("Win Rate", f"{win_rate:.1f}%")
    
    with col4:
        st.markdown(f"**{wins}W - {losses}L** ({games}g)")

def create_threat_card(champ_data, threat_color, champion_data, champ_mapping, ddragon_version):
    """Create a simple threat card with icon and info in dark area"""
    champion_name = champ_data["champion"]
    win_rate = champ_data["win_rate"]
    games = champ_data["games"]
    wins = champ_data["wins"]
    losses = champ_data["losses"]
    
    champ_key = find_champion_key(champion_name, champion_data, champ_mapping)
    
    # Determine threat level
    if win_rate >= 70:
        threat_level = "HIGH THREAT"
        threat_icon = "🔥"
    elif win_rate >= 50:
        threat_level = "MEDIUM THREAT"
        threat_icon = "⚠️"
    else:
        threat_level = "FAVORABLE"
        threat_icon = "✅"
    
    # Champion image at the top
    if champ_key:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(
                f"https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/img/champion/{champ_key}.png",
                width=60
            )
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-bottom: 0.75rem;">
            <div style="width: 60px; height: 60px; border-radius: 50%; border: 2px solid {threat_color}; 
                        background: #374151; display: flex; align-items: center; justify-content: center;">
                <span style="color: white;">?</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # All info in the dark background area
    st.markdown(f"""
    <div style="background: rgba(0, 0, 0, 0.6); border-radius: 8px; padding: 1.25rem; margin: 0.75rem 0; text-align: center;">
        <!-- Champion name -->
        <h4 style="color: {threat_color}; margin: 0 0 0.5rem 0; font-weight: 700;">
            {champion_name}
        </h4>
        
        <!-- Threat level -->
        <div style="color: {threat_color}; font-size: 0.7rem; text-transform: uppercase; 
                    margin-bottom: 0.75rem; font-weight: 600;">
            {threat_icon} {threat_level}
        </div>
        
        <!-- Win rate -->
        <div style="font-size: 1.5rem; font-weight: 700; color: {threat_color}; margin-bottom: 0.25rem;">
            {win_rate:.1f}%
        </div>
        <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 500;">
            {wins}W-{losses}L ({games}g)
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_detailed_opponent_table(opponent_data, champion_data, champ_mapping, ddragon_version):
    """Create a detailed table view of all opponent champions"""
    # Display as rows like the GMB "View All Champions" section
    for champ_data in opponent_data:
        create_champion_row(champ_data, "#64748b", champion_data, champ_mapping, ddragon_version)

def create_threat_layout_with_separators(threat_data, threat_color, champion_data, champ_mapping, ddragon_version, max_display=4):
    """Create threat champion layout with vertical separators"""
    num_to_show = min(max_display, len(threat_data))
    
    if num_to_show == 1:
        cols = st.columns([1, 2, 1])
        with cols[1]:
            create_champion_card(threat_data[0], threat_color, champion_data, champ_mapping, ddragon_version)
    elif num_to_show == 2:
        cols = st.columns([2, 1, 2])
        with cols[0]:
            create_champion_card(threat_data[0], threat_color, champion_data, champ_mapping, ddragon_version)
        with cols[1]:
            st.markdown("", unsafe_allow_html=True)  # Separator space
        with cols[2]:
            create_champion_card(threat_data[1], threat_color, champion_data, champ_mapping, ddragon_version)
    elif num_to_show == 3:
        cols = st.columns([3, 1, 3, 1, 3])
        with cols[0]:
            create_champion_card(threat_data[0], threat_color, champion_data, champ_mapping, ddragon_version)
        with cols[1]:
            st.markdown('<div style="border-left: 2px solid #475569; height: 400px; margin: 2rem 0;"></div>', unsafe_allow_html=True)
        with cols[2]:
            create_champion_card(threat_data[1], threat_color, champion_data, champ_mapping, ddragon_version)
        with cols[3]:
            st.markdown('<div style="border-left: 2px solid #475569; height: 400px; margin: 2rem 0;"></div>', unsafe_allow_html=True)
        with cols[4]:
            create_champion_card(threat_data[2], threat_color, champion_data, champ_mapping, ddragon_version)
    elif num_to_show == 4:
        cols = st.columns([2, 1, 2, 1, 2, 1, 2])
        for i in range(4):
            col_index = i * 2  # 0, 2, 4, 6
            with cols[col_index]:
                create_champion_card(threat_data[i], threat_color, champion_data, champ_mapping, ddragon_version)
            # Add separator after first three champions
            if i < 3:
                with cols[col_index + 1]:
                    st.markdown('<div style="border-left: 2px solid #475569; height: 400px; margin: 2rem 0;"></div>', unsafe_allow_html=True)

# Page routing based on selection
if page == "Scrims":
    st.title("Scrims Overview")
    
    if not games:
        st.warning("No games found in database. Please import game data first.")
    else:
        # Create games table for listing
        games_df = pd.DataFrame([
            {
                "id": str(game.get("_id")),
                "date": game.get("date"),
                "opponent": game.get("opponent_team", {}).get("name", "Unknown"),
                "result": "WIN" if game.get("win") else "LOSS",
                "side": game.get("gmb_side", "").upper(),
                "duration": game.get("game_duration", "0:00")
            } for game in games
        ])
        
        # Enhanced filtering section
        with st.container():

            st.subheader("Find a Scrim")
            
            # Extract all champions for filtering
            all_gmb_champions = set()
            all_enemy_champions = set()
            gmb_player_names = ["ILYXOU", "Goliah", "iwanan", "Marth", "Mahonix"]
            
            for game in games:
                gmb_team_id = game.get("gmb_team_id")
                if "final_items" in game:
                    for player, item_data in game["final_items"].items():
                        champion = item_data.get("champion", "")
                        team_id = item_data.get("team_id")
                        
                        if champion:  # Only add if champion name exists
                            # Check if this is a GMB player
                            is_gmb_player = any(player.upper() == gmb_name.upper() for gmb_name in gmb_player_names)
                            
                            if is_gmb_player and team_id == gmb_team_id:
                                all_gmb_champions.add(champion)
                            elif team_id != gmb_team_id:
                                all_enemy_champions.add(champion)
            
            # Sort champion lists
            gmb_champions_list = ["All"] + sorted(list(all_gmb_champions))
            enemy_champions_list = ["All"] + sorted(list(all_enemy_champions))
            
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            
            with col1:
                # Date filtering
                min_date = games_df["date"].min() if not games_df.empty else ""
                max_date = games_df["date"].max() if not games_df.empty else ""
                date_range = st.date_input("Date Range", 
                                           value=[min_date, max_date] if min_date and max_date else None,
                                           key="date_filter")
                
                # Result filter
                result_filter = st.radio("Result", ["All", "WIN", "LOSS"])
            
            with col2:
                # Side filter
                side_filter = st.radio("Side", ["All", "BLUE", "RED"])
                
                # Opponent filter
                opponents = ["All"] + sorted(list(set(games_df["opponent"].tolist())))
                opponent_filter = st.selectbox("Opponent", opponents)
            
            with col3:
                # Champion filters
                st.markdown("**Champion Filters**")
                allied_champion_filter = st.selectbox("Allied Champion", gmb_champions_list, 
                                                     help="Filter games where GMB played this champion")
                enemy_champion_filter = st.selectbox("Enemy Champion", enemy_champions_list,
                                                    help="Filter games where opponent played this champion")
            
            with col4:
                # Apply filters
                filtered_games = games_df.copy()
                
                # Date filter
                if len(date_range) == 2:
                    try:
                        start_date, end_date = date_range
                        filtered_games = filtered_games[(filtered_games["date"] >= str(start_date)) & 
                                                       (filtered_games["date"] <= str(end_date))]
                    except:
                        pass
                
                # Basic filters
                if result_filter != "All":
                    filtered_games = filtered_games[filtered_games["result"] == result_filter]
                if side_filter != "All":
                    filtered_games = filtered_games[filtered_games["side"] == side_filter]
                if opponent_filter != "All":
                    filtered_games = filtered_games[filtered_games["opponent"] == opponent_filter]
                
                # Champion filters - need to check actual game data
                if allied_champion_filter != "All" or enemy_champion_filter != "All":
                    valid_game_ids = []
                    
                    for game in games:
                        game_id = str(game.get("_id"))
                        gmb_team_id = game.get("gmb_team_id")
                        
                        # Check if this game matches current filters (before champion filter)
                        if game_id not in filtered_games["id"].values:
                            continue
                        
                        gmb_champions_in_game = set()
                        enemy_champions_in_game = set()
                        
                        if "final_items" in game:
                            for player, item_data in game["final_items"].items():
                                champion = item_data.get("champion", "")
                                team_id = item_data.get("team_id")
                                
                                if champion:
                                    is_gmb_player = any(player.upper() == gmb_name.upper() for gmb_name in gmb_player_names)
                                    
                                    if is_gmb_player and team_id == gmb_team_id:
                                        gmb_champions_in_game.add(champion)
                                    elif team_id != gmb_team_id:
                                        enemy_champions_in_game.add(champion)
                        
                        # Check champion filters
                        allied_match = (allied_champion_filter == "All" or 
                                      allied_champion_filter in gmb_champions_in_game)
                        enemy_match = (enemy_champion_filter == "All" or 
                                     enemy_champion_filter in enemy_champions_in_game)
                        
                        if allied_match and enemy_match:
                            valid_game_ids.append(game_id)
                    
                    # Filter dataframe to only include games that match champion criteria
                    filtered_games = filtered_games[filtered_games["id"].isin(valid_game_ids)]
                
                # Game selection
                if not filtered_games.empty:
                    game_options = [f"{row['date']} | {row['opponent']} ({row['result']}, {row['side']} side)" 
                                  for _, row in filtered_games.iterrows()]
                    
                    selected_index = st.selectbox("Select a Scrim", 
                                                range(len(game_options)),
                                                format_func=lambda i: game_options[i])
                    
                    selected_id = filtered_games.iloc[selected_index]["id"]
                    
                    # Display selection summary with champion info
                    selected_row = filtered_games.iloc[selected_index]
                    result_color = "#10b981" if selected_row['result'] == "WIN" else "#ef4444"
                    
                    # Add champion info to summary if filters are active
                    champion_info = ""
                    if allied_champion_filter != "All":
                        champion_info += f" • Allied: {allied_champion_filter}"
                    if enemy_champion_filter != "All":
                        champion_info += f" • Enemy: {enemy_champion_filter}"
                    
                    st.markdown(f"""
                    <div style="background: rgba(51, 65, 85, 0.3); padding: 1rem; border-radius: 8px; margin-top: 1rem; border-left: 4px solid {result_color};">
                        <strong>Selected:</strong> {selected_row['date']} vs {selected_row['opponent']} • 
                        <span style="color: {result_color}; font-weight: 600;">{selected_row['result']}</span> • 
                        {selected_row['side']} side • Duration: {selected_row['duration']}{champion_info}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("No scrims match the selected filters.")
                    selected_id = None
        
        # Game details section
        if selected_id:
            game = next((g for g in games if str(g.get("_id")) == selected_id), None)
            
            if game:
                st.header("Game Details")
                
                # Game header with enhanced styling
                result_color = "#10b981" if game.get("win") else "#ef4444"
                result_text = "VICTORY" if game.get("win") else "DEFEAT"
                
                st.markdown(f"""
                <div class="modern-card" style="text-align: center; padding: 2rem;">
                    <h2 style="margin: 0; color: {result_color}; font-size: 2.5rem; text-shadow: 0 0 20px {result_color}50;">
                        {result_text}
                    </h2>
                    <h3 style="margin: 0.5rem 0 0 0; color: #94a3b8;">
                        vs {game.get('opponent_team', {}).get('name', 'Unknown')}
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Game metadata with modern cards
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    styled_metric("Date", game.get('date'))
                    styled_metric("Duration", game.get('game_duration', '0:00'))
                
                with col2:
                    styled_metric("Side", game.get('gmb_side', '').upper())
                    # Simplified first blood - just show team (no time)
                    first_blood = game.get('first_blood', {})
                    if first_blood.get('team'):
                        fb_team = "GMB" if first_blood.get('team') == "GMB" else "Opponent"
                        styled_metric("First Blood", fb_team)
                
                with col3:
                    # Objectives with enhanced display
                    gmb_objectives = game.get('objectives', {}).get('blue_team' if game.get('gmb_side') == 'blue' else 'red_team', {}).get('objectives', {})
                    enemy_objectives = game.get('objectives', {}).get('red_team' if game.get('gmb_side') == 'blue' else 'blue_team', {}).get('objectives', {})
                    
                    dragons_gmb = gmb_objectives.get('dragon', {}).get('kills', 0)
                    dragons_enemy = enemy_objectives.get('dragon', {}).get('kills', 0)
                    styled_metric("Dragons", f"{dragons_gmb} - {dragons_enemy}")
                    
                    barons_gmb = gmb_objectives.get('baron', {}).get('kills', 0)
                    barons_enemy = enemy_objectives.get('baron', {}).get('kills', 0)
                    styled_metric("Barons", f"{barons_gmb} - {barons_enemy}")
                
                # Enhanced Draft Section
                st.header("Draft Analysis")
                if "draft" in game:
                    pick_order = game["draft"].get("pick_order", [])
                    
                    if pick_order:
                        pick_order.sort(key=lambda x: x.get("sequence_number", 99) if x.get("sequence_number") is not None else 99)
                        

                        st.subheader("Pick Order")
                        
                        # Create draft visualization
                        cols = st.columns(len(pick_order))
                        
                        for i, pick in enumerate(pick_order):
                            team = pick.get("team", "")
                            champion = pick.get("champion", "")
                            is_gmb = "GMB" in team or team == "GMBLERS Esports"
                            
                            sequence = pick.get("sequence_number", i + 1)
                            pick_labels = {
                                1: "B1", 2: "R1", 3: "R2", 4: "B2", 5: "B3",
                                6: "R3", 7: "R4", 8: "B4", 9: "B5", 10: "R5"
                            }
                            pick_code = pick_labels.get(sequence, f"Pick {sequence}")
                            
                            with cols[i]:
                                champ_key = find_champion_key(champion, champion_data, champ_mapping)
                                if champ_key:
                                    st.image(
                                        f"https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/img/champion/{champ_key}.png", 
                                        width=60,
                                        use_container_width=False
                                    )
                                else:
                                    st.markdown(f"""
                                    <div style='height:60px;width:60px;background:linear-gradient(135deg, var(--bg-card), var(--bg-secondary));
                                    border-radius:8px;display:flex;align-items:center;justify-content:center;margin:0 auto;
                                    border:2px solid var(--border);'>
                                        <span style='color:white;font-size:1.2rem;'>?</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                team_color = "#3b82f6" if is_gmb else "#ef4444"
                                st.markdown(f"""
                                <div style='text-align:center; margin-top:0.5rem;'>
                                    <div style='background:{team_color}; color:white; padding:0.25rem 0.5rem; 
                                    border-radius:6px; font-weight:600; font-size:0.8rem; margin-bottom:0.25rem;'>
                                        {pick_code}
                                    </div>
                                    <div style='font-size:0.75rem; color:var(--text-secondary);'>
                                        {champion}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                
                # Enhanced Final Items Section with new layout: Champion -> Items -> Name/KDA under champion
                st.header("Scoreboard")
                if "final_items" in game and "player_data" in game:
                    gmb_team_id = game.get("gmb_team_id")
                    gmb_player_items = []
                    opponent_player_items = []
                    
                    for player, item_data in game["final_items"].items():
                        # Get player KDA from game data
                        player_stats = game["player_data"].get(player, {})
                        kda = player_stats.get("kda", "0/0/0")
                        
                        if item_data.get("team_id") == gmb_team_id:
                            gmb_player_items.append((player, item_data, kda))
                        else:
                            opponent_player_items.append((player, item_data, kda))
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("GMB Final Items")
                        
                        for player, item_data, kda in gmb_player_items:
                            champ_name = item_data.get("champion")
                            champ_key = find_champion_key(champ_name, champion_data, champ_mapping)
                            
                            st.markdown('<div class="player-items-row">', unsafe_allow_html=True)
                            
                            # Layout: Champion section (icon + name/KDA below) | Items section
                            champion_col, items_col = st.columns([1, 4])
                            
                            with champion_col:
                                # Champion icon
                                if champ_key:
                                    st.image(
                                        f"https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/img/champion/{champ_key}.png", 
                                        width=60
                                    )
                                
                                # Player info under champion
                                st.markdown(f"""
                                <div class="player-info-section">
                                    <div class="player-name">{player}</div>
                                    <div class="player-score">{kda}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with items_col:
                                # Items right after champion
                                items_html = '<div class="items-section">'
                                for i, item_id in enumerate(item_data.get("items", [])):
                                    if i < 6 and item_id > 0:
                                        items_html += f'<img src="https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/img/item/{item_id}.png" width="35" style="margin:2px; border-radius:4px; border:1px solid var(--border);" />'
                                
                                trinket_id = item_data.get("trinket", 0)
                                if trinket_id > 0:
                                    items_html += f'<img src="https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/img/item/{trinket_id}.png" width="35" style="margin:2px 2px 2px 8px; border-radius:4px; border:2px solid var(--accent-primary);" />'
                                
                                items_html += '</div>'
                                st.markdown(items_html, unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.subheader("Opponent Final Items")
                        
                        for player, item_data, kda in opponent_player_items:
                            champ_name = item_data.get("champion")
                            champ_key = find_champion_key(champ_name, champion_data, champ_mapping)
                            
                            st.markdown('<div class="player-items-row">', unsafe_allow_html=True)
                            
                            # Layout: Champion section (icon + name/KDA below) | Items section
                            champion_col, items_col = st.columns([1, 4])
                            
                            with champion_col:
                                # Champion icon
                                if champ_key:
                                    st.image(
                                        f"https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/img/champion/{champ_key}.png", 
                                        width=60
                                    )
                                
                                # Player info under champion
                                st.markdown(f"""
                                <div class="player-info-section">
                                    <div class="player-name" style="color: var(--danger);">{player}</div>
                                    <div class="player-score">{kda}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with items_col:
                                # Items right after champion
                                items_html = '<div class="items-section">'
                                for i, item_id in enumerate(item_data.get("items", [])):
                                    if i < 6 and item_id > 0:
                                        items_html += f'<img src="https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/img/item/{item_id}.png" width="35" style="margin:2px; border-radius:4px; border:1px solid var(--border);" />'
                                
                                trinket_id = item_data.get("trinket", 0)
                                if trinket_id > 0:
                                    items_html += f'<img src="https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/img/item/{trinket_id}.png" width="35" style="margin:2px 2px 2px 8px; border-radius:4px; border:2px solid var(--danger);" />'
                                
                                items_html += '</div>'
                                st.markdown(items_html, unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                
                # Enhanced Player Performance
                st.header("Player Performance")
                
                if "player_data" in game and "player_positions" in game:
                    gmb_player_names = ["ILYXOU", "Goliah", "iwanan", "Marth", "Mahonix"]
                    gmb_players = []
                    opponent_players = []
                    
                    for player, stats in game["player_data"].items():
                        player_data = {
                            "Player": player,
                            "KDA": stats.get("kda", "0/0/0"),
                            "Gold@15": stats.get("gold_15min", 0),
                            "CS@15": stats.get("cs_15min", 0),
                            "Gold Diff@15": stats.get("gold_diff_15min", 0),
                            "CS Diff@15": stats.get("cs_diff_15min", 0)
                        }
                        
                        if player in gmb_player_names or player.upper() in [p.upper() for p in gmb_player_names]:
                            gmb_players.append(player_data)
                        else:
                            opponent_players.append(player_data)
                    
                    column_config = {
                        "Gold Diff@15": st.column_config.NumberColumn(
                            "Gold Diff@15",
                            help="Gold difference at 15 minutes",
                            format="%d"
                        ),
                        "CS Diff@15": st.column_config.NumberColumn(
                            "CS Diff@15",
                            help="CS difference at 15 minutes",
                            format="%.1f"
                        ),
                    }
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if gmb_players:
                            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                            st.subheader("GMBLERS Players")
                            gmb_df = pd.DataFrame(gmb_players)
                            st.dataframe(
                                gmb_df,
                                column_config=column_config,
                                hide_index=True,
                                use_container_width=True
                            )
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        if opponent_players:
                            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                            st.subheader("Opponent Players")
                            opponent_df = pd.DataFrame(opponent_players)
                            st.dataframe(
                                opponent_df,
                                column_config=column_config,
                                hide_index=True,
                                use_container_width=True
                            )
                            st.markdown('</div>', unsafe_allow_html=True)

elif page == "Team Stats":
    st.title("Team Statistics")
    
    if not games:
        st.warning("No games found in database. Please import game data first.")
    else:
        # Calculate stats
        total_games = len(games)
        wins = sum(1 for game in games if game.get("win"))
        losses = total_games - wins
        win_rate = (wins / total_games * 100) if total_games > 0 else 0
        
        # Side stats
        blue_games = sum(1 for game in games if game.get("gmb_side") == "blue")
        blue_wins = sum(1 for game in games if game.get("gmb_side") == "blue" and game.get("win"))
        blue_win_rate = (blue_wins / blue_games * 100) if blue_games > 0 else 0
        
        red_games = sum(1 for game in games if game.get("gmb_side") == "red")
        red_wins = sum(1 for game in games if game.get("gmb_side") == "red" and game.get("win"))
        red_win_rate = (red_wins / red_games * 100) if red_games > 0 else 0
        
        # Modern metrics display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            styled_metric("Overall Record", f"{wins}W - {losses}L", f"Win Rate: {win_rate:.1f}%", "blue")
            st.progress(win_rate/100)
        
        with col2:
            styled_metric("Blue Side Record", f"{blue_wins}W - {blue_games-blue_wins}L", f"Win Rate: {blue_win_rate:.1f}%", "blue")
            st.progress(blue_win_rate/100)
        
        with col3:
            styled_metric("Red Side Record", f"{red_wins}W - {red_games-red_wins}L", f"Win Rate: {red_win_rate:.1f}%", "blue") 
            st.progress(red_win_rate/100)
        
        # Enhanced Objective Control section
        st.header("Objective Control")
        
        # Calculate objective stats (excluding first blood from dataframe)
        dragons_total = 0
        barons_total = 0
        first_dragon_games = 0
        first_dragon_wins = 0
        first_baron_games = 0
        first_baron_wins = 0
        first_herald_games = 0
        first_herald_wins = 0
        
        for game in games:
            gmb_team_data = None
            if game.get("gmb_side") == "blue" and "objectives" in game:
                gmb_team_data = game["objectives"].get("blue_team", {})
            elif game.get("gmb_side") == "red" and "objectives" in game:
                gmb_team_data = game["objectives"].get("red_team", {})
            
            if gmb_team_data and "objectives" in gmb_team_data:
                dragons_total += gmb_team_data["objectives"].get("dragon", {}).get("kills", 0)
                barons_total += gmb_team_data["objectives"].get("baron", {}).get("kills", 0)
                
                if gmb_team_data["objectives"].get("dragon", {}).get("first", False):
                    first_dragon_games += 1
                    if game.get("win"):
                        first_dragon_wins += 1
                
                if gmb_team_data["objectives"].get("baron", {}).get("first", False):
                    first_baron_games += 1
                    if game.get("win"):
                        first_baron_wins += 1
                
                if gmb_team_data["objectives"].get("riftHerald", {}).get("first", False):
                    first_herald_games += 1
                    if game.get("win"):
                        first_herald_wins += 1
        
        # Calculate rates
        first_dragon_rate = (first_dragon_wins / first_dragon_games * 100) if first_dragon_games > 0 else 0
        first_baron_rate = (first_baron_wins / first_baron_games * 100) if first_baron_games > 0 else 0
        first_herald_rate = (first_herald_wins / first_herald_games * 100) if first_herald_games > 0 else 0
        
        # Create modern visualization with Plotly (excluding first blood)
        objective_df = pd.DataFrame({
            "Objective": ["First Dragon", "First Herald", "First Baron"],
            "Win Rate": [first_dragon_rate, first_herald_rate, first_baron_rate],
            "Total Games": [first_dragon_games, first_herald_games, first_baron_games]
        })
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Create Plotly chart
            fig = go.Figure(data=[
                go.Bar(
                    x=objective_df["Objective"], 
                    y=objective_df["Win Rate"],
                    marker=dict(
                        color=['#f59e0b', '#8b5cf6', '#3b82f6'],
                        line=dict(color='#1e293b', width=2)
                    ),
                    text=[f"{rate:.1f}%" for rate in objective_df["Win Rate"]],
                    textposition='auto',
                    textfont=dict(color='white', size=12, family='Inter')
                )
            ])
            
            fig.update_layout(
                title=dict(
                    text="Win Rate When Securing Objectives",
                    font=dict(color='#f8fafc', size=16, family='Inter'),
                    x=0.5
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f8fafc', family='Inter'),
                yaxis=dict(
                    range=[0, 100],
                    title="Win Rate (%)",
                    gridcolor='#334155',
                    gridwidth=1
                ),
                xaxis=dict(
                    title="",
                    tickfont=dict(size=10)
                ),
                margin=dict(l=20, r=20, t=50, b=20),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            styled_metric("Avg. Dragons per Game", f"{dragons_total / total_games:.1f}" if total_games > 0 else "0")
            styled_metric("Avg. Barons per Game", f"{barons_total / total_games:.1f}" if total_games > 0 else "0")
            
            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
            st.dataframe(
                objective_df,
                column_config={
                    "Win Rate": st.column_config.ProgressColumn(
                        "Win Rate",
                        help="Win rate when securing objective",
                        format="%.1f%%",
                        min_value=0,
                        max_value=100,
                    ),
                },
                hide_index=True,
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

elif page == "Player Stats":
    st.title("Player Statistics")
    
    if not players_db:
        st.warning("No player data found in database.")
    else:
        # Convert player data
        players_data = []
        for player in players_db:
            players_data.append({
                "name": player.get("name", "Unknown"),
                "games_played": player.get("games_played", 0),
                "avg_gold_15min": player.get("avg_player_data", {}).get("gold_15min", 0),
                "avg_cs_15min": player.get("avg_player_data", {}).get("cs_15min", 0),
                "avg_gold_diff_15min": player.get("avg_player_data", {}).get("gold_diff_15min", 0),
                "avg_cs_diff_15min": player.get("avg_player_data", {}).get("cs_diff_15min", 0),
                "kda_kills": player.get("avg_player_data", {}).get("kda_kills", 0),
                "kda_deaths": player.get("avg_player_data", {}).get("kda_deaths", 0),
                "kda_assists": player.get("avg_player_data", {}).get("kda_assists", 0),
                "kda_ratio": player.get("avg_player_data", {}).get("kda_ratio", 0),
                "avg_kda": player.get("avg_player_data", {}).get("kda", "0/0/0"),
                "avg_control_wards": player.get("avg_control_wards", 0),
                "avg_vision_score": player.get("avg_challenges", {}).get("vision_score", 0),
                "avg_damage_per_minute": player.get("avg_challenges", {}).get("damage_per_minute", 0)
            })
        
        players_df = pd.DataFrame(players_data)
        
        # Enhanced player selector
        # st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        players = sorted(list(players_df["name"]))
        selected_player = st.selectbox("Select Player", players)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if selected_player:
            player_data = players_df[players_df["name"] == selected_player].iloc[0]
            
            # Header with player stats
            st.markdown(f"""
            <div class="modern-card" style="text-align: center; padding: 2rem;">
                <h2 style="margin: 0; background: linear-gradient(135deg, #3b82f6, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {selected_player}
                </h2>
                <p style="color: #94a3b8; margin: 0.5rem 0 0 0;">Player Statistics Overview</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Key metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                styled_metric("Games Played", str(player_data["games_played"]))
            with col2:
                styled_metric("KDA Ratio", f"{player_data['kda_ratio']:.2f}")
            with col3:
                styled_metric("Average KDA", player_data["avg_kda"])
            
            # Performance metrics
            st.header("Performance Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                styled_metric("Avg Gold@15", f"{player_data['avg_gold_15min']:.0f}")
                diff_color = "good" if player_data['avg_gold_diff_15min'] >= 0 else "bad"
                styled_metric("Avg Gold Diff@15", f"{player_data['avg_gold_diff_15min']:+.0f}", delta_color=diff_color)
            
            with col2:
                styled_metric("Avg CS@15", f"{player_data['avg_cs_15min']:.1f}")
                cs_diff_color = "good" if player_data['avg_cs_diff_15min'] >= 0 else "bad"
                styled_metric("Avg CS Diff@15", f"{player_data['avg_cs_diff_15min']:+.1f}", delta_color=cs_diff_color)
            
            with col3:
                styled_metric("Avg Vision Score", f"{player_data['avg_vision_score']:.1f}")
                styled_metric("Avg Control Wards", f"{player_data['avg_control_wards']:.1f}")
            
            with col4:
                styled_metric("Avg Damage/Min", f"{player_data['avg_damage_per_minute']:.1f}")
            
            # Player Challenges (without visualization)
            st.header("Player Challenges")
            
            player_challenges = {}
            for player in players_db:
                if player.get("name") == selected_player:
                    player_challenges = player.get("avg_challenges", {})
                    break
            
            if player_challenges:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    styled_metric("Vision Score", f"{player_challenges.get('vision_score', 0):.1f}")
                    styled_metric("Damage Per Minute", f"{player_challenges.get('damage_per_minute', 0):.1f}")
                    styled_metric("Buffs Stolen", f"{player_challenges.get('buffs_stolen', 0):.1f}")
                
                with col2:
                    styled_metric("Skillshots Hit", f"{player_challenges.get('skill_shots_hit', 0):.1f}")
                    styled_metric("Skillshots Dodged", f"{player_challenges.get('skill_shots_dodged', 0):.1f}")
                    styled_metric("Perfect Game", f"{player_challenges.get('perfect_game', 0):.2f}")
                
                with col3:
                    styled_metric("Turret Plates Taken", f"{player_challenges.get('turret_plates_taken', 0):.1f}")
                    # styled_metric("KDA Ratio", f"{player_challenges.get('kda', 0):.2f}")
                    danced = "Yes" if player_challenges.get('dance_with_rift_herald', False) else "No"
                    styled_metric("Danced with Herald", danced)
            else:
                st.warning(f"No challenge data found for player {selected_player}")
            
            # Game history moved to bottom
            player_games = []
            for game in games:
                if selected_player in game.get("player_data", {}):
                    player_stats = game["player_data"][selected_player]
                    player_games.append({
                        "game_id": str(game.get("_id")),
                        "date": game.get("date"),
                        "opponent": game.get("opponent_team", {}).get("name", "Unknown"),
                        "win": game.get("win", False),
                        "kda": player_stats.get("kda", "0/0/0"),
                        "gold_15min": player_stats.get("gold_15min", 0),
                        "cs_15min": player_stats.get("cs_15min", 0),
                        "gold_diff_15min": player_stats.get("gold_diff_15min", 0),
                        "cs_diff_15min": player_stats.get("cs_diff_15min", 0),
                        "position": game.get("player_positions", {}).get(selected_player, "")
                    })
            
            if player_games:
                st.header("Game History")
                
                games_df = pd.DataFrame(player_games)
                games_df = games_df.sort_values("date", ascending=False)
                
                st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                st.dataframe(
                    games_df,
                    column_config={
                        "game_id": None,
                        "date": "Date",
                        "opponent": "Opponent",
                        "win": st.column_config.CheckboxColumn("Win"),
                        "kda": "KDA",
                        "gold_15min": st.column_config.NumberColumn("Gold@15", format="%d"),
                        "cs_15min": st.column_config.NumberColumn("CS@15", format="%.1f"),
                        "gold_diff_15min": st.column_config.NumberColumn("Gold Diff@15", format="%+d"),
                        "cs_diff_15min": st.column_config.NumberColumn("CS Diff@15", format="%+.1f")
                    },
                    hide_index=True,
                    use_container_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

elif page == "Champion Analysis":
    st.title("Champion Analysis")
    
    if not games:
        st.warning("No games found in database. Please import game data first.")
    else:
        # Define player roles
        gmb_players = {
            "ILYXOU": "Top",
            "Goliah": "Jungle", 
            "iwanan": "Mid",
            "Marth": "ADC",
            "Mahonix": "Support"
        }
        
        # Role colors for better visual distinction
        role_colors = {
            "Top": "#e11d48",      # Red
            "Jungle": "#10b981",   # Green  
            "Mid": "#3b82f6",      # Blue
            "ADC": "#f59e0b",      # Orange
            "Support": "#8b5cf6"   # Purple
        }
        
        # Collect champion data for GMB players
        gmb_champion_data = {}
        opponent_champion_data = {}
        
        for game in games:
            game_win = game.get("win", False)
            gmb_team_id = game.get("gmb_team_id")
            
            if "final_items" in game:
                for player, item_data in game["final_items"].items():
                    champion = item_data.get("champion", "Unknown")
                    team_id = item_data.get("team_id")
                    
                    # Check if this is a GMB player
                    gmb_player = None
                    for gmb_name, role in gmb_players.items():
                        if player.upper() == gmb_name.upper() or player == gmb_name:
                            gmb_player = gmb_name
                            break
                    
                    if gmb_player and team_id == gmb_team_id:
                        # GMB player
                        role = gmb_players[gmb_player]
                        if role not in gmb_champion_data:
                            gmb_champion_data[role] = {}
                        if champion not in gmb_champion_data[role]:
                            gmb_champion_data[role][champion] = {"wins": 0, "games": 0}
                        
                        gmb_champion_data[role][champion]["games"] += 1
                        if game_win:
                            gmb_champion_data[role][champion]["wins"] += 1
                    
                    elif team_id != gmb_team_id:
                        # Opponent player
                        if "Opponent" not in opponent_champion_data:
                            opponent_champion_data["Opponent"] = {}
                        if champion not in opponent_champion_data["Opponent"]:
                            opponent_champion_data["Opponent"][champion] = {"wins": 0, "games": 0}
                        
                        opponent_champion_data["Opponent"][champion]["games"] += 1
                        if not game_win:  # Opponent wins when GMB loses
                            opponent_champion_data["Opponent"][champion]["wins"] += 1
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["🏆 GMB Champions", "⚔️ Opponent Analysis"])
        
        with tab1:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="background: linear-gradient(135deg, #3b82f6, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">
                    GMBLERS Champion Performance by Role
                </h2>
                <p style="color: #94a3b8; font-size: 1.1rem;">Analyzing champion win rates for each team member</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create role sections
            for role in ["Top", "Jungle", "Mid", "ADC", "Support"]:
                player_name = [k for k, v in gmb_players.items() if v == role][0]
                role_color = role_colors.get(role, "#3b82f6")
                
                if role in gmb_champion_data and gmb_champion_data[role]:
                    # Prepare data for this role
                    role_data = []
                    for champion, stats in gmb_champion_data[role].items():
                        if stats["games"] > 0:
                            win_rate = (stats["wins"] / stats["games"]) * 100
                            role_data.append({
                                "champion": champion,
                                "games": stats["games"],
                                "wins": stats["wins"],
                                "losses": stats["games"] - stats["wins"],
                                "win_rate": win_rate
                            })
                    
                    # Sort by games played, then by win rate
                    role_data.sort(key=lambda x: (x["games"], x["win_rate"]), reverse=True)
                    
                    # Role header with modern styling
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {role_color}20, {role_color}10); 
                                border-left: 4px solid {role_color}; 
                                border-radius: 12px; 
                                padding: 1.5rem; 
                                margin: 2rem 0 1rem 0;
                                backdrop-filter: blur(10px);">
                        <h3 style="color: {role_color}; margin: 0; display: flex; align-items: center; gap: 1rem;">
                            <span style="font-size: 1.8rem;">{role}</span>
                            <span style="color: #94a3b8; font-size: 1.2rem; font-weight: 400;">• {player_name}</span>
                        </h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create champion cards layout
                    if len(role_data) <= 3:
                        # Few champions - display in columns with vertical separators
                        if len(role_data) == 1:
                            cols = st.columns([1, 2, 1])
                            with cols[1]:
                                create_champion_card(role_data[0], role_color, champion_data, champ_mapping, ddragon_version)
                        elif len(role_data) == 2:
                            cols = st.columns([2, 1, 2])
                            with cols[0]:
                                create_champion_card(role_data[0], role_color, champion_data, champ_mapping, ddragon_version)
                            with cols[1]:
                                st.markdown("", unsafe_allow_html=True)  # Separator space
                            with cols[2]:
                                create_champion_card(role_data[1], role_color, champion_data, champ_mapping, ddragon_version)
                        elif len(role_data) == 3:
                            cols = st.columns([3, 1, 3, 1, 3])
                            with cols[0]:
                                create_champion_card(role_data[0], role_color, champion_data, champ_mapping, ddragon_version)
                            with cols[1]:
                                st.markdown('<div style="border-left: 2px solid #475569; height: 400px; margin: 2rem 0;"></div>', unsafe_allow_html=True)
                            with cols[2]:
                                create_champion_card(role_data[1], role_color, champion_data, champ_mapping, ddragon_version)
                            with cols[3]:
                                st.markdown('<div style="border-left: 2px solid #475569; height: 400px; margin: 2rem 0;"></div>', unsafe_allow_html=True)
                            with cols[4]:
                                create_champion_card(role_data[2], role_color, champion_data, champ_mapping, ddragon_version)
                    else:
                        # Many champions - display in grid with metrics + detailed table
                        # Top 3 champions as cards with separators
                        cols = st.columns([3, 1, 3, 1, 3])
                        for i in range(min(3, len(role_data))):
                            col_index = i * 2  # 0, 2, 4
                            with cols[col_index]:
                                create_champion_card(role_data[i], role_color, champion_data, champ_mapping, ddragon_version)
                            # Add separator after first two champions
                            if i < 2:
                                with cols[col_index + 1]:
                                    st.markdown('<div style="border-left: 2px solid #475569; height: 400px; margin: 2rem 0;"></div>', unsafe_allow_html=True)
                        
                        # Remaining champions in detailed view
                        if len(role_data) > 3:
                            with st.expander(f"View All {role} Champions ({len(role_data)} total)", expanded=False):
                                # Create detailed champion grid
                                remaining_champs = role_data[3:]
                                for champ_data in remaining_champs:
                                    create_champion_row(champ_data, role_color, champion_data, champ_mapping, ddragon_version)
                else:
                    # No data for this role
                    st.markdown(f"""
                    <div style="background: rgba(51, 65, 85, 0.3); 
                                border-left: 4px solid {role_color}; 
                                border-radius: 12px; 
                                padding: 1.5rem; 
                                margin: 2rem 0 1rem 0;
                                text-align: center;">
                        <h3 style="color: {role_color}; margin: 0 0 0.5rem 0;">{role} • {player_name}</h3>
                        <p style="color: #94a3b8; margin: 0;">No champion data available</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="background: linear-gradient(135deg, #ef4444, #f87171); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">
                    Enemy Champion Analysis
                </h2>
                <p style="color: #94a3b8; font-size: 1.1rem;">Champions that opponents use against GMBLERS</p>
            </div>
            """, unsafe_allow_html=True)
            
            if "Opponent" in opponent_champion_data:
                # Prepare opponent data
                opponent_data = []
                for champion, stats in opponent_champion_data["Opponent"].items():
                    if stats["games"] > 0:
                        win_rate = (stats["wins"] / stats["games"]) * 100
                        opponent_data.append({
                            "champion": champion,
                            "games": stats["games"],
                            "wins": stats["wins"],
                            "losses": stats["games"] - stats["wins"],
                            "win_rate": win_rate
                        })
                
                if opponent_data:
                    # Sort by games played, then by win rate
                    opponent_data.sort(key=lambda x: (x["games"], x["win_rate"]), reverse=True)
                    
                    # Summary stats cards
                    total_unique_champs = len(opponent_data)
                    high_winrate_champs = len([d for d in opponent_data if d["win_rate"] > 60])
                    most_played = opponent_data[0] if opponent_data else None
                    
                    # Top stats
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        styled_metric("Unique Champions Faced", str(total_unique_champs))
                    with col2:
                        styled_metric("High Win Rate vs GMB", f"{high_winrate_champs} champions", "> 60% win rate", "bad")
                    with col3:
                        if most_played:
                            styled_metric("Most Played Against Us", most_played["champion"], f"{most_played['games']} games", "blue")
                    
                    # Threat Level Analysis
                    st.subheader("🚨 Threat Level Analysis")
                    
                    # Categorize threats
                    high_threat = [d for d in opponent_data if d["win_rate"] >= 70 and d["games"] >= 2]
                    medium_threat = [d for d in opponent_data if 50 <= d["win_rate"] < 70 and d["games"] >= 2]
                    low_threat = [d for d in opponent_data if d["win_rate"] < 50 and d["games"] >= 2]
                    
                    # High threat champions
                    if high_threat:
                        st.markdown("""
                        <h4 style="color: #ef4444; margin: 1.5rem 0 1rem 0;">
                            🔥 High Threat Champions (≥70% win rate, min 2 games)
                        </h4>
                        """, unsafe_allow_html=True)
                        
                        create_threat_layout_with_separators(high_threat, "#ef4444", champion_data, champ_mapping, ddragon_version)
                    
                    # Medium threat champions  
                    if medium_threat:
                        st.markdown("""
                        <h4 style="color: #f59e0b; margin: 1.5rem 0 1rem 0;">
                            ⚠️ Medium Threat Champions (50-69% win rate, min 2 games)
                        </h4>
                        """, unsafe_allow_html=True)
                        
                        create_threat_layout_with_separators(medium_threat, "#f59e0b", champion_data, champ_mapping, ddragon_version)
                    
                    # Low threat champions
                    if low_threat:
                        st.markdown("""
                        <h4 style="color: #10b981; margin: 1.5rem 0 1rem 0;">
                            ✅ Favorable Matchups (<50% win rate vs us, min 2 games)
                        </h4>
                        """, unsafe_allow_html=True)
                        
                        create_threat_layout_with_separators(low_threat, "#10b981", champion_data, champ_mapping, ddragon_version)
                    
                    # Detailed table for all opponents
                    with st.expander("📊 Complete Opponent Champion Statistics", expanded=False):
                        create_detailed_opponent_table(opponent_data, champion_data, champ_mapping, ddragon_version)
            else:
                st.info("No opponent champion data available")

# Logout button at the end of the application
st.markdown("---")
st.markdown('<div style="text-align: center; padding: 2rem 0;">', unsafe_allow_html=True)
if st.button("🔓 Logout", key="logout_button"):
    st.session_state.authenticated = False
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)