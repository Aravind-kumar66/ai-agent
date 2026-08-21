# 🤖 Gemini AI Agent

> A multi-tool AI agent built with Python and Google's Gemini API, combining autonomous tool selection, web search, weather, calculation, conversation memory, and Retrieval-Augmented Generation (RAG) over personal documents.

## 🚀 Overview

This project is an end-to-end AI agent designed to demonstrate how modern LLM-powered agents work beyond simple chatbot interactions.

Instead of only generating text, the agent can **reason about a user's request, select the appropriate tool, execute it, receive the result, and generate a final response**.

### Available tools

- 🧮 **Calculator** — performs mathematical calculations
- 🌤️ **Weather** — retrieves current weather information
- 🌐 **Web Search** — searches the web for external/current information
- 📚 **RAG** — searches my own documents using semantic similarity

The agent also maintains **conversation context** during the terminal session.

---

## ✨ Key Features

### 🧠 Automatic Tool Selection

The Gemini model decides which tool is appropriate for the user's request.

```text
User
 │
 ▼
Gemini Agent
 │
 ├── Calculator
 ├── Weather
 ├── Web Search
 └── RAG
````

The user doesn't need to manually select a tool.

---

### 🧮 Calculator

Uses a Python-based calculation tool for mathematical operations.

Example:

```text
You: Calculate 875 * 43

🔧 Using tool: calculate
Arguments: {'expression': '875 * 43'}

🤖 Agent: 875 × 43 = 37625
```

---

### 🌤️ Weather

Retrieves current weather information using geographic coordinates.

Example:

```text
You: What's the weather in Hyderabad?

🔧 Using tool: get_weather

🤖 Agent:
Temperature: 30°C
Condition: Clear sky
Humidity: 50%
Wind Speed: 14 km/h
```

---

### 🌐 Web Search

The agent can search the web when the requested information requires external or current information.

Example:

```text
You: Search the web for the latest Python release.

🔧 Using tool: web_search

🤖 Agent: ...
```

---

### 📚 Retrieval-Augmented Generation

The agent can search information from my own documents.

Supported document types:

* PDF
* TXT
* Markdown

The RAG pipeline performs:

```text
Document
   ↓
Text Extraction
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Store
   ↓
Similarity Search
   ↓
Relevant Chunks
   ↓
Gemini
   ↓
Answer
```

Example:

```text
You: What projects are mentioned in my resume?

🔧 Using tool: rag_search

🤖 Agent:
The documents mention projects including
Fake News Detection, Customer Segmentation,
Sales Data Analysis Dashboard, and Jarvis.
```

Retrieved results also include their document source.

---

## 🧠 Conversation Memory

The agent maintains conversation context using a Gemini chat session.

Example:

```text
You: My name is Aravind.

Agent: Nice to meet you, Aravind!

You: What is my name?

Agent: Your name is Aravind.
```

---

## 🔄 Multi-Tool Reasoning

The agent can handle requests that require more than one tool.

Example:

```text
You: Calculate 25 * 48 and then tell me
what projects are in my resume.
```

The agent can perform:

```text
              User Request
                   │
                   ▼
                Gemini
                /    \
               ▼      ▼
        Calculator    RAG
             │         │
             ▼         ▼
           1200    Resume Data
               \     /
                ▼   ▼
             Final Answer
```

A safety limit is also applied to prevent excessive tool execution.

---

# 🏗️ Architecture

```text
                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Terminal Chat   │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Gemini Agent   │
                       │                 │
                       │ Reasoning       │
                       │ Tool Selection  │
                       │ Memory          │
                       └────────┬────────┘
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             ▼                  ▼                  ▼
       ┌──────────┐       ┌──────────┐       ┌───────────┐
       │Calculator│       │ Weather  │       │Web Search │
       └──────────┘       └──────────┘       └───────────┘
                                │
                                ▼
                         ┌────────────┐
                         │    RAG     │
                         └─────┬──────┘
                               │
                               ▼
                       ┌───────────────┐
                       │ Own Documents │
                       └───────────────┘
```

---

# 🛠️ Tech Stack

| Technology            | Purpose                          |
| --------------------- | -------------------------------- |
| Python                | Core application                 |
| Google Gemini API     | LLM reasoning and tool selection |
| google-genai          | Gemini API integration           |
| Requests              | HTTP requests                    |
| Open-Meteo            | Weather data                     |
| DuckDuckGo            | Web search                       |
| Sentence Transformers | Document embeddings              |
| NumPy                 | Vector similarity                |
| PyPDF                 | PDF text extraction              |
| python-dotenv         | Environment variables            |
| Git                   | Version control                  |
| GitHub                | Project hosting                  |

---

# 📁 Project Structure

```text
ai-agent/
│
├── .gitignore
├── README.md
├── requirements.txt
├── .env                  # Local only - never commit
│
├── main.py               # Terminal chat interface
├── agent.py              # Gemini agent and tool orchestration
├── config.py             # Configuration and API key loading
│
├── tools/
│   ├── __init__.py
│   ├── calculator.py     # Calculator tool
│   ├── weather.py        # Weather tool
│   └── web_search.py     # Web search tool
│
└── rag/
    ├── __init__.py
    ├── rag_tool.py       # RAG document retrieval
    ├── vector_store.py   # Embeddings and similarity search
    │
    └── documents/
        ├── about_me.txt
        └── IIT RESUME.pdf
