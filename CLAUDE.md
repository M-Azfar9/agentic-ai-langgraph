# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A hands-on learning repository for **Agentic AI with LangGraph**. It collects Jupyter notebooks and small Python backends that explore LangGraph workflow patterns (sequential, parallel, conditional, iterative, persistent) and build progressively more capable chatbots (in-memory → SQLite-persistent → tool-augmented). There is no package/library structure — it is a study collection, so files are meant to be read and run top-to-bottom as experiments rather than imported as a cohesive app.

Primary LLMs: Google Gemini (`gemini-2.5-flash`) and Mistral AI (`mistral-large-latest`). Newer notebooks also use **OpenRouter** via `langchain-openrouter` (`ChatOpenRouter`) to reach models like `nvidia/nemotron-3-ultra-550b-a55b:free` and `z-ai/glm-5.2`.

## Environment & Commands

This is a Windows/PowerShell environment. A local virtualenv lives at `myenv/` (note: `.gitignore` lists `myvenv/` but the actual dir is `myenv/`).

```powershell
# Activate the virtualenv
myenv\Scripts\Activate.ps1

# Install dependencies (env-specific pins)
pip install -r requirements.txt

# Run a chatbot UI (Streamlit)
streamlit run chatbot\streamlit_frontend.py            # in-memory backend
streamlit run chatbot\streamlit_database_frontend.py   # SQLite + tool backend

# Run the plain LLM example
python main.py
```

Jupyter notebooks are the core deliverables — open and run them cell-by-cell in the activated env (e.g. `jupyter notebook`, or an IDE Jupyter integration). There is no test suite or build step.

**Secrets:** A `.env` file (gitignored) holds API keys (`GOOGLE_API_KEY`, `MISTRAL_API_KEY`, `OPENROUTER_API_KEY`, `LANGSMITH_API_KEY`, etc.) and is loaded with `load_dotenv()`. Note that some backend files still **hardcode** keys directly (`langgraph_database_backend.py`, `langgraph_tool_backend.py`) instead of reading them from env — prefer `os.getenv(...)` / `load_dotenv()` when editing these.

## Architecture

### The shared LangGraph pattern
Every chatbot backend follows the same shape, so once you understand one you understand all:
- A `ChatState(TypedDict)` whose `messages` field is `Annotated[list[BaseMessage], add_messages]` — the `add_messages` reducer appends rather than overwrites, which is what makes multi-turn history work.
- A single `chat_node(state)` that calls `llm.invoke(state["messages"])` and returns `{"messages": [response]}`.
- A `StateGraph(ChatState)` compiled with a **checkpointer**; `START → chat_node → END`.

### Backends (`chatbot/`)
Three backends demonstrate escalating capability, all sharing the pattern above:
- `langgraph_backend.py` — simplest; `InMemorySaver` checkpointer, Gemini, no persistence across process restarts.
- `langgraph_database_backend.py` — same graph but `SqliteSaver` over `chatbot.db` (SQLite checkpointing) so conversations survive restarts; also hardcodes LangSmith tracing env vars. Exposes `retrieve_all_threads()` to enumerate `thread_id`s from stored checkpoints.
- `langgraph_tool_backend.py` — tool-augmented agent using **Mistral**. Beyond the basic pattern it: binds tools with `llm.bind_tools(tools)`, adds a `ToolNode`, and wires `graph.add_conditional_edges("chat_node", tools_condition)` plus an edge `tools → chat_node` so the LLM can loop back after a tool runs. Tools: DuckDuckGo search, a `calculator` `@tool`, and `get_stock_price` (Alpha Vantage).

### Frontends (`chatbot/`)
`streamlit_frontend.py` and `streamlit_database_frontend.py` are thin UIs that import a compiled `chatbot` graph from the backend module and drive it. Key concepts:
- Conversation isolation is by **`thread_id`** (a `uuid`), passed as `config={'configurable': {'thread_id': ...}}` to `chatbot.invoke`/`chatbot.stream`. The DB frontend seeds its thread list from `retrieve_all_threads()` (reads existing threads from SQLite); the in-memory frontend only tracks threads in `st.session_state`.
- Streaming uses `chatbot.stream(..., stream_mode="messages")` fed into `st.write_stream`. The DB frontend additionally inspects `metadata["langgraph_node"]` to show a live status ("Thinking…" vs "Executing tools…") and renders tool calls from `msg.tool_calls`.

### OpenRouter experiments
`open_router_testing.ipynb` (and `openRouterApi.txt`, `payload.json`, `claude_help*.txt`) explore `langchain_openrouter.ChatOpenRouter` for streaming/invoking various non-Anthropic models. This is separate from the Gemini/Mistral chatbot backends and is exploratory rather than integrated.

### Workflow notebooks
`sequential_workflow.ipynb`, `parallel_workflow.ipynb`, `conditional_workflow.ipynb` (+ `_2`), `iterative_workflow.ipynb`, and `persistent.ipynb` build up LangGraph graph concepts (node ordering, branching, routing, loops, checkpointed state) using the same `StateGraph` + `ChatState` primitives before applying them to the chatbots. `Langchain_Tools/tool_calling.ipynb` and `custom_tools.ipynb` cover the tool/function-calling foundations used by the tool backend.
