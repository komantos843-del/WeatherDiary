import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("700x500")
        
        self.file_name = "movies.json"
        self.movies = self.load_data()

        # Поля ввода
        frame_input = tk.Frame(root, padx=10, pady=10)
        frame_input.pack(fill="x")

        tk.Label(frame_input, text="Название:").grid(row=0, column=0)
        self.ent_title = tk.Entry(frame_input)
        self.ent_title.grid(row=0, column=1)

        tk.Label(frame_input, text="Жанр:").grid(row=0, column=2)
        self.ent_genre = tk.Entry(frame_input)
        self.ent_genre.grid(row=0, column=3)

        tk.Label(frame_input, text="Год:").grid(row=1, column=0)
        self.ent_year = tk.Entry(frame_input)
        self.ent_year.grid(row=1, column=1)

        tk.Label(frame_input, text="Рейтинг (0-10):").grid(row=1, column=2)
        self.ent_rating = tk.Entry(frame_input)
        self.ent_rating.grid(row=1, column=3)

        btn_add = tk.Button(frame_input, text="Добавить фильм", command=self.add_movie)
        btn_add.grid(row=2, column=0, columnspan=4, pady=10)

        # Фильтрация
        frame_filter = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=5)
        frame_filter.pack(fill="x", padx=10)

        tk.Label(frame_filter, text="Жанр:").grid(row=0, column=0)
        self.filter_genre = tk.Entry(frame_filter)
        self.filter_genre.grid(row=0, column=1)

        tk.Label(frame_filter, text="Год:").grid(row=0, column=2)
        self.filter_year = tk.Entry(frame_filter)
        self.filter_year.grid(row=0, column=3)

        btn_filter = tk.Button(frame_filter, text="Применить", command=self.update_table)
        btn_filter.grid(row=0, column=4, padx=5)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Title", "Genre", "Year", "Rating"), show='headings')
        self.tree.heading("Title", text="Название")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Year", text="Год")
        self.tree.heading("Rating", text="Рейтинг")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_table()

    def add_movie(self):
        title = self.ent_title.get()
        genre = self.ent_genre.get()
        year = self.ent_year.get()
        rating = self.ent_rating.get()

        if not (title and genre and year and rating):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            year = int(year)
            rating = float(rating)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Год — число, Рейтинг — от 0 до 10!")
            return

        self.movies.append({"title": title, "genre": genre, "year": year, "rating": rating})
        self.save_data()
        self.update_table()
        
        # Очистка полей
        for entry in [self.ent_title, self.ent_genre, self.ent_year, self.ent_rating]:
            entry.delete(0, tk.END)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        f_genre = self.filter_genre.get().lower()
        f_year = self.filter_year.get()

        for m in self.movies:
            if f_genre and f_genre not in m['genre'].lower(): continue
            if f_year and f_year != str(m['year']): continue
            self.tree.insert("", "end", values=(m['title'], m['genre'], m['year'], m['rating']))

    def save_data(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()
