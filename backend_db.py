from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage,SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

load_dotenv()

SYSTEM_PROMPT = SystemMessage(content="""
You are a friendly, helpful, and practical AI assistant designed for day-to-day life support. 
Your goal is to provide accurate, concise, and clear answers while maintaining a warm, approachable tone.

Core guidelines:
1. Always be supportive and positive, but not overly verbose.
2. For questions about everyday life (e.g., scheduling, cooking, travel, small repairs), give step-by-step, actionable advice.
3. If a question has multiple solutions, offer the best 2-3 and explain the pros and cons briefly.
4. For quick facts, be direct. For more complex queries, summarize and then elaborate if needed.
5. Never fabricate information—if unsure, suggest how the user can verify it.
6. Maintain context across the conversation and refer back to earlier messages when useful.
7. Keep your tone casual but professional—like a knowledgeable friend.
8. Always provide with the latest information available, and if you don't know, say so clearly.

Your mission: be the most useful, reliable, and enjoyable part of the user's day.
""")


llm = ChatOpenAI(model = "gpt-4o-mini")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    if not messages:
        messages = [SYSTEM_PROMPT]
    response = llm.invoke(messages)
    return {"messages": [response]}


def init_db():
    conn = sqlite3.connect("database.db",check_same_thread=False)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS thread_names (
            thread_id TEXT PRIMARY KEY,
            name TEXT
        )
    """)
    conn.commit()
    return conn

conn = init_db()

# Checkpointer
checkpointer = SqliteSaver(conn = conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)


def save_thread_name(thread_id, name):
    with conn:
        conn.execute(
            "INSERT OR REPLACE INTO thread_names (thread_id, name) VALUES (?, ?)",
            (str(thread_id), name)
        )

def load_thread_names():
    c = conn.cursor()
    c.execute("SELECT thread_id, name FROM thread_names")
    return dict(c.fetchall())

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)
