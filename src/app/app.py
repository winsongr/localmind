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


def fetch_html(url: str) -> str:
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            html = page.content()
            browser.close()
            return html
    except Exception as e:
        print(f"Error fetching HTML from {url}: {e}")
        return ""


def extract_text_from_html(html: str) -> str:
    try:
        from unstructured.partition.html import partition_html

        elements = partition_html(text=html)
        text = "\n".join([el.text for el in elements if hasattr(el, "text")])
        return text
    except Exception as e:
        print(f"Error extracting text from HTML: {e}")
        return ""


def ingest_to_chroma(text: str, url: str, vectordb):
    try:
        from langchain.schema import Document

        doc = Document(page_content=text, metadata={"source": url})
        vectordb.add_documents([doc])
        vectordb.persist()
        print(f"Successfully ingested {url} into ChromaDB")
        return True
    except Exception as e:
        print(f"Error ingesting to ChromaDB: {e}")
        return False


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

    # --- Crawl UI ---
    st.subheader("Crawl a Web Page")
    crawl_url = st.text_input("Paste a URL to crawl and ingest:")
    if st.button("Crawl and Ingest") and crawl_url:
        with st.spinner(f"Crawling {crawl_url}..."):
            html = fetch_html(crawl_url)
            if not html:
                st.error("Failed to fetch HTML from the URL.")
            else:
                text = extract_text_from_html(html)
                if not text:
                    st.error("Failed to extract text from the HTML.")
                else:
                    success = ingest_to_chroma(text, crawl_url, vectordb)
                    if success:
                        st.success(
                            f"Successfully ingested {crawl_url} into the database."
                        )
                    else:
                        st.error(
                            "Failed to ingest the content into the database."
                        )
    # --- End Crawl UI ---

    user_input = st.text_input("Ask a question:")
    if st.button("Send") and user_input:
        with st.spinner("Thinking..."):
            try:
                # Retrieve context
                docs = vectordb.similarity_search(user_input, k=3)
                context = "\n".join([doc.page_content for doc in docs])
                prompt = (
                    f"Context:\n{context}\n\nQuestion: {user_input}\nAnswer:"
                )
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
