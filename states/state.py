from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from typing import Dict, List, Any, TypedDict, Optional
from pydantic import BaseModel


class Article(BaseModel):
    """
    Represents a single news article

    Attributes:
        title (str): Article headline
        url (str): Source URL
        content (str): Article content
    """
    title: str
    url: str
    content: str


class Summary(TypedDict):
    """
    Represents a processed article summary

    Attributes:
        title (str): Original article title
        summary (str): Generated summary
        url (str): Source URL for reference
    """
    title: str
    summary: str
    url: str


# This defines what information we can store and pass between nodes later
class AgentGraphState(TypedDict):
    """
    Maintains workflow state between agents

    Attributes:
        articles (Optional[List[Article]]): Found articles
        summaries (Optional[List[Summary]]): Generated summaries
        report (Optional[str]): Final compiled report
    """
    query: str
    articles: Optional[List[Article]]
    summaries: Optional[List[Summary]]
    report: Optional[str]

# # Define the state object for the agent graph
# class AgentGraphState(TypedDict):
#     task: str
#     prompt_writer_response: Annotated[list, add_messages]
#     prompt_reviewer_response: Annotated[list, add_messages]


# # Define the nodes in the agent graph
# def get_agent_graph_state(state:AgentGraphState, state_key:str):
#     if state_key == "prompt_writer":
#         return state["prompt_writer_response"]
#     elif state_key == "prompt_reviewer":
#         return state["prompt_reviewer_response"]
#     else:
#         return None

    
# state = {
#     "task":"",
#     "prompt_writer_response": [],
#     "prompt_reviewer_response": [],
#     "end_chain": []
# }