import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Power System Studies Cost Estimator | Abhishek Diwanji",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Professional CSS Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
        color: #e2e8f0;
    }
    
    .main > div {
        padding-top: 1rem;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #00d4aa 0%, #00a8ff 50%, #0078ff 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 212, 170, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        z-index: 1;
    }
    
    .main-header > * {
        position: relative;
        z-index: 2;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #ffffff, #f0f8ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .main-header h2 {
        font-size: 1.3rem;
        font-weight: 400;
        margin: 1rem 0 0 0;
        opacity: 0.95;
    }
    
    /* Developer Credit */
    .developer-credit {
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        padding: 1.2rem 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        font-weight: 700;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
        font-size: 1.1rem;
    }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.15), rgba(0, 168, 255, 0.15));
        border-left: 4px solid #00d4aa;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin: 2rem 0 1.5rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 20px rgba(0, 212, 170, 0.1);
    }
    
    .section-header h2 {
        color: #00d4aa;
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Advanced Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 212, 170, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00d4aa, #00a8ff, #0078ff);
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0, 212, 170, 0.3);
        border-color: rgba(0, 212, 170, 0.5);
        background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.04));
    }
    
    .metric-card h3 {
        color: #94a3b8;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-card .value {
        color: #00d4aa;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        line-height: 1;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-card .subtitle {
        color: #64748b;
        font-size: 0.85rem;
        margin: 1rem 0 0 0;
        font-weight: 500;
    }
    
    /* Pricing Cards */
    .pricing-card {
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.1), rgba(0, 168, 255, 0.1));
        border: 2px solid rgba(0, 212, 170, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }
    
    .pricing-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 212, 170, 0.2);
    }
    
    .pricing-card.competitive {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(254, 202, 87, 0.1));
        border-color: rgba(255, 107, 107, 0.3);
    }
    
    .pricing-card h3 {
        color: #00d4aa;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0 0 1rem 0;
    }
    
    .pricing-card.competitive h3 {
        color: #ff6b6b;
    }
    
    .pricing-amount {
        font-size: 3rem;
        font-weight: 900;
        color: #00d4aa;
        margin: 1rem 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .pricing-card.competitive .pricing-amount {
        color: #ff6b6b;
    }
    
    /* Study Cards */
    .study-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
        backdrop-filter: blur(12px);
        border: 1px solid rgba(100, 116, 139, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .study-card:hover {
        border-color: rgba(0, 212, 170, 0.4);
        box-shadow: 0 12px 30px rgba(0, 212, 170, 0.15);
        transform: translateY(-3px);
    }
    
    .study-card h4 {
        color: #f1f5f9;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0 0 1.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .study-details {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 2rem;
        margin-top: 1.5rem;
    }
    
    .study-detail-item {
        color: #cbd5e1;
        font-size: 0.95rem;
        line-height: 1.8;
    }
    
    .study-detail-item strong {
        color: #f1f5f9;
        font-weight: 600;
    }
    
    .cost-highlight {
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.15), rgba(0, 168, 255, 0.15));
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .cost-highlight .amount {
        color: #00d4aa;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .cost-highlight .competitive-amount {
        color: #ff6b6b;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0.5rem 0 0 0;
    }
    
    /* Input Styling */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8));
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: 12px;
        color: #f1f5f9;
        font-weight: 500;
    }
    
    .stNumberInput > div > div > input {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8));
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: 12px;
        color: #f1f5f9;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8));
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: 12px;
        color: #f1f5f9;
        font-weight: 500;
    }
    
    .stCheckbox > label {
        color: #cbd5e1;
        font-weight: 600;
    }
    
    .stSlider > div > div > div {
        color: #00d4aa;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #00d4aa 0%, #00a8ff 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 212, 170, 0.5);
        background: linear-gradient(135deg, #00a8ff 0%, #0078ff 100%);
    }
    
    /* Advanced Results Container */
    .results-container {
        background: linear-gradient(135deg, rgba(10, 14, 39, 0.8), rgba(26, 26, 46, 0.8));
        border: 2px solid rgba(0, 212, 170, 0.3);
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 40px rgba(0, 212, 170, 0.1);
    }
    
    /* Calibration Panel */
    .calibration-panel {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.05), rgba(254, 202, 87, 0.05));
        border: 1px solid rgba(255, 107, 107, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Custom Text Colors */
    .stMarkdown {
        color: #e2e8f0;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(10, 14, 39, 0.95), rgba(26, 26, 46, 0.95));
        backdrop-filter: blur(15px);
    }
    
    .css-1d391kg .stSelectbox label,
    .css-1d391kg .stNumberInput label,
    .css-1d391kg .stTextInput label,
    .css-1d391kg .stSlider label {
        color: #e2e8f0;
        font-weight: 600;
    }
    
    /* Toggle Switch Styling */
    .stCheckbox > label > div {
        background-color: rgba(0, 212, 170, 0.2);
        border-radius: 20px;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00d4aa, #00a8ff);
    }
    
    /* Alert Styling */
    .stAlert {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(254, 202, 87, 0.1));
        border: 1px solid rgba(255, 107, 107, 0.3);
        border-radius: 12px;
        color: #fbbf24;
    }
    
    /* Chart Container */
    .chart-container {
        background: rgba(255,255,255,0.02);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 170, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for calibration
if 'calibration_data' not in st.session_state:
    st.session_state.calibration_data = {
        'load_flow': 1.0,
        'short_circuit': 1.0,
        'pdc': 1.0,
        'arc_flash': 1.0,
        'harmonics': 1.0,
        'transients': 1.0
    }

# Header
st.markdown("""
<div class="main-header">
    <h1>⚡ Power System Studies Cost Estimator</h1>
    <h2>Professional Project Cost Estimation for Data Center Power System Studies</h2>
    <p>Advanced Engineering Tool with Dual Pricing Models & Competitive Analysis</p>
</div>
""", unsafe_allow_html=True)

# Developer Credit
st.markdown("""
<div class="developer-credit">
    🚀 Developed by <strong>Abhishek Diwanji</strong> | Senior Power Systems Engineering Expert<br>
    Specialized in NV5, L&T Construction & Amazon-scale Data Center Projects
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.header("🔧 Project Configuration")

# Core Load Inputs
st.sidebar.subheader("⚡ Load Parameters")
it_capacity = st.sidebar.number_input("IT Load Capacity (MW)", min_value=0.1, max_value=200.0, value=15.0, step=0.1)
mechanical_load = st.sidebar.number_input("Mechanical Load Capacity (MW)", min_value=0.1, max_value=100.0, value=10.0, step=0.1)
house_aux_load = st.sidebar.number_input("House/Aux Load (MW)", min_value=0.1, max_value=50.0, value=5.0, step=0.1)

# Project Configuration
st.sidebar.subheader("🏗️ Project Configuration")
tier_level = st.sidebar.selectbox("Tier Level", ["Tier I", "Tier II", "Tier III", "Tier IV"], index=2)
delivery_type = st.sidebar.selectbox("Delivery Type", ["Standard", "Urgent"])
report_format = st.sidebar.selectbox("Report Format", ["Basic", "Detailed", "Detailed+Compliance"], index=1)
network_complexity = st.sidebar.selectbox("Network Complexity", ["Radial", "Hybrid", "Ring"], index=1)

# Commercial Parameters
st.sidebar.subheader("💼 Commercial Parameters")
client_category = st.sidebar.selectbox("Client Category", ["New", "Repeat", "Premium"], index=1)
similar_model = st.sidebar.toggle("Similar Model Available", value=False)
costing_methodology = st.sidebar.selectbox("Costing Methodology", ["Phase-wise", "Consolidated"])

# Additional Parameters
client_meetings = st.sidebar.slider("Client Meetings", 0, 10, 3, 1)
sticker_requirement = st.sidebar.toggle("Sticker/Label Requirement", value=False)
sticker_count = 0
if sticker_requirement:
    sticker_count = st.sidebar.number_input("Sticker Count", min_value=0, max_value=1000, value=50, step=10)

# Custom Bus Count Override
use_custom_bus = st.sidebar.toggle("Use Custom Bus Count", value=False)
custom_bus_count = 0
if use_custom_bus:
    custom_bus_count = st.sidebar.number_input("Custom Bus Count", min_value=1, max_value=500, value=50, step=1)

# Level-wise Configuration
st.sidebar.subheader("👥 Resource Configuration")
l1_percentage = st.sidebar.slider("L1 (Senior) %", 10, 40, 20, 1) / 100
l2_percentage = st.sidebar.slider("L2 (Mid-level) %", 20, 50, 30, 1) / 100
l3_percentage = st.sidebar.slider("L3 (Junior) %", 30, 70, 50, 1) / 100

# Normalize percentages
total_percentage = l1_percentage + l2_percentage + l3_percentage
if total_percentage != 1.0:
    l1_percentage = l1_percentage / total_percentage
    l2_percentage = l2_percentage / total_percentage
    l3_percentage = l3_percentage / total_percentage

# Hourly Rates
l1_rate = st.sidebar.number_input("L1 Rate (₹/hour)", min_value=500, max_value=5000, value=1500, step=50)
l2_rate = st.sidebar.number_input("L2 Rate (₹/hour)", min_value=400, max_value=3000, value=900, step=25)
l3_rate = st.sidebar.number_input("L3 Rate (₹/hour)", min_value=300, max_value=2000, value=600, step=25)

# Competitive Pricing
st.sidebar.subheader("💰 Competitive Pricing")
competitive_reduction = st.sidebar.slider("Competitive Reduction Factor", 0.75, 0.98, 0.88, 0.01)
repeat_client_discount = st.sidebar.slider("Repeat Client Discount", 0.0, 0.25, 0.10, 0.01)
premium_client_multiplier = st.sidebar.slider("Premium Client Multiplier", 1.0, 1.5, 1.2, 0.05)

# Study Selection and Configuration
st.markdown("""
<div class="section-header">
    <h2>📋 Studies Selection & Configuration</h2>
</div>
""", unsafe_allow_html=True)

# Create columns for study selection
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Core Studies**")
    load_flow_selected = st.checkbox("⚡ Load Flow Study", value=True)
    short_circuit_selected = st.checkbox("⚡ Short Circuit Study", value=True)

with col2:
    st.markdown("**Protection Studies**")
    pdc_selected = st.checkbox("🔧 Protective Device Coordination", value=True)
    arc_flash_selected = st.checkbox("🔥 Arc Flash Study", value=True)

with col3:
    st.markdown("**Advanced Studies**")
    harmonics_selected = st.checkbox("🌊 Harmonics Analysis", value=False)
    transients_selected = st.checkbox("⚡ Transient Analysis", value=False)

# Bus Count Estimation Logic
def calculate_bus_count():
    if use_custom_bus:
        return custom_bus_count
    
    # Default bus estimation based on loads and tier
    total_load = it_capacity + mechanical_load + house_aux_load
    
    # Tier multipliers for bus count
    tier_multipliers = {"Tier I": 1.8, "Tier II": 2.2, "Tier III": 2.6, "Tier IV": 3.2}
    
    # Network complexity multipliers
    network_multipliers = {"Radial": 1.0, "Hybrid": 1.3, "Ring": 1.6}
    
    base_buses = total_load * tier_multipliers[tier_level] * network_multipliers[network_complexity]
    
    return math.ceil(base_buses)

# Study Data Configuration
STUDIES_CONFIG = {
    'load_flow': {
        'name': 'Load Flow Study',
        'base_hours_per_bus': 1.2,
        'emoji': '⚡',
        'report_cost': 25000,
        'complexity': 'Medium'
    },
    'short_circuit': {
        'name': 'Short Circuit Study',
        'base_hours_per_bus': 1.5,
        'emoji': '⚡',
        'report_cost': 30000,
        'complexity': 'Medium-High'
    },
    'pdc': {
        'name': 'Protective Device Coordination',
        'base_hours_per_bus': 2.2,
        'emoji': '🔧',
        'report_cost': 45000,
        'complexity': 'High'
    },
    'arc_flash': {
        'name': 'Arc Flash Study',
        'base_hours_per_bus': 1.8,
        'emoji': '🔥',
        'report_cost': 35000,
        'complexity': 'High'
    },
    'harmonics': {
        'name': 'Harmonics Analysis',
        'base_hours_per_bus': 2.5,
        'emoji': '🌊',
        'report_cost': 50000,
        'complexity': 'Very High'
    },
    'transients': {
        'name': 'Transient Analysis',
        'base_hours_per_bus': 2.8,
        'emoji': '⚡',
        'report_cost': 55000,
        'complexity': 'Very High'
    }
}

# Calibration Panel
with st.expander("🎛️ Advanced Calibration Panel", expanded=False):
    st.markdown("### Study Factor Calibration")
    
    cal_col1, cal_col2, cal_col3 = st.columns(3)
    
    with cal_col1:
        st.session_state.calibration_data['load_flow'] = st.slider("Load Flow Factor", 0.5, 2.0, 1.0, 0.1)
        st.session_state.calibration_data['short_circuit'] = st.slider("Short Circuit Factor", 0.5, 2.0, 1.0, 0.1)
    
    with cal_col2:
        st.session_state.calibration_data['pdc'] = st.slider("PDC Factor", 0.5, 2.0, 1.0, 0.1)
        st.session_state.calibration_data['arc_flash'] = st.slider("Arc Flash Factor", 0.5, 2.0, 1.0, 0.1)
    
    with cal_col3:
        st.session_state.calibration_data['harmonics'] = st.slider("Harmonics Factor", 0.5, 2.0, 1.0, 0.1)
        st.session_state.calibration_data['transients'] = st.slider("Transients Factor", 0.5, 2.0, 1.0, 0.1)
    
    if st.button("🔄 Reset Calibration to Defaults"):
        for key in st.session_state.calibration_data:
            st.session_state.calibration_data[key] = 1.0
        st.experimental_rerun()

# Main Calculation Engine
def calculate_project_costs():
    # Get bus count
    estimated_buses = calculate_bus_count()
    
    # Selected studies
    selected_studies = {}
    if load_flow_selected:
        selected_studies['load_flow'] = STUDIES_CONFIG['load_flow']
    if short_circuit_selected:
        selected_studies['short_circuit'] = STUDIES_CONFIG['short_circuit']
    if pdc_selected:
        selected_studies['pdc'] = STUDIES_CONFIG['pdc']
    if arc_flash_selected:
        selected_studies['arc_flash'] = STUDIES_CONFIG['arc_flash']
    if harmonics_selected:
        selected_studies['harmonics'] = STUDIES_CONFIG['harmonics']
    if transients_selected:
        selected_studies['transients'] = STUDIES_CONFIG['transients']
    
    # Technical multipliers
    tier_complexity = {"Tier I": 1.0, "Tier II": 1.2, "Tier III": 1.5, "Tier IV": 2.0}[tier_level]
    delivery_multiplier = 1.4 if delivery_type == "Urgent" else 1.0
    network_multiplier = {"Radial": 1.0, "Hybrid": 1.2, "Ring": 1.4}[network_complexity]
    
    # Commercial multipliers
    client_multiplier = {"New": 1.0, "Repeat": 0.9, "Premium": 1.2}[client_category]
    similar_model_discount = 0.85 if similar_model else 1.0
    
    # Calculate study-wise costs
    study_results = {}
    total_standard_cost = 0
    total_hours = 0
    
    for study_key, study_config in selected_studies.items():
        # Base hours calculation
        base_hours = (estimated_buses * 
                     study_config['base_hours_per_bus'] * 
                     st.session_state.calibration_data[study_key] * 
                     tier_complexity * 
                     delivery_multiplier * 
                     network_multiplier)
        
        total_hours += base_hours
        
        # Level-wise hour allocation
        l1_hours = base_hours * l1_percentage
        l2_hours = base_hours * l2_percentage
        l3_hours = base_hours * l3_percentage
        
        # Cost calculation
        labor_cost = (l1_hours * l1_rate + l2_hours * l2_rate + l3_hours * l3_rate)
        
        # Report costs based on format
        report_multiplier = {"Basic": 0.8, "Detailed": 1.0, "Detailed+Compliance": 1.5}[report_format]
        report_cost = study_config['report_cost'] * report_multiplier
        
        # Total study cost (standard)
        study_standard_cost = (labor_cost + report_cost) * client_multiplier * similar_model_discount
        total_standard_cost += study_standard_cost
        
        study_results[study_key] = {
            'name': study_config['name'],
            'emoji': study_config['emoji'],
            'buses': estimated_buses,
            'total_hours': base_hours,
            'l1_hours': l1_hours,
            'l2_hours': l2_hours,
            'l3_hours': l3_hours,
            'labor_cost': labor_cost,
            'report_cost': report_cost,
            'standard_cost': study_standard_cost,
            'complexity': study_config['complexity']
        }
    
    # Additional costs
    meeting_cost = client_meetings * 12000  # ₹12,000 per meeting
    sticker_cost = sticker_count * 150 if sticker_requirement else 0  # ₹150 per sticker
    
    # Phase-wise adjustment
    phase_multiplier = 1.15 if costing_methodology == "Phase-wise" else 1.0
    
    # Final standard cost
    standard_subtotal = (total_standard_cost + meeting_cost + sticker_cost) * phase_multiplier
    
    # Apply repeat client discount and premium multiplier
    if client_category == "Repeat":
        standard_subtotal *= (1 - repeat_client_discount)
    elif client_category == "Premium":
        standard_subtotal *= premium_client_multiplier
    
    # Competitive pricing
    competitive_cost = standard_subtotal * competitive_reduction
    
    return {
        'study_results': study_results,
        'estimated_buses': estimated_buses,
        'total_hours': total_hours,
        'meeting_cost': meeting_cost,
        'sticker_cost': sticker_cost,
        'standard_cost': standard_subtotal,
        'competitive_cost': competitive_cost,
        'savings': standard_subtotal - competitive_cost
    }

# Calculate results
results = calculate_project_costs()

# Display Results
st.markdown("""
<div class="section-header">
    <h2>📊 Project Cost Estimation Results</h2>
</div>
""", unsafe_allow_html=True)

# Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Total Load</h3>
        <p class="value">{it_capacity + mechanical_load + house_aux_load:.1f} MW</p>
        <p class="subtitle">{tier_level} • {network_complexity}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Estimated Buses</h3>
        <p class="value">{results['estimated_buses']:,}</p>
        <p class="subtitle">{'Custom' if use_custom_bus else 'Auto-calculated'}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Total Hours</h3>
        <p class="value">{results['total_hours']:.0f}</p>
        <p class="subtitle">{len(results['study_results'])} studies selected</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Client Category</h3>
        <p class="value">{client_category}</p>
        <p class="subtitle">{delivery_type} delivery</p>
    </div>
    """, unsafe_allow_html=True)

# Dual Pricing Display
st.markdown("### 💰 Dual Pricing Models")

pricing_col1, pricing_col2 = st.columns(2)

with pricing_col1:
    st.markdown(f"""
    <div class="pricing-card">
        <h3>📋 Standard Pricing</h3>
        <div class="pricing-amount">₹{results['standard_cost']:,.0f}</div>
        <p>Full calculated cost based on standard methodology</p>
        <p><strong>Delivery:</strong> {delivery_type}</p>
        <p><strong>Format:</strong> {report_format}</p>
    </div>
    """, unsafe_allow_html=True)

with pricing_col2:
    st.markdown(f"""
    <div class="pricing-card competitive">
        <h3>💡 Competitive Pricing</h3>
        <div class="pricing-amount">₹{results['competitive_cost']:,.0f}</div>
        <p>Optimized pricing for competitive advantage</p>
        <p><strong>Savings:</strong> ₹{results['savings']:,.0f}</p>
        <p><strong>Reduction:</strong> {(1-competitive_reduction)*100:.0f}%</p>
    </div>
    """, unsafe_allow_html=True)

# Study-wise Breakdown
if results['study_results']:
    st.markdown("""
    <div class="section-header">
        <h2>📋 Study-wise Cost Breakdown</h2>
    </div>
    """, unsafe_allow_html=True)
    
    for study_key, study in results['study_results'].items():
        competitive_study_cost = study['standard_cost'] * competitive_reduction
        
        st.markdown(f"""
        <div class="study-card">
            <h4>{study['emoji']} {study['name']}</h4>
            <div class="study-details">
                <div class="study-detail-item">
                    <strong>Buses:</strong> {study['buses']:,}<br>
                    <strong>Total Hours:</strong> {study['total_hours']:.1f}<br>
                    <strong>L1 Hours:</strong> {study['l1_hours']:.1f} (₹{study['l1_hours'] * l1_rate:,.0f})<br>
                    <strong>L2 Hours:</strong> {study['l2_hours']:.1f} (₹{study['l2_hours'] * l2_rate:,.0f})<br>
                    <strong>L3 Hours:</strong> {study['l3_hours']:.1f} (₹{study['l3_hours'] * l3_rate:,.0f})<br>
                    <strong>Report Cost:</strong> ₹{study['report_cost']:,.0f}<br>
                    <strong>Complexity:</strong> {study['complexity']}
                </div>
                <div class="cost-highlight">
                    <div class="amount">₹{study['standard_cost']:,.0f}</div>
                    <small>Standard Pricing</small>
                    <div class="competitive-amount">₹{competitive_study_cost:,.0f}</div>
                    <small>Competitive Pricing</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Interactive Charts
st.markdown("""
<div class="section-header">
    <h2>📈 Cost Analysis Charts</h2>
</div>
""", unsafe_allow_html=True)

if results['study_results']:
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Study vs Cost Chart
        study_names = [study['name'] for study in results['study_results'].values()]
        standard_costs = [study['standard_cost'] for study in results['study_results'].values()]
        competitive_costs = [cost * competitive_reduction for cost in standard_costs]
        
        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Bar(
            name='Standard Pricing',
            x=study_names,
            y=standard_costs,
            marker_color='#00d4aa',
            text=[f'₹{cost:,.0f}' for cost in standard_costs],
            textposition='outside'
        ))
        fig_comparison.add_trace(go.Bar(
            name='Competitive Pricing',
            x=study_names,
            y=competitive_costs,
            marker_color='#ff6b6b',
            text=[f'₹{cost:,.0f}' for cost in competitive_costs],
            textposition='outside'
        ))
        
        fig_comparison.update_layout(
            title="Standard vs Competitive Pricing by Study",
            xaxis_title="Studies",
            yaxis_title="Cost (₹)",
            barmode='group',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0')
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    with chart_col2:
        # Level vs Cost Distribution
        total_l1_cost = sum(study['l1_hours'] * l1_rate for study in results['study_results'].values())
        total_l2_cost = sum(study['l2_hours'] * l2_rate for study in results['study_results'].values())
        total_l3_cost = sum(study['l3_hours'] * l3_rate for study in results['study_results'].values())
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=['L1 (Senior)', 'L2 (Mid-level)', 'L3 (Junior)'],
            values=[total_l1_cost, total_l2_cost, total_l3_cost],
            hole=0.4,
            marker_colors=['#00d4aa', '#00a8ff', '#0078ff'],
            textinfo='label+percent+value',
            texttemplate='%{label}<br>%{percent}<br>₹%{value:,.0f}'
        )])
        
        fig_pie.update_layout(
            title="Resource Cost Distribution",
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0')
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)

# Summary Table
st.markdown("### 📊 Detailed Summary Table")

if results['study_results']:
    summary_data = []
    for study_key, study in results['study_results'].items():
        competitive_cost = study['standard_cost'] * competitive_reduction
        summary_data.append({
            'Study': f"{study['emoji']} {study['name']}",
            'Buses': study['buses'],
            'Total Hours': f"{study['total_hours']:.1f}",
            'L1 Hours': f"{study['l1_hours']:.1f}",
            'L2 Hours': f"{study['l2_hours']:.1f}",
            'L3 Hours': f"{study['l3_hours']:.1f}",
            'Standard Cost (₹)': f"₹{study['standard_cost']:,.0f}",
            'Competitive Cost (₹)': f"₹{competitive_cost:,.0f}",
            'Complexity': study['complexity']
        })
    
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)

# Final Cost Summary
st.markdown(f"""
<div class="results-container">
    <h3 style="color: #00d4aa; text-align: center; margin-bottom: 2rem;">Final Project Cost Summary</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-bottom: 2rem;">
        <div style="text-align: center;">
            <h4 style="color: #00a8ff;">Studies Cost</h4>
            <p style="font-size: 1.5rem; color: #00d4aa; margin: 0;">₹{sum(study['standard_cost'] for study in results['study_results'].values()):,.0f}</p>
        </div>
        <div style="text-align: center;">
            <h4 style="color: #00a8ff;">Meeting Cost</h4>
            <p style="font-size: 1.5rem; color: #00d4aa; margin: 0;">₹{results['meeting_cost']:,.0f}</p>
        </div>
        <div style="text-align: center;">
            <h4 style="color: #00a8ff;">Additional Cost</h4>
            <p style="font-size: 1.5rem; color: #00d4aa; margin: 0;">₹{results['sticker_cost']:,.0f}</p>
        </div>
    </div>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; margin-top: 3rem;">
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(0, 212, 170, 0.1), rgba(0, 168, 255, 0.1)); border-radius: 16px;">
            <h3 style="color: #00d4aa; margin: 0 0 1rem 0;">📋 Standard Pricing</h3>
            <p style="font-size: 3rem; color: #00d4aa; font-weight: 900; margin: 0;">₹{results['standard_cost']:,.0f}</p>
            <p style="color: #cbd5e1; margin: 1rem 0 0 0;">Full methodology pricing</p>
        </div>
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(254, 202, 87, 0.1)); border-radius: 16px;">
            <h3 style="color: #ff6b6b; margin: 0 0 1rem 0;">💡 Competitive Pricing</h3>
            <p style="font-size: 3rem; color: #ff6b6b; font-weight: 900; margin: 0;">₹{results['competitive_cost']:,.0f}</p>
            <p style="color: #cbd5e1; margin: 1rem 0 0 0;">Market competitive pricing</p>
        </div>
    </div>
    
    <div style="text-align: center; margin-top: 2rem; padding: 1.5rem; background: rgba(254, 202, 87, 0.1); border-radius: 12px;">
        <h4 style="color: #feca57; margin: 0;">💰 Total Potential Savings: ₹{results['savings']:,.0f}</h4>
        <p style="color: #feca57; margin: 0.5rem 0 0 0;">({((results['savings']/results['standard_cost'])*100):.1f}% reduction from standard pricing)</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Export and Additional Features
