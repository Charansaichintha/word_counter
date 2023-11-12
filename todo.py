import os
import json
import argparse
import sys

TODO_FILE = 'todo.json'

def load_tasks():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    else:
        return []

def save_tasks(tasks):
    with open(TODO_FILE, 'w') as file:
        json.dump(tasks, file, indent=2)

def list_tasks(tasks):
    if tasks:
        print("Tasks:")
        for index, task in enumerate(tasks, start=1):
            status = "✓" if task['completed'] else " "
            print(f"{index}. [{status}] {task['description']}")
    else:
        print("No tasks found.")

def add_task(tasks, description):
    tasks.append({'description': description, 'completed': False})
    save_tasks(tasks)
    print(f"Task added: {description}")

def complete_task(tasks, index):
    if 1 <= index <= len(tasks):
        tasks[index - 1]['completed'] = True
        save_tasks(tasks)
        print(f"Task marked as complete: {tasks[index - 1]['description']}")
    else:
        print("Invalid task index.")

def main():
    parser = argparse.ArgumentParser(description="Simple command line to-do list manager.")
    parser.add_argument('-a', '--add', help="Add a new task", type=str)
    parser.add_argument('-l', '--list', help="List all tasks", action='store_true')
    parser.add_argument('-c', '--complete', help="Mark a task as complete", type=int)

    args = parser.parse_args()

    tasks = load_tasks()

    try:
        if args.add:
            add_task(tasks, args.add)
        elif args.list:
            list_tasks(tasks)
        elif args.complete is not None:
            complete_task(tasks, args.complete)
        else:
            print("Use -h or --help for usage information.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
