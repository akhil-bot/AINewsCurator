import json
import ast
from langgraph.graph import StateGraph, END, START
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage
from models.openai_models import get_open_ai_json
# from langgraph.checkpoint.sqlite import SqliteSaver
from agents.Agents import (
    NewsSearcher,
    Summarizer,
    Publisher,
    EndNodeAgent
)
from states.state import AgentGraphState

def create_graph(server=None, model=None, stop=None, model_endpoint=None, temperature=0):
    graph = StateGraph(AgentGraphState)

    graph.add_node(
        "news_searcher", 
        lambda state: NewsSearcher(
            state=state,
            model=model,
            server=server,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            query=state["query"],
        )
    )

    graph.add_node(
        "summarizer",
        lambda state: Summarizer(
            state=state,
            model=model,
            server=server,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
        )
    )

    graph.add_node(
        "publisher",
        lambda state: Publisher(
            state=state,
            model=model,
            server=server,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
        )
    )


    graph.add_node("end", lambda state: EndNodeAgent(state).invoke())


    # Add edges to the graph
    graph.set_entry_point("news_searcher")
    graph.set_finish_point("end")
    graph.add_edge("news_searcher", "summarizer")
    graph.add_edge("summarizer", "publisher")
    graph.add_edge("publisher", "end")


    return graph

def compile_workflow(graph):
    workflow = graph.compile()
    app = workflow
    from IPython.display import Image, display

    # display(Image(app.get_graph(xray=True).draw_mermaid_png()))
    return app
