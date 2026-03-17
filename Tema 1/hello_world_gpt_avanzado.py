import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


load_dotenv(override=True)
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Falta la API KEY")

chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# plantilla = PrompTemplate(
#     input_variables = ["nombre"],
#     template = f"Saluda al usuario con su nombre. \nNombre del usuario: {nombre}\nAsistente:"
# )

plantilla = PromptTemplate.from_template(
    "Saluda al usuario con su nombre.\nNombre del usuario: {nombre}\nAsistente:"
)

#chain = LLMChain(llm = chat, prompt = plantilla)
chain = plantilla | chat
#resultado = chain.run(nombre="Juan Andres")
resultado = chain.invoke({"nombre": "Juan Andres"})
print(resultado.content)

