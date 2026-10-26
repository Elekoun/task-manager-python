"""
Task Manager — command-line application.

Add, view, edit, delete and prioritise personal tasks. Tasks are saved in a
JSON file between sessions, a weighted productivity score tracks progress,
and the list can be exported to Excel with pandas.

Run:  python task_manager.py
"""

import json
import os

TASKS_FILE = "tasks.json"
EXCEL_FILE = "tasks.xlsx"

PRIORITIES = ["low", "medium", "high"]
STATUSES = ["todo", "in progress", "done"]
PRIORITY_ORDER = {"high": 1, "medium": 2, "low": 3}
PRIORITY_WEIGHT = {"high": 3, "medium": 2, "low": 1}


# ---------- Storage ----------

def load_tasks():
    """Load tasks from the JSON file, or start with an empty list."""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2, ensure_ascii=False)


# ---------- Input helpers ----------

def ask_choice(prompt, options, allow_blank=False):
    """Ask until the answer is one of the allowed options."""
    while True:
        answer = input(f"{prompt} ({'/'.join(options)}): ").strip().lower()
        if answer in options or (allow_blank and answer == ""):
            return answer
        print(f"Please type one of: {', '.join(options)}")


def ask_index(tasks, prompt):
    """Ask for a valid task number; return None if the list is empty."""
    if not tasks:
        print("No tasks yet.")
        return None
    while True:
        answer = input(f"{prompt} (0-{len(tasks) - 1}): ").strip()
        if answer.isdigit() and int(answer) < len(tasks):
            return int(answer)
        print("Invalid task number.")


# ---------- Display ----------

def print_table(tasks):
    print(f"\n{'#':<5}{'Title':<32}{'Priority':<10}{'Status':<14}{'Deadline'}")
    print("-" * 72)
    for i, task in enumerate(tasks):
        title = task["title"] if len(task["title"]) <= 30 else task["title"][:29] + "…"
        print(f"{i:<5}{title:<32}{task['priority']:<10}{task['status']:<14}{task['deadline']}")


# ---------- Actions ----------

def add_task(tasks):
    task = {
        "title": input("Title: ").strip(),
        "priority": ask_choice("Priority", PRIORITIES),
        "status": "todo",
        "deadline": input("Deadline (YYYY-MM-DD): ").strip(),
    }
    tasks.append(task)
    print("Task added.")


def mark_done(tasks):
    print_table(tasks)
    index = ask_index(tasks, "Task number")
    if index is not None:
        tasks[index]["status"] = "done"
        print("Marked as done.")


def delete_task(tasks):
    print_table(tasks)
    index = ask_index(tasks, "Task to delete")
    if index is not None:
        removed = tasks.pop(index)
        print(f"Deleted: {removed['title']}")


def edit_task(tasks):
    print_table(tasks)
    index = ask_index(tasks, "Task to edit")
    if index is None:
        return
    task = tasks[index]
    print("Leave blank to keep the current value.")
    title = input(f"Title ({task['title']}): ").strip()
    priority = ask_choice(f"Priority [{task['priority']}]", PRIORITIES, allow_blank=True)
    status = ask_choice(f"Status [{task['status']}]", STATUSES, allow_blank=True)
    deadline = input(f"Deadline ({task['deadline']}): ").strip()
    if title:
        task["title"] = title
    if priority:
        task["priority"] = priority
    if status:
        task["status"] = status
    if deadline:
        task["deadline"] = deadline
    print("Task updated.")


def show_by_priority(tasks):
    """Active tasks first, sorted by priority then deadline; done tasks below."""
    def sort_key(task):
        return (PRIORITY_ORDER.get(task["priority"], 4), task["deadline"])

    active = sorted([t for t in tasks if t["status"] != "done"], key=sort_key)
    done = sorted([t for t in tasks if t["status"] == "done"], key=sort_key)

    print_table(active)
    if done:
        print("\n--- DONE ---")
        print_table(done)


def productivity_report(tasks):
    """Completion rate and a productivity score weighted by priority."""
    total = len(tasks)
    if total == 0:
        print("No tasks found.")
        return

    done = sum(1 for t in tasks if t["status"] == "done")
    score = sum(PRIORITY_WEIGHT.get(t["priority"], 1) for t in tasks if t["status"] == "done")
    max_score = sum(PRIORITY_WEIGHT.get(t["priority"], 1) for t in tasks)

    print("\nPRODUCTIVITY REPORT")
    print("-" * 30)
    print(f"Total tasks    : {total}")
    print(f"Completed      : {done}")
    print(f"Remaining      : {total - done}")
    print(f"Completion     : {done / total * 100:.1f}%")
    print(f"Productivity   : {score / max_score * 100:.1f}%")


def export_to_excel(tasks):
    import pandas as pd
    pd.DataFrame(tasks).to_excel(EXCEL_FILE, index=False)
    print(f"Exported to {EXCEL_FILE}")


# ---------- Menu ----------

MENU = {
    "1": ("Add task", add_task),
    "2": ("Show tasks", print_table),
    "3": ("Mark as done", mark_done),
    "4": ("Delete task", delete_task),
    "5": ("Edit task", edit_task),
    "6": ("Show by priority", show_by_priority),
    "7": ("My productivity", productivity_report),
    "8": ("Export to Excel", export_to_excel),
}


def main():
    tasks = load_tasks()
    while True:
        print("\nTASK MANAGER")
        for key, (label, _) in MENU.items():
            print(f"{key} {label}")
        print("9 Save and exit")

        choice = input("Choice: ").strip()
        if choice == "9":
            save_tasks(tasks)
            print("Tasks saved. Goodbye!")
            break
        if choice in MENU:
            MENU[choice][1](tasks)
            save_tasks(tasks)  # save after every action so nothing is lost
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
