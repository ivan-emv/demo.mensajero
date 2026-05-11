import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="Demo Mensajero Interno",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded",
)

hide_streamlit_style = """
    <style>
        /* Oculta el menú hamburguesa de Streamlit y el footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Mantén el header visible para conservar el botón de expandir/contraer la barra lateral.
           Solo ocultamos las acciones de la derecha (Share / Favorito) */
        header [data-testid="stToolbarActions"] {display: none !important;}

        /* En algunas versiones, Share/Fav aparecen dentro del AppToolbar */
        [data-testid="stAppToolbar"] [data-testid="stToolbarActions"] {display: none !important;}
    </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)


TEMPORADAS = ["2025/2026", "2026/2027", "2027/2028"]

TIPOS_MENSAJE = ["VIAJE REAL", "APP"]

VIAJES_REALES = [
    "SCTOPO",
    "SCANDALU",
    "MIESTE",
    "SCTPAR",
    "SCTROM",
]

ALCANCES_VIAJE = ["SECTOR", "ROOMING", "CIUDAD"]

SECTORES_DEMO = [
    "MADRID",
    "MADRID-GRANADA",
    "MADRID-OPORTO",
    "BURDEOS-PARÍS",
    "ROMA-FLORENCIA",
]

ROOMINGS_DEMO = [
    "RMG-SCTOPO-01",
    "RMG-SCTOPO-02",
    "RMG-SCANDALU-01",
    "RMG-MIESTE-01",
]

CIUDADES_DEMO = [
    "Madrid",
    "Granada",
    "Oporto",
    "Burdeos",
    "París",
    "Roma",
]

APP_OPCIONES = [
    "App Cliente",
    "App Guía",
    "App Operador",
    "App Interna",
]

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

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

st.title("✉️ Demo Mensajero Interno")
st.caption("Prototipo conceptual para demostrar el flujo de carga de mensajes internos.")

with st.sidebar:
    st.header("Panel Demo")
    st.metric("Mensajes generados", len(st.session_state.mensajes))

    if st.button("Limpiar historial"):
        st.session_state.mensajes = []
        st.rerun()

st.subheader("1. Crear mensaje")

with st.container(border=True):
    temporada = st.selectbox(
        "Temporada",
        TEMPORADAS,
        index=None,
        placeholder="Seleccione la temporada...",
    )

    tipo_mensaje = st.selectbox(
        "Tipo de Mensaje",
        TIPOS_MENSAJE,
        index=None,
        placeholder="Seleccione el tipo de mensaje...",
    )

    viaje_real = None
    alcance_viaje = None
    detalle_alcance = None
    seleccion_detalle = []
    tipo_fecha_ciudad = None
    fechas_ciudad = []

    if tipo_mensaje == "VIAJE REAL":
        viaje_real = st.selectbox(
            "Viaje Real",
            VIAJES_REALES,
            index=None,
            placeholder="Seleccione el viaje real...",
        )

        alcance_viaje = st.selectbox(
            "Alcance dentro del viaje",
            ALCANCES_VIAJE,
            index=None,
            placeholder="Seleccione SECTOR, ROOMING o CIUDAD...",
        )

        if alcance_viaje == "SECTOR":
            seleccion_detalle = st.multiselect(
                "Sector / tramo específico",
                SECTORES_DEMO,
                placeholder="Seleccione uno o varios sectores...",
            )
            detalle_alcance = ", ".join(seleccion_detalle)

        elif alcance_viaje == "ROOMING":
            tipo_rooming = st.radio(
                "Tipo de Rooming",
                ["1 ROOMING", "VARIAS ROOMING"],
                horizontal=True,
                index=None,
            )

            if tipo_rooming == "1 ROOMING":
                rooming = st.selectbox(
                    "Rooming",
                    ROOMINGS_DEMO,
                    index=None,
                    placeholder="Seleccione una rooming...",
                )
                seleccion_detalle = [rooming] if rooming else []
                detalle_alcance = rooming

            elif tipo_rooming == "VARIAS ROOMING":
                seleccion_detalle = st.multiselect(
                    "Roomings",
                    ROOMINGS_DEMO,
                    placeholder="Seleccione una o varias roomings...",
                )
                detalle_alcance = ", ".join(seleccion_detalle)

        elif alcance_viaje == "CIUDAD":
            tipo_ciudad = st.radio(
                "Tipo de Ciudad",
                ["1 CIUDAD", "VARIAS CIUDADES"],
                horizontal=True,
                index=None,
            )

            if tipo_ciudad == "1 CIUDAD":
                ciudad = st.selectbox(
                    "Ciudad",
                    CIUDADES_DEMO,
                    index=None,
                    placeholder="Seleccione una ciudad...",
                )
                seleccion_detalle = [ciudad] if ciudad else []

            elif tipo_ciudad == "VARIAS CIUDADES":
                seleccion_detalle = st.multiselect(
                    "Ciudades",
                    CIUDADES_DEMO,
                    placeholder="Seleccione una o varias ciudades...",
                )

            if seleccion_detalle:
                tipo_fecha_ciudad = st.radio(
                    "Fecha de aplicación para ciudad",
                    ["1 FECHA", "VARIAS FECHAS"],
                    horizontal=True,
                    index=None,
                )

                if tipo_fecha_ciudad == "1 FECHA":
                    fecha_unica = st.date_input(
                        "Fecha",
                        value=None,
                        format="DD/MM/YYYY",
                    )

                    if fecha_unica:
                        fechas_ciudad = [fecha_unica.strftime("%d/%m/%Y")]

                elif tipo_fecha_ciudad == "VARIAS FECHAS":
                    fechas_seleccionadas = st.date_input(
                        "Fechas",
                        value=[],
                        format="DD/MM/YYYY",
                    )

                    if fechas_seleccionadas:
                        fechas_ciudad = [
                            fecha.strftime("%d/%m/%Y")
                            for fecha in fechas_seleccionadas
                        ]

            detalle_alcance = " | ".join(
                [
                    f"Ciudades: {', '.join(seleccion_detalle)}" if seleccion_detalle else "",
                    f"Fechas: {', '.join(fechas_ciudad)}" if fechas_ciudad else "",
                ]
            ).strip(" | ")

    elif tipo_mensaje == "APP":
        viaje_real = "No aplica"
        alcance_viaje = "APP"

        detalle_alcance = st.selectbox(
            "Opción APP",
            APP_OPCIONES,
            index=None,
            placeholder="Seleccione la opción APP...",
        )

        seleccion_detalle = [detalle_alcance] if detalle_alcance else []

    agregar_a_nuevas_reservas = st.checkbox(
        "Agregar este mensaje a nuevas reservas",
        help="Si se selecciona, el mensaje se adicionará a futuras reservas asociadas al criterio elegido.",
    )

    destino_nota = st.radio(
        "Destino de la Nota",
        DESTINOS_NOTA,
        index=None,
    )

    alcance_reservas = st.radio(
        "El mensaje puede dirigirse a",
        ALCANCE_RESERVAS,
        horizontal=True,
        index=None,
    )

    reservas_seleccionadas = []
    modo_carga_reservas = None

    if alcance_reservas == "Reserva Específica":
        localizador = st.text_input(
            "Localizador",
            placeholder="Ej.: AB123456",
            help="Ingrese manualmente el localizador de la reserva.",
        )

        reservas_seleccionadas = [localizador.strip().upper()] if localizador.strip() else []

    elif alcance_reservas == "Varias Reservas":
        modo_carga_reservas = st.radio(
            "Modo de selección de reservas",
            [
                "Escribir manualmente",
                "Seleccionar reservas según datos del viaje",
            ],
            horizontal=True,
            index=None,
        )

        if modo_carga_reservas == "Escribir manualmente":
            localizadores_texto = st.text_area(
                "Localizadores",
                placeholder="Ingrese un localizador por línea. Ej.:\nAB123456\nCD789012\nEF345678",
                height=120,
                help="Puede escribir varios localizadores, uno por línea.",
            )

            reservas_seleccionadas = [
                loc.strip().upper()
                for loc in localizadores_texto.splitlines()
                if loc.strip()
            ]

        elif modo_carga_reservas == "Seleccionar reservas según datos del viaje":
            reservas_seleccionadas = st.multiselect(
                "Reservas disponibles del viaje",
                RESERVAS_DEMO,
                placeholder="Seleccione una o varias reservas...",
                help="En una versión real, este listado se filtraría según temporada, viaje real y alcance seleccionado.",
            )

    elif alcance_reservas == "Todas las Reservas":
        reservas_seleccionadas = ["Todas las Reservas"]
        st.warning("El mensaje se aplicará a todas las reservas que cumplan el criterio seleccionado.")

    st.divider()

    st.markdown("### Resumen del criterio")
    st.info(
        f"{temporada or 'Temporada'} → "
        f"{tipo_mensaje or 'Tipo'} → "
        f"{viaje_real or 'Viaje'} → "
        f"{alcance_viaje or 'Alcance'} → "
        f"{detalle_alcance or 'Detalle'}"
    )

    asunto = st.text_input(
        "Título interno del mensaje",
        placeholder="Ej.: Cambio de horario de traslado",
    )

    mensaje = st.text_area(
        "Mensaje",
        placeholder="Ingrese aquí el contenido del mensaje interno...",
        height=160,
    )

    prioridad = st.selectbox(
        "Prioridad",
        ["Baja", "Media", "Alta", "Crítica"],
        index=1,
    )

    guardar = st.button("💾 Generar mensaje demo", type="primary")

    if guardar:
        errores = []

        if not temporada:
            errores.append("Debe seleccionar la temporada.")

        if not tipo_mensaje:
            errores.append("Debe seleccionar el tipo de mensaje.")

        if tipo_mensaje == "VIAJE REAL":
            if not viaje_real:
                errores.append("Debe seleccionar el viaje real.")

            if not alcance_viaje:
                errores.append("Debe seleccionar el alcance dentro del viaje.")

            if alcance_viaje in ["SECTOR", "ROOMING", "CIUDAD"] and not seleccion_detalle:
                errores.append("Debe seleccionar al menos un detalle del alcance.")

            if alcance_viaje == "CIUDAD":
                if not tipo_fecha_ciudad:
                    errores.append("Debe seleccionar si la ciudad aplica para una fecha o varias fechas.")
                if not fechas_ciudad:
                    errores.append("Debe seleccionar al menos una fecha para la ciudad.")

        if tipo_mensaje == "APP":
            if not detalle_alcance:
                errores.append("Debe seleccionar una opción APP.")

        if not destino_nota:
            errores.append("Debe seleccionar el destino de la nota.")

        if not alcance_reservas:
            errores.append("Debe seleccionar a qué reservas se dirige el mensaje.")

        if alcance_reservas == "Varias Reservas" and not modo_carga_reservas:
            errores.append("Debe seleccionar el modo de carga de reservas.")

        if alcance_reservas in ["Reserva Específica", "Varias Reservas"] and not reservas_seleccionadas:
            errores.append("Debe ingresar o seleccionar al menos una reserva.")

        if not asunto.strip():
            errores.append("Debe ingresar un título interno.")

        if not mensaje.strip():
            errores.append("Debe ingresar el mensaje.")

        if errores:
            for error in errores:
                st.error(error)
        else:
            nuevo_mensaje = {
                "Fecha/Hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Temporada": temporada,
                "Tipo Mensaje": tipo_mensaje,
                "Viaje Real": viaje_real,
                "Alcance Viaje": alcance_viaje,
                "Detalle Alcance": detalle_alcance,
                "Fechas Ciudad": ", ".join(fechas_ciudad) if fechas_ciudad else "",
                "Agregar a Nuevas Reservas": "Sí" if agregar_a_nuevas_reservas else "No",
                "Destino Nota": destino_nota,
                "Alcance Reservas": alcance_reservas,
                "Reservas": ", ".join(reservas_seleccionadas),
                "Título": asunto,
                "Mensaje": mensaje,
                "Prioridad": prioridad,
                "Estado": "Demo - No enviado",
            }

            st.session_state.mensajes.insert(0, nuevo_mensaje)
            st.success("Mensaje demo generado correctamente.")

st.subheader("2. Historial demo")

if st.session_state.mensajes:
    df = pd.DataFrame(st.session_state.mensajes)
    st.dataframe(df, use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ Descargar historial CSV",
        data=csv,
        file_name="historial_mensajes_demo.csv",
        mime="text/csv",
    )
else:
    st.caption("Aún no se generaron mensajes.")
