import os
from typing import List
from tkinter import messagebox

# Файл по умолчанию для хранения задач
TASK_FILE = "tasks.txt"


def load_tasks(filename: str = TASK_FILE, show_errors: bool = True) -> List[str]:
    """Загружает задачи из указанного файла. Пробелы по краям удаляются, пустые строки игнорируются."""
    tasks: List[str] = []
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                tasks = [line.strip() for line in f if line.strip()]
    except (IOError, OSError) as e:
        if show_errors:
            from tkinter import messagebox

            messagebox.showerror("Ошибка", f"Не удалось загрузить задачи:\n{e}")
    return tasks


def save_tasks(
    tasks: List[str], filename: str = TASK_FILE, show_errors: bool = True
) -> None:
    """Сохраняет список задач в указанный файл."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for task in tasks:
                f.write(task + "\n")
    except (IOError, OSError) as e:
        if show_errors:
            from tkinter import messagebox

            messagebox.showerror("Ошибка", f"Не удалось сохранить задачи:\n{e}")
