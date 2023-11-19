import json
from pathlib import Path

from loguru import logger
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_auto_update.webdriver_auto_update import WebdriverAutoUpdate
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import PATH_TO_URLS
from data_classes import Video
from db import Database
from enums import Options, VideoContainer


class Chrome(webdriver.Chrome):
    def __init__(
        self,
        options: ChromeOptions = None,
        service: Service = None,
        keep_alive: bool = True
    ) -> None:
        """Создаёт объект браузера, автоматически подтягивая
           необходимую версию"""

        driver_manager = WebdriverAutoUpdate(Path('.'))
        driver_manager.main()
        super().__init__(options, service, keep_alive)


class YotubeParser:
    def __init__(self):
        """Создаёт объект парсера с конфигом"""

        options = self._set_options()
        self.driver = Chrome(options)

    def _set_options(self) -> ChromeOptions:
        """Создаёт объект конфигурации браузера

        Возвращает:
            ChromeOptions: Объект конфига"""

        options = ChromeOptions()
        options.add_argument(Options.HEADLESS)
        options.add_argument(Options.NO_ERRORS)
        options.add_argument(Options.NO_IMAGES)
        options.add_argument(Options.NO_EXTENSTIONS)
        options.add_argument(Options.NO_DEV_SHM)
        options.add_argument(Options.NO_SANDBOX)
        options.add_argument(Options.NO_NOTIFICATIONS)
        options.add_argument(Options.NO_ADS)
        options.add_argument(Options.NO_POPUPS)
        options.add_argument(Options.MAXIMIZE)
        return options

    def _parse_url(self) -> list[WebElement]:
        """Парсит урл, находит контейнеры, содержащие
        информацию о видео

        Возвращает:
            list[WebElement]: Список контейнеров"""

        self.driver.get(self.channel_url)
        video_containers = WebDriverWait(
            self.driver, 5).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, VideoContainer.TAG)
                )
            )
        return video_containers

    def _get_video_data(self, video_container: WebElement) -> Video:
        """Парсит информацию о видео из контейнера и возвращает
        объект Video

        Принимает:
            video_container (WebElement): Контейнер с видео

        Возвращает:
            Video: Видео"""

        url = video_container.find_element(
            By.ID,
            VideoContainer.ID
        ).get_attribute(
            VideoContainer.URL
        )
        try:
            video = Video(
                channel_username=self.channel_url.split('@')[1],
                video_id=url.split('=')[1],
                video_href=url
            )
        except IndexError:
            logger.error(f'Неверный url: {url}')
        return video

    def start_parsing(self, channel_url: str) -> list[Video]:
        """Запускает процесс парсинга

        Принимает:
            channel_url: Ссылка на Youtube-канал

        Возвращает:
            list[Video]: Список Видео"""

        self.channel_url = channel_url
        logger.info(f'Запуск парсинга: {channel_url}')
        video_containers = self._parse_url()
        videos = [
            self._get_video_data(vc)
            for vc in video_containers
        ]
        logger.info(f'Найденных видео: {len(videos)}')
        return videos


def script():
    try:
        with open(PATH_TO_URLS, 'r') as file:
            urls = json.loads(file.read())['urls']
    except FileNotFoundError:
        logger.error(f'JSON с ссылками не найден по адресу: {PATH_TO_URLS}')
    except IndexError:
        logger.error('Неверный формат JSON')
    parser = YotubeParser()
    for url in urls:
        videos = parser.start_parsing(url)
        if videos:
            logger.info('Запись данных в БД')
            try:
                with Database() as db:
                    db.write(videos)
            except Exception as ex:
                logger.error(f'Ошибка записи в БД: {ex}')


if __name__ == '__main__':
    script()
