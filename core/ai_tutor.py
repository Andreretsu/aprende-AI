import os
import ollama  # Vamos usar o Ollama direto, sem passar pelo LangChain
from django.conf import settings

# Importações dos pacotes "satélites" que costumam dar menos erro
try:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_chroma import Chroma
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("Verifique se instalou: langchain-community langchain-chroma langchain-huggingface")

# Variável global para guardar o Banco de Dados (não a Chain)
_db = None

def carregar_banco_vetorial():
    """
    Carrega o PDF e cria o índice de busca (Vector Store).
    """
    global _db
    
    if _db is not None:
        return _db

    print("🔄 [IA] Carregando banco de dados vetorial...")
    
    pdf_path = os.path.join(settings.BASE_DIR, 'ApostilaPortugues.pdf')
    persist_directory = os.path.join(settings.BASE_DIR, 'db_chroma')
    
    # Configuração de Embeddings (o tradutor texto -> números)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Se o banco já existe no disco, carrega ele (muito mais rápido)
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        print("   - Carregando do disco...")
        _db = Chroma(
            persist_directory=persist_directory, 
            embedding_function=embeddings
        )
    else:
        # Se não existe, cria do zero
        if not os.path.exists(pdf_path):
            print(f"❌ [IA] Erro: Arquivo {pdf_path} não encontrado.")
            return None

        print("   - Processando PDF (pode demorar um pouco)...")
        loader = PyPDFLoader(pdf_path)
        documentos = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        textos_divididos = text_splitter.split_documents(documentos)
        
        _db = Chroma.from_documents(
            documents=textos_divididos, 
            embedding=embeddings,
            persist_directory=persist_directory
        )
    
    print("✅ [IA] Banco de dados pronto!")
    return _db

def perguntar_ao_tutor(pergunta):
    db = carregar_banco_vetorial()
    if not db:
        return "Erro: Material de estudo não encontrado."
    
    try:
        # 1. Busca: Encontra os 3 parágrafos mais parecidos com a pergunta no PDF
        docs = db.similarity_search(pergunta, k=3)
        
        # Junta o conteúdo desses parágrafos em um texto só
        contexto = "\n\n".join([doc.page_content for doc in docs])
        
        # 2. Prompt: Monta a mensagem para o Ollama
        prompt_sistema = """Você é um tutor paciente e didático de alfabetização. 
Use APENAS o contexto abaixo para responder à pergunta do aluno. 
Se a resposta não estiver no contexto, diga que não sabe."""
        
        prompt_usuario = f"""
Contexto retirado da apostila:
{contexto}

Pergunta do aluno: 
{pergunta}
"""

        # 3. Geração: Chama o Ollama direto (sem LangChain no meio)
        print("🤖 Enviando para o Llama 3.2...")
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'system', 'content': prompt_sistema},
            {'role': 'user', 'content': prompt_usuario},
        ])
        
        return response['message']['content']

    except Exception as e:
        print(f"Erro na geração: {e}")
        return "Desculpe, tive um problema técnico para responder."