# Chatbot Using LangGraph, Streamlit, and SQLite

This project is a multi-threaded conversational AI chatbot built with [LangGraph](https://github.com/langchain-ai/langgraph), [Streamlit](https://streamlit.io/), and [SQLite](https://www.sqlite.org/). It supports persistent chat threads, custom thread naming, and conversation history storage.

## Features

- **Multi-threaded chat:** Start new conversations, switch between threads, and view chat history.
- **Persistent storage:** All chat threads and their names are saved in an SQLite database, so your conversations are not lost after restarting the app.
- **Custom thread names:** Each chat thread can be named automatically (using the first message) or manually.
- **Modern UI:** Built with Streamlit for an interactive and user-friendly experience.
- **LLM-powered:** Uses OpenAI's GPT-4o-mini (or your configured LLM) for responses.

## Project Structure

```
LANGGRAPH/Projects/chatbot_using_langgraph/
│
├── backend_db.py                # Handles database, thread management, and LLM graph
├── frontend_connected_with_db.py # Streamlit frontend for chat UI and thread management
├── database.db                  # SQLite database file (auto-created)
└── ...                          # Other supporting files
```

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/hitanshramtani/chatbot_using_langgraph.github.io.git
cd LANGGRAPH/Projects/chatbot_using_langgraph
```

2. **Create and activate a virtual environment**

```bash
python -m venv newvenv
# On Windows:
newvenv\Scripts\activate
# On Linux/Mac:
source newvenv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

5. **Run the Streamlit app**

```bash
streamlit run frontend_connected_with_db.py
```

## Usage

- Click **New Chat** in the sidebar to start a new conversation thread.
- Each thread is named "New Chat" initially and is renamed after your first message.
- Switch between threads using the sidebar buttons.
- All chat history and thread names are saved in `database.db`.

## Customization

- You can change the LLM model in `backend_db.py` by modifying the `ChatOpenAI` initialization.
- The database schema can be extended for more metadata or user management.

## Requirements

- Python 3.8+
- Streamlit
- LangGraph
- LangChain
- OpenAI Python SDK
- SQLite (included with Python)



## Acknowledgements

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Streamlit](https://streamlit.io/)
- [OpenAI](https://openai.com/)
