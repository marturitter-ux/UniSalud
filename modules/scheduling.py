import streamlit as st
from modules.helpers import query_df, patient_options, add_appointment

def show_appointments(actor):
    st.title("Turnos y agenda")
    tab1,tab2=st.tabs(["Nuevo turno","Agenda"])
    opts=patient_options()
    with tab1:
        if not opts:
            st.info("Primero registrá un paciente.")
        else:
            with st.form("appointment_form",clear_on_submit=True):
                patient=st.selectbox("Paciente",list(opts.keys()))
                c1,c2=st.columns(2)
                professional=c1.text_input("Profesional")
                institution=c2.text_input("Institución")
                c3,c4=st.columns(2)
                date=c3.date_input("Fecha")
                time=c4.time_input("Hora")
                reason=st.text_input("Motivo / especialidad")
                status=st.selectbox("Estado",["Solicitado","Confirmado","Realizado","Cancelado"])
                ok=st.form_submit_button("Guardar turno",type="primary")
                if ok:
                    add_appointment(opts[patient],professional,institution,str(date),str(time),reason,status,actor)
                    st.success("Turno registrado.")
                    st.rerun()
    with tab2:
        df=query_df("""SELECT a.id AS ID,p.full_name AS Paciente,a.appointment_date AS Fecha,
        a.appointment_time AS Hora,a.professional AS Profesional,a.institution AS Institución,
        a.reason AS Motivo,a.status AS Estado FROM appointments a
        LEFT JOIN patients p ON p.id=a.patient_id ORDER BY a.appointment_date,a.appointment_time""")
        st.dataframe(df,use_container_width=True,hide_index=True)
