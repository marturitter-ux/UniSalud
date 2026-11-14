import streamlit as st
from modules.helpers import query_df, patient_options

def show_history():
    st.title("Historia clínica unificada")
    opts = patient_options()
    if not opts:
        st.info("Primero registrá un paciente en la sección Pacientes.")
        return
    selected = st.selectbox("Seleccionar paciente", list(opts.keys()))
    pid = opts[selected]
    p = query_df("SELECT * FROM patients WHERE id=?",(pid,))
    if not p.empty:
        r = p.iloc[0]
        c1,c2,c3 = st.columns(3)
        c1.metric("Documento", r["document"])
        c2.metric("Grupo sanguíneo", r["blood_group"] or "No informado")
        c3.metric("Fecha de nacimiento", r["birth_date"] or "No informada")
        st.subheader(r["full_name"])
        tabs = st.tabs(["Datos y antecedentes","Estudios e informes","Turnos","Consentimientos"])
        with tabs[0]:
            st.write("**Teléfono:**",r["phone"] or "No informado")
            st.write("**Correo:**",r["email"] or "No informado")
            st.write("**Domicilio:**",r["address"] or "No informado")
            st.write("**Observaciones:**",r["notes"] or "Sin observaciones")
        with tabs[1]:
            df = query_df("SELECT study_date AS Fecha, modality AS Modalidad, body_region AS Región, institution AS Institución, professional AS Profesional, status AS Estado, report AS Informe FROM studies WHERE patient_id=? ORDER BY study_date DESC",(pid,))
            st.dataframe(df,use_container_width=True,hide_index=True)
        with tabs[2]:
            df = query_df("SELECT appointment_date AS Fecha, appointment_time AS Hora, professional AS Profesional, institution AS Institución, reason AS Motivo, status AS Estado FROM appointments WHERE patient_id=? ORDER BY appointment_date DESC",(pid,))
            st.dataframe(df,use_container_width=True,hide_index=True)
        with tabs[3]:
            df = query_df("SELECT consent_type AS Tipo, granted_to AS Destinatario, consent_date AS Fecha, status AS Estado, notes AS Observaciones FROM consents WHERE patient_id=? ORDER BY consent_date DESC",(pid,))
            st.dataframe(df,use_container_width=True,hide_index=True)
