import streamlit as st
from modules.helpers import query_df, add_patient

def show_patients(actor):
    st.title("Pacientes")
    st.caption("Registro y consulta de pacientes de demostración.")
    tab1,tab2 = st.tabs(["Registrar paciente","Listado y búsqueda"])
    with tab1:
        with st.form("patient_form", clear_on_submit=True):
            a,b = st.columns(2)
            document = a.text_input("DNI / documento *")
            full_name = b.text_input("Nombre y apellido *")
            c,d = st.columns(2)
            birth = c.date_input("Fecha de nacimiento", value=None, min_value=None)
            phone = d.text_input("Teléfono")
            email = st.text_input("Correo electrónico")
            address = st.text_input("Domicilio")
            blood = st.selectbox("Grupo sanguíneo", ["No informado","A+","A-","B+","B-","AB+","AB-","O+","O-"])
            notes = st.text_area("Observaciones (datos ficticios)")
            ok = st.form_submit_button("Guardar paciente", type="primary")
            if ok:
                if not document.strip() or not full_name.strip():
                    st.error("Completá documento y nombre.")
                else:
                    try:
                        add_patient(document.strip(),full_name.strip(),str(birth or ""),phone,email,address,blood,notes,actor)
                        st.success("Paciente registrado.")
                        st.rerun()
                    except Exception as e:
                        st.error("No se pudo guardar. Revisá que el documento no esté repetido.")
    with tab2:
        q = st.text_input("Buscar por nombre o documento")
        df = query_df("""SELECT id AS ID, document AS Documento, full_name AS Paciente,
        birth_date AS Nacimiento, phone AS Teléfono, email AS Correo FROM patients
        WHERE full_name LIKE ? OR document LIKE ? ORDER BY full_name""",(f"%{q}%",f"%{q}%"))
        st.dataframe(df,use_container_width=True,hide_index=True)
        if not df.empty:
            chosen = st.selectbox("Abrir ficha", df["ID"].tolist(), format_func=lambda x: f"Paciente #{x}")
            record = query_df("SELECT * FROM patients WHERE id=?",(chosen,))
            if not record.empty:
                st.markdown("#### Ficha del paciente")
                st.json(record.iloc[0].fillna("").to_dict())
