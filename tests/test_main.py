"""Тесты парсера и команд эмулятора."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from main import execute, parse_command  # noqa: E402


class TestParser(unittest.TestCase):
    """Проверка разделения ввода на команду и аргументы."""

    def test_command_without_args(self):
        """Команда без аргументов."""
        self.assertEqual(parse_command("ls"), ("ls", []))

    def test_command_with_args(self):
        """Аргументы разделяются по пробелам, лишние пробелы игнорируются."""
        self.assertEqual(
            parse_command("cd   /home  user"), ("cd", ["/home", "user"])
        )


class TestCommands(unittest.TestCase):
    """Проверка команд-заглушек, exit и обработки ошибок."""

    def test_stub_prints_name_and_args(self):
        """Заглушка выводит своё имя и аргументы."""
        output = execute("ls", ["-l", "/home"])
        self.assertIn("ls", output)
        self.assertIn("-l /home", output)

    def test_stub_without_args(self):
        """Заглушка без аргументов."""
        self.assertIn("[нет аргументов]", execute("cd", []))

    def test_unknown_command(self):
        """Неизвестная команда — ошибка command not found."""
        self.assertIn("command not found: foo", execute("foo", []))

    def test_exit(self):
        """exit без аргументов — сигнал к выходу."""
        self.assertIsNone(execute("exit", []))

    def test_exit_with_args(self):
        """exit с аргументами — ошибка."""
        self.assertIn("too many arguments", execute("exit", ["1"]))


if __name__ == "__main__":
    unittest.main()
