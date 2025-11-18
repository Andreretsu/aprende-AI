# Aprende AI 🤖💬

![Badge do Hackathon](https://img.shields.io/badge/Hackathon-Unibarretos-blue)
![Linguagem](https://img.shields.io/badge/Python-3.10-yellow)
![Framework](https://img.shields.io/badge/Django-4.2-green)
![Impacto](https://img.shields.io/badge/Impacto_Social-Alfabetização_&_Cultura-brightgreen)

O **Aprende AI** é um projeto de IA focado em impacto social, desenvolvido para o Hackathon da Unibarretos. Nossa missão é usar a tecnologia para combater o analfabetismo e preservar patrimônios culturais imateriais.

## 🎯 O Problema

O analfabetismo funcional e digital ainda é uma barreira massiva para a inclusão social, especialmente para populações vulneráveis ou em áreas remotas sem acesso fácil a escolas. Paralelamente, centenas de línguas minoritárias e indígenas estão desaparecendo, levando consigo um patrimônio cultural inestimável.

## ✨ A Solução

O Aprende AI ataca esses dois problemas com uma plataforma web unificada que atua como:

1.  **Tutor de Alfabetização por Voz:** Um módulo focado em alfabetização de adultos e crianças. O usuário pode praticar a leitura de palavras e frases simples, e a nossa IA:

    - Usa **Speech-to-Text (STT)** para "ouvir" a pronúncia do usuário e validar seu aprendizado.
    - Usa **Text-to-Speech (TTS)** para ensinar a pronúncia correta, permitindo o aprendizado auditivo.

2.  **Preservador de Línguas Minoritárias:** A mesma tecnologia de IA é usada para criar um banco de dados cultural. Falantes nativos de línguas ameaçadas podem gravar áudios e textos, permitindo que a IA aprenda a estrutura da língua e ajude a criar:
    - Dicionários digitais.
    - Materiais didáticos interativos (usando o módulo de alfabetização).
    - Modelos básicos de tradução.

### 💸 Modelo de Sustentabilidade

O projeto é 100% gratuito e **open-source**. Buscamos sustentabilidade através de parcerias com fundações educacionais, departamentos de linguística e antropologia de universidades, e diretamente com as comunidades que desejam preservar sua língua.

---

## 🛠️ Tecnologias Utilizadas

Este projeto utiliza uma arquitetura full-stack moderna com o backend em Django servindo uma API REST.

- **Backend:** Python 3.10+, Django, Django REST Framework
- **Database:** SQLite 3 (padrão do Django, para agilidade no hackathon)
- **Frontend:** React / Vue.js / Svelte _(Time de frontend deve confirmar)_
- **Comunicação:** API REST (JSON)

### 🧠 Principais Bibliotecas de IA (Python)

- **Speech-to-Text (STT):** `SpeechRecognition`, `vosk` ou `whisper.ai`
- **Text-to-Speech (TTS):** `gTTS` (Google Text-to-Speech) ou `pyttsx3`
- **NLP (Processamento de Língua):** `spaCy` ou `NLTK` (para análises futuras)

---

## ⚙️ Configuração do Ambiente Local

Para executar este projeto, você precisará ter **Python 3.8+**, **Node.js 16+** (para o frontend) e **Git** instalados.

### 1. Clonar o Repositório

```bash
git clone [URL_DO_SEU_REPOSITÓRIO_GITHUB]
cd aprende-ai
```

2. Configurar o Backend (Python/Django)
   Abra um terminal na raiz do projeto (/aprende-ai).

Bash

# Criar o ambiente virtual

python -m venv venv

# Ativar o ambiente virtual

# No Windows:

.\venv\Scripts\activate

# No macOS/Linux:

source venv/bin/activate

# Com o (venv) ativo, instalar as dependências

pip install -r requirements.txt 3. Configurar o Frontend (JavaScript)
Abra outro terminal e navegue até a pasta do frontend (ex: /aprende-ai/frontend).

Bash

# Front-end: pasta templates

cd templates

# Instalar as dependências do Node.js

npm install
🚀 Como Executar o Projeto
Você precisará de dois terminais abertos simultaneamente.

1. Iniciar o Backend (Servidor Django)
   No primeiro terminal (com o venv ativo):

Bash

# 1. Aplicar as migrações do banco de dados

python manage.py migrate

# (Opcional) Criar um superusuário para o Admin

python manage.py createsuperuser

# 2. Iniciar o servidor de API

python manage.py runserver
🔥 O backend estará rodando em http://127.0.0.1:8000/

2. Iniciar o Frontend (Servidor React/Vue/Svelte)
   No segundo terminal (na pasta /frontend):

Bash

# Iniciar o servidor de desenvolvimento

npm start
🖥️ A aplicação estará acessível em http://localhost:3000/

👨‍💻 Equipe (Unibarretos)
[André Luiz Campos Silva] - (Função, ex: Desenvolvedor Front-end)