```

---

# ⚙️ How It Works

## 1. User sends a message

```text
What projects are in my resume?
```

## 2. Gemini analyzes the request

The model determines that the user's documents are required.

## 3. Gemini selects the RAG tool

```text
rag_search(
    query="What projects are in my resume?"
)
```

## 4. RAG retrieves relevant information

The query is converted into an embedding and compared with document embeddings.

## 5. Results are returned to Gemini

Relevant document chunks and their similarity scores are provided.

## 6. Gemini generates the final response

The model uses the retrieved information to answer the user.

---

# 📚 RAG Implementation

The RAG system uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

for generating document and query embeddings.

Documents are divided into chunks and stored with their source filename.

Example retrieved result:

```text
Source: IIT RESUME.pdf
Similarity: 0.179

Fake News Detection using Machine Learning...
```

This allows the system to provide both the retrieved information and its source.

---

# 🔐 Environment Setup

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

The API key is loaded through environment variables.

**Never commit `.env` to GitHub.**

The repository includes a `.gitignore` file that excludes:

```text
.env
venv/
__pycache__/
```

---

# 📦 Installation

## Clone the repository

```bash
git clone https://github.com/Aravind-kumar66/ai-agent.git
cd ai-agent
```

## Create a virtual environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Configure Gemini

Create `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key
```

---

# ▶️ Run

Start the terminal agent:

```bash
python main.py
```

You should see:

```text
============================================================
🤖 GEMINI AI AGENT
============================================================
Available tools:
  🧮 Calculator
  🌤️  Weather
  🌐 Web Search
  📚 Document RAG

Type 'exit' to quit.
============================================================
```

---

# 🧪 Example Queries

### Calculator

```text
Calculate 125 * 48
```

### Weather

```text
What is the weather in Hyderabad right now?
```

### Web Search

```text
Search the web for the latest Python release.
```

### RAG

```text
What machine learning projects are in my resume?
```

### Memory

```text
My name is Aravind.

What is my name?
```

### Multi-tool

```text
Calculate 25 * 48 and then tell me
what projects are in my resume.
```

---

# 🧩 Design Principles

### LLM for reasoning

Gemini is responsible for:

* Understanding natural language
* Deciding whether a tool is required
* Selecting the appropriate tool
* Interpreting tool results
* Generating the final response

### Python for deterministic operations

Tools handle tasks where deterministic execution is preferable:

```text
Mathematics  → Calculator
Weather      → Weather API
Web data     → Search API
Documents    → RAG
```

This keeps the agent modular and easier to extend.

---

# 🛡️ Reliability & Safety

The agent includes a maximum tool-call limit per request.

This helps prevent:

* Infinite tool loops
* Accidental repeated API calls
* Excessive API usage

API errors such as quota exhaustion are also handled separately from normal application errors.

---

# 🧠 What I Learned

Building this project helped me understand the practical architecture behind AI agents:

* Gemini API integration
* Function declarations
* Automatic tool calling
* Tool execution loops
* Conversation sessions
* API integration
* REST requests
* Embeddings
* Semantic search
* RAG pipelines
* PDF processing
* Vector similarity
* Environment variables
* Git/GitHub project management
* Modular Python architecture

---

# 🚧 Future Improvements

Planned improvements:

* [ ] Persistent long-term memory
* [ ] Streaming responses
* [ ] Better document chunking
* [ ] Metadata filtering
* [ ] RAG similarity threshold
* [ ] More document formats
* [ ] Improved source citations
* [ ] Automated unit tests
* [ ] Web interface
* [ ] FastAPI backend
* [ ] Docker support
* [ ] Cloud deployment
* [ ] Agent execution tracing
* [ ] Additional tools

---

# 🎯 Project Highlights

This project demonstrates practical implementation of:

**Generative AI**
**AI Agents**
**LLM Tool Calling**
**RAG**
**Embeddings**
**Semantic Search**
**API Integration**
**Conversation Memory**
**Python Software Architecture**

The goal was not simply to build another chatbot, but to understand how an LLM can act as a **reasoning layer that coordinates deterministic tools and external knowledge sources**.

---

# 👨‍💻 About

**Aravind Kumar**

Computer Science & Engineering Student

Interested in:

* Artificial Intelligence
* Machine Learning
* Generative AI
* AI Agents
* Data Analytics
* Retrieval-Augmented Generation

---

## ⭐ If you find this project interesting

Feel free to explore the code, experiment with the tools, and extend the agent with your own capabilities.

---

**Built with Python 🐍 + Gemini 🤖 + RAG 📚**

```

That's the **actual README.md content**. No extra files or code are needed for the README itself.
```
