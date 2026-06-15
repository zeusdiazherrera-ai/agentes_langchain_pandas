# agentes_langchain_pandas
Este repositorio contiene scripts de agentes en ReAct para el análisis de datos usando pandas para mayor efectividad

# Asistente Autónomo de Análisis de Datos con IA

Este proyecto consiste en una aplicación web empresarial diseñada para automatizar el análisis exploratorio, descriptivo y visual de conjuntos de datos en formato CSV. Utiliza una arquitectura basada en agentes de Inteligencia Artificial mediante **LangChain**, un motor lingüístico avanzado a través de la API de **DeepSeek**, y una interfaz de usuario interactiva construida con **Streamlit**.

La aplicación está completamente desplegada y disponible en producción en el siguiente enlace:
👉 **[Acceder a la Aplicación en la Nube](https://agentes-langchain-zdiaz.streamlit.app/)**

---

## Arquitectura del Sistema

A diferencia de los enfoques tradicionales basados en flujos de ejecución lineales o "scripts espagueti", este sistema implementa un patrón de diseño **Full-Stack de IA** modular, dividiendo estrictamente las responsabilidades entre la interfaz de usuario, la orquestación lingüística y la ejecución lógica de operaciones informáticas.

### Componentes Clave

1. **Orquestador ReAct (Reasoning and Acting):** Implementado mediante `create_react_agent` de LangChain. Permite al modelo de lenguaje alternar de forma autónoma entre fases de razonamiento y ejecución de acciones para resolver consultas complejas de forma iterativa.
2. **Inyección Dinámica de Dependencias:** El sistema no depende de un dataset estático local. Cuando el usuario carga un archivo CSV en la interfaz web, el DataFrame de Pandas es inyectado dinámicamente en tiempo de ejecución a cada una de las herramientas que el agente tiene a su disposición.
3. **Seguridad y Aislamiento de Credenciales:** Diseño orientado a producción que desacopla por completo las llaves de API (`API_KEYS`) del código fuente. Localmente se gestionan a través de variables de entorno (`python-dotenv`) y en producción mediante la bóveda segura de *Streamlit Secrets*, evitando la fuga de credenciales en repositorios públicos.

---

## Catálogo de Herramientas Especializadas

El agente mitiga el riesgo de alucinaciones y optimiza el consumo de tokens mediante un enrutamiento estricto guiado por *Negative Prompting*. Cuenta con cuatro herramientas específicas:

* **Herramienta Exploratoria (`Informaciones DF`):** Extrae la estructura del archivo mediante operaciones nativas de Pandas (`.shape`, `.dtypes`, `.isnull()`, `.duplicated()`). Retorna un diagnóstico sobre la limpieza del dataset, datos nulos, duplicados y sugerencias de preprocesamiento.
* **Herramienta Estadística (`Resumen Estadístico`):** Ejecuta un análisis estadístico descriptivo completo de las variables numéricas mediante la transposición limpia de un bloque `.describe()`. Identifica promedios, desviaciones estándar, rangos y posibles valores atípicos (outliers).
* **Herramienta Visual (`Generar Gráfico`):** Actúa como un programador bajo demanda. El LLM genera exclusivamente código limpio de Python (`Seaborn` y `Matplotlib`), el cual es ejecutado dinámicamente en un entorno seguro mediante `exec()`. Captura la figura resultante y la renderiza nativamente en la web a través de `st.pyplot()`.
* **Herramienta de Código Técnico (`Códigos de Python`):** Utiliza un entorno REPL (`PythonAstREPLTool`) para ejecutar consultas específicas y operaciones aritméticas puntuales pedidas por el usuario en lenguaje natural (ej. correlaciones exactas o filtrados categóricos).

---

## Stack Tecnológico

* **Core Framework:** LangChain 0.3 (LangChain-Core, LangChain-Community, LangChain-Experimental)
* **Modelos de Lenguaje:** DeepSeek Chat API (arquitectura compatible con OpenAI)
* **Interfaz de Usuario:** Streamlit 1.44
* **Procesamiento de Datos:** Pandas 2.2
* **Visualización Gráfica:** Matplotlib 3.10 & Seaborn 0.13
* **Entorno de Despliegue:** Streamlit Community Cloud (Python 3.12)

---

## Licencia

Este proyecto es de código abierto y está diseñado con fines educativos y de portafolio profesional en ingeniería de Inteligencia Artificial.
