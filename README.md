# 🧩 Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de ingestão e busca semântica com RAG (Retrieval-Augmented Generation), usando Python + LangChain + PostgreSQL com pgvector.

## 🎯 O que a aplicação faz

Esta aplicação permite conversar com o conteúdo de um PDF em 3 etapas:

1. 📥 Ingestão: lê o PDF e divide em chunks.
2. 🧠 Vetorização: gera embeddings e salva no PostgreSQL + pgvector.
3. 💬 Perguntas e respostas: recupera contexto por similaridade e usa LLM para responder.

O comportamento do prompt força respostas apenas com base no contexto recuperado. Quando não há base suficiente, a aplicação retorna a mensagem padrão de ausência de contexto.

## 🛠️ Tecnologias usadas

- **Embeddings e Chat:** Google Gemini ou OpenAI
- **Banco Vetorial:** PostgreSQL + pgvector
- **Framework:** LangChain + Python

## ⚙️ Funcionalidades Técnicas


Fluxo de execução:

```mermaid
flowchart LR
		A[PDF] --> B[PyPDFLoader]
		B --> C[RecursiveCharacterTextSplitter]
		C --> D[Embeddings]
		D --> E[(PostgreSQL + pgvector)]
		F[Pergunta do usuário] --> G[Similarity Search]
		E --> G
		G --> H[Prompt com contexto]
		H --> I[LLM]
		I --> J[Resposta]
```

### 📄 Pipeline de ingestão de documentos

- Carregamento de PDF com `PyPDFLoader`.
- Segmentação de conteúdo com `RecursiveCharacterTextSplitter`.
- Configuração atual de chunking:
	- `chunk_size=1000`
	- `chunk_overlap=150`
- Geração de embeddings por factory (`embedding_factory`) para desacoplar o provedor do restante do pipeline.
- Persistência no PostgreSQL com extensão `pgvector` via `PGVector`.
- Configuração do banco vetorial centralizada em `src/utils/vector_store.py` por meio da função `create_pgvector_store`, reutilizada na ingestão e na busca.

### 🔎 Recuperação semântica (retrieval)

- Busca por similaridade vetorial com `similarity_search_with_score`.
- Estratégia de recuperação `top-k` configurada com `k=10`.
- Montagem de contexto a partir dos chunks retornados, descartando textos vazios para melhorar a qualidade do prompt.

### 🧠 Geração de resposta com controle de contexto

- Uso de prompt com regras explícitas para responder somente com base no conteúdo recuperado.
- Tratamento de cenários sem resultado com mensagem padrão:
	- `Não tenho informações necessárias para responder sua pergunta.`
- Redução de alucinação por meio de instruções de não uso de conhecimento externo.

### 🔄 Suporte a múltiplos provedores de IA

- Seleção de provedor por variável de ambiente (`MODEL_PROVIDER`).
- Providers suportados:
	- `openai`
	- `gemini`
- Separação em duas factories:
	- `embedding_factory` para embeddings
	- `llm_factory` para modelo de chat

### 🛡️ Validação e resiliência operacional

- Validação centralizada das variáveis de ambiente obrigatórias (`require_env_vars`).
- Falha rápida quando variáveis obrigatórias não estão definidas.
- Tratamento de exceções nos scripts principais (`ingest.py`, `search.py`, `chat.py`) com mensagens de erro objetivas para facilitar troubleshooting.

### 💬 Experiência de uso no terminal

- Chat interativo com loop contínuo para múltiplas perguntas.
- Comandos de saída suportados: `sair`, `exit`, `quit`.
- Feedback de execução em tempo real (`processando`, sucesso, falha), útil para estudo e depuração.

## 🚀 Como executar a aplicação

### ✅ Pré-requisitos

- Python 3.12+
- Docker e Docker Compose
- Chave de API de um provedor:
	- OpenAI ou
	- Google Gemini

### ⚡ Quick Start (30 segundos)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker compose up -d
cp .env.example .env
```

Depois de copiar o arquivo, configure as variáveis do `.env` conforme seu provedor (OpenAI ou Gemini) e então execute:

```bash
python3 src/ingest.py
python3 src/chat.py
```

### 🧭 Passo a passo

#### 1. Clone o repositório e entre na pasta do projeto

```bash
git clone https://github.com/rafaelaqueirozg/mba-ia-desafio-ingestao-busca.git
cd mba-ia-desafio-ingestao-busca
```

#### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

#### 4. Copie o arquivo `.env.example` para `.env` e edite com os valores correspondentes

```bash
cp .env.example .env
```

Variáveis obrigatórias:

| Variável | Descrição | Exemplo |
|---|---|---|
| `DATABASE_URL` | String de conexão com PostgreSQL | `postgresql+psycopg://postgres:postgres@localhost:5432/rag` |
| `PG_VECTOR_COLLECTION_NAME` | Nome da coleção vetorial | `documentos_mba` |
| `PDF_PATH` | Caminho do PDF a ser ingerido | `./document.pdf` |
| `MODEL_PROVIDER` | Provedor do modelo | `openai` ou `gemini` |

Para OpenAI, também configure:

- `OPENAI_API_KEY`
- `OPENAI_CHAT_MODEL`
- `OPENAI_EMBEDDING_MODEL`

Para Gemini, também configure:

- `GOOGLE_API_KEY`
- `GOOGLE_CHAT_MODEL`
- `GOOGLE_EMBEDDING_MODEL`

