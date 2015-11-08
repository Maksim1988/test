# -*- coding: utf-8 -*-
"""
Feature: Настройки магазина
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



class FillOrEditStoreDescription(HelpAuthCheckMethods, HelpProfileSettingsCheckMethods):
    """
    Story: Заполнить \ Редактировать описание магазина
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        databases.db1.accounting.update_account_details_by_criteria(default_user_id, "locale='ru'")
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"],
                                             salt=cls.user["salt"])

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

    @priority("Medium")
    def test_fill_store_description(self):
        """
        Title: Я могу заполнить описание свеого магазина и сохранить изменения. Новый пользователь.
        Description:
        Если у меня не заполнены данные о магазине, Я могу заполнить их на страниц и сохранить.
        Любой пользователь увидит эту информацию зайдя на страницу моего магазина.
        Проверить:
        * в БД созадалась запись о новом магазине пользователя
        * изменения отображаются на странице своего магазина
        """
        self.go_to_main_page(self.driver)
        user = self.registration(link_db=databases.db1)
        store = {
            'name': None,
            'address': None,
            'description': None
        }
        self.get_page(self.driver, self.path_settings.URL_SHOP_INFO)
        store = self.get_store_form(self.driver, user_id=user["id"], shop=store)
        info_new = {
            'name': common_utils.random_string(params="letters"),
            'address': common_utils.random_string(length=30),
            'description': common_utils.random_string(length=150)
        }
        store["name_input"].send_keys(info_new["name"])
        store["address_input"].send_keys(info_new["address"])
        store["description_input"].send_keys(info_new["description"])
        self.click_button(store["save_btn"])
        self.get_element_navigate(self.driver, self.check_settings.CHANGE_STORE_INFO_SUCCESS)

        self.driver.refresh()
        time.sleep(self.time_sleep)
        HelpProfileSettingsCheckMethods.progress(self.driver)
        self.get_store_form(self.driver, user_id=user["id"], shop=info_new)
        info_user = databases.db1.accounting.get_user_by_account_id(user["id"])[0]
        shop_id = str(info_user["shop_id"])
        criteria = "shop_id=%s and name='%s' and address='%s' and description='%s'" % (shop_id, info_new["name"],
                                                                                       info_new["address"],
                                                                                       info_new["description"])
        store_new = databases.db1.accounting.get_shop_details_by_criteria(criteria)[0]
        self.assertIsNotNone(store_new, "Не найдено записей в таблице shop_details по запросу %s" % criteria)
        self.get_store_form(self.driver, user_id=user["id"], shop=store_new)

        self.get_page(self.driver, self.path_shop.URL_SHOP % user["id"])
        time.sleep(self.time_sleep)
        self.get_element_navigate(self.driver, self.check_shop.NAME_STORE % info_new["name"])
        self.get_element_navigate(self.driver, self.check_shop.ADDRESS_STORE % info_new["address"])
        self.get_element_navigate(self.driver, self.check_shop.DESCRIPTION_STORE % info_new["description"])

    @priority("Medium")
    def test_edit_store_description(self):
        """
        Title: Я могу отредактировать описание свеого магазина и сохранить изменения (Существующий пользователь.)
        Description:
        Если у меня уже заполнены данные о магазине, Я могу изменить их и сохранить изменения.
        Любой пользователь увидит новую информацию зайдя на страницу моего магазина.
        Проверить:
        * в БД корректно сохранилась новая информация
        * изменения отображаются на странице своего магазина
        """
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)
        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_api=False)
        self.get_page(self.driver, self.path_settings.URL_SHOP_INFO)
        self.assertIsNotNone(self.user["shop_id"], "У user_id='%s' нет идентификатора магазина" % self.user["id"])
        shop_details = databases.db1.accounting.get_shop_details_by_shop_id(self.user["shop_id"])[0]
        self.assertIsNotNone(shop_details, "У user_id='%s' не найдено данных в таблице shop_details" % self.user["id"])
        time.sleep(self.time_sleep)
        store = self.get_store_form(self.driver, user_id=self.user["id"], shop=shop_details)
        self.clear_input_row(self.driver, store["name_input"])
        self.clear_input_row(self.driver, store["address_input"])
        self.clear_input_row(self.driver, store["description_input"])
        info_new = {
            'name': common_utils.random_string(params="letters"),
            'address': common_utils.random_string(length=30),
            'description': common_utils.random_string(length=150)
        }
        store["name_input"].send_keys(info_new["name"])
        store["address_input"].send_keys(info_new["address"])
        store["description_input"].send_keys(info_new["description"])
        self.click_button(store["save_btn"])
        self.get_element_navigate(self.driver, self.check_settings.CHANGE_STORE_INFO_SUCCESS)

        self.driver.refresh()
        HelpProfileSettingsCheckMethods.progress(self.driver)
        time.sleep(self.time_sleep)
        self.get_store_form(self.driver, user_id=self.user["id"], shop=info_new)
        info_user = databases.db1.accounting.get_user_by_account_id(self.user["id"])[0]
        shop_id = str(info_user["shop_id"])
        criteria = "shop_id=%s and name='%s' and address='%s' and description='%s'" % (shop_id, info_new["name"],
                                                                                       info_new["address"],
                                                                                       info_new["description"])
        store_new = databases.db1.accounting.get_shop_details_by_criteria(criteria)[0]
        self.assertIsNotNone(store_new, "Не найдено записей в таблице shop_details по запросу %s" % criteria)
        self.get_store_form(self.driver, user_id=self.user["id"], shop=store_new)

        self.get_page(self.driver, self.path_shop.URL_SHOP % self.user["id"])
        self.get_element_navigate(self.driver, self.check_shop.NAME_STORE % info_new["name"])
        self.get_element_navigate(self.driver, self.check_shop.ADDRESS_STORE % info_new["address"])
        self.get_element_navigate(self.driver, self.check_shop.DESCRIPTION_STORE % info_new["description"])

    @skip('manual')
    @priority("Low")
    def test_not_save_changes_store_description(self):
        """
        Title: Я могу ввести данные о магазине, но не сохранять изменения. Данные магазина останутся старыми
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()



class AddOrEditStoreLogo():
    """
    Story: Добавить \ Удалить логотип магазина
    """

    @skip('need_auto')
    @priority("Must")
    def test_add_store_logo_from_PC(self):
        """
        Title: Я могу изменить \ загрузить логотип магазина (Через файвловый менеджер на ПК).
        Description: Любой пользователь увидит новый логотип, зайдя на страницу моего магазина
        """
        pass

    @skip('need_auto')
    @priority("High")
    def test_delete_store_logo(self):
        """
        Title: Я могу удалить логотип магазина.
        Description: Любой пользователь увидит заглушку логотипа магазина, зайдя на страницу моего магазина
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_add_store_logo_from_tablet(self):
        """
        Title: Я могу изменить \ загрузить логотип магазина (Через файвловый менеджер на планшете).
        Description: Любой пользователь увидит новый логотип, зайдя на страницу моего магазина
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_add_store_logo_from_tablet_camera(self):
        """
        Title: Я могу изменить \ загрузить логотип магазина (Через камеру на планшете).
        Description: Любой пользователь увидит новый логотип, зайдя на страницу моего магазина
        """
        pass



class StoreDescriptionForm():
    """
    Story: Форма Описание магазина + логотип магазина
    """

    @skip('manual')
    @priority("Medium")
    def test_store_description_form_view(self):
        """
        Title: Вид формы описания магазина
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_store_description_form_validation_positive(self):
        """
        Title: Проверка ограничения на поля формы: Позитивные значения
        Description:
        Наборы значений: Зеленые из таблицы сущностей, проверить:
        * Появилось сообщение об успешном сохранении изменений
        * Проверить корректность сохранения значений в базе данных
        * Проверить корректность отображения сделанных изменений на странице настроек магазина
        * Проверить отображение изменений на странице магазина пользователя
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_store_description_form_validation_negative(self):
        """
        Title: Проверка ограничения на поля формы: Негативные значения
        Description:
        Наборы значений: Красные из таблицы сущностей, проверить:
        * невозможность сохранить изменения
        * выдачу соответствующего предупреждающего сообщения
        * в базе значения измененных полей не поменялись на новые.
        """
        pass