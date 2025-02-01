import os
from states import state
from termcolor import colored
from models.openai_models import get_open_ai, get_open_ai_json
from models.ollama_models import OllamaModel, OllamaJSONModel
from models.vllm_models import VllmJSONModel, VllmModel
from models.groq_models import GroqModel, GroqJSONModel
from models.claude_models import ClaudModel, ClaudJSONModel
from models.gemini_models import GeminiModel, GeminiJSONModel
from states.state import AgentGraphState, Article, Summary
from prompts.prompts import Prompts
from tavily import TavilyClient
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict, List, Any, TypedDict, Optional
from datetime import datetime




tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

prompts = Prompts()

class Agent:
    def __init__(self, state: AgentGraphState, model=None, server=None, temperature=0, model_endpoint=None, stop=None,
                 guided_json=None):
        self.state = state
        self.model = model
        self.server = server
        self.temperature = temperature
        self.model_endpoint = model_endpoint
        self.stop = stop
        self.guided_json = guided_json

    def get_llm(self, json_model=True):
        if self.server == 'openai':
            return get_open_ai_json(model=self.model, temperature=self.temperature) if json_model else get_open_ai(
                model=self.model, temperature=self.temperature)
        if self.server == 'ollama':
            return OllamaJSONModel(model=self.model, temperature=self.temperature) if json_model else OllamaModel(
                model=self.model, temperature=self.temperature)
        if self.server == 'vllm':
            return VllmJSONModel(
                model=self.model,
                guided_json=self.guided_json,
                stop=self.stop,
                model_endpoint=self.model_endpoint,
                temperature=self.temperature
            ) if json_model else VllmModel(
                model=self.model,
                model_endpoint=self.model_endpoint,
                stop=self.stop,
                temperature=self.temperature
            )
        if self.server == 'groq':
            return GroqJSONModel(
                model=self.model,
                temperature=self.temperature
            ) if json_model else GroqModel(
                model=self.model,
                temperature=self.temperature
            )
        if self.server == 'claude':
            return ClaudJSONModel(
                model=self.model,
                temperature=self.temperature
            ) if json_model else ClaudModel(
                model=self.model,
                temperature=self.temperature
            )
        if self.server == 'gemini':
            return GeminiJSONModel(
                model=self.model,
                temperature=self.temperature
            ) if json_model else GeminiModel(
                model=self.model,
                temperature=self.temperature
            )

    def update_state(self, key, value):
        self.state = {**self.state, key: value}

class PromptWriterAgent(Agent):
    def invoke(self, task, prompt="", feedback=None):

        prompt_writer_prompt = prompts.prompt_writer_prompt.format(
            )

        messages = [
            {"role": "system", "content": prompt_writer_prompt},
            {"role": "user", "content": f"Task, Goal, or Current Prompt:\n{task}"}
        ]

        llm = self.get_llm(json_model=False)
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        self.update_state("prompt_writer_response", response)
        print(colored(f"PromptWriter 👩🏿‍💻: {response}", 'cyan'))
        return self.state
    

class PromptReviewerAgent(Agent):
    def invoke(self, task="", prompt_writer_response="", prompt="", feedback=None):
        print(f"Task: {task}")
        print(f"PromptWriterResponse: {prompt_writer_response}")
        print(f"Prompt: {prompt}")
        prompt_reviewer_prompt = prompts.prompt_reviewer_prompt.replace("{task}", task).replace("{promptGenerated}", prompt_writer_response[0].content)

        messages = [
            {"role": "system", "content": prompt_reviewer_prompt},
        ]

        llm = self.get_llm(json_model=False)
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        self.update_state("prompt_reviewer_response", response)
        print(colored(f"PromptReviewer 👩🏿‍💻: {response}", 'cyan'))
        return self.state

class EndNodeAgent(Agent):
    def invoke(self):
        self.update_state("end_chain", "end_chain")
        return self.state
    



class NewsSearcher(Agent):
    """
    Agent responsible for finding relevant AI/ML news articles
    using the Tavily search API
    """

    def invoke(self, query: str):
        """
        Performs news search with configured parameters

        Returns:
            List[Article]: Collection of found articles
        """
        response = tavily.search(
            query=query,
            topic="news",
            time_period="1w",
            search_depth="advanced",
            max_results=5
        )

        articles = []
        for result in response['results']:
            articles.append(Article(
                title=result['title'],
                url=result['url'],
                content=result['content']
            ))
        self.state['articles'] = articles
        return self.state



class Summarizer(Agent):
    """
    Agent that processes articles and generates accessible summaries
    using gpt-4o-mini
    """

    def summarize(self, article: Article):
        self.system_prompt = """
        You are an AI expert who makes complex topics accessible 
        to general audiences. Summarize this article in 2-3 sentences, focusing on the key points 
        and explaining any technical terms simply.
        """
        llm = self.get_llm(json_model=False)
        response = llm.invoke([
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"Title: {article.title}\n\nContent: {article.content}")
        ])
        return response.content


    def invoke(self):
        """
        Generates an accessible summary of a single article

        Args:
            article (Article): Article to summarize

        Returns:
            str: Generated summary
        """
        self.state['summaries'] = []

        for article in self.state['articles']:  # Uses articles from previous node
            summary = self.summarize(article)
            self.state['summaries'].append({
                'title': article.title,
                'summary': summary,
                'url': article.url
            })
        return self.state
        


class Publisher(Agent):
    """
    Agent that compiles summaries into a formatted report
    and saves it to disk
    """

    def invoke(self) -> str:
        """
        Creates and saves a formatted markdown report

        Args:
            summaries (List[Dict]): Collection of article summaries

        Returns:
            str: Generated report content
        """
        prompt = """
        Create a weekly AI/ML news report for the general public. 
        Format it with:
        1. A brief introduction
        2. The main news items with their summaries
        3. Links for further reading

        Make it engaging and accessible to non-technical readers. Use emojis wherever needed. And add a motivational quote at the end.
        """
        summaries = self.state['summaries']

        # Format summaries for the LLM
        summaries_text = "\n\n".join([
            f"Title: {item['title']}\nSummary: {item['summary']}\nSource: {item['url']}"
            for item in summaries
        ])

        llm = self.get_llm(json_model=False)

        # Generate report
        response = llm.invoke([
            SystemMessage(content=prompt),
            HumanMessage(content=summaries_text)
        ])

        # Add metadata and save
        current_date = datetime.now().strftime("%Y-%m-%d")
        markdown_content = f"""
        Generated on: {current_date}

        {response.content}
        """

        filename = f"ai_news_report_{current_date}.md"
        with open(filename, 'w') as f:
            f.write(markdown_content)
        
        report_content = response.content

        self.state['report'] = report_content
        return self.state
    
