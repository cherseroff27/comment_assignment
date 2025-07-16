from selenium.webdriver.common.by import By
from web_elements_handler import WebElementsHandler as Weh

from logger_config import Logger

logger = Logger.get_logger(__name__)


class DzenArticleParser:
    def __init__(self, driver):
        self.driver = driver


    def open_page(self, link):
        self.driver.get(link)


    def fetch_article_text(self, article_link: str):
        try:
            if self.is_dzen_tab_open():
                self.open_page(article_link)
            else:
                self.open_page(article_link)

            self.scroll_article_down_to_comments()

            content_page_locator_1 = "//div[@class='ui-lib-brief-content-page__text']//span[@class='content--rich-text__text-1W content--rich-text__colorPrimary-2J']"
            content_page_locator_2 = "//div[@class='brief-viewer--brief-content-page__text-2d']"
            header_locator = ".//h3[@class='content--common-block__block-3U content--common-block__header3-3x']"
            paragraph_locator = ".//p[@class='content--common-block__block-3U']/span"
            list_locator = ".//ul[@class='content--article-render__block-3j content--article-render__unorderedList-2l']//li[@class='content--common-block__block-3U content--common-block__list-Nq']"
            quote_locator = ".//blockquote[@class='content--common-block__block-3U content--common-block__quote-s4']"
            link_locator = "//a[@class='content--article-link__articleLink-OU content--article-link__colorDefault-3s']"
            logger.info(self.driver.current_url)

            if "dzen.ru/b" in self.driver.current_url:
                elements_to_parse = [
                    content_page_locator_1,
                    content_page_locator_2
                ]

                while True:
                    article_body_element = Weh.wait_for_element_xpath(content_page_locator_1, content_page_locator_2, driver=self.driver, timeout=30)
                    if article_body_element:
                        content_elements = article_body_element.find_elements(By.XPATH, " | ".join(elements_to_parse))

                        article_text = "\n".join([element.text for element in content_elements])
                        if article_text.strip() == "":
                            continue
                        else:
                            logger.info(f"Текст статьи: {article_text}")
                            break

                return article_text

            elif "dzen.ru/a" in self.driver.current_url:
                article_title_locator = ".//h1[@data-testid='article-title']"
                article_title_element = Weh.wait_for_element_xpath(article_title_locator, driver=self.driver, timeout=30)

                article_title_text = article_title_element.text

                article_body_locator = "//div[@itemprop='articleBody']"
                article_body_element = Weh.wait_for_element_xpath(article_body_locator, driver=self.driver, timeout=30)

                elements_to_parse = [
                    header_locator,
                    header_locator,
                    paragraph_locator,
                    list_locator,
                    quote_locator,
                    link_locator
                ]
                while True:
                    if article_body_element:
                        content_elements = article_body_element.find_elements(By.XPATH, " | ".join(elements_to_parse))

                        article_text = "\n".join([element.text for element in content_elements])
                        if article_text.strip() == "":
                            continue
                        else:
                            article_text = f"Заголовок статьи:\n{article_title_text}\nТекст статьи:\n{article_text}"
                            logger.info(f"Заголовок статьи: {article_title_text}")
                            logger.info(f"Текст статьи: {article_text}")
                            break

                return article_text
        except Exception as e:
            logger.error("Ошибка при парсинге:", e)


    def scroll_article_down_to_comments(self):
        try:
            comments_bar_locator_1 = "//div[@data-testid='article-comments']"
            comments_bar_locator_2 = "//div[@id='comments']"
            comments_bar_element = Weh.wait_for_element_xpath(comments_bar_locator_1, comments_bar_locator_2, driver=self.driver, timeout=30)

            if comments_bar_element:
                self.driver.execute_script("arguments[0].scrollIntoView();", comments_bar_element)
        except Exception as e:
            logger.error("Ошибка при скроллинге к комментариям:", e)

    def is_dzen_tab_open(self):
        original_window = self.driver.current_window_handle

        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)

            if "dzen.ru/a/" in self.driver.current_url:
                return True

        self.driver.switch_to.window(original_window)
        return False