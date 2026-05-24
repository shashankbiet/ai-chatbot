from functools import partial
from typing import Annotated, TypedDict

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph

CHAT_NODE = "chat_node"


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


class Chatbot:
    @staticmethod
    def chat_node(state: ChatState, chat_model: BaseChatModel) -> ChatState:
        messages = state["messages"]
        response = chat_model.invoke(messages)
        return {"messages": [response]}

    @staticmethod
    def build_chatbot_workflow(chat_model: BaseChatModel) -> CompiledStateGraph:
        checkpointer = MemorySaver()
        graph = StateGraph(ChatState)

        graph.add_node(CHAT_NODE, partial(Chatbot.chat_node, chat_model=chat_model))

        graph.add_edge(START, CHAT_NODE)
        graph.add_edge(CHAT_NODE, END)

        return graph.compile(checkpointer=checkpointer)
