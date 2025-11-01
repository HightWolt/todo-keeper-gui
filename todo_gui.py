import tkinter as tk
import os
from typing import List
from tkinter import messagebox, Listbox, Scrollbar, END

# Файл для хранения задач
TASK_FILE = "tasks.txt"


# Загрузка задач из файла
def load_tasks() -> List[str]:
    tasks: List[str] = []
    try:
        if os.path.exists(TASK_FILE):
            with open(TASK_FILE, "r", encoding="utf-8") as f:
                tasks = [line.strip() for line in f if line.strip()]
    except (IOError, OSError) as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить задачи:\n{e}")
    return tasks


# Сохранение задач в файл
def save_tasks(tasks: List[str]) -> None:
    try:
        with open(TASK_FILE, "w", encoding="utf-8") as f:
            for task in tasks:
                f.write(task + "\n")
    except (IOError, OSError) as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить задачи:\n{e}")


# Создание GUI
def create_gui(tasks: List[str]) -> tk.Tk:
    root = tk.Tk()
    root.title("Хранитель Полезных Дел")
    root.geometry("400x400")
    try:
        root.iconbitmap("icon.ico")
    except tk.TclError:
        # Иконка не найдена - просто пропускаем, окно без иконки
        pass

    # Храним ссылки на виджеты и данные
    widgets = {}

    # Функция: добавить задачу
    def add_task():
        task = widgets["entry"].get().strip()
        if task:
            tasks.append(task)
            widgets["listbox"].insert(END, task)
            widgets["entry"].delete(0, END)
            save_tasks(tasks)
        else:
            messagebox.showwarning("Внимание", "Введите задачу!")

    # Интерфейс
    frame = tk.Frame(root)
    frame.pack(pady=10)

    entry = tk.Entry(frame, width=30, font=("Arial", 12))
    entry.pack(side=tk.LEFT, padx=5)
    widgets["entry"] = entry

    add_btn = tk.Button(frame, text="Добавить", command=add_task, font=("Arial", 10))
    add_btn.pack(side=tk.LEFT)

    # Список задач с прокруткой
    list_frame = tk.Frame(root)
    list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = Listbox(list_frame, font=("Arial", 11), yscrollcommand=scrollbar.set)
    listbox.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)
    widgets["listbox"] = listbox

    # Загрузка задач в список
    for task in tasks:
        listbox.insert(END, task)

    return root


# === ТОЧКА ВХОДА ===
if __name__ == "__main__":
    tasks = load_tasks()
    app = create_gui(tasks)
    app.mainloop()
