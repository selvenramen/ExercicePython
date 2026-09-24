def is_empty(tasks):
    """Return True when the task list has no items."""
    return len(tasks) == 0


def display_tasks(tasks):
    """Display all tasks with their index and status."""
    if is_empty(tasks):
        print("Your task list is empty.")
        return

    print("\n--- Your Tasks ---")

    for index, task in enumerate(tasks):
        print(f"{index + 1}. {task['description']} [{task['status']}]")

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


def ask_for_task_index(tasks):
    """Ask the user for a task number and return its index."""
    while True:
        value = input("Enter a task number, or q to cancel: ").strip()

        if value.lower() == "q":
            return None

        if not value.isdigit():
            print("Please enter a number.")
            continue

        index = int(value) - 1

        if 0 <= index < len(tasks):
            return index

        print("That task number is out of range.")


def mark_task_complete(tasks):
    """Mark a selected task as completed."""
    if is_empty(tasks):
        print("No tasks to mark.")
        return

    display_tasks(tasks)

    task_index = ask_for_task_index(tasks)

    if task_index is None:
        print("Operation cancelled.")
        return

    if tasks[task_index]["status"] == "completed":
        print("That task is already completed.")
    else:
        tasks[task_index]["status"] = "completed"
        print(
            f'Task "{tasks[task_index]["description"]}" '
            "marked as completed."
        )


def delete_task(tasks):
    """Delete a selected task."""
    if is_empty(tasks):
        print("No tasks to delete.")
        return

    display_tasks(tasks)

    task_index = ask_for_task_index(tasks)

    if task_index is None:
        print("Operation cancelled.")
        return

    removed = tasks.pop(task_index)

    print(f'Deleted: "{removed["description"]}"')


def search_tasks(tasks, keyword):
    """Return tasks whose descriptions contain the keyword."""
    keyword = keyword.strip().lower()

    return [
        task for task in tasks
        if keyword in task["description"].lower()
    ]


def main():
    """Run the Task Manager."""
    tasks = []

    print("=== Task Manager ===")

    while True:
        print("\nWhat would you like to do?")
        print("1. Add a task")
        print("2. View tasks")
        print("3. Mark a task as complete")
        print("4. Delete a task")
        print("5. Search tasks")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

        if choice == "1":
            add_task(tasks)

        elif choice == "2":
            display_tasks(tasks)

        elif choice == "3":
            mark_task_complete(tasks)

        elif choice == "4":
            delete_task(tasks)

        elif choice == "5":
            if is_empty(tasks):
                print("Your task list is empty.")
                continue

            keyword = input("Enter a keyword to search: ")

            matches = search_tasks(tasks, keyword)

            if is_empty(matches):
                print(f'No tasks found containing "{keyword}".')
            else:
                print(f'\n--- Search Results for "{keyword}" ---')
                display_tasks(matches)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")


main()