import yaml
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from src.tools import SearchPdfTool
import json
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import requests
from unstructured.partition.html import partition_html


# the next tool uses the serper api to search the internet - serper api costs money
class SearchToolInput(BaseModel):
    """Input Schema for SearchTool with Serper Api."""""
    query: str = Field(..., description="The query which helps to do the internet search.")

class SearchToolInternet(BaseTool):
    name: str = "SearchToolInternet"
    description: str = "Search the internet relevant data about the query."
    args_schema: Type[BaseModel] = SearchToolInput

    def _run(self, query: str) -> str:
        """Search the internet for specific query"""
        top_result_to_return = 1
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': "884f4e4408448bda7dca60e6c8ed554e0859c59d",
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        # check if there is an organic key
        if 'organic' not in response.json():
            return "Sorry, I couldn't find anything about that, there could be an error with you serper api key."
        else:
            results = response.json()['organic']
            string = []
            for result in results[:top_result_to_return]:
                try:
                    string.append('\n'.join([
                        f"Title: {result['title']}", f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}", "\n-----------------"
                    ]))
                except KeyError:
                    next
            return '\n'.join(string)

class BrowserToolInput(BaseModel):
    """Input Schema for BrowserTool with Browserless.io Api."""
    website :str = Field(...,description="The website that we browse.")

class BrowserTool(BaseTool):
    name: str = "BrowserTool"
    description: str = "Browse the website"
    args_schema: Type[BaseModel]=BrowserToolInput
    def _run(self, website: str) -> str:
        url = f"https://chrome.browserless.io/content?token=Ry1BtFad2muSTm6797200961b45a20a3bd162b2cef"
        payload = json.dumps({"url": website})
        headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        elements = partition_html(text=response.text)
        content = "\n\n".join([str(el) for el in elements])
        content = [content[i:i + 1000] for i in range(0, len(content), 1000)]
        summaries = []
        for chunk in content:
            agent = Agent(
                role='Principal Researcher',
                goal=
                'Do amazing researches and summaries based on the content you are working with',
                backstory=
                "You're a Principal Researcher at a big company and you need to do a research about a given topic.",
                allow_delegation=False,
                verbose=False)
            task = Task(
                agent=agent,
                description=
                f'Analyze and summarize the content bellow, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
            )
            summary = task.execute()
            summaries.append(summary)
        return "\n".join(summaries)

browser_tool = BrowserTool()
web_content = browser_tool._run("https://tripsplanner.pro/business/")
print(web_content)

class AgenticWorkflow:
    def __init__(self):
        self.agents_config = self._load_yaml('config/agents.yaml')
        self.tasks_config = self._load_yaml('config/tasks.yaml')
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        self.llm_strict = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def _load_yaml(self, path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def run(self, query: str, chat_history: str):
        # you have to instantiate your custom tools before using them
        search_tool = SearchPdfTool()
        search_tool_interent = SearchToolInternet()
        # 2. Create Agents
        researcher = Agent(
            role=self.agents_config['researcher']['role'],
            goal=self.agents_config['researcher']['goal'],
            backstory=self.agents_config['researcher']['backstory'],
            tools=[search_tool, search_tool_interent],  # Injecting your tool instance
            llm=self.llm_strict,
            verbose=True,
            allow_delegation=False
        )
        
        strategist = Agent(
            role=self.agents_config['strategist']['role'],
            goal=self.agents_config['strategist']['goal'],
            backstory=self.agents_config['strategist']['backstory'],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        # 3. Create Tasks
        task_research = Task(
            description=self.tasks_config['research_task']['description'].format(query=query),
            expected_output=self.tasks_config['research_task']['expected_output'],
            agent=researcher
        )

        task_answer = Task(
            description=self.tasks_config['answer_task']['description'].format(
                query=query, 
                chat_history=chat_history
            ),
            expected_output=self.tasks_config['answer_task']['expected_output'],
            agent=strategist,
            context=[task_research]
        )

        # 4. Kickoff
        crew = Crew(
            agents=[researcher, strategist],
            tasks=[task_research, task_answer],
            process=Process.sequential
        )

        return str(crew.kickoff())
