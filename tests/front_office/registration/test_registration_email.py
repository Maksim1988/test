# -*- coding: utf-8 -*-
"""
Feature: Регистрация по email
"""
import time
from unittest import skip
from unittest import expectedFailure
from support import service_log
from support.utils import common_utils
from support.utils.common_utils import priority
from support.utils.db import databases
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.authorization.classes.class_authorization import AuthCheckMethods
from tests.front_office.registration.classes.class_registration_email import RegEmailCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate
from support.utils.mail_api import Inbox


class RegistrationByEmailLogic(Navigate, HelpAuthCheckMethods, AuthCheckMethods, RegEmailCheckMethods, Inbox):
    """
    Story: Регистрация по e-mail
    """
    def check_count_roles_and_status(self, user_id, count_roles=1, roles=None):
        result_data_user = databases.db1.accounting.get_data_user_by_id(user_id)
        roles_user = databases.db1.accounting.get_roles_by_id(user_id)
        # проверка роли пользователя
        self.assertEqual(len(roles_user), count_roles, "ОШИБКА: У пользователя не совпало количество ролей")
        for role_user in roles_user:
            self.assertIn(str(role_user["permission_id"]), roles, "Проверка роли неуспешна.")
        self.assertEqual(result_data_user[0]["account_status"], 'ENABLED')

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        cls.go_to_main_page(cls.driver)
        #p = cls.set_cookies(cls.driver)
        service_log.preparing_env(cls)

    @priority("Must")
    def test_registration_by_email_correct(self, new_messages=2):
        """
        Title: Я могу зарегистрироваться по e-mail
        Description:
        1. Заполнить форму регистрации, указав имя, корректный адрес почты и пароль, нажать "Зарегистрироваться"
            * Отображается страница "Регистрация завершена"
            * Проверить содержимое страницы (текст и иконку)
            * Проверить наличие кнопки "Начать работу"
            * В базу сохранен новый пользователь, с введенным им паролем. Статус пользователя: "Активный", роль Продавец.
        2. Нажать на кнопку "Начать работу"
            * Произошел вход в систему под созданной учетной записью, в  профиле (справа-сверху)
            корректно отображается имя пользователя в соответствии с созданным
            * на странице настроек профиля  корректно отображается информация в соответствии с введеным
            при регистрации (сразу после создания отображается, e-mail, роль и имя)
            * Проверить наличие двух сообщений в мессенджере.
        3. Проверить что на введенный при регистрации e-mail пришло подтверждающее письмо
        """
        service_log.run(self)
        # Регистрация
        url_main = self.driver.current_url.encode('utf-8')
        self.click_reg_and_auth(self.driver)
        reg_email = self.get_reg_email_form(self.driver)
        name = common_utils.random_string()

        email = self.get_new_email(databases.db1)

        password = AccountingMethods.get_default_password(5)
        reg_email["name_input"].send_keys(name)
        reg_email["email_input"].send_keys(email)
        reg_email["password_input"].send_keys(password)
        self.element_click(self.driver, reg_email["reg_btn"], change_page_url=False)
        crt = "display_name='%s' and email='%s'" % (name, email.lower())
        user = databases.db1.accounting.get_user_by_criteria(account_status="ENABLED", criteria=crt)[0]
        start_work = self.get_reg_email_success(self.driver, email.lower())
        self.check_count_roles_and_status(user_id=user["id"], count_roles=2, roles='1,2')
        self.element_click(self.driver, start_work)
        # Проверка, что после нажатия на кнопку Начать работу произошел переход обратно на главную
        url_web = self.driver.current_url.encode('utf-8')
        err_msg = "Не произошел переход на главную страницу %s, пользователь остался на странице %s"
        self.assertEqual(url_web, url_main, err_msg % (url_main, url_web))

        # Проверка что сформирован хеш для подтеврждения емайл при регистрации
        criteria = "auth_type='EMAIL_VALIDATION' and account_details_id=%s" % user["id"]
        auth_user = databases.db1.accounting.get_auths_criteria(criteria)[0]
        err_msg = "Из БД не получено записей о формировании хеша валидации емайла для user_id=%s"
        self.assertIsNotNone(auth_user, err_msg % user["id"])
        # Проверка статуса отправленного сообщения
        email_statuses = databases.db6.accounting.get_email_statuses_by_email(user["email"])[0]
        self.assertEqual(email_statuses["status_id"], 2, "Сообщение не доставлено на mail=%s" % user["email"])
        # Проверка отправленного сообщения и ссылки для завершения регистрации
        hash_value = auth_user["code_value"]
        emails = databases.db6.accounting.get_emails_by_hash(hash_value)[0]
        validate_path = self.URL_VALIDATE_EMAIL % hash_value
        url_validate = self.ENV_BASE_URL + validate_path
        url_validate_path = url_validate[url_validate.find('//')+2:]
        err_msg_url = "Полученный урл активации емайла %s не найден в теле отправленного письма id=%s"
        self.assertIn(url_validate_path, emails["body"], err_msg_url % (url_validate, emails["id"]))
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
        err_msg_url_1 = "Полученный урл активации емайла %s не найден в теле полученного письма id=%s"
        #self.assertEqual(mail_subject, 'OORRAA.com - активация аккаунта', "Тема письма: %s" % mail_subject)
        self.assertIn('noreply@oorraa.com', mail_from, "Почта отправителя: %s" % mail_from)
        self.assertIn(url_validate_path, mail_body, err_msg_url_1 % (url_validate, mail_body))
        # Проверка виджета продавца
        self.check_header_widget_seller_all(self.driver, user)
        # Проверка количества новых сообщений в мессенждере
        self.get_element_navigate(self.driver, self.check_main.COUNT_NEW_MSG % new_messages)
        # Чтение сообщений
        self.get_page(self.driver, self.path_chat.URL_CHAT)
        self.progress(self.driver)
        msg = self.reading_unread_messages_after_reg(self.driver, new_messages)
        self.assertEqual(msg, "Сообщения", "Остались непрочитанные %s" % msg)

        # Переход по ссылке валидации емайла
        self.get_page(self.driver, validate_path)
        url_web = self.driver.current_url.encode('utf-8')
        url_need = self.ENV_BASE_URL + self.path_reg.URL_VALIDATED_EMAIL
        err_msg = "Урл страницы успешной валидации емайла: %s не соответствует целевому урлу: %s"
        self.assertEqual(url_web, url_need, err_msg % (url_web, url_need))
        # Проверка, что из БД удален активационный хеш
        criteria = "auth_type='EMAIL_VALIDATION' and account_details_id=%s and creation_timestamp=%s"
        a_user = databases.db1.accounting.get_auths_criteria(criteria % (user["id"], auth_user["creation_timestamp"]))
        err_msg = "Из БД не удалена запись о формировании хеша валидации емайла для user_id=%s"
        self.assertEqual(a_user, list(), err_msg % user["id"])
        start_work = self.get_validated_email_success(self.driver)
        self.element_click(self.driver, start_work)

        # Проверка, что после нажатия на кнопку Начать работу произошел переход обратно на главную
        url_web = self.driver.current_url.encode('utf-8')
        err_msg = "Не произошел переход на главную страницу %s, пользователь остался на странице %s"
        self.assertEqual(url_web, url_main, err_msg % (url_main, url_web))
        # Проверка виджета продавца
        self.check_header_widget_seller_all(self.driver, user)

    @priority("High")
    def test_registration_by_email_incorrect_already_in_db(self):
        """
        Title: Я не могу зарегистрироваться по e-mail, если на этот e-mail уже регистрировались ранее.
        Description:
        * Отображается сообщение "Пользователь с указанным email-адресом уже зарегистрирован"
        """
        service_log.run(self)
        # Регистрация
        self.click_reg_and_auth(self.driver)
        reg_email = self.get_reg_email_form(self.driver)

        name = common_utils.random_string()
        stamp = str(time.time())
        email = 'oratest+%s@oorraa.com' % stamp
        password = AccountingMethods.get_default_password(5)

        crt = "id=%s" % AccountingMethods.get_default_user_id('seller')
        user = databases.db1.accounting.get_user_by_criteria_only(criteria=crt)[0]
        databases.db1.accounting.update_account_details_by_criteria(user["id"], "email='%s'" % email.lower())

        reg_email["name_input"].send_keys(name)
        reg_email["email_input"].send_keys(email)
        reg_email["password_input"].send_keys(password)
        self.click_button(reg_email["reg_btn"])
        self.get_element_navigate(self.driver, self.check_reg.E_ALREADY_REG_EMAIL)
        self.go_to_main_page(self.driver)
        self.check_header_widget_visitor(self.driver)

    @priority("High")
    def test_registration_by_email_incorrect_user_disabled(self):
        """
        Title: Я не могу зарегистрироваться по e-mail, если мой пользователь ранее был заблокирован (DISABLED)
        Description: Отображается соответствующее сообщение
        """
        service_log.run(self)
        # Регистрация
        self.click_reg_and_auth(self.driver)
        reg_email = self.get_reg_email_form(self.driver)

        name = common_utils.random_string()
        stamp = str(time.time())
        email = 'oratest+%s@oorraa.com' % stamp
        password = AccountingMethods.get_default_password(5)

        user = databases.db1.accounting.get_user_by_criteria(account_status="DISABLED", criteria="id is not NULL")[0]
        databases.db1.accounting.update_account_details_by_criteria(user["id"], "email='%s'" % email.lower())

        reg_email["name_input"].send_keys(name)
        reg_email["email_input"].send_keys(email)
        reg_email["password_input"].send_keys(password)
        self.click_button(reg_email["reg_btn"])
        self.get_element_navigate(self.driver, self.check_reg.E_ALREADY_REG_EMAIL)
        self.go_to_main_page(self.driver)
        self.check_header_widget_visitor(self.driver)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()



