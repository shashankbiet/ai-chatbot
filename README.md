# ai-chatbot

A lightweight Python chatbot foundation using LangChain, LangGraph, and local LM Studio-compatible models.

This repository is designed as a minimal AI workflow example, separating configuration, application entrypoints, and workflow logic so future features like retrieval or document QA can be added without duplicating core infrastructure.


## What this repo contains

- `src/app/cli.py` — thin command-line interface for interactive chat
- `src/config/settings.py` — model and runtime settings using Pydantic
- `src/workflows/chatbot_workflow.py` — chat workflow built with LangGraph


## How it works

1. The CLI asks for user input
2. The chat model is created by `llm-factory` using LM Studio settings
3. `Chatbot.build_chatbot_workflow` constructs a simple LangGraph workflow
4. The workflow uses an in-memory LangGraph checkpoint saver (`MemorySaver`) so state can be tracked during execution without persisting it to disk
5. User messages are passed to the chat model
6. The generated response is printed to the terminal


## Repository Layout

```text
ai-chatbot/
├── src/
│   ├── app/
│   │   └── cli.py
│   ├── config/
│   │   └── settings.py
│   └── workflows/
│       └── chatbot_workflow.py
├── pyproject.toml
├── requirements.txt
└── README.md
```


## Tech stack

- Python 3.12+
- LangChain
- LangGraph
- llm-factory
- Pydantic Settings
- uv
- Ruff


## Setup

Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate
```

Install dependencies:

```bash
uv sync
```

Start the app:

```bash
uv run python main.py
```

Run lint checks:

```bash
uv run ruff check src
```

Then type messages and use `exit`, `quit`, or `bye` to end the session.


## Local Model Setup

The default settings expect LM Studio-compatible local models:

```python
chat_model = "gemma-3-1b"
embedding_model = "nomic-embed-text-v1.5"
```

Start the LM Studio local server with an OpenAI-compatible endpoint:

```text
http://localhost:1234/v1
```

Model names can be changed in:

```text
src/config/settings.py
```
