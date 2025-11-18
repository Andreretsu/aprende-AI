import os
import sys

# --- DIAGNÓSTICO (Para garantir que estamos no lugar certo) ---
print(f"Usando Python de: {sys.executable}")

try:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_community.llms import Ollama
    # Importação que estava dando erro
    from langchain.chains import RetrievalQA 
except ImportError as e:
    print(f"\n❌ ERRO FATAL DE IMPORTAÇÃO: {e}")
    print("Verifique se você ativou o venv (.venv\\Scripts\\activate)")
    sys.exit(1)

# --- CONFIGURAÇÃO ---
# Certifique-se que o arquivo existe!
NOME_DO_ARQUIVO = "ApostilaPortugues.pdf" 
MODELO_OLLAMA = "llama3.2"

if not os.path.exists(NOME_DO_ARQUIVO):
    print(f"\n❌ ARQUIVO NÃO ENCONTRADO: {NOME_DO_ARQUIVO}")
    print("Coloque o PDF na mesma pasta deste script.")
    sys.exit(1)

print("\n1. 📄 Carregando o PDF...")
loader = PyPDFLoader(NOME_DO_ARQUIVO)
documentos = loader.load()
print(f"   - Carregado com sucesso: {len(documentos)} páginas.")

print("2. ✂️  Dividindo o texto...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
textos_divididos = text_splitter.split_documents(documentos)

print("3. 🧠 Criando memória (Embeddings)...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma.from_documents(documents=textos_divididos, embedding=embeddings)

print("4. 🤖 Iniciando Llama 3.2...")
llm = Ollama(model=MODELO_OLLAMA)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 3})
)

print("\n✅ TUTOR PRONTO! Pergunte algo sobre o texto.")
while True:
    pergunta = input("\nAluno: ")
    if pergunta.lower() in ['sair', 'exit']: break
    print("Tutor: ...")
    try:
        res = qa_chain.invoke(pergunta)
        print(f"Tutor: {res['result']}")
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")