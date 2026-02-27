# 🤖 Agentic AI with LangGraph

A practical learning repository exploring Agentic AI concepts using **LangGraph**, **LangChain**, and LLMs like **Google Gemini** and **Mistral AI**.

## 📁 What's Inside

### 🔄 Workflow Patterns (Jupyter Notebooks)
- `sequential_workflow.ipynb` — Linear chain of nodes executing one after another
- `parallel_workflow.ipynb` — Nodes running in parallel branches
- `conditional_workflow.ipynb` / `conditional_workflow2.ipynb` — Dynamic routing based on state conditions
- `iterative_workflow.ipynb` — Loops and repeated execution within a graph
- `persistent.ipynb` — Stateful conversations with memory/checkpointing

### 💬 Chatbot Implementations (`/chatbot`)
- `langgraph_backend.py` — Basic LangGraph chatbot with in-memory conversation history
- `langgraph_database_backend.py` — Persistent chatbot using SQLite checkpointing + LangSmith tracing
- `langgraph_tool_backend.py` — Tool-augmented chatbot (web search, calculator, stock prices) using Mistral AI
- `streamlit_frontend.py` / `streamlit_database_frontend.py` — Streamlit UI for the chatbots

### 🛠️ LangChain Tools (`/Langchain_Tools`)
- `tool_calling.ipynb` — Basics of tool/function calling with LangChain
- `custom_tools.ipynb` — Building and integrating custom tools

### ⚡ Other
- `advanced_chatbot.ipynb` — Advanced chatbot experiments
- `tools.ipynb` — Tool usage exploration
- `main.py` — Simple LLM invocation example with Gemini

## 🧰 Tech Stack
- **LangGraph** — Graph-based agentic workflow orchestration
- **LangChain** — LLM framework and tool integration
- **Google Gemini (gemini-2.5-flash)** — Primary LLM
- **Mistral AI** — Used in tool-augmented chatbot
- **Streamlit** — Frontend UI
- **SQLite** — Persistent conversation memory
- **DuckDuckGo Search, Alpha Vantage** — External tools

## 🚀 Getting Started
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your API keys:
   ```python
    GOOGLE_API_KEY=your_key_here
    MISTRAL_API_KEY=your_key_here
   ```
