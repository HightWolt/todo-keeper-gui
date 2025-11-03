import unittest
import os
from storage import load_tasks, save_tasks


class TestTaskStorage(unittest.TestCase):

    def setUp(self):
        """Выплняется перед каждым тестом - создаём временный файл"""
        self.test_file = "test_tasks.txt"

    def tearDown(self):
        """Удаляем врменный файл после теста"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_empty_file(self):
        """Тест: загрузка из несуществующего файла - пустой список"""
        tasks = load_tasks(self.test_file, show_errors=False)
        self.assertEqual(tasks, [])

    def test_save_and_load_tasks(self):
        """Тест: сохранение и загрузка работают корректно"""
        original_tasks = ["Купить хлеб", "Выучить Python", "Создать игру"]
        save_tasks(original_tasks, self.test_file, show_errors=False)
        loaded_tasks = load_tasks(self.test_file, show_errors=False)
        self.assertEqual(loaded_tasks, original_tasks)

    def test_load_strips_whitespace(self):
        """Тест: пробелы в начале/конце строк удаляются"""
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(" Задача 1 \n\n Задача 2 \n")
        tasks = load_tasks(self.test_file, show_errors=False)
        expected = ["Задача 1", "Задача 2"]
        self.assertEqual(tasks, expected)

    def test_save_after_deletion(self):
        """Тест на удаление"""
        tasks = ["A", "B", "C"]
        save_tasks(tasks, self.test_file, show_errors=False)
        del tasks[1]
        save_tasks(tasks, self.test_file, show_errors=False)
        loaded = load_tasks(self.test_file, show_errors=False)
        self.assertEqual(loaded, ["A", "C"])


if __name__ == "__main__":
    unittest.main()
