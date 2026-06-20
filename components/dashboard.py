# GreenMind AI - Sustainability Scorecard & Metrics Dashboard

import streamlit as st
import plotly.graph_objects as go
from utils.calculations import simulate_scenario, get_grade, BASE_STUDENTS, GRID_CO2_FACTOR

def render_dashboard():
    # Page Header
    st.markdown("<h1 class='gradient-text' style='margin-bottom:5px;'>Sustainability Scorecard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #cbd5e1; font-size: 0.95rem;'>Live campus performance grades, resource metrics, and projected savings from your scenario.</p>", unsafe_allow_html=True)
    
    # Retrieve current simulation parameters
    sim_data = simulate_scenario(
        st.session_state.sim_params["elec_pct"],
        st.session_state.sim_params["solar_kw"],
        st.session_state.sim_params["water_pct"],
        st.session_state.sim_params["waste_rate"]
    )
    
    baseline = sim_data["baseline"]
    optimized = sim_data["optimized"]
    savings = sim_data["savings"]
      # ------------------ TOP PANEL: OVERALL SCORE & GRADE ------------------
    col1, col2 = st.columns([1.5, 2.5])
    
    with col1:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0; color: #34d399; text-align: center;'>Current Sustainability Grade</h3>", unsafe_allow_html=True)
            
            # Display grade change via Plotly Gauge
            base_score = baseline["scores"]["overall"]
            opt_score = optimized["scores"]["overall"]
            grade = get_grade(opt_score)
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = opt_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': f"Grade: {grade}", 'font': {'size': 24, 'color': '#10b981'}},
                delta = {'reference': base_score, 'increasing': {'color': "#34d399"}, 'decreasing': {'color': "#ef4444"}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#10b981"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "#1e293b",
                    'steps': [
                        {'range': [0, 50], 'color': '#ef4444'},
                        {'range': [50, 70], 'color': '#f59e0b'},
                        {'range': [70, 90], 'color': '#3b82f6'},
                        {'range': [90, 100], 'color': '#10b981'}],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': opt_score}
                }
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': "#f8fafc", 'family': "Outfit"},
                height=250,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            if opt_score == base_score:
                st.markdown("<p style='color: #cbd5e1; font-size: 0.9rem; text-align: center; margin-top: -20px;'>Baseline score. Adjust sliders in simulator to improve.</p>", unsafe_allow_html=True)
            
    with col2:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0; color: #60a5fa;'>Environmental Savings Summary</h3>", unsafe_allow_html=True)
            
            # Display savings in columns
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.metric(label="CO₂ Saved", value=f"{savings['co2_tons']} tons/yr", delta=f"{savings['trees']} trees equivalent")
            with sc2:
                st.metric(label="Water Saved", value=f"{int(savings['water_liters']):,} L/yr", delta=f"{round(savings['water_liters']/1000/365, 1)} kL/day")
            with sc3:
                st.metric(label="Cost Saved", value=f"₹ {int(savings['financial']):,}/yr", delta="Operational Savings")
                
            st.markdown("<p style='color: #cbd5e1; font-size: 0.9rem; margin-top: 15px;'>*Carbon equivalency calculated at 22 kg CO₂/tree/year. Financial figures computed using standard state institutional tariffs.</p>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ------------------ MIDDLE PANEL: KPI COMPARISON CARDS ------------------
    st.markdown("<h3 style='color:#e2e8f0;'>Resource Footprint Performance</h3>", unsafe_allow_html=True)
    
    k1, k2, k3, k4 = st.columns(4)
    
    # Energy
    with k1:
        with st.container(border=True):
            st.markdown("<h4 style='margin: 0 0 10px 0; color: #fb7185;'>⚡ Energy Efficiency</h4>", unsafe_allow_html=True)
            st.metric(
                label="Purchased Grid Power",
                value=f"{optimized['electricity_kwh']:,} kWh/yr",
                delta=f"{int(baseline['electricity_kwh'] - optimized['electricity_kwh']):,} kWh reduction" if (baseline['electricity_kwh'] - optimized['electricity_kwh']) > 0 else None,
                delta_color="inverse"
            )
            st.markdown(f"**Score:** {optimized['scores']['energy']}/100")
            st.markdown(f"**Intensity:** {optimized['kwh_per_student']} kWh/student")
        
    # Water
    with k2:
        with st.container(border=True):
            st.markdown("<h4 style='margin: 0 0 10px 0; color: #38bdf8;'>💧 Water Efficiency</h4>", unsafe_allow_html=True)
            st.metric(
                label="Total Consumed",
                value=f"{int(optimized['water_liters']):,} Liters/yr",
                delta=f"{int(baseline['water_liters'] - optimized['water_liters']):,} L reduction" if (baseline['water_liters'] - optimized['water_liters']) > 0 else None,
                delta_color="inverse"
            )
            st.markdown(f"**Score:** {optimized['scores']['water']}/100")
            st.markdown(f"**Intensity:** {optimized['lpcd']} LPCD per capita")
        
    # Waste
    with k3:
        with st.container(border=True):
            st.markdown("<h4 style='margin: 0 0 10px 0; color: #fb923c;'>♻️ Waste Management</h4>", unsafe_allow_html=True)
            st.metric(
                label="Diversion Rate",
                value=f"{optimized['recycling_rate']}%",
                delta=f"+{optimized['recycling_rate'] - baseline['recycling_rate']}% points" if (optimized['recycling_rate'] - baseline['recycling_rate']) > 0 else None
            )
            st.markdown(f"**Score:** {optimized['scores']['waste']}/100")
            st.markdown(f"**Gen Rate:** {optimized['waste_tons']} Tons/yr")
        
    # Carbon
    with k4:
        with st.container(border=True):
            st.markdown("<h4 style='margin: 0 0 10px 0; color: #a78bfa;'>☁️ Carbon Emissions</h4>", unsafe_allow_html=True)
            st.metric(
                label="Carbon Footprint",
                value=f"{optimized['co2_tons']} tCO2e/yr",
                delta=f"-{round(baseline['co2_tons'] - optimized['co2_tons'], 1)} tons" if (baseline['co2_tons'] - optimized['co2_tons']) > 0 else None,
                delta_color="inverse"
            )
            st.markdown(f"**Score:** {optimized['scores']['carbon']}/100")
            st.markdown(f"**Grid Factor:** {GRID_CO2_FACTOR} kg/kWh")
 
    # ------------------ PLOTLY VISUALIZATION ------------------
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h3 style='margin-top:0; color:#e2e8f0;'>Visualized Comparison: Score Categories</h3>", unsafe_allow_html=True)
        
        categories = ['Energy Efficiency', 'Water Conservation', 'Waste Management', 'Carbon Footprint', 'Overall Score']
        base_scores = [baseline['scores']['energy'], baseline['scores']['water'], baseline['scores']['waste'], baseline['scores']['carbon'], baseline['scores']['overall']]
        opt_scores = [optimized['scores']['energy'], optimized['scores']['water'], optimized['scores']['waste'], optimized['scores']['carbon'], optimized['scores']['overall']]
        
        fig = go.Figure()
        
        # Baseline Bars
        fig.add_trace(go.Bar(
            x=categories,
            y=base_scores,
            name='Baseline Baseline',
            marker_color='#94a3b8',
            opacity=0.8
        ))
        
        # Optimized Bars
        fig.add_trace(go.Bar(
            x=categories,
            y=opt_scores,
            name='Optimized Strategy',
            marker_color='#10b981',
            opacity=0.9
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Outfit'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', range=[0, 100]),
            barmode='group',
            margin=dict(l=40, r=40, t=20, b=20),
            height=320,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # ------------------ RESPONSIBLE AI & ETHICS SECTION ------------------
    st.markdown("<br><hr style='border: 1px solid rgba(255,255,255,0.08);'/><br>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #10b981;'>⚖️ Responsible AI, Transparency & Ethics</h2>", unsafe_allow_html=True)
    
    col_ethics_1, col_ethics_2 = st.columns(2)
    
    with col_ethics_1:
        st.markdown("""
        <div style='background: rgba(16, 185, 129, 0.05); padding: 20px; border-left: 4px solid #10b981; border-radius: 8px;'>
            <h4 style='margin-top:0; color:#34d399;'>Model Governance &amp; Transparency</h4>
            <p style='font-size:0.88rem; line-height:1.6; color:#cbd5e1;'>
                Scores use fixed mathematical formulas calibrated against GRIHA/LEED benchmarks — fully reproducible, no black-box ML. RAG answers are grounded strictly in the local knowledge base.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_ethics_2:
        st.markdown("""
        <div style='background: rgba(239, 68, 68, 0.05); padding: 20px; border-left: 4px solid #ef4444; border-radius: 8px;'>
            <h4 style='margin-top:0; color:#f87171;'>Limitations &amp; Data Privacy</h4>
            <p style='font-size:0.88rem; line-height:1.6; color:#cbd5e1;'>
                Environmental offsets are estimates — real-world results vary. Uploaded documents are processed in-memory only and never stored or shared.
            </p>
        </div>
        """, unsafe_allow_html=True)
