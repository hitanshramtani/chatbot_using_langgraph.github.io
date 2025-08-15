import streamlit as st
from backend_db import chatbot, retrieve_all_threads,save_thread_name, load_thread_names
from langchain_core.messages import HumanMessage
import uuid

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id
def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
        st.session_state["chat_thread_names"][thread_id] = "New Chat"
def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']
def update_thread_name(thread_id,name):
    st.session_state["chat_thread_names"][thread_id] = name
    save_thread_name(thread_id, name)


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if "thread_id" not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
    
if "chat_threads" not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

if "chat_thread_names" not in st.session_state:
    st.session_state["chat_thread_names"] = load_thread_names()
    
add_thread(st.session_state['thread_id'])
    
    
CONFIG = {'configurable': {'thread_id':  st.session_state['thread_id']}}
    
st.sidebar.title('Hitansh Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()
    
st.sidebar.header('Chat History')
for thread_id in st.session_state['chat_threads'][::-1]:
    thread_name = st.session_state["chat_thread_names"].get(thread_id, str(thread_id))
    if st.sidebar.button(thread_name,key=str(thread_id)):
        st.session_state['thread_id'] = thread_id
        try:
            messages = load_conversation(thread_id)
        except Exception as e:
            messages = []

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input("Type your message here...")

if user_input:
    if len(st.session_state['message_history']) == 0:
        update_thread_name(st.session_state['thread_id'], user_input[:20])
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message("user"):
        st.text(user_input)
        
    
    # first add the message to message_history
    
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadeta in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            )
        )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})