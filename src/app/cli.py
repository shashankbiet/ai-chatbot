from typing import Final

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from llm_factory import LLMFactory, Provider

from src.config import settings
from src.workflows import Chatbot

DEFAULT_THREAD_ID: Final = "1"
EXIT_COMMANDS: Final = {"exit", "quit", "bye"}


def get_chat_model() -> BaseChatModel:
    return LLMFactory.create_chat_model(
        provider=Provider.LMSTUDIO,
        model=settings.chat_model,
    )


def run_chat(thread_id: str = DEFAULT_THREAD_ID) -> None:
    chat_model = get_chat_model()
    chatbot_workflow = Chatbot.build_chatbot_workflow(chat_model)
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        user_message = input("Type here: ")
        if user_message.strip().lower() in EXIT_COMMANDS:
            break

        response = chatbot_workflow.invoke(
            {"messages": [HumanMessage(content=user_message)]},
            config=config,
        )

        print("AI:", response["messages"][-1].content)

    # print(f"STATE - {chatbot_workflow.get_state(config=config)}")
    # print(f"STATE HISTORY - {chatbot_workflow.get_state_history(config=config)}")
