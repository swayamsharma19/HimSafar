# 🏔️ HimSafar

> Your AI companion for the Land of the Gods — permits, trekking rules, road conditions, and travel planning across Himachal Pradesh, grounded in real sources.

**Status:** `Live` &nbsp;|&nbsp; **Type:** `RAG Chatbot` &nbsp;|&nbsp; **Domain:** `Travel & Tourism`

---

## 🌐 Live Demo

- 🚀 **App:** [himsafar.streamlit.app](https://himsafar.streamlit.app)
- 💻 **Source:** this repository

---

## ✨ Features

- 📚 **Grounded answers** — retrieves from a local knowledge base of official Himachal Pradesh tourism/government sources before answering
- 🌐 **Live web search fallback** — falls back to real-time Tavily search when local documents don't cover a question, instead of guessing
- 🎯 **Topic-scoped** — politely declines questions unrelated to Himachal Pradesh travel, using a fast pre-classification step to avoid wasted searches
- 🔍 **Source transparency** — every answer shows whether it came from local documents, the web, or general knowledge
- 🎨 **Custom themed UI** — mountain-themed design built with Streamlit + custom CSS

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| 🐍 Python | Core application logic |
| 🦜 LangChain | RAG orchestration & prompt chaining |
| 🔮 FastEmbed | Local text embeddings |
| 🗄️ ChromaDB | Vector database for document retrieval |
| ⚡ Groq (Llama) | LLM inference |
| 🔎 Tavily | Live web search API |
| 🎈 Streamlit | Chat UI & deployment |

---

## 📂 Project Structure
HimSafar/
├── src/
│ ├── app.py # Streamlit chat UI
│ ├── rag_chain.py # RAG pipeline: retrieval, web fallback, generation
│ └── build_index.py # Builds the local vector index from data/raw/
├── data/
│ └── raw/ # Source documents (permits, destinations, seasons, safety)
├── requirements.txt
└── README.md


---

## 🧠 Design Decisions

- **Chunking & retrieval threshold** tuned by testing real questions against actual similarity scores, not guessed values
- **Topic guardrail** runs a cheap classification call *before* retrieval, so off-topic questions never trigger a wasted search
- **Graceful degradation** — if web search fails, the app falls back to general knowledge rather than crashing

---

## 🚀 Run Locally

```bash
pip install -r requirements.txt
python src/build_index.py
streamlit run src/app.py
```

Requires free API keys from [Groq](https://console.groq.com) and [Tavily](https://tavily.com), set in a `.env` file:
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key


---

**Built by [Swayam Sharma](https://github.com/swayamsharma19)**
