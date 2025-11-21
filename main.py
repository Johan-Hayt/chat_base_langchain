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

## inicializar llm
llm = ChatOpenAI(model="gpt-5-nano", temperature=0.7)

# Inicializar el historial de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


# iterar por los mensajes
for msg in st.session_state.mensajes:
    #validar si el mensaje es de tipo SytemMessage para no imprimirlo
    if isinstance(msg, SystemMessage):
        continue
    
    #escribir mensaje
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
         st.markdown(msg.content)


#cuadro de entrada de texto de usuario
pregunta = st.chat_input("Escribe un mensaje...")

if pregunta:
    #Mostrar inmediatamente el mensaje del usuario en la interfaz
    with st.chat_message("user"):
        st.markdown(pregunta)
    
    st.session_state.mensajes.append()