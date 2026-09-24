import json

TASKS_FILE = "tasks.json"


class Task:
    """Represents a single task with a description and status."""

    def __init__(self, description, status="pending"):
        self.description = description
        self.status = status

    def __str__(self):
        return f"{self.description} [{self.status}]"

    def is_complete(self):
        """Return True if this task is completed."""
        return self.status == "completed"

    def mark_complete(self):
        """Mark this task as completed."""
        self.status = "completed"

    def to_dict(self):
        """Convert to a dictionary for JSON serialization."""
        return {
            "description": self.description,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task from a dictionary."""
        return cls(data["description"], data["status"])


# Test the Task class
task1 = Task("Learn Python")
task2 = Task("Build a Task Manager")
task3 = Task("Write tests", "completed")

print(task1)
print(task2)
print(task3)

task1.mark_complete()
print(task1)

data = task1.to_dict()
print(data)

copy_of_task1 = Task.from_dict(data)
print(copy_of_task1)


def load_tasks(filename):
    """Load tasks from a JSON file, returning a list of Task objects."""
    try:
        with open(filename, "r") as f:
            tasks_data = json.load(f)

        tasks = [Task.from_dict(d) for d in tasks_data]

        print(f"Loaded {len(tasks)} task(s) from {filename}.")
        return tasks

    except FileNotFoundError:
        print("No save file found. Starting with an empty task list.")
        return []

    except json.JSONDecodeError:
        print("Save file is corrupted. Starting with an empty task list.")
        return []


def save_tasks(tasks, filename):
    """Save a list of Task objects to a JSON file."""
    tasks_data = [task.to_dict() for task in tasks]

    try:
        with open(filename, "w") as f:
            json.dump(tasks_data, f, indent=4)

        print("Tasks saved.")

    except IOError as e:
        print(f"Error saving tasks: {e}")


def display_tasks(tasks):
    """Display all tasks with their index and status."""
    if len(tasks) == 0:
        print("Your task list is empty.")
        return

    print("\n--- Your Tasks ---")

    for index, task in enumerate(tasks):
        print(f"  {index + 1}. {task}")

    print("------------------")


def add_task(tasks):
    """Ask the user for a description and add a new Task."""
    description = input("Enter the task description: ")

    if description.strip() == "":
        print("Task description cannot be empty.")
        return

    task = Task(description)
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

    task = tasks[task_index]

    if task.is_complete():
        print("That task is already completed.")
    else:
        task.mark_complete()
        print(f'Marked "{task.description}" as completed.')


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