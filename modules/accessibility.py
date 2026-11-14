import streamlit as st

def show_accessibility():
    st.title("Accesibilidad y configuración")
    st.caption("Opciones de presentación para facilitar el uso de UniSalud.")
    st.subheader("Preferencias visuales")
    scale=st.select_slider("Tamaño de letra",options=["Pequeño","Normal","Grande","Muy grande"],value="Normal")
    contrast=st.toggle("Activar alto contraste")
    simple=st.toggle("Interfaz simplificada")
    st.subheader("Ayudas de navegación")
    st.checkbox("Mostrar etiquetas descriptivas en los botones",value=True)
    st.checkbox("Resaltar campos obligatorios",value=True)
    st.info("Estas preferencias son demostrativas en esta versión. La accesibilidad completa requiere pruebas con usuarios y tecnologías de asistencia.")
    if st.button("Aplicar preferencias",type="primary"):
        st.session_state["font_scale"]=scale
        st.session_state["high_contrast"]=contrast
        st.session_state["simple_mode"]=simple
        st.success("Preferencias aplicadas durante esta sesión.")
