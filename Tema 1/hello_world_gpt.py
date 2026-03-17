import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

pregunta = "¿En que año llego el ser humano a la luna por primera vez?"
print("Pregunta: ", pregunta)

respuesta = llm.invoke(pregunta)
print("Respuesta del modelo ", respuesta.content)
