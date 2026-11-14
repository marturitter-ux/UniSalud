import streamlit as st
import plotly.express as px
from modules.helpers import query_df

def show_dashboard(role, actor):
    st.markdown(f'<div class="hero"><h2>¡Bienvenido/a a UniSalud!</h2><p>Panel de {role.lower()} · Información organizada para una atención conectada.</p></div>', unsafe_allow_html=True)
    patients = query_df("SELECT COUNT(*) n FROM patients").iloc[0,0]
    studies = query_df("SELECT COUNT(*) n FROM studies").iloc[0,0]
    appointments = query_df("SELECT COUNT(*) n FROM appointments").iloc[0,0]
    professionals = query_df("SELECT COUNT(*) n FROM professionals").iloc[0,0]
    if role == "Paciente":
        c1,c2,c3 = st.columns(3)
        c1.metric("Mis estudios registrados", studies)
        c2.metric("Mis turnos registrados", appointments)
        c3.metric("Documentos disponibles", query_df("SELECT COUNT(*) n FROM consents").iloc[0,0])
    elif role == "Profesional":
        c1,c2,c3 = st.columns(3)
        c1.metric("Pacientes en el prototipo", patients)
        c2.metric("Estudios registrados", studies)
        c3.metric("Turnos registrados", appointments)
    else:
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Pacientes", patients)
        c2.metric("Estudios", studies)
        c3.metric("Turnos", appointments)
        c4.metric("Profesionales", professionals)

    left,right = st.columns([1.25,1])
    with left:
        st.subheader("Actividad de estudios")
        data = query_df("SELECT modality, COUNT(*) cantidad FROM studies GROUP BY modality ORDER BY cantidad DESC")
        if data.empty:
            st.info("Todavía no hay estudios registrados. Cuando agregues datos de prueba, el gráfico aparecerá aquí.")
        else:
            fig = px.bar(data, x="modality", y="cantidad", color="cantidad",
                         color_continuous_scale=["#B7DDE5","#267FA3"], labels={"modality":"Modalidad","cantidad":"Estudios"})
            fig.update_layout(showlegend=False, margin=dict(l=10,r=10,t=20,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Estados de turnos")
        data = query_df("SELECT status, COUNT(*) cantidad FROM appointments GROUP BY status")
        if data.empty:
            st.info("Los estados de turnos se mostrarán cuando existan registros.")
        else:
            fig = px.pie(data, names="status", values="cantidad", hole=.58,
                         color_discrete_sequence=["#267FA3","#5ABDAA","#83C9D5","#B8C9D2"])
            fig.update_layout(margin=dict(l=5,r=5,t=15,b=5), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
    st.subheader("Actividad reciente")
    activity = query_df("SELECT created_at AS Fecha, actor AS Usuario, action AS Acción, detail AS Detalle FROM activity ORDER BY id DESC LIMIT 8")
    if activity.empty:
        st.caption("Todavía no hay movimientos registrados.")
    else:
        st.dataframe(activity, use_container_width=True, hide_index=True)
