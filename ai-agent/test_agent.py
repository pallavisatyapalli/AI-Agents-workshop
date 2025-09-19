#!/usr/bin/env python3
"""
Test script for the Todo List Agent
"""

from agent import chat_with_agent

def test_agent():
    """Test basic agent functionality"""
    print("🤖 Testing Todo List Agent...\n")
    
    # Test 1: Create a task
    print("1️⃣ Creating a task...")
    response = chat_with_agent("Create a task called 'Buy groceries' with description 'Milk, bread, eggs'")
    print(f"Response: {response}\n")
    
    # Test 2: Show all tasks
    print("2️⃣ Showing all tasks...")
    response = chat_with_agent("Show me all my tasks")
    print(f"Response: {response}\n")
    
    # Test 3: Create another task
    print("3️⃣ Creating another task...")
    response = chat_with_agent("Add a task called 'Call mom'")
    print(f"Response: {response}\n")
    
    # Test 4: Mark first task as complete
    print("4️⃣ Marking first task as complete...")
    response = chat_with_agent("Mark task 1 as complete")
    print(f"Response: {response}\n")
    
    # Test 5: Show tasks again
    print("5️⃣ Showing tasks again...")
    response = chat_with_agent("What are my current tasks?")
    print(f"Response: {response}\n")
    
    # Test 6: Update a task
    print("6️⃣ Updating a task...")
    response = chat_with_agent("Update task 2 description to 'Call mom to check in'")
    print(f"Response: {response}\n")
    
    # Test 7: Final task list
    print("7️⃣ Final task list...")
    response = chat_with_agent("Show me my final task list")
    print(f"Response: {response}\n")

if __name__ == "__main__":
    test_agent()
