from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
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

if st.button("🗑️ Nueva conversación"):
    st.session_state.mensajes = []
    st.rerun()  # Refresca para mostrar vacío

#sidebar de configuración de parámetros del chat
with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-5-nano", "gpt-5-mini", "gpt-4o-mini"])

    #recrear modelo
    chat_model = ChatOpenAI(model=model_name, temperature=temperature)


#Estructura de Prompt
prompt_template = PromptTemplate(
    input_variables=["query", "historial"],
    template="""Eres un asistente útil y amigable llamado LaloBot. 
    Historial de conversación:
    {historial}

    Responde de manera clara y concreta a la siguiente pregunta: {query}"""
)


# Configurar LCEL 
cadena = prompt_template | chat_model


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
  with st.chat_message("user"):
    st.markdown(pregunta)
  
  try:
    with st.chat_message("assistant"):
      response_placeholder = st.empty()
      full_response = ""

      # Ejecución por stream de la respuesta del modelo!
      for chunk in cadena.stream({"query": pregunta, "historial": st.session_state.mensajes}):
        full_response += chunk.content
        response_placeholder.markdown(full_response + "▌") # El cursor parpadeante
      
      response_placeholder.markdown(full_response)
    
    # Almacenando los mensajes en el historial
    st.session_state.mensajes.append(HumanMessage(content=pregunta))
    st.session_state.mensajes.append(AIMessage(content=full_response))
    
  except Exception as e:
    st.error(f"Error al generar respuesta: {str(e)}")
    st.info("Verifica que tu API Key de OpenAI esté configurada correctamente.")

