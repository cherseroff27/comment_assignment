import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tk_font
import threading

from ArticleData import ArticleData

from logger_config import Logger

logger = Logger.get_logger(__name__)


class CommentsManagerUI:
    def __init__(self, root, logic):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.logic = logic
        self.root.title("Comment Manager")
        self.root.geometry("900x900")

        # Настройки шрифтов
        self.header_font = tk_font.Font(family="Helvetica", size=12, weight="bold")
        self.custom_font = tk_font.Font(family="Calibri", size=10, weight="normal")

        # Инициализация интерфейсных переменных
        self.links_var = tk.StringVar(value=self.logic.load_initial_data("links") or "")
        self.gender_var = tk.StringVar(value=self.logic.load_initial_data("gender") or "male")
        self.browser_profiles_dir = tk.StringVar(value=self.logic.default_browser_profiles_dir)
        self.profile_name = tk.StringVar(value=self.logic.load_initial_data("profile_name"))
        self.bot_token = tk.StringVar(value=self.logic.load_initial_data("bot_token"))
        self.chat_id = tk.StringVar(value=self.logic.load_initial_data("chat_id"))
        self.use_user_agent = tk.BooleanVar(value=self.logic.load_initial_data("use_user_agent"))
        self.use_stealth = tk.BooleanVar(value=self.logic.load_initial_data("use_stealth"))
        self.use_profile_folder = tk.BooleanVar(value=self.logic.load_initial_data("use_profile_folder"))
        self.use_manual_control = tk.BooleanVar(value=self.logic.load_initial_data("use_manual_control"))
        self.comments_amount = tk.IntVar(value=self.logic.load_initial_data("comments_amount"))

        self.initial_data_dict = {
            "links": self.links_var,
            "gender": self.gender_var,
            "profile_name": self.profile_name,
            "bot_token": self.bot_token,
            "chat_id": self.chat_id,
            "use_user_agent": self.use_user_agent,
            "use_stealth": self.use_stealth,
            "use_profile_folder": self.use_profile_folder,
            "use_manual_control": self.use_manual_control,
            "comments_amount": self.comments_amount,
        }
        self.initial_data_frame = ttk.Frame(self.root)
        self.browser_properties_frame = ttk.Frame(self.root)

        # Создание виджетов
        self.create_widgets()

    def create_widgets(self):
        """Создание и размещение всех виджетов интерфейса"""
        # Контейнер для ввода ссылок
        top_frame = tk.LabelFrame(self.root, text="Ссылки на посты/статьи", font=self.header_font)
        top_frame.pack(fill="x", padx=10, pady=5)

        self.links_entry = tk.Text(top_frame, height=10, font=self.custom_font)
        self.links_entry.delete("1.0", tk.END)  # Очистить поле
        self.links_entry.insert("1.0", self.links_var.get())  # Вставить текст
        self.links_entry.pack(fill="x", padx=10, pady=5)

        # Контейнер для выбора пола
        gender_frame = tk.LabelFrame(self.root, text="Выбор пола комментариев", font=self.header_font)
        gender_frame.pack(fill="x", padx=10, pady=5)

        gender_buttons_frame = tk.Frame(gender_frame)
        gender_buttons_frame.pack(pady=5)

        tk.Radiobutton(gender_buttons_frame, text='Мужской', variable=self.gender_var,
                       value='male', font=self.custom_font).grid(row=0, column=0, padx=10)
        tk.Radiobutton(gender_buttons_frame, text='Женский', variable=self.gender_var,
                       value='female', font=self.custom_font).grid(row=0, column=1, padx=10)
        tk.Radiobutton(gender_buttons_frame, text='Смешанный', variable=self.gender_var,
                       value='mixed', font=self.custom_font).grid(row=0, column=2, padx=10)

        # Кнопки управления
        control_button_frame = tk.Frame(self.root)
        control_button_frame.pack(fill="x", padx= 10, pady=10)

        self.save_config_button = tk.Button(control_button_frame, text='Сохранить конфиг', font=self.custom_font, command=self.save_config)
        self.save_config_button.pack(side="left", padx=5)

        self.generate_button = tk.Button(control_button_frame, text='Запустить генерацию', font=self.custom_font, command=self.start_generation)
        self.generate_button.pack(side="left", padx=5)

        # Данные начальной конфигурации
        config_frame = tk.LabelFrame(self.root, text="Настройки подключения и профилей", font=self.header_font)
        config_frame.pack(fill="x", padx=10, pady=5)

        # Поля профиля
        def create_labeled_entry(parent, label_text, variable):
            frame = tk.Frame(parent)
            frame.pack(fill="x", padx=5, pady=2)
            tk.Label(frame, text=label_text, font=self.custom_font).pack(anchor="w")
            tk.Entry(frame, textvariable=variable, font=self.custom_font, width=50).pack(fill="x")

        create_labeled_entry(config_frame, "Название профиля браузера", self.profile_name)
        create_labeled_entry(config_frame, "Bot Token", self.bot_token)
        create_labeled_entry(config_frame, "Chat ID", self.chat_id)
        create_labeled_entry(config_frame, "Требуемое количество комментариев", self.comments_amount)

        # Опции браузера
        browser_options_frame = tk.LabelFrame(self.root, text="Настройки браузера", font=self.header_font)
        browser_options_frame.pack(fill="x", padx=10, pady=5)

        options_grid = tk.Frame(browser_options_frame)
        options_grid.pack(pady=5)

        tk.Checkbutton(options_grid, text='Использовать User-Agent', variable=self.use_user_agent,
                       font=self.custom_font).grid(row=0, column=0, padx=10, sticky="w")
        tk.Checkbutton(options_grid, text='Использовать Stealth', variable=self.use_stealth,
                       font=self.custom_font).grid(row=0, column=1, padx=10, sticky="w")
        tk.Checkbutton(options_grid, text='Использовать папку профиля браузера', variable=self.use_profile_folder,
                       font=self.custom_font).grid(row=0, column=2, padx=10, sticky="w")
        tk.Checkbutton(options_grid, text='Управлять браузером вручную', variable=self.use_manual_control,
                       font=self.custom_font).grid(row=0, column=3, padx=10, sticky="w")

        # Таблица для предварительного просмотра
        self.table_frame = tk.LabelFrame(self.root, text="Сгенерированные комментарии", font=self.header_font)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.table = ttk.Treeview(self.table_frame, columns=('link', 'gender', 'comment'), show='headings')
        self.table.heading('link', text='Ссылка')
        self.table.heading('gender', text='Пол')
        self.table.heading('comment', text='Комментарий')
        self.table.column('link', width=200)
        self.table.column('gender', width=100)
        self.table.column('comment', width=400)
        self.table.bind("<Double-1>", self.on_row_double_click)

        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.table.pack(fill=tk.BOTH, expand=True)

        # Кнопка сохранения в БД
        self.save_button = tk.Button(self.root, text='Сохранить в БД', font=self.custom_font, state=tk.DISABLED, command=self.save_to_db)
        self.save_button.pack(pady=10)


    def save_config(self):
        """Сохраняет текущие настройки в конфиг"""
        for key, value in self.initial_data_dict.items():
            if key == "links":
                value = self.get_links_list() # подменяем value вручную
            self.logic.save_value_to_config(key, value)

        tk.messagebox.showinfo("Успех", "Конфигурация успешно сохранена")


    def get_links_list(self):
        """Возвращает список ссылок из текстового поля"""
        return self.links_entry.get("1.0", tk.END).strip()


    def start_generation(self):
        """Запуск генерации комментариев"""
        links_text = self.get_links_list()
        links = [link.strip() for link in links_text.split('\n') if link.strip()]

        if not links:
            tk.messagebox.showwarning("Ошибка", "Пожалуйста, введите хотя бы одну ссылку")
            return

        self.generate_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)

        thread = threading.Thread(target=self._generation_worker, args=(links,))
        thread.start()


    def _generation_worker(self, links):
        """Рабочий метод генерации, выполняющийся в отдельном потоке"""
        try:
            articles_data = self.logic.start_generation(
                links=links,
                bot_token=self.bot_token.get(),
                chat_id=self.chat_id.get(),
                gender=self.gender_var.get(),
                comments_amount=self.comments_amount.get(),
                profile_name=self.profile_name.get(),
                browser_profiles_dir=self.browser_profiles_dir.get(),
                use_stealth=self.use_stealth.get(),
                use_user_agent=self.use_user_agent.get(),
                use_profile_folder=self.use_profile_folder.get(),
                use_manual_control=self.use_manual_control.get(),
            )

            all_comments = []
            for article_data in articles_data.values():
                for comment in article_data.comments:
                    all_comments.append(ArticleData(
                        link=article_data.link,
                        gender=article_data.gender,
                        comments=comment
                    ))

            # Безопасное обновление интерфейса из потока
            self.root.after(0, self.display_comments, all_comments)
            self.root.after(0, lambda: self.save_button.config(state=tk.NORMAL))

        except Exception as e:
            self.root.after(0, lambda: tk.messagebox.showerror("Ошибка", f"Произошла ошибка при генерации: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.generate_button.config(state=tk.NORMAL))


    def display_comments(self, articles_data):
        """Отображает сгенерированные комментарии в таблице"""
        for item in self.table.get_children():
            self.table.delete(item)

        for data in articles_data:
            self.table.insert('', 'end', values=(
                data.link or '',
                data.gender or '',
                data.comments or ''
            ))


    def save_to_db(self):
        """Сохранение сгенерированных данных в базу"""
        if self.logic.save_to_db():
            tk.messagebox.showinfo("Успех", "Комментарии успешно сохранены в БД")
            self.save_button.config(state=tk.DISABLED)
        else:
            tk.messagebox.showerror("Ошибка", "Не удалось сохранить комментарии в БД")


    def on_row_double_click(self, event):
        item = self.table.selection()[0]
        values = self.table.item(item, "values")
        comment = values[2]
        top = tk.Toplevel(self.root)
        top.title("Комментарий")
        text = tk.Text(top, wrap=tk.WORD)
        text.insert(tk.END, comment)
        text.pack(expand=True, fill=tk.BOTH)


    def on_close(self):
        logger.info("Сохраняем конфиг перед выходом...")
        self.save_config()
        self.root.destroy()


    @staticmethod
    def open_in_explorer(path_var):
        """Открывает папку в проводнике, игнорируя наличие файла."""
        path = path_var.get()
        folder_to_open = path if os.path.isdir(path) else os.path.dirname(path)  # Извлекаем папку
        if os.path.exists(folder_to_open):
            os.startfile(folder_to_open)
        else:
            messagebox.showerror("Ошибка", "Указанная папка не найдена!")
