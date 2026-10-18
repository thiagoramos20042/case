# Sales Insights | API de vendas com IA

API que consulta vendas em SQLite e reúne endpoints analíticos e perguntas em linguagem natural.

**Inteligência Artificial** · API FastAPI

[← Data Science, IA e Automações · Thiago Oliveira](https://github.com/thiagoramos20042/thiagoramos20042) · [Catálogo de projetos](https://github.com/thiagoramos20042/thiagoramos20042/blob/main/PROJETOS.md)

## Objetivo

Disponibilizar consultas de vendas por HTTP e explorar respostas geradas a partir dos registros comerciais.

## O que você encontra

- GET /top-products para consultar os cinco produtos mais vendidos no mês anterior.
- GET /sales-insights para perguntas sobre os dados de vendas.
- GET /api-endpoints e documentação interativa da API.

## Tecnologias

Python · FastAPI · SQLAlchemy · SQLite · LangChain · FAISS · OpenAI

## Arquivos principais

| Arquivo | Conteúdo |
| --- | --- |
| [main.py](main.py) | Modelos, consultas, endpoints e integração com IA. |
| [requirements.txt](requirements.txt) | Dependências do serviço. |

## Como explorar

Na raiz do repositório:

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Com o serviço iniciado, abra http://127.0.0.1:8000/docs para consultar os endpoints.

## Contexto do projeto

A funcionalidade de IA usa a API da OpenAI e requer credencial própria. Em main.py, a leitura dos embeddings ainda usa o nome de variável sua_senha; ajuste essa configuração ao preparar seu ambiente. A base local é criada/populada pelo fluxo da aplicação.

---

Integra o [portfólio de Thiago Oliveira](https://github.com/thiagoramos20042).
