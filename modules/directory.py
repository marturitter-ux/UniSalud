import streamlit as st
from modules.helpers import query_df, add_professional, add_institution

def show_professionals(actor):
    st.title("Profesionales")
    with st.expander("Registrar profesional",expanded=True):
        with st.form("prof_form",clear_on_submit=True):
            a,b=st.columns(2)
            name=a.text_input("Nombre y apellido *")
            specialty=b.text_input("Especialidad")
            c,d=st.columns(2)
            registration=c.text_input("Matrícula (demostración)")
            email=d.text_input("Correo")
            phone=st.text_input("Teléfono")
            ok=st.form_submit_button("Guardar profesional",type="primary")
            if ok:
                if name.strip():
                    add_professional(name,specialty,registration,email,phone,actor)
                    st.success("Profesional registrado."); st.rerun()
                else: st.error("Ingresá el nombre.")
    st.dataframe(query_df("SELECT id AS ID,full_name AS Profesional,specialty AS Especialidad,registration AS Matrícula,email AS Correo,phone AS Teléfono FROM professionals ORDER BY full_name"),use_container_width=True,hide_index=True)

def show_institutions(actor):
    st.title("Instituciones")
    with st.expander("Registrar institución",expanded=True):
        with st.form("inst_form",clear_on_submit=True):
            name=st.text_input("Nombre *")
            a,b=st.columns(2)
            kind=a.selectbox("Tipo",["Hospital","Clínica","Sanatorio","Centro de diagnóstico","Centro de salud","Otro"])
            city=b.text_input("Localidad")
            address=st.text_input("Dirección")
            contact=st.text_input("Contacto")
            ok=st.form_submit_button("Guardar institución",type="primary")
            if ok:
                if name.strip():
                    add_institution(name,kind,city,address,contact,actor)
                    st.success("Institución registrada."); st.rerun()
                else: st.error("Ingresá el nombre.")
    st.dataframe(query_df("SELECT id AS ID,name AS Institución,type AS Tipo,city AS Localidad,address AS Dirección,contact AS Contacto FROM institutions ORDER BY name"),use_container_width=True,hide_index=True)
