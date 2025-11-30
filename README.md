# 🧠 Agentic Voice RAG Template 🎙️

> **A production-ready, modular template for building Voice-Activated Agentic Workflows.**

This repository provides a robust scaffold for building AI applications that can **listen**, **think**, and **respond**. It combines local Speech-to-Text (Whisper), Vector Search (RAG), and Multi-Agent Orchestration (CrewAI) into a seamless, containerized experience.



[Image of agentic workflow architecture diagram]


## ✨ Key Features

* **🗣️ Privacy-First Voice:** Uses a local, optimized Whisper C++ backend (\`pywhispercpp\`) for speech transcription. No audio data leaves your server.

* **🤖 Modular Agent Architecture:** Logic is decoupled from configuration. Define your Agents and Tasks in \`YAML\` files—no code changes required to change behavior!

* **📚 RAG (Retrieval Augmented Generation):** Built-in support for PDF ingestion, chunking, and vector retrieval using FAISS and OpenAI Embeddings.

* **🐳 Docker Ready:** Fully containerized architecture (Frontend + Backend) for one-click deployment.

* **🛠️ Custom Tools:** Includes a pre-built, robust \`BaseTool\` implementation for PDF searching, ready to be expanded.

## 🏗️ Architecture

The application is split into two microservices:

1. **Backend (\`backend_server.py\`):** A lightweight Flask API that handles audio processing. It accepts WAV files, sanitizes them, and runs them through a local Whisper model.

2. **Frontend (\`app.py\`):** A Streamlit interface that handles:

   * Microphone recording (browser-native).

   * Chat interface.

   * Agent orchestration (CrewAI).

## 🚀 Getting Started

### Option A: Docker (Recommended)

The easiest way to run the stack.

1. **Clone the repository:**

   \`\`\`bash
   git clone https://github.com/yourusername/agentic-voice-rag.git
   cd agentic-voice-rag
   \`\`\`

2. **Set up environment variables:**

   \`\`\`bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   \`\`\`

3. **Run with Docker Compose:**

   \`\`\`bash
   docker-compose up --build
   \`\`\`

4. **Access the App:**
   Open \`http://localhost:8501\` in your browser.

### Option B: Local Python Development

1. **Install system dependencies (required for Audio):**

   * *Linux:* \`sudo apt install ffmpeg libsndfile1\`

   * *Mac:* \`brew install ffmpeg\`

2. **Install Python dependencies:**

   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Run the Backend (Terminal 1):**

   \`\`\`bash
   python backend_server.py
   \`\`\`

4. **Run the Frontend (Terminal 2):**

   \`\`\`bash
   streamlit run app.py
   \`\`\`

## ⚙️ Customization

Make this template your own by editing the \`config/\` directory.

### 1. Define Your Agents (\`config/agents.yaml\`)

Want to change the "Researcher" to a "Financial Analyst"? Just edit the YAML:

\`\`\`yaml
financial_analyst:
  role: "Senior Financial Analyst"
  goal: "Analyze the uploaded earnings report and extract key metrics."
  backstory: "You are a Wall Street veteran..."
\`\`\`

### 2. Define Your Tasks (\`config/tasks.yaml\`)

Control the workflow by defining tasks that reference your agents:

\`\`\`yaml
analysis_task:
  description: "Analyze the spreadsheet for Q3 growth."
  expected_output: "A markdown table summarizing Q3 revenue."
  agent: financial_analyst
\`\`\`

## 🤝 Contributing

We love contributions! If you have ideas for new tools, better Whisper models, or UI improvements:

1. Fork the Project

2. Create your Feature Branch (\`git checkout -b feature/AmazingFeature\`)

3. Commit your Changes (\`git commit -m 'Add some AmazingFeature'\`)

4. Push to the Branch (\`git push origin feature/AmazingFeature\`)

5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See \`LICENSE\` for more information.
