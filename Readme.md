# 📄 SmartPDF Assistant
### AI-Powered PDF Summariser and Question Answering System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![LangChain](https://img.shields.io/badge/LangChain-Powered-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

> Upload any PDF and instantly get a comprehensive summary plus ask unlimited questions about its content — powered by free AI tools.

🔗 **Live Demo:** [Click here to try it](https://smartpdf-assistant-ievdhvfdkrhry572jjkqej.streamlit.app/)
---

## 📌 Problem Statement

Reading long PDFs is time consuming. Students, researchers, and professionals waste hours:
- Reading entire documents just to find one answer
- Struggling to summarise lengthy reports
- Missing key information buried deep in documents

SmartPDF Assistant solves this — upload your PDF and get answers in seconds.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📝 Auto Summary | Generates structured summary with key points instantly |
| 💬 Smart Q&A | Ask any question and get detailed answers from the PDF |
| 📚 Source Citations | See exactly which part of the PDF the answer came from |
| ⚡ Fast Responses | Powered by Groq LLaMA3 — answers in 2-4 seconds |
| 🎨 Beautiful UI | Clean, professional interface with chat history |
| 📊 Session Stats | Tracks questions asked and average response time |

---

## 🏗️ How It Works
User uploads PDF

↓

PDF loaded and split into chunks (800 tokens each)

↓

Chunks converted to embeddings 

↓

Embeddings stored in FAISS vector database

↓

User asks question

↓

Top 6 relevant chunks retrieved from FAISS

↓

Groq LLaMA3 generates answer using retrieved chunks

↓

Answer + Source citations shown to user

---

## 🧰 Tech Stack

| Tool | Purpose |
|---|---|
| 🦜 LangChain | Document loading, text splitting, retrieval |
| 🧠 Groq + LLaMA3 | Free, fast LLM for summarisation and Q&A |
| 🗃️ FAISS | Lightweight vector database for storing embeddings |
| 🤗 HuggingFace | Sentence embeddings (all-MiniLM-L6-v2) |
| 🖥️ Streamlit | Beautiful web UI with chat interface |
| 🐍 Python 3.10 | Core language |

---

## 📁 Project Structure
smartpdf-assistant/

├── app.py                  # Main Streamlit app

├── .env                    # API keys (not uploaded to GitHub)

├── .gitignore              # Keeps secrets safe

└── requirements.txt        # All dependencies

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/kaursunainapreet-lgtm/smartpdf-assistant.git
cd smartpdf-assistant
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
Create a `.env` file and add:
GROQ_API_KEY=your_groq_api_key

Get your free Groq API key from: https://console.groq.com

### 5. Run the app
```bash
streamlit run app.py
```

---

## 💡 Example Use Cases

- 📖 **Students** — Summarise textbooks and research papers instantly
- 📋 **Job seekers** — Extract key points from company documents
- 🏛️ **Government documents** — Understand complex policies easily
- 📊 **Research** — Ask questions about research papers
- 📝 **Reports** — Get quick summaries of lengthy business reports

---

## 💬 Example Questions to Ask

- *"What are the key benefits mentioned in this document?"*
- *"Summarise the main findings of this report"*
- *"What are the eligibility criteria mentioned?"*
- *"What is the conclusion of this document?"*
- *"List all important dates mentioned"*

---

## 📊 Performance

- ⚡ Average response time: **2-4 seconds**
- 📄 Supports PDFs of any size
- 🔍 Retrieves top 6 most relevant chunks per question
- 💬 Unlimited questions per session

---

## 🔮 Future Improvements

- [ ] Support for multiple PDFs simultaneously
- [ ] Export summary as PDF or Word document
- [ ] Support for Hindi and Punjabi language PDFs
- [ ] Voice input for questions
- [ ] Email summary feature

---

## 👩‍💻 Built By

**Sunainapreet Kaur**
Student, Khalsa College
📧 kaursunainapreet@gmail.com
🐙 [GitHub](https://github.com/kaursunainapreet-lgtm)

### 🔗 My Other Projects
- 🎓 [Indian Scholarship Assistant](https://github.com/kaursunainapreet-lgtm/scholarship-assistant) — Agentic RAG with LangGraph and Safety Guardrails

---

## 📄 License

MIT License — free to use and modify.

---

⭐ **If this project helped you, please give it a star on GitHub!**

