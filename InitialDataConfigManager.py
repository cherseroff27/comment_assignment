from BaseConfigManager import BaseConfigManager

from logger_config import Logger
logger = Logger.get_logger(__name__)


class InitialDataConfigManager(BaseConfigManager):
    def __init__(self):
        super().__init__(
            config_dir="./configs",
            config_name="initial_data_config.json",
            default_config={
                "gender": "mixed",
                "links": []
            }
        )