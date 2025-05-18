import os
import streamlit as st
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM

CHROMA_PATH = os.path.expanduser("~/localmind_chroma_db")
# or
CHROMA_PATH = os.path.join(os.getcwd(), "data", "chroma_db")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL = "gemma:2b"


@st.cache_resource
def get_vectordb():
    embeddings = OllamaEmbeddings(model=MODEL, base_url=OLLAMA_HOST)
    return Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)


@st.cache_resource
def get_llm():
    return OllamaLLM(model=MODEL, base_url=OLLAMA_HOST)


def main():
    st.title("ZeroBot: Local LLM Chatbot")
    if "history" not in st.session_state:
        st.session_state.history = []

    try:
        vectordb = get_vectordb()
        llm = get_llm()
    except Exception as e:
        st.error(f"Failed to initialize models: {e}")
        return

    user_input = st.text_input("Ask a question:")
    if st.button("Send") and user_input:
        try:
            # Retrieve context
            docs = vectordb.similarity_search(user_input, k=3)
            context = "\n".join([doc.page_content for doc in docs])
            prompt = f"Context:\n{context}\n\nQuestion: {user_input}\nAnswer:"
            response = llm.invoke(prompt)
        except Exception as e:
            response = f"[Error: {str(e)}]"
            st.error("Failed to process query. Please try again.")
        st.session_state.history.append((user_input, response))

    for q, a in st.session_state.history[::-1]:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**ZeroBot:** {a}")


if __name__ == "__main__":
    main()
