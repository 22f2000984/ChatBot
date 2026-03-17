from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from google import genai
import os

# ── INIT ─────────────────────────────────────────────
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ── LOAD EMBEDDINGS + VECTOR DB ──────────────────────
embeddings = OpenAIEmbeddings()

db = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

# ── LOAD LLM ─────────────────────────────────────────
llm = ChatOpenAI(model="gpt-4o-mini")

# ── CORE FUNCTION ────────────────────────────────────
def get_answer(query: str) -> str:
    docs = db.similarity_search(query, k=3)

    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
You are a helpful assistant for a telecom company.

Answer clearly and professionally using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)

    return response.content


# ── ROUTES ───────────────────────────────────────────
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/ask")
def ask(q: str):
    try:
        answer = get_answer(q)
        return {"answer": answer}

    except Exception as e:
        print("ERROR:", str(e))
        return {"answer": f"Error: {str(e)}"}