import os
from typing import Final
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from src.workflows import Chatbot

load_dotenv()

DEFAULT_THREAD_ID: Final = "1"
EXIT_COMMANDS: Final = {"exit", "quit", "bye"}

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_BASE_URL"),
)

langfuse_callback_handler = CallbackHandler(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
)


def get_chat_model() -> BaseChatModel:
    return ChatOpenAI(
        model="gemma-3-1b",
        api_key=os.getenv("OPENAI_API_KEY", "lm-studio"),
        base_url="http://localhost:1234/v1",
        temperature=0,
        callbacks=[langfuse_callback_handler],
    )


def run_chat(thread_id: str = DEFAULT_THREAD_ID) -> None:
    chat_model = get_chat_model()
    chatbot_workflow = Chatbot.build_chatbot_workflow(chat_model)
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        user_message = input("Type here: ")
        if user_message.strip().lower() in EXIT_COMMANDS:
            langfuse.flush()  # Ensure all events are sent to Langfuse before exiting
            break

        response = chatbot_workflow.invoke(
            {"messages": [HumanMessage(content=user_message)]},
            config=config,
        )

        print("AI:", response["messages"][-1].content)

    # print(f"STATE - {chatbot_workflow.get_state(config=config)}")
    # print(f"STATE HISTORY - {chatbot_workflow.get_state_history(config=config)}")
