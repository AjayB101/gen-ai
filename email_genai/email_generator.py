from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from markdown import markdown

llm = ChatGroq(model="llama-3.1-8b-instant", api_key="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", temperature=0)

template = """
### JOB DESCRIPTION:
{job_description}

### INSTRUCTION:
You are Mohan, a business development executive at AtliQ. AtliQ is an AI & Software Consulting company dedicated to facilitating
the seamless integration of business processes through automated tools. 
Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
process optimization, cost reduction, and heightened overall efficiency. 
Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ 
in fulfilling their needs.
Also add the most relevant ones from the following links to showcase Atliq's portfolio: {link_list}
Remember you are Mohan, BDE at AtliQ. 
Do not provide a preamble.
### EMAIL (NO PREAMBLE):
"""

prompt_email = PromptTemplate.from_template(template)
email_chain = prompt_email | llm

def generate_email(job_desc, links):
    res = email_chain.invoke({"job_description": job_desc, "link_list": links})
    return markdown(res.content)