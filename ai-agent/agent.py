# agent.py - Todo List Agent using Agno

from agno.agent import Agent
from agno.tools import tool
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from models import add_task, update_task, get_all_tasks, delete_task, get_next_task_id
from dotenv import load_dotenv
import os

load_dotenv()

# --- Model Configuration ---
USE_VERTEX = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "false").lower() in ("1", "true", "yes")

if USE_VERTEX:
    llm = Gemini(
        id="gemini-2.0-flash",
        vertexai=True,
    )
else:
    llm = Gemini(
        id="gemini-2.0-flash",
        api_key=os.getenv("GOOGLE_API_KEY"),
    )

# --- Tools ---

@tool(show_result=True)
def create_task(name: str, description: str = "", status: bool = False):
    """Create a new task with auto-generated ID. Call this function when user wants to add a new task."""
    try:
        next_id = get_next_task_id()
        result = add_task(next_id, name, description, status)
        return f"Created task #{next_id}: {name}"
    except Exception as e:
        return f"Failed to create task: {str(e)}"

@tool(show_result=True)
def update_task_info(task_id: int, name: str = None, description: str = None, status: bool = None):
    """Update an existing task's information. Call this function when user wants to modify a task."""
    try:
        # Get current task to preserve unchanged fields
        all_tasks = get_all_tasks()
        current_task = next((task for task in all_tasks if task["id"] == task_id), None)
        
        if not current_task:
            return f"Task #{task_id} not found"
        
        # Use current values if not provided
        new_name = name if name is not None else current_task["name"]
        new_description = description if description is not None else current_task["description"]
        new_status = status if status is not None else current_task["status"]
        
        result = update_task(task_id, new_name, new_description, new_status)
        return f"Updated task #{task_id}: {new_name}"
    except Exception as e:
        return f"Failed to update task: {str(e)}"

@tool(show_result=True)
def show_tasks():
    """Display all tasks in a friendly format. Call this function when user wants to see their task list."""
    try:
        tasks = get_all_tasks()
        if not tasks:
            return "No tasks found. Time to get productive!"
        
        result = "Here are your tasks:\n\n"
        for task in tasks:
            status_icon = "✅" if task["status"] else "⏳"
            status_text = "Done" if task["status"] else "Pending"
            result += f"{status_icon} **Task #{task['id']}**: {task['name']}\n"
            if task["description"]:
                result += f"   📝 {task['description']}\n"
            result += f"   Status: {status_text}\n\n"
        
        return result
    except Exception as e:
        return f"Failed to fetch tasks: {str(e)}"

@tool(show_result=True)
def remove_task(task_id: int):
    """Delete a task by ID. Call this function when user wants to remove a task."""
    try:
        result = delete_task(task_id)
        return f"Task deleted: {result}"
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Failed to delete task: {str(e)}"

@tool(show_result=True)
def mark_task_complete(task_id: int):
    """Mark a task as completed. Call this function when user wants to mark a task as done."""
    try:
        # Get current task
        all_tasks = get_all_tasks()
        current_task = next((task for task in all_tasks if task["id"] == task_id), None)
        
        if not current_task:
            return f"Task #{task_id} not found"
        
        if current_task["status"]:
            return f"Task #{task_id} is already completed"
        
        result = update_task(task_id, current_task["name"], current_task["description"], True)
        return f"Task #{task_id} marked as complete"
    except Exception as e:
        return f"Failed to mark task complete: {str(e)}"

@tool(show_result=True)
def mark_task_pending(task_id: int):
    """Mark a task as pending/incomplete. Call this function when user wants to mark a task as not done."""
    try:
        # Get current task
        all_tasks = get_all_tasks()
        current_task = next((task for task in all_tasks if task["id"] == task_id), None)
        
        if not current_task:
            return f"Task #{task_id} not found"
        
        if not current_task["status"]:
            return f"Task #{task_id} is already pending"
        
        result = update_task(task_id, current_task["name"], current_task["description"], False)
        return f"Task #{task_id} marked as pending"
    except Exception as e:
        return f"Failed to mark task pending: {str(e)}"

# --- Agent Configuration ---
agent = Agent(
    model=llm,
    tools=[
        create_task, 
        update_task_info, 
        show_tasks, 
        remove_task, 
        mark_task_complete, 
        mark_task_pending
    ],
    description="""
        You are a todo list management AI. Your ONLY job is to use the provided tools to help users manage their tasks.
        
        CRITICAL: You MUST use the tools provided. Do NOT try to handle tasks manually or show raw data.
        
        **Tool Usage Rules:**
        1. ALWAYS use `create_task` when user wants to add a new task
        2. ALWAYS use `show_tasks` when user wants to see their tasks
        3. ALWAYS use `mark_task_complete` when user wants to mark a task as done
        4. ALWAYS use `mark_task_pending` when user wants to mark a task as not done
        5. ALWAYS use `update_task_info` when user wants to modify a task
        6. ALWAYS use `remove_task` when user wants to delete a task
        
        **Examples:**
        - User: "Create a task called 'Buy groceries'" → Use `create_task(name="Buy groceries")`
        - User: "Show me my tasks" → Use `show_tasks()`
        - User: "Mark task 1 as complete" → Use `mark_task_complete(task_id=1)`
        - User: "Update task 2 description" → Use `update_task_info(task_id=2, description="new description")`
        
        **Response Format:**
        - Use the tool's response directly without adding extra text
        - Keep responses concise and professional
        - Do not repeat or embellish the tool responses
        - Use minimal emojis (only ✅ and ⏳ for task status)
        - NEVER add phrases like "Here's your current todo list!" or similar text
        - Return ONLY the tool response, nothing more
        
        Remember: You are a tool-using AI. Use the tools for everything and return their responses directly!
    """,
    markdown=True,
    storage=SqliteStorage(db_file="todos.db", table_name="sessions"),
    add_history_to_messages=True,
    add_datetime_to_instructions=True,
)

def chat_with_agent(message: str):
    """Chat with the todo list agent"""
    try:
        response = agent.run(message, stream=False)
        return getattr(response, "content", str(response))
    except Exception as e:
        return f"Sorry, something went wrong: {str(e)}"
