# -*- coding: utf-8 -*-
"""
Feature: Страница "Контакты УУРРАА"
"""
import base64
import quopri
from imaplib import IMAP4_SSL
import email
import re
from email.header import Header, decode_header, make_header
from ddt import ddt, data
import time
from support import service_log
from support.utils.common_utils import generate_sha256, priority
from support.utils.db import databases
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateData
from tests.front_office.help.classes.class_contacts import HelpContactsCheckMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods
from unittest import skip


@ddt
class TestSendFeedbackByGuest(HelpAuthCheckMethods, HelpContactsCheckMethods):
    """
    Story: Отправить отзыв со страницы Контакты УУРРАА как Гость
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

        # Генерим тестовые данные
        cls.test_data = cls.generate_data_for_feedback()
        # Переходим на страницу контакты
        cls.get_page(cls.driver, cls.path_contacts.URL_CONTACTS)

    @priority("High")
    def test_all_fields(self):
        """
        Title: Я, как Гость, могу отправить форму обратной связи, заполни в все поля.
        """
        obj = self.get_all_fields(self.driver)
        self.set_fields(obj, self.test_data)
        self.click_button(self.get_element_navigate(self.driver, self.click_contacts.SENDING))
        self.check_success_sent(self.driver)
        #self.get_email()
        pass
        #TODO: сделать проверку в почте, что получено сообщение https://jira.oorraa.net/browse/RT-773

    @priority("medium")
    def test_require_fields(self):
        """
        Title: Я, как Гость, могу отправить форму обратной связи, заполнив только обязательные поля.
        """
        obj = self.get_all_fields(self.driver)
        # удаляем сгенерированный телефон - необязательное поле
        self.test_data.update({'phone': ''})
        self.set_fields(obj, self.test_data)
        self.click_button(self.get_element_navigate(self.driver, self.click_contacts.SENDING))
        self.check_success_sent(self.driver)
        #TODO: сделать проверку в почте, что получено сообщение https://jira.oorraa.net/browse/RT-773

    @priority("medium")
    def test_empty_field_name(self):
        """
        Title: Если поле "Имя" не заполнено, то я не смогу отправить форму обратной связи, -
        отобразится соответствующее сообщение
        """
        obj = self.get_all_fields(self.driver)
        # удаляем сгенерированное имя
        self.test_data.update({'name': ''})
        self.set_fields(obj, self.test_data)
        self.click_button(self.get_element_navigate(self.driver, self.click_contacts.SENDING))
        self.check_err_msg(self.driver, field='name')

    @priority("medium")
    def test_empty_field_email(self):
        """
        Title: Если поле "e-mail" не заполнено, то я не смогу отправить форму обратной связи, -
        отобразится соответствующее сообщение
        """
        obj = self.get_all_fields(self.driver)
        # удаляем сгенерированный емайл
        self.test_data.update({'email': ''})
        self.set_fields(obj, self.test_data)
        self.click_button(self.get_element_navigate(self.driver, self.click_contacts.SENDING))
        self.check_err_msg(self.driver, field='email')

    @priority("medium")
    def test_empty_field_message(self):
        """
        Title: Если поле "Сообщение" не заполнено, то я не смогу отправить форму обратной связи, -
        отобразится соответствующее сообщение
        """
        obj = self.get_all_fields(self.driver)
        # удаляем сгенерированное сообщение
        self.test_data.update({'message': ''})
        self.set_fields(obj, self.test_data)
        self.click_button(self.get_element_navigate(self.driver, self.click_contacts.SENDING))
        self.check_err_msg(self.driver, field='message')

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()



@ddt
class TestSendFeedbackByUser(HelpAuthCheckMethods, HelpContactsCheckMethods):
    """
    Story: Отправить отзыв со страницы Контакты УУРРАА как авторизованный пользователь
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

    @priority("High")
    def test_buyer_with_email(self):
        """
        Title: Я как Пользователь, у которого заполнено поле e-mail в профиле, могу отправить форму обратной связи, указав текст Сообщения.
        """
        # Настройка окружения и вспомогательные параметры
        criteria = "email is not NULL and phone like '7%s' and LENGTH(phone)=11 and locale='ru' and display_name is not NULL"
        self.user = databases.db1.accounting.get_user_by_criteria("ENABLED", criteria % '%')[0]
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        self.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(self.default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)
        self.go_main(self.driver, phone=self.user["phone"], passwd=self.default_new_passwd, flag_auth=True)

        # Генерим тестовые данные
        self.test_data = self.generate_data_for_feedback()
        # Проверяем, что залогинены
        self.check_menu_profile_widget_total(self.driver, self.user['display_name'])
        ## Переходим на страницу Настройки
        #self.get_page(self.driver, self.path_settings.PATH_PROFILE_SETTINGS)
        ## Меняем емайл
        #self.set_email(self.driver, self.test_data['email'])
        ## Проверка успешности смены емайла
        #self.check_email(databases.db1, self.default_user_id, self.test_data['email'])
        # Переходим на страницу контакты
        self.get_page(self.driver, self.path_contacts.URL_CONTACTS)
        msg = self.get_element_navigate(self.driver, self.input_contacts.MESSAGE)
        msg.send_keys(self.test_data['message'])
        self.click_button(self.get_element_navigate(self.driver, self.click_contacts.SENDING))
        self.check_success_sent_user(self.driver)
        #TODO: сделать проверку в почте, что получено сообщение https://jira.oorraa.net/browse/RT-773

    @priority("medium")
    def test_buyer_without_email(self):
        """
        Title: Я как Пользователь, у которого не заполнено поле e-mail в профиле, могу отправить форму обратной связи, указав текст Сообщения.
        """
        # Настройка окружения и вспомогательные параметры
        criteria = "email is NULL and phone like '7%s' and LENGTH(phone)=11 and locale='ru' and display_name is not NULL"
        self.user = databases.db1.accounting.get_user_by_criteria("ENABLED", criteria % '%')[0]
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        self.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(self.default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=self.default_new_passwd, flag_auth=True)

        # Генерим тестовые данные
        self.test_data = self.generate_data_for_feedback()
        # Проверяем, что залогинены
        self.check_menu_profile_widget_total(self.driver, self.user['display_name'])
        ## Переходим на страницу Настройки
        #self.get_page(self.driver, self.path_settings.PATH_PROFILE_SETTINGS)
        #self.test_data.update({'email': ''})
        ## Меняем емайл
        #self.set_email(self.driver, self.test_data['email'])
        ## Проверка успешности смены емайла
        #self.check_email(databases.db1, self.default_user_id, self.test_data['email'])
        # Переходим на страницу контакты
        self.get_page(self.driver, self.path_contacts.URL_CONTACTS)
        msg = self.get_element_navigate(self.driver, self.input_contacts.MESSAGE)
        msg.send_keys(self.test_data['message'])
        self.click_button(self.get_element_navigate(self.driver, self.click_contacts.SENDING))
        self.check_success_sent_user(self.driver)
        #TODO: сделать проверку в почте, что получено сообщение https://jira.oorraa.net/browse/RT-773

    @priority("medium")
    def test_empty_field_message(self):
        """
        Title: Если текст сообщения не введен, то я не смогу отправить форму обратной связи - отобразится соответствующее сообщение
        """
        # Настройка окружения и вспомогательные параметры
        criteria = "email is not NULL and phone like '7%s' and LENGTH(phone)=11 and locale='ru' and display_name is not NULL"
        self.user = databases.db1.accounting.get_user_by_criteria("ENABLED", criteria % '%')[0]
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        self.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(self.default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=self.default_new_passwd, flag_auth=True)

        # Проверяем, что залогинены
        self.check_menu_profile_widget_total(self.driver, self.user['display_name'])
        # Переходим на страницу контакты
        self.get_page(self.driver, self.path_contacts.URL_CONTACTS)
        self.click_button(self.get_element_navigate(self.driver, self.click_contacts.SENDING))
        self.check_err_msg(self.driver, field='message')

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()



