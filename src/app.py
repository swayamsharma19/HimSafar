"""
app.py
------
Streamlit chat interface for the Himachal Pradesh Travel RAG assistant.
Local documents are checked first; falls back to live Tavily web search
when local docs don't cover the question.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from rag_chain import ask, load_vector_store

load_dotenv()

st.set_page_config(page_title="Himachal Travel Assistant", page_icon="🏔️")

st.markdown("""
<style>
    .stApp {
        background-image: linear-gradient(rgba(20, 40, 60, 0.35), rgba(20, 40, 60, 0.45)),
                           url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    h1 {
        color: #FFFFFF !important;
        font-weight: 800;
        text-shadow: 0 2px 14px rgba(0,0,0,0.5);
    }
    .stCaption, p {
        color: #F0F4F8 !important;
        text-shadow: 0 1px 6px rgba(0,0,0,0.4);
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.92) !important;
        color: #1a1a1a !important;
        border-radius: 16px;
        padding: 8px 12px;
        border: 1px solid rgba(255,255,255,0.5);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    .stChatMessage p,
    .stChatMessage li,
    .stChatMessage strong,
    .stChatMessage span,
    .stChatMessage div {
        color: #1a1a1a !important;
        text-shadow: none !important;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.95);
    }
    [data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }

    [data-testid="stChatInput"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    [data-testid="stChatInputTextArea"] {
        background-color: #FFFFFF !important;
        color: #1a1a1a !important;
        -webkit-text-fill-color: #1a1a1a !important;
        caret-color: #1a1a1a !important;
        border-radius: 14px !important;
        border: 2px solid #F4A950 !important;
        padding: 12px 16px !important;
    }
    [data-testid="stChatInputTextArea"]::placeholder {
        color: #6b6b6b !important;
        -webkit-text-fill-color: #6b6b6b !important;
    }

    .stButton button, [data-testid="stChatInputSubmitButton"] {
        background-color: #F4A950 !important;
        color: white !important;
    }

    [data-testid="stBottom"] {
        background: linear-gradient(180deg, rgba(20,40,60,0) 0%, rgba(10,20,30,0.92) 80%) !important;
    }
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"] {
        background: transparent !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex; align-items:center; gap:14px; margin-bottom:6px;">
  <svg width="52" height="52" viewBox="0 0 24 24" fill="none">
    <path d="M3 20L9 8L12 13L15 9L21 20H3Z" fill="#7FD6C6" stroke="#FFFFFF" stroke-width="0.5"/>
    <path d="M9 8L11 11.5L12 10L9 8Z" fill="#FFFFFF" opacity="0.9"/>
  </svg>
  <h1 style="margin:0;">HimSafar</h1>
</div>
""", unsafe_allow_html=True)

st.caption("Your AI companion for the Land of the Gods — permits, trekking rules, road conditions, "
           "and travel planning across Himachal Pradesh, grounded in real sources.")

groq_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "") or st.sidebar.text_input(
    "Groq API Key", type="password", help="Get a free key at console.groq.com"
)
tavily_key = os.environ.get("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY", "") or st.sidebar.text_input(
    "Tavily API Key", type="password", help="Get a free key at tavily.com"
)

@st.cache_resource
def get_vector_store():
    return load_vector_store()

vector_store = get_vector_store()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("e.g. Do I need a permit to cross Rohtang Pass to Spiti?")

if question:
    if not groq_key or not tavily_key:
        st.warning("Please enter both API keys in the sidebar first.")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Checking sources..."):
                answer, source_type, sources = ask(question, groq_key, tavily_key)

            st.markdown(answer)

            badge = {
                "local": "📚 Local knowledge base",
                "web": "🌐 Live web search",
                "general_knowledge": "🧠 General knowledge (no source found)",
                "off_topic": "🚫 Off-topic — declined",
            }.get(source_type, source_type)
            st.caption(f"Source: {badge}")

            with st.expander("View sources used"):
                if source_type == "local":
                    for doc in sources:
                        source_name = os.path.basename(doc.metadata.get("source", "unknown"))
                        st.markdown(f"**{source_name}**")
                        st.text(doc.page_content)
                        st.divider()
                elif source_type == "web":
                    for r in sources:
                        st.markdown(f"**[{r.get('title', 'Untitled')}]({r.get('url', '')})**")
                        st.text(r.get("content", "")[:300])
                        st.divider()
                else:
                    st.text("No specific sources — answered from general knowledge.")

        st.session_state.messages.append({"role": "assistant", "content": answer})