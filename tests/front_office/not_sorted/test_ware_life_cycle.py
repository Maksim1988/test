# -*- coding: utf-8 -*-
"""
Feature: Жизненный цикл товара
Description: Проверка жизненного цикла товара (вариации)
"""
from unittest import skip
from selenium.common.exceptions import NoSuchElementException
from support import service_log
from support.utils.common_utils import generate_sha256, priority
from support.utils.db import databases
from support.utils.thrift4req import services
from tests.front_office.authorization.classes.class_front import HelpAuthMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods, HelpNavigateData
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.worker_warehouse.class_warehouse import WarehouseCheckMethods

__author__ = 's.trubachev'


class TestLifeCycleGood(HelpNavigateCheckMethods, HelpAuthMethods, WarehouseCheckMethods, HelpLifeCycleCheckMethods,
                        AccountingMethods):
    """
    Story: Жизненный цикл товара
    """
    driver = None

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()

        # Подготовка данных о товаре
        cls.ware = cls.get_random_ware(databases.db0.warehouse.get_wares_with_limit(100))
        cls.moderator_id = int(cls.get_default_user_id('moderator'))
        cls.save_ware_data(cls.ware)

        # Берём пользователя товара и сохраняем его пароль
        cls.user_seller = databases.db1.accounting.get_data_user_by_id(cls.ware['shop_id'])[0]
        cls.save_user_password(user_id=cls.user_seller["id"], hash_passwd=cls.user_seller["code_value"])

        # Устанавливаем новый пароль для пользователя
        cls.default_new_passwd = cls.get_default_password()
        hash_res_new = generate_sha256(cls.default_new_passwd, cls.user_seller["salt"])
        databases.db1.accounting.update_user_password(cls.user_seller["id"], hash_res_new)
        service_log.preparing_env(cls)

    def authorization(self, user, passwd):
        """ Авторизуемся.
        :param user: данные пользователя
        :param passwd: пароль пользователя
        """
        # Переходим на страницу авторизации
        self.get_auth_page(self.driver)
        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        # Вводим данные на авторизацию
        self.send_phone(phone_object=obj_phone, phone_number=user["phone"][1:])
        self.send_password(password_object=obj_password, password_number=passwd)
        # Нажатие на кнопку авторизации
        self.submit_button(obj_submit_button)

    def check_product_page(self, content_ware):
        """ Краткая проверка страницы товара.
        Название товара, количество и цена за штуку.
        :param content_ware: контент товара
        """
        title_ware = self.get_name(self.get_element(self.driver, self.check_good.TITLE_GOOD))

        # Метод определяет значение для поиска, если количество не указано
        none_value = lambda n, v:  n % "---" if v is None else n % v['min_stock'].value

        count = none_value(self.check_good.COUNT_GOODS, content_ware.integerFields)
        price = none_value(self.check_good.PRICE_PER_PIECE, content_ware.integerRangeFields)

        self.assertEqual(title_ware, content_ware.textFields['title'].value, "Incorrect name of the product.")
        self.assertTrue(self.get_element(self.driver, count), "Incorrect the price of the goods")
        self.assertTrue(self.get_element(self.driver, price), "Incorrect the price of the goods")

    def check_not_found(self, func, *args, **kwargs):
        """ Перехватываем исключение, если элемент не найден и говорим, что так и должно быть.
        :param func: результат поиска элемента
        :return: True
        """
        try:
            func(*args, **kwargs)
            msg = "Find element!"
            service_log.error(msg)
            raise AssertionError("Error: %s" % msg)
        except NoSuchElementException, tx:
            service_log.put("Success! Element not found.")
            return True

    def check_bestsellers_page(self, content_ware):
        """ Проверяем, что элемент найден.
        Ищем только название товара.
        :param content_ware: контент товара
        :return: True
        """
        service_log.put("Try to found ware in all bestsellers.")
        ware_bestsellers = self.check_catalog.PATH_WARE_IN_PAGE % content_ware.textFields['title'].value
        self.assertTrue(self.get_element(self.driver, ware_bestsellers), "Not found ware name in bestsellers.")
        service_log.put("Find ware in all bestsellers.")
        return True

    def check_ware_from_my_goods(self, content_ware):
        """ Проверяем, что товар есть в магазине продавца.
        :param content_ware: контент товара
        :return: True
        """
        ware_name = self.check_my_goods.WARE_NAME % content_ware.textFields['title'].value
        self.assertTrue(self.get_element(self.driver, ware_name), "Not found ware name in my goods.")
        service_log.put("Find ware in all bestsellers.")
        return True

    def check_favorite_ware_page(self, content_ware):
        """Проверяем страницу "Избранное", товары.
        :param content_ware: контент товара
        :return: True
        """
        ware_favorite = self.check_favorite.WARE_NAME_FAVORITE % content_ware.textFields['title'].value

        self.assertTrue(self.get_element(self.driver, ware_favorite), "Not found ware name in favorite page.")
        service_log.put("Find ware in favorite page.")
        return True

    def check_page_search(self, ware_data):
        """ Проверка поиска через главную страницу.
        Переходим на Главную и вбиваем поиск искомы товар.
        Проверяем, что товар нашелся. Проверяем соответствие его url.
        :return:
        """
        ware_id = ware_data.wareId
        ware_name = ware_data.content.textFields['title'].value
        ware_url = HelpNavigateData.ENV_BASE_URL + HelpNavigateData.path_my_goods.URL_GOODS % ware_id
        ware_info = ware_name

        # Получаем инпут поиска и кнопку поиска
        input_search = self.get_element(self.driver, self.input_main.SEARCH)
        btn_search = self.get_element(self.driver, self.click_main.BTN_SEARCH)
        # Вводим название товара и жмем кнопку поиска
        input_search.send_keys(ware_name.decode('utf-8'))
        btn_search.click()
        # Проверяем, что перешли в результаты поиска
        self.get_element(self.driver, self.check_search.TITLE_SEARCH)
        # Ищем на странице товар, заданный в поиске и переходим на страницу товара, проверяем урл страницы и название
        good_in_search = self.get_element(self.driver, self.click_search.LNK_GOOD_WITH_HREF % (ware_id, ware_info))
        good_in_search.click()
        self.assertEqual(self.driver.current_url, ware_url)
        self.assertEqual(self.get_name(self.get_element_navigate(self.driver, self.check_good.TITLE_GOOD)), ware_name)

    def check_new_ware_all_page(self, content_ware):
        """ Проверяем, что новый товар появился на странице "Новинки".
        :param content_ware: контент товара
        :return: True
        """
        ware_favorite = self.check_catalog.PATH_WARE_IN_PAGE % content_ware.textFields['title'].value
        self.assertTrue(self.get_element(self.driver, ware_favorite), "Not found ware name in New_ware page.")
        service_log.put("Find ware in New_ware page.")
        return True

    def check_last_deal_page(self, content_ware):
        """ Проверяем, что новый товар появился на странице "Последнии сделки".
        :param content_ware: контент товара
        :return: True
        """
        ware_last_deal = self.check_catalog.PATH_WARE_IN_PAGE % content_ware.textFields['title'].value
        self.assertTrue(self.get_element(self.driver, ware_last_deal), "Not found ware name in Last_deals page.")
        service_log.put("Find ware in Last_deals page.")
        return True

    def check_goods_from_best_sellers_page(self, content_ware):
        """ Проверяем, что новый товар появился на странице "Товары от лучших продавцов".
        :param content_ware: контент товара
        :return: True
        """
        ware_last_deal = self.check_catalog.PATH_WARE_IN_PAGE % content_ware.textFields['title'].value
        self.assertTrue(self.get_element(self.driver, ware_last_deal), "Not found ware in best_sellers page.")
        service_log.put("Find ware in best_sellers page.")
        return True

    def check_ware_in_all(self, data_ware):
        """ Проверяем, что товар появился на странице "Все товары".
        :param data_ware: данные товара
        :return: True
        """
        service_log.put("Try to found ware in all wares.")
        ware_in_all = self.check_catalog.WARE_ID_ALL_CATALOG % data_ware.wareId
        self.assertTrue(self.get_element(self.driver, ware_in_all), "Not found ware in catalog all wares.")
        service_log.put("Find ware in catalog all wares.")
        return True

    @skip('update')
    @priority("medium")
    def test_ware_believed(self):
        """
        Title: Жизненный цикл товара.
        Description: Товар на протяжениие теста может находиться в следующих состояниях:
         -> Доверенный.
        Для каждого состояния проверяется наличие или отсутствие товара на следующих страницах:
        А) Карточка товара.
        Б) Каталог:
            1) страница "Все товары"!
            2) страница "Бестселлеры"!
            3) страница "Новинки" (auto)!
            4) страница "Последние сделки"  (auto)
            #4) блок "Спецраздел"
            #5) Типовая страница подкатегории
        В) Главная:
            1) блок "Новинки"
            2) блок "Последние сделки"  и
            3) блок и страница "Товары от лучших продавцов"
        Г) Магазин продавца
        Д) Результаты поиска
        Е) Избранное
        WARNING: на данный момент по умолчанию товар явл. Двоверенным, это должно измениться.
        """
        # авторизуемся
        self.authorization(self.user_seller, self.default_new_passwd)

        # создаём товар, статус товара BELIEVED (по умолчанию - Доверенный)
        ware_req = self.duplicate_ware_req(self.ware['shop_id'], self.ware['managed_category'], self.ware["content"])
        wh_ware_st1_0 = services.warehouse.root.tframed.createWare(ware_req)

        # выставляем состояние StockState Опубликованный товар. Доступен всем. Индексируется. PUBLISHED = 2
        stock_state = self.get_StockState('PUBLISHED')
        wh_ware_st1_0 = services.warehouse.root.tframed.makePublication(wh_ware_st1_0.wareId, stock_state)

        service_log.put("Created ware: %s" % wh_ware_st1_0)
        self.assertEqual(wh_ware_st1_0.moderationState, 1, "Moderation-state ware not BELIEVED.")

        # -- Обход страниц --

        # Карточка товара
        self.get_page(self.driver, HelpNavigateData.path_my_goods.URL_GOODS % wh_ware_st1_0.wareId)
        self.check_product_page(wh_ware_st1_0.content)

        # Все товары
        self.get_page(self.driver, self.path_category.URL_ALL_CATALOG)
        self.check_not_found(self.check_ware_in_all, wh_ware_st1_0)  # TODO: должен находить?!

        # Бестселлеры
        self.get_page(self.driver, self.path_category.URL_ALL_BESTSELLERS)
        self.check_not_found(self.check_bestsellers_page, wh_ware_st1_0.content)

        # Магазин продавца
        self.get_my_goods_page(self.driver)
        self.check_ware_from_my_goods(wh_ware_st1_0.content)

        # Избранное
        self.get_page(self.driver, self.path_favorites.URL_FAVORITES_GOODS)
        self.check_not_found(self.check_favorite_ware_page, wh_ware_st1_0.content)

        # Новые товары
        self.get_page(self.driver, self.path_category.URL_ALL_WARE_NEW)
        self.check_not_found(self.check_new_ware_all_page, wh_ware_st1_0.content)

        # Последние сделки
        self.get_page(self.driver, self.path_category.URL_ALL_LAST_DEALS)
        self.check_not_found(self.check_last_deal_page, wh_ware_st1_0.content)

        # Товары от лучших продавцов
        self.get_page(self.driver, self.path_category.URL_GOODS_FROM_BEST_SELLERS)
        self.check_not_found(self.check_goods_from_best_sellers_page, wh_ware_st1_0.content)

        # Проверяем результаты поиска
        self.go_to_main_page(self.driver)  # Переходим на главную (если мы на другой странице)
        self.check_page_search(wh_ware_st1_0)

        # -- Блоки на "Главной" --
        #self.go_to_main_page(self.driver)
        # TODO: дописать

    @skip('update')
    @priority("medium")
    def test_ware_accepted(self):
        """
        Title: Жизненный цикл товара.
        Description: Товар на протяжениие теста может находиться в следующих состояниях:
        Доверенный -> Утверждённый.
        Для каждого состояния проверяется наличие или отсутствие товара на следующих страницах:
        А) Карточка товара.
        Б) Каталог:
            1) страница "Все товары"!
            2) страница "Бестселлеры"!
            3) страница "Новинки"
            4) страница "Последние сделки"
            #4) блок "Спецраздел"
            #5) Типовая страница подкатегории
        В) Главная:
            1) блок "Новинки"
            2) блок "Последние сделки"  и
            3) блок и страница "Товары от лучших продавцов"
        Г) Магазин продавца
        Д) Результаты поиска
        Е) Избранное
        WARNING: на данный момент по умолчанию товар явл. Двоверенным, это должно измениться.
        """
        # авторизуемся
        self.authorization(self.user_seller, self.default_new_passwd)

        # создаём товар, статус товара BELIEVED (по умолчанию - Доверенный)
        ware_req = self.duplicate_ware_req(self.ware['shop_id'], self.ware['managed_category'], self.ware["content"])
        wh_ware_st1_0 = services.warehouse.root.tframed.createWare(ware_req)

        # выставляем состояние StockState Опубликованный товар. Доступен всем. Индексируется. PUBLISHED = 2
        stock_state = self.get_StockState('PUBLISHED')
        wh_ware_st1_0 = services.warehouse.root.tframed.makePublication(wh_ware_st1_0.wareId, stock_state)
        service_log.put("Created ware: %s" % wh_ware_st1_0)
        self.assertEqual(wh_ware_st1_0.moderationState, 1, "Moderation-state ware not BELIEVED.")
        # Меняем статус на ACCEPTED
        wh_ware_st2_1 = services.warehouse.root.tframed.makeModeration(wh_ware_st1_0.wareId, True, self.moderator_id)
        self.assertEqual(wh_ware_st2_1.moderationState, 2, "Moderation-state ware not ACCEPTED.")

        # -- Обход страниц --

        # Карточка товара
        self.get_page(self.driver, HelpNavigateData.path_my_goods.URL_GOODS % wh_ware_st1_0.wareId)
        self.check_product_page(wh_ware_st1_0.content)

        # Все товары
        self.get_page(self.driver, self.path_category.URL_ALL_CATALOG)
        self.check_not_found(self.check_ware_in_all, wh_ware_st1_0)  # TODO: должен находить?!

        # Бестселлеры
        self.get_page(self.driver, self.path_category.URL_ALL_BESTSELLERS)
        self.check_not_found(self.check_bestsellers_page, wh_ware_st1_0.content)

        # Магазин продавца
        self.get_my_goods_page(self.driver)
        self.check_ware_from_my_goods(wh_ware_st1_0.content)

        # Избранное
        self.get_page(self.driver, self.path_favorites.URL_FAVORITES_GOODS)
        self.check_not_found(self.check_favorite_ware_page, wh_ware_st1_0.content)

        # Новые товары
        self.get_page(self.driver, self.path_category.URL_ALL_WARE_NEW)
        self.check_new_ware_all_page(wh_ware_st1_0.content)

        # Последние сделки
        self.get_page(self.driver, self.path_category.URL_ALL_LAST_DEALS)
        self.check_not_found(self.check_last_deal_page, wh_ware_st1_0.content)

        # Товары от лучших продавцов
        self.get_page(self.driver, self.path_category.URL_GOODS_FROM_BEST_SELLERS)
        self.check_not_found(self.check_goods_from_best_sellers_page, wh_ware_st1_0.content)

        # Проверяем результаты поиска
        self.go_to_main_page(self.driver)  # Переходим на главную (если мы на другой странице)
        self.check_page_search(wh_ware_st1_0)

        # -- Блоки на "Главной" --
        #self.go_to_main_page(self.driver)
        # TODO: дописать

    @skip('update')
    @priority("medium")
    def test_ware_banned(self):
        """
        Title: Жизненный цикл товара.
        Description: Товар на протяжениие теста может находиться в следующих состояниях:
        Доверенный -> Утверждённый -> Забаненный.
        Для каждого состояния проверяется наличие или отсутствие товара на следующих страницах:
        А) Карточка товара.
        Б) Каталог:
            1) страница "Все товары"!
            2) страница "Бестселлеры"!
            3) страница "Новинки"
            4) страница "Последние сделки"
            #4) блок "Спецраздел"
            #5) Типовая страница подкатегории
        В) Главная:
            1) блок "Новинки"
            2) блок "Последние сделки"  и
            3) блок и страница "Товары от лучших продавцов"
        Г) Магазин продавца
        Д) Результаты поиска
        Е) Избранное
        WARNING: на данный момент по умолчанию товар явл. Двоверенным, это должно измениться.
        """
        # авторизуемся
        self.authorization(self.user_seller, self.default_new_passwd)

        # создаём товар, статус товара BELIEVED (по умолчанию - Доверенный)
        ware_req = self.duplicate_ware_req(self.ware['shop_id'], self.ware['managed_category'], self.ware["content"])
        wh_ware_st1_0 = services.warehouse.root.tframed.createWare(ware_req)

        # выставляем состояние StockState Опубликованный товар. Доступен всем. Индексируется. PUBLISHED = 2
        stock_state = self.get_StockState('PUBLISHED')
        wh_ware_st1_0 = services.warehouse.root.tframed.makePublication(wh_ware_st1_0.wareId, stock_state)
        service_log.put("Created ware: %s" % wh_ware_st1_0)
        self.assertEqual(wh_ware_st1_0.moderationState, 1, "Moderation-state ware not BELIEVED.")
        # Меняем статус на ACCEPTED
        wh_ware_st2_1 = services.warehouse.root.tframed.makeModeration(wh_ware_st1_0.wareId, True, self.moderator_id)
        self.assertEqual(wh_ware_st2_1.moderationState, 2, "Moderation-state ware not ACCEPTED.")

        # Меняем статус на BANNED
        wh_ware_st4_2 = services.warehouse.root.tframed.makeModeration(wh_ware_st1_0.wareId, False, self.moderator_id)
        self.assertEqual(wh_ware_st4_2.moderationState, 4, "Moderation-state ware not BANNED.")

        # -- Обход страниц --

        # Карточка товара
        self.get_page(self.driver, HelpNavigateData.path_my_goods.URL_GOODS % wh_ware_st1_0.wareId)
        self.check_product_page(wh_ware_st1_0.content)

        # Все товары
        self.get_page(self.driver, self.path_category.URL_ALL_CATALOG)
        self.check_not_found(self.check_ware_in_all, wh_ware_st1_0)  # TODO: должен находить?!

        # Бестселлеры
        self.get_page(self.driver, self.path_category.URL_ALL_BESTSELLERS)
        self.check_not_found(self.check_bestsellers_page, wh_ware_st1_0.content)

        # Магазин продавца
        self.get_my_goods_page(self.driver)
        self.check_not_found(self.check_ware_from_my_goods, wh_ware_st1_0.content)

        # Избранное
        self.get_page(self.driver, self.path_favorites.URL_FAVORITES_GOODS)
        self.check_not_found(self.check_favorite_ware_page, wh_ware_st1_0.content)

        # Новые товары
        self.get_page(self.driver, self.path_category.URL_ALL_WARE_NEW)
        self.check_not_found(self.check_new_ware_all_page, wh_ware_st1_0.content)

        # Последние сделки
        self.get_page(self.driver, self.path_category.URL_ALL_LAST_DEALS)
        self.check_not_found(self.check_last_deal_page, wh_ware_st1_0.content)

        # Товары от лучших продавцов
        self.get_page(self.driver, self.path_category.URL_GOODS_FROM_BEST_SELLERS)
        self.check_not_found(self.check_goods_from_best_sellers_page, wh_ware_st1_0.content)

        # Проверяем результаты поиска
        self.go_to_main_page(self.driver)  # Переходим на главную (если мы на другой странице)
        self.check_not_found(self.check_page_search, wh_ware_st1_0)

        # -- Блоки на "Главной" --
        #self.go_to_main_page(self.driver)
        # TODO: дописать

    @skip('update')
    @priority("medium")
    def test_ware_banned_accepted(self):
        """
        Title: Жизненный цикл товара.
        Description: Товар на протяжениие теста может находиться в следующих состояниях:
        Доверенный -> Утверждённый -> Забаненный -> Утверждённый.
        Для каждого состояния проверяется наличие или отсутствие товара на следующих страницах:
        А) Карточка товара.
        Б) Каталог:
            1) страница "Все товары"!
            2) страница "Бестселлеры"!
            3) страница "Новинки"
            4) страница "Последние сделки"
            #4) блок "Спецраздел"
            #5) Типовая страница подкатегории
        В) Главная:
            1) блок "Новинки"
            2) блок "Последние сделки"  и
            3) блок и страница "Товары от лучших продавцов"
        Г) Магазин продавца
        Д) Результаты поиска
        Е) Избранное
        WARNING: на данный момент по умолчанию товар явл. Двоверенным, это должно измениться.
        """
        # авторизуемся
        self.authorization(self.user_seller, self.default_new_passwd)

        # создаём товар, статус товара BELIEVED (по умолчанию - Доверенный)
        ware_req = self.duplicate_ware_req(self.ware['shop_id'], self.ware['managed_category'], self.ware["content"])
        wh_ware_st1_0 = services.warehouse.root.tframed.createWare(ware_req)

        # выставляем состояние StockState Опубликованный товар. Доступен всем. Индексируется. PUBLISHED = 2
        stock_state = self.get_StockState('PUBLISHED')
        wh_ware_st1_0 = services.warehouse.root.tframed.makePublication(wh_ware_st1_0.wareId, stock_state)
        service_log.put("Created ware: %s" % wh_ware_st1_0)
        self.assertEqual(wh_ware_st1_0.moderationState, 1, "Moderation-state ware not BELIEVED.")
        # Меняем статус на ACCEPTED
        wh_ware_st2_1 = services.warehouse.root.tframed.makeModeration(wh_ware_st1_0.wareId, True, self.moderator_id)
        self.assertEqual(wh_ware_st2_1.moderationState, 2, "Moderation-state ware not ACCEPTED.")
        # Меняем статус на BANNED
        wh_ware_st4_2 = services.warehouse.root.tframed.makeModeration(wh_ware_st1_0.wareId, False, self.moderator_id)
        self.assertEqual(wh_ware_st4_2.moderationState, 4, "Moderation-state ware not BANNED.")
        # Меняем статус на ACCEPTED
        wh_ware_st2_3 = services.warehouse.root.tframed.makeModeration(wh_ware_st1_0.wareId, True, self.moderator_id)
        self.assertEqual(wh_ware_st2_3.moderationState, 2, "Moderation-state ware not ACCEPTED.")

        # -- Обход страниц --

        # Карточка товара
        self.get_page(self.driver, HelpNavigateData.path_my_goods.URL_GOODS % wh_ware_st1_0.wareId)
        self.check_product_page(wh_ware_st1_0.content)

        # Все товары
        self.get_page(self.driver, self.path_category.URL_ALL_CATALOG)
        self.check_not_found(self.check_ware_in_all, wh_ware_st1_0)  # TODO: должен находить?!

        # Бестселлеры
        self.get_page(self.driver, self.path_category.URL_ALL_BESTSELLERS)
        self.check_not_found(self.check_bestsellers_page, wh_ware_st1_0.content)

        # Магазин продавца
        self.get_my_goods_page(self.driver)
        self.check_ware_from_my_goods(wh_ware_st1_0.content)

        # Избранное
        self.get_page(self.driver, self.path_favorites.URL_FAVORITES_GOODS)
        self.check_not_found(self.check_favorite_ware_page, wh_ware_st1_0.content)

        # Новые товары
        self.get_page(self.driver, self.path_category.URL_ALL_WARE_NEW)
        self.check_new_ware_all_page(wh_ware_st1_0.content)

        # Последние сделки
        self.get_page(self.driver, self.path_category.URL_ALL_LAST_DEALS)
        self.check_not_found(self.check_last_deal_page, wh_ware_st1_0.content)

        # Товары от лучших продавцов
        self.get_page(self.driver, self.path_category.URL_GOODS_FROM_BEST_SELLERS)
        self.check_not_found(self.check_goods_from_best_sellers_page, wh_ware_st1_0.content)

        # Проверяем результаты поиска
        self.go_to_main_page(self.driver)  # Переходим на главную (если мы на другой странице)
        self.check_page_search(wh_ware_st1_0)

        # -- Блоки на "Главной" --
        #self.go_to_main_page(self.driver)
        # TODO: дописать

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        cls.recover_ware_data(databases.db0)
        cls.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()
