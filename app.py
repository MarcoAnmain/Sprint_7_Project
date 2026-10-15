import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title='Ventas de vehículos en México',
    layout='wide'
)

st.header('Panel de ventas de vehículos ligeros en México')

st.write(
    'Explora tendencias de ventas por marca, segmento y modelo, '
    'y compara su evolución entre distintos años.'
)

st.caption(
    'Fuente: INEGI. Los datos de 2026 están disponibles hasta septiembre. '
    'Los valores ausentes no representan cero ventas.'
)

# Cargar y preparar los datos
ventas = pd.read_csv('ventas_autos_mexico.csv')

ventas['descripcion_vehiculo'] = (
    ventas['descripcion_vehiculo']
    .str.strip()
    .str.lower()
)

# Separar las características conservando los guiones del modelo
partes = ventas['descripcion_vehiculo'].str.rsplit(
    ' - ', n=4, expand=True
)

marca_modelo = partes[0].str.split(
    ' - ', n=1, expand=True
)

separadas = pd.concat(
    [marca_modelo, partes.iloc[:, 1:]],
    axis=1
)

columnas = [
    'marca', 'modelo', 'tipo',
    'segmento', 'origen', 'pais_origen'
]

separadas.columns = columnas
ventas[columnas] = separadas

# Conservar los ausentes y los ceros reales
ventas['ventas'] = pd.to_numeric(
    ventas['ventas'].replace('-', pd.NA),
    errors='raise'
).astype('Int64')

# Ordenar los meses
orden_meses = [
    'enero', 'febrero', 'marzo', 'abril',
    'mayo', 'junio', 'julio', 'agosto',
    'septiembre', 'octubre', 'noviembre', 'diciembre'
]

ventas['mes_numero'] = (
    ventas['mes']
    .str.strip()
    .str.lower()
    .map({
        mes: numero
        for numero, mes in enumerate(orden_meses, start=1)
    })
)

# Filtros de marca, segmento, modelo y años
st.subheader('Selecciona qué quieres explorar')

marcas_disponibles = sorted(
    ventas.loc[ventas['ventas'].notna(), 'marca'].unique()
)

marca_elegida = st.selectbox(
    'Marca',
    options=marcas_disponibles
)

datos_marca = ventas.loc[
    ventas['marca'] == marca_elegida
].copy()

segmentos_disponibles = sorted(
    datos_marca.loc[
        datos_marca['ventas'].notna(),
        'segmento'
    ].unique()
)

segmento_elegido = st.selectbox(
    'Segmento',
    options=['Todos los segmentos'] + segmentos_disponibles
)

datos_segmento = datos_marca.copy()

if segmento_elegido != 'Todos los segmentos':
    datos_segmento = datos_segmento.loc[
        datos_segmento['segmento'] == segmento_elegido
    ].copy()

modelos_disponibles = sorted(
    datos_segmento.loc[
        datos_segmento['ventas'].notna(),
        'modelo'
    ].unique()
)

modelo_elegido = st.selectbox(
    'Modelo',
    options=['Todos los modelos'] + modelos_disponibles
)

anios_elegidos = st.multiselect(
    'Años que quieres comparar',
    options=sorted(ventas['anio'].unique()),
    default=[2025, 2026]
)

ventas_filtradas = datos_segmento.loc[
    datos_segmento['anio'].isin(anios_elegidos)
].copy()

if modelo_elegido != 'Todos los modelos':
    ventas_filtradas = ventas_filtradas.loc[
        ventas_filtradas['modelo'] == modelo_elegido
    ].copy()

seleccion = marca_elegida.title()

if segmento_elegido != 'Todos los segmentos':
    seleccion += f' · {segmento_elegido}'

if modelo_elegido != 'Todos los modelos':
    seleccion += f' · {modelo_elegido}'

st.caption(f'Selección: {seleccion}')

# Tabla opcional
mostrar_tabla = st.checkbox('Mostrar datos de la selección')

if mostrar_tabla:
    st.dataframe(
        ventas_filtradas.sort_values(
            ['anio', 'mes_numero', 'modelo']
        )[
            ['anio', 'mes', 'marca', 'modelo', 'segmento', 'ventas']
        ]
    )

# Resumen mensual para alimentar los gráficos
datos_tendencia = (
    ventas_filtradas
    .groupby(['anio', 'mes_numero'])['ventas']
    .sum(min_count=1)
    .reset_index(name='ventas_totales')
    .sort_values(['anio', 'mes_numero'])
)

