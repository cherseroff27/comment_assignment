import sys
from fake_useragent import UserAgent

from comments_generator import CommentsGenerator
from browser_manager import BrowserManager
from manual_script_control import ManualScriptControl
from telegram_notificator import TelegramNotificator

from DzenArticleParser import DzenArticleParser
from ArticleData import ArticleData

from logger_config import Logger

logger = Logger.get_logger(__name__)


class CommentsGeneratorManager:
    def __init__(self):
        self.chatgpt_link = "https://chatgpt.com/"


    def generate_comments(
            self,
            bot_token,
            chat_id,
            gender,
            links,
            comments_amount,
            profile_name,
            browser_profiles_dir,
            use_stealth,
            use_user_agent,
            use_profile_folder,
            use_manual_control,
    ):
        user_agent = self.get_user_agent(use_user_agent) if use_user_agent else None

        tg_notificator = TelegramNotificator(bot_token, chat_id)

        chrome_browser_manager = BrowserManager(user_agent=user_agent)
        driver = chrome_browser_manager.initialize_webdriver(
            browser_profiles_dir=browser_profiles_dir,
            profile_name=profile_name,
            use_profile_folder=use_profile_folder,
            use_stealth = use_stealth
        )
        try:
            if driver is None:
                logger.error("driver == None")
                sys.exit()

            if use_manual_control:
                ManualScriptControl.wait_for_user_input()

            articles_content_parser = DzenArticleParser(driver)
            comments_generator = CommentsGenerator(driver, tg_notificator)

            articles_data = {}
            for link in links:
                article_content = articles_content_parser.fetch_article_text(article_link=link)
                comments = comments_generator.get_comments(
                    chatgpt_link=self.chatgpt_link,
                    article_content=article_content,
                    gender=gender,
                    comments_amount=comments_amount
                )

                article_data = ArticleData(link=link, gender=gender, comments=comments)
                logger.info(article_data.to_dict())

                articles_data[link] = article_data

            return articles_data

        finally:
            logger.info("Закрываем браузер...")
            driver.quit()


    @staticmethod
    def get_user_agent(use_user_agent):
        if use_user_agent:
            try:
                ua = UserAgent()
                return ua.random
            except Exception as e:
                logger.error(f"Не удалось получить user-agent через fake_useragent: {e}")
        return None


