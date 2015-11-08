# -*- coding: utf-8 -*-
"""
Feature: Варианты оплаты
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



class OnOrOffStorePaymentsInfo(HelpAuthCheckMethods, HelpProfileSettingsCheckMethods):
    """
    Story: Включение \ Отключение способов оплаты
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        cls.payment_db = databases.db1.accounting.get_payment_details_by_user_id(default_user_id)
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

        # Переход на страницу Оплата и выключение всех настроек оплаты
        cls.get_page(cls.driver, cls.path_settings.URL_PAYMENT_INFO)
        payment_info = cls.get_status_payment_options(cls.payment_db)
        payments = cls.get_payment_form(cls.driver, payment_info)
        cls.change_all_payment_options(cls.driver, payment_info, drop=True)
        cls.click_button(payments["save_btn"])
        cls.element_is_present(cls.driver, cls.check_settings.CHANGE_PAYMENTS_SUCCESS)
        #cls.get_element_navigate(cls.driver, cls.check_settings.CHANGE_PAYMENTS_SUCCESS)

    @priority("High")
    def test_select_all_payments(self):
        """
        Title: Я могу включить все доступные варианты оплаты. Любой посетитель увидит их на карточке любого моего товара.
        Description:
        * проверить, сохранение изменений в ui
        * проверить сохранение данных в Бд
        * проверить отображение всех включенных вариантов оплаты на карточке любого своего товара.
        """
        text_card = "Visa, Master Card, %s" % common_utils.random_string()
        text_e_money = "Webmoney, Bitcoint, %s" % common_utils.random_string()
        self.get_page(self.driver, self.path_settings.URL_PAYMENT_INFO)
        payment_db = databases.db1.accounting.get_payment_details_by_user_id(self.user["id"])
        err_msg_1 = "У пользователя есть активные варианты оплаты: %s. Метод setUp отработал некорректно"
        self.assertEqual(len(payment_db), 0, err_msg_1 % payment_db)
        payment_info = self.get_status_payment_options(payment_db)
        payments = self.get_payment_form(self.driver, payment_info)
        self.change_all_payment_options(self.driver, payment_info, drop=False)
        payments["card_input"].send_keys(text_card)
        payments["e_money_input"].send_keys(text_e_money)
        self.click_button(payments["save_btn"])
        self.element_is_present(self.driver, self.check_settings.CHANGE_PAYMENTS_SUCCESS)
        payment_db_updated = databases.db1.accounting.get_payment_details_by_user_id(self.user["id"])
        err_msg = "В БД добавлено только %s записей, вместо 5"
        self.assertEqual(len(payment_db_updated), 5, err_msg % len(payment_db_updated))
        self.driver.refresh()
        HelpProfileSettingsCheckMethods.progress(self.driver)
        payment_info_updated = self.get_status_payment_options(payment_db_updated)
        self.get_payment_form(self.driver, payment_info_updated)
        # переход на страницу магазина и в товар
        self.get_page(self.driver, self.path_shop.URL_SHOP % self.user["id"])
        obj_good = self.get_element_navigate(self.driver, self.click_shop.GOOD % 1)
        good_name = obj_good.text.encode('utf-8')
        self.click_button(obj_good)
        self.get_element_navigate(self.driver, self.check_good.NAME_GOOD % good_name)
        # Проверка блока Варианты оплаты на странице товара
        self.check_all_payment_options_in_good(self.driver, text_card, text_e_money)

    @priority("Medium")
    def test_deselect_all_payments(self):
        """
        Title: Я могу выключить все доступные варианты оплаты. На карточке моего товара не будет способов доставки
        Description:
        * проверить, сохранение изменений в ui
        * проверить сохранение данных в Бд
        * проверить, что на карточке любого своего товара нет пункта с доставкой.
        """
        payment_db = databases.db1.accounting.get_payment_details_by_user_id(self.user["id"])
        err_msg_1 = "У пользователя есть активные варианты оплаты: %s. Метод setUp отработал некорректно"
        self.assertEqual(len(payment_db), 0, err_msg_1 % payment_db)
        payment_info = self.get_status_payment_options(payment_db)
        time.sleep(self.time_sleep)
        self.get_payment_form(self.driver, payment_info)
        # переход на страницу магазина и в товар
        self.get_page(self.driver, self.path_shop.URL_SHOP % self.user["id"])
        obj_good = self.get_element_navigate(self.driver, self.click_shop.GOOD % 1)
        good_name = obj_good.text.encode('utf-8')
        self.click_button(obj_good)
        self.get_element_navigate(self.driver, self.check_good.NAME_GOOD % good_name)
        # Проверка блока Варианты оплаты на странице товара
        self.element_is_none(self.driver, self.check_good.BLOCK_PAYMENT_INFO)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()



class StorePaymentsInfoForm():
    """
    Story: Форма настройки способов оплаты
    """

    @skip('manual')
    @priority("Low")
    def test_store_payments_form_view(self):
        """
        Title: Вид формы реквизиты компании
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_store_payments_empty_transfer_on_bank_card(self):
        """
        Title: Я не могу включить и сохранить способ оплаты "Перевод на карту банка" не заполнив поле.
        Description: Отображается сообщение "Обязательное поле"
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_store_payments_empty_bank_card_or_emoney(self):
        """
        Title: Я не могу включить  и сохранить способ оплаты "Картой или электронными деньгами" не заполнив поле.
        Description: Отображается сообщение "Обязательное поле"
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_store_payments_max_transfer_on_bank_card(self):
        """
        Title: Поле "Перевод на карту банка" максимально принимает 200 символов
        Description: Это не точно, нужно уточнить требования
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_store_payments_max_bank_card_or_emoney(self):
        """
        Title: Поле "Картой или электронными деньгами" максимально принимает 200 символов
        Description: Это не точно, нужно уточнить требования
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_store_payments_negative_transfer_on_bank_card(self):
        """
        Title: Я не могу включить и сохранить способ оплаты "Перевод на карту банка" если в нем 201 символ.
        Description: Отображается сообщение "Уточнить текст"
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_store_payments_negative_bank_card_or_emoney(self):
        """
        Title: Я не могу включить и сохранить способ оплаты "Картой или электронными деньгами" если в нем 201 символ.
        Description: Отображается сообщение "Уточнить текст"
        """
        pass
