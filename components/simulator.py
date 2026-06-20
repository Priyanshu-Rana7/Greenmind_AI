# GreenMind AI - What-If Scenario Simulator

import streamlit as st
import plotly.graph_objects as go
from utils.calculations import simulate_scenario

def render_simulator():
    # Page Header
    st.markdown("<h1 class='gradient-text' style='margin-bottom:5px;'>What-If Scenario Simulator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #cbd5e1; font-size: 0.95rem;'>Adjust infrastructure levers — solar, LEDs, water fixes, recycling — and instantly see the environmental and financial impact.</p>", unsafe_allow_html=True)
    
    # Initialize slider state values from sim_params for robust synchronization
    if "sim_elec_pct" not in st.session_state:
        st.session_state["sim_elec_pct"] = int(st.session_state.sim_params["elec_pct"])
    if "sim_solar_kw" not in st.session_state:
        st.session_state["sim_solar_kw"] = int(st.session_state.sim_params["solar_kw"])
    if "sim_water_pct" not in st.session_state:
        st.session_state["sim_water_pct"] = int(st.session_state.sim_params["water_pct"])
    if "sim_waste_rate" not in st.session_state:
        st.session_state["sim_waste_rate"] = int(st.session_state.sim_params["waste_rate"])

    # ------------------ SLIDER INPUTS ------------------
    with st.container(border=True):
        st.markdown("<h3 style='margin-top:0; color:#3b82f6;'>Configure Sustainability Scenario</h3>", unsafe_allow_html=True)
        
        col_input1, col_input2 = st.columns(2)
        
        with col_input1:
            st.slider(
                "Electricity Consumption Reduction (%)",
                min_value=0,
                max_value=50,
                step=5,
                key="sim_elec_pct",
                help="E.g., upgrading to LEDs and implementing strict HVAC rules (24°C setting)."
            )
            
            st.slider(
                "Rooftop Solar PV Installed (kW)",
                min_value=0,
                max_value=200,
                step=10,
                key="sim_solar_kw",
                help="10 sq. meters of shadow-free roof required per kW. Generates ~1,460 kWh per year."
            )
            
        with col_input2:
            st.slider(
                "Water Consumption/Leakage Reduction (%)",
                min_value=0,
                max_value=50,
                step=5,
                key="sim_water_pct",
                help="E.g., installing faucet aerators, push-button taps, and fixing float valves."
            )
            
            st.slider(
                "Solid Waste Recycling/Composting Rate (%)",
                min_value=20,
                max_value=90,
                step=5,
                key="sim_waste_rate",
                help="E.g., banning single-use plastics and operating on-site composting units."
            )
            
        # Extract active values and synchronize back to the global state dict
        elec_pct = st.session_state["sim_elec_pct"]
        solar_kw = st.session_state["sim_solar_kw"]
        water_pct = st.session_state["sim_water_pct"]
        waste_rate = st.session_state["sim_waste_rate"]
        
        st.session_state.sim_params["elec_pct"] = elec_pct
        st.session_state.sim_params["solar_kw"] = solar_kw
        st.session_state.sim_params["water_pct"] = water_pct
        st.session_state.sim_params["waste_rate"] = waste_rate

    # Calculate metrics based on current sliders
    sim_data = simulate_scenario(elec_pct, solar_kw, water_pct, waste_rate)
    baseline = sim_data["baseline"]
    optimized = sim_data["optimized"]
    savings = sim_data["savings"]
    sdg_impact = sim_data["sdg_impact"]
    
    # ------------------ SIMULATOR HIGHLIGHTS ------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3>Estimated Scenario Impact</h3>", unsafe_allow_html=True)
    
    sh1, sh2, sh3 = st.columns(3)
    
    with sh1:
        with st.container(border=True):
            st.markdown("<p style='margin:0; text-align: center; color:#cbd5e1; font-weight:500;'>Carbon Offset</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color:#34d399; margin: 10px 0;'>{savings['co2_tons']} tCO2e / year</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin:0; text-align: center; font-size:0.9rem; color:#a78bfa;'>🌳 Equivalent to {int(savings['trees'])} mature trees/year</p>", unsafe_allow_html=True)
        
    with sh2:
        with st.container(border=True):
            st.markdown("<p style='margin:0; text-align: center; color:#cbd5e1; font-weight:500;'>Water Preserved</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color:#38bdf8; margin: 10px 0;'>{int(savings['water_liters']):,} Liters / year</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin:0; text-align: center; font-size:0.9rem; color:#60a5fa;'>💧 ~{round(savings['water_liters']/1000/365, 1)} kL saved daily</p>", unsafe_allow_html=True)
        
    with sh3:
        with st.container(border=True):
            st.markdown("<p style='margin:0; text-align: center; color:#cbd5e1; font-weight:500;'>Utility Bill Reductions</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color:#fb923c; margin: 10px 0;'>₹ {int(savings['financial']):,} / year</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin:0; text-align: center; font-size:0.9rem; color:#f43f5e;'>💰 Decreased annual utility expenses</p>", unsafe_allow_html=True)

    # ------------------ SDG CONTRIBUTION IMPACT ------------------
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_sdg, col_chart = st.columns([2, 3])
    
    with col_sdg:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top:0; color:#10b981;'>UN SDG Contribution Profile</h3>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.9rem; color:#cbd5e1; margin-top:-5px;'>Your simulation supports the following SDG targets:</p>", unsafe_allow_html=True)
            
            # Display progress bars for each SDG
            for sdg, score in sdg_impact.items():
                st.markdown(f"<p style='margin: 10px 0 2px 0; font-size: 0.9rem; font-weight:600;'>{sdg}: {int(score)}% alignment strength</p>", unsafe_allow_html=True)
                st.progress(score / 100.0)
            
    with col_chart:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top:0; color:#60a5fa;'>Carbon Emissions Reduction Pathway</h3>", unsafe_allow_html=True)
            
            # Plot comparison of CO2 baseline vs opt
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Baseline', 'Optimized Scenario'],
                y=[baseline["co2_tons"], optimized["co2_tons"]],
                text=[f'{baseline["co2_tons"]} t', f'{optimized["co2_tons"]} t'],
                textposition='auto',
                marker_color=['#94a3b8', '#10b981'],
                width=0.4
            ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', family='Outfit'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title="Metric Tons of CO2e / Year"),
                margin=dict(l=50, r=30, t=15, b=25),
                height=250
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
    # Bottom notification to apply changes
    st.markdown("<br><div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("Simulate metrics in Sustainability Scorecard"):
        st.success("Scenario parameters locked! Navigate to the 'Sustainability Scorecard' tab to view full details.")
    st.markdown("</div>", unsafe_allow_html=True)
