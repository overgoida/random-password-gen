import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os


class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.history_file = "history.json"

        # Настройки интерфейса
        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        # Фрейм настроек
        settings_frame = ttk.LabelFrame(self.root, text="Настройки")
        settings_frame.pack(padx=10, pady=10, fill="x")

        # Длина пароля
        ttk.Label(settings_frame, text="Длина:").grid(row=0, column=0, padx=5)
        self.length_var = tk.IntVar(value=12)
        self.length_scale = ttk.Scale(settings_frame, from_=4, to=32, variable=self.length_var, orient="horizontal")
        self.length_scale.grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Label(settings_frame, textvariable=self.length_var).grid(row=0, column=2, padx=5)

        # Опции
        self.use_digits = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Цифры", variable=self.use_digits).grid(row=1, column=0)

        self.use_letters = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Буквы", variable=self.use_letters).grid(row=1, column=1)

        self.use_special = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="Спецсимволы", variable=self.use_special).grid(row=1, column=2)

        # Кнопка генерации
        ttk.Button(self.root, text="Сгенерировать пароль", command=self.generate).pack(pady=5)

        # Поле вывода
        self.result_entry = ttk.Entry(self.root, font=("Courier", 12), justify="center")
        self.result_entry.pack(padx=10, pady=5, fill="x")

        # Таблица истории
        ttk.Label(self.root, text="История:").pack()
        self.tree = ttk.Treeview(self.root, columns=("Password"), show="headings", height=5)
        self.tree.heading("Password", text="Пароль")
        self.tree.pack(padx=10, pady=10, fill="both")

    def generate(self):
        chars = ""
        if self.use_letters.get(): chars += string.ascii_letters
        if self.use_digits.get(): chars += string.digits
        if self.use_special.get(): chars += string.punctuation

        if not chars:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
            return

        length = self.length_var.get()
        password = "".join(random.choice(chars) for _ in range(length))

        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, password)
        self.save_to_history(password)

    def save_to_history(self, password):
        self.tree.insert("", 0, values=(password,))
        history = []
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                history = json.load(f)

        history.append(password)
        with open(self.history_file, "w") as f:
            json.dump(history[-20:], f)  # Храним последние 20

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                history = json.load(f)
                for pwd in reversed(history):
                    self.tree.insert("", "end", values=(pwd,))


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
