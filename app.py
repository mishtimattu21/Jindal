"""
CSR Dashboard - Professional Dashboard Application
Main Streamlit application for CSR data management and visualization
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
from data_loader import DataLoader
import os

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="JSPL CSR Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None  # Hide default menu but keep sidebar
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main styling */
    .main {
        padding: 2rem 2rem;
    }
    
    /* Header styling */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .dashboard-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .dashboard-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 0.5rem 0;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Progress bar styling */
    .progress-container {
        background: #f0f0f0;
        border-radius: 10px;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    
    /* Status badges */
    .status-on-track {
        background: #10b981;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-at-risk {
        background: #f59e0b;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-delayed {
        background: #ef4444;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 2rem;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Table styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Form styling */
    .stSelectbox, .stTextInput, .stDateInput, .stTextArea {
        margin-bottom: 1rem;
    }
    
    /* Hide Streamlit default elements - but keep sidebar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Dark Sidebar Theme - Black/Dark Grey Background */
    section[data-testid="stSidebar"] {
        visibility: visible !important;
        display: block !important;
        background-color: #1a1a1a !important;
        color: white !important;
    }
    
    /* Sidebar content container */
    [data-testid="stSidebar"] > div {
        visibility: visible !important;
        background-color: #1a1a1a !important;
    }
    
    /* All text in sidebar - white by default */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h2 {
        color: #667eea !important;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #b0b0b0 !important;
    }
    
    [data-testid="stSidebar"] p {
        color: #b0b0b0 !important;
    }
    
    /* Navigation radio buttons - CRITICAL: Make text visible */
    [data-testid="stSidebar"] .stRadio {
        visibility: visible !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: white !important;
        background-color: transparent !important;
    }
    
    /* Radio button text labels - MUST be visible */
    [data-testid="stSidebar"] .stRadio label p {
        color: white !important;
        visibility: visible !important;
        opacity: 1 !important;
        display: block !important;
    }
    
    [data-testid="stSidebar"] .stRadio label > div {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stRadio label > div > p {
        color: white !important;
        visibility: visible !important;
    }
    
    /* Selected/active navigation item - purple highlight */
    [data-testid="stSidebar"] .stRadio label:has(input:checked) {
        background-color: #667eea !important;
        color: white !important;
        border-radius: 5px;
        padding: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stRadio label:has(input:checked) p {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Hover state */
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: #2d2d2d !important;
        border-radius: 5px;
    }
    
    /* Selectbox styling */
    [data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #2d2d2d !important;
        color: white !important;
    }
    
    /* Markdown text */
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        color: #b0b0b0 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown strong {
        color: white !important;
    }
    
    /* Alert/Info boxes */
    [data-testid="stSidebar"] .stAlert {
        background-color: #2d2d2d !important;
        border-color: #444 !important;
        color: white !important;
    }
    
    /* Dividers */
    [data-testid="stSidebar"] hr {
        border-color: #444 !important;
    }
    
    /* Radio button input styling */
    [data-testid="stSidebar"] .stRadio input[type="radio"] {
        accent-color: #667eea !important;
    }
    
    .css-1d391kg {
        padding-top: 2rem;
        background-color: #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loader' not in st.session_state:
    csr_mis_path = "CSR MIS.xlsx"
    jspl_input_path = "JSPL CSR Data Input.xlsx"
    
    # Check if files exist
    if not os.path.exists(csr_mis_path):
        st.error(f"❌ File not found: {csr_mis_path}")
        st.info(f"Current directory: {os.getcwd()}")
        st.info(f"Please ensure the Excel file is in: {os.path.abspath(csr_mis_path)}")
        st.stop()
    
    if not os.path.exists(jspl_input_path):
        st.error(f"❌ File not found: {jspl_input_path}")
        st.info(f"Current directory: {os.getcwd()}")
        st.info(f"Please ensure the Excel file is in: {os.path.abspath(jspl_input_path)}")
        st.stop()
    
    # Load data with progress indicator
    try:
        with st.spinner("🔄 Loading Excel files... This may take a moment."):
            st.session_state.data_loader = DataLoader(csr_mis_path, jspl_input_path)
            loaded_keys = len(st.session_state.data_loader.get_all_keys())
            if loaded_keys > 0:
                st.success(f"✅ Successfully loaded {loaded_keys} data sheets!")
            else:
                st.warning("⚠️ No data sheets were loaded. Please check your Excel files.")
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.exception(e)
        st.info("💡 Troubleshooting tips:")
        st.info("1. Make sure both Excel files are not open in another program")
        st.info("2. Check that the files are not corrupted")
        st.info("3. Verify the file names match exactly: 'CSR MIS.xlsx' and 'JSPL CSR Data Input.xlsx'")
        st.stop()

def calculate_kpis(data_loader):
    """Calculate KPIs from the data"""
    kpis = {}
    
    # Try to get program data and calculate metrics
    programs = ['JindalArogym', 'Kishori Express', 'Vatsalya', 'Subhangi', 'Swasti Express']
    
    for program in programs:
        df = data_loader.get_program_data(program)
        if df is not None and not df.empty:
            # Calculate various metrics based on available columns
            kpis[program] = {
                'total_records': len(df),
                'columns': list(df.columns)
            }
    
    return kpis

def render_kpi_card(title, value, subtitle="", color="#667eea"):
    """Render a KPI card"""
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: {color};">
        <div class="kpi-label">{title}</div>
        <div class="kpi-value">{value}</div>
        {f'<div style="color: #666; font-size: 0.9rem;">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def render_progress_bar(current, target, label):
    """Render a progress bar with status"""
    if target == 0:
        percentage = 0
    else:
        percentage = min((current / target) * 100, 100)
    
    # Determine status
    if percentage >= 90:
        status = "On track"
        status_class = "status-on-track"
        bar_color = "#10b981"
    elif percentage >= 50:
        status = "On track"
        status_class = "status-on-track"
        bar_color = "#10b981"
    else:
        status = "At risk"
        status_class = "status-at-risk"
        bar_color = "#f59e0b"
    
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-weight: 600;">{label}</span>
            <span class="{status_class}">{status}</span>
        </div>
        <div style="background: #f0f0f0; border-radius: 10px; height: 30px; position: relative; overflow: hidden;">
            <div style="background: {bar_color}; height: 100%; width: {percentage}%; transition: width 0.3s ease; display: flex; align-items: center; justify-content: flex-end; padding-right: 10px;">
                <span style="color: white; font-weight: 600; font-size: 0.85rem;">{current}/{target}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_donut_chart(labels, values, title, colors=None):
    """Create a donut chart"""
    if colors is None:
        colors = px.colors.qualitative.Set3
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textposition='outside'
    )])
    
    fig.update_layout(
        title=title,
        showlegend=True,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(size=12)
    )
    
    return fig

def create_bar_chart(df, x_col, y_col, title, color="#667eea"):
    """Create a bar chart"""
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=title,
        color_discrete_sequence=[color],
        text=y_col
    )
    
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(size=12),
        showlegend=False
    )
    
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    
    return fig

def create_stacked_bar_chart(df, x_col, y_col, color_col, title, colors=None):
    """Create a stacked bar chart"""
    if colors is None:
        colors = ["#ff6b6b", "#4ecdc4", "#45b7d1", "#f9ca24"]
    
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        color_discrete_sequence=colors,
        text=y_col
    )
    
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(size=12),
        barmode='stack'
    )
    
    return fig

def create_waterfall_chart(categories, values, title):
    """Create a waterfall chart"""
    fig = go.Figure()
    
    # Calculate cumulative values
    cumulative = [0]
    for i, val in enumerate(values[:-1]):
        cumulative.append(cumulative[-1] + val)
    
    # Add bars
    for i, (cat, val, cum) in enumerate(zip(categories, values, cumulative)):
        if i == len(categories) - 1:  # Total bar
            fig.add_trace(go.Bar(
                name=categories[i],
                x=[categories[i]],
                y=[values[i]],
                marker_color='#95a5a6',
                text=[f"{values[i]:.2f}"],
                textposition='outside'
            ))
        else:
            fig.add_trace(go.Bar(
                name=categories[i],
                x=[categories[i]],
                y=[values[i]],
                base=[cum],
                marker_color='#10b981',
                text=[f"{values[i]:.2f}"],
                textposition='outside'
            ))
    
    fig.update_layout(
        title=title,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(size=12),
        showlegend=False,
        barmode='relative'
    )
    
    return fig

def create_sunburst_chart(labels, parents, values, title):
    """Create a sunburst/nested donut chart"""
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        hovertemplate='<b>%{label}</b><br>Value: %{value}<extra></extra>',
    ))
    
    fig.update_layout(
        title=title,
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(size=12)
    )
    
    return fig

def overview_page(data_loader):
    """Overview/KPI Dashboard Page"""
    try:
        st.markdown("""
        <div class="dashboard-header">
            <h1>📊 CSR Dashboard Overview</h1>
            <p>Comprehensive view of all CSR programs and key performance indicators</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate KPIs
        with st.spinner("Calculating KPIs..."):
            kpis = calculate_kpis(data_loader)
    except Exception as e:
        st.error(f"Error loading overview page: {str(e)}")
        st.exception(e)
        return
    
    # KPI Cards Row 1
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_programs = len([k for k in kpis.keys() if kpis[k].get('total_records', 0) > 0])
        if total_programs == 0:
            total_programs = len(data_loader.get_all_keys())
        render_kpi_card("Active Programs", total_programs, "Programs with data", "#667eea")
    
    with col2:
        total_records = sum([kpis[k].get('total_records', 0) for k in kpis.keys()])
        if total_records == 0:
            # Count total rows across all sheets
            for key in data_loader.get_all_keys():
                df = data_loader.get_data(key)
                if df is not None and not df.empty:
                    total_records += len(df)
        render_kpi_card("Total Records", f"{total_records:,}", "All programs combined", "#10b981")
    
    with col3:
        # Calculate beneficiaries if available
        beneficiaries = 0
        try:
            for key in data_loader.get_all_keys():
                df = data_loader.get_data(key)
                if df is not None and not df.empty:
                    # Look for beneficiary-related columns
                    for col in df.columns:
                        if 'beneficiary' in col.lower() or 'screened' in col.lower():
                            try:
                                if df[col].dtype in ['int64', 'float64']:
                                    beneficiaries += df[col].sum()
                            except:
                                pass
        except:
            pass
        render_kpi_card("Beneficiaries", f"{int(beneficiaries):,}", "Total beneficiaries", "#f59e0b")
    
    with col4:
        # Last updated date
        last_updated = datetime.now().strftime("%d-%m-%Y")
        render_kpi_card("Last Updated", last_updated, "Data refresh date", "#ef4444")
    
    st.markdown("---")
    
    # KPI Progress Indicators
    st.markdown("### 📈 Key Performance Indicators")
    
    # Sample KPI data - in real implementation, this would come from actual data
    kpi_data = [
        {"indicator": "Improvement in HB", "current": 10.1, "target": 11, "last_updated": "27-11-2025"},
        {"indicator": "Number of Beneficiaries Screened", "current": 39645, "target": 50000, "last_updated": "27-11-2025"},
        {"indicator": "Number of Village level health awareness sessions conducted", "current": 0, "target": 1500, "last_updated": "27-11-2025"},
        {"indicator": "ASHA Workers trained", "current": 200, "target": 1500, "last_updated": "27-11-2025"},
        {"indicator": "No of menstrual hygiene education sessions conducted", "current": 0, "target": 120, "last_updated": "27-11-2025"},
    ]
    
    for kpi in kpi_data:
        render_progress_bar(
            kpi["current"],
            kpi["target"],
            f"{kpi['indicator']} (Last Updated: {kpi['last_updated']})"
        )
    
    st.markdown("---")
    
    # Charts Section
    st.markdown("### 📊 Data Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Age Distribution Chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Age Distribution of Participants")
        
        # Sample data for age distribution
        age_data = {
            'Age': [11, 12, 13, 14, 15, 16, 17],
            'Count': [50, 80, 120, 200, 150, 100, 50]
        }
        age_df = pd.DataFrame(age_data)
        
        fig = create_donut_chart(
            age_df['Age'].astype(str),
            age_df['Count'],
            "Age Distribution",
            px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Income Distribution Chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Income Distribution of Participant Families")
        
        income_data = {
            'Income Class': ['Middle Class', 'Lower Middle Class', 'Below Poverty Line'],
            'Count': [116, 108, 526]
        }
        income_df = pd.DataFrame(income_data)
        
        fig = create_bar_chart(
            income_df,
            'Income Class',
            'Count',
            "Income Distribution",
            "#667eea"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional Charts Row
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        # Average Attendance Chart (Stacked Bar)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Average Attendance School-wise")
        
        attendance_data = {
            'School': ['Verma Nagar', 'Sultanpur', 'Sharma Colony', 'Shanti Colony', 'Ram Nagar'],
            'Male': [86.4, 86.6, 84.6, 85.4, 85.9],
            'Female': [86.0, 84.6, 84.8, 84.9, 85.5]
        }
        attendance_df = pd.DataFrame(attendance_data)
        attendance_melted = pd.melt(
            attendance_df,
            id_vars=['School'],
            value_vars=['Male', 'Female'],
            var_name='Gender',
            value_name='Attendance'
        )
        
        fig = create_stacked_bar_chart(
            attendance_melted,
            'School',
            'Attendance',
            'Gender',
            "Average Attendance by School",
            ["#ff6b6b", "#4ecdc4"]
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Waterfall Chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Afterschool Program Progress")
        
        schools = ['Krishna Puram', 'Nehru Nagar', 'Patel Vihar', 'Rajpur', 'Ram Nagar', 'Total']
        values = [8.21, 6.92, 6.04, 6.44, 6.08, 33.69]
        
        fig = create_waterfall_chart(schools, values, "Afterschool Program Contributions")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def program_data_page(data_loader, program_name):
    """Program-specific data page"""
    st.markdown(f"""
    <div class="dashboard-header">
        <h1>🏥 {program_name}</h1>
        <p>Program data and analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get program data
    df = data_loader.get_program_data(program_name)
    
    if df is not None and not df.empty:
        # Display KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            render_kpi_card("Total Records", len(df), "Data entries", "#667eea")
        
        with col2:
            # Calculate unique beneficiaries if column exists
            beneficiary_cols = [col for col in df.columns if 'beneficiary' in col.lower() or 'name' in col.lower()]
            unique_count = df[beneficiary_cols[0]].nunique() if beneficiary_cols else 0
            render_kpi_card("Unique Beneficiaries", unique_count, "Distinct individuals", "#10b981")
        
        with col3:
            # Calculate average age if column exists
            age_cols = [col for col in df.columns if 'age' in col.lower()]
            avg_age = df[age_cols[0]].mean() if age_cols and df[age_cols[0]].dtype in ['int64', 'float64'] else 0
            render_kpi_card("Average Age", f"{avg_age:.2f}", "Years", "#f59e0b")
        
        with col4:
            # Gender distribution
            gender_cols = [col for col in df.columns if 'gender' in col.lower()]
            if gender_cols:
                gender_counts = df[gender_cols[0]].value_counts()
                male_count = gender_counts.get('M', 0) + gender_counts.get('Male', 0)
                female_count = gender_counts.get('F', 0) + gender_counts.get('Female', 0)
                render_kpi_card("Gender Ratio", f"M:{male_count} F:{female_count}", "Male:Female", "#ef4444")
            else:
                render_kpi_card("Data Points", len(df), "Records", "#ef4444")
        
        st.markdown("---")
        
        # Data Table
        st.markdown("### 📋 Program Data")
        st.dataframe(df, use_container_width=True, height=400)
        
        # Charts
        st.markdown("---")
        st.markdown("### 📊 Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gender distribution chart
            if gender_cols:
                gender_counts = df[gender_cols[0]].value_counts()
                fig = create_donut_chart(
                    gender_counts.index.astype(str),
                    gender_counts.values,
                    "Gender Distribution",
                    ["#ff6b6b", "#4ecdc4"]
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Age distribution if available
            if age_cols:
                age_counts = df[age_cols[0]].value_counts().sort_index()
                fig = create_bar_chart(
                    pd.DataFrame({'Age': age_counts.index, 'Count': age_counts.values}),
                    'Age',
                    'Count',
                    "Age Distribution",
                    "#667eea"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning(f"No data available for {program_name}")

def kpis_page(data_loader):
    """KPIs page with detailed indicators"""
    st.markdown("""
    <div class="dashboard-header">
        <h1>📊 Key Performance Indicators</h1>
        <p>Track progress across all CSR programs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Indicators Table
    kpi_data = [
        {"indicator": "Improvement in HB", "current": 10.1, "target": 11, "last_updated": "27-11-2025", "status": "On track"},
        {"indicator": "Number of Beneficiaries Screened", "current": 39645, "target": 50000, "last_updated": "27-11-2025", "status": "On track"},
        {"indicator": "Number of Village level health awareness sessions conducted", "current": 0, "target": 1500, "last_updated": "27-11-2025", "status": "On track"},
        {"indicator": "ASHA Workers trained", "current": 200, "target": 1500, "last_updated": "27-11-2025", "status": "At risk"},
        {"indicator": "No of menstrual hygiene education sessions conducted", "current": 0, "target": 120, "last_updated": "27-11-2025", "status": "On track"},
    ]
    
    st.markdown("### 📈 Indicator Progress")
    
    for kpi in kpi_data:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1.5, 2, 1, 1])
            
            with col1:
                st.markdown(f"**{kpi['indicator']}**")
            
            with col2:
                st.markdown(f"**{kpi['current']}/{kpi['target']}**")
            
            with col3:
                render_progress_bar(kpi['current'], kpi['target'], "")
            
            with col4:
                st.markdown(kpi['last_updated'])
            
            with col5:
                status_class = "status-on-track" if kpi['status'] == "On track" else "status-at-risk"
                st.markdown(f'<span class="{status_class}">{kpi["status"]}</span>', unsafe_allow_html=True)
            
            st.markdown("---")

def framework_page(data_loader):
    """Framework page"""
    st.markdown("""
    <div class="dashboard-header">
        <h1>📋 CSR Framework</h1>
        <p>Governance structure and framework documentation</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Framework documentation and governance structure will be displayed here.")
    
    # Display master data
    st.markdown("### Master Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        state_master = data_loader.get_data("CSR_MIS_State Master")
        if state_master is not None and not state_master.empty:
            st.markdown("#### State Master")
            st.dataframe(state_master, use_container_width=True, height=300)
    
    with col2:
        location_master = data_loader.get_data("CSR_MIS_Location Master")
        if location_master is not None and not location_master.empty:
            st.markdown("#### Location Master")
            st.dataframe(location_master, use_container_width=True, height=300)
    
    with col3:
        sdg_master = data_loader.get_data("CSR_MIS_SDG Master")
        if sdg_master is not None and not sdg_master.empty:
            st.markdown("#### SDG Master")
            st.dataframe(sdg_master, use_container_width=True, height=300)

def documents_page():
    """Documents page"""
    st.markdown("""
    <div class="dashboard-header">
        <h1>📄 Documents</h1>
        <p>CSR documentation and reports</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Document management system - Upload, view, and manage CSR documents here.")
    
    # Document categories
    doc_categories = [
        "Policy Documents",
        "Annual Reports",
        "Program Reports",
        "Compliance Documents",
        "Impact Assessments"
    ]
    
    selected_category = st.selectbox("Select Document Category", doc_categories)
    st.markdown(f"### {selected_category}")
    st.info(f"Documents in {selected_category} category will be listed here.")

def budgets_page(data_loader):
    """Budgets page"""
    st.markdown("""
    <div class="dashboard-header">
        <h1>💰 Budgets</h1>
        <p>Budget allocation and expenditure tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Budget overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_kpi_card("Total Budget", "₹50,00,00,000", "Allocated", "#667eea")
    
    with col2:
        render_kpi_card("Utilized", "₹35,00,00,000", "70% utilized", "#10b981")
    
    with col3:
        render_kpi_card("Remaining", "₹15,00,00,000", "30% remaining", "#f59e0b")
    
    with col4:
        render_kpi_card("Programs", "12", "Active programs", "#ef4444")
    
    st.markdown("---")
    
    # Budget breakdown by program
    st.markdown("### Budget Breakdown by Program")
    
    budget_data = {
        'Program': ['Jindal Arogyam', 'Kishori Express', 'Vatsalya', 'Education', 'Health Awareness'],
        'Allocated': [10000000, 8000000, 6000000, 12000000, 5000000],
        'Utilized': [7500000, 6000000, 4500000, 9000000, 3500000],
        'Remaining': [2500000, 2000000, 1500000, 3000000, 1500000]
    }
    
    budget_df = pd.DataFrame(budget_data)
    budget_df['Utilization %'] = (budget_df['Utilized'] / budget_df['Allocated'] * 100).round(2)
    
    st.dataframe(budget_df, use_container_width=True)
    
    # Budget chart
    fig = create_bar_chart(
        budget_df,
        'Program',
        'Allocated',
        "Budget Allocation by Program",
        "#667eea"
    )
    st.plotly_chart(fig, use_container_width=True)

def reports_page(data_loader):
    """Reports page"""
    st.markdown("""
    <div class="dashboard-header">
        <h1>📊 Reports</h1>
        <p>Generate and view CSR reports</p>
    </div>
    """, unsafe_allow_html=True)
    
    report_types = [
        "Monthly Report",
        "Quarterly Report",
        "Annual Report",
        "Program-Specific Report",
        "Impact Assessment Report"
    ]
    
    selected_report = st.selectbox("Select Report Type", report_types)
    
    st.markdown(f"### {selected_report}")
    
    # Report generation options
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
    
    with col2:
        programs = st.multiselect("Select Programs", [
            "Jindal Arogyam Hospital",
            "Kishori Express",
            "Vatsalya",
            "Subhangi",
            "Swasti Express"
        ])
    
    if st.button("📥 Generate Report"):
        st.success(f"{selected_report} generated successfully!")
        st.info("Report download functionality will be implemented here.")

def data_entry_page(data_loader):
    """Data entry form page"""
    st.markdown("""
    <div class="dashboard-header">
        <h1>📝 Data Entry</h1>
        <p>Enter new CSR program data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Program selection
    programs = [
        "Jindal Arogyam Hospital",
        "Kishori Express",
        "Vatsalya",
        "Subhangi",
        "Swasti Express",
        "Chiranjeevi",
        "HIV/AIDS",
        "TB Mukt Bharat",
        "Poor Patient Treatment",
        "Tele-Medicine",
        "Mobile Medical Van/ Emergency Care"
    ]
    
    selected_program = st.selectbox("Select Program", programs)
    
    st.markdown("---")
    
    # Form in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        program_code = st.text_input("Program Code*", value=selected_program)
        location = st.text_input("Location*")
        objective = st.text_area("Objective*", placeholder="Enter objective")
        program_type = st.selectbox("Please mention if it is*", ["Direct", "Collaboration", "Partnership"])
        agency_name = st.text_input("Agency Name", placeholder="Agency Name:")
        services = st.text_input("Services", placeholder="Services")
        name = st.text_input("Name", placeholder="Name")
        gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
    
    with col2:
        business_location = st.selectbox("Business Location/Non-Business Location*", ["Business", "Non-Business"])
        activities = st.text_area("Activities*", placeholder="Activities")
        
        # Get SDG options from master data
        sdg_master = data_loader.get_data("CSR_MIS_SDG Master")
        sdg_options = [""]
        if sdg_master is not None and not sdg_master.empty:
            sdg_col = sdg_master.columns[0] if len(sdg_master.columns) > 0 else None
            if sdg_col:
                sdg_options.extend(sdg_master[sdg_col].dropna().unique().tolist())
        
        sdg_alignment = st.selectbox("SDG Alignment*", sdg_options)
        collaboration_type = st.selectbox("Please mention if it is*", ["", "Direct", "Collaboration", "Partnership"])
        date = st.date_input("Date*")
        beneficiary_code = st.selectbox("Beneficiary Code", [""])
        age = st.number_input("Age", min_value=0, max_value=120, value=0)
        
        # Get State options from master data
        state_master = data_loader.get_data("CSR_MIS_State Master")
        state_options = [""]
        if state_master is not None and not state_master.empty:
            state_col = state_master.columns[0] if len(state_master.columns) > 0 else None
            if state_col:
                state_options.extend(state_master[state_col].dropna().unique().tolist())
        
        state = st.selectbox("State*", state_options)
    
    st.markdown("---")
    
    # Submit button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💾 Submit Data", use_container_width=True):
            st.success("Data submitted successfully! (This is a demo - data would be saved to database in production)")

def main():
    """Main application"""
    # Sidebar Navigation - Always show this first (before any checks)
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0; background-color: #1e1e1e;">
        <h2 style="color: #667eea; margin: 0; font-weight: 700;">JSPL Foundation</h2>
        <p style="color: #b0b0b0; margin: 0.5rem 0; font-size: 0.9rem;">CSR Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if data_loader exists
    if 'data_loader' not in st.session_state:
        st.error("❌ Data loader not initialized. Please refresh the page.")
        st.info("If the problem persists, check that both Excel files are in the correct location.")
        # Still show sidebar even if data loader fails
        st.sidebar.markdown('<h3 style="color: #b0b0b0;">⚠️ Data Not Loaded</h3>', unsafe_allow_html=True)
        st.sidebar.info("Please refresh the page to reload data.")
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Navigation")
        st.sidebar.info("Data must be loaded to access pages.")
        return
    
    # Show data status in sidebar
    try:
        data_loader = st.session_state.data_loader
        total_sheets = len(data_loader.get_all_keys())
        st.sidebar.markdown(f'<p style="color: #b0b0b0; font-size: 0.85rem;">📊 <strong>Loaded:</strong> {total_sheets} sheets</p>', unsafe_allow_html=True)
    except Exception as e:
        st.sidebar.error(f"Error: {str(e)}")
        data_loader = None
    
    st.sidebar.markdown("---")
    
    # Navigation menu
    try:
        page = st.sidebar.radio(
            "Navigation",
            ["Overview", "KPIs", "Framework", "Documents", "Budgets", "Health & Nutrition", "Education", "Data Entry", "Reports"],
            label_visibility="visible"
        )
    except Exception as e:
        st.sidebar.error(f"Navigation Error: {str(e)}")
        # Fallback navigation
        page = st.sidebar.selectbox(
            "Navigation",
            ["Overview", "KPIs", "Framework", "Documents", "Budgets", "Health & Nutrition", "Education", "Data Entry", "Reports"]
        )
    
    # Ensure data_loader is available for page routing
    if data_loader is None:
        st.error("Cannot load pages - data loader unavailable")
        return
    
    # Route to appropriate page
    try:
        if page == "Overview":
            overview_page(data_loader)
        
        elif page == "Health & Nutrition":
            st.sidebar.markdown('<h3 style="color: #b0b0b0; margin-top: 1rem;">Programs</h3>', unsafe_allow_html=True)
            health_programs = [
                "Jindal Arogyam Hospital",
                "Kishori Express",
                "Vatsalya",
                "Subhangi",
                "Swasti Express",
                "Chiranjeevi",
                "HIV/AIDS",
                "TB Mukt Bharat",
                "Poor Patient Treatment",
                "Tele-Medicine",
                "Mobile Medical Van"
            ]
            
            selected_program = st.sidebar.selectbox("Select Program", health_programs)
            
            # Map display names to data keys
            program_mapping = {
                "Jindal Arogyam Hospital": "JindalArogym",
                "Kishori Express": "Kishori Express",
                "Vatsalya": "Vatsalya",
                "Subhangi": "Subhangi",
                "Swasti Express": "Swasti Express",
                "Chiranjeevi": "chiranjeevi",
                "HIV/AIDS": "HIV  Aids",
                "TB Mukt Bharat": "TB Mukt Bharat",
                "Poor Patient Treatment": "Poor Patients Treatment",
                "Tele-Medicine": "TeleMedicine",
                "Mobile Medical Van": "Mobile Medical Van"
            }
            
            program_key = program_mapping.get(selected_program, selected_program)
            program_data_page(data_loader, program_key)
        
        elif page == "Education":
            st.info("Education programs page - Coming soon!")
            # Add education-specific programs here
        
        elif page == "Data Entry":
            data_entry_page(data_loader)
        
        elif page == "KPIs":
            kpis_page(data_loader)
        
        elif page == "Framework":
            framework_page(data_loader)
        
        elif page == "Documents":
            documents_page()
        
        elif page == "Budgets":
            budgets_page(data_loader)
        
        elif page == "Reports":
            reports_page(data_loader)
    
    except Exception as e:
        st.error(f"Error loading page '{page}': {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"❌ Application Error: {str(e)}")
        st.exception(e)
        st.info("Please check the console for more details or refresh the page.")
