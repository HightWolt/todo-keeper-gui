import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, END
import os

# Файл для хранения задач
TASK_FILE = "tasks.txt"

# Загрузка задач из файла
def load_tasks():
    tasks = []
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            tasks = [line.strip() for line in f if line.strip()]
    return tasks

# Сохранение задач в файл
def save_tasks(tasks):
    with open(TASK_FILE, "w", encoding="utf-8") as f:
            for task in tasks:
                f.write(task + "\n")

# Основное окно
root = tk.Tk()
root.title("Хранитель Полезных Дел")
root.geometry("400x400")
root.iconbitmap("icon.ico")

# Список задач (в памяти)
tasks = load_tasks()

# Функция: добавить задачу
def add_task():
    task = entry.get().strip()
    if task:
        tasks.append(task)
        listbox.insert(END, task)
        entry.delete(0, END)
        save_tasks(tasks)
    else:
        messagebox.showwarning("Внимание", "Введите задачу!")

# Функция: обновить список при запуске
def refresh_list():
    for task in tasks:
        listbox.insert(END, task)

# Элементы интерфейса
frame = tk.Frame(root)
frame.pack(pady=10)

entry = tk.Entry(frame, width=30, font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(frame, text="Добавить", command=add_task, font=("Arial", 10))
add_button.pack(side=tk.LEFT)

# Список задач с прокруткой
list_frame = tk.Frame(root)
list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = Listbox(list_frame, font=("Arial", 11), yscrollcommand=scrollbar.set)
listbox.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox.yview)

# Загружаем задачи в список
refresh_list()

# Запуск окна
root.mainloop()