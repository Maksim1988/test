# -*- coding: utf-8 -*-
"""
Feature: Варианты доставки
"""
import time
from support import service_log
from support.utils import common_utils
from support.utils.common_utils import generate_sha256, priority
from support.utils.db import databases
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.settings.classes.class_profile_settings import HelpProfileSettingsCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods
from unittest import skip



class OnOrOffStoreDeliveryInfo(HelpAuthCheckMethods, HelpProfileSettingsCheckMethods):
    """
    Story: Включение \ Отключение способов доставки
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        cls.delivery_db = databases.db1.accounting.get_delivery_details_by_user_id(default_user_id)
        databases.db1.accounting.update_account_details_by_criteria(default_user_id, "locale='ru'")
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"],
                                             salt=cls.user["salt"])
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)
        cls.go_to_main_page(cls.driver)
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_api=False)

        # Переход на страницу Доставка и выключение всех настроек доставки
        cls.get_page(cls.driver, cls.path_settings.URL_DELIVERY_INFO)
        delivery_info = cls.get_status_delivery_options(cls.delivery_db)
        delivery = cls.get_delivery_form(cls.driver, delivery_info)
        cls.change_all_delivery_options(cls.driver, delivery_info, drop=True)
        cls.click_button(delivery["save_btn"])
        cls.element_is_present(cls.driver, cls.check_settings.CHANGE_DELIVERY_SUCCESS)
        time.sleep(cls.time_sleep)
        #cls.get_element_navigate(cls.driver, cls.check_settings.CHANGE_DELIVERY_SUCCESS)

    @priority("High")
    def test_select_all_delivery(self):
        """
        Title: Я могу включить все доступные варианты доставки. Любой посетитель увидит их на карточке любого моего товара.
        Description:
        * проверить, сохранение изменений в ui
        * проверить сохранение данных в Бд
        * проверить отображение всех включенных вариантов доставки на карточке любого своего товара.
        """
        text_tk = "SDEK, B2C, RZD, %s" % common_utils.random_string()
        text_courier = "Moscow, %s" % common_utils.random_string()
        text_pickup = "Moscow, %s" % common_utils.random_string()
        self.get_page(self.driver, self.path_settings.URL_DELIVERY_INFO)
        delivery_db = databases.db1.accounting.get_delivery_details_by_user_id(self.user["id"])
        err_msg_1 = "У пользователя есть активные варианты доставки: %s. Метод setUp отработал некорректно"
        self.assertEqual(len(delivery_db), 0, err_msg_1 % delivery_db)
        delivery_info = self.get_status_delivery_options(delivery_db)
        time.sleep(self.time_sleep)
        delivery = self.get_delivery_form(self.driver, delivery_info)
        self.change_all_delivery_options(self.driver, delivery_info, drop=False)
        delivery["tk_input"].send_keys(text_tk)
        delivery["courier_input"].send_keys(text_courier)
        delivery["pickup_input"].send_keys(text_pickup)
        self.click_button(delivery["save_btn"])
        self.element_is_present(self.driver, self.check_settings.CHANGE_DELIVERY_SUCCESS)
        delivery_db_updated = databases.db1.accounting.get_delivery_details_by_user_id(self.user["id"])
        err_msg = "В БД добавлено только %s записей, вместо 5"
        self.assertEqual(len(delivery_db_updated), 5, err_msg % len(delivery_db_updated))
        self.driver.refresh()
        HelpProfileSettingsCheckMethods.progress(self.driver)
        delivery_info_updated = self.get_status_delivery_options(delivery_db_updated)
        time.sleep(self.time_sleep)
        self.get_delivery_form(self.driver, delivery_info_updated)
        # переход на страницу магазина и в товар
        self.get_page(self.driver, self.path_shop.URL_SHOP % self.user["id"])
        obj_good = self.get_element_navigate(self.driver, self.click_shop.GOOD % 1)
        good_name = obj_good.text.encode('utf-8')
        self.click_button(obj_good)
        self.get_element_navigate(self.driver, self.check_good.NAME_GOOD % good_name)
        # Проверка блока Варианты доставки на странице товара
        self.check_all_delivery_options_in_good(self.driver, text_tk, text_courier, text_pickup)

    @priority("Medium")
    def test_deselect_all_delivery(self):
        """
        Title: Я могу выключить все доступные варианты доставки. На карточке моего товара не будет способов доставки
        Description:
        * проверить, сохранение изменений в ui
        * проверить сохранение данных в Бд
        * проверить, что на карточке любого своего товара нет пункта с доставкой.
        """
        delivery_db = databases.db1.accounting.get_delivery_details_by_user_id(self.user["id"])
        err_msg_1 = "У пользователя есть активные варианты доставки: %s. Метод setUp отработал некорректно"
        self.assertEqual(len(delivery_db), 0, err_msg_1 % delivery_db)
        delivery_info = self.get_status_delivery_options(delivery_db)
        self.get_delivery_form(self.driver, delivery_info)
        # переход на страницу магазина и в товар
        self.get_page(self.driver, self.path_shop.URL_SHOP % self.user["id"])
        obj_good = self.get_element_navigate(self.driver, self.click_shop.GOOD % 1)
        good_name = obj_good.text.encode('utf-8')
        self.click_button(obj_good)
        self.get_element_navigate(self.driver, self.check_good.NAME_GOOD % good_name)
        # Проверка блока Варианты доставки на странице товара
        self.element_is_none(self.driver, self.check_good.BLOCK_DELIVERY_INFO)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()



class StoreDeliveryInfoForm():
    """
    Story: Форма настройки способов доставки
    """

    @skip('manual')
    @priority("Low")
    def test_store_delivery_form_view(self):
        """
        Title: Вид формы реквизиты компании
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_store_delivery_empty_transport_company(self):
        """
        Title: Я не могу включить и сохранить способ доставки "Транспортными компаниями" не заполнив поле.
        Description: Отображается сообщение "Обязательное поле"
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_store_delivery_empty_courier_in_the_city(self):
        """
        Title: Я не могу включить и сохранить способ доставки "Курьером по городу" не заполнив поле.
        Description: Отображается сообщение "Обязательное поле"
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_store_delivery_empty_pickup(self):
        """
        Title: Я не могу включить и сохранить способ доставки "Самовывоз" не заполнив поле.
        Description: Отображается сообщение "Обязательное поле"
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_store_delivery_max_transport_company(self):
        """
        Title: Поле "Транспортными компаниями" максимально принимает 200 символов
        Description: Это не точно, нужно уточнить требования
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_store_delivery_max_courier_in_the_city(self):
        """
        Title: Поле "Курьером по городу" максимально принимает 200 символов
        Description: Это не точно, нужно уточнить требования
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_store_delivery_max_pickup(self):
        """
        Title: Поле "Самовывоз" максимально принимает 200 символов
        Description: Это не точно, нужно уточнить требования
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_store_delivery_negative_transport_company(self):
        """
        Title: Я не могу включить и сохранить способ оплаты "Транспортными компаниями" если в нем 201 символ.
        Description: Отображается сообщение "Уточнить текст"
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_store_delivery_negative_courier_in_the_city(self):
        """
        Title: Я не могу включить и сохранить способ оплаты "Курьером по городу" если в нем 201 символ.
        Description: Отображается сообщение "Уточнить текст"
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_store_delivery_negative_pickup(self):
        """
        Title: Я не могу включить и сохранить способ оплаты "Самовывоз" если в нем 201 символ.
        Description: Отображается сообщение "Уточнить текст"
        """
        pass