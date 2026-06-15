import pandas as pd
import streamlit as st
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate

# IMPORTAMOS DEEPSEEK (Sustituyendo a Groq)
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from herramientas import crear_herramientas
from my_keys import DEEPSEEK_API_KEY
from my_models import DEEPSEEK_CHAT

# Inicia la aplicación
st.set_page_config(
    page_title="Asistente de Análisis de Datos con IA", layout="centered"
)
st.title("🦜 Asistente de Análisis de Datos con IA")

# Descripción de la herramienta
st.info("""
Este asistente utiliza un agente, creado con Langchain, para ayudarte a explorar, 
        analizar y visualizar datos de forma interactiva.
Basta con subir un archivo CSV y podrás:

* 📄 **Generar reportes automáticos**:
  * **Reporte de información general**: dimensión, nulos, duplicados y tratamientos.
  * **Reporte de estadísticas descriptivas**: media, mediana, desviación, outliers.
* 🔎 **Hacer preguntas simples sobre los datos**.
* 📊 **Crear gráficos automáticamente** a partir de lenguaje natural.
""")

# Upload de CSV
st.markdown("### 📁 Realiza la carga de tu archivo CSV")
archivo_cargado = st.file_uploader(
    "Selecciona un archivo CSV", type="csv", label_visibility="collapsed"
)

if archivo_cargado:
    df = pd.read_csv(archivo_cargado)
    st.success("¡Archivo cargado exitosamente!")
    st.markdown("### 🔍 Primeras filas de tu conjunto de datos")
    st.dataframe(df.head())

    # 🧠 INICIALIZAMOS DEEPSEEK EN LUGAR DE GROQ
    llm = ChatOpenAI(
        api_key=SecretStr(str(DEEPSEEK_API_KEY)),
        model=DEEPSEEK_CHAT,
        base_url="https://api.deepseek.com",
        temperature=0.0,
    )

    # Herramientas
    tools = crear_herramientas(df)

    # Prompt react
    df_head = df.head().to_markdown()

    prompt_react_es = PromptTemplate(
        input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
        partial_variables={"df_head": df_head},
        template="""
            Eres un asistente que responde en castellano.

            Tienes acceso a un dataframe pandas llamado `df`.
            Aquí están las primeras filas del DataFrame:
            
            {df_head}

            Responde a las siguientes preguntas de la mejor manera posible.
            Para este fin, tienes acceso a las siguientes herramientas:

            {tools}

            Usa el siguiente formato:

            Question: La pregunta de entrada que debes responder
            Thought: Debes siempre pensar en lo que debes hacer
            Action: La acción que será ejecutada, debe ser una de las [{tool_names}]
            Action Input: La entrada para la acción
            Observation: El resultado de la acción
            ... (este Thought/Action/Action Input/Observation puede repetirse N veces)
            Thought: Ahora sé la respuesta final
            Final Answer: La respuesta final para la pregunta de entrada inicial.

            Comienza!

            Question: {input}
            Thought: {agent_scratchpad}
        """,
    )

    # Agente
    agente = create_react_agent(llm=llm, tools=tools, prompt=prompt_react_es)
    orquestador = AgentExecutor(
        agent=agente,
        tools=tools,
        verbose=True,  # Verás el pensamiento en la terminal de VS Code
        handle_parsing_errors=True,
    )

    # ACCIONES RÁPIDAS
    st.markdown("---")
    st.markdown("## ⚡ Acciones rápidas")

    # Reporte de Informaciones Generales (Corregido el idioma a Español)
    if st.button("📄 Reporte de Informaciones Generales", key="boton_reporte_general"):
        with st.spinner("Generando Reporte 🦜..."):
            respuesta = orquestador.invoke(
                {
                    "input": "Quiero un reporte con la información general sobre los datos"
                }
            )
            st.session_state["reporte_general"] = respuesta["output"]

    # Exhibe el reporte con botón de descarga
    if "reporte_general" in st.session_state:
        with st.expander("Resultado: Reporte de Informaciones Generales"):
            st.markdown(st.session_state["reporte_general"])
            st.download_button(
                label="📥 Descargar Reporte",
                data=st.session_state["reporte_general"],
                file_name="reporte_informaciones_generales.md",
                mime="text/markdown",
            )

    # Reporte de estadísticas descriptivas
    if st.button(
        "📄 Reporte de estadísticas descriptivas", key="boton_reporte_estadisticas"
    ):
        with st.spinner("Generando Reporte 🦜..."):
            respuesta = orquestador.invoke(
                {"input": "Quiero un Reporte de estadísticas descriptivas"}
            )
            st.session_state["reporte_estadisticas"] = respuesta["output"]

    # Exhibe el reporte almacenado con opción de descarga
    if "reporte_estadisticas" in st.session_state:
        with st.expander("Resultado: Reporte de estadísticas descriptivas"):
            st.markdown(st.session_state["reporte_estadisticas"])
            st.download_button(
                label="📥 Descargar Reporte",
                data=st.session_state["reporte_estadisticas"],
                file_name="reporte_estadisticas_descritivas.md",
                mime="text/markdown",
            )

    # PREGUNTA SOBRE LOS DATOS
    st.markdown("---")
    st.markdown("## 🔎 Preguntas sobre los datos")
    pregunta_sobre_datos = st.text_input(
        "Realiza una pregunta sobre los datos (ej: '¿Cuál es el promedio de tiempo de entrega?')"
    )
    if st.button("Responder pregunta", key="responder_pregunta_datos"):
        if pregunta_sobre_datos:
            with st.spinner("Analizando los datos 🦜..."):
                respuesta = orquestador.invoke({"input": pregunta_sobre_datos})
                st.markdown((respuesta["output"]))
        else:
            st.warning("Por favor, escribe una pregunta primero.")

    # GENERACIÓN DE GRÁFICOS
    st.markdown("---")
    st.markdown("## 📊 Crear gráfico con base en una pregunta")

    pregunta_grafico = st.text_input(
        "¿Qué deseas visualizar? (ej: 'Genera un gráfico del promedio de tiempo de entrega por clima.')"
    )
    if st.button("Generar gráfico", key="generar_grafico"):
        if pregunta_grafico:
            with st.spinner("Generando el gráfico 🦜..."):
                orquestador.invoke({"input": pregunta_grafico})
        else:
            st.warning("Por favor, escribe qué gráfico deseas generar.")
