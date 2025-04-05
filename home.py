import streamlit as st

st.set_page_config(page_title="IDP", layout="centered")

# Header bar
st.markdown("""
<div style="background-color: #1F2B3E; padding: 1rem; border-radius: 0.75rem 0.75rem 0 0;
    display: flex; justify-content: space-between; align-items: center;">
    <div style="color: white; font-size: 1.4rem; font-weight: bold;">IDP</div>
    <div style="font-size: 1.5rem; color: white;">👤</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='margin-top: 1rem;'>Home</h2>", unsafe_allow_html=True)

card_style = """
    background-color: #F7F9FC;
    padding: 1.2rem;
    border-radius: 0.75rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    height: 120px;
    transition: 0.3s;
"""

st.markdown("""
    <style>
    a.card:hover {
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
        transform: scale(1.01);
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <a href="/frontend" class="card" style="text-decoration: none; color: inherit;">
        <div style="{card_style}">
            <b>📤 Upload Document</b><br>
            <span style="font-size: 0.9rem;">Upload a new document</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="{card_style}">
        <b>🕒 View History</b><br>
        <span style="font-size: 0.9rem;">View previously processed documents</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown(f"""
    <div style="{card_style}">
        <b>📊 Reports</b><br>
        <span style="font-size: 0.9rem;">View processing reports</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="{card_style}">
        <b>⚙️ Settings</b><br>
        <span style="font-size: 0.9rem;">Manage application settings</span>
    </div>
    """, unsafe_allow_html=True)
