# Python Book Chatbot 🐍

A RAG (Retrieval Augmented Generation) chatbot that reads your Python PDF book and answers questions based on its exact content. Built with LlamaIndex, ChromaDB, Groq (free AI), and Streamlit.

---

## How It Works

1. Your PDF book is loaded from the `books/` folder
2. The text is split into chunks and stored as vector embeddings in ChromaDB
3. When you ask a question, the most relevant chunks are retrieved
4. Those chunks + your question are sent to Groq's free AI model
5. The AI answers based strictly on your book's content

---

## Project Structure

```
python-book-chatbot/
├── app.py                  # Main application (core logic ~70 lines)
├── styles.css              # All UI styling (glassmorphism theme)
├── requirements.txt        # Python dependencies
├── .env                    # Your API key (not shared/uploaded)
├── books/                  # Put your PDF books here
│   └── Python_Beginners_Guide.pdf
└── chroma_db/              # Auto-created vector database (local storage)
```

---

## APIs and Libraries Used

| Tool | Purpose |
|---|---|
| **Groq API** (`llama-3.1-8b-instant`) | Free AI model for generating answers |
| **HuggingFace Embedding** (`BAAI/bge-small-en-v1.5`) | Converts text to vectors (runs locally, no API key needed) |
| **LlamaIndex** | PDF loading, chunking, indexing, RAG pipeline |
| **ChromaDB** | Local vector database for storing and searching embeddings |
| **Streamlit** | Web UI framework |
| **python-dotenv** | Loads API key from `.env` file safely |

> Only **one API key** is required: your Groq API key (free at console.groq.com)

---

## Setup Instructions

### Step 1: Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Add Your Groq API Key

Create a `.env` file in the project folder:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

Get a free key at: https://console.groq.com

### Step 4: Add Your PDF Book

```bash
cp ~/Downloads/Python_Beginners_Guide.pdf books/
```

### Step 5: Run the App

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`. First run takes 1-3 minutes to index the book.

---

## Key Features

- **Book-accurate answers** — AI uses only your book's content, never guesses
- **Chapter lookup** — Type "Chapter 5" to get the full chapter content directly
- **Multi-chat sessions** — Gemini-style Recents sidebar, independent memory per chat
- **Friend-like tone** — Casual, warm responses
- **Glassmorphism UI** — Soft gradient background, frosted-glass panels

---

## Resetting the Index

If you replace your PDF, delete the old index first:

```bash
rm -rf chroma_db
streamlit run app.py
```

---

## Rate Limits

Groq's free tier: **6,000 tokens/minute**. If you hit the limit, wait ~60 seconds. For unlimited usage: https://console.groq.com/settings/billing

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `GROQ_API_KEY missing` | Check `.env` file has the correct key |
| `No PDFs found in books/` | Make sure PDF is inside `books/` folder |
| Rate limit error (413) | Wait 60 seconds, then retry |
| Old book content showing | Run `rm -rf chroma_db` then restart |
| Slow first run | Normal — embedding model downloads once (~100MB) |