# -*- coding: utf-8 -*-
"""
Feature: Избранные товары
"""

import random
import time
from unittest import skip
from support import service_log
from support.utils.common_utils import generate_sha256, priority
from support.utils.db import databases
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateData
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods



class TestFavoriteGood(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Добавить/удалить товар в избранное
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

    @priority("High")
    def test_add_good_to_favorite_remove(self, test_data=HelpNavigateData.CATALOG_TO_GOOD):
        """
        Title: Я могу добавить товар в избранное
        """
        service_log.run(self)

        # Берем тестового продавца на магазине которого будут проводиться проверки
        self.default_test_seller_id = AccountingMethods.get_default_user_id(role='buyer')
        self.user = databases.db1.accounting.get_user_by_account_id(self.default_test_seller_id)[0]
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_auth=True)

        number_good = random.randrange(1, 5, 1)
        # Переходим на все товары рандомной рутовой категории
        self.get_page(self.driver, self.path_category.URL_ALL_IN_CATEGORY % random.choice(self.ROOT_CATEGORY_SUITE))
        # Выбираем товар и сохраняем его имя
        service_log.put("Выбираем товар и сохраняем его имя")
        good_name = self.get_name(self.get_element_navigate(self.driver, test_data["start_xpath_good"] % number_good))
        # Переход на страницу товара
        service_log.put("Переход на страницу товара")
        self.check_navigate_in_good_page(self.driver, test_data, number_good)
        url_good = self.driver.current_url.encode('utf-8')
        good_id = url_good[url_good.rfind('/')+1:]
        # Жмем кнопку добавить в избранное
        service_log.put("Жмем кнопку добавить в избранное")
        btn_add_to_favorite = self.element_is_present(self.driver, self.click_good.ADD_FAVORITE, wait=10)
        btn_add_to_favorite.click()
        # Проверяем, что кнопка изменилась на удалить из избранного  остается такой же после обновления страницы
        service_log.put("Проверяем, что кнопка изменилась на удалить из избранного")
        self.get_element_navigate(self.driver, self.click_good.DEL_FAVORITE)
        self.driver.refresh()
        HelpNavigateCheckMethods.progress(self.driver)
        self.get_element_navigate(self.driver, self.click_good.DEL_FAVORITE)
        # Переходим в избранные товары
        service_log.put("Переходим в избранные товары")
        self.get_page(self.driver, self.path_favorites.URL_FAVORITES_GOODS)
        # Проверяем наличие товара в избранном и переходим на страницу товара
        service_log.put("Проверяем наличие товара в избранном и переходим на страницу товара")
        good_name_lnk = self.get_element_navigate(self.driver, self.click_favorite.GOOD_NAME_BY_ID % good_id)
        good_name_lnk.click()
        # Удаляем из избранного
        service_log.put("Удаляем из избранного")
        del_favorite = self.get_element_navigate(self.driver, self.click_good.DEL_FAVORITE)
        del_favorite.click()
        # Проверяем, что кнопка изменилась на добавить в избранное
        service_log.put("Проверяем, что кнопка изменилась на добавить в избранное")
        self.get_element_navigate(self.driver, self.click_good.ADD_FAVORITE)
        # Переходим в избранные товары
        service_log.put("Переходим в избранные товары")
        self.get_page(self.driver, self.path_favorites.URL_FAVORITES_GOODS)
        test_good = dict(xpath=(self.click_favorite.GOOD_NAME_BY_ID_AND_TITLE % (good_name, good_id)),
                         err_msg="Товар остался в списке избранного после удаления")
        # Проверяем, что в избранном нет этого товара
        self.check_no_such_element(self.driver, test_good)

    @priority("medium")
    def test_add_good_in_deal_to_favorite_remove(self, test_data=HelpNavigateData.CATALOG_TO_GOOD, sleep=2):
        """
        Title: Добавить товар в избранное \ Удалить товар из избранного
        """
        service_log.run(self)

        # Берем тестового продавца на магазине которого будут проводиться проверки
        self.default_test_seller_id = AccountingMethods.get_default_user_id(role='buyer')
        self.user = databases.db1.accounting.get_user_by_account_id(self.default_test_seller_id)[0]
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_auth=True)

        number_good = random.randrange(1, 10, 1)
        #test_data["start_xpath_good"] = self.click_catalog.GOOD_LNK

        # Переходим на все товары рандомной рутовой категории
        self.get_page(self.driver, self.path_category.URL_ALL_IN_CATEGORY % random.choice(self.ROOT_CATEGORY_SUITE))
        # Выбираем товар и сохраняем его имя
        service_log.put("Выбираем товар и сохраняем его имя")
        good_name = self.get_name(self.get_element_navigate(self.driver, test_data["start_xpath_good"] % number_good))
        # Переход на страницу товара
        service_log.put("Переход на страницу товара")
        self.check_navigate_in_good_page(self.driver, test_data, number_good)
        url_good = self.driver.current_url.encode('utf-8')
        good_id = url_good[url_good.rfind('/')+1:]
        # Жмем кнопку запросить цену по товару - товар в сделке, обновляем страницу
        service_log.put("Жмем кнопку запросить цену по товару - товар в сделке, обновляем страницу")
        btn_call_seller = self.get_element_navigate(self.driver, self.click_good.BTN_CALL_SELLER)
        self.click_button(btn_call_seller)
        input_msg = self.element_is_present(self.driver, self.input_good.POPUP_INPUT_MSG)
        input_msg.send_keys(str(time.time()))
        btn_send = self.get_element_navigate(self.driver, self.click_good.BTN_SEND)
        self.click_button(btn_send)
        btn_to_good = self.get_element_navigate(self.driver, self.click_good.BTN_TO_CARD_GOOD)
        self.click_button(btn_to_good)
        # Жмем кнопку добавить в избранное
        service_log.put("Жмем кнопку добавить в избранное")
        btn_add_to_favorite = self.get_element_navigate(self.driver, self.click_good.ADD_FAVORITE)
        btn_add_to_favorite.click()
        # Проверяем, что кнопка изменилась на удалить из избранного  остается такой же после обновления страницы
        service_log.put("Проверяем, что кнопка изменилась на удалить из избранного")
        self.get_element_navigate(self.driver, self.click_good.DEL_FAVORITE)
        self.driver.refresh()
        HelpNavigateCheckMethods.progress(self.driver)
        self.get_element_navigate(self.driver, self.click_good.DEL_FAVORITE)
        # Переходим в избранные товары
        service_log.put("Переходим в избранные товары")
        self.get_page(self.driver, self.path_favorites.URL_FAVORITES_GOODS)
        # Проверяем наличие товара в избранном
        service_log.put("Проверяем наличие товара в избранном")
        self.get_element_navigate(self.driver, self.click_favorite.GOOD_NAME_BY_ID_AND_TITLE % (good_name, good_id))
        # Удаляем из избранного
        service_log.put("Удаляем из избранного")
        del_favorite = self.get_element_navigate(self.driver, self.click_favorite.DEL_FAVORITE % (good_name, good_id))
        del_favorite.click()
        time.sleep(sleep)
        # Проверяем, что нет на странице избранного
        test_good = dict(xpath=(self.click_favorite.GOOD_NAME_BY_ID_AND_TITLE % (good_id, good_name)),
                         err_msg="Товар остался в списке избранного после удаления")
        self.check_no_such_element(self.driver, test_good)
        # Переходим на страницу товара и проверяем, что кнопка добавить в избранное
        service_log.put("Get page: %s" % url_good)
        do_get_work = time.time()
        self.driver.get(url_good)
        work_get_time = HelpNavigateCheckMethods.work_time(do_get_work)
        service_log.put("Onload event time: [%s]" % work_get_time)
        HelpNavigateCheckMethods.progress(self.driver)
        work_load_time = HelpNavigateCheckMethods.work_time(do_get_work)
        service_log.put("Page received: %s" % url_good)
        service_log.put("Page received time: %s" % work_load_time)
        self.get_element_navigate(self.driver, self.click_good.ADD_FAVORITE)

    @priority("Medium")
    def test_add_to_favorite_visitor(self, number_good=1, test_data=HelpNavigateData.CATALOG_TO_GOOD):
        """
        Title: Я как Гость, при добавлении товара в избранное вижу страницу регистрации
        """
        service_log.run(self)
        self.go_to_main_page(self.driver)
        # Переходим на все товары рандомной рутовой категории
        self.get_page(self.driver, self.path_category.URL_ALL_IN_CATEGORY % random.choice(self.ROOT_CATEGORY_SUITE))
        # Выбираем товар и сохраняем его имя
        service_log.put("Выбираем товар и сохраняем его имя")
        good_name = self.get_name(self.get_element_navigate(self.driver, test_data["start_xpath_good"] % number_good))
        # Переход на страницу товара
        service_log.put("Переход на страницу товара")
        self.check_navigate_in_good_page(self.driver, test_data, number_good)
        # Жмем кнопку добавить в избранное
        service_log.put("Жмем кнопку добавить в избранное")
        btn_add_to_favorite = self.get_element_navigate(self.driver, self.click_good.ADD_FAVORITE)
        btn_add_to_favorite.click()
        self.element_is_present(self.driver, self.check_good.POPUP_REGISTRATION)

    @priority("Medium")
    def test_add_to_favorites_your_good(self, number_good=1, test_data=HelpNavigateData.SHP_TO_GOOD):
        """
        Title: Я не могу добавить свой товар в избранное, кнопка залочена
        """
        service_log.run(self)
        # Берем тестового продавца на магазине которого будут проводиться проверки
        self.default_test_seller_id = AccountingMethods.get_default_user_id(role='seller')
        self.user = databases.db1.accounting.get_user_by_account_id(self.default_test_seller_id)[0]
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_auth=True)

        self.get_page(self.driver, self.path_shop.URL_SHOP % self.default_test_seller_id)
        # Переход на страницу товара
        service_log.put("Переход на страницу товара")
        self.check_navigate_in_good_page(self.driver, test_data, number_good)
        # Проверяем кнопку добавить в избранное - заблокированна
        service_log.put("Проверяем кнопки добавить в избранное - нет")
        self.element_is_none(self.driver, self.click_good.ADD_FAVORITE)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()



class FavoriteGoodListing():
    """
    Story: Листинг Избранных товаров
    """

    @skip('manual')
    @priority("Low")
    def test_favorite_listing_view(self):
        """
        Title: Внешний вид страницы Избранные товары
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_favorite_listing_store_card(self):
        """
        Title: Отображается карточка магазина со способами доставки и оплаты
        Description:
        * Если какого-либо атрибута нет то отображается прочерк
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_favorite_listing_goods_card(self):
        """
        Title: Отображается карточка товара со следующими атрибутами: название, цвет, материал, размеры
        Description:
        * Если какого-либо атрибута нет то отображается прочерк
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_empty_favorite_listing(self):
        """
        Title: Внешний вид страницы Избранные товары - Нет избранных товаров
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_hide_or_show_favorite_good_this_seller(self):
        """
        Title: Скрыть \ Показать избранные товары продавца
        Description:
        * Скрыть товары, скрывает избранные товары под магазином продавца
        * Показать товары, раскрывает избранные товары конкретного продавца
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_favorite_listing_contact_to_seller_link(self):
        """
        Title: Кнопка "Связаться с продавцом" ведет на страницу чата с данным продавцом
        """
        pass