# Tendencia mensual
st.subheader('Tendencia mensual de ventas')

if datos_tendencia['ventas_totales'].notna().any():
    datos_linea = datos_tendencia.copy()
    datos_linea['anio'] = datos_linea['anio'].astype(str)

    fig_tendencia = px.line(
        datos_linea,
        x='mes_numero',
        y='ventas_totales',
        color='anio',
        markers=True,
        title=f'Ventas mensuales: {seleccion}',
        labels={
            'mes_numero': 'Mes',
            'ventas_totales': 'Vehículos vendidos',
            'anio': 'Año'
        }
    )

    fig_tendencia.update_xaxes(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=[mes.capitalize() for mes in orden_meses]
    )

    st.plotly_chart(fig_tendencia)
else:
    st.info('Selecciona años con cifras disponibles para estos filtros.')

# Histograma
st.subheader('Distribución de ventas mensuales')

mostrar_histograma = st.checkbox('Mostrar histograma')

if mostrar_histograma:
    datos_histograma = datos_tendencia.dropna(
        subset=['ventas_totales']
    )

    if not datos_histograma.empty:
        fig_histograma = px.histogram(
            datos_histograma,
            x='ventas_totales',
            nbins=8,
            title=f'Distribución de ventas mensuales: {seleccion}',
            labels={
                'ventas_totales': 'Vehículos vendidos en un mes'
            }
        )

        fig_histograma.update_yaxes(
            title_text='Cantidad de meses',
            dtick=1
        )

        st.plotly_chart(fig_histograma)

        st.caption(
            'Cada registro representa un mes de uno de los años '
            'seleccionados. Las barras cuentan cuántos registros '
            'caen en cada rango de ventas.'
        )
    else:
        st.info('No hay cifras disponibles para la selección.')

# Dispersión
st.subheader('Comparación de ventas entre dos años')

mostrar_dispersion = st.checkbox('Mostrar gráfico de dispersión')

if mostrar_dispersion:
    if len(anios_elegidos) < 2:
        st.info('Selecciona al menos dos años para compararlos.')
    else:
        anios_comparables = sorted(anios_elegidos)

        anio_base = st.selectbox(
            'Año de referencia',
            options=anios_comparables,
            index=0
        )

        anio_comparacion = st.selectbox(
            'Año para comparar',
            options=[
                anio for anio in anios_comparables
                if anio != anio_base
            ]
        )

        # Comparar únicamente meses con cifras en ambos años
        comparacion = (
            datos_tendencia
            .pivot(
                index='mes_numero',
                columns='anio',
                values='ventas_totales'
            )
            .reindex(columns=[anio_base, anio_comparacion])
            .dropna()
            .reset_index()
        )

        comparacion.columns = [
            'mes_numero', 'ventas_base', 'ventas_comparacion'
        ]

        if comparacion.empty:
            st.info('No hay meses con cifras disponibles en ambos años.')
        else:
            comparacion['mes'] = comparacion['mes_numero'].map(
                {
                    numero: mes.capitalize()
                    for numero, mes in enumerate(orden_meses, start=1)
                }
            )

            fig_dispersion = px.scatter(
                comparacion,
                x='ventas_base',
                y='ventas_comparacion',
                text='mes_numero',
                hover_name='mes',
                title=(
                    f'{seleccion}: '
                    f'{anio_base} frente a {anio_comparacion}'
                ),
                labels={
                    'ventas_base': f'Vehículos vendidos en {anio_base}',
                    'ventas_comparacion': (
                        f'Vehículos vendidos en {anio_comparacion}'
                    ),
                    'mes_numero': 'Número de mes'
                }
            )

            fig_dispersion.update_traces(
                textposition='top center'
            )

            limite = comparacion[
                ['ventas_base', 'ventas_comparacion']
            ].max().max()

            fig_dispersion.add_shape(
                type='line',
                x0=0,
                y0=0,
                x1=limite,
                y1=limite,
                line=dict(color='gray', dash='dash')
            )

            st.plotly_chart(fig_dispersion)

            st.caption(
                'Cada punto representa el mismo mes en ambos años '
                '(1 = enero, 12 = diciembre). '
                'Arriba de la línea gris, las ventas fueron mayores '
                'en el año de comparación; debajo, fueron menores. '
                'Solo se incluyen meses con cifras en ambos años.'
            )