class RegistrationByEmailView(Navigate, HelpAuthCheckMethods, AuthCheckMethods, RegEmailCheckMethods):
    """
    Story: Форма регистрации по e-mail
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        cls.go_to_main_page(cls.driver)
        # Подготовка тестовых данных
        cls.name = common_utils.random_string()
        stamp = str(time.time())
        cls.email = 'oratest+%s@oorraa.com' % stamp
        cls.password = AccountingMethods.get_default_password(5)
        # Переход на страницу регистрации по емайл
        cls.click_reg_and_auth(cls.driver)
        cls.reg_email = cls.get_reg_email_form(cls.driver)
        service_log.preparing_env(cls)

    @priority("Medium")
    def test_registration_by_email_form_empty_password(self):
        """
        Title: Я не могу зарегистрироваться по e-mail, если не ввел пароль. Отобразится сообщение "Введите пароль"
        """
        service_log.run(self)
        self.reg_email["name_input"].send_keys(self.name)
        self.reg_email["email_input"].send_keys(self.email)
        self.click_button(self.reg_email["reg_btn"])
        self.get_element_navigate(self.driver, self.check_reg.E_PASSWORD_EMPTY)
        self.go_to_main_page(self.driver)
        self.check_header_widget_visitor(self.driver)

    @priority("Medium")
    def test_registration_by_email_form__empty_name(self):
        """
        Title: Я не могу зарегистрироваться по e-mail, если не ввел Имя. Отображается сообщение "Введите имя"
        """
        service_log.run(self)
        self.reg_email["email_input"].send_keys(self.email)
        self.reg_email["password_input"].send_keys(self.password)
        self.click_button(self.reg_email["reg_btn"])
        self.get_element_navigate(self.driver, self.check_reg.E_NAME_EMPTY)
        self.go_to_main_page(self.driver)
        self.check_header_widget_visitor(self.driver)

    @priority("Medium")
    def test_registration_by_email_form__empty_email(self):
        """
        Title: Я не могу зарегистрироваться по e-mail, если не ввел e-mail. Отображается сообщение "Введите e-mail"
        """
        service_log.run(self)
        self.reg_email["name_input"].send_keys(self.name)
        self.reg_email["password_input"].send_keys(self.password)
        self.click_button(self.reg_email["reg_btn"])
        self.get_element_navigate(self.driver, self.check_reg.E_EMAIL_EMPTY)
        self.go_to_main_page(self.driver)
        self.check_header_widget_visitor(self.driver)

    @skip('manual')
    @priority("Low")
    def test_registration_by_email_form__negative_checks(self):
        """
        Title: Валидация полей формы Регистрации: Email, Имя и Пароль: Негативные
        Description:
        По Таблице Сущностей проверить, для каждого КРАСНОГО :
            * невозможность создать данную уч. запись
            * выдачу соответствующего предупреждающего сообщения или невозможность ввода в поля данного значения
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_registration_by_email_form__positive_checks(self):
        """
        Title: Валидация полей формы Регистрации: Email, Имя и Пароль: Позитивные
        Description:
        По Таблице Сущностей проверить, для каждог ЗЕЛЕНОГО:
            * корректность создания и отображения пользователя в виджете "Профиль пользователя" в шапке
            * корректность создания и отображения пользователя на странице Настройки пользователя
            * корректность создания и отображения пользователя в бек-офисе
        * корректность сохранения в БД
        """
        pass

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()