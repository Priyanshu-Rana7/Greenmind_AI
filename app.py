# GreenMind AI - Sustainability Decision-Support System
# Main Entrypoint & Layout Manager

import streamlit as st
import os
from dotenv import load_dotenv

# Load components and helpers
from components.dashboard import render_dashboard
from components.copilot import render_copilot
from components.doc_analyzer import render_doc_analyzer
from components.simulator import render_simulator
from components.methodology import render_methodology

# Initialize environment
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="GreenMind AI - Sustainability Support",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling inject
def inject_custom_css():
    st.markdown("""
        <style>
        /* Import Inter Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global CSS Overrides */
        html, body, [class*="css"], .stApp {
            font-family: 'Inter', sans-serif;
            background-color: #09090b !important; /* Zinc 950 */
            color: #fafafa !important; /* Zinc 50 */
        }
        
        /* Glassmorphism card styling - flattened */
        .glass-card {
            background: #18181b; /* Zinc 900 */
            border: 1px solid #27272a; /* Zinc 800 */
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: none;
            transition: border-color 0.2s ease;
        }
        
        .glass-card:hover {
            border-color: #52525b; /* Zinc 600 */
        }
        
        /* Style Streamlit container borders as minimal cards */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: transparent !important;
            border: none !important;
            border-radius: 0px !important;
            padding: 0px !important;
            margin-bottom: 24px !important;
            box-shadow: none !important;
        }
        
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: transparent !important;
            box-shadow: none !important;
        }
        
        /* Minimalist Headers */
        .gradient-text {
            color: #f8fafc;
            font-weight: 700;
            font-size: 2.25rem;
            letter-spacing: -0.025em;
        }
        
        .gradient-header {
            color: #38bdf8; /* Light Sky Blue */
            font-weight: 600;
        }

        /* Metric cards styling override (flat, transparent, and borderless) */
        div[data-testid="stMetric"] {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }
        
        div[data-testid="stMetricValue"], div[data-testid="stMetricValue"] > * {
            font-size: 1.85rem !important;
            font-weight: 700 !important;
            color: #10b981 !important; /* Emerald 500 */
            letter-spacing: -0.02em;
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: clip !important;
        }
        
        div[data-testid="stMetricLabel"], div[data-testid="stMetricLabel"] > * {
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #cbd5e1 !important; /* Slate 400 */
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: clip !important;
        }

        div[data-testid="stMetricDelta"], div[data-testid="stMetricDelta"] > * {
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: clip !important;
        }

        /* Remove inner borders/backgrounds for nested container wrappers */
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }
        
        /* Custom sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #070a13 !important;
            border-right: 1px solid #1e293b !important;
        }
        
        section[data-testid="stSidebar"] .stMarkdown h1 {
            color: #10b981;
            font-size: 1.6rem;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        /* Ensure all sidebar texts, widget labels, and paragraph notes are white */
        section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p,
        section[data-testid="stSidebar"] p {
            color: #ffffff !important;
        }
        
        /* Custom tab-like sidebar list selection */
        div[role="radiogroup"] {
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-top: 15px;
        }
        
        div[role="radiogroup"] label {
            background-color: transparent !important;
            border: 1px solid transparent !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            transition: all 0.2s ease;
            margin-bottom: 0px !important;
            font-weight: 500 !important;
            color: #ffffff !important;
            cursor: pointer;
            width: 100%;
        }
        
        div[role="radiogroup"] label:hover {
            background-color: rgba(255, 255, 255, 0.03) !important;
            color: #f8fafc !important;
        }
        
        div[role="radiogroup"] label[data-baseweb="radio"] {
            display: block !important;
        }
        
        /* Hide the default radio circle indicator to look like nav tabs */
        div[role="radiogroup"] label[data-baseweb="radio"] div[data-testid="stWidgetDynamicLabel"] {
            margin-left: 0 !important;
        }
        
        div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child {
            display: none !important;
        }

        /* Highlight selected tab */
        div[role="radiogroup"] label[data-checked="true"] {
            background-color: rgba(16, 185, 129, 0.1) !important;
            border-color: rgba(16, 185, 129, 0.2) !important;
            color: #34d399 !important;
        }
        
        /* Custom buttons styling - Minimalist Flat/Ghost */
        .stButton>button {
            background: transparent !important;
            color: #e4e4e7 !important; /* Zinc 200 */
            border: 1px solid #3f3f46 !important; /* Zinc 700 */
            border-radius: 6px !important;
            padding: 6px 16px !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton>button:hover {
            background: #27272a !important; /* Zinc 800 */
            color: #fafafa !important;
            border-color: #52525b !important; /* Zinc 600 */
        }
        
        .stButton>button:active {
            transform: scale(0.98) !important;
        }
        
        /* Primary button override if any */
        .stButton>button[data-testid="baseButton-primary"] {
            background: #fafafa !important; /* White */
            color: #09090b !important; /* Black */
            border: none !important;
        }
        .stButton>button[data-testid="baseButton-primary"]:hover {
            background: #e4e4e7 !important; /* Gray */
        }
        
        /* Slider style polish */
        div[data-testid="stSlider"] {
            padding-bottom: 15px;
        }
        
        /* Hide default Streamlit header bar to prevent overlap */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        
        /* Adjust main container padding top to give breathing space */
        div.block-container {
            padding-top: 2.5rem !important;
            padding-bottom: 3rem !important;
        }



        /* Chat Input Dark Theme Override */
        /* Fix the sticky bottom bar that holds the chat input */
        div[data-testid="stBottom"] {
            background-color: transparent !important;
            border-top: 1px solid #1e293b !important;
        }
        
        div[data-testid="stBottom"] > div {
            background-color: #09090b !important;
        }

        div[data-testid="stChatInput"] {
            background-color: #18181b !important; /* Zinc 900 */
            border: 1px solid #27272a !important; /* Zinc 800 */
            border-radius: 8px !important;
            color: #fafafa !important;
        }
        
        div[data-testid="stChatInput"] textarea {
            background-color: #18181b !important;
            color: #fafafa !important;
            border: none !important;
        }
        
        div[data-testid="stChatInput"] button {
            background-color: transparent !important;
            color: #fafafa !important;
        }
        
        /* File Uploader styling */
        div[data-testid="stFileUploader"] {
            background-color: transparent !important;
        }
        div[data-testid="stFileUploader"] > div {
            background-color: #18181b !important;
            border: 1px dashed #3f3f46 !important;
            border-radius: 8px !important;
            color: #fafafa !important;
        }
        div[data-testid="stFileUploader"] > div > div > small {
            color: #a1a1aa !important; /* Zinc 400 */
        }

        /* Chat message bubbles */
        div[data-testid="stChatMessage"] {
            background-color: transparent !important;
        }
        
        div[data-testid="stChatMessage"][data-testid*="user"],
        div[data-testid="stChatMessageUser"] {
            background-color: rgba(16, 185, 129, 0.06) !important;
            border: 1px solid rgba(16, 185, 129, 0.12) !important;
            border-radius: 10px !important;
        }
        
        div[data-testid="stChatMessageAssistant"],
        div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
            background-color: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 10px !important;
        }
        
        /* Footer text styling */
        .footer {
            text-align: center;
            font-size: 0.8rem;
            color: #94a3b8;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #1e293b;
        }
        </style>
    """, unsafe_allow_html=True)

