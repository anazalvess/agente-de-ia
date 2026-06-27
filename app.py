#importando as bibliotecas
from flask import Flask, jsonify, request
from flask_cors import CORS
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from dotenv import load_dotenv

#leitura da chave de api 
load_dotenv()
#criar o nosso app
app = Flask (__name__)
#habilitar o cors
CORS(app)

#criar o agente 
agente = Agent(
    model= OpenAIChat(id="gpt-4o-mini"),
    description="você é um agente virtual do hotel: The Grand Monarch Hotel, slogan: O endereço do luxo. Onde a exclusividade reside"
    "você responde de forma clara e bem humorada, informações sobre quartos, serviço, reservas e preços"
    "quato standard ($500), quarto Deluxe ($700), qauarto suíte presidencial ($1000)"
    "seviços oferecidos: academia, café da manhã, lavanderia, restaurante, piscina",
    markdown=True    
)

#criar a rota VAZIA e o método GET
@app.route("/", methods=['GET'])
def testar():
    return jsonify({"mensagem":"API funcionando"})



#criar a rota e o método POST
@app.route("/chat",methods=['POST'])
def pergunta():
    dados = request.get_json()
    pergunta = dados['pergunta']
    resposta = agente.run(pergunta)
    return jsonify({"resposta":resposta.content})

#rodar o nosso app
if __name__ == '__main__':   
    app.run(host="0.0.0.0",port=8000) 