# -*- coding: utf-8 -*-
"""
Feature: Навигация по сайту
Description: Простой кликер, переходы по страницам
"""
import time
from unittest import skip

from ddt import ddt, data

from support import service_log
from support.utils.common_utils import generate_sha256, priority
from support.utils.db import databases
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateData
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods

__author__ = 'm.senchuk'


@ddt
class TestMainPageVisitorHeader(HelpNavigateCheckMethods, HelpNavigateData):
    """
    Story: Шапка главной сраницы для посетителя
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

        # Переходим на страницу авторизации
        cls.go_to_main_page(cls.driver)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_HEADER)
    def test_check_header(self, test_data):
        """
        Title: Проверка хедера
        """
        service_log.run(self)
        self.check_header_widget_visitor(self.driver)
        self.check_navigate(self.driver, test_data)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageVisitorRootCategory(HelpNavigateCheckMethods, HelpNavigateData):
    """
    Story: Родительские категории на главной странице для посетителя
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

        # Переходим на страницу авторизации
        cls.go_to_main_page(cls.driver)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_ROOT_CATEGORY)
    def test_check_root_category(self, test_data):
        """
        Title: Главная страница. Переход по каждой из категорий каталога на соответствующую страницу категории
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_click"])
        self.check_navigate(self.driver, test_data)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageVisitorBanners(HelpNavigateCheckMethods, HelpNavigateData):
    """
    Story: Баннеры на главной странице для посетителя
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

        # Переходим на страницу авторизации
        cls.go_to_main_page(cls.driver)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_BANNER_V)
    def test_check_banner_main(self, test_data):
        """
        Title: Баннеры для Посетителя - на ротаторе
        """
        service_log.run(self)
        test_data["second_click"] = HelpNavigateData.click_main.MAIN_BANNER
        self.check_navigate_two_click(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_BANNER_RIGHT)
    def test_check_banner_right(self, test_data):
        """
        Title: Баннеры для Посетителя - справа
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_click"])
        self.check_navigate(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_BANNER_WIDTH)
    def test_check_banner_width(self, test_data):
        """
        Title: Баннеры для Посетителя - внизу
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_click"])
        self.check_navigate(self.driver, test_data)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageVisitorFooter(HelpNavigateCheckMethods, HelpNavigateData):
    """
    Story: Подвал на главной странице для посетителя
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

        # Переходим на страницу авторизации
        cls.go_main(cls.driver, flag_auth=False)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_FOOTER_NEW_WINDOW)
    def test_check_footer(self, test_data):
        """
        Title: Переходы по ссылкам из подвала
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_click"])
        self.check_navigate(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_FOOTER_NEW_WINDOW)
    def test_check_footer_in_new_window(self, test_data):
        """
        Title: Тест проверяет переход по кнопкам из подвала (Вакансии, Контакты)
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_click"])
        self.check_navigate_in_new_window(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    def test_check_footer_copyright(self):
        """
        Title: Проверка - логотип уурраа - текст 2015 © OORRAA.com Все права защищены - отсутствие строчки с версией
        """
        self.check_footer_copyright(self.driver)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageVisitorSpecialBlocks(HelpNavigateCheckMethods, HelpNavigateData):
    """
    Story: Спец-категории на главной странице для посетителя
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

        # Переходим на страницу авторизации
        cls.go_to_main_page(cls.driver)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_SPECIAL_CATEGORY)
    def test_check_special_category(self, test_data):
        """
        Title: Проверка перехода по заголовкам спец категорий в спец категории на главной
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_click"])
        self.check_navigate(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    @data(*range(1, 2))
    def test_check_last_deals_in_good_page(self, number_good, test_data=HelpNavigateData.MAIN_LAST_DEALS_TO_GOOD):
        """
        Title: Проверка перехода на страницу товара из спец категории Последние сделки с главной
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_xpath_good"] % number_good)
        self.check_navigate_in_good_page(self.driver, test_data, number_good)

    @skip('deprecated')
    @priority('low')
    @data(*range(1, 2))
    def test_check_best_sell_in_good_page(self, number_good, test_data=HelpNavigateData.MAIN_GOOD_BEST_SELLERS_TO_GOOD):
        """
        Title: Проверка перехода на страницу товара из спец категории Товары от лучших продавцов с главной
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_xpath_good"] % number_good)
        self.check_navigate_in_good_page(self.driver, test_data, number_good)

    @skip('deprecated')
    @priority('low')
    @data(*range(1, 2))
    def test_check_best_sell_in_shop_page(self, number_good, test_data=HelpNavigateData.MAIN_NAME_BEST_SELLERS_TO_SHOP):
        """
        Title: Проверка перехода на страницу магазина из спец категории Товары от лучших продавцов с главной
        """
        service_log.run(self)
        self.check_navigate_in_good_page(self.driver, test_data, number_good)

    @skip('deprecated')
    @priority('low')
    @data(*range(1, 2))
    def test_check_new_good_in_good_page(self, number_good, test_data=HelpNavigateData.MAIN_NEW_GOOD_TO_GOOD):
        """
        Title: Проверка перехода на страницу товара из спец категории Новинки с главной
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_xpath_good"] % number_good) 1
        self.check_navigate_in_good_page(self.driver, test_data, number_good)

    @skip('deprecated')
    @priority('low')
    @data(*range(1, 2))
    def test_check_popular_in_good_page(self, number_good, test_data=HelpNavigateData.MAIN_POPULAR_GOOD_TO_GOOD):
        """
        Title: Проверка перехода на страницу товара из спец категории Популярные товары с главной
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_xpath_good"] % number_good)
        self.check_navigate_in_good_page(self.driver, test_data, number_good)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageBuyerHeader(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Шапка на главной странице для покупателя
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.B_SUITE_MAIN_HEADER)
    def test_check_header(self, test_data):
        """
        Title: Проверка перехода по кнопкам сделки и сообщени и избранное для покупателя
        """
        service_log.run(self)
        self.check_header_widget_buyer(self.driver, self.user["id"])
        self.check_navigate(self.driver, test_data)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageBuyerRootCategory(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Родительские категории на главной странице для покупателя
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_ROOT_CATEGORY)
    def test_check_root_category(self, test_data):
        """
        Title: Проверка перехода по родительским категория для покупателя
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_click"])
        self.check_navigate(self.driver, test_data)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageBuyerBanners(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Баннер на главной странице для покупателя
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_BANNER_V)
    def test_check_banner_main(self, test_data):
        """
        Title: Проверка перехода с главной по баннерам ротатора для покупателя
        """
        service_log.run(self)
        test_data["second_click"] = HelpNavigateData.click_main.MAIN_BANNER
        self.check_navigate_two_click(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_BANNER_RIGHT_B)
    def test_check_banner_right(self, test_data):
        """
        Title: Проверка перехода с главной по баннерам справа для покупателя
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_click"])
        self.check_navigate(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_BANNER_WIDTH)
    def test_check_banner_width(self, test_data):
        """
        Title: Проверка перехода с главной по баннерам снизу для покупателя
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_click"])
        self.check_navigate(self.driver, test_data)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageBuyerFooter(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Подвал на главной странице для покупателя
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_FOOTER_NEW_WINDOW)
    def test_check_footer(self, test_data):
        """
        Title: Проверка перехода по ссылкам из подвала для покупателя
        """
        service_log.run(self)
        time.sleep(3)
        #self.check_visible(self.driver, test_data["start_click"])
        self.check_navigate(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_FOOTER_NEW_WINDOW)
    def test_check_footer_in_new_window(self, test_data):
        """
        Title: Тест проверяет пепреход по кнопкам из подвала (Вакансии, Контакты) для покупателя
        """
        service_log.run(self)
        time.sleep(3)
        #self.check_visible(self.driver, test_data["start_click"])
        self.check_navigate_in_new_window(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    def test_check_footer_copyright(self):
        """
        Title: Проверка: логотип уурраа, 2015 © OORRAA.com Все права защищены,отсутствие строчки с версией для покупателя
        """
        self.check_footer_copyright(self.driver)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageBuyerSpecialBlocks(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Спец-категории на главной странице для покупателя
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_SPECIAL_CATEGORY)
    def test_check_special_category(self, test_data):
        """
        Title: Проверка перехода на листинг спец катгории с заголовков спец цкатегории на главной для покупателя
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_click"])
        self.check_navigate(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    @data(*range(1, 2))
    def test_check_last_deals_in_good_page(self, number_good, test_data=HelpNavigateData.MAIN_LAST_DEALS_TO_GOOD):
        """
        Title: Проверка перехода на страницу товара из спец категории Последние сделки с главной для покупателя
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_xpath_good"] % number_good)
        self.check_navigate_in_good_page(self.driver, test_data, number_good)

    @skip('deprecated')
    @priority('low')
    @data(*range(1, 2))
    def test_check_best_sell_in_good_page(self, number_good, test_data=HelpNavigateData.MAIN_GOOD_BEST_SELLERS_TO_GOOD):
        """
        Title: Проверка перехода на страницу товара из спец категории Товары от лучших продавцов с главной для покупателя
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_xpath_good"] % number_good)
        self.check_navigate_in_good_page(self.driver, test_data, number_good)

    @skip('deprecated')
    @priority('low')
    @data(*range(1, 2))
    def test_check_best_sell_in_shop_page(self, number_good, test_data=HelpNavigateData.MAIN_NAME_BEST_SELLERS_TO_SHOP):
        """
        Title: Проверка перехода на страницу магазина из спец категории Товары от лучших продавцов с главной для покупателя
        """
        service_log.run(self)
        self.check_navigate_in_good_page(self.driver, test_data, number_good)

    @skip('deprecated')
    @priority('low')
    @data(*range(1, 2))
    def test_check_new_good_in_good_page(self, number_good, test_data=HelpNavigateData.MAIN_NEW_GOOD_TO_GOOD):
        """
        Title: Проверка перехода на страницу товара из спец категории Новинки с главной для покупателя
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_xpath_good"] % number_good)
        self.check_navigate_in_good_page(self.driver, test_data, number_good)

    @skip('deprecated')
    @priority('low')
    @data(*range(1, 2))
    def test_check_popular_in_good_page(self, number_good, test_data=HelpNavigateData.MAIN_POPULAR_GOOD_TO_GOOD):
        """
        Title: Проверка перехода на страницу товара из спец категории Популярные товары с главной для покупателя
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_xpath_good"] % number_good)
        self.check_navigate_in_good_page(self.driver, test_data, number_good)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageSellerHeader(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Шапка на главной странице для продавца
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SELLER_MAIN_HEADER)
    def test_check_header(self, test_data):
        """
        Title: Проверка перехода по кнопкам сделки и сообщени и избранное для продавца
        """
        service_log.run(self)
        self.check_header_widget_seller(self.driver, self.user["id"])
        self.check_navigate(self.driver, test_data)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageSellerRootCategory(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Родительские категории на главной странице для продавца
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_ROOT_CATEGORY)
    def test_check_root_category(self, test_data):
        """
        Title: Проверка перехода по родительским категория для продавца
        """
        service_log.run(self)
        #self.check_visible(self.driver, test_data["start_click"])
        self.check_navigate(self.driver, test_data)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageSellerBanners(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Баннеры на главной странице для продавца
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()


        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_BANNER_S)
    def test_check_banner_main(self, test_data):
        """
        Title: Проверка перехода с главной по баннерам ротатора для продавца
        """
        service_log.run(self)
        test_data["second_click"] = HelpNavigateData.click_main.MAIN_BANNER
        self.check_navigate_two_click(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SELLER_BANNER_RIGHT)
    def test_check_banner_right(self, test_data):
        """
        Title: Проверка перехода с главной по баннерам справа для продавца
        """
        service_log.run(self)
        self.check_navigate(self.driver, test_data)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageSellerFooter(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Подвал на главной странице для продавца
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_FOOTER_NEW_WINDOW)
    def test_check_footer(self, test_data):
        """
        Title: Проверка перехода по ссылкам из подвала для продавца
        """
        service_log.run(self)
        time.sleep(3)
        #self.check_visible(self.driver, test_data["start_click"])
        self.check_navigate(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_FOOTER_NEW_WINDOW)
    def test_check_footer_in_new_window(self, test_data):
        """
        Title: Тест проверяет пепреход по кнопкам из подвала (Вакансии, Контакты) для продавца
        """
        service_log.run(self)
        time.sleep(3)
        #self.check_visible(self.driver, test_data["start_click"])
        self.check_navigate_in_new_window(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    def test_check_footer_copyright(self):
        """
        Title: Проверка копирайта
        Description:
            - логотип уурраа
            - текст 2014 © OORRAA.com Все права защищены
            - отсутствие строчки с версией (ОБязательно)
        """
        self.check_footer_copyright(self.driver)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageSellerSpecialBlocks(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Спец-категории на главной странице для продавца
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SELLER_SPECIAL_CATEGORY)
    def test_check_special_category(self, test_data):
        """
        Title: Проверка перехода на листинг спец катгории с заголовков спец цкатегории на главной для продавца
        """
        service_log.run(self)
        self.check_navigate(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    @data(*range(1, 2))
    def test_check_last_deals_in_good_page(self, number_good, test_data=HelpNavigateData.MAIN_LAST_DEALS_TO_GOOD):
        """
        Title: Проверка перехода на страницу товара из спец категории Последние сделки с главной для продавца
        """
        service_log.run(self)
        self.check_navigate_in_good_page(self.driver, test_data, number_good)

    @skip('deprecated')
    @priority('low')
    @data(*range(1, 2))
    def test_check_new_good_in_good_page(self, number_good, test_data=HelpNavigateData.MAIN_NEW_GOOD_TO_GOOD):
        """
        Title: Проверка перехода на страницу товара из спец категории Новинки с главной для продавца
        """
        service_log.run(self)
        self.check_navigate_in_good_page(self.driver, test_data, number_good)

    @skip('deprecated')
    @priority('low')
    @data(*range(1, 2))
    def test_check_popular_in_good_page(self, number_good, test_data=HelpNavigateData.MAIN_POPULAR_GOOD_TO_GOOD):
        """
        Title: Проверка перехода на страницу товара из спец категории Популярные товары с главной для покупателя
        """
        service_log.run(self)
        self.check_navigate_in_good_page(self.driver, test_data, number_good)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageCategory(HelpNavigateCheckMethods, HelpNavigateData):
    """
    Story: Категории на главной странице
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

        # Переходим на страницу авторизации
        cls.go_main(cls.driver,flag_auth=False)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_MAIN_ROOT_CATEGORY)
    def test_check_final_category(self, test_data, sleep=2):
        """
        Title: Главная страница. Переход на любую из подкатегорий на соответствующую страницу подкатегории.
        """
        service_log.run(self)
        # Получаем объект рутовой категории
        obj_root_category = self.get_element_navigate(self.driver, test_data['start_click'])
        # Наводим мышку на рутовую категорию - открывается список финальных категорий
        self.move_to_element(self.driver, obj_root_category)
        time.sleep(sleep)
        # Получаем список финальных категорий для рутовой категории obj_root_category
        obj_list_elements = self.get_list_elements(self.driver, test_data['start_click'] +
                                                   HelpNavigateData.path_main.PATH_ALL_FINAL_CATEGORY)
        # Удаляем первый элемент из списка финальных категорий,э то финальная категория "Все товары", она скрыта
        del obj_list_elements[00]

        # Собираем список из названий финальных категорий
        text_list_elements = []
        for obj_element in obj_list_elements:
            text_list_elements.append(obj_element.text.encode('utf-8'))
        self.assertNotEqual(text_list_elements, [], "ERROR: Empty list items.")
        # Проверяем переходы по клику на название финальной категорий на нужный листинг категории (первые две категории).
        for text_element in text_list_elements[:2]:
            obj_click = self.get_element_navigate(self.driver, test_data['start_click'] +
                                                  HelpNavigateData.path_main.PATH_FINAL_CATEGORY % text_element)
            obj_click.click()
            self.get_element_navigate(self.driver, HelpNavigateData.path_category.CAT_PATH_FINAL_CATEG % text_element)
            self.go_to_main_page(self.driver)
            obj_root_category = self.get_element_navigate(self.driver, test_data['start_click'])
            self.move_to_element(self.driver, obj_root_category)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestCategoryPageTreeCategory(HelpNavigateCheckMethods, HelpNavigateData):
    """
    Story: Дерево категорий в каталоге
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.ROOT_CATEGORY_SUITE)
    def test_check_tree_category(self, test_data):
        """
        Title: Проверка переходов по дереву категорий и из каждой финальной категории на страницу товара
        """
        service_log.run(self)
        # Переходим на страницу рутовой категории
        self.get_page(self.driver, HelpNavigateData.path_category.URL_PATH_ROOT_CATEGORY % test_data)

        # Получаем список дерева категорий для рутовой категории test_data['category_path']
        obj_list_elements = self.get_list_elements(self.driver, HelpNavigateData.path_category.PATH_TREE_CATEGORY)

        # Собираем список из названий дерева категорий
        text_list_elements = []
        service_log.put("obj_list_elements: " + str(obj_list_elements))
        for obj_element in obj_list_elements:
            text_list_elements.append(obj_element.text.encode('utf-8'))

        self.assertNotEqual(text_list_elements, [], "ERROR: Empty list items.")

        # Проверяем переходы по клику на название дерева категорий на нужный листинг категории.
        for text_element in text_list_elements[:4]:
            obj_click = self.get_element_navigate(self.driver, HelpNavigateData.click_catalog.LINK_TREE_CATEGORY
                                                  % text_element)
            obj_click.click()
            self.get_element_navigate(self.driver, HelpNavigateData.check_catalog.FINAL_CATEGORY % text_element)
            self.get_element_navigate(self.driver, HelpNavigateData.check_catalog.ACTIVE_TREE_CATEGORY % text_element)
            navigate = dict()
            navigate['start_xpath_good'] = "/" + HelpNavigateData.click_main.PATH_GOOD
            navigate['finish_xpath_good'] = HelpNavigateData.check_good.TITLE_GOOD
            self.check_navigate_in_good_page(self.driver, navigate, 1)
            self.get_page(self.driver, HelpNavigateData.path_category.URL_PATH_ROOT_CATEGORY % test_data)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestCategoryPageWindowCategory(HelpNavigateCheckMethods, HelpNavigateData):
    """
    Story: Переходы по категориям
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.WINDOW_CATEGORY_SUITE)
    def test_check_window_category(self, test_data):
        """
        Title: Переход в листинг Все товары, Бестселлеры со страницы родительской категории
        """
        service_log.run(self)
        # Переходим на страницу рутовой категории
        self.get_page(self.driver, HelpNavigateData.path_category.URL_PATH_ROOT_CATEGORY % test_data['category_id'])
        obj_click = self.get_element_navigate(self.driver, HelpNavigateData.click_catalog.LINK_TREE_CATEGORY
                                              % test_data['window_category'])
        obj_click.click()
        self.get_element_navigate(self.driver, HelpNavigateData.check_catalog.FINAL_CATEGORY
                                  % test_data['window_category'])
        self.get_element_navigate(self.driver, HelpNavigateData.check_catalog.ACTIVE_TREE_CATEGORY
                                  % test_data['window_category'])

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.WINDOW_CATEGORY_SUITE)
    def test_check_good_window_category(self, test_data):
        """
        Title: Переход в листинг Все товары и на товар, Бестселлеры со страницы родительской категории
        """
        service_log.run(self)
        # Переходим на страницу рутовой категории
        self.get_page(self.driver, HelpNavigateData.path_category.URL_PATH_ROOT_CATEGORY % test_data['category_id'])
        #Кликаем на первый товар из блока test_data['window_category']
        navigate = dict()
        navigate['start_xpath_good'] = (HelpNavigateData.click_catalog.WINDOW_CATALOG % test_data['window_category'])\
                                       + HelpNavigateData.path_category.PATH_GOOD_IN_WIN_CATALOG
        navigate['finish_xpath_good'] = HelpNavigateData.check_good.TITLE_GOOD
        self.check_navigate_in_good_page(self.driver, navigate, 1)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


