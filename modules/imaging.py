import streamlit as st
from modules.helpers import query_df, patient_options, add_study

MODALITIES = [
"Radiología convencional","Radiología digital directa","Radiografía computarizada",
"Radiología portátil","Radiología pediátrica","Radiología odontológica",
"Tomografía computada","Angio-TC","Resonancia magnética","Angio-RM",
"Ecografía","Ecografía Doppler","Mamografía digital","Tomosíntesis",
"Fluoroscopia / Arco en C","Hemodinamia / Angiografía","Procedimientos intervencionistas guiados por imágenes",
"Medicina nuclear","SPECT","PET / PET-CT","Densitometría ósea","CBCT",
"Simulación para radioterapia","Planificación 3D / IMRT / VMAT","Braquiterapia"
]

def show_imaging(actor):
    st.title("Diagnóstico por imágenes")
    st.caption("Registro organizado de estudios de las distintas modalidades.")
    tab1,tab2 = st.tabs(["Registrar estudio","Explorar estudios"])
    opts = patient_options()
    with tab1:
        if not opts:
            st.info("Primero registrá un paciente.")
        else:
            with st.form("study_form",clear_on_submit=True):
                patient = st.selectbox("Paciente",list(opts.keys()))
                modality = st.selectbox("Modalidad",MODALITIES)
                region = st.text_input("Región anatómica")
                date = st.date_input("Fecha del estudio")
                institution = st.text_input("Institución")
                professional = st.text_input("Profesional responsable")
                status = st.selectbox("Estado",["Pendiente","En proceso","Informado","Entregado"])
                report = st.text_area("Informe / observaciones (texto de prueba)")
                upload = st.file_uploader("Adjuntar archivo de demostración",type=["png","jpg","jpeg","pdf","dcm"])
                ok = st.form_submit_button("Guardar estudio",type="primary")
                if ok:
                    try:
                        filename = ""
                        if upload:
                            filename = upload.name
                            # En esta versión académica se registra el nombre, no se almacena el archivo.
                        add_study(opts[patient],modality,region,str(date),institution,professional,status,report,filename,actor)
                        st.success("Estudio registrado.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"No se pudo registrar el estudio: {e}")
    with tab2:
        f1,f2 = st.columns(2)
        filt = f1.selectbox("Filtrar modalidad",["Todas"]+MODALITIES)
        status = f2.selectbox("Filtrar estado",["Todos","Pendiente","En proceso","Informado","Entregado"])
        sql = """SELECT s.id AS ID,p.full_name AS Paciente,s.modality AS Modalidad,s.body_region AS Región,
        s.study_date AS Fecha,s.institution AS Institución,s.professional AS Profesional,s.status AS Estado,
        s.file_name AS Archivo,s.report AS Informe FROM studies s JOIN patients p ON p.id=s.patient_id WHERE 1=1"""
        params=[]
        if filt!="Todas": sql+=" AND s.modality=?"; params.append(filt)
        if status!="Todos": sql+=" AND s.status=?"; params.append(status)
        sql+=" ORDER BY s.study_date DESC"
        df=query_df(sql,tuple(params))
        st.dataframe(df,use_container_width=True,hide_index=True)
