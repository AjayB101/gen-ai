from langchain_core.prompts import PromptTemplate
import os
from langchain_groq import ChatGroq

from db import get_review, setup_chroma_if_needed
from dotenv import load_dotenv
load_dotenv()
setup_chroma_if_needed()
q = "Overrall rating"
db_data = get_review([q])
llm = ChatGroq(model="llama-3.1-8b-instant",
               api_key=os.getenv("API_KEY"), temperature=0)
template = """
You are an exeprt in answering questions about a pizza restaurant

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""
temp = PromptTemplate.from_template(template)
chain = temp | llm
res = chain.invoke({"reviews": db_data, "question": q})
print(res)
