# -*- coding: utf-8 -*-
"""
Feature: Главная страница
"""
from unittest import skip
from ddt import ddt, data
from support.utils.common_utils import priority
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate
from support import service_log
from support.utils.db import databases
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods
from tests.front_office.main.classes.class_main_page import MainPageCheckMethods as Main


@ddt
class TestMainBanners(Navigate, Main):
    """
    Story: Секция "Главные баннеры"
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        cls.get_page(cls.driver)
        service_log.preparing_env(cls)

    @skip('need_auto')
    @priority("Must")
    @data('visitor', 'user')
    def test_name1(self):
        """
        Title: Проверить отображение главных баннеров в зависимости от роли
        Description:
        * Для Гостя: "УУРРАА в Краснодаре" и "Как покупать и продавать на УУРРАА"
        * Для Зарегистрированного: "УУРРАА в Краснодаре" и "Как покупать и продавать на УУРРАА"
        """
        pass

    @skip('need_auto')
    @priority("Must")
    def test_name1(self):
        """
        Title: Click:  Я могу перейти на страницу назначения баннера, кликнув по нему
        """
        pass

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class Test_Statistic_Section(Navigate, HelpAuthCheckMethods):
    """
    Story: Секция "Статистика"
    """

    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Переходим на главную
        cls.go_to_main_page(cls.driver)

    @priority("Medium")
    def test_stat_banner_item_users(self):
        """
        Title: Проверить корректность выводимых значений: Кол-во покупателей на платформе
        """
        stat_ui = self.element_is_present(self.driver, self.check_main.TEXT_USERS_ON_MAIN)
        text_ui = stat_ui.text.encode('utf-8').replace(' ', '')
        item_users_from_db = (lambda x: x // 100 * 100)(int(databases.db1.accounting.get_count_users()[0]['count']))
        text_db = ("Более\n" + str(item_users_from_db) + "\nпокупателей и продавцов").replace(' ', '')
        e_msg = "Количество пользователей на главной [%s] не совпадает с количестовом из БД [%s]"
        self.assertEqual(text_ui, text_db, e_msg % (text_ui, text_db))


    @priority("Medium")
    def test_stat_banner_item_wares(self):
        """
        Title: Проверить корректность выводимых значений: Кол-во товаров на платформе
        """
        stat_ui = self.get_element_navigate(self.driver, self.check_main.TEXT_WARES_ON_MAIN)
        text_ui = stat_ui.text.encode('utf-8').replace(' ', '')
        item_wares_from_db = (lambda x: x // 100 * 100)(int(databases.db7.warehouse.get_count_wares()[0]['count']))
        text_db = "Более\n" + str(item_wares_from_db) + "\nтоваров"
        e_msg = "Количество товаров на главной [%s] не совпадает с количестовом из БД [%s]"
        self.assertEqual(text_ui, text_db, e_msg % (text_ui, text_db))

    @skip('manual')
    @priority("Medium")
    def test_stat_banner_item_seller(self):
        """
        Title: Проверить Баннер Видео о компании и переход на соответствующую страницу при клике на него
        """

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class TestSectionsCatalog():
    """
    Story: Блоки Разделов каталога ("Одежда". "Обувь и аксессуары и пр.")
    """

    @skip('manual')
    @priority("Must")
    def test_name5(self):
        """
        Title: Я вижу 6ть блоков, название каждого = названию Раздела каталога
        """
        pass

    @skip('manual')
    @priority("Must")
    def test_name5(self):
        """
        Title: В каждом блоке отображается по 4-е товара удовлетворяющих условию: [Accepted] & [Активный]
        (проверить каждый товар, каждого блока)
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_name5(self):
        """
        Title: Если переместить товар, отображающийся в этом блоке в [Неактивные], то он пропадет из блока
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_name5(self):
        """
        Title: В заголовке каждого блока раздела содержится список категорий данного раздела
        (проверить порядок и содержание в соответствии с моделью каталога)
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_name5(self):
        """
        Title: Если все категории не помещаются, то часть скрывается под выпадающим списком "Еще"
        """
        pass

    @skip('manual')
    @priority("Must")
    def test_name5(self):
        """
        Title: Click:  Я могу перейти на страницу Раздела ("Одежда", "Обувь и акссесуары",  и.т.д), кликнув по заголовку соответствующего блока
        (проверить для каждого Раздела)
        """
        pass

    @skip('manual')
    @priority("Must")
    def test_name5(self):
        """
        Title: Click:  Я могу перейти на страницу Категории раздела, кликнув по соответствующей ссылке в блоке раздела
        (проверить для каждой категории, каждого раздела)
        """
        pass

    @skip('manual')
    @priority("Must")
    def test_name5(self):
        """
        Title: Click: Я могу перейти на любой товар, экспресс-карточка которого есть на главной страницы, кликнув по ней
        (проверить для каждого товара)
        """
        pass


class TestBannersOnMain():
    """
    Story: Баннеры на главной
    """

    @skip('need_auto')
    @priority("Must")
    def test_9(self):
        """
        Title: Проверить отображение второстепенных баннеров на главной и переходы на страницы назначения баннера, кликнув на нем
        (для каждого баннера главной)
        """
        pass