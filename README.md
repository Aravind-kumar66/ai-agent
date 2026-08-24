
# 🤖 AI Agent

> A multi-tool AI agent built with Python, Streamlit, and Google Gemini API, combining autonomous tool selection, web search, weather forecasts, calculation, conversation memory, and Retrieval-Augmented Generation (RAG).

## 🌐 Live Demo
👉 [Try it here](https://your-app-name.streamlit.app/)

---

## 📌 What it does

An end-to-end autonomous AI agent capable of reasoning over user queries, selecting the correct execution tools, and streaming responses back via a dark-mode glassmorphism web interface.

- Autonomous tool routing using Gemini API function calling
- Mathematical evaluation via custom python execution tool
- Live weather retrieval via Open-Meteo API
- Real-time web search integration via DuckDuckGo
- Semantic vector search (RAG) over personal documents (PDF, TXT, MD)
- Multi-tool reasoning for complex, multi-step user prompts
- Session memory management with clear-history controls
- Futuristic Streamlit UI with animated streaming text and neon accents

---

## 🔧 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web interface & session management |
| Google Gemini API | LLM reasoning & tool routing |
| Sentence Transformers | Document text embeddings (`all-MiniLM-L6-v2`) |
| NumPy | In-memory vector similarity computation |
| pypdf | PDF document extraction |
| python-dotenv | Local environment configuration |

---

## ⚙️ How it works

User Input
↓
Gemini Reasoning & Tool Selection
├── 🧮 Calculator Tool
├── 🌤️ Weather API Tool
├── 🌐 Web Search Tool
└── 📚 RAG (Embeddings Vector Search)
↓
Tool Execution & Context Retrieval
↓
Gemini Synthesizes Final Answer
↓
Streamed UI Response

---

## ▶️ Run Locally

```bash
git clone [https://github.com/Aravind-kumar66/ai-agent.git](https://github.com/Aravind-kumar66/ai-agent.git)
cd ai-agent
pip install -r requirements.txt

```

Set your API key:

```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-key-here"

# Mac/Linux
export GEMINI_API_KEY="your-key-here"

```

Run:

```bash
streamlit run app.py

```

---

## 📦 Requirements

google-genai==2.19.0
python-dotenv==1.2.3
requests==2.34.2
pypdf==6.16.1
sentence-transformers==6.0.0
numpy==2.2.6
streamlit

---

## 🚀 Future Improvements

* Dynamic in-browser PDF uploader for instant RAG indexing
* Persistent vector store integration (ChromaDB)
* Additional tools (Code Interpreter, Database Queries)
* REST API backend using FastAPI
* Docker containerization

---

## 👨‍💻 Author

**Kudupuri Aravind Kumar**
B.Tech CSE — Adikavi Nannaya University

GitHub: [Aravind-kumar66](https://github.com/Aravind-kumar66)
LinkedIn: [aravindkumar1066](https://linkedin.com/in/aravindkumar1066)

```