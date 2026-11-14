from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
import streamlit as st
from database.database import init_db, log_activity
from components.theme import apply_theme, brand_header
from modules.dashboard import show_dashboard
from modules.patients import show_patients
from modules.records import show_history
from modules.imaging import show_imaging
from modules.scheduling import show_appointments
from modules.directory import show_professionals, show_institutions
from modules.consents import show_consents
from modules.reports import show_reports
from modules.accessibility import show_accessibility
from modules.helpers import query_df

st.set_page_config(page_title="UniSalud | Tu historia clínica en un solo lugar",page_icon="💙",layout="wide",initial_sidebar_state="expanded")
logo_path = BASE_DIR / "assets"

imagenes = list(logo_path.glob("*"))

if imagenes:
    st.image(str(imagenes[0]), width=180)
init_db()
apply_theme()

if "actor" not in st.session_state: st.session_state.actor="Usuario de demostración"
if "role" not in st.session_state: st.session_state.role="Institución"

with st.sidebar:
    st.markdown("## 💙 UniSalud")
    st.caption("Tu historia clínica en un solo lugar.")
    st.divider()
    role=st.selectbox("Ingresar como",["Paciente","Profesional","Institución"],index=["Paciente","Profesional","Institución"].index(st.session_state.role))
    st.session_state.role=role
    actor=st.text_input("Nombre de usuario (demostración)",value=st.session_state.actor)
    st.session_state.actor=actor or "Usuario de demostración"
    st.divider()
    menu = {
        "Inicio":"Inicio",
        "Pacientes":"Pacientes",
        "Historia clínica":"Historia clínica",
        "Diagnóstico por imágenes":"Diagnóstico por imágenes",
        "Turnos y agenda":"Turnos y agenda",
        "Profesionales":"Profesionales",
        "Instituciones":"Instituciones",
        "Consentimientos":"Consentimientos",
        "Estadísticas y reportes":"Estadísticas y reportes",
        "Accesibilidad y configuración":"Accesibilidad y configuración"
    }
    allowed = {
        "Paciente":["Inicio","Historia clínica","Diagnóstico por imágenes","Turnos y agenda","Consentimientos","Accesibilidad y configuración"],
        "Profesional":["Inicio","Pacientes","Historia clínica","Diagnóstico por imágenes","Turnos y agenda","Consentimientos","Estadísticas y reportes","Accesibilidad y configuración"],
        "Institución":list(menu.keys())
    }
    pages=allowed[role]
    page=st.radio("NAVEGACIÓN",pages,label_visibility="collapsed")
    st.divider()
    st.caption("PROTOTIPO ACADÉMICO · DATOS FICTICIOS")
    st.caption("La selección de perfil es demostrativa, no equivale a autenticación.")

top1,top2=st.columns([4,1])
with top1:
    brand_header()
with top2:
    st.markdown("<div style='height:10px'></div>",unsafe_allow_html=True)
    st.markdown("🔔  **Centro de avisos**")
    st.caption(f"Perfil: {role}")

st.divider()

if page=="Inicio":
    show_dashboard(role,st.session_state.actor)
elif page=="Pacientes":
    show_patients(st.session_state.actor)
elif page=="Historia clínica":
    show_history()
elif page=="Diagnóstico por imágenes":
    show_imaging(st.session_state.actor)
elif page=="Turnos y agenda":
    show_appointments(st.session_state.actor)
elif page=="Profesionales":
    show_professionals(st.session_state.actor)
elif page=="Instituciones":
    show_institutions(st.session_state.actor)
elif page=="Consentimientos":
    show_consents(st.session_state.actor)
elif page=="Estadísticas y reportes":
    show_reports()
elif page=="Accesibilidad y configuración":
    show_accessibility()

st.divider()
st.markdown("<div class='small-muted'>UniSalud · Prototipo académico · No utilizar con información clínica real.</div>",unsafe_allow_html=True)
