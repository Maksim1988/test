# -*- coding: utf-8 -*-
"""
Feature: Каталог
Description: Набор тестов для проверки функционала каталог
"""
import time
from unittest import skip

from ddt import ddt, data

from support import service_log
from support.utils.db import databases
from support.utils.common_utils import generate_sha256, priority
from support.utils.thrift4req import services
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateData
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods
from tests.worker_warehouse.class_warehouse import WarehouseCheckMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods

__author__ = 'm.senchuk'

@ddt
class TestCatalogFinalCategory(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods, WarehouseCheckMethods,
                               HelpLifeCycleCheckMethods):
    """
    Story: Финальная категория
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

        # Переходим на главную
        cls.go_main(cls.driver, flag_auth=False)

    def get_final_filter(self, filters):
        """

        :param filters:
        :return:
        """
        dict = {"clothing": ["clothing_shape"],
                "shoes": ["shoes_shape"],
                "underwear": ["underwear_type"],
                "accessories": ["accessories_type", "jewelry_type"],
                "textile": ["textiles_type"],
                "children": ["children_type", "children_shoes_type"]
        }
        keys = filters.keys()
        root_filter = filters['macro_type']['value']
        for root in dict[root_filter]:
            for key in keys:
                if key == root:
                    final_filter = filters[key]
        return root_filter, final_filter

    @skip('deprecated')
    @priority('medium')
    @data(*HelpNavigateData.ROOT_CATEGORY_SUITE)
    def test_final_catalog_good_status(self, test_data):
        """
        Title: Проверить что страница содержит только товары удовлетворяющие условию ...
        """
        service_log.run(self)
        # Переходим на страницу рутовой категории
        self.get_page(self.driver, HelpNavigateData.path_category.URL_PATH_ROOT_CATEGORY % test_data)
        # Получаем список дерева категорий для рутовой категории test_data['category_path']
        obj_list_elements = self.get_list_elements(self.driver, HelpNavigateData.path_category.PATH_TREE_CATEGORY)

        # Собираем список из названий дерева категорий
        text_list_elements = []
        for obj_element in obj_list_elements:
            text_list_elements.append(obj_element.text.encode('utf-8'))
        self.assertNotEqual(text_list_elements, [], "ERROR: Empty list items.")
        need_final_categories = text_list_elements[2:3]
        # Проверяем переходы по клику на название дерева категорий на нужный листинг категории.
        for need_final_category in need_final_categories:
            obj_click = self.driver.find_element_by_xpath(HelpNavigateData.click_catalog.LINK_TREE_CATEGORY
                                                          % need_final_category)
            obj_click.click()
            self.get_element_navigate(self.driver, HelpNavigateData.check_catalog.FINAL_CATEGORY % need_final_category)
            self.get_element_navigate(self.driver, HelpNavigateData.check_catalog.ACTIVE_TREE_CATEGORY %
                                      need_final_category)
            list_good_id = self.get_good_id_from_page_source(self.driver, self.path_category.TO_FIND_GOODS)
            str_good = ''
            for good_id in list_good_id:
                str_good += "'" + good_id + "'"
                str_good += ", "
            wares_cassandra = databases.db0.warehouse.get_wares_by_ware_ids(str_good[:-2])
            self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
            for ware_cassandra in wares_cassandra:
                self.update_data_content(ware_cassandra, self.deserialize_content(ware_cassandra['content']))
                self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
                msg_error = "Статус товара не равен 1 или 2 - опубликованному или прошедшему модерацию"
                self.assertLessEqual(ware_cassandra['moderation_state'], 2, msg_error)

            filters = wares_cassandra[0]['content']['enumFields']
            root_filter, final_filter = self.get_final_filter(filters)

            goods_elastic = databases.db2.warehouse.get_wares_final_category(size=len(list_good_id),
                                                                             macro_value=root_filter,
                                                                             final_filter=final_filter)
            creation_time = 2422539153447
            list_good_elastic = []
            for good_elastic in goods_elastic[u'hits'][u'hits']:
                self.assertLess(good_elastic[u'_source'][u'creationTimestamp'], creation_time)
                list_good_elastic.append(good_elastic[u'_id'].encode('utf-8'))
                creation_time = good_elastic[u'_source'][u'creationTimestamp'] + 1

            msg_error = "Список товаров из блока новинки не совпал со списком популярных товаров из elastic search"
            self.assertListEqual(list_good_id, list_good_elastic, msg_error)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class TestCatalogShop(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods, WarehouseCheckMethods,
                      HelpLifeCycleCheckMethods):
    """
    Story: Каталог товаров в магазине
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

        # Берем тестового продавца
        default_test_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_test_user_id)[0]

        # Переходим на страницу магазина
        cls.get_page(cls.driver, HelpNavigateData.path_shop.URL_SHOP % cls.user["id"])
        # Ждем, чтобы страница подгрузилась
        time.sleep(HelpNavigateData.time_sleep)

    @skip('deprecated')
    @priority('medium')
    def test_seller_shop_good_status(self):
        """
        Title: Отображаются только АКТИВНЫЕ товары (Активные.В модерации или Активные.Утвержден)
        """
        service_log.run(self)
        # получаем список id товаров
        list_good_id = self.get_good_id_from_page_source(self.driver, self.path_shop.TO_FIND_GOODS)
        str_good = ''
        for good_id in list_good_id:
            str_good += "'" + good_id + "'"
            str_good += ", "
        wares_cassandra = databases.db0.warehouse.get_wares_by_ware_ids(str_good[:-2])
        self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
        for ware_cassandra in wares_cassandra:
            self.assertEqual(ware_cassandra['shop_id'], self.user["id"], "Id продавца не совпадает с shop_id")
            self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
            msg_error = "Статус товара не равен 1 или 2 - опубликованному или прошедшему модерацию"
            self.assertLessEqual(ware_cassandra['moderation_state'], 2, msg_error)

    @skip('deprecated')
    @priority('medium')
    def test_seller_shop_switch_good_status(self):
        """
        Title: Отображаются только АКТИВНЫЕ товары (Активные.В модерации или Активные.Утвержден)
        """
        service_log.run(self)
        # получаем список id товаров
        list_good_id = self.get_good_id_from_page_source(self.driver, self.path_shop.TO_FIND_GOODS)
        str_good = ''
        for good_id in list_good_id:
            str_good += "'" + good_id + "'"
            str_good += ", "
        # Первый товар преводим в статус НЕАКТИВНЫЙ
        name_stock_state = 'HIDDEN'
        stock_state = self.get_StockState(name_stock_state)
        services.warehouse.root.tframed.makePublication(list_good_id[0], stock_state)
        # Проверяем, что товар перешел в статус HIDDEN
        ware_cassandra = databases.db0.warehouse.get_wares_by_ware_id(list_good_id[0])[0]
        self.assertEqual(ware_cassandra['stock_state'], stock_state, "Статус товара не равен 3 - неактивному товару")
        # Обновляем страницу магазина
        self.driver.refresh()
        HelpNavigateCheckMethods.progress(self.driver)
        time.sleep(self.time_sleep)
        # Получаем обновленный список товаров на странице магазина
        list_good_id_new = self.get_good_id_from_page_source(self.driver, self.path_shop.TO_FIND_GOODS)
        msg_error = "Неактивный товар присутствует в обновленном списке товаров на странице магазина."
        self.assertEqual(list_good_id_new.count(list_good_id[0]), 0, msg_error)
        str_good_new = ''
        for good_id_new in list_good_id_new:
            str_good_new += "'" + good_id_new + "'"
            str_good_new += ", "
        wares_cassandra = databases.db0.warehouse.get_wares_by_ware_ids(str_good_new[:-2])
        self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
        for ware_cassandra in wares_cassandra:
            self.assertEqual(ware_cassandra['shop_id'], self.user["id"], "Id продавца не совпадает с shop_id")
            self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
            msg_error = "Статус товара не равен 1 или 2 - опубликованному или прошедшему модерацию"
            self.assertLessEqual(ware_cassandra['moderation_state'], 2, msg_error)
        # Первый товар преводим в статус АКТИВНЫЙ
        name_stock_state = 'PUBLISHED'
        stock_state = self.get_StockState(name_stock_state)
        services.warehouse.root.tframed.makePublication(list_good_id[0], stock_state)
        # Проверяем, что товар перешел в статус PUBLISHED
        ware_cassandra = databases.db0.warehouse.get_wares_by_ware_id(list_good_id[0])[0]
        self.assertEqual(ware_cassandra['stock_state'], stock_state, "Статус товара не равен 2 - активному товару")

        # Обновляем страницу магазина
        self.driver.refresh()
        HelpNavigateCheckMethods.progress(self.driver)
        time.sleep(self.time_sleep)
        # Получаем обновленный список товаров на странице магазина
        list_good_id_new_2 = self.get_good_id_from_page_source(self.driver, self.path_shop.TO_FIND_GOODS)
        msg_error = "Активный товар отсутствует в обновленном списке товаров на странице магазина"
        self.assertEqual(list_good_id_new_2.count(list_good_id[0]), 1, msg_error)
        str_good_new_2 = ''
        for good_id_new_2 in list_good_id_new_2:
            str_good_new_2 += "'" + good_id_new_2 + "'"
            str_good_new_2 += ", "
        wares_cassandra_2 = databases.db0.warehouse.get_wares_by_ware_ids(str_good_new_2[:-2])
        self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
        for ware_cassandra in wares_cassandra_2:
            self.assertEqual(ware_cassandra['shop_id'], self.user["id"], "Id продавца не совпадает с shop_id")
            self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
            msg_error = "Статус товара не равен 1 или 2 - опубликованному или прошедшему модерацию"
            self.assertLessEqual(ware_cassandra['moderation_state'], 2, msg_error)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class TestMyGoods(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods, WarehouseCheckMethods,
                  HelpLifeCycleCheckMethods):
    """
    Story: Мои товары
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        databases.db1.accounting.update_account_details_by_criteria(default_user_id, "locale='ru'")
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)

        # Ждем, чтобы страница подгрузилась
        time.sleep(HelpNavigateData.time_sleep)

    @skip('deprecated')
    @priority('medium')
    def test_my_goods_active_page(self):
        """
        Title: Вкладка "Активные" содержит: только товары данного продавца в статусе Активные
        """
        service_log.run(self)
        # получаем список id товаров
        list_good_id = self.get_good_id_from_page_source(self.driver, self.path_my_goods.TO_FIND_GOODS)
        str_good = ''
        for good_id in list_good_id:
            str_good += "'" + good_id + "'"
            str_good += ", "
        wares_cassandra = databases.db0.warehouse.get_wares_by_ware_ids(str_good[:-2])
        self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
        for ware_cassandra in wares_cassandra:
            self.assertEqual(ware_cassandra['shop_id'], self.user["id"], "Id продавца не совпадает с shop_id")
            self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
            msg_error = "Статус товара не равен 1 или 2 - опубликованному или прошедшему модерацию"
            self.assertLessEqual(ware_cassandra['moderation_state'], 2, msg_error)

    @skip('deprecated')
    @priority('medium')
    def test_my_goods_inactive_page(self):
        """
        Title: Вкладка "Неактивные" содержит: товары продавца в статусе Неактивные, Отклоненные модератором и Ожидающие модерации
        """
        service_log.run(self)
        # Переходим на страницу - неактивные
        obj_inactive_page = self.get_element_navigate(self.driver, self.click_my_goods.INACTIVE_PAGE)
        self.click_button(obj_inactive_page)
        # получаем список id товаров
        list_good_id = self.get_good_id_from_page_source(self.driver, self.path_my_goods.TO_FIND_GOODS)
        str_good = ''
        for good_id in list_good_id:
            str_good += "'" + good_id + "'"
            str_good += ", "
        wares_cassandra = databases.db0.warehouse.get_wares_by_ware_ids(str_good[:-2])
        self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
        for ware_cassandra in wares_cassandra:
            self.assertEqual(ware_cassandra['shop_id'], self.user["id"], "Id продавца не совпадает с shop_id")
            self.assertEqual(ware_cassandra['stock_state'], 3, "Статус товара не равен 3 - неактивному товару.")
            msg_error = "Товар в статусах: Отклоненные модератором и Ожидающие модерации, Одобренные или Забанненые."
            self.assertIn(str(ware_cassandra['moderation_state']), '1,2,3,4', msg_error)

    @skip('deprecated')
    @priority('medium')
    def test_my_goods_switch_good_status(self):
        """
        Title: Перемещение товара [В Активные]. Перемещение товара [В Неактивые]
        """
        service_log.run(self)
        # получаем список id товаров
        list_good_id = self.get_good_id_from_page_source(self.driver, self.path_my_goods.TO_FIND_GOODS)
        str_good = ''
        for good_id in list_good_id:
            str_good += "'" + good_id + "'"
            str_good += ", "
        # Первый товар преводим в статус НЕАКТИВНЫЙ
        checkbox = self.get_element_navigate(self.driver, self.click_my_goods.CHECKBOX % list_good_id[0])
        self.click_button(checkbox)
        good_to_inactive = self.get_element_navigate(self.driver, self.click_my_goods.GOOD_BY_ID_TO_STATUS %
                                                     'В неактивные')
        self.click_button(good_to_inactive)
        name_stock_state = 'HIDDEN'
        stock_state = self.get_StockState(name_stock_state)
        #services.warehouse.root.tframed.makePublication(list_good_id[0], stock_state)
        # Проверяем, что товар перешел в статус HIDDEN
        ware_cassandra = databases.db0.warehouse.get_wares_by_ware_id(list_good_id[0])[0]
        self.assertEqual(ware_cassandra['stock_state'], stock_state, "Статус товара не равен 3 - неактивному товару")
        # Обновляем страницу мои товары
        self.driver.refresh()
        HelpNavigateCheckMethods.progress(self.driver)
        time.sleep(self.time_sleep)
        # Получаем обновленный список товаров на странице мои товары - активные
        list_good_id_new = self.get_good_id_from_page_source(self.driver, self.path_my_goods.TO_FIND_GOODS)
        msg_error = "Неактивный товар присутствует в обновленном списке товаров - активные"
        self.assertEqual(list_good_id_new.count(list_good_id[0]), 0, msg_error)
        # Проверяем товары на странице - активные
        str_good_new = ''
        for good_id_new in list_good_id_new:
            str_good_new += "'" + good_id_new + "'"
            str_good_new += ", "
        wares_cassandra_new = databases.db0.warehouse.get_wares_by_ware_ids(str_good_new[:-2])
        self.assertIsNotNone(wares_cassandra_new, "Из базы не были получены товары")
        for ware_cassandra in wares_cassandra_new:
            self.assertEqual(ware_cassandra['shop_id'], self.user["id"], "Id продавца не совпадает с shop_id")
            self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
            msg_error = "Статус товара не равен 1 или 2 - опубликованному или прошедшему модерацию"
            self.assertLessEqual(ware_cassandra['moderation_state'], 2, msg_error)

        # Переходим на страницу - неактивные
        obj_inactive_page = self.get_element_navigate(self.driver, self.click_my_goods.INACTIVE_PAGE)
        self.click_button(obj_inactive_page)
        # получаем список id товаров
        list_good_id_inact = self.get_good_id_from_page_source(self.driver, self.path_my_goods.TO_FIND_GOODS)
        msg_error = "Неактивный товар отсутствует в списке товаров - неактивные"
        self.assertEqual(list_good_id_inact.count(list_good_id[0]), 1, msg_error)
        str_good_inact = ''
        for good_id_inact in list_good_id_inact:
            str_good_inact += "'" + good_id_inact + "'"
            str_good_inact += ", "
        wares_cassandra_inact = databases.db0.warehouse.get_wares_by_ware_ids(str_good_inact[:-2])
        self.assertIsNotNone(wares_cassandra_inact, "Из базы не были получены товары")
        for ware_cassandra in wares_cassandra_inact:
            self.assertEqual(ware_cassandra['shop_id'], self.user["id"], "Id продавца не совпадает с shop_id")
            self.assertEqual(ware_cassandra['stock_state'], 3, "Статус товара не равен 3 - неактивному товару")
            msg_error = "Товар в статусах: Отклоненные модератором и Ожидающие модерации, Одобренные или Забанненые"
            self.assertIn(str(ware_cassandra['moderation_state']), '1,2,3,4', msg_error)

        # Первый товар преводим в статус АКТИВНЫЙ
        checkbox = self.get_element_navigate(self.driver, self.click_my_goods.CHECKBOX % list_good_id[0])
        self.click_button(checkbox)
        good_to_active = self.get_element_navigate(self.driver, self.click_my_goods.GOOD_BY_ID_TO_STATUS % 'В активные')
        self.click_button(good_to_active)
        name_stock_state = 'PUBLISHED'
        stock_state = self.get_StockState(name_stock_state)
        #services.warehouse.root.tframed.makePublication(list_good_id[0], stock_state)
        # Проверяем, что товар перешел в статус PUBLISHED
        ware_cassandra = databases.db0.warehouse.get_wares_by_ware_id(list_good_id[0])[0]
        self.assertEqual(ware_cassandra['stock_state'], stock_state, "Статус товара не равен 2 - активному товару")

        # Обновляем страницу товаров - неактивные
        self.driver.refresh()
        HelpNavigateCheckMethods.progress(self.driver)
        time.sleep(self.time_sleep)

        # получаем список id товаров
        list_good_id_inact_new = self.get_good_id_from_page_source(self.driver, self.path_my_goods.TO_FIND_GOODS)
        msg_error = "Активный товар присутствует в списке товаров - неактивные"
        self.assertEqual(list_good_id_inact_new.count(list_good_id[0]), 0, msg_error)
        # Переходим на страницу - активные
        obj_active_page = self.get_element_navigate(self.driver, self.click_my_goods.ACTIVE_PAGE)
        self.click_button(obj_active_page)
        # получаем список id товаров
        list_good_id_act_new = self.get_good_id_from_page_source(self.driver, self.path_my_goods.TO_FIND_GOODS)
        msg_error = "Активный товар отсутствует в списке товаров - активные"
        self.assertEqual(list_good_id_act_new.count(list_good_id[0]), 1, msg_error)


    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class TestCatalogInMain(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods, WarehouseCheckMethods,
                        HelpLifeCycleCheckMethods):
    """
    Story: Каталог на главной
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        cls.go_main(cls.driver, flag_auth=False)
        time.sleep(HelpNavigateData.time_sleep)
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('medium')
    def test_popular_good_block(self):
        """
        Title: Блок "Популярные товары". Содержимое
        """
        service_log.run(self)
        position = self.get_position_in_page_source(self.driver, self.path_main.HTML_POPULAR_GOODS)
        # получаем список id товаров блока Популярные товары
        list_good_id = self.get_good_id_from_page_source(self.driver, self.path_main.TO_FIND_GOODS, good_count=5,
                                                         cont=position)
        str_good = ''
        for good_id in list_good_id:
            str_good += "'" + good_id + "'"
            str_good += ", "
        wares_cassandra = databases.db0.warehouse.get_wares_by_ware_ids(str_good[:-2])
        self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
        for ware_cassandra in wares_cassandra:
            self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
            msg_error = "Товар не находится в статусе: Доверенный товар / Принятый товар"
            self.assertIn(str(ware_cassandra['moderation_state']), '1,2', msg_error)
        goods_elastic = databases.db2.warehouse.get_popular_wares()
        creation_time = 2422539153447
        list_good_elastic = []
        for good_elastic in goods_elastic[u'hits'][u'hits']:
            msg_error = "У товара нет флага, что он относится к популярным товарам."
            self.assertEqual(good_elastic[u'_source'][u'special_category_marker'], [u'totalpopular'], msg_error)
            self.assertLess(good_elastic[u'_source'][u'creationTimestamp'], creation_time)
            list_good_elastic.append(good_elastic[u'_id'].encode('utf-8'))
            creation_time = good_elastic[u'_source'][u'creationTimestamp'] + 1

        msg_error = "Список товаров из блока новинки не совпал со списком популярных товаров из elastic search"
        self.assertListEqual(list_good_id, list_good_elastic, msg_error)

    @skip('deprecated')
    @priority('medium')
    def test_last_deals_block(self):
        """
        Title: Блок "Последние сделки". Содержимое
        """
        service_log.run(self)
        position = self.get_position_in_page_source(self.driver, self.path_main.HTML_LAST_DEALS)
        # получаем список id товаров блока Последние сделки
        list_good_id = self.get_good_id_from_page_source(self.driver, self.path_main.TO_FIND_GOODS, good_count=5,
                                                         cont=position)
        str_good = ''
        for good_id in list_good_id:
            str_good += "'" + good_id + "'"
            str_good += ", "
        wares_cassandra = databases.db0.warehouse.get_wares_by_ware_ids(str_good[:-2])
        self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
        for ware_cassandra in wares_cassandra:
            self.assertGreaterEqual(ware_cassandra['successful_deals_count'], 1, "У товара нет завершенных сделок")
            self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
            self.assertEqual(ware_cassandra['moderation_state'], 2, "Товар не находится в статусе: Принятый товар")

        goods_elastic = databases.db2.warehouse.get_last_deals_wares()
        last_deal_time = 2422539153447
        list_good_elastic = []
        for good_elastic in goods_elastic[u'hits'][u'hits']:
            self.assertLess(good_elastic[u'_source'][u'lastDealTimestamp'], last_deal_time)
            list_good_elastic.append(good_elastic[u'_id'].encode('utf-8'))
            last_deal_time = good_elastic[u'_source'][u'lastDealTimestamp'] + 1

        msg = "Список товаров из блока новинки не совпал со списком последних сделок - товаров из elastic search"
        self.assertListEqual(list_good_id, list_good_elastic, msg)

    @skip('deprecated')
    @priority('medium')
    def test_goods_from_best_sellers_block(self):
        """
        Title: Блок "Товары от лучших поставщиков". Содержимое
        """

        position = self.get_position_in_page_source(self.driver, self.path_main.HTML_GOODS_FROM_BEST_SELLERS)
        # получаем список id товаров блока Товары от лучших поставщиков
        list_good_id = self.get_good_id_from_page_source(self.driver, self.path_main.TO_FIND_GOODS, good_count=5,
                                                         cont=position)
        str_good = ''
        for good_id in list_good_id:
            str_good += "'" + good_id + "'"
            str_good += ", "
        wares_cassandra = databases.db0.warehouse.get_wares_by_ware_ids(str_good[:-2])
        self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
        for ware_cassandra in wares_cassandra:
            self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
            msg_error = "Товар не находится в статусе: Доверенный товар / Принятый товар"
            self.assertIn(str(ware_cassandra['moderation_state']), '1,2', msg_error)
        goods_elastic = databases.db2.warehouse.get_best_sellers_wares()
        creation_time = 2422539153447
        list_good_elastic = []
        for good_elastic in goods_elastic[u'hits'][u'hits']:
            msg_error = "У товара нет флага, что он относится к bestsellers товарам."
            self.assertEqual(good_elastic[u'_source'][u'special_category_marker'], [u'bestsellers'], msg_error)
            self.assertLess(good_elastic[u'_source'][u'creationTimestamp'], creation_time)
            list_good_elastic.append(good_elastic[u'_id'].encode('utf-8'))
            creation_time = good_elastic[u'_source'][u'creationTimestamp'] + 1

        msg_error = "Список товаров из блока новинки не совпал со списком bestsellers товаров из elastic search"
        self.assertListEqual(list_good_id, list_good_elastic, msg_error)

    @skip('deprecated')
    @priority('medium')
    def test_new_goods_block(self):
        """
        Title: Новые товары. Содержимое
        """
        service_log.run(self)

        position = self.get_position_in_page_source(self.driver, self.path_main.HTML_NEW_GOODS)
        # получаем список id товаров блока Новые товары
        list_good_id = self.get_good_id_from_page_source(self.driver, self.path_main.TO_FIND_GOODS, good_count=5,
                                                         cont=position)
        str_good = ''
        for good_id in list_good_id:
            str_good += "'" + good_id + "'"
            str_good += ", "
        wares_cassandra = databases.db0.warehouse.get_wares_by_ware_ids(str_good[:-2])
        self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
        creation_time = 2422539153447
        for ware_cassandra in wares_cassandra:
            self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
            msg_error = "Товар не находится в статусе: Принятый товар - прошел модерацию и теперь опубликован"
            self.assertEqual(ware_cassandra['moderation_state'], 2, msg_error)

        goods_elastic = databases.db2.warehouse.get_new_wares()
        list_good_elastic = []
        for good_elastic in goods_elastic[u'hits'][u'hits']:
            self.assertLess(good_elastic[u'_source'][u'creationTimestamp'], creation_time)
            list_good_elastic.append(good_elastic[u'_id'].encode('utf-8'))
            creation_time = good_elastic[u'_source'][u'creationTimestamp'] + 1

        msg_error = "Список товаров из блока новинки не совпал со списком товаров новинок из elastic search"
        self.assertListEqual(list_good_id, list_good_elastic, msg_error)


    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class TestCatalogSpecial(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods, WarehouseCheckMethods,
                         HelpLifeCycleCheckMethods):
    """
    Story: Спец-категории
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('medium')
    def test_category_best_sellers(self):
        """
        Title: Категория "Товары от лучших поставщиков". Содержимое
        """
        self.get_page(self.driver, self.path_category.URL_GOODS_FROM_BEST_SELLERS)
        time.sleep(HelpNavigateData.time_sleep)

        # получаем список id товаров блока Товары от лучших поставщиков
        good_count = self.get_count_goods_in_page(self.driver.page_source, self.path_category.TO_FIND_GOODS)
        list_good_id = self.get_good_id_from_page_source(self.driver, self.path_category.TO_FIND_GOODS,
                                                         good_count=good_count)
        str_good = ''
        for good_id in list_good_id:
            str_good += "'" + good_id + "'"
            str_good += ", "
        wares_cassandra = databases.db0.warehouse.get_wares_by_ware_ids(str_good[:-2])
        self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
        for ware_cassandra in wares_cassandra:
            self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
            msg_error = "Товар не находится в статусе: Доверенный товар / Принятый товар"
            self.assertIn(str(ware_cassandra['moderation_state']), '1,2', msg_error)
        goods_elastic = databases.db2.warehouse.get_best_sellers_wares(good_count)
        creation_time = 2422539153447
        list_good_elastic = []
        for good_elastic in goods_elastic[u'hits'][u'hits']:
            msg_error = "У товара нет флага, что он относится к bestsellers товарам."
            self.assertEqual(good_elastic[u'_source'][u'special_category_marker'], [u'bestsellers'], msg_error)
            self.assertLess(good_elastic[u'_source'][u'creationTimestamp'], creation_time)
            list_good_elastic.append(good_elastic[u'_id'].encode('utf-8'))
            creation_time = good_elastic[u'_source'][u'creationTimestamp'] + 1

        msg_error = "Список товаров из блока новинки не совпал со списком bestsellers товаров из elastic search"
        self.assertListEqual(list_good_id, list_good_elastic, msg_error)

    @skip('deprecated')
    @priority('medium')
    def test_category_new_goods(self):
        """
        Title: Новые товары категория. Содержимое
        """
        service_log.run(self)

        self.get_page(self.driver, self.path_category.URL_ALL_WARE_NEW)
        time.sleep(HelpNavigateData.time_sleep)

        # получаем список id товаров категории Новые товары - первая страница
        good_count = self.get_count_goods_in_page(self.driver.page_source, self.path_category.TO_FIND_GOODS)
        list_good_id = self.get_good_id_from_page_source(self.driver, self.path_category.TO_FIND_GOODS,
                                                         good_count=good_count)

        str_good = ''
        for good_id in list_good_id:
            str_good += "'" + good_id + "'"
            str_good += ", "
        wares_cassandra = databases.db0.warehouse.get_wares_by_ware_ids(str_good[:-2])
        self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
        creation_time = 2422539153447
        for ware_cassandra in wares_cassandra:
            self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
            msg_error = "Товар не находится в статусе: Принятый товар - прошел модерацию и теперь опубликован"
            self.assertEqual(ware_cassandra['moderation_state'], 2, msg_error)

        goods_elastic = databases.db2.warehouse.get_new_wares(good_count)
        list_good_elastic = []
        for good_elastic in goods_elastic[u'hits'][u'hits']:
            self.assertLess(good_elastic[u'_source'][u'creationTimestamp'], creation_time)
            list_good_elastic.append(good_elastic[u'_id'].encode('utf-8'))
            creation_time = good_elastic[u'_source'][u'creationTimestamp'] + 1

        msg_error = "Список товаров из блока новинки не совпал со списком товаров новинок из elastic search"
        self.assertListEqual(list_good_id, list_good_elastic, msg_error)

    @skip('deprecated')
    @priority('medium')
    def test_category_last_deals(self):
        """
        Title: Категория "Последние сделки". Содержимое
        """
        service_log.run(self)
        self.get_page(self.driver, self.path_category.URL_ALL_LAST_DEALS)
        time.sleep(HelpNavigateData.time_sleep)

        # получаем список id товаров категории Последние сделки - первая страница
        good_count = self.get_count_goods_in_page(self.driver.page_source, self.path_category.TO_FIND_GOODS)
        list_good_id = self.get_good_id_from_page_source(self.driver, self.path_category.TO_FIND_GOODS,
                                                         good_count=good_count)
        str_good = ''
        for good_id in list_good_id:
            str_good += "'" + good_id + "'"
            str_good += ", "
        wares_cassandra = databases.db0.warehouse.get_wares_by_ware_ids(str_good[:-2])
        self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
        for ware_cassandra in wares_cassandra:
            self.assertGreaterEqual(ware_cassandra['successful_deals_count'], 1, "У товара нет завершенных сделок")
            self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
            self.assertEqual(ware_cassandra['moderation_state'], 2, "Товар не находится в статусе: Принятый товар")

        goods_elastic = databases.db2.warehouse.get_last_deals_wares(good_count)
        last_deal_time = 2422539153447
        list_good_elastic = []
        for good_elastic in goods_elastic[u'hits'][u'hits']:
            self.assertLess(good_elastic[u'_source'][u'lastDealTimestamp'], last_deal_time)
            list_good_elastic.append(good_elastic[u'_id'].encode('utf-8'))
            last_deal_time = good_elastic[u'_source'][u'lastDealTimestamp'] + 1

        msg = "Список товаров из блока новинки не совпал со списком последних сделок - товаров из elastic search"
        self.assertListEqual(list_good_id, list_good_elastic, msg)

    @skip('deprecated')
    @priority('medium')
    def test_category_popular_good(self):
        """
        Title: Категория "Популярные товары". Содержимое
        """
        service_log.run(self)
        self.get_page(self.driver, self.path_category.URL_POPULAR_GOODS)
        time.sleep(HelpNavigateData.time_sleep)

        # получаем список id товаров категории Популярные товары - первая страница
        good_count = self.get_count_goods_in_page(self.driver.page_source, self.path_category.TO_FIND_GOODS)
        list_good_id = self.get_good_id_from_page_source(self.driver, self.path_category.TO_FIND_GOODS,
                                                         good_count=good_count)
        str_good = ''
        for good_id in list_good_id:
            str_good += "'" + good_id + "'"
            str_good += ", "
        wares_cassandra = databases.db0.warehouse.get_wares_by_ware_ids(str_good[:-2])
        self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
        for ware_cassandra in wares_cassandra:
            self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
            msg_error = "Товар не находится в статусе: Доверенный товар / Принятый товар"
            self.assertIn(str(ware_cassandra['moderation_state']), '1,2', msg_error)
        goods_elastic = databases.db2.warehouse.get_popular_wares(good_count)
        creation_time = 2422539153447
        list_good_elastic = []
        for good_elastic in goods_elastic[u'hits'][u'hits']:
            msg_error = "У товара нет флага, что он относится к популярным товарам."
            self.assertEqual(good_elastic[u'_source'][u'special_category_marker'], [u'totalpopular'], msg_error)
            self.assertLess(good_elastic[u'_source'][u'creationTimestamp'], creation_time)
            list_good_elastic.append(good_elastic[u'_id'].encode('utf-8'))
            creation_time = good_elastic[u'_source'][u'creationTimestamp'] + 1

        msg_error = "Список товаров из блока новинки не совпал со списком популярных товаров из elastic search"
        self.assertListEqual(list_good_id, list_good_elastic, msg_error)


    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestParentCategory(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods, WarehouseCheckMethods,
                         HelpLifeCycleCheckMethods):
    """
    Story: Родительская категория
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

        # Переходим на главную
        #cls.go_to_main_page(cls.driver)

    @skip('deprecated')
    @priority('medium')
    @data(*HelpNavigateData.ROOT_CATEGORY_SUITE)
    def test_bestseller_block_in_category(self, test_data):
        """
        Title: Проверка спец-витрин в каждой родительской категории
        """
        service_log.run(self)
        # Переходим на страницу рутовой категории
        self.get_page(self.driver, HelpNavigateData.path_category.URL_PATH_ROOT_CATEGORY % test_data)
        time.sleep(self.time_sleep)
        list_category = self.get_category_id_from_page_source(self.driver, self.path_category.START_FIND_CATEGORY,
                                                              self.path_category.END_FIND_CATEGORY)
        list_category.pop(0)
        query = "category_id=%s and field_name='macro_type'" % test_data
        spec_markers = databases.db3.accounting.get_provided_filter_by_criteria(query)[0]
        goods_elastic = databases.db2.warehouse.get_bestsellers_category_wares(macro_type=spec_markers["value"])
        list_good_elastic = []
        #creation_time = 2422539153447
        for good_elastic in goods_elastic[u'hits'][u'hits']:
            #self.assertLess(good_elastic[u'_source'][u'creationTimestamp'], creation_time)
            list_good_elastic.append(good_elastic[u'_id'].encode('utf-8'))
            #creation_time = good_elastic[u'_source'][u'creationTimestamp'] + 1
        position = self.get_position_in_page_source(self.driver, self.path_category.HTML_CATEGORY % list_category[0])
        page_html = self.driver.page_source
        position_end_block = page_html.find(self.path_category.HTML_END_SECTION, position)
        # получаем список id товаров блока спецкатегории
        count_good = self.get_count_goods_in_page(self.driver.page_source[position:position_end_block],
                                                  self.path_category.TO_FIND_GOODS)
        list_good_id = self.get_good_id_from_page_source(self.driver, self.path_category.TO_FIND_GOODS,
                                                         good_count=self.get_count_good_in_block(count_good, 5),
                                                         cont=position)
        str_good = ''
        for good_id in list_good_id:
            str_good += "'" + good_id + "'"
            str_good += ", "
        wares_cassandra = databases.db0.warehouse.get_wares_by_ware_ids(str_good[:-2])
        self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
        for ware_cassandra in wares_cassandra:
            self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
            msg_error = "Товар не находится в статусе: Принятый товар - прошел модерацию и теперь опубликован"
            self.assertIn(str(ware_cassandra['moderation_state']), '1,2', msg_error)

    @skip('deprecated')
    @priority('medium')
    @data(*HelpNavigateData.ROOT_CATEGORY_SUITE)
    def test_special_block_in_category(self, test_data):
        """
        Title: Проверка спец-витрин в каждой родительской категории
        """
        service_log.run(self)
        # Переходим на страницу рутовой категории
        self.get_page(self.driver, HelpNavigateData.path_category.URL_PATH_ROOT_CATEGORY % test_data)
        #time.sleep(self.time_sleep)
        list_category = self.get_category_id_from_page_source(self.driver, self.path_category.START_FIND_CATEGORY,
                                                              self.path_category.END_FIND_CATEGORY)
        self.assertGreater(len(list_category), 2, "Нет спецкатегорий на странице категории")
        list_category.pop(0)
        list_category.pop(0)
        for category in list_category:
            spec_markers = databases.db3.accounting.get_provided_filter_by_id(category)[0]
            goods_elastic = databases.db2.warehouse.get_spec_category_wares(marker=spec_markers["value"])
            list_good_elastic = []
            creation_time = 2422539153447
            for good_elastic in goods_elastic[u'hits'][u'hits']:
                self.assertLess(good_elastic[u'_source'][u'creationTimestamp'], creation_time)
                list_good_elastic.append(good_elastic[u'_id'].encode('utf-8'))
                creation_time = good_elastic[u'_source'][u'creationTimestamp'] + 1

            position = self.get_position_in_page_source(self.driver, self.path_category.HTML_CATEGORY % category)
            page_html = self.driver.page_source
            position_end_block = page_html.find(self.path_category.HTML_END_SECTION, position)
            # получаем список id товаров блока спецкатегории
            count_good = self.get_count_goods_in_page(self.driver.page_source[position:position_end_block],
                                                      self.path_category.TO_FIND_GOODS)
            list_good_id = self.get_good_id_from_page_source(self.driver, self.path_category.TO_FIND_GOODS,
                                                             good_count=self.get_count_good_in_block(count_good, 5),
                                                             cont=position)
            str_good = ''
            for good_id in list_good_id:
                str_good += "'" + good_id + "'"
                str_good += ", "
            wares_cassandra = databases.db0.warehouse.get_wares_by_ware_ids(str_good[:-2])
            self.assertIsNotNone(wares_cassandra, "Из базы не были получены товары")
            for ware_cassandra in wares_cassandra:
                self.assertEqual(ware_cassandra['stock_state'], 2, "Статус товара не равен 2 - активному товару")
                msg_error = "Товар не находится в статусе: Принятый товар - прошел модерацию и теперь опубликован"
                self.assertIn(str(ware_cassandra['moderation_state']), '1,2', msg_error)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()