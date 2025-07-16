import json
from pathlib import Path

from logger_config import Logger

logger = Logger.get_logger(__name__)

class DataBaseConfigManager:
    def __init__(self, config_dir="~/PycharmProjects/configs/dzen_comments_db_path_config", config_name="config.json"):
        self.config_dir = Path(config_dir).expanduser().resolve()   # Преобразуем путь к директории в абсолютный и создаём директорию, если её нет
        logger.info(f"config_dir: {self.config_dir}")
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.config_path = self.config_dir / config_name    # Формируем полный путь к файлу конфигурации
        logger.info(f"config_path: {self.config_path}")


    def create_config(self, db_path="data/database.db"):
        """Создаёт конфигурационный файл, если его нет."""
        config_data = {"db_path": db_path}

        if self.config_path.exists():
            logger.info(f"Конфигурационный файл перезаписан: {self.config_path}")
        else:
            logger.info(f"Конфигурационный файл создан: {self.config_path}")

        with open(self.config_path, "w", encoding="utf-8") as config_file:
            json.dump(config_data, config_file, indent=4)


    def read_config(self):
        """Читает данные из конфигурационного файла."""
        with open(self.config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
            return config.get("db_path", "data/dzen_comments_database.db")