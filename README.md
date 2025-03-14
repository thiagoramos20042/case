Sales Insights API

📌 Visão Geral

A Sales Insights API é uma API desenvolvida com FastAPI e SQLAlchemy para fornecer insights sobre vendas a partir de um banco de dados SQLite. Além disso, a API integra o LangChain para responder perguntas sobre vendas de maneira inteligente e baseada em dados.

🚀 Funcionalidades

📊 Obter os 5 produtos mais vendidos no mês anterior

🔍 Analisar vendas com processamento via LangChain

🔗 Listar os endpoints disponíveis

🛠 Tecnologias Utilizadas

Python

FastAPI

SQLAlchemy

SQLite

LangChain

FAISS

OpenAI API

Uvicorn

dotenv

📂 Estrutura do Projeto
📁 sales_insights_api/

│── main.py               # Arquivo principal com a API

│── requirements.txt      # Dependências do projeto

│── .env                  # Variáveis de ambiente (chave OpenAI)

│── sales.db              # Banco de dados SQLite

⚡ Como Executar o Projeto

1️⃣ Pré-requisitos

Ter o Python 3.8+ instalado

Criar e ativar um ambiente virtual:
python -m venv venv
source venv/bin/activate

Instalar as dependências:
pip install -r requirements.txt

Criar um arquivo .env e adicionar a chave da OpenAI:
OPENAI_API_KEY= "sua-chave-aqui"

🌍 Endpoints Disponíveis

🔹 Obter os top 5 produtos mais vendidos
GET /top-products

🔹 Obter insights sobre vendas
GET /sales-insights?question=Sua Pergunta Aqui

🔹 Listar endpoints disponíveis
GET /api-endpoints

🔹 Para testar as APi´s (só acesse depois de rodar o código) 
http://127.0.0.1:8000/docs#/

🛠 Contribuição

Faça um fork do repositório

Crie uma branch (git checkout -b feature-nova)

Commit suas alterações (git commit -m 'Adiciona nova feature')

Envie suas alterações (git push origin feature-nova)

Abra um Pull Request




