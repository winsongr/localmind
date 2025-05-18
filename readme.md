# ZeroBot

A fully local, zero-cost LLM chatbot built with Docker. This is a hobby project I use to explore LLMs, RAG, and full-stack AI deployment. It’s also part of my public portfolio.

## 🔥 Highlights

- 100% local: No APIs, no internet calls after setup
- Runs via Docker Compose
- Crawls websites for context (RAG)
- Supports chatting with custom data
- Uses Ollama + Mistral for LLM
- Vector store: ChromaDB
- Web UI: Streamlit

## 📦 Tech Stack

- LLM: Ollama (`mistral`, `llama2`, etc.)
- RAG: LangChain + ChromaDB
- Web crawler: `unstructured` + `playwright`
- Frontend: Streamlit (chat interface)
- Containerized with Docker Compose

## 🛠️ Setup

```bash
git clone https://github.com/yourusername/zerobot.git
cd zerobot
docker compose up --build
```
