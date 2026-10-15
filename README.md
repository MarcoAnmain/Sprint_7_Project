# Sprint_7_Project
Sprint_7_Project

# Panel de ventas de vehículos ligeros en México

Aplicación web desarrollada con Streamlit para explorar las ventas
de vehículos ligeros reportadas al INEGI en México durante 2021–2026.

Está orientada a personas interesadas en consultar tendencias de ventas
por marca, segmento y modelo, y comparar su evolución entre años.

## Funcionalidades

- Filtros por marca, segmento, modelo y años.
- Tabla opcional con los registros seleccionados.
- Gráfico de evolución mensual de ventas.
- Histograma de la distribución de ventas mensuales.
- Gráfico de dispersión para comparar el mismo mes entre dos años.

## Datos y alcance

Fuente: Registro Administrativo de la Industria Automotriz de Vehículos
Ligeros (RAIAVL) del INEGI.

https://www.inegi.org.mx/datosprimarios/iavl/

El archivo `ventas_autos_mexico.csv` se preparó a partir del tabulado
descargado del INEGI, conservando sus registros y retirando los títulos
y notas que acompañaban la tabla.

Los años 2021–2025 contienen periodos completos. Los datos de 2026
están disponibles hasta septiembre.

Los guiones de la fuente se tratan como valores ausentes, no como
cero ventas. Pueden indicar modelos que no se comercializaban en
un periodo o que dejaron de reportarse.

Las sumas corresponden a cifras disponibles de las marcas que reportan
al registro. La disponibilidad de datos puede variar entre marcas
y periodos. El gráfico de dispersión compara únicamente meses con
cifras en ambos años.

El país de origen corresponde al origen de fabricación del vehículo,
no necesariamente a la nacionalidad de la marca.

## Archivos del proyecto

- `app.py`: código de la aplicación web.
- `ventas_autos_mexico.csv`: datos utilizados.
- `notebooks/EDA.ipynb`: preparación, exploración y visualización de datos.
- `requirements.txt`: librerías necesarias para ejecutar la aplicación.
- `.gitignore`: archivos y carpetas excluidos del repositorio.

## Tecnologías utilizadas

- Python
- pandas
- Plotly Express
- Streamlit

## Ejecución local

Desde la carpeta del proyecto, con un entorno de Python activo,
instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

Iniciar la aplicación:

```bash
python -m streamlit run app.py
```

Para ejecutar el notebook también se necesitan `ipykernel` y `nbformat`.

## Aplicación en Render

Pendiente de despliegue. Se añadirá aquí el enlace público.
