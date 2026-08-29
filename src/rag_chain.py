"""
rag_chain.py
------------
The RAG pipeline: first retrieve relevant chunks from the local vector
store (built from data/raw/). If the local documents don't cover the
question well (similarity score below threshold), fall back to a fast,
reliable web search via Tavily's API instead of guessing from the model's
own memory.
"""

import os
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from tavily import TavilyClient

PERSIST_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "chroma_db")

DISTANCE_THRESHOLD = 1.2

PROMPT_TEMPLATE = """You are a knowledgeable, friendly Himachal Pradesh travel assistant.

Answer the question naturally and directly, the way a helpful travel expert would.

Use the context below, and mention where the information came from briefly
and naturally.

Context:
{context}

Question: {question}

Answer:"""


def format_docs(docs):
    formatted = []
    for doc in docs:
        source = os.path.basename(doc.metadata.get("source", "unknown"))
        formatted.append(f"[Local source: {source}]\n{doc.page_content}")
    return "\n\n---\n\n".join(formatted)


def format_web_results(results):
    formatted = []
    for r in results.get("results", []):
        title = r.get("title", "")
        content = r.get("content", "")
        url = r.get("url", "")
        formatted.append(f"[Web source: {title} ({url})]\n{content}")
    return "\n\n---\n\n".join(formatted)


def web_search(query, tavily_api_key, max_results=4):
    client = TavilyClient(api_key=tavily_api_key)
    return client.search(f"{query} Himachal Pradesh travel", max_results=max_results)


def get_context(question, vector_store, tavily_api_key):
    results_with_scores = vector_store.similarity_search_with_score(question, k=4)
    if results_with_scores:
        print(f"DEBUG: top match distance = {results_with_scores[0][1]:.3f} (threshold = {DISTANCE_THRESHOLD})")

    if results_with_scores and results_with_scores[0][1] <= DISTANCE_THRESHOLD:

     if results_with_scores and results_with_scores[0][1] <= DISTANCE_THRESHOLD:
        docs = [doc for doc, score in results_with_scores]
        return format_docs(docs), "local", docs

    try:
        web_results = web_search(question, tavily_api_key)
        sources = web_results.get("results", [])
        if sources:
            return format_web_results(web_results), "web", sources
    except Exception as e:
        print(f"Web search failed: {e}")

    return "(No local or web sources available for this question.)", "general_knowledge", []


def build_llm(groq_api_key):
    return ChatGroq(
        groq_api_key=groq_api_key,
        model_name="openai/gpt-oss-20b",
        temperature=0,
    )


def load_vector_store():
    """Load the embedding model and vector store once, not on every question."""
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    return Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)


OFF_TOPIC_MESSAGE = (
    "I'm focused on helping with Himachal Pradesh travel — feel free to ask me "
    "about permits, trekking routes, weather, or places to visit here!"
)


def is_on_topic(question, groq_api_key):
    """
    Quick, cheap classification call: is this question about Himachal Pradesh
    travel? Runs BEFORE retrieval/search so off-topic questions don't waste
    a web search call.
    """
    llm = build_llm(groq_api_key)
    check_prompt = ChatPromptTemplate.from_template(
        "Is the following question related to Himachal Pradesh travel, tourism, "
        "permits, trekking, weather, or destinations? Answer with only one word: "
        "YES or NO.\n\nQuestion: {question}\n\nAnswer:"
    )
    chain = check_prompt | llm | StrOutputParser()
    result = chain.invoke({"question": question}).strip().upper()
    return result.startswith("YES")


def ask(question, groq_api_key, tavily_api_key):
    """
    Ask a question. First checks if it's on-topic. If not, declines without
    doing any retrieval or search. If on-topic, retrieves from local docs
    first, falls back to Tavily web search if local docs don't cover it.
    """
    if not is_on_topic(question, groq_api_key):
        return OFF_TOPIC_MESSAGE, "off_topic", []

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)

    context, source_type, raw_sources = get_context(question, vector_store, tavily_api_key)

    llm = build_llm(groq_api_key)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({"context": context, "question": question})
    return answer, source_type, raw_sources
