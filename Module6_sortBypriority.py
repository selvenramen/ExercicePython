import json
from datetime import datetime, timezone


class Task:
    """Represents a single task."""

    VALID_STATUSES = {"pending", "completed"}
    VALID_PRIORITIES = {"high", "medium", "low"}

    def __init__(
        self,
        description,
        status="pending",
        created_at=None,
        priority="medium",
        due_date=None
    ):
        description = description.strip()

        if not description:
            raise ValueError("Task description cannot be empty.")

        if status not in self.VALID_STATUSES:
            raise ValueError(f"Unsupported status: {status}")

        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Unsupported priority: {priority}")

        self.description = description
        self.status = status
        self.created_at = (
            created_at or datetime.now(timezone.utc).isoformat()
        )
        self.priority = priority
        self.due_date = due_date

    def __str__(self):
        """Return a readable representation of the task."""
        return (
            f"{self.description} "
            f"[{self.status}] "
            f"(Priority: {self.priority})"
        )

    def is_complete(self):
        """Return True if this task is completed."""
        return self.status == "completed"

    def mark_complete(self):
        """Mark this task as completed."""
        self.status = "completed"

    def to_dict(self):
        """Convert the task to a dictionary for JSON storage."""
        return {
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "priority": self.priority,
            "due_date": self.due_date,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task object from a dictionary."""
        return cls(
            description=data["description"],
            status=data.get("status", "pending"),
            created_at=data.get("created_at"),
            priority=data.get("priority", "medium"),
            due_date=data.get("due_date"),
        )


class TaskManager:
    """Manages a collection of tasks."""

    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self._load_tasks()

    def _load_tasks(self):
        """Load tasks from the JSON file."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                tasks_data = json.load(f)

            self.tasks = [
                Task.from_dict(data)
                for data in tasks_data
            ]

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
        """Save tasks to the JSON file."""
        tasks_data = [
            task.to_dict()
            for task in self.tasks
        ]

        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(tasks_data, f, indent=4)

            print(
                f"Saved {len(self.tasks)} task(s) "
                f"to {self.filename}."
            )

        except OSError as e:
            print(f"Error saving tasks: {e}")

    def _display_task_list(
        self,
        task_list,
        title="Your Tasks"
    ):
        """Display a list of tasks."""
        if not task_list:
            print("No tasks to display.")
            return

        print(f"\n--- {title} ---")

        for index, task in enumerate(task_list):
            print(f"  {index + 1}. {task}")

        print("------------------")

    def add_task(self):
        """Interactively add a new task."""
        description = input(
            "Enter the task description: "
        )

        if not description.strip():
            print("Task description cannot be empty.")
            return

        priority = input(
            "Priority (high/medium/low) [medium]: "
        ).strip().lower()

        if priority not in ("high", "medium", "low"):
            print("Invalid priority. Using medium.")
            priority = "medium"

        due_date = input(
            "Due date (YYYY-MM-DD) "
            "or press Enter for none: "
        ).strip()

        if due_date == "":
            due_date = None

        try:
            task = Task(
                description=description,
                priority=priority,
                due_date=due_date
            )

            self.tasks.append(task)
            self._save_tasks()

            print(f'Added: "{task.description}"')

        except ValueError as e:
            print(f"Error: {e}")

    def view_tasks(self):
        """Display all tasks."""
        self._display_task_list(
            self.tasks,
            "Your Tasks"
        )

    def view_pending(self):
        """Display only tasks whose status is pending."""
        pending = [
            task
            for task in self.tasks
            if task.status == "pending"
        ]

        if not pending:
            print("No pending tasks.")
            return

        self._display_task_list(
            pending,
            "Pending Tasks"
        )

    def view_by_priority(self):
        """Display tasks ordered high, medium, then low."""
        priority_order = {
            "high": 0,
            "medium": 1,
            "low": 2
        }

        ordered = sorted(
            self.tasks,
            key=lambda task: priority_order.get(
                task.priority,
                99
            )
        )

        self._display_task_list(
            ordered,
            "Tasks by Priority"
        )

    def mark_task_complete(self):
        """Show tasks and mark one as complete."""
        if not self.tasks:
            print("No tasks to mark.")
            return

        self.view_tasks()

        task_number = input(
            "Enter the task number to mark complete: "
        )

        if not task_number.isdigit():
            print("Please enter a valid number.")
            return

        task_index = int(task_number) - 1

        if task_index < 0 or task_index >= len(self.tasks):
            print("Invalid task number.")
            return

        task = self.tasks[task_index]

        if task.is_complete():
            print("That task is already completed.")
        else:
            task.mark_complete()
            self._save_tasks()

            print(
                f'Marked "{task.description}" '
                "as completed."
            )

    def delete_task(self):
        """Show tasks and delete one."""
        if not self.tasks:
            print("No tasks to delete.")
            return

        self.view_tasks()

        task_number = input(
            "Enter the task number to delete: "
        )

        if not task_number.isdigit():
            print("Please enter a valid number.")
            return

        task_index = int(task_number) - 1

        if task_index < 0 or task_index >= len(self.tasks):
            print("Invalid task number.")
            return

        removed = self.tasks.pop(task_index)

        self._save_tasks()

        print(
            f'Deleted: "{removed.description}"'
        )

    def run(self):
        """Run the interactive Task Manager."""
        print("=== Task Manager ===")

        while True:
            print("\nWhat would you like to do?")
            print("1. Add a task")
            print("2. View all tasks")
            print("3. Mark a task as complete")
            print("4. Delete a task")
            print("5. View pending tasks")
            print("6. View tasks by priority")
            print("7. Exit")

            choice = input(
                "\nEnter your choice (1-7): "
            )

            if choice == "1":
                self.add_task()

            elif choice == "2":
                self.view_tasks()

            elif choice == "3":
                self.mark_task_complete()

            elif choice == "4":
                self.delete_task()

            elif choice == "5":
                self.view_pending()

            elif choice == "6":
                self.view_by_priority()

            elif choice == "7":
                self._save_tasks()
                print("Goodbye!")
                break

            else:
                print(
                    "Invalid choice. "
                    "Please enter 1, 2, 3, 4, 5, 6, or 7."
                )


if __name__ == "__main__":
    app = TaskManager()
    app.run()