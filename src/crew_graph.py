import yaml
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from src.tools import SearchPdfTool

class AgenticWorkflow:
    def __init__(self):
        self.agents_config = self._load_yaml('config/agents.yaml')
        self.tasks_config = self._load_yaml('config/tasks.yaml')
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        self.llm_strict = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def _load_yaml(self, path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def run(self, query: str, chat_history: str):
        # 1. Instantiate Your Tool
        search_tool = SearchPdfTool()

        # 2. Create Agents
        researcher = Agent(
            role=self.agents_config['researcher']['role'],
            goal=self.agents_config['researcher']['goal'],
            backstory=self.agents_config['researcher']['backstory'],
            tools=[search_tool],  # Injecting your tool instance
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