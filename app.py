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

            fechas_ciudad = []
            tipo_fecha_ciudad = None

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
