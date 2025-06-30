# README.md

## Visão Geral do Projeto

Este projeto consiste em um site com frontend em React que consome dados por meio de um backend em Python utilizando FastAPI. A aplicação expõe os dados como um endpoint REST, para que o frontend possa exibi-las.

A seguir, estão as instruções para que seus amigos (colaboradores) configurem corretamente o projeto após efetuarem o clone do repositório.

---

## 1. Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:

1. **Git** (para clonar o repositório)
2. **Python 3.9+** (recomendado) e **pip**
3. **Node.js 16+** e **npm** (ou **yarn**) para o frontend React

Opcionalmente, recomenda-se o uso de um ambiente virtual Python (virtualenv ou `venv`) para isolar dependências.

---

## 2. Configuração do Backend (FastAPI)

### 2.1. Clonar o Repositório

```bash
# No terminal, navegue até o diretório desejado e execute:
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO/backend
```

> **Observação:** Ajuste a URL conforme o repositório real.

### 2.2. Criar o Ambiente Virtual Python

```bash
# No diretório `backend/`, execute:
python3 -m venv venv         # Cria o virtualenv
source venv/bin/activate     # Linux/macOS
# ou
venv\Scripts\activate      # Windows

# Após ativar, você deve ver algo como: (venv) usuario@máquina backend$
```

### 2.3. Instalar Dependências Python

Com o ambiente virtual ativado:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém as versões das bibliotecas necessárias:

### 2.4. Executar o Servidor FastAPI

1. Ative o virtualenv (caso não esteja ativo).
2. Execute o servidor:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

* O `--reload` garante recarregamento automático quando arquivos Python forem alterados.
* Se tudo estiver configurado corretamente, ao acessar [http://localhost:8000/docs](http://localhost:8000/docs) você verá a interface do Swagger com o endpoint `/responses`.

#### 2.4.1. Testar Manualmente

Para verificar, abra o navegador ou use o `curl`:

```bash
curl http://localhost:8000/responses
```

Você deverá visualizar um array JSON com as respostas do formulário, por exemplo:

```json
[
  {
    "Timestamp": "2025-06-01T12:34:56",
    "Nome": "Ana Silva",
    "Email": "ana.silva@example.com"
  },
  {
    "Timestamp": "2025-06-02T08:20:15",
    "Nome": "Bruno Souza",
    "Email": "bruno.souza@example.com"
  }
]
```

---

## 4. Estrutura de Pastas do Projeto

```text
InunData/
│
├── FastAPI/               # Backend FastAPI
│   ├── app/
│   │   ├── main.py        # Ponto de entrada FastAPI
│   ├── requirements.txt
│
└── React/                 # Frontend React
    ├── public/
    ├── src/
    │   ├── App.jsx
    │   ├── index.jsx
    │   └── components/    # Componentes React      
    ├── package.json
    └── ...
```

---
