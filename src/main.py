"""Эмулятор UNIX-оболочки с графическим интерфейсом (этап 1: REPL)."""

import getpass
import socket
import sys
import tkinter as tk

BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#fe14ee"
FONT = ("Courier", 12)


def get_user_and_host():
    """Возвращает имя пользователя и имя компьютера из реальной ОС."""
    try:
        username = getpass.getuser()
    except Exception:
        username = "user"
    try:
        hostname = socket.gethostname()
    except Exception:
        hostname = "localhost"
    return username, hostname


def parse_command(line):
    """Разделяет строку ввода на команду и аргументы по пробелам."""
    tokens = line.split()
    return tokens[0], tokens[1:]


def execute(command, args):
    """Выполняет команду и возвращает текст вывода.

    Для команды exit без аргументов возвращает None — сигнал к выходу.
    """
    if command == "exit":
        if args:
            return "shell-emulator: exit: too many arguments\n"
        return None
    if command in ["ls", "cd"]:
        args_str = " ".join(args) if args else "[нет аргументов]"
        return (
            f"Вызвана заглушка команды: {command}\n"
            f"Переданные аргументы: {args_str}\n"
        )
    return f"shell-emulator: command not found: {command}\n"


class TerminalEmulator:
    """Окно эмулятора: область вывода, поле ввода и кнопка Enter."""

    def __init__(self, root):
        """Создаёт окно с заголовком вида Эмулятор - [user@host]."""
        self.root = root
        self.username, self.hostname = get_user_and_host()

        self.root.title(f"Эмулятор - [{self.username}@{self.hostname}]")
        self.root.geometry("750x450")
        self.root.configure(bg=BG_COLOR)

        self.build_output_area()
        self.build_input_area()

        self.print_to_console(
            "Имитатор UNIX-оболочки загружен.\n"
            f"Система: {sys.platform}\n"
            "Введите 'exit' для выхода.\n\n"
        )

    def build_output_area(self):
        """Создаёт область для отображения команд и их вывода."""
        self.text_area = tk.Text(
            self.root,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            insertbackground="white",
            font=FONT,
            wrap="word",
        )
        self.text_area.pack(expand=True, fill="both", padx=10, pady=(10, 5))
        self.text_area.bind("<Key>", lambda e: "break")

    def build_input_area(self):
        """Создаёт поле ввода команды и кнопку Enter."""
        bottom_frame = tk.Frame(self.root, bg=BG_COLOR)
        bottom_frame.pack(fill="x", padx=10, pady=(0, 10))
        bottom_frame.columnconfigure(0, weight=1)

        self.entry = tk.Entry(
            bottom_frame,
            bg="#2d2d2d",
            fg=TEXT_COLOR,
            insertbackground="white",
            font=FONT,
            bd=0,
            highlightthickness=1,
            highlightbackground="#555555",
            highlightcolor=ACCENT_COLOR,
        )
        self.entry.grid(row=0, column=0, sticky="ew", ipady=6, padx=(0, 10))
        self.entry.focus_set()
        self.entry.bind("<Return>", lambda event: self.process_command())

        enter_button = tk.Button(
            bottom_frame,
            text="Enter",
            bg="#3a3a3a",
            fg=ACCENT_COLOR,
            activebackground=ACCENT_COLOR,
            activeforeground=BG_COLOR,
            font=("Courier", 11, "bold"),
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.process_command,
        )
        enter_button.grid(row=0, column=1, sticky="ns", ipadx=20)

    def print_to_console(self, text):
        """Добавляет текст в конец области вывода."""
        self.text_area.configure(state="normal")
        self.text_area.insert(tk.END, text)
        self.text_area.configure(state="disabled")
        self.text_area.see(tk.END)

    def process_command(self):
        """Считывает команду из поля ввода, выполняет её и выводит результат."""
        line = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        self.print_to_console(f"{self.username}@{self.hostname}:~$ {line}\n")
        if not line:
            return

        command, args = parse_command(line)
        output = execute(command, args)
        if output is None:
            self.root.destroy()
        else:
            self.print_to_console(output + "\n")


if __name__ == "__main__":
    main_window = tk.Tk()
    TerminalEmulator(main_window)
    main_window.mainloop()
