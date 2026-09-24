import json
import csv

TASKS_FILE = "tasks.json"
CSV_FILE = "tasks.csv"

FIELDNAMES = ["description", "status"]


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


def save_tasks_csv(tasks, filename):
    """Save the task list to a CSV file."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(tasks)

        print(f"Saved {len(tasks)} task(s) to {filename}.")

    except OSError as e:
        print(f"Error saving CSV file: {e}")


def load_tasks_csv(filename):
    """Load tasks from a CSV file."""
    try:
        with open(filename, "r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    except FileNotFoundError:
        return []


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
        print("4. Export tasks to CSV")
        print("5. Import tasks from CSV")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

        if choice == "1":
            add_task(tasks)
            save_tasks(tasks, TASKS_FILE)

        elif choice == "2":
            display_tasks(tasks)

        elif choice == "3":
            mark_task_complete(tasks)
            save_tasks(tasks, TASKS_FILE)

        elif choice == "4":
            save_tasks_csv(tasks, CSV_FILE)

        elif choice == "5":
            imported_tasks = load_tasks_csv(CSV_FILE)

            if len(imported_tasks) == 0:
                print("No tasks found in the CSV file.")
            else:
                tasks = imported_tasks
                print(f"Imported {len(tasks)} task(s) from {CSV_FILE}.")

        elif choice == "6":
            save_tasks(tasks, TASKS_FILE)
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")


main()