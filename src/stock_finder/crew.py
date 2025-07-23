from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from pydantic import BaseModel, Field
from typing import List 
from .tools.custom_tool import PushoverNotificationTool


# defines the parameters to be present mandatorily for each finding
class TrendingCompany(BaseModel):
    """
    Defines the parameters to be considered for each trending company found
    (Obligatory)
    The researched trending companies should have a stock ticker
    """
    name : str = Field(description = 'The name of the company')
    ticker : str  = Field(description = 'The stock ticker symbol')
    reason : str = Field(description = 'Reason this company is trending in the news')

class TrendingCompanyList(BaseModel):
    """
    List of multiple trending companies found in the news
    Format of the list to be strictly followed as per the defined custom pydantic class
    """
    companies : List[TrendingCompany] = Field(description = "List of companies trending in the news")

class TrendingCompanyResearch(BaseModel):
    """" Detailed research on a company with defined parameters (obligatory)"""
    name: str = Field(description="Company name")
    market_position: str = Field(description="Current market position and competitive analysis")
    future_outlook: str = Field(description="Future outlook and growth prospects")
    investment_potential: str = Field(description="Investment potential and suitability for investment")
    

class TrendingCompanyResearchList(BaseModel):
    """
    A detailed and concise report analyzing the trending companies
    Format of the list to be strictly followed as per the defined custom pydantic class
    """
    research_list : List[TrendingCompanyResearch] = Field(description = 'Comprehensive research on all trending companies')

@CrewBase
class StockFinder():
    """StockFinder crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(
            config = self.agents_config['trending_company_finder'],
            tools = [SerperDevTool()],
            memory = True
        )
    
    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config = self.agents_config['financial_researcher'],
            tools = [SerperDevTool()]
        )
    
    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config = self.agents_config['stock_picker'],
            tools = [PushoverNotificationTool()],
            memory = True
        )
    
    @task 
    def find_trending_companies(self) -> Task:
        return Task(
            config = self.tasks_config['find_trending_companies'],
            output_pydantic = TrendingCompanyList,
        )
    
    @task 
    def research_trending_companies(self) -> Task:
        return Task(
            config = self.tasks_config['research_trending_companies'],
            output_pydantic = TrendingCompanyResearchList,
        )
    
    @task 
    def pick_best_company(self) -> Task:
        return Task(
            config = self.tasks_config['pick_best_company']
        )

    @crew
    def crew(self) -> Crew:
        """
        Defines the entire stock picker crew consisting of agents and their tasks and tools
        All the hierarchical tasks managed by the manager agent
        """
        manager = Agent(
            config = self.agents_config['manager'],
            allow_delegation = True,
        )
        
        short_term_memory = ShortTermMemory(
            storage = RAGStorage(
                embedder_config = {
                    'provider' : 'huggingface',
                    'config' : {
                        'model' : 'sentence-transformers/paraphrase-MiniLM-L3-v2'
                    }
                },
                type = 'short_term',
                path = './memory/' 
            )
        )
        long_term_memory = LongTermMemory(
            storage = LTMSQLiteStorage(
                db_path = './memory/long_term_memory_storage.db'
            )
        )
        entity_memory = EntityMemory(
            storage = RAGStorage(
                embedder_config = {
                    'provider' : 'huggingface',
                    'config' : {
                        'model' : 'sentence-transformers/paraphrase-MiniLM-L3-v2'
                    }
                },
                type = 'short_term',
                path = './memory/' 
            )
        )
        
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory = True,
            long_term_memory = long_term_memory,
            short_term_memory = short_term_memory,
            entity_memory = entity_memory
        )
    