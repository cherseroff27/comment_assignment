from InitialDataConfigManager import InitialDataConfigManager
from CommentsGeneratorManager import CommentsGeneratorManager

from logger_config import Logger

logger = Logger.get_logger(__name__)


class CommentsManagerUILogic:
    def __init__(
            self,
            initial_data_config_manager: InitialDataConfigManager,
            default_browser_profiles_dir: str,
            comments_generator_manager: CommentsGeneratorManager
    ):
        self.initial_data_config_manager = initial_data_config_manager
        self.generated_comments = []
        self.default_browser_profiles_dir = default_browser_profiles_dir
        self.comments_generator_manager = comments_generator_manager


    def load_initial_data(self, data_var: str):
        """Загружает начальные данные из конфига"""
        config = self.config_manager.config
        if data_var in config:
            logger.info(f"Считываем данные из конфига по ключу {data_var}: {config[data_var]}")
            return config[data_var]


    def save_value_to_config(self, data_key, data_value):
        if hasattr(data_value, "get"):
            value_to_save = data_value.get()
        else:
            value_to_save = data_value

        self.config_manager.save_value_to_config(data_key, value_to_save)


    def start_generation(self, links, bot_token, chat_id, gender, comments_amount, profile_name,
            browser_profiles_dir, use_stealth, use_user_agent, use_profile_folder, use_manual_control,
    ):
        """Запускает процесс генерации комментариев"""
        logger.info(f"Начало генерации комментариев для {len(links)} ссылок, пол: {gender}")

        return self.comments_generator_manager.generate_comments(
            links=links, bot_token=bot_token, chat_id=chat_id, gender=gender, comments_amount=comments_amount,
            profile_name=profile_name, browser_profiles_dir=browser_profiles_dir, use_stealth=use_stealth,
            use_user_agent=use_user_agent, use_profile_folder=use_profile_folder, use_manual_control=use_manual_control,
        )


    def save_to_db(self):
        """Сохраняет сгенерированные комментарии в базу данных"""
        if not self.generated_comments:
            logger.error("Попытка сохранения пустого списка комментариев")
            return False

        try:
            # Здесь должна быть реальная логика сохранения в БД
            logger.info(f"Сохранение {len(self.generated_comments)} комментариев в БД")
            return True
        except Exception as e:
            logger.error(f"Ошибка при сохранении в БД: {str(e)}")
            return False