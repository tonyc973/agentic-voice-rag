import streamlit as st
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

# Tool Input Schema
class SearchPdfToolInput(BaseModel):
    query: str = Field(..., description="The query string to search in the PDF")

# Tool Definition 
# go to https://docs.crewai.com/en/tools/ to find out more about creating tools in crewai 
# sky is the limit
class SearchPdfTool(BaseTool):
    name: str = "SearchPdfTool"
    description: str = "Tool used to search information in a PDF given a query"
    args_schema: Type[BaseModel] = SearchPdfToolInput

    def _run(self, query: str) -> str:
        # Accessing Streamlit session state directly
        if "vectorstore" in st.session_state and st.session_state.vectorstore:
            retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 4})
            docs = retriever.invoke(query)
            return "\n\n".join([d.page_content for d in docs])
        else:
            return "No PDF uploaded yet."