##################### Страница Мои товары. Переходы между активными и неактивными, пагинация. #######################
@ddt
class TestMyGoodsPageSeller(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Раздел Мои товары
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)
        cls.get_my_goods_page(cls.driver)  # Переходим на страницу Мои товары
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('low')
    def test_active_inactive_page(self):
        """
        Title: Переход между вкладками активный/неактивный
        """
        test_data = dict(active='Активные', inactive='Неактивные')
        self.check_navigate_active_inactive(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SUITE_ADD_EDIT)
    def test_add_edit_good(self, test_data):
        """
        Title: Добавить товар/ редактировать товар - проверка кнопок
        """
        self.check_navigate(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    def test_go_good(self, test_data=HelpNavigateData.MG_TO_GOOD, list_xpath=HelpNavigateData.MG_GOOD):
        """
        Title: Переход с моих товаров на страницу товара
        """
        self.check_navigate_in_good_page(self.driver, test_data, 1)
        self.check_mini(self.driver, list_xpath)

    @skip('deprecated')
    @priority('low')
    def test_paginator_number(self):
        """
        Title: Проверка пагинатора на странице мои товары (переход по цифрам)
        """
        items = self.get_paginator_items(self.driver, HelpNavigateData.path_my_goods.PAGINATOR_LIST)
        #items.reverse()
        info_good = HelpNavigateData.check_my_goods.SHOT_INFO_GOOD % 1
        self.check_paginator_items(self.driver, items[1:], info_good)

    @skip('deprecated')
    @priority('low')
    def test_paginator_prev_next(self):
        """
        Title: Проверка пагинатора на странице мои товары (переход по стрелкам)
        """
        items = self.get_paginator_items(self.driver, HelpNavigateData.path_my_goods.PAGINATOR_LIST)
        leng = len(items)-1
        info_good = HelpNavigateData.check_my_goods.SHOT_INFO_GOOD % 1
        self.check_paginator_next_prev(self.driver, leng, info_good)


    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


##################### Страница Помошь. Переходы по кнопкам для разных ролей со страницы помощи. #######################
@ddt
class TestHelpPagesToAllRoles(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Раздел Помощь
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('low')
    @data('buyer', 'seller')
    def test_to_catalog_buyer_seller(self, user_role, test_data=HelpNavigateData.HELP_PAGE_GO_SUITE):
        """
        Title: Переход в каталог со страницы помощи для продавца и покупателя
        """
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role=user_role)
        self.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_auth=True)

        # Переходим на страницу Помощь, Как покупать на уурраа!
        self.get_page(self.driver, HelpNavigateData.path_help.UH_HOW_BUY)
        self.check_navigate(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.HELP_PAGE_VISITOR_SUITE)
    def test_to_help_1_visitor(self, test_data):
        """
        Title: Переход по кнопкам в тексте помощи для посетителя (В каталог, Зарегистрироваться)
        """
        # Переходим на страницу Помощь, Как покупать на уурраа!
        self.get_page(self.driver, HelpNavigateData.path_help.UH_HOW_BUY)
        self.check_navigate(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    def test_to_help_2_visitor(self, test_data=HelpNavigateData.HP_BE_SELLER):
        """
        Title: Переход по кнопкам в тексте помощи для посетителя Как стать продавцом
        """
        # Переходим на страницу Помощь, Как покупать на уурраа!
        self.get_page(self.driver, HelpNavigateData.path_help.UH_HOW_BE_SELLER)
        self.check_navigate(self.driver, test_data)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestShopPageToAllRoles(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Страница магазина
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()

        # Берем тестового продавца на магазине которого будут проводиться проверки
        cls.default_test_seller_id = AccountingMethods.get_default_user_id(role='seller')
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('low')
    @data('seller_alien', 'buyer')
    def test_check_chat_button(self, user_role, check_widget_my_shop=HelpNavigateData.MY_SHOP_CASE):
        """
        Title: ПОКУПАТЕЛЬ или ПРОДАВЕЦ.ЧУЖОЙ МАГАЗИН: Кнопка "Сообщение" ведет на страницу чата с данным продавцом
        """
        default_user_id = AccountingMethods.get_default_user_id(role=user_role)
        self.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_auth=True)

        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.default_test_seller_id)

        service_log.run(self)
        self.check_no_such_element(self.driver, check_widget_my_shop)
        self.check_shop_to_chat(self.driver, self.default_test_seller_id)

    @skip('deprecated')
    @priority('low')
    def test_check_chat_button_visitor(self, test_data=HelpNavigateData.SHOP_TO_CHAT_VISITOR,
                                       check_widget_my_shop=HelpNavigateData.MY_SHOP_CASE):
        """
        Title: ПОСЕТИТЕЛЬ Кнопка "Сообщение" ведет на страницу авторизации
        """
        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.default_test_seller_id)
        test_data['start_click'] = test_data['start_click'] % self.default_test_seller_id
        service_log.run(self)
        self.check_no_such_element(self.driver, check_widget_my_shop)
        self.check_navigate(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    def test_check_chat_button_seller(self, test_data=HelpNavigateData.CHAT_BUTTON_SELLER):
        """
        Title:  Продавец свой магазин - нет кнопки "Сообщение"
        """
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        self.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_auth=True)

        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.default_test_seller_id)

        service_log.run(self)
        test_data['xpath'] = test_data['xpath'] % self.default_test_seller_id
        self.check_no_such_element(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    def test_check_go_good_visitor(self, test_data=HelpNavigateData.SHP_TO_GOOD):
        """
        Title: Переход на страницу товара посетителем
        """
        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.default_test_seller_id)
        self.check_navigate_in_good_page(self.driver, test_data, 1)

    @skip('deprecated')
    @priority('low')
    def test_paginator_number(self, seller_big_data=96):
        """
        Title: Пагинация на странице магазина
        """
        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % seller_big_data)
        items = self.get_paginator_items(self.driver, HelpNavigateData.path_my_goods.PAGINATOR_LIST)
        items.reverse()
        info_good = HelpNavigateData.click_shop.GOOD % 1
        self.check_paginator_items(self.driver, items, info_good)

    @skip('deprecated')
    @priority('low')
    def test_paginator_prev_next(self, seller_big_data=96):
        """
        Title: Пагинация стрелочками на странице магазина
        """
        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % seller_big_data)
        items = self.get_paginator_items(self.driver, HelpNavigateData.path_my_goods.PAGINATOR_LIST)
        leng = len(items)-1
        info_good = HelpNavigateData.click_shop.GOOD % 1
        self.check_paginator_next_prev(self.driver, leng, info_good)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.SHP_TO_SELLER_BTN)
    def test_button_seller_add_good_settings(self, test_data):
        """
        Title: Переход в настройки
        """
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        self.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_auth=True)

        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.default_test_seller_id)
        self.check_navigate(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    def test_check_seller_info(self):
        """
        Title: Инфо о продавце
        """
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        self.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        databases.db1.accounting.update_shop_details_by_criteria(self.user["shop_id"], "address='test magazin'")
        self.shop = databases.db1.accounting.get_shop_details_by_shop_id(self.user["shop_id"])[0]
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_auth=True)

        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.default_test_seller_id)


        check_list = {"1": HelpNavigateData.check_shop.NOTIFY_MY_SHOP,
                      "2": HelpNavigateData.check_shop.INFO_URL % self.user["id"],
                      "3": HelpNavigateData.check_shop.INFO_ADDRESS % self.shop["address"]}
        self.check_mini(self.driver, check_list)
        #seller_name = self.get_element_navigate(self.driver, HelpNavigateData.check_shop.NAME_SELLER).text.encode('utf-8')
        #self.assertEqual(self.user["display_name"], seller_name)

    @skip('deprecated')
    @priority('low')
    def test_empty_address_shop(self, test_data=HelpNavigateData.EMPTY_SHOP_ADDRESS_CASE):
        """
        Title: Проверить что при не заполненном Адресе магазина, данное поле не выводится в магазине продавца
        """
        # Получаем ID продавцов из таблицы account_details_groups
        self.users_by_role = databases.db1.accounting.get_user_by_role(need_role='2', not_role='3,4')
        # Делаем из полученных значений список ID продавцов
        users = []
        for user_by_role in self.users_by_role:
            users.append(str(user_by_role.get("account_details_id")))
        # Получаем продавца в статусе ENABLED без заполненного поля адрес магазина
        self.user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                                  criteria="shop_id IS NULL AND id IN (%s)"
                                                                           % ', '.join(users))[0]
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.user["id"])
        self.check_no_such_element(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    def test_check_hide_widget_my_shop(self, check_widget_my_shop=HelpNavigateData.MY_SHOP_CASE):
        """
        Title: При Logout плашка "Это ваш магазин" исчезает
        """
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        self.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        databases.db1.accounting.update_shop_details_by_criteria(self.user["shop_id"], "address='test magazin'")
        self.shop = databases.db1.accounting.get_shop_details_by_shop_id(self.user["shop_id"])[0]
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_auth=True)

        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.default_test_seller_id)

        check_list = {"1": HelpNavigateData.check_shop.NOTIFY_MY_SHOP,
                      "2": HelpNavigateData.check_shop.INFO_URL % self.user["id"],
                      "3": HelpNavigateData.check_shop.INFO_ADDRESS % self.shop["address"]}
        self.check_mini(self.driver, check_list)
        service_log.put("STEP 1.1. Find current url.")
        start_url = self.get_current_url(self.driver)
        self.logout(self.driver)
        service_log.put("STEP 2.2. Find current url before click.")
        finish_url = self.get_current_url(self.driver)
        service_log.put("STEP 2.3. Compare 'finish_url' with 'start_url'.")
        self.assertEqual(finish_url, start_url, "ОШИБКА: Урлы не совпадают, после логина произошел переход на "
                                                "страницу %s" % finish_url.encode('utf-8'))
        service_log.put("Success! Compare 'finish_url' with 'start_url'.")
        self.check_no_such_element(self.driver, check_widget_my_shop)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestGoodPage(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Страница товара
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()

        # Берем тестового продавца на магазине которого будут проводиться проверки
        cls.default_test_seller_id = AccountingMethods.get_default_user_id(role='seller')
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.GOOD_PAGE_IN_SHOP_PAGE_SUITE)
    def test_check_go_shop_page(self, test_data, test_good=HelpNavigateData.SHP_TO_GOOD):
        """
        Title: Переход по: кнопке "В магазин" на магазин продавца, аватарке продавца, кнопке "Показать больше"
        """
        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.default_test_seller_id)
        self.check_navigate_in_good_page(self.driver, test_good, 1)
        test_data['start_click'] = test_data['start_click'] % self.default_test_seller_id
        self.check_navigate(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    @data(*range(1, 4))
    def test_check_go_good_page(self, num_good, test_data=HelpNavigateData.GOOD_PAGE_TO_GOOD_CASE,
                                test_good=HelpNavigateData.SHP_TO_GOOD):
        """
        Title: переход по товару в блоке Другие товары продавца на карточку данного товара
        """
        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.default_test_seller_id)
        self.check_navigate_in_good_page(self.driver, test_good, 1)
        self.check_navigate_in_good_page(self.driver, test_data, num_good)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.BREADCRUMBS_SUITE)
    def test_check_go_breadcrumbs(self, test_data, test_good=HelpNavigateData.SHP_TO_GOOD):
        """
        Title: Переход по хлебным крошкам в категорию и переход по хлебным крошам в подкатегорию.
        """
        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.default_test_seller_id)
        self.check_navigate_in_good_page(self.driver, test_good, 1)
        self.check_navigate_in_good_page(self.driver, test_data, test_data['brc_num'])

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestFavoritePage(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Избранное
    """
    @classmethod
    def setUp(cls):
        # Берем тестового продавца на магазине которого будут проводиться проверки
        cls.default_test_seller_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(cls.default_test_seller_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('low')
    def test_check_good_user_favorite_pages(self):
        """
        Title: Переход между на вкладку Товары. Переход на вкладку Пользователи
        """
        # Переход в Избранное
        self.check_navigate(self.driver, self.MAIN_TO_FAVORITE)
        test_data = dict(goods='Товары', users='Пользователи')
        self.check_navigate_good_user_favorite(self.driver, test_data)

    @skip('deprecated')
    @priority('low')
    def test_check_good_pages_to_good(self, test_data=HelpNavigateData.FAV_GOOD_TO_GOOD_PAGE):
        """
        Title: Переход на полную карточку товара при клике на фото товара
        """
        # Переход в Избранное
        self.get_page(self.driver, HelpNavigateData.path_favorites.URL_FAVORITES_GOODS)
        self.check_navigate_in_good_page(self.driver, test_data, 1)

    @skip('deprecated')
    @priority('low')
    def test_check_good_pages_to_shop(self, test_data=HelpNavigateData.FAV_GOOD_SELLER_TO_SHOP):
        """
        Title: Переход в магазин продавца при клике на карточку продавца
        """
        # Переход в Избранное
        self.get_page(self.driver, HelpNavigateData.path_favorites.URL_FAVORITES_GOODS)
        self.check_navigate_in_good_page(self.driver, test_data, 1)

    @skip('deprecated')
    @priority('low')
    @data(*HelpNavigateData.FAV_GOOD_TO_BREAD_CATEGORY_SUITE)
    def test_check_good_pages_to_category(self, test_data):
        """
        Title: Переход по хлебным крошкам в категорию и в подкатегорию
        """
        # Переход в Избранное
        self.get_page(self.driver, HelpNavigateData.path_favorites.URL_FAVORITES_GOODS)
        self.check_navigate_in_good_page(self.driver, test_data, test_data['brc_num'])

    @skip('deprecated')
    @priority('low')
    def test_check_user_pages_to_shop(self, test_data=HelpNavigateData.FAV_USER_USER_TO_SHOP):
        """
        Title: Переход в магазин продавца при клике на карточку продавца
        """
        # Переход в Избранное
        self.get_page(self.driver, HelpNavigateData.path_favorites.URL_FAVORITES_USERS)
        self.check_navigate_in_good_page(self.driver, test_data, 1)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()