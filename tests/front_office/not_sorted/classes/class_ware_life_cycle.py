# -*- coding: utf-8 -*-
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from support import service_log
from support.utils.chromedriver import CHROMEDRIVER_PATH
from tests.MainClass import MainClass
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateData

__author__ = 'm.senchuk'


class HelpLifeCycleData(MainClass):
    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0; OORRAA-TEST/Bot"


class HelpLifeCycleMethods(HelpLifeCycleData):
    # TODO: дубляж
    # @staticmethod
    # def go_to_main_page(driver, env_base_url=MainClass.ENV_BASE_URL):
    #    driver.get(env_base_url)

    @staticmethod
    def get_driver():
        """ Подготовка работы с selenium.
        Драйвер хрома. Устанавливаем задержку. Раскрываем окно браузера.
        :return: драйвер
        """
        browser = MainClass.ENV_BROWSER
        service_log.put("Get browser: %s" % browser)
        if browser.lower() == 'firefox':
            driver = HelpLifeCycleCheckMethods.get_firefox_driver()
        else:
            service_log.put("Setup options for Chrome: --no-sandbox")
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            service_log.put("Get Chrome driver by path=%s." % CHROMEDRIVER_PATH)
            driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)
            service_log.put("Settings implicitly_wait=%s." % HelpNavigateData.timeout)
            driver.implicitly_wait(time_to_wait=HelpNavigateData.timeout)
            service_log.put("Maximize window.")
            driver.set_window_size(1920, 1080)
            driver.maximize_window()
        return driver

    @staticmethod
    def get_fast_driver():
        """ Подготовка работы с selenium.
        Драйвер хрома. Драйвер без задержки, для тестирования времени открытия страниц. Раскрываем окно браузера.
        :return: драйвер
        """
        service_log.put("Setup options for Chrome: --no-sandbox")
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        service_log.put("Get Chrome driver by path=%s." % CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)
        service_log.put("Maximize window.")
        driver.set_window_size(1920, 1080)
        driver.maximize_window()
        return driver

    @staticmethod
    def get_driver_with_user_agent(user_agent, cache_disk, cache_memory, cache_offline, http_cache, load_strategy):
        """
        Получить драйвер с юзер агентом.
        WARNING: работает только для Firefox
        :param flag: добавлять подпись user-agent
        :return: ссылка на драйвер
        """
        profile = webdriver.FirefoxProfile()
        profile.set_preference("intl.accept_languages", "ru")
        if user_agent is True or cache_disk is False or cache_memory is False or cache_offline is False or \
                        http_cache is False or load_strategy.lower() == 'unstable':
            profile = webdriver.FirefoxProfile()
            # отключаем кеширование браузера
            profile.set_preference("browser.cache.disk.enable", cache_disk)
            profile.set_preference("browser.cache.memory.enable", cache_memory)
            profile.set_preference("browser.cache.offline.enable", cache_offline)
            profile.set_preference("network.http.use-cache", http_cache)
            service_log.put("Setup options for Firefox: add in user-agent signature OORRAA-TEST")
            # прописываем юзер агент
            profile.set_preference("general.useragent.override", HelpLifeCycleData.USER_AGENT)
            if load_strategy.lower() == "unstable":
                # включаем режим "не ждать построение DOM"
                profile.set_preference("webdriver.load.strategy", "unstable")
            driver = webdriver.Firefox(firefox_profile=profile)
        else:
            driver = webdriver.Firefox(firefox_profile=profile)
        return driver

    @staticmethod
    def get_firefox_driver(manual_user_agent=False, cache_disk=True, cache_memory=True, cache_offline=True,
                           http_cache=True, load_strategy='stable'):
        """
        Подготовка работы с selenium.
        Драйвер фокса. С специальным user agent
        :return: драйвер
        """
        service_log.put("Get Firefox driver.")
        driver = HelpLifeCycleMethods.get_driver_with_user_agent(manual_user_agent, cache_disk, cache_memory,
                                                                 cache_offline, http_cache, load_strategy)
        service_log.put("Maximize window.")
        driver.set_window_size(1920, 1080)
        driver.maximize_window()
        return driver


class HelpLifeCycleCheckMethods(HelpLifeCycleMethods):
    pass
