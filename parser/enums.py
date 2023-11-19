from enum import StrEnum


class VideoContainer(StrEnum):
    TAG = 'ytd-grid-video-renderer'
    ID = 'thumbnail'
    URL = 'href'


class Options(StrEnum):
    HEADLESS = '--headless'
    NO_ERRORS = '--ignore-certificate-errors'
    NO_IMAGES = '--blink-settings=imagesEnabled=false'
    NO_EXTENSTIONS = '--disable-extensions'
    NO_DEV_SHM = '--disable-dev-shm-usage'
    NO_SANDBOX = '--no-sandbox'
    NO_NOTIFICATIONS = '--disable-notifications'
    NO_ADS = '--disable-Advertisement'
    NO_POPUPS = '--disable-popup-blocking'
    MAXIMIZE = 'start-maximized'
