import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "movies.json")

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("800x500")

        self.movies = []
        self.all_movies = []  # Для хранения полной копии данных при фильтрации

        # --- Виджеты ввода ---
        tk.Label(root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_title = tk.Entry(root, width=30)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Жанр:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_genre = tk.Entry(root, width=30)
        self.entry_genre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Год:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_year = tk.Entry(root, width=10)
        self.entry_year.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        tk.Label(root, text="Рейтинг:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_rating = tk.Entry(root, width=10)
        self.entry_rating.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # --- Кнопки управления ---
        tk.Button(root, text="Добавить фильм", command=self.add_movie).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Сохранить", command=self.save_movies).grid(row=4, column=2, padx=5)
        tk.Button(root, text="Загрузить", command=self.load_movies).grid(row=4, column=3, padx=5)

        # --- Фильтрация ---
        tk.Label(root, text="Фильтр по жанру:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.combo_genre = ttk.Combobox(root, values=["Все"], state="readonly", width=27)
        self.combo_genre.current(0)
        self.combo_genre.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(root, text="Фильтр по году:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.combo_year = ttk.Combobox(root, values=["Все"], state="readonly", width=27)
        self.combo_year.current(0)
        self.combo_year.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(root, text="Применить фильтр", command=self.filter_movies).grid(row=7, column=0, columnspan=4, pady=10)

        # --- Таблица ---
        self.columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.table = ttk.Treeview(root, columns=self.columns, show="headings")
        for col in self.columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=180)
        self.table.grid(row=8, column=0, columnspan=4, padx=5, pady=5)

    def add_movie(self):
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year = self.entry_year.get().strip()
        rating = self.entry_rating.get().strip()

        if not title or not genre or not year or not rating:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
            return

        if not year.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return

        year_int = int(year)

        try:
            rating_float = float(rating)
            if not (0 <= rating_float <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10!")
            return

        movie = {"title": title, "genre": genre, "year": year_int, "rating": rating_float}
        
        self.movies.append(movie)
        
        # Обновляем фильтры после добавления нового фильма
        self.update_filters()
        
        self.update_table()
        self.clear_entries()

    def filter_movies(self):
        genre = self.combo_genre.get()
        year_text = self.combo_year.get()
        
        filtered_data = self.all_movies.copy()
        
        if genre != "Все":
            filtered_data = [m for m in filtered_data if m["genre"] == genre]
            
        if year_text != "Все":
            try:
                year_int = int(year_text)
                filtered_data = [m for m in filtered_data if m["year"] == year_int]
            except ValueError:
                pass

        self.movies = filtered_data
        self.update_table()

    def update_table(self):
        for i in self.table.get_children():
            self.table.delete(i)
            
        for m in self.movies:
            self.table.insert("", "end", values=(m["title"], m["genre"], m["year"], m["rating"]))

    def clear_entries(self):
         self.entry_title.delete(0, tk.END)
         self.entry_genre.delete(0, tk.END)
         self.entry_year.delete(0, tk.END)
         self.entry_rating.delete(0, tk.END)
         
    def update_filters(self):
         # Обновляем список жанров и годов на основе всех фильмов (all_movies)
         genres = sorted({m["genre"] for m in self.all_movies})
         years = sorted({str(m["year"]) for m in self.all_movies})
         
         current_genre = self.combo_genre.get()
         current_year = self.combo_year.get()
         
         self.combo_genre['values'] = ["Все"] + genres
         self.combo_year['values'] = ["Все"] + years
         
         # Сохраняем текущий выбор фильтра (если он всё ещё валиден)
         if current_genre not in ["Все"] + genres:
             self.combo_genre.current(0)
         else:
             self.combo_genre.set(current_genre)
             
         if current_year not in ["Все"] + years:
             self.combo_year.current(0)
         else:
             self.combo_year.set(current_year)

    def save_movies(self):
         save_path = filedialog.asksaveasfilename(
             defaultextension=".json",
             filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
             initialfile="movies.json"
         )
         
         if save_path:
             try:
                 with open(save_path, "w", encoding="utf-8") as f:
                     json.dump(self.movies + (self.all_movies if hasattr(self,'all_movies') else []), f,
                               ensure_ascii=False, indent=4)
                 messagebox.showinfo("Успех", f"Данные сохранены в {save_path}")
             except Exception as e:
                 messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

    def load_movies(self):
         load_path = filedialog.askopenfilename(
             filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
         )
         
         if load_path:
             try:
                 with open(load_path, "r", encoding="utf-8") as f:
                     data = json.load(f)
                     
                 # Проверяем структуру данных
                 if isinstance(data, list) and all(isinstance(x,dict) for x in data):
                     self.movies = data.copy()
                     self.all_movies = data.copy()
                     self.update_filters()
                     self.update_table()
                     messagebox.showinfo("Успех", f"Данные загружены из {load_path}")
                 else:
                     raise ValueError("Некорректный формат данных в файле.")
             except Exception as e:
                 messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")
                 
    def load_default_data(self):
         """Загрузка данных по умолчанию при запуске"""
         if not os.path.exists(DATA_DIR):
             os.makedirs(DATA_DIR)
             
         if os.path.exists(DATA_FILE):
             try:
                 with open(DATA_FILE, "r", encoding="utf-8") as f:
                     data = json.load(f)
                     
                 if isinstance(data, list) and all(isinstance(x,dict) for x in data):
                     self.movies = data.copy()
                     self.all_movies = data.copy()
                     return True
             except Exception as e:
                 print(f"Ошибка при загрузке данных по умолчанию: {e}")
                 
         return False

if __name__ == '__main__':
    root = tk.Tk()
    app = MovieLibraryApp(root)
    
    # Загрузка данных по умолчанию при запуске
    if not app.load_default_data():
       messagebox.showinfo("Приветствие", "Добро пожаловать! Ваша библиотека фильмов пуста.")
    
    root.mainloop()