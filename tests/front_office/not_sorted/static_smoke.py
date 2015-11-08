# -*- coding: utf-8 -*-
"""
Feature: Набор смоук тестов продакшена
Description: Используются статичные данные
"""
from ddt import ddt, data
import time

from support import service_log
from support.utils import common_utils
from support.utils.common_utils import run_on_prod, priority
from support.utils.mail_api import Inbox
from tests.front_office.authorization.classes.class_authorization import AuthMethods
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods, HelpNavigateMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleMethods
from tests.front_office.registration.classes.class_registration_email import RegEmailMethods
from tests.worker_accounting.class_accounting import AccountingMethods

__author__ = 's.trubachev'

users = {"test_alpha": {"name": "Тест Alfa", "phone": "71110000001", "passwd": "95755"},
         "test_bravo": {"name": "Тест Bravo", "phone": "71110000002", "passwd": "79224"},
         "test_charlie": {"name": "Тест Charlie", "email": "oratest+charlie@oorraa.com", "passwd": "123456"},
         "test_delta": {"name": "Тест Delta", "email": "oratest+delta@oorraa.com", "passwd": "123456"}
}

@ddt
class TestAuthorization(HelpAuthCheckMethods, AuthMethods):
    """
    Story: Страница авторизация
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)

    @run_on_prod(True)
    @priority('medium')
    @data('test_charlie', 'test_delta')
    def test_authorization_by_mail(self, name_user='test_charlie'):
        """
        Title: Авторизация пользователя по e-mail со статичными данными.
        """
        user = users[name_user]
        service_log.run(self)
        # Переходим на страницу авторизации
        self.go_authorization_page(self.driver)

        # Вводим данные на авторизацию
        auth_form = self.get_auth_email_form(self.driver)

        auth_form["email_input"].send_keys(user["email"])
        auth_form["password_input"].send_keys(user["passwd"])
        HelpNavigateMethods.element_click(self.driver, auth_form["login_btn"], change_page_url=True)

        # Проверка виджета профиля
        self.check_menu_profile_widget_total(self.driver, user["name"])

    @run_on_prod(True)
    @priority('medium')
    @data('test_alpha', 'test_bravo')
    def test_authorization_by_phone(self, name_user='test_alpha'):
        """
        Title: Авторизация пользователя по номеру телефона со статичными данными.
        """
        user = users[name_user]
        service_log.run(self)
        # Переходим на страницу авторизации
        self.go_authorization_page(self.driver)
        #self.click_to_phone(self.driver)

        # Проверка страница авторизации
        self.check_page_authorization(self.driver)

        # Вводим данные на авторизацию
        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        self.send_phone(phone_object=obj_phone, phone_number=user["phone"])
        self.send_password(password_object=obj_password, password_number=user["passwd"])

        # Нажатие на кнопку авторизации
        HelpNavigateCheckMethods.element_click(self.driver, obj_submit_button, change_page_url=True)

        # Проверка виджета профиля
        self.check_menu_profile_widget_total(self.driver, user["name"])

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class TestRegistration(HelpAuthCheckMethods, AuthMethods, RegEmailMethods, HelpNavigateMethods, Inbox):
    """
    Story: Страница регистрация
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        HelpNavigateMethods.go_to_main_page(cls.driver)
        service_log.preparing_env(cls)

    @priority('medium')
    def test_registration_by_email(self):
        """
        Title: Регистрация пользователя.
        """
        service_log.run(self)
        # Регистрация
        url_main = self.driver.current_url.encode('utf-8')
        self.click_reg_and_auth(self.driver)
        reg_email = self.get_reg_email_form(self.driver)
        name = u'Тест %s' % common_utils.random_string(length=4)

        email = 'oratest+%s@oorraa.com' % str(time.time())
        password = AccountingMethods.get_default_password(5)

        reg_email["name_input"].send_keys(name)
        reg_email["email_input"].send_keys(email)
        reg_email["password_input"].send_keys(password)
        self.element_click(self.driver, reg_email["reg_btn"], change_page_url=False)
        start_work = self.get_reg_email_success(self.driver, email.lower())
        self.element_click(self.driver, start_work, change_page_url=True)
        work = time.time()
        messages = None
        while time.time() - work < self.email_timeout:
            try:
                messages = self.get_email(to_email=email)
                self.assertNotEqual(len(messages), 0, "Не получено сообщение")
                break
            except Exception:
                pass
        self.assertIsNotNone(messages, "Не получено сообщение")
        message = messages[0]
        mail_from = message['From']
        mail_body = message['Body']
        valid = mail_body.split(self.URL_VALIDATE_PATH)
        valid_hash = valid[1][:64]
        validate_path = self.URL_VALIDATE_EMAIL % valid_hash
        err_msg_1 = "Полученный урл активации емайла не найден в теле полученного письма"
        self.assertIn('noreply@oorraa.com', mail_from, "Почта отправителя: %s" % mail_from)
        self.assertIn(validate_path, mail_body, err_msg_1)
        # Переход по ссылке валидации емайла
        self.get_page(self.driver, validate_path)
        url_web = self.driver.current_url.encode('utf-8')
        url_need = self.ENV_BASE_URL + self.path_reg.URL_VALIDATED_EMAIL
        err_msg = "Урл страницы успешной валидации емайла: %s не соответствует целевому урлу: %s"
        self.assertEqual(url_web, url_need, err_msg % (url_web, url_need))
        # начать работу
        start_work = self.get_validated_email_success(self.driver)
        self.element_click(self.driver, start_work)

        # Проверка, что после нажатия на кнопку Начать работу произошел переход обратно на главную
        url_web = self.driver.current_url.encode('utf-8')
        err_msg = "Не произошел переход на главную страницу %s, пользователь остался на странице %s"
        self.assertEqual(url_web, url_main, err_msg % (url_main, url_web))

        # Проверка виджета профиля
        self.check_menu_profile_widget_total(self.driver, name)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()