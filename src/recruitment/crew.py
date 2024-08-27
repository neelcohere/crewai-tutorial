# ../src/project/crew.py

import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from recruitment.tools.linkedin import LinkedinTool
from langchain_cohere import ChatCohere

from dotenv import load_dotenv
load_dotenv()


llm = ChatCohere(
    cohere_api_key=os.getenv("COHERE_API_KEY"),
    model="command-r-plus"
)


@CrewBase
class RecruitmentCrew():
    """Recruitment crew"""
    agents_config = "config/agents.yaml"
    tools_config = "config/tools.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[SerperDevTool(), ScrapeWebsiteTool(), LinkedinTool()],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def matcher(self) -> Agent:
        return Agent(
            config=self.agents_config["matcher"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
            verbose=True,
        )
    
    @agent
    def communicator(self) -> Agent:
        return Agent(
            config=self.agents_config["communicator"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['reporter'],
            allow_delegation=False,
            verbose=True,
        )

    @task
    def research_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_candidates_task"],
            agent=self.researcher(),
        )
    
    @task
    def match_and_score_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config["match_and_score_candidates_task"],
            agent=self.matcher(),
        )
    
    @task
    def outreach_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config["outreach_strategy_task"],
            agent=self.communicator()
        )
    
    @task
    def report_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config["report_candidates_task"],
            agent=self.reporter(),
            context=[
                self.research_candidates_task(), 
                self.match_and_score_candidates_task(), 
                self.outreach_strategy_task()
            ],
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the recruitment crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
