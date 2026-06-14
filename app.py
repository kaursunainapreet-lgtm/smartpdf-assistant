import streamlit as st
import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(
    page_title="SmartPDF Assistant",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
    .header-box {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 28px 32px;
        border-radius: 16px;
        margin-bottom: 24px;
        color: white;
    }
    .header-box h1 { margin:0; font-size:30px; }
    .header-box p { margin:6px 0 0; opacity:0.85; font-size:14px; }
    .badge {
        display: inline-block;
        background: rgba(255,255,255,0.18);
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 12px;
        margin-right: 6px;
        margin-top: 10px;
    }
    .summary-box {
        background: #f0f7ff;
        border-left: 4px solid #2563eb;
        border-radius: 0 12px 12px 0;
        padding: 18px 22px;
        margin-top: 12px;
        font-size: 14px;
        line-height: 1.9;
        color: #1e3a5f;
    }
    .source-box {
        background: #f0fdf4;
        border-left: 4px solid #16a34a;
        border-radius: 0 8px 8px 0;
        padding: 10px 14px;
        margin-top: 8px;
        font-size: 12px;
        color: #14532d;
        line-height: 1.6;
    }
    .metric-box {
        background: white;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        border: 1px solid #e0e7ff;
        margin-bottom: 8px;
    }
    .metric-number { font-size: 22px; font-weight: bold; color: #2563eb; }
    .metric-label { font-size: 11px; color: #6b7280; margin-top: 2px; }
    .empty-state {
        text-align: center;
        padding: 60px 20px;
    }
    .stChatMessage { border-radius: 12px; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

# --- LLM ---
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)

# --- Session state ---
for key, val in {
    "vectorstore": None,
    "documents": [],
    "chat_history": [],
    "summary": None,
    "pdf_ready": False,
    "pdf_name": "",
    "total_questions": 0,
    "total_time": 0.0,
    "save_path": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- Process PDF ---
def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db_" + str(int(time.time()))
    )
    return vectorstore, documents
    # clear old db
    # clear old db
    import shutil
    import gc
    if "vectorstore" in st.session_state and st.session_state.vectorstore is not None:
        st.session_state.vectorstore = None
        gc.collect()
    if os.path.exists("chroma_db"):
        try:
            shutil.rmtree("chroma_db")
        except:
            pass
# --- Generate Summary ---
def generate_summary(documents):
    full_text = " ".join([doc.page_content for doc in documents[:8]])
    response = llm.invoke(f"""
You are an expert document analyst.
Read the document below and provide a comprehensive response with:

## 📋 Overview
Write 3-4 sentences summarising what this document is about.

## 🔑 Key Points
List 6-8 important points from the document as bullet points.

## 💡 Main Takeaway
Write 1-2 sentences about the most important conclusion.

Document:
{full_text[:4000]}
""")
    return response.content

# --- Answer Question ---
def answer_question(question, vectorstore):
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 6}
    )
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    sources = [doc.page_content[:250] for doc in docs[:3]]

    response = llm.invoke(f"""
You are a helpful and thorough document assistant.
Answer the question below using the context provided.
Give a detailed, clear answer with all relevant information from the context.
If the context has partial information, share what you found.
Only say you cannot find information if there is truly nothing relevant.

Context from document:
{context}

Question: {question}

Detailed Answer:
""")
    return response.content, sources

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 📄 SmartPDF Assistant")
    st.markdown("*Upload any PDF — instant summary + Q&A*")
    st.divider()

    st.markdown("### 📂 Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file is not None:
        save_path = os.path.join(".", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("⏳ Processing PDF..."):
            vectorstore, documents = process_pdf(save_path)
            st.session_state.vectorstore = vectorstore
            st.session_state.documents = documents
            st.session_state.pdf_ready = True
            st.session_state.pdf_name = uploaded_file.name
            st.session_state.save_path = save_path
            st.session_state.chat_history = []
            st.session_state.summary = None
            st.session_state.total_questions = 0
            st.session_state.total_time = 0.0

        st.success(f"✅ Ready! {len(documents)} pages loaded.")

    st.divider()

    st.markdown("### 📊 Session Stats")
    total_q = st.session_state.total_questions
    avg_time = round(st.session_state.total_time / total_q, 2) if total_q > 0 else 0

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="metric-box">
            <div class="metric-number">{total_q}</div>
            <div class="metric-label">Questions</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-box">
            <div class="metric-number">{avg_time}s</div>
            <div class="metric-label">Avg Time</div>
        </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("**⚙️ Powered By**")
    st.markdown("🧠 Groq LLaMA3 · 🗃️ ChromaDB · 🤗 HuggingFace · 🦜 LangChain")

    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.total_questions = 0
        st.session_state.total_time = 0.0
        st.rerun()

# --- MAIN ---
st.markdown("""
<div class="header-box">
    <h1>📄 SmartPDF Assistant</h1>
    <p>Upload any PDF — get an instant summary and ask unlimited questions about it</p>
    <span class="badge">📝 Auto Summary</span>
    <span class="badge">💬 Smart Q&A</span>
    <span class="badge">📚 Source Citations</span>
    <span class="badge">⚡ LLaMA3 Powered</span>
</div>
""", unsafe_allow_html=True)

if st.session_state.pdf_ready:
    st.markdown(f"**📂 Loaded:** `{st.session_state.pdf_name}` — {len(st.session_state.documents)} pages")
    st.divider()

    # Summary
    st.markdown("### 📝 Document Summary")
    if st.session_state.summary is None:
        if st.button("✨ Generate Summary", type="primary"):
            with st.spinner("📖 Reading and summarising..."):
                summary = generate_summary(st.session_state.documents)
                st.session_state.summary = summary
            st.rerun()
    
    if st.session_state.summary:
        st.markdown(f"""<div class="summary-box">{st.session_state.summary}</div>""",
                    unsafe_allow_html=True)

    st.divider()

    # Q&A
    st.markdown("### 💬 Ask Anything About This PDF")

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])
            if chat["role"] == "assistant" and chat.get("sources"):
                with st.expander("📚 View Sources"):
                    for i, src in enumerate(chat["sources"], 1):
                        st.markdown(f"""<div class="source-box">
                            <strong>Source {i}:</strong> {src}
                        </div>""", unsafe_allow_html=True)
            if chat["role"] == "assistant":
                st.caption(f"⏱️ {chat.get('response_time', '')}s")

    question = st.chat_input("Ask anything about your PDF — key points, details, comparisons...")

    if question:
        with st.chat_message("user"):
            st.markdown(question)
        st.session_state.chat_history.append({
            "role": "user", "content": question
        })

        with st.chat_message("assistant"):
            with st.spinner("🤔 Finding answer..."):
                start = time.time()
                answer, sources = answer_question(
                    question, st.session_state.vectorstore
                )
                response_time = round(time.time() - start, 2)

            st.markdown(answer)
            with st.expander("📚 View Sources"):
                for i, src in enumerate(sources, 1):
                    st.markdown(f"""<div class="source-box">
                        <strong>Source {i}:</strong> {src}
                    </div>""", unsafe_allow_html=True)
            st.caption(f"⏱️ {response_time}s")

        st.session_state.total_questions += 1
        st.session_state.total_time += response_time
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "response_time": response_time
        })

else:
    st.markdown("""
    <div class="empty-state">
        <div style="font-size:72px">📄</div>
        <h2 style="color:#0f2027;margin-top:12px">Upload a PDF to get started</h2>
        <p style="color:#6b7280;font-size:15px">Use the sidebar on the left to upload any PDF document</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.info("📝 Get automatic summary of any PDF")
        st.info("💬 Ask detailed questions about content")
    with c2:
        st.info("📚 See exact sources for every answer")
        st.info("⚡ Fast answers using free Groq LLaMA3")