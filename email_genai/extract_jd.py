from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

llm = ChatGroq(model="llama-3.1-8b-instant", api_key="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", temperature=0)

class JD(BaseModel):
    role: str = Field(description="Role of the job")
    experience: int = Field(description="experience needed for the job in years")
    skills: list[str] = Field(description="skills required of the job")

parser = JsonOutputParser(pydantic_object=JD)

template = """
You are an intelligent extraction agent.

{format}

Here is the job description:
{job_description}

Only return a valid JSON response. Do not include any explanation or extra text.
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["job_description"],
    partial_variables={"format": parser.get_format_instructions()},
)


chain = prompt | llm | parser

def extract_job_details(url, return_json=False):
    loader = WebBaseLoader(url)
    doc = loader.load().pop().page_content
    result = chain.invoke({"job_description": doc})
    print(result)
    return result if return_json else doc