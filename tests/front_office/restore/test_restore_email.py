# -*- coding: utf-8 -*-
"""
Feature: Восстановление пароля по email
"""

import time
from unittest import skip, expectedFailure
from support import service_log
from support.utils import common_utils
from support.utils.common_utils import generate_sha256, priority
from support.utils.db import databases
from tests.front_office.registration.classes.class_registration_email import RegEmailCheckMethods as RegEmail
from tests.front_office.authorization.classes.class_authorization import AuthCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods as Front
from support.utils.mail_api import Inbox


class TestRestorePasswordByEmailLogic(Navigate, AuthCheckMethods, Front, Inbox, RegEmail):
    """
    Story: Восстановление пароля по email
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

        cls.user = databases.db1.accounting.get_user_by_criteria_only("id=%s" % cls.default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"],
                                             salt=cls.user["salt"])

        # Устанавливаем новый пароль для пользователя
        cls.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(cls.default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)
        service_log.preparing_env(cls)

    @priority("Must")
    def test_restore_by_email_correct(self):
        """
        Title: Я могу восстановить пароль, введя свой e-mail, на который зарегистрирован аккаунт
        Description:
        1. Ввести корректный зарегистрированный номер e-mail в нажать "Выслать пароль"
            * отображается страница с информационным сообщением о том, что ссылка на сброс пароля высланы письмом
            * при нажатии на главную выполнен переход на главную страницу
            * на указанный e-mail отправлено письмо с сылкой на страницу смены пароля (кнопка "Сбросить пароль")
        2. Получив письмо, нажать на "Сбросить пароль"
            * выполнен переход на страницу сервиса \reset-password?token=
            [специально_сгенерированный_уникальный_токен_одноразового_перехоа_по_ссылке]
            * форма содержит поля "Эл. почта", "Пароль" и "Повторите пароль" и кнопку "Установить новый пароль"
            * поле "Эл. почта" заблокировано для изменения и содержит email аккаунта для которого восстанавливали пароль
        3. Ввести новый пароль на форме "Установить новый пароль" и подтверждение и нажать "Установить новый пароль":
            * отображается страница с сообщением, что новый пароль установлен и кнопкой "Начать работу"
            * в БД для пользователя записывается новый пароль = вводимому на предыдущем шаге (хеш пароля).
            * статус пользователя и другие данные (кроме пароля) не меняется
        4. Нажать "Начать работу"
            * Происходит успешный вход в систему под учетной записью, для которой восстанавливали пароль.
            * Проверить что под ней можно снова войти после  логаута из системы
        """
        service_log.run(self)
        self.email = self.get_new_email(databases.db1)
        databases.db1.accounting.update_account_details_by_criteria(self.default_user_id, "email='%s'" % self.email.lower())

        url_main = self.driver.current_url.encode('utf-8')
        self.get_page(self.driver, self.path_restore.URL_RESTORE_EMAIL)

        # Ввод емайл для восстановления пароля и клик Выслать пароль
        restore_form = self.get_restore_email_form(self.driver)
        restore_form["email_input"].send_keys(self.email)
        self.element_click(self.driver, restore_form["restore_btn"], change_page_url=False)

        # Проверка, что в БД появилась запись о письме и статус письма
        # Проверка что сформирован хеш для подтеврждения емайл при регистрации
        criteria = "auth_type='PASSWORD_CHANGE' and account_details_id=%s" % self.user["id"]
        auth_user = databases.db1.accounting.get_auths_criteria(criteria)[0]
        err_msg = "Из БД не получено записей о формировании хеша восстановления пароля по емайлу для user_id=%s"
        self.assertIsNotNone(auth_user, err_msg % self.user["id"])
        # Проверка статуса отправленного сообщения
        email_statuses = databases.db6.accounting.get_email_statuses_by_email(self.email.lower())[0]
        #self.assertEqual(email_statuses["status_id"], 2, "Сообщение не доставлено на mail=%s" % self.email)
        # Проверка отправленного сообщения и ссылки для завершения регистрации
        hash_value = auth_user["code_value"]
        emails = databases.db6.accounting.get_emails_by_hash(hash_value)[0]
        err_msg_1 = "Из БД не получено писем о восстановлении пароля с хешом=%s, для user_id=%s"
        self.assertIsNotNone(emails, err_msg_1 % (hash_value, self.user["id"]))
        restore_path = self.URL_RESTORE_EMAIL % hash_value
        url_validate = self.ENV_BASE_URL + restore_path
        url_validate_path = url_validate[url_validate.find('//')+2:]
        err_msg_url = "Полученный урл восстановления пароля по емайлу %s не найден в теле отправленного письма id=%s"
        self.assertIn(url_validate_path, emails["body"], err_msg_url % (url_validate, emails["id"]))

        # Проверка страницы На ваш эл. ящик выслано письмо
        email_sent_form = self.get_restore_email_sent_form(self.driver)
        self.element_click(self.driver, email_sent_form["to_main_btn"])
        # Проверка, что после нажатия на кнопку На главную произошел переход обратно на главную
        url_web = self.driver.current_url.encode('utf-8')
        err_msg = "Не произошел переход на главную страницу %s, пользователь остался на странице %s"
        self.assertEqual(url_web, url_main, err_msg % (url_main, url_web))
        self.get_element_navigate(self.driver, self.check_main.MAIN_MENU_HOME_ACTIVE)
        work = time.time()
        messages = None
        while time.time() - work < self.email_timeout:
            try:
                messages = self.get_email(to_email=self.email)
                self.assertNotEqual(len(messages), 0, "Не получено сообщение")
                break
            except Exception:
                pass
        self.assertIsNotNone(messages, "Не получено сообщение")
        message = messages[0]
        mail_from = message['From']
        mail_body = message['Body']
        err_msg_url_1 = "Полученный урл восстановления пароля по емайл %s не найден в теле полученного письма id=%s"
        #self.assertEqual(mail_subject, 'OORRAA.com - сброс пароля', "Тема письма: %s" % mail_subject)
        self.assertIn('noreply@oorraa.com', mail_from, "Почта отправителя: %s" % mail_from)
        self.assertIn(url_validate_path, mail_body, err_msg_url_1 % (url_validate, mail_body))

        # Переход по ссылке валидации емайла
        self.get_page(self.driver, restore_path)
        url_web = self.driver.current_url.encode('utf-8')
        err_msg = "Урл страницы ввода нового пароля из письма: %s не соответствует целевому урлу: %s"
        self.assertEqual(url_web, url_validate, err_msg % (url_web, url_validate))

        # Проверка формы ввода нового пароля и ввод
        input_pass_form = self.get_restore_email_input_pass_form(self.driver, self.email)
        new_password = common_utils.random_string()
        input_pass_form["password_input"].send_keys(new_password)
        input_pass_form["password_repeat_input"].send_keys(new_password)
        self.element_click(self.driver, input_pass_form["set_pass_btn"], change_page_url=False)

        # Проверка что хеш пароля изменился и статус пользователя не изменился
        user_new = databases.db1.accounting.get_user_by_criteria_only("id=%s" % self.default_user_id)[0]
        self.assertNotEqual(self.user['code_value'], user_new['code_value'], "Хеш нового пароля совпадает со старым")
        err = "Статус аккаунта пользователя изменился на %s"
        self.assertEqual(self.user['account_status'], user_new['account_status'], err % user_new['account_status'])

        # Проверка, что из БД удален активационный хеш
        crt = "auth_type='PASSWORD_CHANGE' and account_details_id=%s and creation_timestamp=%s"
        a_user = databases.db1.accounting.get_auths_criteria(crt % (self.user["id"], auth_user["creation_timestamp"]))
        err_msg = "Из БД не удалена запись о формировании хеша восстановления пароля для user_id=%s"
        self.assertEqual(a_user, list(), err_msg % self.user["id"])
        start_work = self.get_restore_password_by_email_success(self.driver)
        self.element_click(self.driver, start_work["start_work_btn"])
        time.sleep(self.time_sleep)
        # Проверка, что после нажатия на кнопку Начать работу произошел переход обратно на главную
        url_web = self.driver.current_url.encode('utf-8')
        err_msg = "Не произошел переход на главную страницу %s, пользователь остался на странице %s"
        self.assertEqual(url_web, url_main, err_msg % (url_main, url_web))
        self.get_element_navigate(self.driver, self.check_main.MAIN_MENU_HOME_ACTIVE)
        # Проверка виджета продавца
        self.check_header_widget_seller_all(self.driver, self.user)

        exit_btn = self.get_element_navigate(self.driver, self.click_main.MENU_PROFILE_EXIT)
        self.element_click(self.driver, exit_btn, change_page_url=False)

        # Проверка успешного логина с новым паролем
        self.go_authorization_page(self.driver)
        auth_form = self.get_auth_email_form(self.driver)
        auth_form["email_input"].send_keys(self.email)
        auth_form["password_input"].send_keys(new_password)
        self.element_click(self.driver, auth_form["login_btn"])
        time.sleep(self.time_sleep)
        self.check_header_widget_seller_all(self.driver, self.user)

    #TODO: https://jira.oorraa.net/browse/GO-1505
    @priority("Medium")
    @expectedFailure
    def test_restore_by_email_not_in_db(self):
        """
        Title: Я не могу восстановить пароль по e-mail, если его нет в системе. Отображается сообщение
        "Пользователь с таким email-адресом не зарегистрирован"
        """
        self.get_page(self.driver, self.path_restore.URL_RESTORE_EMAIL)
        restore_form = self.get_restore_email_form(self.driver)
        email = self.get_new_email(databases.db1)
        self.input_str(restore_form['email_input'], email)
        self.element_click(self.driver, restore_form['restore_btn'], change_page_url=False)
        self.element_is_present(self.driver, self.check_restore.ERR_EMAIL_OR_PASS)

    @priority("Medium")
    def test_restore_by_email_incorrect_user_disabled(self, status='DISABLED'):
        """
        Title: Я не могу восстановить пароль по e-mail, если мой пользователь заблокирован (Disabled)
        """
        service_log.run(self)
        self.go_authorization_page(self.driver)
        self.go_restore_page(self.driver)
        restore_form = self.get_restore_email_form(self.driver)
        user = databases.db1.accounting.get_not_enabled_user(status)[0]
        email = self.get_new_email(databases.db1)
        databases.db1.accounting.update_account_details_by_criteria(user["id"], "email='%s'" % email.lower())
        AccountingMethods.save_user_password(user_id=user["id"], hash_passwd=user["code_value"], salt=user["salt"])

        self.input_str(restore_form['email_input'], email)
        self.element_click(self.driver, restore_form['restore_btn'], change_page_url=False)

        user_new_info = databases.db1.accounting.get_data_accounts_by_user_id_and_status(user["id"], status)[0]

        msg_error1 = "ОШИБКА: Хеши паролей не совпадают. Пароль изменился"
        self.assertEqual(user["code_value"], user_new_info["code_value"], msg_error1)

        # сравниваем хеш нового и старого пароля
        msg_error2 = "ОШИБКА: Соль паролей не совпадает. Пароль изменился"
        self.assertEqual(user["salt"], user_new_info["salt"], msg_error2)

        self.check_message_error_by_status_user(self.driver, status)

    @priority("Medium")
    def test_restore_by_email_link_to_restore(self):
        """
        Title: Ссылка в письме на форму "Установите новый пароль" одноразовая.
        Description:
        * Если попытаться пройти по ней во второй раз, отображается сообщение "Истек срок действия активационной ссылки,
         повторите активацию еще раз"
        """
        service_log.run(self)
        self.email = self.get_new_email(databases.db1)
        databases.db1.accounting.update_account_details_by_criteria(self.default_user_id, "email='%s'" % self.email.lower())

        url_main = self.driver.current_url.encode('utf-8')
        self.get_page(self.driver, self.path_restore.URL_RESTORE_EMAIL)

        # Ввод емайл для восстановления пароля и клик Выслать пароль
        restore_form = self.get_restore_email_form(self.driver)
        restore_form["email_input"].send_keys(self.email)
        self.element_click(self.driver, restore_form["restore_btn"], change_page_url=False)
        time.sleep(self.time_sleep)
        # Проверка, что в БД появилась запись о письме и статус письма
        # Проверка что сформирован хеш для подтеврждения емайл при регистрации
        criteria = "auth_type='PASSWORD_CHANGE' and account_details_id=%s" % self.user["id"]
        auth_user = databases.db1.accounting.get_auths_criteria(criteria)[0]
        err_msg = "Из БД не получено записей о формировании хеша восстановления пароля по емайлу для user_id=%s"
        self.assertIsNotNone(auth_user, err_msg % self.user["id"])
        # Проверка статуса отправленного сообщения
        email_statuses = databases.db6.accounting.get_email_statuses_by_email(self.email.lower())[0]
        #self.assertEqual(email_statuses["status_id"], 2, "Сообщение не доставлено на mail=%s" % self.email)
        # Проверка отправленного сообщения и ссылки для завершения регистрации
        hash_value = auth_user["code_value"]
        emails = databases.db6.accounting.get_emails_by_hash(hash_value)[0]
        err_msg_1 = "Из БД не получено писем о восстановлении пароля с хешом=%s, для user_id=%s"
        self.assertIsNotNone(emails, err_msg_1 % (hash_value, self.user["id"]))
        restore_path = self.URL_RESTORE_EMAIL % hash_value
        url_validate = self.ENV_BASE_URL + restore_path

        # Переход по ссылке валидации емайла
        self.get_page(self.driver, restore_path)
        url_web = self.driver.current_url.encode('utf-8')
        err_msg = "Урл страницы ввода нового пароля из письма: %s не соответствует целевому урлу: %s"
        self.assertEqual(url_web, url_validate, err_msg % (url_web, url_validate))

        self.get_restore_email_input_pass_form(self.driver, self.email)
        # Проверка формы ввода нового пароля и ввод
        input_pass_form = self.get_restore_email_input_pass_form(self.driver, self.email)
        new_password = common_utils.random_string()
        input_pass_form["password_input"].send_keys(new_password)
        input_pass_form["password_repeat_input"].send_keys(new_password)
        self.element_click(self.driver, input_pass_form["set_pass_btn"], change_page_url=False)
        self.driver.delete_all_cookies()
        # Повторный переход по ссылке валидации емайла
        self.get_page(self.driver, restore_path)
        self.element_is_present(self.driver, self.check_restore.ERR_VALIDATE_URL)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class TestRestorePasswordByEmailForm(Navigate, AuthCheckMethods, Front, Inbox, RegEmail):
    """
    Story: Форма восстановления пароля по e-mail
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

    @priority("Medium")
    def test_restore_by_email_form_empty_email(self):
        """
        Title: Если не введен e-mail, отображается сообщение "Введите e-mail"
        """
        self.get_page(self.driver, self.path_restore.URL_RESTORE_EMAIL)
        # клик Выслать пароль
        restore_form = self.get_restore_email_form(self.driver)
        self.element_click(self.driver, restore_form["restore_btn"], change_page_url=False)
        self.element_is_present(self.driver, self.check_restore.E_EMAIL_EMPTY)

    @skip('manual')
    @priority("Medium")
    def test_restore_by_email_form_invalid_email(self, password):
        """
        Title: Если введеный e-mail не попадает под маску. Отображается сообщение  "Неверный формат email"
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_restore_by_email_form_empty_password(self, password):
        """
        Title: Если на форме "Установите новый пароль" не ввести новый пароль,  отображается сообщение "Введите пароль"
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_restore_by_email_form_empty_confirm_password(self, password):
        """
        Title: Если на форме "Установите новый пароль" не ввести подтверждение пароля, отображается сообщение
        "Введите подтверждение пароля"
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_restore_by_email_form_password_mismatch(self, password):
        """
        Title: Если на форме "Установите новый пароль" ввести разные пароли в пароль и подтверждение пароль,
        отображается сообщение "Пароли не совпадают"
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()