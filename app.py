# -*- coding: utf-8 -*-
"""
Bandung Multi-Modal Isochrone & Traffic Simulator
Main entry point for multi-page Streamlit application
"""

import streamlit as st
import os

# Configure page
st.set_page_config(
    page_title="Bandung Transit System",
    layout="wide",
    page_icon="🧭",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Bandung Multi-Modal Isochrone & Traffic Simulator v2.0"
    }
)

# Load custom CSS
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("style.css")

# Add custom styles for multi-page layout
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Pages configuration
pages = {
    "👥 User Dashboard": "pages/01_user_dashboard.py",
    "⚙️ Admin Panel": "pages/02_admin_dashboard.py",
    "📊 Analytics": "pages/03_analytics_dashboard.py",
    "ℹ️ About": "pages/04_about.py"
}

# Sidebar navigation
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Lambang_Kota_Bandung.svg/1200px-Lambang_Kota_Bandung.svg.png" 
         width="80" style="border-radius: 10px;">
    <h2 style="margin-top: 1rem;">🧭 Bandung Transit</h2>
    <p style="color: #64748b; font-size: 0.9rem;">Multi-Modal Isochrone Simulator</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Page selection
selected_page = st.sidebar.radio(
    "Navigation",
    list(pages.keys()),
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# Footer
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0; color: #64748b; font-size: 0.85rem;">
    <p><b>Version 2.0</b> - Admin Dashboard Edition</p>
    <p>Built with Streamlit • OSMnx • NetworkX</p>
</div>
""", unsafe_allow_html=True)

# Route to selected page
if selected_page == "👥 User Dashboard":
    exec(open("pages/01_user_dashboard.py").read())
elif selected_page == "⚙️ Admin Panel":
    exec(open("pages/02_admin_dashboard.py").read())
elif selected_page == "📊 Analytics":
    exec(open("pages/03_analytics_dashboard.py").read())
else:  # About
    exec(open("pages/04_about.py").read())
