import sqlite3


class DataBaseTaskManager:
    def __init__(self, db_path):
        self.db_path = db_path


    def init_user_comments_table(self):
        """Создаёт таблицу user_comments, если она ещё не существует."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                comment_id INTEGER NOT NULL,
                link TEXT NOT NULL,
                comment TEXT NOT NULL,
                FOREIGN KEY (comment_id) REFERENCES articles (id)
            )
        ''')
        conn.commit()
        conn.close()


    def get_available_comments(self, gender, user_id):
        """Получить доступные комментарии с учётом уникальности ссылок и пола."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Извлекаем комментарии, которые ещё не выдавались этому пользователю
        cursor.execute("""
            SELECT id, link, comment
            FROM articles
            WHERE gender = ? AND assigned = 0 
            AND link NOT IN (s
                SELECT link
                FROM user_comments
                WHERE user_id = ?
            )
            GROUP BY link
            ORDER BY RANDOM()
        """, (gender, user_id))
        comments = cursor.fetchall()
        conn.close()
        return comments


    def save_user_comments(self, user_id, comments):
        """Сохраняет комментарии, выданные пользователю."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Сохраняем комментарии в user_comments
        cursor.executemany("""
            INSERT INTO user_comments (user_id, comment_id, link, comment)
            VALUES (?, ?, ?, ?)
        """, [(user_id, c[0], c[1], c[2]) for c in comments])

        # Обновляем статус комментариев как "выданные"
        cursor.executemany("""
            UPDATE articles SET assigned = 1 WHERE id = ?
        """, [(c[0],) for c in comments])

        conn.commit()
        conn.close()


    def mark_comments_as_assigned(self, comment_ids):
        """Пометить комментарии как выданные."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.executemany(
            "UPDATE articles SET assigned = 1 WHERE id = ?",
            [(id_,) for id_ in comment_ids]
        )
        conn.commit()
        conn.close()


    def get_user_comments(self, user_id):
        """Возвращает комментарии, которые уже были выданы пользователю."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT comment_id, link, comment
            FROM user_comments
            WHERE user_id = ?
        """, (user_id,))
        comments = cursor.fetchall()
        conn.close()
        return comments
