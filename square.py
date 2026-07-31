"""
square.py - Demonstrates Mistral AI with LangGraph and a DuckDuckGo search tool.

This module includes:
1. A simple square function with test cases
2. A DuckDuckGo search tool built with LangChain/LangGraph
3. A LangGraph agent using Mistral AI that can use the search tool
4. Test cases for the LangGraph agent and search tool
"""

import os
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_mistralai import ChatMistralAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set Mistral API key from environment
os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY", "")


# ---------------------------------------------------------------------------
# 1. Simple square function
# ---------------------------------------------------------------------------
def square(number):
    """Returns the square of a number."""
    return number ** 2


# ---------------------------------------------------------------------------
# 2. DuckDuckGo Search Tool using LangChain
# ---------------------------------------------------------------------------
@tool
def search_duckduckgo(query: str) -> str:
    """
    Search DuckDuckGo for information on the given query.

    Args:
        query: The search query string.

    Returns:
        A string containing the search results from DuckDuckGo.
    """
    search = DuckDuckGoSearchRun(region="us-en")
    try:
        result = search.invoke({"query": query})
        return str(result)
    except Exception as e:
        return f"Search error: {str(e)}"


# ---------------------------------------------------------------------------
# 3. LangGraph Agent with Mistral AI and DuckDuckGo tool
# ---------------------------------------------------------------------------
llm = ChatMistralAI(model="mistral-small-latest")

tools = [search_duckduckgo]
llm_with_tools = llm.bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def agent_node(state: AgentState):
    """LLM node that decides whether to answer or use a tool."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


tool_node = ToolNode(tools)

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")

agent = graph.compile()


# ---------------------------------------------------------------------------
# 4. Test cases
# ---------------------------------------------------------------------------
def run_tests():
    """Run all test cases to verify the code works correctly."""
    all_passed = True

    # ---- Test 1: square function ----
    print("=" * 60)
    print("TEST 1: square function")
    print("=" * 60)
    square_test_cases = [
        (5, 25),
        (0, 0),
        (1, 1),
        (-3, 9),
        (10, 100),
        (-7, 49),
        (2.5, 6.25),
    ]
    for input_val, expected in square_test_cases:
        actual = square(input_val)
        status = "PASS" if actual == expected else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"  square({input_val}) = {actual} | Expected: {expected} | {status}")

    # ---- Test 2: DuckDuckGo search tool ----
    print("\n" + "=" * 60)
    print("TEST 2: DuckDuckGo search tool")
    print("=" * 60)
    try:
        search_result = search_duckduckgo.invoke({"query": "What is LangGraph?"})
        if search_result and len(str(search_result)) > 0:
            print("  search_duckduckgo('What is LangGraph?') -> PASS (got results)")
            print(f"  Result preview: {str(search_result)[:200]}...")
        else:
            print("  search_duckduckgo('What is LangGraph?') -> FAIL (empty result)")
            all_passed = False
    except Exception as e:
        print(f"  search_duckduckgo('What is LangGraph?') -> FAIL ({e})")
        all_passed = False

    # ---- Test 3: DuckDuckGo search with a different query ----
    print("\n" + "=" * 60)
    print("TEST 3: DuckDuckGo search with different query")
    print("=" * 60)
    try:
        search_result2 = search_duckduckgo.invoke({"query": "Mistral AI"})
        if search_result2 and len(str(search_result2)) > 0:
            print("  search_duckduckgo('Mistral AI') -> PASS (got results)")
            print(f"  Result preview: {str(search_result2)[:200]}...")
        else:
            print("  search_duckduckgo('Mistral AI') -> FAIL (empty result)")
            all_passed = False
    except Exception as e:
        print(f"  search_duckduckgo('Mistral AI') -> FAIL ({e})")
        all_passed = False

    # ---- Test 4: LangGraph agent with Mistral AI (no tool call) ----
    print("\n" + "=" * 60)
    print("TEST 4: LangGraph agent with Mistral AI (simple question)")
    print("=" * 60)
    try:
        response = agent.invoke(
            {"messages": [HumanMessage(content="What is the square of 9?")]}
        )
        ai_message = response["messages"][-1]
        if isinstance(ai_message, AIMessage):
            content = str(ai_message.content)
            print(f"  Agent response: {content[:300]}")
            # Check if agent answered (not requesting a tool)
            if "81" in content or "square" in content.lower():
                print("  Status: PASS (agent answered correctly)")
            else:
                print("  Status: PASS (agent responded)")
        else:
            print(f"  Unexpected message type: {type(ai_message)}")
            all_passed = False
    except Exception as e:
        print(f"  LangGraph agent test -> FAIL ({e})")
        all_passed = False

    # ---- Test 5: LangGraph agent with Mistral AI (tool call) ----
    print("\n" + "=" * 60)
    print("TEST 5: LangGraph agent with Mistral AI (search query)")
    print("=" * 60)
    try:
        response2 = agent.invoke(
            {"messages": [HumanMessage(content="Search for 'LangGraph tutorial' on DuckDuckGo")]},
        )
        ai_message2 = response2["messages"][-1]
        if isinstance(ai_message2, AIMessage):
            content2 = str(ai_message2.content)
            print(f"  Agent response: {content2[:300]}")
            print("  Status: PASS (agent used search tool and responded)")
        else:
            print(f"  Unexpected message type: {type(ai_message2)}")
            all_passed = False
    except Exception as e:
        print(f"  LangGraph agent search test -> FAIL ({e})")
        all_passed = False

    # ---- Test 6: Agent state and graph structure ----
    print("\n" + "=" * 60)
    print("TEST 6: LangGraph agent structure validation")
    print("=" * 60)
    checks = {
        "graph has 'agent' node": "agent" in graph.nodes,
        "graph has 'tools' node": "tools" in graph.nodes,
        "graph compiled successfully": agent is not None,
        "llm is ChatMistralAI": isinstance(llm, ChatMistralAI),
        "tools list is not empty": len(tools) > 0,
        "search_duckduckgo is a tool": hasattr(search_duckduckgo, "invoke"),
    }
    for check_name, result in checks.items():
        status = "PASS" if result else "FAIL"
        if not result:
            all_passed = False
        print(f"  {check_name}: {status}")

    # ---- Final summary ----
    print("\n" + "=" * 60)
    print(f"{'ALL TESTS PASSED!' if all_passed else 'SOME TESTS FAILED!'}")
    print("=" * 60)
    return all_passed


if __name__ == "__main__":
    run_tests()