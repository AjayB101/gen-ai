import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


class Agent:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")

    def get_agent(self):
        llm = ChatGroq(model="llama-3.1-8b-instant",
                       api_key=self.api_key, temperature=0)
        return llm
