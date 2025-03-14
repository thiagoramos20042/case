import os
from fastapi import FastAPI, Depends, Query
from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
import uvicorn

# 🔹 Importações do LangChain e ambiente
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv, find_dotenv

# Carrega variáveis de ambiente
_ = load_dotenv(find_dotenv())
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "sua_senha"
# 🔹 Configuração do Banco de Dados SQLite
DATABASE_URL = "sqlite:///./sales.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 🔹 Modelos SQLAlchemy
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    price = Column(Numeric(10, 2))

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    sale_date = Column(TIMESTAMP, nullable=False)

    product = relationship("Product")
    customer = relationship("Customer")

# Criar as tabelas se ainda não existirem
Base.metadata.create_all(bind=engine)

# 🔹 Dependência para gerenciar sessões do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 Populando o banco de dados (caso não haja dados)
def populate_db():
    db = SessionLocal()
    if db.query(Sale).first() is None:
        print("📌 Populando banco de dados com produtos, clientes e vendas...")
        # Inserindo produtos
        products_data = [
            ("SKU001", "Product A", "Category 1", 10.99),
            ("SKU002", "Product B", "Category 1", 20.50),
            ("SKU003", "Product C", "Category 2", 15.75),
            ("SKU004", "Product D", "Category 3", 30.00),
            ("SKU005", "Product E", "Category 4", 25.00)
        ]
        db.add_all([Product(sku=p[0], name=p[1], category=p[2], price=p[3]) for p in products_data])

        # Inserindo clientes
        customers_data = [
            ("John Doe", "john@example.com"),
            ("Jane Smith", "jane@example.com"),
            ("Bob Johnson", "bob@example.com"),
            ("Alice Brown", "alice@example.com"),
            ("Charlie Davis", "charlie@example.com")
        ]
        db.add_all([Customer(name=c[0], email=c[1]) for c in customers_data])

        # Inserindo vendas
        sales_data = [
            (4, 1, 4, 120.00, '2025-01-17 12:22:49'),
            (5, 1, 7, 175.00, '2025-01-28 04:04:17'),
            (5, 4, 4, 100.00, '2025-02-04 11:58:16'),
            (1, 2, 2, 21.98, '2025-01-05 10:30:45'),
            (2, 3, 1, 20.50, '2025-01-06 15:15:10'),
            (3, 5, 3, 47.25, '2025-01-08 09:45:22'),
            (4, 2, 1, 30.00, '2025-01-10 17:22:30'),
            (5, 4, 5, 125.00, '2025-01-12 11:00:00'),
            (1, 3, 2, 21.98, '2025-01-14 18:25:45'),
            (2, 5, 6, 123.00, '2025-01-15 13:12:22'),
            (3, 1, 2, 31.50, '2025-01-18 08:10:33'),
            (4, 4, 1, 30.00, '2025-01-20 14:05:20'),
            (5, 2, 3, 75.00, '2025-01-23 19:30:40'),
            (1, 5, 2, 21.98, '2025-01-25 10:45:10'),
            (2, 4, 4, 82.00, '2025-01-29 16:20:50'),
            (3, 2, 1, 15.75, '2025-02-01 12:00:00'),
            (4, 5, 2, 60.00, '2025-02-03 18:40:30'),
            (5, 1, 8, 200.00, '2025-02-05 11:25:00'),
            (1, 4, 3, 32.97, '2025-02-07 14:50:10'),
            (2, 3, 2, 41.00, '2025-02-08 10:20:15'),
            (3, 5, 4, 63.00, '2025-02-10 16:45:55'),
            (4, 2, 1, 30.00, '2025-02-12 20:30:00'),
            (5, 3, 2, 50.00, '2025-02-15 09:10:10'),
            (1, 1, 6, 65.94, '2025-02-16 13:35:30'),
            (2, 4, 2, 41.00, '2025-02-18 15:00:00'),
            (3, 2, 3, 47.25, '2025-02-19 11:30:45'),
            (4, 5, 2, 60.00, '2025-02-21 14:10:22'),
            (5, 4, 1, 25.00, '2025-02-22 19:45:55'),
            (1, 2, 7, 76.93, '2025-02-24 12:10:10'),
            (2, 1, 4, 82.00, '2025-02-25 17:30:50'),
            (3, 3, 5, 78.75, '2025-02-27 09:55:00'),
            (4, 5, 3, 90.00, '2025-02-28 14:25:30'),
            (5, 2, 9, 225.00, '2025-03-02 10:00:00')
        ]
        sales_objects = [
            Sale(
                product_id=s[0],
                customer_id=s[1],
                quantity=s[2],
                total_amount=s[3],
                sale_date=datetime.strptime(s[4], "%Y-%m-%d %H:%M:%S")
            )
            for s in sales_data
        ]
        db.add_all(sales_objects)
        db.commit()
        print("✅ Banco de dados populado com sucesso!")
    db.close()

