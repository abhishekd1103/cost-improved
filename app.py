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
    page_title="Enhanced DC Cost Estimator v2.0 | Abhishek Diwanji",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS (keeping the successful styling from Perplexity Labs)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
        color: #e2e8f0;
    }
    
    .main-header {
        background: linear-gradient(135deg, #00d4aa 0%, #00a8ff 50%, #0078ff 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 212, 170, 0.3);
    }
    
    .enhanced-badge {
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        color: white;
        display: inline-block;
        margin: 0.5rem;
    }
    
    .pricing-comparison {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .pricing-card {
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.1), rgba(0, 168, 255, 0.1));
        border: 2px solid rgba(0, 212, 170, 0.3);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .pricing-card.competitive {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(254, 202, 87, 0.1));
        border-color: rgba(255, 107, 107, 0.3);
    }
    
    .pricing-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 212, 170, 0.2);
    }
    
    .factor-section {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #00d4aa;
    }
    
    .study-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
        backdrop-filter: blur(12px);
        border: 1px solid rgba(100, 116, 139, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    
    .phase-section {
        background: linear-gradient(135deg, rgba(0, 168, 255, 0.1), rgba(0, 212, 170, 0.1));
        border: 1px solid rgba(0, 168, 255, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .savings-highlight {
        background: linear-gradient(135deg, rgba(254, 202, 87, 0.2), rgba(255, 107, 107, 0.2));
        border: 2px solid rgba(254, 202, 87, 0.4);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Header
st.markdown("""
<div class="main-header">
    <h1>⚡ Enhanced DC Project Cost Estimator v2.0</h1>
    <h2>Advanced Competitive Pricing & Phase-wise Calculation</h2>
    <div class="enhanced-badge">NEW: Dual Pricing Models</div>
    <div class="enhanced-badge">NEW: Dynamic Reporting Costs</div>
    <div class="enhanced-badge">NEW: Phase-wise Methodology</div>
</div>
""", unsafe_allow_html=True)

# Enhanced Sidebar Configuration
st.sidebar.header("🔧 Enhanced Project Configuration")

# Core Load Parameters (from successful Perplexity model)
st.sidebar.subheader("⚡ Load Parameters")
it_capacity = st.sidebar.number_input("IT Capacity (MW)", min_value=0.1, max_value=200.0, value=15.0, step=0.1)
mechanical_load = st.sidebar.number_input("Mechanical Load (MW)", min_value=0.1, max_value=100.0, value=10.0, step=0.1)
house_load = st.sidebar.number_input("House/Auxiliary Load (MW)", min_value=0.1, max_value=50.0, value=5.0, step=0.1)

# Enhanced Bus Count with Custom Override
st.sidebar.subheader("🔌 Bus Count Configuration")
use_custom_bus = st.sidebar.toggle("Override Estimated Bus Count", value=False)
if use_custom_bus:
    custom_bus_count = st.sidebar.number_input("Custom Bus Count", min_value=1, max_value=1000, value=100, step=1)
    st.sidebar.info("Using custom bus count instead of calculated estimate")
else:
    custom_bus_count = None

# Project Configuration
st.sidebar.subheader("🏗️ Project Configuration")
tier_level = st.sidebar.selectbox("Tier Level", ["Tier I", "Tier II", "Tier III", "Tier IV"], index=2)
delivery_type = st.sidebar.selectbox("Delivery Type", ["Standard", "Urgent"])

# NEW: Project Type and Methodology
project_type = st.sidebar.selectbox("Project Type", ["Fresh/New Project", "Phase Extension"])
calculation_methodology = st.sidebar.selectbox("Calculation Methodology", ["Consolidated", "Phase-wise"])

# NEW: Client Type with Premium Factor
client_type = st.sidebar.selectbox("Client Type", ["Normal", "Premium"])
if client_type == "Premium":
    premium_factor = st.sidebar.slider("Premium Client Factor", 1.0, 2.0, 1.3, 0.05)
else:
    premium_factor = 1.0

# Phase-wise Configuration (NEW)
if calculation_methodology == "Phase-wise":
    st.sidebar.subheader("📊 Phase-wise Configuration")
    num_phases = st.sidebar.slider("Number of Phases", 1, 5, 2, 1)
    
    phases = []
    for i in range(num_phases):
        st.sidebar.write(f"**Phase {i+1}:**")
        phase_name = st.sidebar.text_input(f"Phase {i+1} Name", value=f"Phase {i+1}", key=f"phase_name_{i}")
        phase_capacity = st.sidebar.number_input(f"Phase {i+1} Capacity (MW)", 
                                                min_value=0.1, max_value=100.0, 
                                                value=round((it_capacity + mechanical_load + house_load)/num_phases, 1), 
                                                step=0.1, key=f"phase_cap_{i}")
        phases.append({"name": phase_name, "capacity": phase_capacity})

# Studies Selection with Enhanced Configuration
st.sidebar.subheader("📋 Studies Configuration")
studies_config = {
    'load_flow': st.sidebar.checkbox("⚡ Load Flow Study", value=True),
    'short_circuit': st.sidebar.checkbox("⚡ Short Circuit Study", value=True),
    'pdc': st.sidebar.checkbox("🔧 Protective Device Coordination", value=True),
    'arc_flash': st.sidebar.checkbox("🔥 Arc Flash Study", value=True)
}

# NEW: Dynamic Reporting Cost Configuration
st.sidebar.subheader("📄 Dynamic Reporting Configuration")
st.sidebar.write("**Base Report Prices (₹):**")
base_report_costs = {
    'load_flow': st.sidebar.number_input("Load Flow Report Base Price", min_value=5000, max_value=50000, value=18000, step=1000),
    'short_circuit': st.sidebar.number_input("Short Circuit Report Base Price", min_value=5000, max_value=50000, value=22000, step=1000),
    'pdc': st.sidebar.number_input("PDC Report Base Price", min_value=10000, max_value=80000, value=32000, step=2000),
    'arc_flash': st.sidebar.number_input("Arc Flash Report Base Price", min_value=8000, max_value=60000, value=25000, step=1000)
}

report_format = st.sidebar.selectbox("Report Format", ["Basic", "Detailed", "Comprehensive"], index=1)
report_complexity_factor = st.sidebar.slider("Study Complexity Factor for Reports", 0.5, 2.0, 1.0, 0.1)

# Main Content Area
col1, col2 = st.columns([2, 1])

with col1:
    # Study Selection Display
    st.markdown("### 📋 Selected Studies Configuration")
    
    selected_studies = []
    for study_key, selected in studies_config.items():
        if selected:
            selected_studies.append(study_key)
    
    if selected_studies:
        study_names = {
            'load_flow': 'Load Flow Study',
            'short_circuit': 'Short Circuit Study', 
            'pdc': 'Protective Device Coordination',
            'arc_flash': 'Arc Flash Study'
        }
        
        for study in selected_studies:
            st.success(f"✅ {study_names[study]}")
    else:
        st.warning("⚠️ No studies selected")

with col2:
    # Enhanced Competitive Factors Section
    st.markdown("### 🎯 Competitive Pricing Factors")
    
    with st.expander("🔧 Advanced Pricing Controls", expanded=True):
        st.markdown("**Historical Project Benefits:**")
        etap_model_available = st.toggle("ETAP Model Available from Historical Projects")
        etap_discount_factor = st.slider("ETAP Model Discount Factor", 0.70, 0.95, 0.85, 0.01) if etap_model_available else 1.0
        
        typical_modeling_factor = st.slider("Typical Modelling Factor", 0.80, 1.20, 1.0, 0.05)
        
        st.markdown("**Client Relationship Benefits:**")
        repeat_customer = st.toggle("Repeat Customer")
        repeat_discount_factor = st.slider("Repeat Customer Discount", 0.75, 0.95, 0.88, 0.01) if repeat_customer else 1.0
        
        st.markdown("**Project-Specific Factors:**")
        if project_type == "Phase Extension":
            phase_extension_discount = st.slider("Phase Extension Discount", 0.80, 0.95, 0.90, 0.01)
        else:
            phase_extension_discount = 1.0
        
        st.markdown("**Overall Competitive Factor:**")
        overall_competitive_factor = st.slider("Overall Competitive Reduction", 0.75, 0.98, 0.88, 0.01)

# Custom Additional Costs Section
st.markdown("### 💰 Custom Additional Costs")

additional_col1, additional_col2, additional_col3 = st.columns(3)

with additional_col1:
    labels_required = st.toggle("Labels/Stickers Required")
    if labels_required:
        label_count = st.number_input("Number of Labels", min_value=0, max_value=1000, value=50, step=10)
        label_cost_per_unit = st.number_input("Cost per Label (₹)", min_value=50, max_value=500, value=150, step=25)
        total_label_cost = label_count * label_cost_per_unit
    else:
        total_label_cost = 0

with additional_col2:
    site_visits_required = st.toggle("Additional Site Visits")
    if site_visits_required:
        visit_count = st.number_input("Number of Additional Visits", min_value=0, max_value=20, value=3, step=1)
        visit_cost_per_trip = st.number_input("Cost per Visit (₹)", min_value=2000, max_value=25000, value=8000, step=500)
        total_visit_cost = visit_count * visit_cost_per_trip
    else:
        total_visit_cost = 0

with additional_col3:
    other_costs_required = st.toggle("Other Custom Costs")
    if other_costs_required:
        other_cost_description = st.text_input("Description", value="Miscellaneous")
        other_cost_amount = st.number_input("Amount (₹)", min_value=0, max_value=100000, value=5000, step=1000)
    else:
        other_cost_amount = 0

# Enhanced Calculation Engine
def calculate_enhanced_project_costs():
    # Bus Count Calculation (from successful Perplexity model)
    total_load = it_capacity + mechanical_load + house_load
    
    if use_custom_bus and custom_bus_count:
        estimated_buses = custom_bus_count
    else:
        # Tier-based bus estimation (proven from Perplexity Labs)
        tier_multipliers = {"Tier I": 1.5, "Tier II": 1.8, "Tier III": 2.1, "Tier IV": 2.6}
        estimated_buses = math.ceil(total_load * tier_multipliers[tier_level])
    
    # Study Configuration (from successful Perplexity model)
    STUDIES_DATA = {
        'load_flow': {'name': 'Load Flow Study', 'base_hours_per_bus': 0.8, 'complexity': 'Medium', 'emoji': '⚡'},
        'short_circuit': {'name': 'Short Circuit Study', 'base_hours_per_bus': 1.0, 'complexity': 'Medium-High', 'emoji': '⚡'},
        'pdc': {'name': 'Protective Device Coordination', 'base_hours_per_bus': 1.5, 'complexity': 'High', 'emoji': '🔧'},
        'arc_flash': {'name': 'Arc Flash Study', 'base_hours_per_bus': 1.2, 'complexity': 'High', 'emoji': '🔥'}
    }
    
    # Technical multipliers (proven values)
    tier_complexity = {"Tier I": 1.0, "Tier II": 1.15, "Tier III": 1.3, "Tier IV": 1.6}[tier_level]
    delivery_multiplier = 1.3 if delivery_type == "Urgent" else 1.0
    
    # Resource allocation (successful rates from Perplexity)
    l1_rate, l2_rate, l3_rate = 1200, 750, 500
    l1_percentage, l2_percentage, l3_percentage = 0.20, 0.30, 0.50
    
    results = {
        'estimated_buses': estimated_buses,
        'total_load': total_load,
        'studies': {},
        'phase_results': [],
        'standard_cost': 0,
        'competitive_cost': 0,
        'additional_costs': total_label_cost + total_visit_cost + other_cost_amount
    }
    
    # Phase-wise or Consolidated Calculation
    if calculation_methodology == "Phase-wise":
        # Calculate for each phase
        total_standard_cost = 0
        total_hours = 0
        
        for i, phase in enumerate(phases):
            phase_buses = math.ceil(phase['capacity'] * tier_multipliers[tier_level])
            phase_studies = {}
            phase_total_cost = 0
            phase_total_hours = 0
            
            for study_key in selected_studies:
                study_data = STUDIES_DATA[study_key]
                
                # Hours calculation
                study_hours = (phase_buses * study_data['base_hours_per_bus'] * 
                              tier_complexity * delivery_multiplier * typical_modeling_factor)
                
                # Resource allocation
                l1_hours = study_hours * l1_percentage
                l2_hours = study_hours * l2_percentage
                l3_hours = study_hours * l3_percentage
                
                # Labor cost
                labor_cost = (l1_hours * l1_rate + l2_hours * l2_rate + l3_hours * l3_rate)
                
                # NEW: Dynamic report cost calculation
                base_report_cost = base_report_costs[study_key]
                report_format_multiplier = {"Basic": 0.8, "Detailed": 1.0, "Comprehensive": 1.4}[report_format]
                dynamic_report_cost = base_report_cost * report_format_multiplier * report_complexity_factor
                
                # Total study cost for this phase
                study_total_cost = labor_cost + dynamic_report_cost
                phase_total_cost += study_total_cost
                phase_total_hours += study_hours
                
                phase_studies[study_key] = {
                    'name': study_data['name'],
                    'emoji': study_data['emoji'],
                    'hours': study_hours,
                    'labor_cost': labor_cost,
                    'report_cost': dynamic_report_cost,
                    'total_cost': study_total_cost
                }
            
            phase_result = {
                'name': phase['name'],
                'capacity': phase['capacity'],
                'buses': phase_buses,
                'studies': phase_studies,
                'total_hours': phase_total_hours,
                'total_cost': phase_total_cost
            }
            
            results['phase_results'].append(phase_result)
            total_standard_cost += phase_total_cost
            total_hours += phase_total_hours
            
        results['total_hours'] = total_hours
        
    else:
        # Consolidated Calculation (original successful method)
        total_hours = 0
        total_standard_cost = 0
        
        for study_key in selected_studies:
            study_data = STUDIES_DATA[study_key]
            
            # Hours calculation
            study_hours = (estimated_buses * study_data['base_hours_per_bus'] * 
                          tier_complexity * delivery_multiplier * typical_modeling_factor)
            
            # Resource allocation
            l1_hours = study_hours * l1_percentage
            l2_hours = study_hours * l2_percentage  
            l3_hours = study_hours * l3_percentage
            
            # Labor cost
            labor_cost = (l1_hours * l1_rate + l2_hours * l2_rate + l3_hours * l3_rate)
            
            # NEW: Dynamic report cost calculation
            base_report_cost = base_report_costs[study_key]
            report_format_multiplier = {"Basic": 0.8, "Detailed": 1.0, "Comprehensive": 1.4}[report_format]
            dynamic_report_cost = base_report_cost * report_format_multiplier * report_complexity_factor
            
            # Total study cost
            study_total_cost = labor_cost + dynamic_report_cost
            total_standard_cost += study_total_cost
            total_hours += study_hours
            
            results['studies'][study_key] = {
                'name': study_data['name'],
                'emoji': study_data['emoji'],
                'hours': study_hours,
                'l1_hours': l1_hours,
                'l2_hours': l2_hours,
                'l3_hours': l3_hours,
                'labor_cost': labor_cost,
                'report_cost': dynamic_report_cost,
                'total_cost': study_total_cost,
                'complexity': study_data['complexity']
            }
        
        results['total_hours'] = total_hours
    
    # Apply premium client factor
    total_standard_cost *= premium_factor
    
    # Add additional costs
    total_standard_cost += results['additional_costs']
    
    # Apply phase extension discount
    if project_type == "Phase Extension":
        total_standard_cost *= phase_extension_discount
    
    results['standard_cost'] = total_standard_cost
    
    # NEW: Competitive Cost Calculation
    competitive_multiplier = 1.0
    
    if etap_model_available:
        competitive_multiplier *= etap_discount_factor
    
    if repeat_customer:
        competitive_multiplier *= repeat_discount_factor
    
    # Apply overall competitive factor
    competitive_multiplier *= overall_competitive_factor
    
    results['competitive_cost'] = total_standard_cost * competitive_multiplier
    results['savings'] = results['standard_cost'] - results['competitive_cost']
    results['savings_percentage'] = (results['savings'] / results['standard_cost']) * 100 if results['standard_cost'] > 0 else 0
    
    return results

# Calculate Results
if selected_studies:
    results = calculate_enhanced_project_costs()
    
    # Display Key Metrics
    st.markdown("### 📊 Project Summary")
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric("Total Load", f"{results['total_load']:.1f} MW", delta=f"{tier_level}")
    
    with metric_col2:
        st.metric("Estimated Buses", f"{results['estimated_buses']:,}", 
                 delta="Custom" if use_custom_bus else "Auto")
    
    with metric_col3:
        st.metric("Total Hours", f"{results['total_hours']:.0f}", 
                 delta=f"{len(selected_studies)} studies")
    
    with metric_col4:
        st.metric("Methodology", calculation_methodology, 
                 delta=f"{client_type} Client")
    
    # NEW: Dual Pricing Comparison
    st.markdown("### 💰 Dual Pricing Models Comparison")
    
    pricing_col1, pricing_col2 = st.columns(2)
    
    with pricing_col1:
        st.markdown(f"""
        <div class="pricing-card">
            <h3>📋 Standard Pricing</h3>
            <h2 style="color: #00d4aa; font-size: 2.5rem; margin: 1rem 0;">₹{results['standard_cost']:,.0f}</h2>
            <p><strong>Methodology:</strong> {calculation_methodology}</p>
            <p><strong>Client Type:</strong> {client_type}</p>
            <p><strong>Project Type:</strong> {project_type}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with pricing_col2:
        st.markdown(f"""
        <div class="pricing-card competitive">
            <h3>🎯 Competitive Pricing</h3>
            <h2 style="color: #ff6b6b; font-size: 2.5rem; margin: 1rem 0;">₹{results['competitive_cost']:,.0f}</h2>
            <p><strong>ETAP Model:</strong> {'Available' if etap_model_available else 'Not Available'}</p>
            <p><strong>Repeat Customer:</strong> {'Yes' if repeat_customer else 'No'}</p>
            <p><strong>Overall Factor:</strong> {overall_competitive_factor:.0%}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Savings Highlight
    st.markdown(f"""
    <div class="savings-highlight">
        <h3 style="color: #feca57; margin: 0;">💡 Competitive Advantage</h3>
        <h2 style="color: #feca57; font-size: 2rem; margin: 1rem 0;">₹{results['savings']:,.0f} Savings</h2>
        <p style="margin: 0;"><strong>{results['savings_percentage']:.1f}% reduction</strong> from standard pricing</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Phase-wise Results (if applicable)
    if calculation_methodology == "Phase-wise":
        st.markdown("### 📊 Phase-wise Breakdown")
        
        for i, phase in enumerate(results['phase_results']):
            with st.expander(f"📋 {phase['name']} - {phase['capacity']:.1f} MW"):
                
                phase_col1, phase_col2, phase_col3 = st.columns(3)
                
                with phase_col1:
                    st.metric("Phase Capacity", f"{phase['capacity']:.1f} MW")
                    st.metric("Phase Buses", f"{phase['buses']:,}")
                
                with phase_col2:
                    st.metric("Phase Hours", f"{phase['total_hours']:.0f}")
                    st.metric("Studies", f"{len(phase['studies'])}")
                
                with phase_col3:
                    st.metric("Phase Cost", f"₹{phase['total_cost']:,.0f}")
                    st.metric("Avg Cost/Bus", f"₹{phase['total_cost']/phase['buses']:,.0f}")
                
                # Phase studies detail
                st.markdown("**Phase Studies:**")
                for study_key, study in phase['studies'].items():
                    st.write(f"• {study['emoji']} {study['name']}: {study['hours']:.0f}h - ₹{study['total_cost']:,.0f}")
    
    # Consolidated Study Details
    else:
        st.markdown("### 📋 Study-wise Cost Breakdown")
        
        for study_key, study in results['studies'].items():
            competitive_study_cost = study['total_cost'] * overall_competitive_factor
            
            st.markdown(f"""
            <div class="study-card">
                <h4>{study['emoji']} {study['name']}</h4>
                <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem;">
                    <div>
                        <p><strong>Complexity:</strong> {study['complexity']}</p>
                        <p><strong>Total Hours:</strong> {study['hours']:.1f}</p>
                        <p><strong>Labor Cost:</strong> ₹{study['labor_cost']:,.0f}</p>
                        <p><strong>Dynamic Report Cost:</strong> ₹{study['report_cost']:,.0f}</p>
                        <p><em>Report: {report_format} × {report_complexity_factor}x complexity</em></p>
                    </div>
                    <div style="text-align: center;">
                        <div style="background: rgba(0, 212, 170, 0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                            <p style="margin: 0; color: #00d4aa; font-size: 1.2rem; font-weight: bold;">₹{study['total_cost']:,.0f}</p>
                            <small>Standard</small>
                        </div>
                        <div style="background: rgba(255, 107, 107, 0.1); padding: 1rem; border-radius: 8px;">
                            <p style="margin: 0; color: #ff6b6b; font-size: 1.2rem; font-weight: bold;">₹{competitive_study_cost:,.0f}</p>
                            <small>Competitive</small>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Additional Costs Breakdown
    if results['additional_costs'] > 0:
        st.markdown("### 💰 Additional Costs Breakdown")
        
        additional_breakdown = []
        if total_label_cost > 0:
            additional_breakdown.append(f"🏷️ Labels: {label_count} × ₹{label_cost_per_unit} = ₹{total_label_cost:,.0f}")
        if total_visit_cost > 0:
            additional_breakdown.append(f"🚗 Site Visits: {visit_count} × ₹{visit_cost_per_trip} = ₹{total_visit_cost:,.0f}")
        if other_cost_amount > 0:
            additional_breakdown.append(f"📝 {other_cost_description}: ₹{other_cost_amount:,.0f}")
        
        for item in additional_breakdown:
            st.write(f"• {item}")
        
        st.success(f"**Total Additional Costs: ₹{results['additional_costs']:,.0f}**")
    
    # Competitive Factors Summary
    st.markdown("### 🎯 Applied Competitive Factors")
    
    factors_col1, factors_col2 = st.columns(2)
    
    with factors_col1:
        st.markdown("**Cost Reduction Factors:**")
        if etap_model_available:
            st.write(f"• ETAP Model Discount: {(1-etap_discount_factor)*100:.0f}%")
        if repeat_customer:
            st.write(f"• Repeat Customer: {(1-repeat_discount_factor)*100:.0f}%")
        if project_type == "Phase Extension":
            st.write(f"• Phase Extension: {(1-phase_extension_discount)*100:.0f}%")
        st.write(f"• Overall Competitive: {(1-overall_competitive_factor)*100:.0f}%")
    
    with factors_col2:
        st.markdown("**Premium Factors:**")
        if client_type == "Premium":
            st.write(f"• Premium Client: +{(premium_factor-1)*100:.0f}%")
        st.write(f"• Modeling Factor: {typical_modeling_factor:.0%}")
        st.write(f"• Report Complexity: {report_complexity_factor:.0%}")
    
    # Charts
    if len(selected_studies) > 1:
        st.markdown("### 📈 Cost Analysis Charts")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Standard vs Competitive comparison
            if calculation_methodology == "Consolidated":
                study_names = [results['studies'][key]['name'] for key in selected_studies]
                standard_costs = [results['studies'][key]['total_cost'] for key in selected_studies]
                competitive_costs = [cost * overall_competitive_factor for cost in standard_costs]
            else:
                study_names = ["Phase " + str(i+1) for i in range(len(results['phase_results']))]
                standard_costs = [phase['total_cost'] for phase in results['phase_results']]
                competitive_costs = [cost * overall_competitive_factor for cost in standard_costs]
            
            fig_comparison = go.Figure()
            fig_comparison.add_trace(go.Bar(name='Standard', x=study_names, y=standard_costs, marker_color='#00d4aa'))
            fig_comparison.add_trace(go.Bar(name='Competitive', x=study_names, y=competitive_costs, marker_color='#ff6b6b'))
            fig_comparison.update_layout(
                title="Standard vs Competitive Pricing",
                barmode='group',
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_comparison, use_container_width=True)
        
        with chart_col2:
            # Cost distribution pie chart
            if calculation_methodology == "Consolidated":
                costs = [results['studies'][key]['total_cost'] for key in selected_studies]
                names = [results['studies'][key]['name'] for key in selected_studies]
            else:
                costs = [phase['total_cost'] for phase in results['phase_results']]
                names = [phase['name'] for phase in results['phase_results']]
            
            fig_pie = go.Figure(data=[go.Pie(labels=names, values=costs, hole=0.4)])
            fig_pie.update_layout(
                title="Cost Distribution",
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.warning("⚠️ Please select at least one study to see cost estimates.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 2rem;">
    <p style="font-size: 1.2rem; font-weight: 600; color: #00d4aa;">⚡ Enhanced DC Project Cost Estimator v2.0</p>
    <p>🚀 Developed by <strong>Abhishek Diwanji</strong> | Advanced Competitive Pricing & Phase-wise Analysis</p>
    <p style="font-size: 0.9rem;">Built upon the successful Perplexity Labs foundation with enhanced business intelligence</p>
</div>
""", unsafe_allow_html=True)
