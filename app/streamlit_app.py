"""
RAG Research Assistant - STREAMLIT FRONTEND ONLY.

This file contains the whole UI. The "brain" (reading files, chunking,
embeddings, retrieval, LLM call) is NOT here. Instead there are four
open placeholder functions in the INTEGRATION POINTS section below.
Each one says exactly what it receives and what it must return.
Replace the body of each function with a call to your own code in src/.

The app already runs with the placeholders (it returns demo data),
so you can test the interface before wiring anything in.
"""

import streamlit as st

st.set_page_config(page_title="RAG Research Assistant", page_icon="📚", layout="wide")


# ======================================================================
# INTEGRATION POINTS  -  replace the body of these 4 functions
# ======================================================================

def ingest_documents(files, chunk_size, chunk_overlap):
    """
    STEP 1 - INGESTION + EMBEDDING + STORING  (src/ingestion, src/embeddings)

    RECEIVES
      files          : list of Streamlit UploadedFile objects (.pdf/.txt/.md)
                       - use f.name for the file name
                       - use f.read() / f.getvalue() for the raw bytes
                       - PdfReader(f) works directly on a PDF one
      chunk_size     : int, characters (or tokens) per chunk, from the sidebar
      chunk_overlap  : int, overlap between chunks, from the sidebar

    YOUR CODE SHOULD
      1. read text from each file (keep file name + page number)
      2. split the text into chunks
      3. embed every chunk
      4. save chunks + embeddings somewhere retrieve_chunks() can reach
         (a vector store like FAISS/Chroma, a file in data/processed/,
         or st.session_state)

    MUST RETURN
      dict: {"num_chunks": int, "num_files": int}
    """
    # TODO: replace with your code, e.g.
    # from src.ingestion.loader import load_and_chunk
    # from src.embeddings.embedder import embed_and_store
    # chunks = load_and_chunk(files, chunk_size, chunk_overlap)
    # embed_and_store(chunks)
    # return {"num_chunks": len(chunks), "num_files": len(files)}
    return {"num_chunks": 0, "num_files": len(files)}  # demo value


def retrieve_chunks(question, top_k):
    """
    STEP 2 - RETRIEVAL  (src/retrieval)

    RECEIVES
      question : str, the user's question
      top_k    : int, how many chunks to return, from the sidebar

    YOUR CODE SHOULD
      embed the question, search the stored embeddings, return the best chunks

    MUST RETURN
      list of dicts, best match first, each with these keys:
        {"text": str, "source": str (file name), "page": int, "score": float}
    """
    # TODO: replace with your code, e.g.
    # from src.retrieval.search import search
    # return search(question, top_k)
    return [  # demo value
        {"text": "Demo chunk - connect retrieve_chunks() to see real text.",
         "source": "demo.pdf", "page": 1, "score": 0.0}
    ]


def generate_answer(question, chunks, chat_history, model_name):
    """
    STEP 3 - GENERATION  (src/generation)

    RECEIVES
      question     : str, the user's question
      chunks       : the list returned by retrieve_chunks()
      chat_history : list of {"role": "user"|"assistant", "content": str}
                     (previous turns, in case you want follow-up questions)
      model_name   : str, the model chosen in the sidebar

    YOUR CODE SHOULD
      build a prompt with the chunks as context, call the LLM,
      return the answer text

    MUST RETURN
      str - the answer (markdown is fine)
    """
    # TODO: replace with your code, e.g.
    # from src.generation.llm import answer
    # return answer(question, chunks, chat_history, model_name)
    return "This is a demo answer. Connect generate_answer() to your LLM code."  # demo


def clear_index():
    """
    OPTIONAL - RESET  (called by the "Clear documents" button)

    YOUR CODE SHOULD
      delete / reset the stored chunks and embeddings

    RETURNS
      nothing
    """
    # TODO: replace with your code, e.g. vector_store.reset()
    pass


# Models that appear in the sidebar dropdown. Edit this list to match what
# your generation code supports.
AVAILABLE_MODELS = ["claude-sonnet-5-5", "claude-haiku-5-5"]


# ======================================================================
# UI  -  you normally don't need to edit below this line
# ======================================================================

# Session state keeps data between Streamlit reruns
if "messages" not in st.session_state:
    st.session_state.messages = []      # chat history
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = [] # names of processed files
if "num_chunks" not in st.session_state:
    st.session_state.num_chunks = 0

# ---------------- Sidebar: documents + settings ----------------
with st.sidebar:
    st.header("📄 1. Documents")
    uploaded = st.file_uploader(
        "Upload papers", type=["pdf", "txt", "md"], accept_multiple_files=True
    )

    st.header("⚙️ 2. Settings")
    chunk_size = st.slider("Chunk size", 200, 2000, 800, step=100)
    chunk_overlap = st.slider("Chunk overlap", 0, 500, 150, step=50)
    top_k = st.slider("Chunks to retrieve (top-k)", 1, 10, 4)
    model_name = st.selectbox("LLM model", AVAILABLE_MODELS)
    show_sources = st.toggle("Show sources under answers", value=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Process", type="primary", use_container_width=True):
            if not uploaded:
                st.warning("Upload at least one file first.")
            else:
                with st.spinner("Processing documents..."):
                    result = ingest_documents(uploaded, chunk_size, chunk_overlap)
                st.session_state.indexed_files = [f.name for f in uploaded]
                st.session_state.num_chunks = result.get("num_chunks", 0)
                st.success("Documents processed")
    with col2:
        if st.button("Clear docs", use_container_width=True):
            clear_index()
            st.session_state.indexed_files = []
            st.session_state.num_chunks = 0
            st.session_state.messages = []
            st.rerun()

    # Status panel
    st.divider()
    st.caption("Status")
    st.write(f"Files indexed: **{len(st.session_state.indexed_files)}**")
    st.write(f"Chunks: **{st.session_state.num_chunks}**")
    for name in st.session_state.indexed_files:
        st.caption(f"• {name}")

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------------- Main area: chat ----------------
st.title("📚 RAG Research Assistant")
st.caption("Upload papers in the sidebar, click Process, then ask questions.")

# Replay earlier messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if show_sources and msg.get("sources"):
            with st.expander("Sources used"):
                for c in msg["sources"]:
                    st.caption(f"{c['source']} - page {c['page']} - score {c['score']:.2f}")
                    st.write(c["text"][:400])

# New question
question = st.chat_input("Ask a question about your documents")

if question:
    # show the user's message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        if not st.session_state.indexed_files:
            answer, sources = "Please upload and process some documents first.", []
            st.markdown(answer)
        else:
            with st.spinner("Thinking..."):
                sources = retrieve_chunks(question, top_k)   # <- your retrieval
                answer = generate_answer(                    # <- your LLM call
                    question, sources, st.session_state.messages[:-1], model_name
                )
            st.markdown(answer)
            if show_sources and sources:
                with st.expander("Sources used"):
                    for c in sources:
                        st.caption(f"{c['source']} - page {c['page']} - score {c['score']:.2f}")
                        st.write(c["text"][:400])

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )