import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv(override=True)
api_key = os.getenv('GOOGLE_API_KEY')

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

pregunta = "¿En que año llego el ser humano a la luna por primera vez?"
print("Pregunta: ", pregunta)

respuesta = llm.invoke(pregunta)
print("Respuesta del modelo ", respuesta.content)
