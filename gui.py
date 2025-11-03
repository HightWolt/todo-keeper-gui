import tkinter as tk
from typing import List
from tkinter import messagebox, Listbox, Scrollbar, END
from storage import save_tasks


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

    # Функция: удалить задачу
    def delete_task():
        selected = widgets["listbox"].curselection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите задачу для удаления!")
            return
        index = selected[0]
        task_to_remove = tasks[index]

        # Подтверждение
        confirm = messagebox.askyesno(
            "Подтверждение", f"Удалить задачу?\n«{task_to_remove}»"
        )
        if confirm:
            # Удаляем из списка в памяти
            del tasks[index]
            # Удаляем из интерфейса
            widgets["listbox"].delete(index)
            # Сохраняем изменения
            save_tasks(tasks)

    # Функция: редактировать задачу
    def edit_task(event=None):
        selected = widgets["listbox"].curselection()
        if not selected:
            return
        index = selected[0]
        old_task = tasks[index]

        # Создаём временное окно ввода
        edit_window = tk.Toplevel(root)
        edit_window.title("Редактировать задачу")
        edit_window.geometry("300x120")
        edit_window.transient(root)
        edit_window.grab_set()

        tk.Label(edit_window, text="Измените задачу:", font=("Arial", 10))
        edit_entry = tk.Entry(edit_window, width=35, font=("Arial", 11))
        edit_entry.pack(pady=5)
        edit_entry.insert(0, old_task)
        edit_entry.select_range(0, tk.END)
        edit_entry.focus()

        def save_edit():
            new_task = edit_entry.get().strip()
            if new_task:
                tasks[index] = new_task
                widgets["listbox"].delete(index)
                widgets["listbox"].insert(index, new_task)
                save_tasks(tasks)
            edit_window.destroy()

        tk.Button(
            edit_window, text="Сохранить", command=save_edit, font=("Arial", 10)
        ).pack(pady=5)

    # Интерфейс
    frame = tk.Frame(root)
    frame.pack(pady=10)

    entry = tk.Entry(frame, width=30, font=("Arial", 12))
    entry.pack(side=tk.LEFT, padx=5)
    widgets["entry"] = entry

    add_btn = tk.Button(frame, text="Добавить", command=add_task, font=("Arial", 10))
    add_btn.pack(side=tk.LEFT)

    delete_btn = tk.Button(
        frame, text="Удалить", command=delete_task, font=("Arial", 10), fg="red"
    )
    delete_btn.pack(side=tk.LEFT, padx=5)

    # Список задач с прокруткой
    list_frame = tk.Frame(root)
    list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = Listbox(list_frame, font=("Arial", 11), yscrollcommand=scrollbar.set)
    listbox.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)
    widgets["listbox"] = listbox
    listbox.bind("<Double-1>", edit_task)

    # Загрузка задач в список
    for task in tasks:
        listbox.insert(END, task)

    return root
