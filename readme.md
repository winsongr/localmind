# ZeroBot: Local LLM Chatbot (1-Hour RAG Build)

A 100% offline RAG-based chatbot built in 1 hour using Ollama, Streamlit, LangChain, and ChromaDB. No cloud. No API keys. No BS.

## 🔄 Ollama Model Auto-Pull

ZeroBot uses a custom Ollama Docker image that auto-pulls the model (default: `gemma:2b`) at container start.

### How it works

- Entrypoint pulls model before Ollama server runs
- `OLLAMA_MODEL` env var defines the model
- Docker Compose builds Ollama from the custom image

### Run

```bash
docker compose build ollama
docker compose up -d
```

````

---

## 🚀 Features (Pareto-Optimized)

- 🧠 Local LLM (Mistral, LLaMA2) via Ollama
- 🕸 Web ingestion via Playwright + Unstructured
- 🧩 RAG pipeline using LangChain + ChromaDB
- 💻 Streamlit-based UI
- 🧱 Fully dockerized, one-liner setup

## 🏗️ System Architecture

```
User ⇄ Streamlit ⇄ Ollama ⇄ ChromaDB
                     ⇑
          Playwright + Unstructured
```

## ⚙️ Stack

- LLM: Ollama (`mistral`, `llama2`, `gemma`)
- RAG: LangChain + ChromaDB
- Crawler: Playwright + Unstructured
- UI: Streamlit
- Infra: Docker Compose

## ⚡ Quickstart

```bash
git clone https://github.com/yourusername/zerobot.git
cd zerobot
docker compose up --build
```

- First run pulls LLM model
- Visit: [http://localhost:8501](http://localhost:8501)

## 🌐 Crawling Docs

Edit `src/crawler/crawler.py` → update `URLS` list to your target sites. On startup, it auto-ingests into ChromaDB.

## 💬 Sample Usage

```txt
User: What is a Python list comprehension?
ZeroBot: [Uses local docs + LLM to answer]
```

## 📁 Folder Structure

```
zerobot/
├── docker-compose.yml
├── readme.md
├── src/
│   ├── app/
│   └── crawler/
└── data/ (persistent vector store)
```

## 👨‍💻 Dev Notes

- Change `OLLAMA_MODEL` to try other LLMs
- Extend Streamlit or crawler logic freely
- Pareto tip: tweak crawler before tuning model

## 📝 License

MIT. Open to hacks and PRs.
````
