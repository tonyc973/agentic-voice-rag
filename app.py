import streamlit as st
import os
import tempfile
import requests
import warnings
from dotenv import load_dotenv
from streamlit_mic_recorder import mic_recorder

# --- Local Imports ---
from src.crew_graph import AgenticWorkflow
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# --- Init ---
load_dotenv()
st.set_page_config(page_title="Agentic Voice RAG", layout="wide", page_icon="🧠")
warnings.filterwarnings("ignore")

# --- State ---
if "messages" not in st.session_state: st.session_state.messages = []
if "vectorstore" not in st.session_state: st.session_state.vectorstore = None
if "last_audio" not in st.session_state: st.session_state.last_audio = None

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    if not os.getenv("OPENAI_API_KEY"):
        user_key = st.text_input("OpenAI API Key", type="password")
        if user_key: os.environ["OPENAI_API_KEY"] = user_key
    
    st.divider()
    uploaded_file = st.file_uploader("Upload Knowledge (PDF)", type="pdf")
    
    if uploaded_file and st.button("Ingest Knowledge"):
        if not os.environ.get("OPENAI_API_KEY"):
            st.error("API Key required.")
        else:
            with st.spinner("Indexing..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                loader = PyPDFLoader(tmp_path)
                chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(loader.load())
                st.session_state.vectorstore = FAISS.from_documents(chunks, OpenAIEmbeddings(model="text-embedding-3-small"))
                st.success(f"Indexed {len(chunks)} chunks.")
                os.unlink(tmp_path)

# --- Helper ---
def get_history():
    return "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-6:]])

def transcribe_audio(audio_bytes):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_bytes)
            fname = f.name
        with open(fname, "rb") as f:
            url = os.getenv("WHISPER_URL", "http://127.0.0.1:5001/transcribe")
            resp = requests.post(url, files={"audio": (os.path.basename(fname), f, "audio/wav")}, timeout=30)
        os.unlink(fname)
        return resp.json().get("transcription") if resp.status_code == 200 else None
    except Exception as e:
        st.error(f"Transcription Error: {e}")
        return None

# --- Main UI ---
st.title("🧠 Production Agentic Template")

# Chat UI
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])

# Inputs
input_container = st.container()
with input_container:
    col_mic, col_input = st.columns([1, 8])
    with col_mic:
        audio = mic_recorder(start_prompt="🎙️", stop_prompt="⏹️", key='rec', format='wav')
    
    user_input = st.chat_input("Type message...")

# Logic
final_query = None

if audio and audio['bytes'] != st.session_state.last_audio:
    st.session_state.last_audio = audio['bytes']
    with st.spinner("Transcribing..."):
        text = transcribe_audio(audio['bytes'])
        if text: final_query = text

if user_input:
    final_query = user_input

if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"): st.write(final_query)
    
    with st.chat_message("assistant"):
        with st.spinner("Agent Crew is working..."):
            try:
                workflow = AgenticWorkflow()
                response = workflow.run(query=final_query, chat_history=get_history())
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")
