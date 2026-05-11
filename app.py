import streamlit as st
from datetime import datetime
import pandas as pd

# ============================================================
# APP DEMO - MENSAJERO INTERNO
# Demo conceptual sin envío real ni integración con base de datos
# ============================================================

st.set_page_config(
    page_title="Demo Mensajero Interno",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Catálogos demo
# -----------------------------

TIPOS_MENSAJE = [
    "SECTOR",
    "VIAJE REAL",
    "ROOMING",
    "POR CIUDAD",
    "POR BUS",
    "APP",
]

SUBOPCIONES = {
    "SECTOR": ["Operaciones", "Atención al Cliente", "Traslados", "Guías", "Producto", "Administración"],
    "VIAJE REAL": ["SCTOPO", "SCTPAR", "SCTMAD", "SCTROM", "SCTEUR"],
    "ROOMING": ["1 ROOMING", "VARIAS ROOMING"],
    "POR CIUDAD": ["1 CIUDAD", "VARIAS CIUDADES"],
    "POR BUS": ["BUS 1", "BUS 2", "BUS 3", "BUS 4", "BUS 5"],
    "APP": ["App Cliente", "App Guía", "App Operador", "App Interna"],
}

DESTINOS_NOTA = [
    "Observaciones del Resumen de Servicios",
    "Observaciones ATT Cliente/Guías",
    "+i Del Viaje",
    "+i Del Bus",
]

ALCANCE_RESERVAS = [
    "Reserva Específica",
    "Varias Reservas",
    "Todas las Reservas",
]

RESERVAS_DEMO = [
    "EMV-100245",
    "EMV-100246",
    "EMV-100247",
    "EMV-100248",
    "EMV-100249",
    "EMV-100250",
]

CIUDADES_DEMO = [
    "Madrid",
    "Barcelona",
    "París",
    "Roma",
    "Lisboa",
    "Londres",
    "Ámsterdam",
]

ROOMINGS_DEMO = [
    "RMG-SCTOPO-01",
    "RMG-SCTOPO-02",
    "RMG-SCTPAR-01",
    "RMG-SCTROM-01",
]


# -----------------------------
# Estado de sesión
# -----------------------------

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

if "contador" not in st.session_state:
    st.session_state.contador = 1


def limpiar_formulario():
    """Incrementa el contador para regenerar claves de widgets y limpiar campos."""
    st.session_state.contador += 1


def registrar_mensaje(payload: dict):
    st.session_state.mensajes.insert(0, payload)


def obtener_detalle_contexto(tipo_mensaje, subopcion, seleccion_multiple):
    if tipo_mensaje == "ROOMING":
        return ", ".join(seleccion_multiple) if seleccion_multiple else subopcion
    if tipo_mensaje == "POR CIUDAD":
        return ", ".join(seleccion_multiple) if seleccion_multiple else subopcion
    return subopcion


# -----------------------------
# Estilos básicos
# -----------------------------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #5f6368;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .demo-box {
        padding: 1rem;
        border-radius: 0.75rem;
        background-color: #f7f9fc;
        border: 1px solid #e3e8ef;
        margin-bottom: 1rem;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #5f6368;
    }
    .metric-value {
        font-size: 1.2rem;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:
    st.image("https://static.streamlit.io/examples/cat.jpg", width=80)
    st.title("Mensajero Demo")
    st.caption("Prototipo interno para validación de flujo.")

    st.divider()

    st.subheader("Indicadores Demo")
    st.metric("Mensajes generados", len(st.session_state.mensajes))
    mensajes_futuros = sum(1 for m in st.session_state.mensajes if m["agregar_a_nuevas_reservas"])
    st.metric("Mensajes aplicables a futuras reservas", mensajes_futuros)

    st.divider()

    if st.button("🧹 Limpiar historial demo", use_container_width=True):
        st.session_state.mensajes = []
        st.success("Historial eliminado correctamente.")


# -----------------------------
# Encabezado
# -----------------------------

st.markdown('<div class="main-title">✉️ Demo Mensajero Interno</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Herramienta conceptual para simular la creación y aplicación de mensajes internos sobre reservas, viajes, buses, ciudades, roomings o aplicaciones.</div>',
    unsafe_allow_html=True,
)

col_info_1, col_info_2, col_info_3 = st.columns(3)
with col_info_1:
    st.info("Demo sin envío real ni escritura en base de datos.")
with col_info_2:
    st.info("Permite validar lógica de negocio y experiencia de usuario.")
with col_info_3:
    st.info("Preparada para futura integración con Google Sheets, Firestore o API interna.")


# -----------------------------
# Formulario principal
# -----------------------------

st.subheader("1. Crear nuevo mensaje")

key_suffix = st.session_state.contador

with st.container(border=True):
    col1, col2 = st.columns([1, 1])

    with col1:
        tipo_mensaje = st.selectbox(
            "Tipo de mensaje",
            TIPOS_MENSAJE,
            index=None,
            placeholder="Seleccione el tipo de mensaje...",
            key=f"tipo_mensaje_{key_suffix}",
        )

    with col2:
        subopcion = None
        if tipo_mensaje:
            subopcion = st.selectbox(
                "Segunda opción / criterio",
                SUBOPCIONES[tipo_mensaje],
                index=None,
                placeholder="Seleccione una opción...",
                key=f"subopcion_{key_suffix}",
            )
        else:
            st.selectbox(
                "Segunda opción / criterio",
                [],
                index=None,
                placeholder="Primero seleccione el tipo de mensaje",
                disabled=True,
                key=f"subopcion_disabled_{key_suffix}",
            )

    seleccion_multiple = []

    if tipo_mensaje == "ROOMING" and subopcion == "VARIAS ROOMING":
        seleccion_multiple = st.multiselect(
            "Seleccione las roomings afectadas",
            ROOMINGS_DEMO,
            placeholder="Seleccione una o varias roomings...",
            key=f"roomings_{key_suffix}",
        )

    if tipo_mensaje == "POR CIUDAD" and subopcion == "VARIAS CIUDADES":
        seleccion_multiple = st.multiselect(
            "Seleccione las ciudades afectadas",
            CIUDADES_DEMO,
            placeholder="Seleccione una o varias ciudades...",
            key=f"ciudades_{key_suffix}",
        )

    if tipo_mensaje == "POR CIUDAD" and subopcion == "1 CIUDAD":
        ciudad_unica = st.selectbox(
            "Ciudad",
            CIUDADES_DEMO,
            index=None,
            placeholder="Seleccione la ciudad...",
            key=f"ciudad_unica_{key_suffix}",
        )
        seleccion_multiple = [ciudad_unica] if ciudad_unica else []

    agregar_a_nuevas_reservas = st.checkbox(
        "Agregar este mensaje a nuevas reservas",
        help="Simula que el mensaje quedará asociado a futuras reservas que cumplan el criterio seleccionado.",
        key=f"agregar_futuras_{key_suffix}",
    )

    st.divider()

    destino_nota = st.radio(
        "Destino de la nota",
        DESTINOS_NOTA,
        index=None,
        horizontal=False,
        key=f"destino_{key_suffix}",
    )

    alcance = st.radio(
        "El mensaje puede dirigirse a",
        ALCANCE_RESERVAS,
        index=None,
        horizontal=True,
        key=f"alcance_{key_suffix}",
    )

    reservas_seleccionadas = []

    if alcance == "Reserva Específica":
        reserva = st.selectbox(
            "Reserva",
            RESERVAS_DEMO,
            index=None,
            placeholder="Seleccione la reserva...",
            key=f"reserva_unica_{key_suffix}",
        )
        reservas_seleccionadas = [reserva] if reserva else []

    elif alcance == "Varias Reservas":
        reservas_seleccionadas = st.multiselect(
            "Reservas",
            RESERVAS_DEMO,
            placeholder="Seleccione una o varias reservas...",
            key=f"reservas_varias_{key_suffix}",
        )

    elif alcance == "Todas las Reservas":
        st.warning("Demo: el mensaje se aplicará a todas las reservas que cumplan el criterio seleccionado.")
        reservas_seleccionadas = ["Todas las Reservas"]

    st.divider()

    asunto = st.text_input(
        "Título interno del mensaje",
        placeholder="Ej.: Cambio de horario de traslado / Observación para guía / Aviso operativo",
        key=f"asunto_{key_suffix}",
    )

    mensaje = st.text_area(
        "Mensaje",
        placeholder="Ingrese aquí el contenido del mensaje interno...",
        height=180,
        key=f"mensaje_{key_suffix}",
    )

    prioridad = st.select_slider(
        "Prioridad",
        options=["Baja", "Media", "Alta", "Crítica"],
        value="Media",
        key=f"prioridad_{key_suffix}",
    )

    col_btn1, col_btn2 = st.columns([1, 1])

    with col_btn1:
        guardar = st.button("💾 Generar mensaje demo", type="primary", use_container_width=True)

    with col_btn2:
        if st.button("↩️ Limpiar formulario", use_container_width=True):
            limpiar_formulario()
            st.rerun()

    if guardar:
        errores = []

        if not tipo_mensaje:
            errores.append("Debe seleccionar el tipo de mensaje.")
        if tipo_mensaje and not subopcion:
            errores.append("Debe seleccionar la segunda opción / criterio.")
        if tipo_mensaje in ["ROOMING", "POR CIUDAD"] and subopcion in ["VARIAS ROOMING", "VARIAS CIUDADES"] and not seleccion_multiple:
            errores.append("Debe seleccionar al menos un elemento en la selección múltiple.")
        if tipo_mensaje == "POR CIUDAD" and subopcion == "1 CIUDAD" and not seleccion_multiple:
            errores.append("Debe seleccionar una ciudad.")
        if not destino_nota:
            errores.append("Debe seleccionar el destino de la nota.")
        if not alcance:
            errores.append("Debe seleccionar el alcance de reservas.")
        if alcance in ["Reserva Específica", "Varias Reservas"] and not reservas_seleccionadas:
            errores.append("Debe seleccionar al menos una reserva.")
        if not asunto.strip():
            errores.append("Debe ingresar un título interno del mensaje.")
        if not mensaje.strip():
            errores.append("Debe ingresar el contenido del mensaje.")

        if errores:
            for error in errores:
                st.error(error)
        else:
            payload = {
                "fecha_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "tipo_mensaje": tipo_mensaje,
                "criterio": obtener_detalle_contexto(tipo_mensaje, subopcion, seleccion_multiple),
                "agregar_a_nuevas_reservas": agregar_a_nuevas_reservas,
                "destino_nota": destino_nota,
                "alcance": alcance,
                "reservas": ", ".join(reservas_seleccionadas),
                "asunto": asunto.strip(),
                "mensaje": mensaje.strip(),
                "prioridad": prioridad,
                "estado_demo": "Generado - Sin envío real",
            }

            registrar_mensaje(payload)
            st.success("Mensaje demo generado correctamente.")
            st.balloons()


# -----------------------------
# Vista previa del último mensaje
# -----------------------------

if st.session_state.mensajes:
    st.subheader("2. Vista previa del último mensaje generado")

    ultimo = st.session_state.mensajes[0]

    with st.container(border=True):
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.markdown('<div class="metric-label">Tipo / Criterio</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{ultimo["tipo_mensaje"]}</div>', unsafe_allow_html=True)
            st.caption(ultimo["criterio"])

        with col_b:
            st.markdown('<div class="metric-label">Destino</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{ultimo["destino_nota"]}</div>', unsafe_allow_html=True)

        with col_c:
            st.markdown('<div class="metric-label">Alcance</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{ultimo["alcance"]}</div>', unsafe_allow_html=True)
            st.caption(ultimo["reservas"])

        st.divider()

        st.markdown(f"**Título:** {ultimo['asunto']}")
        st.markdown(f"**Prioridad:** {ultimo['prioridad']}")
        st.markdown(f"**Agregar a nuevas reservas:** {'Sí' if ultimo['agregar_a_nuevas_reservas'] else 'No'}")
        st.markdown("**Mensaje:**")
        st.write(ultimo["mensaje"])

        st.info("Esta vista simula cómo quedaría registrado el mensaje. No se envía ni se guarda fuera de la sesión actual.")


# -----------------------------
# Historial demo
# -----------------------------

st.subheader("3. Historial demo de mensajes")

if st.session_state.mensajes:
    df = pd.DataFrame(st.session_state.mensajes)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "mensaje": st.column_config.TextColumn("Mensaje", width="large"),
            "agregar_a_nuevas_reservas": st.column_config.CheckboxColumn("Futuras reservas"),
        },
    )

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ Descargar historial demo en CSV",
        data=csv,
        file_name="historial_mensajes_demo.csv",
        mime="text/csv",
        use_container_width=True,
    )
else:
    st.caption("Aún no se generaron mensajes en esta sesión.")


# -----------------------------
# Roadmap sugerido
# -----------------------------

with st.expander("Roadmap sugerido para convertir esta demo en herramienta real"):
    st.markdown(
        """
        **Fase 1 — Validación funcional**
        - Confirmar tipos de mensaje, destinos y reglas de aplicación.
        - Validar permisos por perfil de usuario.
        - Definir trazabilidad requerida.

        **Fase 2 — Persistencia**
        - Guardar mensajes en Google Sheets, Firestore o base SQL.
        - Registrar usuario creador, fecha, edición y estado.

        **Fase 3 — Integración operativa**
        - Conectar con reservas reales.
        - Aplicar mensajes automáticamente a futuras reservas según criterio.
        - Incorporar auditoría y control de cambios.

        **Fase 4 — Gobernanza**
        - Roles: lectura, creación, aprobación y administración.
        - Historial completo por reserva, viaje, bus, ciudad o rooming.
        """
    )

