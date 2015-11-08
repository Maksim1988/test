# -*- coding: utf-8 -*-
"""
Feature: Авторизация
"""
from unittest import skip, expectedFailure
from ddt import ddt, data
import time
from support import service_log
from support.utils import common_utils
from support.utils.common_utils import generate_sha256, priority
from support.utils.db import databases
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.authorization.classes.class_authorization import AuthCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate


class TestAuthorizationByPhone(Navigate, HelpAuthCheckMethods, HelpLifeCycleCheckMethods, AuthCheckMethods):
    """
    Story: Авторизация по телефону
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Заданные параметры
        cls.type_phone = 'PHONE_VALID'

        # Настройка окружения и вспомогательные параметры
        user_id = AccountingMethods.get_default_user_id()
        cls.user = databases.db1.accounting.get_user_by_criteria_only(criteria='id=%s' % user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

    @priority("Must")
    def test_authorization_by_phone_correct(self, type_password='CORRECT'):
        """
        Title: Я могу войти в систему введя корректный телефон и пароль
        Description:
        Проверка:
            * Наличие профиля пользователя
            * Имя в профиле совпадает с именем пользователя
            * Аватар пользователя совпадает с аватаром пользователя
            * Номер телефона совпадает с номером телефона пользователя
        """
        service_log.run(self)
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        # Переходим на страницу авторизации
        self.go_authorization_page(self.driver)

        # Проверка страница авторизации
        self.check_page_authorization(self.driver)

        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        changed_passwd = self.get_password(type_passwd=type_password, source_passwd=default_new_passwd)
        changed_phone = self.get_phone(type_phone=self.type_phone, source_phone=self.user["phone"])

        # Вводим данные на авторизацию
        self.send_password(password_object=obj_password, password_number=changed_passwd)
        self.send_phone(phone_object=obj_phone, phone_number=changed_phone)

        # Нажатие на кнопку авторизации
        Navigate.element_click(self.driver, obj_submit_button, change_page_url=True)

        # Проверка виджета профиля
        self.user_profile_menu(self.driver, self.user)

    @priority("Must")
    def test_authorization_by_phone_incorrect_password(self, type_password='INCORRECT'):
        """
        Title: Я не могу войти в систему, введя корректный телефон и неверный пароль.
        Description:
        * Отображается сообщение "Проверьте правильность ввода номера телефона и пароля"
        """
        service_log.run(self)
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password(num=3)
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        # Переходим на страницу авторизации
        self.go_authorization_page(self.driver)
        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        changed_passwd = self.get_password(type_passwd=type_password, source_passwd=default_new_passwd)
        changed_phone = self.get_phone(type_phone=self.type_phone, source_phone=self.user["phone"])

        # Вводим данные на авторизацию
        self.send_password(password_object=obj_password, password_number=changed_passwd)
        self.send_phone(phone_object=obj_phone, phone_number=changed_phone)

        # Нажатие на кнопку авторизации
        self.submit_button(obj_submit_button)

        # Проверка формы при не корректном пароле
        self.check_incorrect_passwd(self.driver)

    @priority("High")
    def test_authorization_by_phone_incorrect_user_wait_for_registration(self, type_password='CORRECT'):
        """
        Title: Я не могу войти в систему по телефону, если мой пользователь в статусе WAIT_FOR_REGISTRATION
        (пользователь не закончил регистрацию)
        Description:
        * Отображается соответствующее сообщение
        """
        service_log.run(self)
        status = 'WAIT_FOR_REGISTRATION'
        user = databases.db1.accounting.get_not_enabled_user(status=status)[0]
        AccountingMethods.save_user_password(user_id=user["id"], hash_passwd=user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, user["salt"])
        databases.db1.accounting.update_user_password(user["id"], hash_res_new)

        # Переходим на страницу авторизации
        self.go_authorization_page(self.driver)
        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        changed_passwd = self.get_password(type_passwd=type_password, source_passwd=default_new_passwd)
        changed_phone = self.get_phone(type_phone=self.type_phone, source_phone=user["phone"])

        # Вводим данные на авторизацию
        self.send_password(password_object=obj_password, password_number=changed_passwd)
        self.send_phone(phone_object=obj_phone, phone_number=changed_phone)

        # Нажатие на кнопку авторизации
        self.submit_button(obj_submit_button)

        # Проверка пользователя с незаконченной регистрацией
        self.check_user_wait_for_registration(self.driver)

    @priority("High")
    def test_authorization_by_phone_incorrect_user_disabled(self, type_password='CORRECT'):
        """
        Title: Я не могу войти в систему по телефону, если  мой пользователь в статусе DISABLED
        (пользователь Заблокирован)
        Description:
        * Отображается соответствующее сообщение
        """
        service_log.run(self)
        status = 'DISABLED'
        user = databases.db1.accounting.get_not_enabled_user(status=status)[0]
        AccountingMethods.save_user_password(user_id=user["id"], hash_passwd=user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, user["salt"])
        databases.db1.accounting.update_user_password(user["id"], hash_res_new)

        # Переходим на страницу авторизации
        self.go_authorization_page(self.driver)
        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        changed_passwd = self.get_password(type_passwd=type_password, source_passwd=default_new_passwd)
        changed_phone = self.get_phone(type_phone=self.type_phone, source_phone=user["phone"])

        # Вводим данные на авторизацию
        self.send_password(password_object=obj_password, password_number=changed_passwd)
        self.send_phone(phone_object=obj_phone, phone_number=changed_phone)

        # Нажатие на кнопку авторизации
        self.submit_button(obj_submit_button)

        # Проверка блокировки пользователя
        Navigate.get_element_navigate(self.driver, self.check_auth.ERR_CHECK_DISABLED)
        Navigate.go_to_main_page(self.driver)
        self.check_header_widget_visitor(self.driver)

    @skip('manual')
    @priority("Medium")
    def test_authorization_by_phone_user_created_from_back_office(self):
        """
        Title: Я могу войти в систему созданным через Админку пользователем (используя введенные при создании телефон и пароль)
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class TestAuthorizationByEmail(Navigate, AuthCheckMethods, HelpAuthCheckMethods):
    """
    Story: Авторизация по e-mail
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        # Переходим на главную
        cls.go_to_main_page(cls.driver)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='seller')
        databases.db1.accounting.update_account_details_by_criteria(cls.default_user_id, "locale='ru'")
        stamp = str(time.time())
        cls.email = 'oratest+%s@oorraa.com' % stamp
        databases.db1.accounting.update_account_details_by_criteria(cls.default_user_id, "email='%s'" % cls.email)
        cls.user = databases.db1.accounting.get_user_by_account_id(cls.default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"],
                                             salt=cls.user["salt"])

        # Устанавливаем новый пароль для пользователя
        cls.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(cls.default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)
        service_log.preparing_env(cls)

    @priority("Must")
    def test_authorization_by_email_correct(self):
        """
        Title: Я могу войти в систему введя корректный телефон и email
        Description:
        Проверка:
            * Наличие профиля пользователя
            * Имя в профиле совпадает с именем пользователя
            * Аватар пользователя совпадает с аватаром пользователя
            * Номер телефона совпадает с номером телефона пользователя
        """
        service_log.run(self)
        self.click_reg_and_auth(self.driver)
        self.click_tab_login(self.driver)
        auth_form = self.get_auth_email_form(self.driver)
        auth_form["email_input"].send_keys(self.email)
        auth_form["password_input"].send_keys(self.default_new_passwd)
        self.element_click(self.driver, auth_form["login_btn"], change_page_url=True)
        self.user_profile_menu(self.driver, self.user)

    @priority("Must")
    def test_authorization_by_email_incorrect_password(self):
        """
        Title: Я не могу войти в систему, введя корректный e-mail и неверный пароль.
        Description:
        * Отображается соответствующее сообщение
        """
        service_log.run(self)
        self.click_reg_and_auth(self.driver)
        self.click_tab_login(self.driver)
        auth_form = self.get_auth_email_form(self.driver)
        auth_form["email_input"].send_keys(self.email)
        auth_form["password_input"].send_keys(self.default_new_passwd + common_utils.random_string())
        self.click_button(auth_form["login_btn"])
        self.get_element_navigate(self.driver, self.check_auth.ERR_CHECK_EMAIL_AND_PASS)
        self.go_to_main_page(self.driver)
        self.check_header_widget_visitor(self.driver)

    @priority("High")
    def test_authorization_by_email_incorrect_user_disabled(self):
        """
        Title: Я не могу войти в систему по e-mail, если мой пользователь в статусе DISABLED (пользователь Заблокирован)
        Description:
        * Отображается соответствующее сообщение
        """
        service_log.run(self)
        criteria = "display_name is not NULL"
        stamp = str(time.time())
        email = 'oratest+%s@oorraa.com' % stamp
        user = databases.db1.accounting.get_user_by_criteria(account_status="DISABLED", criteria=criteria)[0]
        databases.db1.accounting.update_account_details_by_criteria(user["id"], "email='%s'" % email)
        AccountingMethods.save_user_password(user_id=user["id"], hash_passwd=user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(self.default_new_passwd, user["salt"])
        databases.db1.accounting.update_user_password(user["id"], hash_res_new)
        self.click_reg_and_auth(self.driver)
        self.click_tab_login(self.driver)
        auth_form = self.get_auth_email_form(self.driver)
        auth_form["email_input"].send_keys(email)
        auth_form["password_input"].send_keys(default_new_passwd)
        self.click_button(auth_form["login_btn"])
        self.get_element_navigate(self.driver, self.check_auth.ERR_CHECK_DISABLED)
        self.go_to_main_page(self.driver)
        self.check_header_widget_visitor(self.driver)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class TestFormAuthorization(Navigate, AuthCheckMethods, HelpAuthCheckMethods):
    """
    Story: Форма авторизации
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        # Переходим на главную
        cls.go_to_main_page(cls.driver)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='seller')
        databases.db1.accounting.update_account_details_by_criteria(cls.default_user_id, "locale='ru'")
        stamp = str(time.time())
        cls.email = 'oratest+%s@oorraa.com' % stamp
        databases.db1.accounting.update_account_details_by_criteria(cls.default_user_id, "email='%s'" % cls.email)
        cls.user = databases.db1.accounting.get_user_by_account_id(cls.default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        cls.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(cls.default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)
        service_log.preparing_env(cls)

    @priority("Medium")
    def test_authorization_form_empty_password(self):
        """
        Title: Я не могу авторизоваться с пустым паролем. Отображается сообщение "Введите пароль"
        """
        self.click_reg_and_auth(self.driver)
        self.click_tab_login(self.driver)
        auth_form = self.get_auth_email_form(self.driver)
        auth_form["email_input"].send_keys(self.email)
        self.click_button(auth_form["login_btn"])
        self.get_element_navigate(self.driver, self.check_auth.ERR_INPUT_PASS)
        self.go_to_main_page(self.driver)
        self.check_header_widget_visitor(self.driver)

    @priority("Medium")
    def test_authorization_form_empty_login(self):
        """
        Title: Я не могу авторизоваться с пустым логином (телефон или email)
        """
        self.click_reg_and_auth(self.driver)
        self.click_tab_login(self.driver)
        auth_form = self.get_auth_email_form(self.driver)
        auth_form["password_input"].send_keys(self.default_new_passwd)
        self.click_button(auth_form["login_btn"])
        self.get_element_navigate(self.driver, self.check_auth.ERR_EMPTY_EMAIL_OR_PHONE)
        self.go_to_main_page(self.driver)
        self.check_header_widget_visitor(self.driver)

    @skip('manual')
    @priority("Low")
    def test_authorization_form_hide_password(self):
        """
        Title: Вводимые символы пароля маскируются звездочками
        """
        pass

    @priority("High")
    def test_authorization_form_link_to_restore_password_page(self):
        """
        Title: Click: Я могу перейти на страницу восстановления пароля, кликнув на "Забыли пароль"
        """
        service_log.run(self)
        self.click_reg_and_auth(self.driver)
        self.click_tab_login(self.driver)
        auth_form = self.get_auth_email_form(self.driver)
        self.click_button(auth_form["restore_btn"])
        url_web = self.driver.current_url.encode('utf-8')
        url_need = self.ENV_BASE_URL + Navigate.path_restore.URL_RESTORE_EMAIL
        err_msg = "Урл страницы егистрации: %s не соответствует целевому урлу: %s"
        self.assertEqual(url_web, url_need, err_msg % (url_web, url_need))
        self.get_restore_email_form(self.driver)

    @priority("High")
    def test_authorization_form_link_to_main_page(self):
        """
        Title: Click: Я могу вернуться на главную страницу с формы Авторизации, нажав на "На главную"
        """
        service_log.run(self)
        self.get_page(self.driver, self.path_auth.PATH_AUTH)
        back_to_main = self.get_element_navigate(self.driver, self.click_auth.BACK_TO_MAIN)
        self.click_button(back_to_main)
        url = self.driver.current_url.encode('utf-8')[:-1]
        url_need = self.ENV_BASE_URL
        err_msg = "Урл страницы егистрации: %s не соответствует целевому урлу: %s"
        self.assertEqual(url, url_need, err_msg % (url, url_need))
        self.get_element_navigate(self.driver, self.check_main.MAIN_MENU_HOME_ACTIVE)

    @priority("High")
    def test_authorization_form_link_to_registration_page(self):
        """
        Title: Click: Я могу перейти на страницу регистрации, нажав на "Регистрация"
        Description:
        * Отображается форма регистрации на вкладке "Эл. почта"
        """
        service_log.run(self)
        self.go_authorization_page(self.driver)
        self.go_registration_page(self.driver)
        self.check_registration_page(self.driver)

    @priority("Low")
    def test_authorization_form_register_depends(self, type_phone='PHONE_VALID', type_password='INCORRECT_REGISTER'):
        """
        Title: Проверить регистрозависимость пароля, введя пароль, отличающийся от корректного только регистром
        Description:
        * Отображается сообщение "Проверьте правильность ввода номера телефона и пароля"
        """
        service_log.run(self)
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password(num=3)
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        # Переходим на страницу авторизации
        self.go_authorization_page(self.driver)
        #self.click_to_phone(self.driver)
        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        changed_passwd = self.get_password(type_passwd=type_password, source_passwd=default_new_passwd)
        changed_phone = self.get_phone(type_phone=type_phone, source_phone=self.user["phone"])

        # Вводим данные на авторизацию
        self.send_password(password_object=obj_password, password_number=changed_passwd)
        self.send_phone(phone_object=obj_phone, phone_number=changed_phone)

        # Нажатие на кнопку авторизации
        self.submit_button(obj_submit_button)

        # Проверка формы при не корректном пароле
        self.check_incorrect_passwd(self.driver)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()