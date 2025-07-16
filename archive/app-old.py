import sqlite3
import requests
from flask import Flask, request, render_template, redirect
from TelegramNotificator import TelegramNotificator

# Настройки
REQUIRED_COMMENTS = 5
DB_PATH = r"C:\Users\cherseroff\PycharmProjects\comment_assignment\data\database.db"
TELEGRAM_BOT_TOKEN = '7225892740:AAHSGZSdb-7-ZaK6C3psxG3qBBPpQzavaew'
TELEGRAM_CHAT_ID = '1642569912'

app = Flask(__name__)

class TaskManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_available_comments(self, gender):
        """Получить доступные комментарии, отсортированные случайным образом"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, link, comment FROM articles WHERE gender = ? AND assigned = 0 ORDER BY RANDOM()",
            (gender,)
        )
        comments = cursor.fetchall()
        conn.close()
        return comments

    def mark_comments_as_assigned(self, comment_ids):
        """Пометить комментарии как использованные"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.executemany(
            "UPDATE articles SET assigned = 1 WHERE id = ?",
            [(id_,) for id_ in comment_ids]
        )
        conn.commit()
        conn.close()


notificator = TelegramNotificator(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
task_manager = TaskManager(DB_PATH)


url = 'https://8ea6-46-61-245-85.ngrok-free.app'  # Замените на ваш URL от ngrok
headers = {
    'ngrok-skip-browser-warning': 'true',
}

response = requests.get(url, headers=headers)

print(response.text)  # Или используйте как вам нужно


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        gender = request.form.get('gender')
        return redirect(f'/task/{gender}')
    return render_template('index.html')


@app.route('/task/<gender>')
def task(gender):
    all_comments = task_manager.get_available_comments(gender)
    if not all_comments:
        notificator.send_telegram_message(f"Комментарии для пола '{gender}' закончились!")
        return "Нет доступных заданий, попробуйте позже."

    # Группируем комментарии по ссылкам
    comments_by_link = {}
    for comment in all_comments:
        link = comment[1]
        if link not in comments_by_link:
            comments_by_link[link] = []
        comments_by_link[link].append(comment)

    # Составляем список заданий
    selected_comments = []
    used_links = set()

    for link, comments in comments_by_link.items():
        if len(selected_comments) >= REQUIRED_COMMENTS:
            break
        if link not in used_links:
            selected_comments.append(comments[0])  # Берем первый комментарий для уникальной ссылки
            used_links.add(link)

    # Дополняем список комментариями, если их недостаточно
    if len(selected_comments) < REQUIRED_COMMENTS:
        remaining_comments_needed = REQUIRED_COMMENTS - len(selected_comments)
        for link, comments in comments_by_link.items():
            if len(selected_comments) >= REQUIRED_COMMENTS:
                break
            for comment in comments:
                if len(selected_comments) < REQUIRED_COMMENTS and comment not in selected_comments:
                    selected_comments.append(comment)

    # Проверяем достаточность комментариев
    if len(selected_comments) < REQUIRED_COMMENTS:
        notificator.send_telegram_message(
            f"Недостаточно комментариев для пола '{gender}'. Доступно только {len(selected_comments)}."
        )
        return f"Недостаточно комментариев. Доступно только {len(selected_comments)}."

    # Помечаем выбранные комментарии как использованные
    selected_ids = [comment[0] for comment in selected_comments]
    task_manager.mark_comments_as_assigned(selected_ids)

    # Формируем данные для отображения
    response_data = [{"link": comment[1], "comment": comment[2]} for comment in selected_comments]
    return render_template('task.html', tasks=response_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
