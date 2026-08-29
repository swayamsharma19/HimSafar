# Himachal Pradesh Travel RAG Assistant

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about
Himachal Pradesh travel — permits, road closures, trekking rules, and safety
guidelines — grounded in official tourism and government sources, with cited
answers instead of hallucinated ones.

## Why this project

Most student RAG projects are "chat with a generic PDF." This one uses
messy, real, domain-specific government and tourism content — permit rules
that vary by route, district, and nationality — which required real decisions
around chunking, retrieval, and hallucination handling rather than just
following a tutorial.

## Stack

- **LangChain** — RAG orchestration
- **ChromaDB** — local vector database
- **sentence-transformers (all-MiniLM-L6-v2)** — free, local embeddings
- **Groq (Llama 3.1 8B)** — fast, free-tier LLM inference
- **Streamlit** — chat UI

## Setup

```bash
pip install -r requirements.txt

# 1. Build the vector index from the source documents in data/raw/
python src/build_index.py

# 2. Get a free API key at https://console.groq.com

# 3. Run the chat app
streamlit run src/app.py
```

## Design decisions worth mentioning in interviews

- **Chunk size (500 chars, 100 overlap):** government/permit text has dense,
  standalone facts — smaller chunks with overlap preserve context across
  boundaries without diluting retrieval with irrelevant text.
- **Grounded-answer prompting:** the system prompt explicitly instructs the
  model to say "I don't know" when context is insufficient, rather than
  guessing — the core problem RAG is meant to solve.
- **Source citation:** every answer shows which document(s) it drew from,
  so answers are verifiable, not just plausible-sounding.
- **Local embeddings:** using a free local embedding model instead of a paid
  API keeps the project runnable by anyone without cost, and avoids sending
  data to a third party unnecessarily.

## Next steps / possible extensions

- Expand `data/raw/` with more scraped government sources (real scraping
  script, not just static files).
- Add an evaluation step (e.g. a set of test questions with expected answers)
  to measure retrieval quality.
- Swap the local Chroma store for a hosted vector DB if scaling beyond a
  demo.
