# task_manager_v1_exercise.py
#page8
tasks = ["Learn Python", "Build a Task Manager"]

print("Tasks before addition:")
print(tasks)

new_task = input("Enter one more task: ")
tasks.append(new_task)

print("\nTasks after addition:")
print(tasks)