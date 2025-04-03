import streamlit as st
import db

# ===== Crear tablas =====
db.crear_tablas()

# ===== Inicializar sesión =====
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False
    st.session_state["usuario"] = ""

# ===== Estilo general =====
st.markdown("""
<style>
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ===== Título =====
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📋 Gestor de Tareas</h1>", unsafe_allow_html=True)
st.markdown("---")

# ===== BARRA LATERAL =====
with st.sidebar:
    st.markdown("## 🔐 Menú")

    if st.session_state["logueado"]:
        st.write(f"👤 Usuario: **{st.session_state['usuario']}**")
        if st.button("Cerrar sesión"):
            st.session_state["logueado"] = False
            st.session_state["usuario"] = ""
            st.rerun()
    else:
        menu = st.radio("Acceso:", ["Iniciar sesión", "Registrarse"])

    st.markdown("---")
    st.markdown("Made with ❤️ by Zapata")

# ===== CONTENIDO PRINCIPAL =====
if not st.session_state["logueado"]:
    if menu == "Iniciar sesión":
        st.markdown("### 🔑 Iniciar sesión")
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Entrar"):
            if db.verificar_usuario(username, password):
                st.session_state["logueado"] = True
                st.session_state["usuario"] = username
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")

    elif menu == "Registrarse":
        st.markdown("### ✏️ Crear nueva cuenta")
        new_user = st.text_input("Nuevo usuario")
        new_password = st.text_input("Nueva contraseña", type="password")

        if st.button("Registrarse"):
            if new_user and new_password:
                if db.registrar_usuario(new_user, new_password):
                    st.success("✅ Usuario registrado con éxito")
                    st.balloons()
                else:
                    st.warning("⚠️ Ese usuario ya existe")
            else:
                st.warning("Rellena todos los campos")

else:
    st.success(f"✅ Bienvenido, **{st.session_state['usuario']}**!")

    usuario_id = db.obtener_id_usuario(st.session_state["usuario"])
    tareas = db.obtener_tareas(usuario_id)

    with st.container():
        st.markdown("### 🗂️ Tus tareas")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("Pulsa para eliminar una tarea:")
            if tareas:
                for tarea_id, texto in tareas:
                    if st.checkbox(f"{texto}", key=f"tarea_{tarea_id}"):
                        db.eliminar_tarea(tarea_id)
                        st.success(f"Tarea eliminada: {texto}")
                        st.rerun()
            else:
                st.info("No tienes tareas registradas")

        with col2:
            st.markdown("📊 Resumen")
            st.metric("Total de tareas", len(tareas))

    st.markdown("---")

    with st.container():
        st.markdown("### ➕ Añadir nueva tarea")
        nueva_tarea = st.text_input("Escribe tu tarea:")

        if st.button("Guardar tarea"):
            if nueva_tarea:
                db.agregar_tarea(usuario_id, nueva_tarea)
                st.success("✅ Tarea guardada correctamente")
                st.rerun()
            else:
                st.warning("Escribe algo antes de guardar")

    st.markdown("---")
    st.markdown("### 📈 Estadísticas globales")

    datos = db.contar_tareas_por_usuario()
    if datos:
        import pandas as pd
        df = pd.DataFrame(datos, columns=["Usuario", "Tareas"])
        st.bar_chart(df.set_index("Usuario"))
    else:
        st.info("Todavía no hay estadísticas para mostrar.")


    # ===== Footer =====
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray;'>© 2025 Gestor de Tareas - Proyecto Educativo</p>", unsafe_allow_html=True)
