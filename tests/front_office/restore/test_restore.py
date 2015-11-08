# -*- coding: utf-8 -*-
"""
Feature: Восстановление пароля по номеру телефона
"""
import random
import time
from unittest import skip, expectedFailure
from ddt import ddt, data
from support import service_log
from support.utils.common_utils import generate_sha256, priority
from support.utils.db import databases
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.registration.classes.class_registration import HelpRegCheckMethods as Registration
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods


@ddt
class TestRestorePasswordByPhone(HelpAuthCheckMethods, HelpLifeCycleCheckMethods, Navigate, Registration):
    """
    Story: Восстановление пароля по номеру телефона
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

    @priority("Must")
    def test_restorePassword_by_phone_correct(self):
        """
        Title: Я могу восстановить пароль, введя свой номер телефона, на который зарегистрирован аккаунт
        Description:
        1. Ввести корректный зарегистрированный номер моб. телефона в нажать "Выслать пароль"
            * отображается уведомление об отправке пароля на моб. телефон по смс
            * поле "Моб. телефон" становится недоступнынм для редактирования
            * пропадает кнопка "Выслать пароль"
            * появляется кнопка "Войти"
            * есть текст "Пароль отправлен на указанный номер. Введите его в течение 5 минут"
            * есть кнопка "Не приходит пароль?"
            * в БД для пользователя записывается новый пароль, состоящий из 5и чисел (хеш пароля).
            Он отличается от изначального.
            * на введенный моб. телефон приходит сгенерированный пароль, состоящий из 5и чисел.
            Он отличается от изначального.
            * статус пользователя и другие данные (кроме пароля) не меняется
        2. Ввести полученный пароль и нажать "Войти":
            * Происходит успешный вход в систему под учетной записью, для которой восстанавливали пароль.
            * Проверить что под ней можно снова войти после логаута из системы
        """
        service_log.run(self)
        self.go_authorization_page(self.driver)
        self.go_restore_page(self.driver)
        self.click_to_phone(self.driver)

        phone, sent_passwd_button = self.get_data_restore(self.driver)

        user = databases.db1.accounting.get_for_restore()[0]
        AccountingMethods.save_user_password(user_id=user["id"], hash_passwd=user["code_value"], salt=user["salt"])

        # вводим номер телефона
        phone.send_keys(user["phone"][1:])
        self.click_button(sent_passwd_button)
        self.check_password_is_sent(self.driver)

        pass_input = self.get_pass_input(self.driver)
        submit_button = self.get_login(self.driver)

        self.check_form_sent_passwd(self.get_form_note(self.driver))
        data = databases.db1.accounting.get_sms(phone=user["phone"])[0]
        self.check_sms_status(data)
        user_new_info = databases.db1.accounting.get_data_accounts_by_user_id_and_status(user["id"])[0]

        msg_error1 = "ОШИБКА: Хеши паролей совпадают. Пароль не изменился"
        self.assertNotEqual(user["code_value"], user_new_info["code_value"], msg_error1)

        # сравниваем хеш нового и старого пароля
        msg_error2 = "ОШИБКА: Соль паролей совпадает. Пароль не изменился"
        self.assertNotEqual(user["salt"], user_new_info["salt"], msg_error2)

        # сравниваем соль нового и старого пароля
        newPass = data["message"][-5:]

        new_pass_hash = generate_sha256(newPass, user_new_info["salt"])

        msg_error3 = "ОШИБКА: Новый хеш пароля из базы не совпадает с сгенерированным хешом. " \
                     "Возможно из логов получен неверный пароль."

        self.assertEqual(user_new_info["code_value"], new_pass_hash, msg_error3)

        pass_input.send_keys(newPass)

        Navigate.element_click(self.driver, submit_button, change_page_url=True)
        self.set_text_xpath_by_menu(user["display_name"])

    @priority("Medium")
    def test_restorePassword_by_phone_incorrect_password(self):
        """
        Title: Я не могу войти в систему, если некорректно введу полученный при восстановлении по телефону пароль.
        Description:
            * Отобразится сообщение "Пароль неверен"
        """
        service_log.run(self)
        password = ['incorrect pass', '123']
        self.go_authorization_page(self.driver)
        self.go_restore_page(self.driver)
        self.click_to_phone(self.driver)

        phone, sent_passwd_button = self.get_data_restore(self.driver)
        user = databases.db1.accounting.get_users_with_status()[0]
        AccountingMethods.save_user_password(user_id=user["id"], hash_passwd=user["code_value"], salt=user["salt"])
        default_new_passwd = AccountingMethods.get_default_password(4)
        override_passwd_hash = generate_sha256(default_new_passwd, user["salt"])
        databases.db1.accounting.update_passwd_hash_by_phone(passwd_hash=override_passwd_hash, phone=user["phone"])

        # вводим номер телефона
        phone.send_keys(user["phone"][1:])
        self.click_button(sent_passwd_button)
        self.check_password_is_sent(self.driver)

        pass_input = self.get_pass_input(self.driver)
        submit_button = self.get_login(self.driver)

        self.check_form_sent_passwd(self.get_form_note(self.driver))

        pass_input.send_keys(password[1])
        self.click_button(submit_button)

        time.sleep(1)
        self.check_incorrect_passwd_or_phone(self.driver)

    @priority("Medium")
    def test_restorePassword_by_phone_phone_not_in_db(self):
        """
        Title: Я не могу восстановить пароль по номеру телефона, если его нет в системе.
        Description:
            * Отображается сообщение "Проверьте правильность ввода номера телефона"
        """
        service_log.run(self)
        self.get_page(self.driver, self.path_restore.URL_RESTORE_PHONE)
        phone, sent_passwd_button = self.get_data_restore(self.driver)
        phone_num = self.get_new_phone(databases.db1)
        self.assertIsNotNone(phone, "Не получен новый номер телефона")
        input_phone = phone_num[1:]
        self.input_str(phone, input_phone)
        self.element_click(self.driver, sent_passwd_button, change_page_url=False)
        self.element_is_present(self.driver, self.check_restore.ERR_PHONE_OR_PASS)

    @priority("Medium")
    def test_restorePassword_by_phone_incorrect_user_disabled(self, status='DISABLED'):
        """
        Title: Я не могу восстановить пароль по номеру телефона, если мой пользователь заблокирован (Disabled)
        Description:
            * Отображается соответствующее сообщение
        """
        service_log.run(self)
        self.go_authorization_page(self.driver)
        self.go_restore_page(self.driver)
        self.click_to_phone(self.driver)
        phone, sent_passwd_button = self.get_data_restore(self.driver)
        user = databases.db1.accounting.get_not_enabled_user(status)[0]
        AccountingMethods.save_user_password(user_id=user["id"], hash_passwd=user["code_value"], salt=user["salt"])

        phone.send_keys(user["phone"][1:])
        self.click_button(sent_passwd_button, sleep=0.5)

        user_new_info = databases.db1.accounting.get_data_accounts_by_user_id_and_status(user["id"], status)[0]

        msg_error1 = "ОШИБКА: Хеши паролей не совпадают. Пароль изменился"
        self.assertEqual(user["code_value"], user_new_info["code_value"], msg_error1)

        # сравниваем хеш нового и старого пароля
        msg_error2 = "ОШИБКА: Соль паролей не совпадает. Пароль изменился"
        self.assertEqual(user["salt"], user_new_info["salt"], msg_error2)

        self.check_message_error_by_status_user(self.driver, status)

    @priority("Medium")
    def test_restorePassword_by_phone_incorrect_user_wait_for_registration(self, status='WAIT_FOR_REGISTRATION'):
        """
        Title: Я не могу восстановить пароль по номеру телефона, если мой пользователь не окончил регистрацию
        в прошлый раз (WAIT_FOR_REGISTRATION)
        Description:
        * Отображается сообщение "Вы не закончили регистрацию"
        """
        service_log.run(self)
        self.go_authorization_page(self.driver)
        self.go_restore_page(self.driver)
        self.click_to_phone(self.driver)
        phone, sent_passwd_button = self.get_data_restore(self.driver)
        user = databases.db1.accounting.get_not_enabled_user(status)[0]
        AccountingMethods.save_user_password(user_id=user["id"], hash_passwd=user["code_value"], salt=user["salt"])

        phone.send_keys(user["phone"][1:])
        self.click_button(sent_passwd_button, sleep=0.5)

        user_new_info = databases.db1.accounting.get_data_accounts_by_user_id_and_status(user["id"], status)[0]

        msg_error1 = "ОШИБКА: Хеши паролей не совпадают. Пароль изменился"
        self.assertEqual(user["code_value"], user_new_info["code_value"], msg_error1)

        # сравниваем хеш нового и старого пароля
        msg_error2 = "ОШИБКА: Соль паролей не совпадает. Пароль изменился"
        self.assertEqual(user["salt"], user_new_info["salt"], msg_error2)

        self.check_message_error_by_status_user(self.driver, status)

    @skip('manual')
    @priority("Medium")
    def test_restorePassword_by_phone_check_sms_language(self):
        """
        Title: Смс с паролем приходит на том языке, на котором выполняется процесс восстановления пароля
        Description: Тексты:

        "Mật khẩu truy cập dịch vụ của bạn ${SITE_URL} — ${PASSWORD}"
        "Mật khẩu truy cập dịch vụ mới của bạn ${SITE_URL} — ${PASSWORD}"

        "服务密码 ${SITE_URL} — ${PASSWORD}"
        "新的服务密码 ${SITE_URL} — ${PASSWORD}"

        "Your password for ${SITE_URL} — ${PASSWORD}"
        "Your new password for ${SITE_URL} — ${PASSWORD}"

        "Ваш пароль для ${SITE_URL} — ${PASSWORD}"
        "Ваш новый пароль для ${SITE_URL} — ${PASSWORD}"
        """
        pass

    @priority("High")
    def test_restorePassword_by_phone_resend_password(self):
        """
        Title: Я могу запросить Повторную отправку пароля, при восстановлении пароля по телефону
        Description:
            * Отображается соответствующее сообщение
        """
        service_log.run(self)
        self.go_authorization_page(self.driver)
        self.go_restore_page(self.driver)
        self.click_to_phone(self.driver)
        phone, sent_passwd_button = self.get_data_restore(self.driver)
        user = databases.db1.accounting.get_for_restore()[0]
        AccountingMethods.save_user_password(user_id=user["id"], hash_passwd=user["code_value"], salt=user["salt"])

        phone.send_keys(user["phone"][1:])
        self.click_button(sent_passwd_button)
        self.check_password_is_sent(self.driver)
        self.check_form_sent_passwd(self.get_form_note(self.driver))
        data1 = databases.db1.accounting.get_sms(phone=user["phone"])[0]
        self.check_sms_status(data1)


        not_get_passwd = self.get_message_have_not_receiver_passwd(self.driver)
        self.click_button(not_get_passwd)
        self.check_instruction_not_receiver_passwd(self.driver)
        self.click_button(self.get_repeat_send_passwd(self.driver))

        data2 = databases.db1.accounting.get_sms(phone=user["phone"])[0]
        self.check_sms_status(data2)
        new_passwd1 = data1["message"][-5:]
        new_passwd2 = data2["message"][-5:]
        msg_error = "ОШИБКА: Первый высланный пароль совпадает с повторно высланным паролем"
        self.assertNotEqual(new_passwd1, new_passwd2, msg_error)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestRestorePasswordByPhoneForm(HelpAuthCheckMethods, HelpLifeCycleCheckMethods, Navigate):
    """
    Story: Форма восстановления пароля по телефону
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

    @priority("Medium")
    def test_restorePassword_by_phone_form_empty_phone(self):
        """
        Title: Если не введен телефон, отображается сообщение "Введите телефон"
        """
        service_log.run(self)
        self.get_page(self.driver, self.path_restore.URL_RESTORE_PHONE)
        phone, sent_passwd_button = self.get_data_restore(self.driver)
        self.element_click(self.driver, sent_passwd_button, change_page_url=False)
        self.element_is_present(self.driver, self.check_restore.ERR_NEED_PHONE)

    @priority("Medium")
    def test_restorePassword_by_phone_form_empty_password(self):
        """
        Title: Если не введен пришедший по смс пароль. Отображается сообщение "Введите пароль"
        """
        service_log.run(self)
        password = ['empty pass', '']
        self.go_authorization_page(self.driver)
        self.go_restore_page(self.driver)
        self.click_to_phone(self.driver)

        phone, sent_passwd_button = self.get_data_restore(self.driver)
        user = databases.db1.accounting.get_users_with_status()[0]
        AccountingMethods.save_user_password(user_id=user["id"], hash_passwd=user["code_value"], salt=user["salt"])
        default_new_passwd = AccountingMethods.get_default_password(4)
        override_passwd_hash = generate_sha256(default_new_passwd, user["salt"])
        databases.db1.accounting.update_passwd_hash_by_phone(passwd_hash=override_passwd_hash, phone=user["phone"])

        # вводим номер телефона
        phone.send_keys(user["phone"][1:])
        self.click_button(sent_passwd_button)
        self.check_password_is_sent(self.driver)

        pass_input = self.get_pass_input(self.driver)
        submit_button = self.get_login(self.driver)

        self.check_form_sent_passwd(self.get_form_note(self.driver))

        pass_input.send_keys(password[1])
        submit_button.click()

        time.sleep(1)
        self.check_need_password(self.driver)

    @skip('manual')
    @priority("Medium")
    def test_restorePassword_by_phone_form_negative_checks_1(self, phone_number='ttt'):
        """
        Title: Поле ввода телефона не принимает никаких символов кроме чисел.
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_restorePassword_by_phone_form_negative_checks_2(self):
        """
        Title: Поле ввода телефона не принимает никаких символов кроме чисел.
        Не принимает: буквы, символы, знаки препинания, пробелы
        """
        pass

    @priority("Low")
    def test_pageRestorePassword_by_phone_form_check_view(self):
        """
        Title: Тест проверяет внешний вид страницы "Забыли пароль"
        """
        service_log.run(self)
        self.get_page(self.driver, self.path_restore.URL_RESTORE_PHONE)
        self.check_restore_page(self.driver)
        self.check_page_restore_password(self.driver)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()