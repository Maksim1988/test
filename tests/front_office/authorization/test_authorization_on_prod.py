# -*- coding: utf-8 -*-
"""
Feature: Авторизация на проде
Description: Набор тестов для проверки функционала авторизации на проде
"""
import random

from ddt import ddt, data

from support import service_log
from support.utils.common_utils import priority
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods


__author__ = 's.trubachev'


class TestAuthorizationCheckUsers_on_prod(HelpAuthCheckMethods, HelpLifeCycleCheckMethods):
    """
    Story: Авторизация под пользователями на продакшене
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Заданные параметры
        cls.type_password = 'CORRECT'
        cls.type_phone = 'PHONE_VALID'

        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

    @priority("medium")
    def test_authorization_user_buyer(self):
        """
        Title: Проверка авторизации под покупателем. test_authorization_user_buyer
        """
        service_log.run(self)
        user = self.get_static_user_by_role("buyer")[0]
        default_new_passwd = user["password"]

        # Переходим на страницу авторизации
        self.go_authorization_page(self.driver)
        #self.click_to_phone(self.driver)

        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        changed_passwd = self.get_password(type_passwd=self.type_password, source_passwd=default_new_passwd)
        changed_phone = self.get_phone(type_phone=self.type_phone, source_phone=user["phone"])

        # Вводим данные на авторизацию
        self.send_password(password_object=obj_password, password_number=changed_passwd)
        self.send_phone(phone_object=obj_phone, phone_number=changed_phone)

        # Нажатие на кнопку авторизации
        self.submit_button(obj_submit_button)

        # Проверка виджета профиля
        self.check_menu_profile_widget_total(self.driver, user["display_name"])
        self.check_menu_profile_widget_my_shop(self.driver)
        self.check_profile_widget(self.driver)

    @priority("medium")
    def test_authorization_user_seller(self):
        """
        Title: Проверка авторизации под продавцом. test_authorization_user_seller
        """
        service_log.run(self)
        user = self.get_static_user_by_role("seller")[0]
        default_new_passwd = user["password"]

        # Переходим на страницу авторизации
        self.go_authorization_page(self.driver)
        #self.click_to_phone(self.driver)

        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        changed_passwd = self.get_password(type_passwd=self.type_password, source_passwd=default_new_passwd)
        changed_phone = self.get_phone(type_phone=self.type_phone, source_phone=user["phone"])

        # Вводим данные на авторизацию
        self.send_password(password_object=obj_password, password_number=changed_passwd)
        self.send_phone(phone_object=obj_phone, phone_number=changed_phone)

        # Нажатие на кнопку авторизации
        self.submit_button(obj_submit_button)

        # Проверка виджета профиля
        self.check_menu_profile_widget_total(self.driver, user["display_name"])
        self.check_menu_profile_widget_my_shop(self.driver)
        self.check_profile_widget(self.driver)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestCheckRestore_on_prod(HelpAuthCheckMethods, HelpLifeCycleCheckMethods):
    """
    Story: Восстановление пароля под пользователями на продакшене
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

    @priority("medium")
    def test_goToRestorePassword(self):
        """
        Title: Тест проверяет переход на страницы Забыли пароль
        """
        self.go_authorization_page(self.driver)
        self.go_restore_page(self.driver)
        self.click_to_phone(self.driver)
        self.check_restore_page(self.driver)

    @priority("medium")
    def test_pageRestorePassword(self):
        """
        Title: Тест проверяет внешний вид страницы "Забыли пароль"
        """
        self.go_authorization_page(self.driver)
        self.go_restore_page(self.driver)
        self.click_to_phone(self.driver)
        self.check_restore_page(self.driver)
        self.check_page_restore_password(self.driver)

    @priority("medium")
    def test_pageRestoreGoToRegistrationPage(self):
        """
        Title: Тест проверяет переход со страницы "Забыли пароль" на страницу "Регистрация"
        """
        self.go_authorization_page(self.driver)
        #self.click_to_phone(self.driver)
        self.go_restore_page(self.driver)
        self.driver.back()
        self.go_registration_page(self.driver)
        self.check_registration_page(self.driver)

    @priority("medium")
    @data('', '912345678', 'ttt', u'абв')
    def test_checkRestorePasswordNegativePhone(self, phone_number='ttt'):
        """
        Title: Тест проверяет функционал "Забыли пароль" негативные кейсы для поля Мобильный телефон
        """
        self.go_authorization_page(self.driver)
        self.go_restore_page(self.driver)
        self.click_to_phone(self.driver)
        phone, sent_passwd_button = self.get_data_restore(self.driver)
        phone.send_keys(phone_number)
        self.click_button(sent_passwd_button)
        self.check_need_phone(self.driver)

    @priority("medium")
    def test_checkRestorePassword_ErrorPassword(self):
        """
        Title: Тест проверяет функционал "Забыли пароль" негативные кейсы для поля Мобильный телефон
        """
        phone_number = str(random.randrange(1000000000, 9999999999, 1))
        self.go_authorization_page(self.driver)
        self.go_restore_page(self.driver)
        self.click_to_phone(self.driver)
        phone, sent_passwd_button = self.get_data_restore(self.driver)
        phone.send_keys(phone_number)
        self.click_button(sent_passwd_button)
        self.check_sent_passwd(self.driver)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class TestCheckRegistration(HelpAuthCheckMethods, HelpLifeCycleCheckMethods):
    """
    Story: Регистрация под пользователями на продакшене
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

    @priority("medium")
    def test_goToRegistrationPage(self):
        """
        Title: Тест проверяет переход на страницы, Регистрация, Помощь, Забыли пароль
        """
        self.go_authorization_page(self.driver)
        #self.click_to_phone(self.driver)
        self.go_registration_page(self.driver)
        self.check_registration_page(self.driver)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestAuthorizationPageCheckPasswd_on_prod(HelpAuthCheckMethods, HelpLifeCycleCheckMethods):
    """
    Story: Проверка поля пароль при авторизации
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Заданные параметры
        cls.group = '2'  # SELLER
        cls.status = 'ENABLED'
        cls.type_phone = 'PHONE_VALID'

        # Настройка окружения и вспомогательные параметры
        cls.buyer = cls.get_static_user_by_role("seller")[0]
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

    @priority("medium")
    def test_AuthorizationSellerAllCorrect(self, type_password='CORRECT'):
        """
        Title: Тест на авторизацию продавца c корректным паролем и валидным логином (телефоном)
        """
        service_log.run(self)
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = self.buyer["password"]

        # Переходим на страницу авторизации
        self.go_authorization_page(self.driver)
        #self.click_to_phone(self.driver)

        # Проверка страница авторизации
        self.check_page_authorization(self.driver)

        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        changed_passwd = self.get_password(type_passwd=type_password, source_passwd=default_new_passwd)
        changed_phone = self.get_phone(type_phone=self.type_phone, source_phone=self.buyer["phone"])

        # Вводим данные на авторизацию
        self.send_password(password_object=obj_password, password_number=changed_passwd)
        self.send_phone(phone_object=obj_phone, phone_number=changed_phone)

        # Нажатие на кнопку авторизации
        self.submit_button(obj_submit_button)

        # Проверка виджета профиля
        self.check_menu_profile_widget_total(self.driver, self.buyer["display_name"])

    @priority("medium")
    def test_AuthorizationSellerPassword(self, type_password='INCORRECT'):
        """
        Title: Тест на авторизацию продавца с  корректным паролем и валидным логином (телефоном).
        """
        service_log.run(self)
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = self.buyer["password"]

        # Переходим на страницу авторизации
        self.go_authorization_page(self.driver)
        #self.click_to_phone(self.driver)
        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        changed_passwd = self.get_password(type_passwd=type_password, source_passwd=default_new_passwd)
        changed_phone = self.get_phone(type_phone=self.type_phone, source_phone=self.buyer["phone"])

        # Вводим данные на авторизацию
        self.send_password(password_object=obj_password, password_number=changed_passwd)
        self.send_phone(phone_object=obj_phone, phone_number=changed_phone)

        # Нажатие на кнопку авторизации
        self.submit_button(obj_submit_button)

        # Проверка формы при не корректном пароле
        self.check_incorrect_passwd(self.driver)

    @priority("medium")
    def test_AuthorizationSellerNeedPassword(self):
        """
        Title: Валидация полей формы Авторизации.
        Description: http://test-rails.oorraa.pro/index.php?/cases/view/546
        """
        service_log.run(self)
        # Переходим на страницу авторизации
        self.go_authorization_page(self.driver)
        #self.click_to_phone(self.driver)
        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        changed_phone = self.get_phone(type_phone=self.type_phone, source_phone=self.buyer["phone"])

        # Вводим данные на авторизацию
        self.send_phone(phone_object=obj_phone, phone_number=changed_phone)

        # Нажатие на кнопку авторизации
        self.submit_button(obj_submit_button)

        # Проверка формы при не веденном пароле
        self.check_need_password(self.driver)
        self.check_not_need_phone(self.driver)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()

