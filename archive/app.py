from flask import Flask, request, render_template, redirect, session
import uuid
from DataBaseTaskManager import DataBaseTaskManager
from telegram_notificator import TelegramNotificator
from DataBaseConfigManager import DataBaseConfigManager


# Flask конфигурация
app = Flask(__name__)
app.secret_key = 'f3e1b2d7e09f34bb6b847ad05a2cfd3842dc72db874932405ebac1a07fbdcf26'

config_dir = "~/PycharmProjects/configs/dzen_comments_db_path_config"
config_name = "config.json"

db_config_manager = DataBaseConfigManager(config_dir=config_dir, config_name=config_name)
db_path = db_config_manager.read_config()
print(f"db_path: {db_path}")

# Конфигурация Telegram
bot_token = "7225892740:AAHSGZSdb-7-ZaK6C3psxG3qBBPpQzavaew"
chat_id = '1642569912'
db_task_manager = DataBaseTaskManager(db_path)
db_task_manager.init_user_comments_table()  # Инициализация таблицы user_comments
telegram_notificator = TelegramNotificator(bot_token, chat_id)

REQUIRED_COMMENTS = 5


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        gender = request.form.get('gender')
        return redirect(f'/task/{gender}')
    return render_template('index.html')


@app.route('/task/<gender>')
def task(gender):
    # Уникальный идентификатор пользователя
    user_id = session.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        session['user_id'] = user_id

    # Проверяем, есть ли уже выданные комментарии
    existing_comments = db_task_manager.get_user_comments(user_id)
    if existing_comments:
        return render_template('task.html', tasks=[{"link": c[1], "comment": c[2]} for c in existing_comments])

    # Получаем доступные комментарии с учётом уникальности
    available_comments = db_task_manager.get_available_comments(gender, user_id)
    if not available_comments:
        telegram_notificator.send_telegram_message(f"Нет доступных комментариев для {gender}")
        return "К сожалению, для выбранной категории сейчас нет заданий. Попробуйте позже."

    # Выбираем нужное количество комментариев
    selected_comments = available_comments[:REQUIRED_COMMENTS]
    if len(selected_comments) < REQUIRED_COMMENTS:
        telegram_notificator.send_telegram_message(
            f"Доступно только {len(selected_comments)} комментариев для {gender}. Пополните базу!"
        )
        return (f"Доступно только {len(selected_comments)} комментариев. "
                f"Попробуйте позже, когда база данных пополнится.")

    # Сохраняем комментарии для пользователя
    db_task_manager.save_user_comments(user_id, selected_comments)

    return render_template('task.html', tasks=[{"link": c[1], "comment": c[2]} for c in selected_comments])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)