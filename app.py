#importando as bibliotecas
from flask import Flask, jsonify, request
from flask_cors import CORS
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from dotenv import load_dotenv
from supabase import create_client
import os

#leitura da chave de api 
load_dotenv()
#usando o getenv para pegar o arquivo específico
supabase_url = os.getenv("SUPABASE_URL")
#usando o getenv para pegar o arquivo específico
supabase_key = os.getenv("SUPABASE_KEY")
#criando a conexão com o banco de dados, passando a URL e a KEY.
supabase = create_client(supabase_url,supabase_key)

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

#criar a rota para reservas 
@app.route("/reservas", methods=['POST'])
def reserva():
    dados = request.get_json()
    nova_reserva = {
        "nome":dados["nome"],
        "email":dados["email"],
        "check_in":dados["check_in"],
        "tipo_quarto":dados["tipo_quarto"]
    }
    supabase.table("reservas").insert(nova_reserva).execute()
    return jsonify({"mensagem":"reserva realizada com sucesso!"})
#rodar o nosso app
if __name__ == '__main__':   
    app.run(host="0.0.0.0",port=8000) 