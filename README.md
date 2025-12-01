# 🎙️ Your Agentic Voice RAG Template Application
&gt; A plug-and-play template application that enables you build and deploy agentic apps fast.

---

## What is it and what it does
We've all heard about the agentic AI workflows and I bet every curious programmer tried to build and deploy one at least one time. I tried multiple times to implement agentic apps and after all my trial and error approaches, I collected a wide array of insights required to build a versatile system with great reasoning capabilities, access to external tools and a very intuitive UI while keeping it cool and simple. The most amazing thing about this project is that it bridges Local Speech-to-Text (`whispercpp` models), RAG (Retrieval Augmented Generation) and Agent Orchestration (`crewai`) into a single deployable and modular unit that is designed to help you build a fully functional agentic workflow for your use case blazing fast.

---

## ✨ Why you’ll like it
| Feature | Benefit |
|---------|---------|
| **🔒 100 % local audio** | `pywhispercpp` keeps your voice data private |
| **🧩 YAML agents** | Change behaviour by editing `/config`, not code |
| **📄 PDF-native** | Drag-and-drop a PDF and update the knowledge base; it’s chunked & indexed automatically |
| **🐳 One-command deploy** | `docker compose up --build` and you’re done |

---

## 🏗️ Two-service architecture
| Service | Tech stack | Job |
|---------|------------|-----|
| **Backend** | Flask + Whisper CPP | Sanitize & transcribe WAV |
| **Frontend** | Streamlit + CrewAI | Record mic, run agents, chat UI |

---

## 🚀 Quick start
```bash
git clone https://github.com/yourusername/agentic-voice-rag.git
cd agentic-voice-rag

cp .env.example .env
# Open .env and set your OPENAI_API_KEY

docker-compose up --build

# Access the application at http://localhost:8501.

