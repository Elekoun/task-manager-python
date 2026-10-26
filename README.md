# Task Manager — Python command-line app

A small interactive task manager built step by step in Python. It lets you add, view, edit, delete and prioritise personal tasks, saves them between sessions, measures a priority-weighted productivity score, and exports the list to Excel.

## Features

- **Add, edit, delete** tasks, each with a title, priority (`low` / `medium` / `high`), status (`todo` / `in progress` / `done`) and deadline
- **Mark tasks as done**
- **Sort by priority**: active tasks first, ordered by priority then deadline, with completed tasks listed below
- **Productivity report**: completion rate plus a score weighted by priority (high = 3, medium = 2, low = 1), so finishing important tasks counts more
- **Persistence**: tasks are saved to a JSON file and reloaded at startup
- **Excel export** with pandas

## Example

```
TASK MANAGER
1 Add task
2 Show tasks
3 Mark as done
4 Delete task
5 Edit task
6 Show by priority
7 My productivity
8 Export to Excel
9 Save and exit
Choice: 7

PRODUCTIVITY REPORT
------------------------------
Total tasks    : 5
Completed      : 3
Remaining      : 2
Completion     : 60.0%
Productivity   : 64.3%
```

## Run it

```bash
pip install -r requirements.txt
python task_manager.py
```

A `tasks.json` file is created on first save. It is excluded from the repository because it holds your personal tasks.

## Repository structure

```
├── task_manager.py              # The application, as a standalone script
├── Task_Manager_Project.ipynb   # Notebook showing how the app was built, step by step
├── requirements.txt
└── .gitignore
```

The **notebook** documents the development path: storing one task in a dictionary, looping to add several, updating and deleting by index, saving to JSON, assembling the full menu, then exporting to Excel.

The **script** is the finished version of the same app, organised into functions with input validation (invalid task numbers or priorities are re-asked instead of crashing) and automatic saving after each action.

## Skills demonstrated

Python fundamentals (lists, dictionaries, loops, functions) · JSON persistence · Sorting with custom keys · Input validation · pandas · Excel export
