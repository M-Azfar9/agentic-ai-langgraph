import streamlit as st
from langgraph_tool_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid
from dotenv import load_dotenv
import os


load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ['LANGSMITH_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGSMITH_API_KEY'] = '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'
os.environ['LANGCHAIN_PROJECT'] = 'chatbot'


# utility functions
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    st.session_state['thread_id'] = generate_thread_id()
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id) 

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable':{'thread_id': thread_id}})
    # Print or log keys to debug
    print("Available keys in state.values:", state.values.keys())

    # Use .get() to safely access messages
    messages = state.values.get('messages', [])
    return messages




user_input = st.chat_input("Type here...")

if "message_history" not in st.session_state:
    st.session_state.message_history = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])

st.sidebar.title("SONYC")
if st.sidebar.button('New Chat'):
    reset_chat()


st.sidebar.header('Your Conversation')

for thread in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread)):
        st.session_state['thread_id'] = thread
        messages = load_conversation(thread)

        temp_messages = []

        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'

            temp_messages.append({'role': role, 'content': message.content})

        st.session_state['message_history'] = temp_messages


CONFIG={
    'configurable':{'thread_id':st.session_state['thread_id']},
    'metadata':{'thread_id':st.session_state['thread_id']},
    'run_name':'chat_turn'

    }

# Load conversation history
for message in st.session_state.message_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input:
    # User message
    st.session_state.message_history.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.write(user_input)

    # Assistant response (example)
    # response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]}, config=CONFIG)
    # ai_message = response["messages"][-1].content
    # st.session_state.message_history.append(
    #     {"role": "assistant", "content": ai_message}
    # )
    # with st.chat_message("assistant"):
    #     st.write(ai_message)

    # response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]}, config=CONFIG)
    # ai_message = response["messages"][-1].content
    # st.session_state.message_history.append(
    #     {"role": "assistant", "content": ai_message}
    # )
    with st.chat_message("assistant"):
        def ai_only_stream():
            for message, metadata in chatbot.stream(
                {'messages':[HumanMessage(content=user_input)]}, 
                config=CONFIG,
                stream_mode='messages'
            ):
                if isinstance(message, AIMessage):
                    yield message.content
        
        ai_message = st.write_stream(ai_only_stream())
        st.session_state.message_history.append(
        {"role": "assistant", "content": ai_message}
        )