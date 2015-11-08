# -*- coding: utf-8 -*-
"""
Feature: Фавикон, заголовок, описание для Главной страницы сайта
"""
import urllib
from support.utils.common_utils import priority
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateData
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods
from support import service_log
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleMethods



class TestFaviconMainPage(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Фавикон, заголовок, описание для Главной страницы сайта
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

    def test_google(self):
        self.driver.get('http://google.ru')
        pass