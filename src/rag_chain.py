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

PROMPT_TEMPLATE = """You are Himsafar, a Himachal Pradesh travel assistant.

You ONLY answer questions related to travel, tourism, permits, trekking,
roads, weather, destinations, or culture within Himachal Pradesh.

If the question is unrelated to Himachal Pradesh travel, politely decline
and redirect. Do NOT answer the off-topic question even partially.

If the question IS about Himachal Pradesh travel, answer naturally and
directly using the context below, mentioning the source briefly where relevant.

Context:
{context}

Question: {question}

Answer:"""

OFF_TOPIC_MESSAGE = (
    "I'm focused on helping with Himachal Pradesh travel — feel free to ask me "
    "about permits, trekking routes, weather, or places to visit here!"
)


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


def load_vector_store():
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    return Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)


def get_context(question, vector_store, tavily_api_key):
    results_with_scores = vector_store.similarity_search_with_score(question, k=4)

    if results_with_scores:
        print(f"DEBUG: top match distance = {results_with_scores[0][1]:.3f} (threshold = {DISTANCE_THRESHOLD})")

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


def is_on_topic(question, groq_api_key):
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
    if not is_on_topic(question, groq_api_key):
        return OFF_TOPIC_MESSAGE, "off_topic", []

    vector_store = load_vector_store()
    context, source_type, raw_sources = get_context(question, vector_store, tavily_api_key)

    llm = build_llm(groq_api_key)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({"context": context, "question": question})
    return answer, source_type, raw_sources