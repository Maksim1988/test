# -*- coding: utf-8 -*-
"""
Feature: Смена пароля
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



class ChangePassword(HelpProfileSettingsCheckMethods, HelpAuthCheckMethods):
    """
    Story: Блок смена пароля
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

    @priority("Must")
    def test_change_password(self):
        """
        Title: Я могу сменить свой пароль, на новый. После этого я не смогу войти под старым, но смогу под новым
        """
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)
        self.go_to_main_page(self.driver)
        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_api=False)

        new_password = common_utils.random_string(length=6)

        self.get_page(self.driver, self.path_settings.URL_CHANGE_PASSWORD)
        pass_form = self.get_password_form(self.driver)
        pass_form["password_input"].send_keys(default_new_passwd)
        pass_form["new_password_input"].send_keys(new_password)
        pass_form["repeat_password_input"].send_keys(new_password)
        self.click_button(pass_form["save_btn"])

        self.get_element_navigate(self.driver, self.check_settings.CHANGE_PASSWORD_SUCCESS)
        time.sleep(4)
        menu = self.get_element_navigate(self.driver, self.check_main.CHECK_MENU_USER)
        self.element_click(self.driver, menu, change_page_url=False)
        exit_btn = self.get_element_navigate(self.driver, self.click_main.MENU_PROFILE_EXIT)
        self.element_click(self.driver, exit_btn)

        #self.click_to_phone(self.driver)
        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)

        # Вводим данные на авторизацию
        self.send_phone(phone_object=obj_phone, phone_number=self.user["phone"])
        self.send_password(password_object=obj_password, password_number=new_password)
        # Нажатие на кнопку авторизации
        self.element_click(self.driver, obj_submit_button)

        self.check_header_widget_seller(self.driver, self.user["id"])

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class ChangePasswordForm():
    """
    Story: Форма Смены пароля
    """

    @skip('manual')
    @priority("Medium")
    def test_change_password_form_view(self):
        """
        Title: Вид формы смены пароля
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_change_password_form_validation_positive(self):
        """
        Title: Проверка ограничения на поля формы: Позитивные значения
        Description:
        Наборы значений: Зеленые из таблицы сущностей, проверить:
        * Появилось сообщение об успешном сохранении изменений
        * Проверить, что в базе данных значение пароля изменилось и сохранено в зашифрованном виде
        * Проверить успешную авторизацию с новым паролем
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_change_password_form_validation_negative(self):
        """
        Title: Проверка ограничения на поля формы: Негативные значения
        Description:
        Наборы значений: Красные из таблицы сущностей, проверить:
        * невозможность сохранить изменения
        * выдачу соответствующего предупреждающего сообщения
        * в базе значения не поменялись на новые
        """
        pass