#!/bin/sh
set -e

MODEL="${OLLAMA_MODEL:-gemma:2b}"

# Start Ollama server in the background
ollama serve &
OLLAMA_PID=$!

# Wait for the server to be ready
echo "Waiting for Ollama server to be ready..."
until curl -s http://localhost:11434 > /dev/null; do
  sleep 1
done

echo "Pulling Ollama model: $MODEL"
if ! ollama pull "$MODEL"; then
  echo "ERROR: Failed to pull model '$MODEL'."
  echo "Available models:"
  ollama list || true
  kill $OLLAMA_PID
  exit 1
fi

echo "Model pulled. Bringing Ollama server to foreground..."
wait $OLLAMA_PID