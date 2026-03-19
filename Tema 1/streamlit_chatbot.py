from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate


import streamlit as st
from dotenv import load_dotenv
import os

# Lectura de APIKEY

load_dotenv(override=True)
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Falta la API KEY")

# Configuracion de la pagina de la app 

st.set_page_config(page_title="Chatbot Básico Juan Andres", page_icon="😀")
st.title("🤖JuanChatGPT con Langchain🤖")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit. Escribe tu mensaje abajo para comenzar!")


# Sidebar, slider y selectbox

with st.sidebar:
    st.header("Configuracion")
    temperature = st.slider("Temperatura",0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-3.5-turbo","gpt-4", "gpt-4o-mini"])
    
    #chat_model = ChatOpenAI(model = "gpt-4o-mini", temperature=0.5)
    chat_model = ChatOpenAI(model = model_name, temperature=temperature)

# Inicializar el historial de mensajes

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    


prompt_template = PromptTemplate(
    input_variables = ["mensaje","historial"],
    template = """Eres un asistente util y amigable llamado ChatBot Pro.
    
    
    Historial de conversacion:
    {historial}
    
    Responde de manera clara y concisa la siguiente pregunta: {mensaje}  
    """
)

#Crear cadena usando LCEL (LangChain Expression Language)
cadena = prompt_template | chat_model
    
    
# Mostrar mensajes previos en la interfaz
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        # No muestro el mensaje por pantalla
        continue
    
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    
    with st.chat_message(role):
        st.markdown(msg.content)
        
if st.button("🗑️ Nueva conversación"):
    st.session_state.mensajes = []
    st.rerun()
        
        
# Cuadro de entrada de texto de usuario
pregunta = st.chat_input("Escribe tu mensaje: ")

# if pregunta:
#     # Mostrar inmediatamente el mensaje del usuario en la interfaz
#     with st.chat_message("user"):
#         st.markdown(pregunta)
    
#     # Almacenamos el mensaje en la memoria de streamlit
#     st.session_state.mensajes.append(HumanMessage(content=pregunta))
    
#     #Generar respuesta usando el modelo de lenguaje
#     respuesta = chat_model.invoke(st.session_state.mensajes)

#     # Mostrar la respuesta en la interfaz

#     with st.chat_message("assistant"):
#         st.markdown(respuesta.content)
        
#     st.session_state.mensajes.append(respuesta)

if pregunta:
    # Mostrar y almacenar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)
    
    # Generar y mostrar respuesta del asistente
    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            # Streaming de la respuesta
            for chunk in cadena.stream({"mensaje": pregunta, "historial": st.session_state.mensajes}):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
        
        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_response))
        
    except Exception as e:
        st.error(f"Error al generar respuesta: {str(e)}")
        st.info("Verifica que tu API Key de OpenAI esté configurada correctamente.")
    
    
    