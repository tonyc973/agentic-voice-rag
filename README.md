# 🎙️ Your Agentic Voice RAG Template Application



## What is it and what it does
We've all heard about the agentic AI workflows and I bet every curious programmer tried to build and deploy one at least one time. I tried multiple times to implement agentic apps and after all my trial and error approaches, I collected a wide array of insights required to build a versatile system with great reasoning capabilities, access to external tools and a very intuitive UI while keeping it cool and simple. The most amazing thing about this project is that it bridges Local Speech-to-Text (`whispercpp` models), RAG (Retrieval Augmented Generation) and Agent Orchestration (`crewai`) into a single deployable and modular unit that is designed to help you build a fully functional agentic workflow for your use case blazingly fast.

<img width="1919" height="934" alt="image" src="https://github.com/user-attachments/assets/25d25b56-3be6-4aa5-abf8-7e51bdddd3a7" />




## Why you’ll like it
| Feature | Benefit |
|---------|---------|
| **🔒 100 % local audio** | `pywhispercpp` models keep your voice data private running on your CPU|
| **🧩 YAML agents** | Change your entire workflow by simply editing `/config`, not code |
| **📄 PDF-native** | Drag-and-drop a PDF file and update the knowledge base of the workflow; it’s chunked & indexed automatically |
| **🐳 One-command deploy** | `docker compose up --build` and you’re done |



## Two-service architecture
| Service | Tech stack | Job |
|---------|------------|-----|
| **Speech-to-Text Backend** | Flask + Whisper CPP | Sanitize & transcribe WAV files |
| **Agents + Frontend** | Streamlit + CrewAI | Orchetrate agents, chat UI |






## 🚀 Quick start
```bash
# Clone the repo
git clone https://github.com/yourusername/agentic-voice-rag.git
cd agentic-voice-rag

# Open .env and set your OPENAI_API_KEY (momentarily the solution is not fully local, but will be in future)
cp .env.example .env


docker-compose up --build
# Access the application at http://localhost:8501

