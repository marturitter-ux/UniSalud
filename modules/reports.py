import streamlit as st
import pandas as pd
from modules.helpers import query_df

def show_reports():
    st.title("Estadísticas y reportes")
    st.caption("Indicadores calculados a partir de los registros de este prototipo.")
    studies=query_df("SELECT modality AS Modalidad,COUNT(*) AS Cantidad FROM studies GROUP BY modality ORDER BY Cantidad DESC")
    appts=query_df("SELECT status AS Estado,COUNT(*) AS Cantidad FROM appointments GROUP BY status")
    patients=query_df("SELECT id AS ID,document AS Documento,full_name AS Paciente,birth_date AS Nacimiento,created_at AS Registro FROM patients")
    a,b,c=st.columns(3)
    a.metric("Pacientes",len(patients)); b.metric("Estudios",int(studies["Cantidad"].sum()) if not studies.empty else 0)
    c.metric("Turnos",int(appts["Cantidad"].sum()) if not appts.empty else 0)
    st.subheader("Estudios por modalidad"); st.dataframe(studies,use_container_width=True,hide_index=True)
    st.subheader("Turnos por estado"); st.dataframe(appts,use_container_width=True,hide_index=True)
    st.subheader("Listado de pacientes"); st.dataframe(patients,use_container_width=True,hide_index=True)
    csv=patients.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Descargar listado de pacientes (CSV)",csv,"reporte_pacientes_unisalud.csv","text/csv")
    all_studies=query_df("""SELECT p.full_name AS Paciente,s.modality AS Modalidad,s.body_region AS Región,
    s.study_date AS Fecha,s.institution AS Institución,s.status AS Estado,s.report AS Informe
    FROM studies s JOIN patients p ON p.id=s.patient_id ORDER BY s.study_date DESC""")
    st.download_button("Descargar estudios (CSV)",all_studies.to_csv(index=False).encode("utf-8-sig"),
                       "reporte_estudios_unisalud.csv","text/csv")
