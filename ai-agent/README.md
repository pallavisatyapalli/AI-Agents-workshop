# Todo List AI Agent

A friendly AI-powered todo list manager built with Agno and FastAPI.

## Features

- 🤖 **AI-Powered**: Natural language interaction for managing tasks
- 📝 **CRUD Operations**: Create, read, update, and delete tasks
- 🆔 **Auto-ID Generation**: Automatically assigns unique IDs to new tasks
- ✅ **Status Management**: Mark tasks as complete or pending
- 💬 **Natural Responses**: Human-like, friendly conversation style
- 🗄️ **SQLite Storage**: Persistent data storage
- 🌐 **Web API**: RESTful API endpoints for integration

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   # Optional: Use Vertex AI instead
   GOOGLE_GENAI_USE_VERTEXAI=false
   ```

3. **Initialize the database**:
   The database will be created automatically when you first run the application.

## Usage

### Running the Web Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

### Testing the Agent

```bash
python test_agent.py
```

### Web Interface

- **Main page**: `http://localhost:8000/` - View all tasks
- **Chat endpoint**: `POST /agent/chat` - Interact with the AI agent

## API Endpoints

- `GET /` - Get all tasks
- `POST /agent/chat` - Chat with the AI agent
- `POST /add` - Add a new task
- `PUT /update/{task_id}` - Update an existing task
- `DELETE /delete/{task_id}` - Delete a task

## Agent Capabilities

The AI agent can understand natural language requests like:

- "Create a task called 'Buy groceries'"
- "Mark task 1 as complete"
- "Show me all my tasks"
- "Update task 2 description to 'Call mom'"
- "Delete task 3"
- "What are my pending tasks?"

## Example Conversations

**User**: "I need to buy groceries tomorrow"
**Agent**: "✅ Created task #1: Buy groceries"

**User**: "Show me my tasks"
**Agent**: "📋 Here are your tasks:

✅ **Task #1**: Buy groceries
   Status: Pending

⏳ **Task #2**: Call mom
   📝 Call mom to check in
   Status: Pending"

## Architecture

- **`agent.py`**: AI agent implementation using Agno
- **`models.py`**: Database operations and data models
- **`main.py`**: FastAPI web server
- **`todos.db`**: SQLite database for task storage

## Dependencies

- `agno`: AI agent framework
- `fastapi`: Web framework
- `sqlite3`: Database (built-in)
- `python-dotenv`: Environment variable management
- `uvicorn`: ASGI server

## Notes

- The agent automatically generates unique IDs for new tasks
- Tasks are stored with boolean status (true = complete, false = pending)
- The agent provides friendly, encouraging responses with emojis
- All database operations are wrapped in proper error handling
