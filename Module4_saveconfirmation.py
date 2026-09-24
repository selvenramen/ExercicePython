import json

TASKS_FILE = "tasks.json"


def load_tasks(filename):
    """Load tasks from a JSON file. Return an empty list if the file doesn't exist."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            tasks = json.load(f)

        print(f"Loaded {len(tasks)} task(s) from {filename}.")
        return tasks

    except FileNotFoundError:
        print("No save file found. Starting with an empty task list.")
        return []

    except json.JSONDecodeError:
        print("Save file is corrupted. Starting with an empty task list.")
        return []


def save_tasks(tasks, filename):
    """Save the task list to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4)

        print(f"Saved {len(tasks)} task(s) to {filename}.")

    except OSError as e:
        print(f"Error saving tasks: {e}")


def display_tasks(tasks):
    """Display all tasks with their index and status."""
    if len(tasks) == 0:
        print("Your task list is empty.")
        return

    print("\n--- Your Tasks ---")

    for index, task in enumerate(tasks):
        print(f"  {index + 1}. {task['description']} [{task['status']}]")

    print("------------------")


def add_task(tasks):
    """Ask the user for a description and add a new task."""
    description = input("Enter the task description: ")

    if description.strip() == "":
        print("Task description cannot be empty.")
        return

    task = {
        "description": description,
        "status": "pending"
    }

    tasks.append(task)

    print(f'Added: "{description}"')


def mark_task_complete(tasks):
    """Show tasks and let the user mark one as complete."""
    if len(tasks) == 0:
        print("No tasks to mark.")
        return

    display_tasks(tasks)

    task_number = input("Enter the task number to mark complete: ")

    if not task_number.isdigit():
        print("Please enter a valid number.")
        return

    task_index = int(task_number) - 1

    if task_index < 0 or task_index >= len(tasks):
        print("Invalid task number.")
        return

    if tasks[task_index]["status"] == "completed":
        print("That task is already completed.")
    else:
        tasks[task_index]["status"] = "completed"
        print(
            f'Marked "{tasks[task_index]["description"]}" as completed.'
        )


def main():
    """Run the Task Manager."""
    tasks = load_tasks(TASKS_FILE)

    print("=== Task Manager ===\n")

    while True:
        print("\nWhat would you like to do?")
        print("1. Add a task")
        print("2. View tasks")
        print("3. Mark a task as complete")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            add_task(tasks)
            save_tasks(tasks, TASKS_FILE)

        elif choice == "2":
            display_tasks(tasks)

        elif choice == "3":
            mark_task_complete(tasks)
            save_tasks(tasks, TASKS_FILE)

        elif choice == "4":
            save_tasks(tasks, TASKS_FILE)
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


main()