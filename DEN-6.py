import json

# Load tasks from file
def load_tasks(filename="tasks.json"):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save tasks to file
def save_tasks(tasks, filename="tasks.json"):
    with open(filename, 'w') as file:
        json.dump(tasks, file)

# Add task
def add_task(tasks):
    task_id = len(tasks) + 1
    description = input("Enter task description: ")
    tasks.append({"id": task_id, "description": description, "status": "pending"})
    save_tasks(tasks)
    print(f"Task added with ID: {task_id}")

# View tasks
def view_tasks(tasks):
    if not tasks:
        print("No tasks to display.")
    else:
        print("\nID  | Description          | Status")
        print("----------------------------------")
        for task in tasks:
            print(f"{task['id']}   | {task['description']:<20} | {task['status']}")

# Remove task
def remove_task(tasks):
    task_id = int(input("Enter task ID to remove: "))
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    print(f"Task with ID {task_id} removed.")
    return tasks

# Mark task as completed
def mark_task_completed(tasks):
    task_id = int(input("Enter task ID to mark as completed: "))
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'completed'
            save_tasks(tasks)
            print(f"Task {task_id} marked as completed.")
            return
    print(f"Task with ID {task_id} not found.")

# Edit task description
def edit_task(tasks):
    task_id = int(input("Enter task ID to edit: "))
    for task in tasks:
        if task['id'] == task_id:
            new_description = input("Enter new description: ")
            task['description'] = new_description
            save_tasks(tasks)
            print(f"Task {task_id} updated.")
            return
    print(f"Task with ID {task_id} not found.")

# Search tasks by keyword
def search_task(tasks):
    keyword = input("Enter keyword to search: ").lower()
    filtered_tasks = [task for task in tasks if keyword in task['description'].lower()]
    view_tasks(filtered_tasks)

# Filter tasks by status
def filter_tasks(tasks):
    status = input("Enter status to filter by (pending/completed): ").lower()
    filtered_tasks = [task for task in tasks if task['status'] == status]
    view_tasks(filtered_tasks)

# Clear all tasks
def clear_all_tasks(tasks):
    confirm = input("Are you sure you want to clear all tasks? (yes/no): ").lower()
    if confirm == 'yes':
        tasks.clear()
        save_tasks(tasks)
        print("All tasks cleared.")
    else:
        print("Operation canceled.")
    return tasks

# Sort tasks by ID or status
def sort_tasks(tasks):
    choice = input("Sort by (id/status): ").lower()
    if choice == "id":
        tasks.sort(key=lambda x: x['id'])
    elif choice == "status":
        tasks.sort(key=lambda x: x['status'])
    else:
        print("Invalid choice.")
    view_tasks(tasks)

# Menu function to interact with user
def menu():
    tasks = load_tasks()
    while True:
        print("\n1. Add Task\n2. View Tasks\n3. Remove Task\n4. Mark as Completed\n5. Edit Task\n6. Search Task\n7. Filter Tasks\n8. Clear All Tasks\n9. Sort Tasks\n0. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            tasks = remove_task(tasks)
        elif choice == '4':
            mark_task_completed(tasks)
        elif choice == '5':
            edit_task(tasks)
        elif choice == '6':
            search_task(tasks)
        elif choice == '7':
            filter_tasks(tasks)
        elif choice == '8':
            tasks = clear_all_tasks(tasks)
        elif choice == '9':
            sort_tasks(tasks)
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
