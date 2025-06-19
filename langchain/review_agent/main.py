from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from db import get_review, setup_chroma_if_needed
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

import os

load_dotenv()
setup_chroma_if_needed()

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request format


class QueryRequest(BaseModel):
    question: str


@app.post("/ask")
async def ask_question(data: QueryRequest):
    q = data.question
    db_data = get_review([q])
    docs = db_data["documents"][0]
    review_text = "\n".join(docs)

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("API_KEY"),
        temperature=0,
    )

    template = """
    You are an expert in answering questions about a pizza restaurant.

    Here are some relevant reviews:
    {reviews}

    Here is the question to answer:
    {question}
    """

    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm

    response = chain.invoke({"reviews": review_text, "question": q})
    return {"answer": response.content}
