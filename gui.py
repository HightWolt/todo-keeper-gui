import tkinter as tk
from typing import List
from tkinter import messagebox, Listbox, Scrollbar, END
from storage import save_tasks


# Создание GUI
def create_gui(tasks: List[str]) -> tk.Tk:
    # Цветовые схемы
    THEMES = {
        "light": {
            "bg": "#ffffff",
            "fg": "#000000",
            "listbox_bg": "#ffffff",
            "listbox_fg": "#000000",
            "button_bg": "#e0e0e0",
            "button_fg": "#000000",
        },
        "dark": {
            "bg": "#2d2d2d",
            "fg": "#ffffff",
            "listbox_bg": "#3c3f41",
            "listbox_fg": "#ffffff",
            "button_bg": "#5a5a5a",
            "button_fg": "#ffffff",
        },
    }
    current_theme = "light"

    # Функция: применения темы
    def apply_theme(theme_name):
        nonlocal current_theme
        current_theme = theme_name
        theme = THEMES[theme_name]

        # Основное окно
        root.config(bg=theme["bg"])

        # Фреймы
        frame.config(bg=theme["bg"])
        search_frame.config(bg=theme["bg"])
        list_frame.config(bg=theme["bg"])

        # Метки
        for widget in [entry, search_entry, listbox]:
            widget.config(bg=theme["listbox_bg"], fg=theme["listbox_fg"])
        # Метка "Поиск:"
        for child in search_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.config(bg=theme["bg"], fg=theme["fg"])

        # Кнопки
        for btn in [add_btn, delete_btn, sort_btn, theme_btn]:
            btn.config(
                bg=theme["button_bg"],
                fg=theme["button_fg"],
                activebackground=theme["button_bg"],
            )

    root = tk.Tk()
    root.title("Хранитель Полезных Дел")
    root.geometry("600x600")
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
            widgets["listbox"].focus_set()
            update_status()
        else:
            messagebox.showwarning("Внимание", "Введите задачу!")

    # Функция: удалить задачу
    def delete_task():
        selected = widgets["listbox"].curselection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите задачу для удаления!")
            return
        displayed_task = widgets["listbox"].get(selected[0])

        # Подтверждение
        confirm = messagebox.askyesno(
            "Подтверждение", f"Удалить задачу?\n«{displayed_task}»"
        )
        if confirm:
            if displayed_task in tasks:
                tasks.remove(displayed_task)
                save_tasks(tasks)
                filter_tasks()
                update_status()

    # Функция: редактировать задачу
    def edit_task(event=None):
        selected = widgets["listbox"].curselection()
        if not selected:
            return
        old_task = widgets["listbox"].get(selected[0])

        # Создаём временное окно ввода
        edit_window = tk.Toplevel(root)
        edit_window.title("Редактировать задачу")
        edit_window.geometry("300x120")
        edit_window.transient(root)
        edit_window.grab_set()

        tk.Label(edit_window, text="Измените задачу:", font=("Arial", 10)).pack(pady=5)
        edit_entry = tk.Entry(edit_window, width=35, font=("Arial", 11))
        edit_entry.pack(pady=5)
        edit_entry.insert(0, old_task)
        edit_entry.select_range(0, tk.END)
        edit_entry.focus()

        def save_edit():
            new_task = edit_entry.get().strip()
            if new_task:
                if old_task in tasks:
                    idx = tasks.index(old_task)
                    tasks[idx] = new_task
                    save_tasks(tasks)
                    filter_tasks()
                    update_status()
            edit_window.destroy()

        tk.Button(
            edit_window, text="Сохранить", command=save_edit, font=("Arial", 10)
        ).pack(pady=5)

    # Функция: сортировка задач
    def sort_tasks():
        tasks.sort(key=str.lower)
        save_tasks(tasks)
        filter_tasks()
        update_status()

    def update_status():
        count = len(tasks)
        status_label.config(text=f"Всего задач: {count}")

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

    sort_btn = tk.Button(
        frame, text="Сортировать", command=sort_tasks, font=("Arial", 10), fg="blue"
    )
    sort_btn.pack(side=tk.LEFT, padx=5)

    theme_btn = tk.Button(
        frame,
        text="🌙",
        command=lambda: apply_theme("dark" if current_theme == "light" else "light"),
        font=("Arial", 10),
        width=3,
    )
    theme_btn.pack(side=tk.LEFT, padx=2)
    widgets["theme_btn"] = theme_btn

    # Поле поиска
    search_frame = tk.Frame(root)
    search_frame.pack(pady=5, padx=10, fill=tk.X)
    tk.Label(search_frame, text="Поиск:", font=("Arial", 10)).pack(side=tk.LEFT)
    search_entry = tk.Entry(search_frame, font=("Arial", 11))
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    widgets["search_entry"] = search_entry

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

    # Статусная панель
    status_label = tk.Label(
        root, text="", anchor="w", padx=10, pady=5, font=("Arial", 9)
    )
    status_label.pack(side=tk.BOTTOM, fill=tk.X)
    widgets["status_label"] = status_label

    # Загрузка задач в список
    for task in tasks:
        listbox.insert(END, task)

    # Функция: поиск задач
    def filter_tasks(event=None):
        query = search_entry.get().strip().lower()
        listbox = widgets["listbox"]
        listbox.delete(0, END)
        if not query:
            for task in tasks:
                listbox.insert(END, task)
        else:
            for task in tasks:
                if query in task.lower():
                    listbox.insert(END, task)

    search_entry.bind("<KeyRelease>", filter_tasks)

    # Горячие клавиши
    # Добавить: Enter
    root.bind("<Return>", lambda event: add_task())
    # Удалить: Delete
    root.bind("<Delete>", lambda event: delete_task())
    # Редактировать: Ctrl+E
    root.bind("<Control-e>", lambda event: edit_task())
    # Сортировать: Ctrl+S
    root.bind("<Control-s>", lambda event: sort_tasks())
    # Переключение темы: Ctrl+T
    root.bind(
        "<Control-t>",
        lambda event: apply_theme("dark" if current_theme == "light" else "light"),
    )

    widgets["listbox"].focus_set()

    apply_theme("light")

    update_status()

    return root
