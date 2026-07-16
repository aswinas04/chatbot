# ---------- SQLite Patch for Streamlit Cloud Deployment ----------
import sys

try:
    import sqlite3
    if sqlite3.sqlite_version_info < (3, 35, 0):
        __import__('pysqlite3')
        sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except (ImportError, KeyError):
    pass

# ---------- Your Original Imports ----------
import os
import uuid
import chromadb
import streamlit as st
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.vector_stores.chroma import ChromaVectorStore

# ---------- STREAMLIT CLOUD API KEY CONFIGURATION ----------
load_dotenv()

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# LlamaIndex defaults package crash thavirkka openAI placeholder mask injection
os.environ["OPENAI_API_KEY"] = GROQ_API_KEY

# ---------- Configuration & Setup ----------
st.set_page_config(page_title="Python Book Chatbot", page_icon="✨")
st.title("📚 Python Book Chatbot (RAG)")

BOOKS_DIR, CHROMA_DIR, COLLECTION_NAME = "books", "chroma_db", "python_books"

if not GROQ_API_KEY:
    st.error("⚠️ GROQ_API_KEY kidaikala. Streamlit Secrets (illa .env)-la setup pannunga.")
    st.stop()

# --- GLOBAL SETTINGS FORCING GROQ ---
custom_llm = Groq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY, temperature=0.3, max_tokens=2048)
custom_embed = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

Settings.llm = custom_llm
Settings.embed_model = custom_embed

# ---------- Core RAG Initialization ----------
@st.cache_resource(show_spinner=False)
def load_index():
    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    if chroma_collection.count() > 0:
        return VectorStoreIndex.from_vector_store(
            vector_store=vector_store, 
            storage_context=StorageContext.from_defaults(vector_store=vector_store)
        )
        
    if not os.path.exists(BOOKS_DIR) or not os.listdir(BOOKS_DIR):
        return None
        
    documents = SimpleDirectoryReader(BOOKS_DIR).load_data()
    return VectorStoreIndex.from_documents(
        documents, 
        storage_context=StorageContext.from_defaults(vector_store=vector_store), 
        transformations=[SentenceSplitter(chunk_size=1024, chunk_overlap=100)]
    )

with st.spinner("Books-a ready pandren..."):
    index = load_index()

if index is None:
    st.warning(f"📚 `{BOOKS_DIR}/` folder-la PDF books edhum illai.")
    st.stop()

# ---------- Chat Session & Engine Management ----------
def make_new_chat_engine():
    # Enforcing custom llm context mapping directly to response synthesizer internals
    return index.as_chat_engine(
        chat_mode="context",
        llm=custom_llm,
        similarity_top_k=4,
        memory=ChatMemoryBuffer.from_defaults(token_limit=250),
        system_prompt="Talk like a warm friend. Base your answer exactly on the book text/code context. Be concise and don't skip details."
    )

if "chats" not in st.session_state:
    first_id = str(uuid.uuid4())
    st.session_state.chats = {first_id: {"title": "New Chat", "messages": [], "engine": make_new_chat_engine()}}
    st.session_state.active_chat_id = first_id

active_id = st.session_state.active_chat_id
active_chat = st.session_state.chats[active_id]

# ---------- Sidebar UI ----------
with st.sidebar:
    st.subheader("💬 Chat Sessions")
    if st.button("＋ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = {"title": "New Chat", "messages": [], "engine": make_new_chat_engine()}
        st.session_state.active_chat_id = new_id
        st.rerun()
    
    st.divider()
    for chat_id, chat in list(st.session_state.chats.items())[::-1]:
        if chat["messages"]:
            if st.button(chat["title"], key=f"open_{chat_id}", use_container_width=True):
                st.session_state.active_chat_id = chat_id
                st.rerun()

# ---------- Chat Interface ----------
for msg in active_chat["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_question = st.chat_input("Ask a question from your Python book...")
if user_question:
    if not active_chat["messages"]:
        active_chat["title"] = user_question[:30] + "..." if len(user_question) > 30 else user_question

    active_chat["messages"].append({"role": "user", "content": user_question})
    with st.chat_message("user"): st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the book..."):
            response = active_chat["engine"].chat(user_question)
            response_text = str(response)
            st.markdown(response_text)
            
    active_chat["messages"].append({"role": "assistant", "content": response_text})