# Main app layout
def main():
    # Inject Custom styling
    inject_custom_css()
    
    # Initialize Session States if not present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    if "uploaded_analyses" not in st.session_state:
        st.session_state.uploaded_analyses = {}
        
    if "sim_params" not in st.session_state:
        # Save default simulation states
        st.session_state.sim_params = {
            "elec_pct": 0.0,
            "solar_kw": 0.0,
            "water_pct": 0.0,
            "waste_rate": 20.0
        }
    
    # Sidebar Logo and Navigation
    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>🌱 GreenMind AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.9rem; color: #cbd5e1; margin-top: -15px;'>AI Decision-Support for Sustainable Campuses</p>", unsafe_allow_html=True)
        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.08); margin-top: 10px; margin-bottom: 20px;' />", unsafe_allow_html=True)
        
        menu = [
            "📊 Sustainability Scorecard",
            "💬 AI Sustainability Copilot",
            "📄 Document Analyzer",
            "🎛️ What-If Scenario Simulator",
            "💡 Design Thinking & Ethics"
        ]
        
        choice = st.radio("System Navigation", menu)
        
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.08);' />", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #cbd5e1;'>Aligned with UN SDGs 6, 7, 11, 12, 13</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #cbd5e1;'>IBM SkillsBuild + AICTE Internship</p>", unsafe_allow_html=True)
        
    # Page Routing
    if choice == "📊 Sustainability Scorecard":
        render_dashboard()
    elif choice == "💬 AI Sustainability Copilot":
        render_copilot()
    elif choice == "📄 Document Analyzer":
        render_doc_analyzer()
    elif choice == "🎛️ What-If Scenario Simulator":
        render_simulator()
    elif choice == "💡 Design Thinking & Ethics":
        render_methodology()
        
    # Global Footer
    st.markdown("""
        <div class="footer">
            GreenMind AI &copy; 2026 | Built for Campus Sustainability Evaluation and Decision Support | Responsible AI Certified
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
