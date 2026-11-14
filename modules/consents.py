import streamlit as st
from modules.helpers import query_df, patient_options, add_consent

def show_consents(actor):
    st.title("Consentimientos y autorizaciones")
    st.warning("Prototipo académico: estos registros no constituyen firma digital ni consentimiento legal válido.")
    opts=patient_options()
    if not opts:
        st.info("Primero registrá un paciente."); return
    with st.form("consent_form",clear_on_submit=True):
        patient=st.selectbox("Paciente",list(opts.keys()))
        kind=st.selectbox("Tipo",["Autorización para compartir estudios","Consentimiento informado","Autorización de acceso a historia clínica","Otro"])
        granted=st.text_input("Profesional / institución destinataria")
        date=st.date_input("Fecha")
        status=st.selectbox("Estado",["Pendiente","Aceptado (demostración)","Rechazado","Revocado"])
        notes=st.text_area("Observaciones")
        ok=st.form_submit_button("Registrar constancia",type="primary")
        if ok:
            add_consent(opts[patient],kind,granted,str(date),status,notes,actor)
            st.success("Constancia registrada."); st.rerun()
    st.subheader("Registros")
    df=query_df("""SELECT c.id AS ID,p.full_name AS Paciente,c.consent_type AS Tipo,c.granted_to AS Destinatario,
    c.consent_date AS Fecha,c.status AS Estado,c.notes AS Observaciones FROM consents c
    LEFT JOIN patients p ON p.id=c.patient_id ORDER BY c.consent_date DESC""")
    st.dataframe(df,use_container_width=True,hide_index=True)
