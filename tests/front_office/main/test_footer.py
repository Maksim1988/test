# -*- coding: utf-8 -*-
"""
Feature: Подвал
"""
from unittest import skip

from ddt import ddt, data

from support.utils.common_utils import priority
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods, HelpNavigateData
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods


@ddt
class Test_Footer(HelpNavigateCheckMethods):
    """
    Story: Секция "Подвал сайта"
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()

        # Переходим на главную
        cls.go_to_main_page(cls.driver)

    @skip('need_auto')
    @priority("Must")
    def test_footer_copyright(self):
        """
        Title: Проверить наличие секции с логотипом УУРРАА и копирайтом
        """
        self.check_footer_copyright()

    @skip('need_auto')
    @priority("High")
    @data(*HelpNavigateData.SUITE_MAIN_FOOTER_CATALOG)
    def test_catalog_links(self, test_data):
        """
        Title: Click: Все ссылки раздела "Каталог" подвала (включая заголовок), ведут на страницу назначения
        """
        self.check_navigate(self.driver, test_data)

    
    @skip('need_auto')
    @priority("Medium")
    @data(*HelpNavigateData.SUITE_MAIN_FOOTER_COMPANY)
    def test_company_links(self, test_data):
        """
        Title: Click: Все ссылки раздела "Компания" подвала, ведут на страницу назначения
        """
        self.check_navigate(self.driver, test_data)

    @skip('need_auto')
    @priority("Medium")
    @data(*HelpNavigateData.SUITE_MAIN_FOOTER_COMPANY_NEW_WINDOW)
    def test_company_links_in_new_window(self, test_data):
        """
        Title: Click: Все ссылки раздела "Компания" подвала, открывающиеся в новом окне,
        ведут на страницу назначения
        """
        self.check_navigate_in_new_window(self.driver, test_data)

    
    @skip('need_auto')
    @priority("Medium")
    @data(*HelpNavigateData.SUITE_MAIN_FOOTER_SUPPORT)
    def test_support_links(self, test_data):
        """
        Title: Click: Все ссылки раздела "Поддержка" подвала, ведут на страницу назначения
        """
        self.check_navigate(self.driver, test_data)

    @skip('need_auto')
    @priority("Medium")
    @data(*HelpNavigateData.SUITE_MAIN_FOOTER_SUPPORT_NEW_WINDOW)
    def test_support_links_in_new_window(self, test_data):
        """
        Title: Click: Все ссылки раздела "Поддержка" подвала, открывающиеся в новом окне,
        ведут на страницу назначения
        """
        self.check_navigate_in_new_window(self.driver, test_data)


    @skip('need_auto')
    @priority("Must")
    def test_name1(self):
        """
        Title: Блок "Контакты" содержит корректный текст, телефоны, почту и адрес компании (...)
        Description: Адрес почты берется из проперти файла и на тесте отличается от прода
        """
        pass

    @classmethod
    def tearDown(cls):
        cls.driver.quit()