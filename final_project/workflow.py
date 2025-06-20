from re import split
from typing import Dict, Any
import firecrawl
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from model import ResearchState, CompanyInfo, CompanyAnalysis
from firecrwal_service import FireCrawlService
from prompt import DeveloperToolsPrompts
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv


class Workflow:
    def __init__(self):
        load_dotenv()
        self.llm = ChatGroq(model="llama-3.1-8b-instant",
                            temperature=0)
        self.firecrawl = FireCrawlService()
        self.prompt = DeveloperToolsPrompts()

    def init_work_flow(self):
        graph = StateGraph(ResearchState)
        graph.add_node("get_tools", self.get_tools)
        graph.add_node("research", self.research)
        graph.set_entry_point("get_tools")
        graph.add_edge("get_tools", "research")
        graph.add_edge("research", END)
        app = graph.compile()
        app.invoke({"query": "Python"})

    def get_tools(self, state: ResearchState) -> Dict[str, Any]:
        search_query = f"{state.query} alternative"
        res = self.firecrawl.search(search_query, n_res=3)
        print(res)
        content = ""
        tool_name = []
        if res and hasattr(res, "data"):
            for doc in res.data:
                url = doc.get("url", "")
                cont = self.firecrawl.scrape(url)
                if cont and cont.markdown:
                    content += cont.markdown[:1500] + "\n\n"
                messages = [
                    SystemMessage(content=self.prompt.TOOL_EXTRACTION_SYSTEM),
                    HumanMessage(
                        content=self.prompt.tool_extraction_user(search_query, content))
                ]
                response = self.llm.invoke(messages)
                print(response)
                if isinstance(response.content, list):
                    tool_name = [
                        name.strip() for name in response.content
                        if isinstance(name, str) and name.strip()
                    ]
                else:
                    tool_name = [
                        name.strip() for name in str(response.content).strip().split("\n")
                        if name.strip()
                    ]
                print(tool_name)
                # Return after processing the first doc as in original logic
                return {"extracted_tools": tool_name}
        # If no data or nothing processed, return empty list
        return {"extracted_tools": tool_name}

    def analyse_company(self, company_name, content) -> CompanyAnalysis:
        structured_llm = self.llm.with_structured_output(CompanyAnalysis)

        messages = [
            SystemMessage(content=self.prompt.TOOL_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompt.tool_analysis_user(
                company_name, content)),
        ]

        try:
            analysis = structured_llm.invoke(messages)
            if not isinstance(analysis, CompanyAnalysis):
                if isinstance(analysis, dict):
                    # Ensure all required fields are present, provide defaults if missing
                    analysis_dict = {
                        "pricing_model": analysis.get("pricing_model", "Unknown"),
                        "is_open_source": analysis.get("is_open_source", None),
                        "tech_stack": analysis.get("tech_stack", []),
                        "description": analysis.get("description", "Failed"),
                        "api_available": analysis.get("api_available", None),
                        "language_support": analysis.get("language_support", []),
                        "integration_capabilities": analysis.get("integration_capabilities", []),
                    }
                    analysis = CompanyAnalysis(**analysis_dict)
                else:
                    # If analysis is not a dict, return a default CompanyAnalysis
                    analysis = CompanyAnalysis(
                        pricing_model="Unknown",
                        is_open_source=None,
                        tech_stack=[],
                        description="Failed",
                        api_available=None,
                        language_support=[],
                        integration_capabilities=[],
                    )
            return analysis
        except Exception as e:
            print(e)
            return CompanyAnalysis(
                pricing_model="Unknown",
                is_open_source=None,
                tech_stack=[],
                description="Failed",
                api_available=None,
                language_support=[],
                integration_capabilities=[],
            )

    def research(self, state: ResearchState) -> Dict[str, Any]:
        extracted_tools = state.extracted_tools
        companies = []

        for tool in extracted_tools:
            search_query = f"{tool} Official site"
            search_res = self.firecrawl.search(search_query, n_res=1)

            if not search_res or not search_res.data:
                continue

            tool_search_res = search_res.data[0]
            url = tool_search_res.get("url", "")
            company = CompanyInfo(
                name=tool,
                description=tool_search_res.get("markdown", ""),
                website=url,
                tech_stack=[],
                competitors=[]
            )

            if url:
                scraped = self.firecrawl.scrape(url)
                if scraped and scraped.markdown:
                    content = scraped.markdown
                    analysis = self.analyse_company(company.name, content)
                    company.pricing_model = analysis.pricing_model
                    company.is_open_source = analysis.is_open_source
                    company.tech_stack = analysis.tech_stack
                    company.description = analysis.description
                    company.api_available = analysis.api_available
                    company.language_support = analysis.language_support
                    company.integration_capabilities = analysis.integration_capabilities

            companies.append(company)

        # Return updated state
        return {"companies": companies}


if __name__ == "__main__":

    wf = Workflow()  # Create dummy ResearchState if needed
    # Ensure it takes no required args or provide them

    wf.init_work_flow()
