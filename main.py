from storage import load_tasks
from gui import create_gui

# === ТОЧКА ВХОДА ===
if __name__ == "__main__":
    tasks = load_tasks()
    app = create_gui(tasks)
    app.mainloop()
