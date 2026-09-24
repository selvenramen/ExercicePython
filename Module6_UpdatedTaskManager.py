import json


class TaskManager:
    """Manages a collection of tasks."""

    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self._load_tasks()

    def _load_tasks(self):
        """Load tasks from the JSON file into self.tasks."""
        try:
            with open(self.filename, "r") as f:
                tasks_data = json.load(f)

            self.tasks = [Task.from_dict(d) for d in tasks_data]

            print(
                f"Loaded {len(self.tasks)} task(s) "
                f"from {self.filename}."
            )

        except FileNotFoundError:
            print(
                "No save file found. "
                "Starting with an empty task list."
            )
            self.tasks = []

        except json.JSONDecodeError:
            print(
                "Save file is corrupted. "
                "Starting with an empty task list."
            )
            self.tasks = []

    def _save_tasks(self):
        """Save self.tasks to the JSON file."""
        tasks_data = [task.to_dict() for task in self.tasks]

        try:
            with open(self.filename, "w") as f:
                json.dump(tasks_data, f, indent=4)

        except IOError as e:
            print(f"Error saving tasks: {e}")

    def add_task(self):
        """Interactively add a new task."""
        description = input("Enter the task description: ")

        if not description.strip():
            print("Task description cannot be empty.")
            return

        priority = input(
            "Priority (high/medium/low) [medium]: "
        ).strip().lower()

        if priority not in ("high", "medium", "low"):
            priority = "medium"

        due_date = input(
            "Due date (YYYY-MM-DD) or press Enter for none: "
        ).strip()

        if due_date == "":
            due_date = None

        task = Task(
            description,
            priority=priority,
            due_date=due_date
        )

        self.tasks.append(task)
        self._save_tasks()

        print(f'Added: "{description}"')

    def view_tasks(self):
        """Display all tasks."""
        if len(self.tasks) == 0:
            print("Your task list is empty.")
            return

        print("\n--- Your Tasks ---")

        for index, task in enumerate(self.tasks):
            print(f"  {index + 1}. {task}")

        print("------------------")

    def mark_task_complete(self):
        """Show tasks and let the user mark one as complete."""
        if len(self.tasks) == 0:
            print("No tasks to mark.")
            return

        self.view_tasks()

        task_number_str = input(
            "Enter the task number to mark complete: "
        )

        if not task_number_str.isdigit():
            print("Please enter a valid number.")
            return

        task_index = int(task_number_str) - 1

        if task_index < 0 or task_index >= len(self.tasks):
            print("Invalid task number.")
            return

        if self.tasks[task_index].status == "completed":
            print("That task is already completed.")
        else:
            self.tasks[task_index].mark_complete()
            self._save_tasks()

            print(
                f'Marked "{self.tasks[task_index].description}" '
                "as completed."
            )

    def delete_task(self):
        """Show tasks and let the user delete one."""
        if len(self.tasks) == 0:
            print("No tasks to delete.")
            return

        self.view_tasks()

        task_number_str = input(
            "Enter the task number to delete: "
        )

        if not task_number_str.isdigit():
            print("Please enter a valid number.")
            return

        task_index = int(task_number_str) - 1

        if task_index < 0 or task_index >= len(self.tasks):
            print("Invalid task number.")
            return

        removed = self.tasks.pop(task_index)

        self._save_tasks()

        print(f'Deleted: "{removed.description}"')

    def run(self):
        """Run the interactive Task Manager."""
        print("=== Task Manager ===\n")

        while True:
            print("\nWhat would you like to do?")
            print("1. Add a task")
            print("2. View tasks")
            print("3. Mark a task as complete")
            print("4. Delete a task")
            print("5. Exit")

            choice = input("\nEnter your choice (1-5): ")

            if choice == "1":
                self.add_task()

            elif choice == "2":
                self.view_tasks()

            elif choice == "3":
                self.mark_task_complete()

            elif choice == "4":
                self.delete_task()

            elif choice == "5":
                self._save_tasks()
                print("Goodbye!")
                break

            else:
                print(
                    "Invalid choice. "
                    "Please enter 1, 2, 3, 4, or 5."
                )


if __name__ == "__main__":
    app = TaskManager()
    app.run()