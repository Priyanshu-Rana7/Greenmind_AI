# GreenMind AI - Document Analyzer Component

import streamlit as st
import os
from utils.ai_helper import extract_pdf_text, analyze_pdf_content

# Sample report configurations for quick loading
SAMPLE_REPORTS = {
    "Sample Campus Energy Audit (PDF)": {
        "text": "Campus Energy Audit Report 2025\n"
                "Total energy consumption: 520,000 kWh\n"
                "Rooftop solar: 0 kW installed.\n"
                "A/C systems: Running 24 hours in computer labs with setpoints at 18 degrees Celsius.\n"
                "Lighting: Over 800 standard T8 fluorescent tubes in use.\n"
                "Campus population: 2000 students.\n"
                "Key findings: High standby load during weekends (averaging 35 kW per hour). "
                "Canteen kitchen ventilation fans are left running overnight.",
        "filename": "sample_energy_audit.pdf"
    },
    "Sample Water Consumption & Leak Audit (PDF)": {
        "text": "Water Utility Audit 2025\n"
                "Annual consumption: 98,550,000 liters.\n"
                "Daily water use per student: 135 liters per day.\n"
                "Faucets: Standard high-flow taps (15 liters/min) in all student hostels. No sensor taps.\n"
                "Overhead tanks: 4 instances of float valve failures reported last month, causing overflows.\n"
                "Rainwater harvesting: Existing sump of 10,000 L, but lines are clogged and disconnected.\n"
                "Key findings: Heavy underground pressure drop detected between academic block and football ground, indicating a major leak.",
        "filename": "sample_water_leak_audit.pdf"
    }
}

def render_doc_analyzer():
    # Page Header
    st.markdown("<h1 class='gradient-text' style='margin-bottom:5px;'>Document Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #cbd5e1; font-size: 0.95rem;'>Upload a campus audit or utility report (PDF) and get instant AI insights — key issues, risks, and SDG mappings.</p>", unsafe_allow_html=True)
    
    # ------------------ PRE-LOADED SAMPLE DATA ------------------
    with st.container(border=True):
        st.markdown("<h5 style='margin:0 0 10px 0; color:#3b82f6;'>Demo Mode - Load Sample Reports:</h5>", unsafe_allow_html=True)
        
        sc1, sc2 = st.columns(2)
        with sc1:
            if st.button("Load Sample Energy Audit"):
                # Set the sample data in session state
                st.session_state.selected_sample = "Sample Campus Energy Audit (PDF)"
                st.session_state.uploaded_analyses["active_filename"] = SAMPLE_REPORTS["Sample Campus Energy Audit (PDF)"]["filename"]
                st.session_state.uploaded_analyses["active_analysis"] = analyze_pdf_content(
                    SAMPLE_REPORTS["Sample Campus Energy Audit (PDF)"]["filename"],
                    SAMPLE_REPORTS["Sample Campus Energy Audit (PDF)"]["text"]
                )
                st.success("Loaded Sample Energy Audit Report!")
                st.rerun()
                
        with sc2:
            if st.button("Load Sample Water Audit"):
                st.session_state.selected_sample = "Sample Water Consumption & Leak Audit (PDF)"
                st.session_state.uploaded_analyses["active_filename"] = SAMPLE_REPORTS["Sample Water Consumption & Leak Audit (PDF)"]["filename"]
                st.session_state.uploaded_analyses["active_analysis"] = analyze_pdf_content(
                    SAMPLE_REPORTS["Sample Water Consumption & Leak Audit (PDF)"]["filename"],
                    SAMPLE_REPORTS["Sample Water Consumption & Leak Audit (PDF)"]["text"]
                )
                st.success("Loaded Sample Water Audit Report!")
                st.rerun()

    # ------------------ FILE UPLOADER ------------------
    uploaded_file = st.file_uploader("Upload a sustainability report (PDF format only)", type="pdf")
    
    if uploaded_file is not None:
        filename = uploaded_file.name
        
        # Prevent parsing again if already loaded in this session
        if ("active_filename" not in st.session_state.uploaded_analyses or 
            st.session_state.uploaded_analyses["active_filename"] != filename):
            
            with st.spinner("Extracting text from PDF..."):
                pdf_text = extract_pdf_text(uploaded_file)
                
            if pdf_text.startswith("Error"):
                st.error(pdf_text)
            else:
                with st.spinner("Analyzing document content with AI..."):
                    analysis_result = analyze_pdf_content(filename, pdf_text)
                    
                st.session_state.uploaded_analyses["active_filename"] = filename
                st.session_state.uploaded_analyses["active_analysis"] = analysis_result
                st.success("Analysis complete!")
                st.rerun()
                
    # ------------------ RENDER ANALYSIS REPORT ------------------
    if "active_analysis" in st.session_state.uploaded_analyses:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(f"<h3 style='margin-top:0; color:#34d399;'>Audit Report Analysis: {st.session_state.uploaded_analyses['active_filename']}</h3>", unsafe_allow_html=True)
            st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.08); margin-bottom: 20px;' />", unsafe_allow_html=True)
            
            # Display the parsed markdown response
            st.markdown(st.session_state.uploaded_analyses["active_analysis"])
            
            # Clear active analysis button
            if st.button("🗑️ Reset Analysis View"):
                st.session_state.uploaded_analyses = {}
                if "selected_sample" in st.session_state:
                    st.session_state.selected_sample = None
                st.rerun()
    else:
        st.info("Upload a PDF file or click one of the sample buttons above to view AI document summaries and SDG insights.")
