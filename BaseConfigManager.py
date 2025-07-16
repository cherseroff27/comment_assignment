import json
from pathlib import Path
from logger_config import Logger

logger = Logger.get_logger(__name__)


class BaseConfigManager:
    def __init__(self, config_dir: str, config_name: str, default_config: dict = None):
        self.config_dir = Path(config_dir).expanduser().resolve()
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.config_path = self.config_dir / config_name
        logger.info(f"[Config] Путь к конфигу: {self.config_path}")

        if not self.config_path.exists():
            logger.info(f"[Config] Конфиг не найден. Создание с данными по умолчанию: {default_config}")
            self._write_config(default_config or {})

        self.config = self._read_config()

    def _read_config(self) -> dict:
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_config(self, config: dict):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        logger.info(f"[Config] Конфигурация сохранена: {config}")

    def get_value(self, key: str, default=None):
        return self.config.get(key, default)

    def set_value(self, key: str, value):
        self.config[key] = value
        self._write_config(self.config)

    def get_all(self):
        return self.config

    def reload(self):
        self.config = self._read_config()
