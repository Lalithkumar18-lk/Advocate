import streamlit as st
import pandas as pd
import datetime
import random
import time

# Page configuration
st.set_page_config(
    page_title="Human AI Advocate",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with high contrast and visible text
st.markdown("""
<style>
    /* High contrast theme for maximum visibility */
    :root {
        --primary-blue: #1a73e8;
        --dark-blue: #0d47a1;
        --text-dark: #212121;
        --text-light: #ffffff;
        --bg-light: #f8f9fa;
        --success-green: #0d9d58;
        --warning-orange: #f57c00;
        --danger-red: #ea4335;
    }
    
    /* Main containers with good contrast */
    .main-container {
        background: white;
        padding: 25px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 5px solid var(--primary-blue);
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .highlight-box {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        color: white !important;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
    }
    
    .success-box {
        background: #e8f5e9;
        border-left: 5px solid var(--success-green);
        padding: 20px;
        border-radius: 8px;
        margin: 15px 0;
        color: #212121;
    }
    
    .update-box {
        background: #fff3e0;
        border-left: 5px solid var(--warning-orange);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: #212121;
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        border-top: 4px solid var(--primary-blue);
        text-align: center;
    }
    
    /* Typography enhancements */
    h1, h2, h3, h4 {
        color: var(--text-dark) !important;
        font-weight: 600 !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h2 {
        font-size: 2rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
        color: var(--dark-blue) !important;
    }
    
    p, li {
        font-size: 1.1rem !important;
        line-height: 1.6 !important;
        color: #424242 !important;
    }
    
    strong {
        color: var(--text-dark) !important;
        font-weight: 700 !important;
    }
    
    /* List styling */
    ul {
        padding-left: 20px !important;
    }
    
    li {
        margin: 10px 0 !important;
        padding-left: 5px !important;
    }
    
    /* Divider */
    .divider {
        height: 2px;
        background: linear-gradient(to right, #1a73e8, transparent);
        margin: 30px 0;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        margin: 0 5px;
    }
    
    .badge-primary {
        background: var(--primary-blue);
        color: white;
    }
    
    .badge-success {
        background: var(--success-green);
        color: white;
    }
    
    .badge-warning {
        background: var(--warning-orange);
        color: white;
    }
    
    /* Table styling */
    .data-table {
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Ensure all text is visible */
    .stSelectbox, .stTextInput, .stTextArea {
        color: #212121 !important;
    }
    
    .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #212121 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'advocacy_cases' not in st.session_state:
    st.session_state.advocacy_cases = []

# Header Section
st.markdown("""
<div class="highlight-box">
    <h1 style="color: white !important; text-align: center;">🤝 Human AI Advocate</h1>
    <p style="color: white !important; text-align: center; font-size: 1.3rem !important;">
        Protecting human dignity in the age of Artificial Intelligence
    </p>
</div>
""", unsafe_allow_html=True)

# Main Content Columns
col1, col2 = st.columns([2, 1])

with col1:
    # Global Dashboard Section
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 🌍 Global Human Rights & AI Dashboard")
    
    # Real-time Metrics
    st.markdown("### 📊 Current Statistics")
    
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 47")
        st.markdown("**Active Cases**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metrics_col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 2.1M")
        st.markdown("**People Protected**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metrics_col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 23")
        st.markdown("**Policies Influenced**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metrics_col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 89%")
        st.markdown("**Success Rate**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-container
    
    # Current Hotspots Section
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 🔥 Current Human Rights Hotspots")
    
    hotspots_data = pd.DataFrame({
        'Region': ['Brazil', 'Africa', 'European Union', 'United States', 'Asia-Pacific'],
        'Active Cases': [12, 9, 8, 7, 15],
        'Primary Concern': ['Work Rights', 'Healthcare Access', 'Privacy', 'Non-discrimination', 'Freedom of Expression'],
        'Severity': ['High', 'High', 'Medium', 'Medium', 'High']
    })
    
    st.dataframe(
        hotspots_data,
        column_config={
            "Region": st.column_config.TextColumn("🌍 Region", width="medium"),
            "Active Cases": st.column_config.NumberColumn("📋 Active Cases", width="small"),
            "Primary Concern": st.column_config.TextColumn("⚖️ Primary Concern", width="medium"),
            "Severity": st.column_config.TextColumn("⚠️ Severity", width="small")
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Quick Stats Sidebar
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 📈 Quick Overview")
    
    st.markdown("### Most Affected Rights")
    
    rights_data = {
        "Right to Work": "7 active cases",
        "Right to Health": "9 active cases", 
        "Right to Privacy": "12 active cases",
        "Right to Non-discrimination": "8 active cases",
        "Right to Freedom": "5 active cases"
    }
    
    for right, cases in rights_data.items():
        st.markdown(f"""
        <div style="margin: 10px 0; padding: 10px; background: #f5f5f5; border-radius: 5px;">
            <strong>{right}</strong><br>
            <span style="color: #1a73e8;">{cases}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Top AI Systems Involved")
    
    ai_systems = [
        "Automated Hiring Systems",
        "Healthcare Diagnostic AI", 
        "Facial Recognition",
        "Social Media Algorithms",
        "Predictive Policing"
    ]
    
    for system in ai_systems:
        st.markdown(f"• {system}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Success Stories Section
st.markdown("## 🌟 Recent Success Stories")

col_success1, col_success2 = st.columns(2)

with col_success1:
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("### ✅ Banned Discriminatory Hiring AI")
    st.markdown("**Description:** Successfully advocated for removal of biased AI that discriminated against women in tech hiring.")
    st.markdown("""
    **Impact Metrics:**
    - **People Protected:** 5,020+ job seekers
    - **Year:** 2023
    - **Location:** Global tech companies
    - **Duration:** 8-month campaign
    """)
    st.markdown("**Key Achievement:** Established precedent for algorithmic fairness in employment")
    st.markdown('</div>', unsafe_allow_html=True)

with col_success2:
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("### ✅ Transparency in Facial Recognition")
    st.markdown("**Description:** Forced government to disclose facial recognition usage in public spaces.")
    st.markdown("""
    **Impact Metrics:**
    - **People Protected:** 2 million citizens
    - **Year:** 2022  
    - **Location:** Major metropolitan areas
    - **Duration:** 14-month legal battle
    """)
    st.markdown("**Key Achievement:** Set legal standard for AI surveillance transparency")
    st.markdown('</div>', unsafe_allow_html=True)

# Additional Success Story
st.markdown('<div class="success-box">', unsafe_allow_html=True)
st.markdown("### ✅ Healthcare AI Accountability Framework")
st.markdown("**Description:** Established oversight committee for medical diagnostic AI systems.")
st.markdown("""
**Impact Metrics:**
- **People Protected:** Healthcare patients nationwide
- **Year:** 2023
- **Safeguards Implemented:** 15 new protocols
- **Compliance Rate:** 92% adoption
""")
st.markdown("**Key Achievement:** Created gold standard for medical AI ethics")
st.markdown('</div>', unsafe_allow_html=True)

# Divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Live Updates Section
st.markdown("## 🔄 Live Human Rights Updates")

updates = [
    {
        "time": "Just now",
        "update": "New legislation proposed for AI transparency in healthcare",
        "impact": "Affects 500+ hospitals nationwide"
    },
    {
        "time": "15 minutes ago", 
        "update": "Community forum organized on algorithmic bias in education",
        "impact": "200+ participants registered"
    },
    {
        "time": "1 hour ago",
        "update": "UN committee begins review of AI human rights guidelines",
        "impact": "Global policy implications"
    },
    {
        "time": "3 hours ago",
        "update": "Major tech company agrees to independent human rights audit",
        "impact": "Sets precedent for industry accountability"
    },
    {
        "time": "5 hours ago",
        "update": "Class action lawsuit filed against biased credit scoring AI",
        "impact": "50,000+ potentially affected consumers"
    }
]

for update in updates:
    st.markdown(f'''
    <div class="update-box">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <strong style="color: #f57c00;">{update["time"]}</strong><br>
                <strong>{update["update"]}</strong>
            </div>
            <span class="badge badge-warning">LIVE</span>
        </div>
        <p style="margin-top: 10px; color: #666;">Impact: {update["impact"]}</p>
    </div>
    ''', unsafe_allow_html=True)

# Action Section
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown("## 🚨 Take Action Now")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    st.markdown('<div class="main-container" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown("### 📝 Report an Issue")
    st.markdown("Have you experienced AI-related human rights violations?")
    if st.button("Report Now", key="report_btn", use_container_width=True):
        st.success("Redirecting to reporting form...")
    st.markdown('</div>', unsafe_allow_html=True)

with action_col2:
    st.markdown('<div class="main-container" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown("### 🤝 Join Advocacy")
    st.markdown("Become part of our global advocacy network")
    if st.button("Join Network", key="join_btn", use_container_width=True):
        st.success("Welcome to the network!")
    st.markdown('</div>', unsafe_allow_html=True)

with action_col3:
    st.markdown('<div class="main-container" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown("### 📚 Resources")
    st.markdown("Access advocacy tools and guides")
    if st.button("View Resources", key="resources_btn", use_container_width=True):
        st.success("Opening resource library...")
    st.markdown('</div>', unsafe_allow_html=True)

# Human Rights Framework Section
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown("## ⚖️ Protected Human Rights Framework")

rights_cols = st.columns(5)

human_rights = [
    {"name": "Right to Work", "icon": "💼", "cases": 7},
    {"name": "Right to Health", "icon": "🏥", "cases": 9},
    {"name": "Right to Privacy", "icon": "🔒", "cases": 12},
    {"name": "Right to Non-discrimination", "icon": "⚖️", "cases": 8},
    {"name": "Right to Freedom", "icon": "🗽", "cases": 5}
]

for idx, right in enumerate(human_rights):
    with rights_cols[idx]:
        st.markdown(f'''
        <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px; margin: 5px;">
            <div style="font-size: 2rem; margin-bottom: 10px;">{right['icon']}</div>
            <strong>{right['name']}</strong><br>
            <span style="color: #1a73e8; font-weight: bold;">{right['cases']} cases</span>
        </div>
        ''', unsafe_allow_html=True)

# Footer
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 30px; background: #f8f9fa; border-radius: 10px; margin-top: 20px;">
    <h3 style="color: #1a73e8 !important;">🤝 Human AI Advocate Platform</h3>
    <p><strong>Protecting human dignity in the age of artificial intelligence</strong></p>
    
    <div style="margin: 20px 0;">
        <p>📧 <strong>Contact:</strong> human-rights@ai-advocate.org</p>
        <p>📞 <strong>Emergency Hotline:</strong> 1-888-AI-HUMAN</p>
        <p>🌐 <strong>Website:</strong> www.human-ai-advocate.org</p>
    </div>
    
    <div style="border-top: 1px solid #ddd; padding-top: 20px; margin-top: 20px;">
        <p style="color: #666; font-size: 0.9rem;">
            Built with ❤️ for a human-centered AI future • Last updated: {}
        </p>
    </div>
</div>
""".format(datetime.datetime.now().strftime("%B %d, %Y")), unsafe_allow_html=True)

# Real-time refresh option
if st.checkbox("🔄 Enable automatic updates (refresh every 30 seconds)"):
    time.sleep(30)
    st.rerun()
