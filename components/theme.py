import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
    :root { --navy:#123D59; --blue:#267FA3; --sky:#83C9D5; --teal:#5ABDAA; --ink:#18394D; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
    .stApp { background:linear-gradient(135deg,#F7FAFC 0%,#EEF5F8 100%); color:var(--ink); }
    [data-testid="stSidebar"] { background:#123D59; }
    [data-testid="stSidebar"] * { color:#F5FBFD !important; }
    [data-testid="stHeader"] { background:rgba(247,250,252,.86); }
    h1,h2,h3 { font-family:'Manrope',sans-serif !important; color:#123D59; }
    .brand { font-family:'Manrope',sans-serif; font-size:2rem; font-weight:800; letter-spacing:-1.4px; color:#123D59; }
    .brand span { color:#36A99D; }
    .tagline { color:#668294; margin-top:-10px; font-size:.92rem; }
    .hero { background:linear-gradient(120deg,#123D59,#267FA3 65%,#38A99D); color:white;
            padding:1.5rem 1.7rem; border-radius:20px; margin:.4rem 0 1.2rem 0;
            box-shadow:0 12px 30px rgba(18,61,89,.13); }
    .hero h2 { color:white !important; margin:0; }
    .hero p { color:#E1F2F5; margin:.35rem 0 0 0; }
    div[data-testid="stMetric"] { background:white; padding:1rem; border:1px solid #E5EEF2;
        border-radius:16px; box-shadow:0 5px 16px rgba(25,70,95,.04); }
    .section-note { color:#6D8796; font-size:.9rem; }
    div.stButton > button, div.stDownloadButton > button { border-radius:11px; font-weight:600; }
    div.stButton > button[kind="primary"] { background:#267FA3; border-color:#267FA3; }
    [data-testid="stDataFrame"] { border:1px solid #E5EEF2; border-radius:12px; overflow:hidden; }
    .small-muted { color:#718A98; font-size:.82rem; }
    </style>
    """, unsafe_allow_html=True)

def brand_header():
    st.markdown('<div class="brand">Uni<span>Salud</span></div><div class="tagline">Tu historia clínica en un solo lugar.</div>', unsafe_allow_html=True)
