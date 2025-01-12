# ChatGPT Local AI Devops Assistent with Ollama and Chainlit

## Requirements

- python 3.10 or newer
- uv newer
- ollama
- npx --lts

## Installation

- Install python 3.10 or newer (https://www.python.org/downloads/)
- Install uv (https://docs.astral.sh/uv/)
- Install ollama (https://ollama.com)
- Install nvm/node --lts (https://github.com/nvm-sh/nvm)

## Usage

- Download ollama model :
```bash
ollama pull llama3.2
```

- Download uv/python package :
```bash
uv python install 3.10
uv python pin 3.10
uv venv
source .venv/bin/activate
uv sync
```

- Enter values in .env file :
```bash
cp .env.example .env

# Open .env file and enter values
# Generate Secret Key Chainlit

chainlit create-secret

# Enter the secret key in .env file

# Example .env file
CHAINLIT_AUTH_SECRET="secret_key"
USERNAME="user"
PASSWORD="password"
DATBASE_URL=""
```

- Run Postgres database :
```bash
docker compose up -d postgres
```

- Migrate the database :
```bash
npx prisma migrate deploy
```

- Run the chatbot :
```bash
chainlit run main.py
```
