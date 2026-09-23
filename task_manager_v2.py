tasks = []

print("=== Task Manager ===\n")

while True:
    print("\nWhat would you like to do?")
    print("1. Add a task")
    print("2. View tasks")
    print("3. Mark a task as complete")
    print("4. Exit")

    choice = input("\nEnter your choice (1-4): ")

    if choice == "1":
        # Add a task
        description = input("Enter the task description: ")
        task = {"description": description, "status": "pending"}
        tasks.append(task)
        print(f'Added: "{description}"')

    elif choice == "2":
        # View all tasks
        if len(tasks) == 0:
            print("Your task list is empty.")
        else:
            print("\n--- Your Tasks ---")
            for index, task in enumerate(tasks):
                print(
                    f"  {index + 1}. {task['description']} "
                    f"[{task['status']}]"
                )
            print("------------------")

    elif choice == "3":
        # Mark a task as complete
        if len(tasks) == 0:
            print("No tasks to mark.")
        else:
            # Show tasks first so user can see the numbers
            print("\n--- Your Tasks ---")
            for index, task in enumerate(tasks):
                print(
                    f"  {index + 1}. {task['description']} "
                    f"[{task['status']}]"
                )
            print("------------------")

            task_number = input("Enter the task number to mark complete: ")

            # input() returns a string, so we need to convert to an integer
            if task_number.isdigit():
                task_index = int(task_number) - 1

                if 0 <= task_index < len(tasks):
                    if tasks[task_index]["status"] == "completed":
                        print("That task is already completed.")
                    else:
                        tasks[task_index]["status"] = "completed"
                        print(
                            f'Marked "{tasks[task_index]["description"]}" '
                            f'as completed.'
                        )
                else:
                    print("Invalid task number.")
            else:
                print("Please enter a valid number.")

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")