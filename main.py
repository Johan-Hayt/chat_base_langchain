from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
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
    
    # ¡Nuevo! Personalidad configurable
    personalidad = st.selectbox(
        "Personalidad del Asistente",
        [
            "Útil y amigable",
            "Profesional y formal", 
            "Casual y relajado",
            "Experto técnico",
            "Creativo y divertido"
        ]
    )

    # Template dinámico basado en personalidad
    system_messages = {
        "Útil y amigable": "Eres un asistente útil y amigable llamado ChatBot Pro. Responde de manera clara y concisa.",
        "Profesional y formal": "Eres un asistente profesional y formal. Proporciona respuestas precisas y bien estructuradas.",
        "Casual y relajado": "Eres un asistente casual y relajado. Habla de forma natural y amigable, como un buen amigo.",
        "Experto técnico": "Eres un asistente experto técnico. Proporciona respuestas detalladas con precisión técnica.",
        "Creativo y divertido": "Eres un asistente creativo y divertido. Usa analogías, ejemplos creativos y mantén un tono alegre."
    }


    #recrear modelo
    chat_model = ChatOpenAI(model=model_name, temperature=temperature)


    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_messages[personalidad]),
        ("human", "Historial de conversación:\n{historial}\n\nPregunta actual: {query}")
    ])
    
    cadena = chat_prompt | chat_model


#Estructura de Prompt
# prompt_template = PromptTemplate(
#     input_variables=["query", "historial"],
#     template="""Eres un asistente útil y amigable llamado LaloBot. 
#     Historial de conversación:
#     {historial}

#     Responde de manera clara y concreta a la siguiente pregunta: {query}"""
# )

# # Implementación de ChatPromptTemplate
# prompt_template = ChatPromptTemplate.from_messages([
#    ("system","Eres un asistente útil y amigable llamado LaloBot." ),
#    ("human", "Historial de conversación:{historial}\nResponde de manera clara y concreta a la siguiente pregunta: {query}")
# ])


# # Configurar LCEL 
# cadena = prompt_template | chat_model


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

