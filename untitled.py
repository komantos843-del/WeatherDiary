import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []
        self.load_data()

        # --- Поля ввода ---
        tk.Label(root, text="Название").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Жанр").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.genre_entry = tk.Entry(root, width=30)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Год выпуска").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.year_entry = tk.Entry(root, width=30)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Рейтинг (0-10)").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.rating_entry = tk.Entry(root, width=30)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)

        # --- Кнопка добавления ---
        tk.Button(root, text="Добавить фильм", command=self.add_movie).grid(row=4, column=0, columnspan=2, pady=10)

        # --- Таблица ---
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(root, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, minwidth=0, width=120)
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # --- Фильтры ---
        tk.Label(root, text="Фильтр по жанру").grid(row=6, column=0, padx=5, pady=5, sticky='e')
        self.filter_genre = tk.Entry(root, width=30)
        self.filter_genre.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(root, text="Фильтр по году").grid(row=7, column=0, padx=5, pady=5, sticky='e')
        self.filter_year = tk.Entry(root, width=30)
        self.filter_year.grid(row=7, column=1, padx=5, pady=5)

        tk.Button(root, text="Применить фильтр", command=self.apply_filter).grid(row=8, column=0, columnspan=2, pady=10)

        # Заполнение таблицы при запуске
        self.update_table()

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()

        # Проверка на пустые поля
        if not all([title, genre, year, rating]):
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
            return

        # Проверка года
        if not year.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return
        
        year = int(year)

        # Проверка рейтинга
        try:
            rating = float(rating)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10!")
            return

        # Добавление фильма
        self.movies.append({
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        })

        self.clear_entries()
        self.update_table()
        self.save_data()

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def update_table(self):
        # Очистка таблицы
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Заполнение таблицы всеми фильмами (или отфильтрованными при необходимости)
        for movie in self.movies:
            self.tree.insert("", tk.END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def apply_filter(self):
         genre_filter = self.filter_genre.get().strip().lower()
         year_filter = self.filter_year.get().strip()

         filtered_movies = self.movies.copy()

         # Фильтрация по жанру
         if genre_filter:
             filtered_movies = [m for m in filtered_movies if genre_filter in m["genre"].lower()]

         # Фильтрация по году
         if year_filter:
             if year_filter.isdigit():
                 filtered_movies = [m for m in filtered_movies if m["year"] == int(year_filter)]
             else:
                 messagebox.showerror("Ошибка", "Фильтр по году должен быть числом!")
                 return

         # Обновление таблицы с отфильтрованными данными
         for i in self.tree.get_children():
             self.tree.delete(i)
         for movie in filtered_movies:
             self.tree.insert("", tk.END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def save_data(self):
         with open("movies.json", "w", encoding="utf-8") as f:
             json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
         if os.path.exists("movies.json"):
             with open("movies.json", "r", encoding="utf-8") as f:
                 try:
                     self.movies = json.load(f)
                 except json.JSONDecodeError:
                     self.movies = []