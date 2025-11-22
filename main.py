from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, AIMessage, SystemMessage
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

#configuración inicial streamlit
st.set_page_config(
    page_title="Mi Chatbot",
    page_icon="🤖"
)
st.title("🤖 Chatbot con Langchain")
st.markdown("Este es un chatbot base construido con Langchain y Streamlit")


#sidebar de configuración de parámetros del chat
with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-5-nano", "gpt-5-mini", "gpt-4o-mini"])

    #recrear modelo
    chat_model = ChatOpenAI(model=model_name, temperature=temperature)


# Inicializar el historial de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


# iterar por los mensajes
for msg in st.session_state.mensajes:
    #validar si el mensaje es de tipo SystemMessage para no imprimirlo
    if isinstance(msg, SystemMessage):
        continue
    
    #escribir mensaje
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
         st.markdown(msg.content)


#cuadro de entrada de texto de usuario
pregunta = st.chat_input("Ask anything...")

if pregunta:
    #Mostrar inmediatamente el mensaje del usuario en la interfaz
    with st.chat_message("user"):
        st.markdown(pregunta)
    
    #Almacenamos el mensaje en la memoria de streamlit
    st.session_state.mensajes.append(HumanMessage(content = pregunta))


    # Generar respuesta del asistente
    respuesta = llm.invoke(st.session_state.mensajes)

    # mostrar respuesta del modelo
    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    #Agregar respuesta en el historial de mensajes
    st.session_state.mensajes.append(respuesta)