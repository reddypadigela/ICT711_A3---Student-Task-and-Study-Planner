from datetime import date, datetime

# task priorities
PRIORITIES = ("High", "Medium", "Low")

# text validation
def validate_text(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return value.strip()

# date validation
def parse_due_date(value):
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        raise ValueError("Enter a valid date in YYYY-MM-DD format.")

# priority validation
def validate_priority(priority):
    if not isinstance(priority, str):
        raise ValueError("Priority must be High, Medium, or Low.")
    for allowed_priority in PRIORITIES:
        if priority.lower() == allowed_priority.lower():
            return allowed_priority
    raise ValueError("Priority must be High, Medium, or Low.")

# function to find task
def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

# function to add task
def add_task(tasks, title, subject, due_date, priority):
    # user inputs
    title = validate_text(title, "Task title")
    subject = validate_text(subject, "Subject")
    due_date = parse_due_date(due_date)
    priority = validate_priority(priority)

    next_id = max((task["id"] for task in tasks), default=0) + 1
    task = {
        "id": next_id,
        "title": title,
        "subject": subject,
        "due_date": due_date,
        "priority": priority,
        "completed": False,
    }
    tasks.append(task)
    return task

# function to update task
def update_task(tasks, task_id, title, subject, due_date, priority):
    task = find_task(tasks, task_id)
    if task is None:
        return False

    task["title"] = validate_text(title, "Task title")
    task["subject"] = validate_text(subject, "Subject")
    task["due_date"] = parse_due_date(due_date)
    task["priority"] = validate_priority(priority)
    return True

# function to delete task
def delete_task(tasks, task_id):
    task = find_task(tasks, task_id)
    if task is None:
        return False

    tasks.remove(task)
    return True

# function to mark task as completed
def mark_completed(tasks, task_id):
    task = find_task(tasks, task_id)
    if task is None:
        return False

    task["completed"] = True
    return True

# search tasks by task title and subjects
def search_tasks(tasks, keyword):
    keyword = validate_text(keyword, "Search keyword").lower()
    # FIXED: Added space before 'if' and 'or'
    return [task for task in tasks if keyword in task["title"].lower() or keyword in task["subject"].lower()]

# get overdue tasks
def get_overdue_tasks(tasks, today=None):
    if today is None:
        today = date.today()

    # FIXED: Added space before 'if'
    return [task for task in tasks if not task["completed"] and task["due_date"] < today]

# function to show task progress
def get_progress(tasks):
    total = len(tasks)
    completed = sum(task["completed"] for task in tasks)
    pending = total - completed
    percentage = (completed / total * 100) if total else 0.0

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "percentage": round(percentage, 2),
    }

# function to display tasks
def display_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"
        print("-" * 45)
        print(f"ID: {task['id']}")
        print(f"Title: {task['title']}")
        print(f"Subject: {task['subject']}")
        print(f"Due date: {task['due_date']}")
        print(f"Priority: {task['priority']}")
        print(f"Status: {status}")
    print("-" * 45)

# function to read task id
def read_task_id():
    try:
        task_id = int(input("Enter task ID: "))
        if task_id < 1:
            raise ValueError
        return task_id
    except ValueError:
        print("Task ID must be a positive whole number.")
        return None

# function to read the task details
def read_task_details():
    title = input("Task title: ")
    subject = input("Subject: ")
    due_date = input("Due date (YYYY-MM-DD): ")
    priority = input("Priority (High/Medium/Low): ")

    return title, subject, due_date, priority

# it collects the task details and add task details
def add_task_menu(tasks):
    try:
        details = read_task_details()
        task = add_task(tasks, *details)
        print(f"Task {task['id']} added successfully.")
    except ValueError as error:
        print(f"Error: {error}")

# function to collect task details to update
def update_task_menu(tasks):
    task_id = read_task_id()
    if task_id is None:
        return

    if find_task(tasks, task_id) is None:
        print("Task not found.")
        return

    try:
        details = read_task_details()
        if update_task(tasks, task_id, *details):
            print("Task updated successfully.")
    except ValueError as error:
        print(f"Error: {error}")

# display progress report
def show_progress(tasks):
    report = get_progress(tasks)
    print("\nProgress Report: ")
    print(f"Total tasks: {report['total']}")
    print(f"Completed: {report['completed']}")
    print(f"Pending: {report['pending']}")
    print(f"Completion: {report['percentage']}%")

# function to display menu items
def show_menu():
    print("\n" + "=" * 40)
    print("     STUDENT TASK AND STUDY PLANNER")
    print("=" * 40)
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Search Tasks")
    print("4. Update Task")
    print("5. Delete Task")
    print("6. Mark Task as Completed")
    print("7. View Overdue Tasks")
    print("8. View Progress Report")
    print("9. Exit")
    print("=" * 40)


# function to run the application
def main():
    tasks = []

    while True:
        show_menu()
        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            add_task_menu(tasks)

        elif choice == "2":
            display_tasks(tasks)

        elif choice == "3":
            try:
                keyword = input("Enter title or subject to search: ")
                display_tasks(search_tasks(tasks, keyword))
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "4":
            update_task_menu(tasks)

        elif choice == "5":
            task_id = read_task_id()
            if task_id is not None:
                if delete_task(tasks, task_id):
                    print("Task deleted successfully.")
                else:
                    print("Task not found.")

        elif choice == "6":
            task_id = read_task_id()
            if task_id is not None:
                if mark_completed(tasks, task_id):
                    print("Task marked as completed.")
                else:
                    print("Task not found.")

        elif choice == "7":
            display_tasks(get_overdue_tasks(tasks))

        elif choice == "8":
            show_progress(tasks)

        elif choice == "9":
            print("Thank you for using the Study Planner.")
            break

        else:
            print("Invalid choice. Enter a number from 1 to 9.")


if __name__ == "__main__":
    main()
