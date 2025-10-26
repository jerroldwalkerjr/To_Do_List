import tkinter as tk
from tkinter import ttk, messagebox
import json

# Create main window
root = tk.Tk()
root.title("To-Do List")
root.geometry("500x700")

# --- Input Section ---

# Task entry
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=10)
task_entry.bind("<Return>", lambda event: add_task())
root.bind("<BackSpace>", lambda event: remove_task())



# Category dropdown
category_var = tk.StringVar(value="Daily")
category_menu = ttk.Combobox(root, textvariable=category_var, state="readonly")
category_menu['values'] = ("Daily", "Weekly", "Monthly")
category_menu.pack(pady=5)

# --- Task Lists ---

tk.Label(root, text="Daily Tasks", font=('Arial', 12, 'bold')).pack(pady=(10, 0))
daily_listbox = tk.Listbox(root, width=60, height=6)
daily_listbox.pack(pady=5)

tk.Label(root, text="Weekly Tasks", font=('Arial', 12, 'bold')).pack(pady=(10, 0))
weekly_listbox = tk.Listbox(root, width=60, height=6)
weekly_listbox.pack(pady=5)

tk.Label(root, text="Monthly Tasks", font=('Arial', 12, 'bold')).pack(pady=(10, 0))
monthly_listbox = tk.Listbox(root, width=60, height=6)
monthly_listbox.pack(pady=5)

daily_listbox.bind("<Double-Button-1>", lambda e: toggle_task(e, daily_listbox))
weekly_listbox.bind("<Double-Button-1>", lambda e: toggle_task(e, weekly_listbox))
monthly_listbox.bind("<Double-Button-1>", lambda e: toggle_task(e, monthly_listbox))


# --- Functions ---

def add_task():
    task = task_entry.get()
    category = category_var.get()
    if task:
        item = f"[ ] {task}"  # default unchecked
        if category == "Daily":
            daily_listbox.insert(tk.END, item)
        elif category == "Weekly":
            weekly_listbox.insert(tk.END, item)
        elif category == "Monthly":
            monthly_listbox.insert(tk.END, item)
        task_entry.delete(0, tk.END)

def remove_task():
    category = category_var.get()
    if category == "Daily":
        selected = daily_listbox.curselection()
        for index in reversed(selected):
            daily_listbox.delete(index)
    elif category == "Weekly":
        selected = weekly_listbox.curselection()
        for index in reversed(selected):
            weekly_listbox.delete(index)
    elif category == "Monthly":
        selected = monthly_listbox.curselection()
        for index in reversed(selected):
            monthly_listbox.delete(index)

def toggle_task(event, listbox):
    index = listbox.curselection()
    if not index:
        return
    current = listbox.get(index)
    if current.startswith("[ ]"):
        updated = current.replace("[ ]", "[✔]", 1)
    elif current.startswith("[✔]"):
        updated = current.replace("[✔]", "[ ]", 1)
    else:
        return
    listbox.delete(index)
    listbox.insert(index, updated)


def clear_tasks():
    confirm = messagebox.askyesno("Confirm", "Clear all tasks?")
    if confirm:
        daily_listbox.delete(0, tk.END)
        weekly_listbox.delete(0, tk.END)
        monthly_listbox.delete(0, tk.END)

def save_tasks():
    data = {
        "Daily": daily_listbox.get(0, tk.END),
        "Weekly": weekly_listbox.get(0, tk.END),
        "Monthly": monthly_listbox.get(0, tk.END),
    }
    with open("tasks.json", "w") as file:
        json.dump(data, file)

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            data = json.load(file)
            for task in data.get("Daily", []):
                daily_listbox.insert(tk.END, task)
            for task in data.get("Weekly", []):
                weekly_listbox.insert(tk.END, task)
            for task in data.get("Monthly", []):
                monthly_listbox.insert(tk.END, task)
    except FileNotFoundError:
        pass

# --- Buttons ---

add_button = tk.Button(root, text="Add Task", width=20, command=add_task)
add_button.pack(pady=5)

remove_button = tk.Button(root, text="Remove Selected", width=20, command=remove_task)
remove_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear All Tasks", width=20, command=clear_tasks)
clear_button.pack(pady=5)

save_button = tk.Button(root, text="Save Tasks", width=20, command=save_tasks)
save_button.pack(pady=5)

load_button = tk.Button(root, text="Load Tasks", width=20, command=load_tasks)
load_button.pack(pady=5)

# --- Run the App ---
load_tasks()  # Load any saved tasks on startup
root.mainloop()
