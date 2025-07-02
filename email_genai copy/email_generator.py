from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from markdown import markdown
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

template = """
You are a helpful assistant who writes professional, concise referral request messages to employees at companies.

Page content: {page_content}

Generate a short message that:
– is polite and professional  
– clearly mentions the role title, company name, job ID (if available), and location if mentioned
– mentions being connected to the company
– asks for a referral without sounding pushy  
– mentions attaching resume
– ends with a thank-you and a friendly closing
My name is Ajay B.

Example
Hi,
I hope you're doing well! I'm interested in the Software Engineer JOB ID:=45888 role at Honey well
and saw you're connected to the company. I'd really appreciate it if you could refer me for this position. 
I've attached my resume for reference.
Thanks so much for your time and support!
Best regards,
Ajay B

**Instructions:**
- Extract the job title, company name, job ID, and location from the page content
- If no job ID is found, write "JOB ID: [Job ID]" as placeholder
- If no location is found, just use company name without location
- Keep the message concise and exactly match the format above
- Do not add extra details about job requirements or responsibilities
- Keep it short and to the point
- dont forget to add job title, company name, job ID, and location if available

No preamble or additional text, just the message in the exact format specified above.
"""

prompt = PromptTemplate(input_variables=["jd"], template=template)
email_chain = prompt | llm


def generate_message(page_content: str):
    res = email_chain.invoke({"page_content": page_content})
    print(res.content)
    return res.content

    # return markdown(res.content)
