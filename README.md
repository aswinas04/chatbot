# Python Book Chatbot 🐍

Unga Python books-a (PDF) base panni question-answer kudukkura AI chatbot.
LlamaIndex + LangChain + ChromaDB + Groq (free AI) + Streamlit.

---

## 📁 Folder Structure

```
python-book-chatbot/
├── app.py              # Main chatbot code
├── requirements.txt    # Libraries list
├── .env.example         # API key template
├── books/               # Unga PDF books inga podunga
└── chroma_db/           # Auto-create aagum (vector database storage)
```

---

## 🚀 Setup Steps (VS Code-la)

### Step 1: Project folder VS Code-la open pannunga

VS Code open pannunga → `File > Open Folder` → `python-book-chatbot` folder select pannunga.

### Step 2: Virtual environment create pannunga (recommended)

VS Code-la Terminal open pannunga (`Ctrl + ~` / `` Ctrl + ` ``), idha run pannunga:

```bash
python3 -m venv venv
source venv/bin/activate
```

(Linux/Mac command idhu. Terminal-la `(venv)` kaata venum, activate aana mark.)

### Step 3: Libraries install pannunga

```bash
pip install -r requirements.txt
```

Idhu konjam time edukum (especially `sentence-transformers`, `chromadb` - heavy libraries).

### Step 4: API Key Setup

`.env.example` file-a copy panni `.env` nu rename pannunga:

```bash
cp .env.example .env
```

`.env` file open panni, unga Groq API key-a podunga:

```
GROQ_API_KEY=gsk_unga_actual_key_inga
```

### Step 5: Unga Python Books-a `books/` folder-la podunga

PDF files-a `books/` folder-ku copy pannunga. Example:
```
books/
├── python_basics.pdf
├── data_structures.pdf
└── advanced_python.pdf
```

### Step 6: App Run Pannunga

```bash
streamlit run app.py
```

Idhu automatic ah browser-la open aagum (`http://localhost:8501`). Illana, terminal-la kaattura URL-a copy panni browser-la paste pannunga.

**First time run aagumbodhu** - books-a padichu index build panna konjam time edukum (book size depend panni 1-5 minutes). Apparam fast ah varum (already saved index use pannum).

---

## 💬 Eppadi Use Pannanum

1. Browser-la chatbot open aagum
2. Kelvi type pannunga (example: "What is a list comprehension in Python?")
3. AI unga books-la irundhu relevant answer kudukum

---

## ☁️ Online-la Free ah Deploy Pannurathu (Streamlit Cloud)

1. Unga code-a GitHub-la oru repository ah push pannunga (`books/` folder-oda PDFs kooda include pannunga, illana `.env` file mattum **podaadheenga** - API key leak aagidum)
2. https://share.streamlit.io po, GitHub account-oda login pannunga
3. "New app" click pannunga, unga repository select pannunga
4. `app.py` ah main file ah select pannunga
5. **Settings → Secrets** section-la, idha add pannunga:
   ```
   GROQ_API_KEY = "gsk_unga_actual_key"
   ```
6. Deploy click pannunga - 2-3 minutes-la live aagum, free public URL kidaikum

---

## ⚠️ Important Notes

- `.env` file-a **GitHub-ku push pannadheenga** (API key safety). `.gitignore` file-la `.env` add pannunga.
- Books pெரிய ah irundha (100+ pages), first-time indexing konjam time edukum - patience venum.
- Groq free tier-ku rate limits irukku (per minute requests). Romba fast ah multiple questions kekka, konjam wait pannanum varalam.
- Chat history clear panna venum na, sidebar-la "Chat History Clear Pannu" button click pannunga.

---

## 🔧 Common Errors & Fix

| Error | Fix |
|---|---|
| `GROQ_API_KEY kidaikala` | `.env` file create pannitinga nu check pannunga |
| `books folder-la PDF illa` | `books/` folder-la PDF irukka nu check pannunga |
| Slow first response | Normal - first time embedding model download aagum (~100MB) |
| `ModuleNotFoundError` | `pip install -r requirements.txt` again run pannunga, venv activate aana check pannunga |
