# 🏔️ HimSafar

> 🤖 An AI-powered travel companion for exploring Himachal Pradesh with RAG-based insights, real-time web search, and reliable travel information.

![Status](https://img.shields.io/badge/Status-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![LangChain](https://img.shields.io/badge/LangChain-RAG-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Groq](https://img.shields.io/badge/Groq-Llama-purple)
![Tavily](https://img.shields.io/badge/Tavily-Web%20Search-green)

---

## 🌐 Live Demo

🚀 **HimSafar:** https://himsafar.streamlit.app

---

## ✨ Features

- 🏔️ **Himachal-focused AI Assistant** — Get travel-related information specifically for Himachal Pradesh.
- 🤖 **RAG-based Responses** — Retrieves relevant information from a dedicated knowledge base before generating answers.
- 🌐 **Real-Time Web Search** — Uses Tavily to find updated information when the local knowledge base is insufficient.
- 🎯 **Topic Guardrails** — Keeps conversations focused on Himachal Pradesh travel and tourism.
- 🔍 **Source-Aware Answers** — Identifies whether information comes from local documents, web search, or general knowledge.
- 🥾 **Travel & Trekking Information** — Ask about destinations, trekking rules, permits, seasons, road conditions, safety, and more.
- 🎨 **Mountain-Themed UI** — A clean and simple Streamlit interface inspired by the landscapes of Himachal Pradesh.

## 🛠️ Tech Stack

### 🤖 AI & RAG

| Technology | Usage |
|------------|-------|
| 🐍 Python | Core application logic |
| 🦜 LangChain | RAG pipeline and orchestration |
| 🔮 FastEmbed | Text embeddings |
| 🗄️ ChromaDB | Vector database |
| ⚡ Groq | Fast LLM inference |
| 🧠 Llama | Language model |
| 🔎 Tavily | Real-time web search |

### 🎨 Application

| Technology | Usage |
|------------|-------|
| 🎈 Streamlit | Web application |
| 🎨 Custom CSS | UI styling |
| 📄 Markdown | Formatted responses |


## 📂 Project Structure

```text
HimSafar/
│
├── 📁 .streamlit/
│   └── config.toml
│
├── 📁 data/
│   └── 📁 raw/
│       └── Source documents
│
├── 📁 src/
│   ├── app.py
│   ├── rag_chain.py
│   └── build_index.py
│
├── 📄 .gitignore
├── 📄 README.md
├── 📄 requirements.txt
└── 📄 runtime.txt



## 🔄 RAG Pipeline

HimSafar follows a retrieval-first approach.

### 1️⃣ Ask

The user asks a travel-related question.

### 2️⃣ Classify

The system checks whether the question is related to Himachal Pradesh.

### 3️⃣ Retrieve

Relevant information is retrieved from the local ChromaDB vector database.

### 4️⃣ Search

If sufficient information is not found, Tavily performs a real-time web search.

### 5️⃣ Generate

The retrieved information is passed to the Llama model through Groq.

### 6️⃣ Respond

HimSafar generates a clear answer using the available context.

---

## 🔑 API Keys

HimSafar uses:

- ⚡ **Groq** for LLM inference
- 🔎 **Tavily** for real-time web search

> ⚠️ Never commit your `.env` file or expose your API keys publicly.

---

## 🌟 Why HimSafar?

Generic AI assistants may provide broad travel information.

HimSafar is specifically designed around **Himachal Pradesh**, combining:

📚 Local Knowledge
+
🔍 Vector Search
+
🤖 RAG
+
🌐 Real-Time Web Search
+
🧠 LLM
↓
🏔️ AI Travel Assistant

This allows travelers to get more relevant and context-aware information for their Himachal Pradesh journeys.

---

## 🌄 Domain

**Travel & Tourism**

HimSafar focuses on helping travelers explore Himachal Pradesh with AI-assisted and source-grounded information.

---

## 👨‍💻 Developer

### Swayam Sharma

- 🐙 GitHub: [@swayamsharma19](https://github.com/swayamsharma19)
- 💼 LinkedIn: [swayamsharma19](https://www.linkedin.com/in/swayamsharma19/)

---

## ❤️ Made for Himachal Pradesh

> Made with ❤️ for the mountains, valleys, and people of Himachal Pradesh 🏔️

⭐ If you found HimSafar useful, consider giving the repository a star!