Exemplo `.env` com OpenAI:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=documentos_mba
PDF_PATH=./document.pdf

MODEL_PROVIDER=openai
OPENAI_API_KEY=sua_chave_openai
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

Exemplo `.env` com Gemini:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=documentos_mba
PDF_PATH=./document.pdf

MODEL_PROVIDER=gemini
GOOGLE_API_KEY=sua_chave_google
GOOGLE_CHAT_MODEL=gemini-1.5-flash
GOOGLE_EMBEDDING_MODEL=models/embedding-001
```

#### 5. Suba o PostgreSQL com pgvector

```bash
docker compose up -d
```

#### 6. Execute a ingestão

```bash
python3 src/ingest.py
```

#### 7. Inicie o chat

```bash
python3 src/chat.py
```

Faça perguntas no terminal (digite `sair` para encerrar)

### ✅ Saída esperada

Exemplo de saída do `ingest.py`:

```text
[ingest] ▶️​ Iniciando ingestão do PDF
[ingest] ⏳​ Carregando o PDF: document.pdf
[ingest] ✅ PDF carregado com sucesso. Total de páginas: 34
[ingest] ✂️​ Dividindo o PDF em partes menores para processamento...
[ingest] ✅ PDF dividido em 67 partes.
[ingest] 🔍 Enriquecendo os documentos com metadados...
[ingest] ⏳​ Criando a coleção no PGVector e adicionando os documentos...
[ingest] ✅ Documentos adicionados à coleção documentos_mba com sucesso.
```

Exemplo de saída do `chat.py`:

```text
==================================================
Desafio RAG - Ingestão e Busca
==================================================
Digite 'sair' para encerrar
==================================================

[chat] ▶️ Iniciando o sistema

[chat] Digite sua pergunta (ou 'sair' para encerrar): Qual o faturamento da Empresa SuperTechIABrazil
[chat] ⏳ Processando...
[search] ▶️​ Iniciando processo de busca e resposta...
[search] 🔍 Realizando busca por similaridade no PGVector...
[search] ⏳​ Construindo o contexto para a resposta...
[search] ✅ Resposta gerada com sucesso.

==================================================
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil
==================================================
RESPOSTA:
R$ 10.000.000,00.
==================================================

[chat] Digite sua pergunta (ou 'sair' para encerrar): Você acha que o faturamento está bom?
[chat] ⏳ Processando...
[search] ▶️​ Iniciando processo de busca e resposta...
[search] 🔍 Realizando busca por similaridade no PGVector...
[search] ⏳​ Construindo o contexto para a resposta...
[search] ✅ Resposta gerada com sucesso.

==================================================
PERGUNTA: Você acha que o faturamento está bom?
==================================================
RESPOSTA:
Não tenho informações necessárias para responder sua pergunta.
==================================================

[chat] Digite sua pergunta (ou 'sair' para encerrar): sair
[chat] 👋 Encerrando o sistema. Até mais!
```

### 🔄 Troca de provedor

Se você trocar `MODEL_PROVIDER` (por exemplo, de `openai` para `gemini`), é recomendável limpar os dados vetoriais anteriores e executar a ingestão novamente, pois os vetores podem ter dimensões diferentes entre provedores.

### 🛑 Como parar a aplicação

Para parar os serviços do banco:

```bash
docker compose down
```

### 🧪 Exemplos de perguntas

Dentro do contexto do PDF:

- `Quais empresas têm maior faturamento?`
- `Qual empresa foi fundada em 1998?`

Fora do contexto do PDF:

- `Qual é a capital da França?`
- `Quantos clientes temos em 2024?`

### 🛠️ Solução de problemas

- Erro de conexão no banco:
	- verifique se `docker compose up -d` está ativo
	- confira a `DATABASE_URL`
- Erro de variável ausente:
	- revise os campos obrigatórios no `.env`
- Erro de arquivo PDF:
	- valide se o caminho em `PDF_PATH` existe

### ✅ Checklist de validação

- [ ] Banco PostgreSQL com pgvector em execução (`docker compose ps`)
- [ ] Arquivo `.env` criado e preenchido
- [ ] Ingestão executada sem erro (`python3 src/ingest.py`)
- [ ] Chat respondendo perguntas do contexto (`python3 src/chat.py`)
- [ ] Perguntas fora do contexto retornando a mensagem padrão

## 📁 Estrutura do projeto

```text
mba-ia-desafio-ingestao-busca/
├── .env                                # Variáveis de ambiente
├── .env.example                        # Exemplo de variáveis de ambiente
├── .gitignore                          # Configuração para o git ignorar arquivos
├── docker-compose.yml                  # Configuração do PostgreSQL
├── document.pdf                        # Documento a ser ingerido
├── README.md                           # Documentação do projeto
├── requirements.txt                    # Dependências do projeto
└── src/
		├── chat.py                     # Chat interativo para perguntas e respostas
		├── ingest.py                   # Processamento e ingestão do documento
		├── search.py                   # Sistema de busca semântica com RAG
		└── utils/
				├── embedding.py        # Factory de embedding 
				├── env.py              # Validação das variáveis de ambiente obrigatórias
				├── llm.py              # Factory de LLM
				└── vector_store.py     # Factory compartilhada do PGVector
```

## 📝 Licença

Projeto desenvolvido para o MBA de Engenharia de Software com IA da Full Cycle, para fins educacionais.

## 👩‍💻 Autora

[Rafaela Queiroz](https://github.com/rafaelaqueirozg)