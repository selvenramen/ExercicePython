# Task Manager

tasks = []

while True:
    print("\n===== TASK MANAGER =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Completed")
    print("5. Delete Task")
    print("0. Exit")

    choice = input("Enter your choice: ")

    # Add Task
    if choice == "1":
        description = input("Enter task description: ")

        task = {
            "description": description,
            "status": "Pending"
        }

        tasks.append(task)
        print("Task added successfully!")

    # View Tasks
    elif choice == "2":
        if len(tasks) == 0:
            print("No tasks found.")
        else:
            print("\n--- Your Tasks ---")

            for index, task in enumerate(tasks):
                print(f"{index + 1}. {task['description']} [{task['status']}]")

    # Mark Task Completed
    elif choice == "3":
        if len(tasks) == 0:
            print("No tasks available.")
        else:
            print("\n--- Your Tasks ---")

            for index, task in enumerate(tasks):
                print(f"{index + 1}. {task['description']} [{task['status']}]")

            task_number = input("Enter task number to mark as completed: ")

            if task_number.isdigit():
                task_index = int(task_number) - 1

                if 0 <= task_index < len(tasks):
                    tasks[task_index]["status"] = "Completed"
                    print("Task marked as completed.")
                else:
                    print("Invalid task number.")
            else:
                print("Please enter a valid number.")

    # Delete Task
    elif choice == "5":
        if len(tasks) == 0:
            print("No tasks to delete.")
        else:
            print("\n--- Your Tasks ---")

            for index, task in enumerate(tasks):
                print(f"{index + 1}. {task['description']} [{task['status']}]")

            print("------------------")

            task_number = input("Enter the task number to delete: ")

            if task_number.isdigit():
                task_index = int(task_number) - 1

                if 0 <= task_index < len(tasks):
                    removed = tasks.pop(task_index)
                    print(f'Deleted: "{removed["description"]}"')
                else:
                    print("Invalid task number.")
            else:
                print("Please enter a valid number.")

    # Exit
    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")