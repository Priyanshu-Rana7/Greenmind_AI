# GreenMind AI - Design Thinking & Technical Walkthrough

import streamlit as st

def render_methodology():
    # Page Header
    st.markdown("<h1 class='gradient-text' style='margin-bottom:5px;'>💡 Design Thinking & System Architecture</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #cbd5e1; font-size: 0.95rem;'>How GreenMind AI was designed, what drives it, and how to evaluate it.</p>", unsafe_allow_html=True)
    # Load markdown content from external file
    import os
    
    md_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "methodology.md")
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
            
        with st.container(border=True):
            st.markdown(md_content, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading methodology document: {e}")