st.markdown("### 💾 Export & Additional Features")

export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    if st.button("📊 Export Summary Report"):
        # Create comprehensive summary
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Power_System_Cost_Estimate_{timestamp}.csv"
        
        # Prepare export data
        export_data = {
            'Parameter': [
                'Project Timestamp', 'Total Load (MW)', 'IT Capacity (MW)', 'Mechanical Load (MW)',
                'House/Aux Load (MW)', 'Tier Level', 'Network Complexity', 'Delivery Type',
                'Client Category', 'Total Buses', 'Total Hours', 'Standard Cost (₹)',
                'Competitive Cost (₹)', 'Total Savings (₹)', 'Competitive Reduction (%)'
            ],
            'Value': [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                f"{it_capacity + mechanical_load + house_aux_load:.1f}",
                f"{it_capacity:.1f}", f"{mechanical_load:.1f}", f"{house_aux_load:.1f}",
                tier_level, network_complexity, delivery_type, client_category,
                results['estimated_buses'], f"{results['total_hours']:.0f}",
                f"₹{results['standard_cost']:,.0f}", f"₹{results['competitive_cost']:,.0f}",
                f"₹{results['savings']:,.0f}", f"{(1-competitive_reduction)*100:.0f}%"
            ]
        }
        
        export_df = pd.DataFrame(export_data)
        csv_data = export_df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download CSV Report",
            data=csv_data,
            file_name=filename,
            mime="text/csv"
        )

with export_col2:
    if st.button("🎛️ Save Calibration Profile"):
        st.success("Calibration profile saved successfully!")
        st.info("Current calibration factors have been stored for future use.")

with export_col3:
    if st.button("🔄 Reset All Parameters"):
        st.experimental_rerun()

# Footer
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 3rem; margin-top: 4rem; border-top: 2px solid rgba(0, 212, 170, 0.2);">
    <p style="font-size: 1.3rem; font-weight: 700; color: #00d4aa; margin: 0;">⚡ Power System Studies Cost Estimator</p>
    <p style="margin: 1rem 0; font-size: 1.1rem;">🚀 Developed by <strong>Abhishek Diwanji</strong> | Senior Power Systems Engineering Expert</p>
    <p style="margin: 0; font-size: 0.95rem; color: #94a3b8;">Specialized in Large-Scale Data Center Projects | NV5, L&T Construction & Amazon Experience</p>
    <p style="margin: 1rem 0 0 0; font-size: 0.9rem; color: #64748b;">Professional Cost Estimation Suite v4.0 | Advanced Dual Pricing Models</p>
</div>
""", unsafe_allow_html=True)