# 🔹 Função para extrair os dados de vendas e gerar "documentos" de texto
def get_sales_documents(db: Session):
    sales = db.query(Sale).all()
    docs = []
    for sale in sales:
        doc_text = (
            f"Sale ID: {sale.id}. "
            f"Produto: {sale.product.name} (SKU: {sale.product.sku}, Categoria: {sale.product.category}). "
            f"Cliente: {sale.customer.name} (Email: {sale.customer.email}). "
            f"Quantidade: {sale.quantity}. "
            f"Total: {sale.total_amount}. "
            f"Data da venda: {sale.sale_date}."
        )
        docs.append(doc_text)
    return docs

# 🔹 Configuração do LangChain
rag_template = """
Você é um analista de dados experiente e especializado em vendas.
Seu trabalho é responder perguntas utilizando única e exclusivamente os dados presentes no banco de dados.
A seguir, você tem registros de vendas individuais, sem qualquer processamento prévio:
{context}

Analise os registros acima e responda com base neles.
Pergunta: {question}
"""



prompt_template = ChatPromptTemplate.from_template(rag_template)
llm = ChatOpenAI()

# 🔹 Inicializa FastAPI
app = FastAPI(title="Sales Insights API", version="1.0")

# Endpoint 1: Produtos mais vendidos no mês anterior
@app.get("/top-products", summary="Retorna os 5 produtos mais vendidos no mês anterior")
def top_products(db: Session = Depends(get_db)):
    today = datetime.today()
    first_day_last_month = today.replace(day=1) - timedelta(days=1)
    last_day_last_month = first_day_last_month.replace(day=1)

    top_products = (
        db.query(Product.name, func.sum(Sale.quantity).label("total_sold"))
        .join(Sale, Product.id == Sale.product_id)
        .filter(Sale.sale_date >= last_day_last_month, Sale.sale_date < first_day_last_month)
        .group_by(Product.name)
        .order_by(func.sum(Sale.quantity).desc())
        .limit(5)
        .all()
    )
    return [{"product": prod[0], "total_sold": prod[1]} for prod in top_products]

# Endpoint 2: Processamento da pergunta via LangChain com dados da tabela sales
@app.get("/sales-insights", summary="Processa a pergunta utilizando LangChain e retorna resposta baseada nos dados da tabela sales")
def get_sales_insights(question: str = Query(..., description="Pergunta sobre as vendas"), db: Session = Depends(get_db)):
    # Extrai os dados de vendas e cria os documentos
    docs = get_sales_documents(db)
    # Cria embeddings e constrói a base vetorial (FAISS) a partir dos textos
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("sua_senha"))
    vectorstore = FAISS.from_texts(docs, embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    # Recupera os documentos mais relevantes para a pergunta
    retrieved_docs = retriever.get_relevant_documents(question)
    context = "\n".join(doc.page_content for doc in retrieved_docs)  # Se os itens já forem strings; caso contrário, use .page_content
    # Formata o prompt com o contexto e a pergunta do cliente
    prompt = prompt_template.format(context=context, question=question)
    # Obtém a resposta do LLM
    response = llm(prompt)
    return {"response": response.content}

# Endpoint 3: Lista dos endpoints disponíveis
@app.get("/api-endpoints", summary="Lista todos os endpoints disponíveis")
def list_endpoints():
    base_url = "http://127.0.0.1:8000"
    return JSONResponse(content={"endpoints": [
        {"name": "Top Products", "url": f"{base_url}/top-products"},
        {"name": "Sales Insights", "url": f"{base_url}/sales-insights?question=Qual foi o produto mais vendido?"},
        {"name": "API Endpoints", "url": f"{base_url}/api-endpoints"}
    ]})

# Popula o banco de dados ao iniciar a aplicação
@app.on_event("startup")
def startup_event():
    populate_db()

if __name__ == "__main__":
    print("\n🚀 API rodando!\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)