@ddt
class TestContactPageView(HelpAuthCheckMethods, HelpContactsCheckMethods):
    """
    Story: Внешний вид и содержимое страницы Контакты УУРРАА
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        #service_log.preparing_env(cls)

        # Переходим на главную
        cls.go_to_main_page(cls.driver)

    @priority("medium")
    def test_go_to_contacts(self, test_data=HelpNavigateData.MFB_CONTACTS):
        """
        Title: Переход на страницу Контакты
        """
        #service_log.run(self)
        self.check_navigate(self.driver, test_data)

    @priority("Low")
    def test_oorraa_contact_page_view(self):
        """
        Title: Внешний вид страницы Контакты УУРРАА
        """
        self.get_page(self.driver, self.path_contacts.URL_CONTACTS)
        time.sleep(self.time_sleep)
        self.check_view_contacts(self.driver)

    @priority("medium")
    @data(*HelpContactsCheckMethods.CONTACT_NAVIGATE)
    def test_contact_navigate(self, test_data):
        """
        Title: Переходы со страницы Контакты УУРРАА по ссылкам
        Description:
        * По ссылке "Как покупать на Уурраа?" я могу попасть на страницу центра помощи /help-1
        * По ссылке "Как стать продавцом и разместить товары?" я могу попасть на страницу центра помощи /help-6
        * По ссылке "Часто задаваемые вопросы" я могу попасть на страницу центра помощи /help-1
        * По ссылке "Показать на карте" я могу попасть на страницу сайта oorraa.netб в раздел "Схема процезда":
        (http://oorraa.net/#locate)
        """
        self.get_page(self.driver, self.path_contacts.URL_CONTACTS)
        self.check_navigate(self.driver, self.CONTACT_NAVIGATE[test_data])

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()



class TestFeedbackForm():
    """
    Story: Форма обратной связи
    """

    @skip('manual')
    @priority("Low")
    def test_feedback_form_validation_positive(self):
        """
        Title: Проверка ограничения на поля формы: Позитивные значения
        Description:
        Наборы значений: Зеленые из таблицы сущностей, проверить:
        * При отправке сообщений не возникло ошибок
        * Письмо корректно отправлено и содержимое письма соответствует тому что отправлялось
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_feedback_form_validation_negative(self):
        """
        Title: Проверка ограничения на поля формы: Негативные значения
        Description:
        Наборы значений: Красные из таблицы сущностей, проверить:
        * невозможность отправить форму обратной связи
        * выдачу соответствующего предупреждающего сообщения
        """
        pass
