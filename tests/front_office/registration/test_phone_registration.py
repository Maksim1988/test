# -*- coding: utf-8 -*-
"""
Feature: Регистрация по номеру телефона
"""
import random
from unittest import skip
from ddt import ddt, data
from support import service_log
from support.utils.common_utils import generate_sha256, run_on_prod, priority
from support.utils.db import databases
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.authorization.classes.class_authorization import AuthCheckMethods as Auth
from tests.front_office.registration.classes.class_registration import HelpRegCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate


class TestRegistrationByPhoneLogic(HelpRegCheckMethods, HelpAuthCheckMethods, HelpLifeCycleCheckMethods, Auth, Navigate):
    """
    Story: Регистрация по номеру телефона
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

    def write_passwd_and_click_button(self, passwd):
        """ Вводим пароль и нажимаем кнопку "ок".
        :param passwd: пароль
        """
        pass_form = self.get_name_pass(self.driver)
        pass_form.send_keys(passwd)

    def click_buyer(self):
        """ Пробуем нажать на кнопки на странице (Покупатель, продавец).
        """
        buyer_button = self.get_radio_set_byuer(self.driver)
        seller_button = self.get_radio_set_seller(self.driver)
        self.click_button(seller_button, sleep=0.1)
        self.click_button(buyer_button, sleep=0.1)

    def click_seller(self):
        """ Пробуем нажать на кнопки на странице (покупатель, Продавец).
        """
        buyer_button = self.get_radio_set_byuer(self.driver)
        seller_button = self.get_radio_set_seller(self.driver)
        self.click_button(buyer_button, sleep=0.1)
        self.click_button(seller_button, sleep=0.1)

    def check_page_registration_after_add_passwd(self, user_id, name, phone):
        """ Восстановить пароль пользователя.
        Восстанавливаем пароль и проверяем, страница остаётся такой же.
        :param user_id: идентификатор пользователя
        :param name: имя пользователя
        :param phone: номер телефона
        """
        self.check_disable_fields_by_registration_page(self.driver)
        # Проверка регистрации
        result_data_user = databases.db1.accounting.get_data_user_by_id(user_id)
        roles_user = databases.db1.accounting.get_roles_by_id(user_id)
        self.assertEqual(result_data_user[0]["phone"], "7" + phone)
        self.assertEqual(result_data_user[0]["display_name"], name)
        self.assertEqual(result_data_user[0]["login"], "id%s" % user_id)
        msg_status = u'Seller successful registration with activated promo code'
        self.assertEqual(result_data_user[0]["account_status"], 'WAIT_FOR_REGISTRATION', msg_status)
        self.check_license_option(self.driver)

    def check_count_roles_and_status(self, user_id, count_roles=1, roles=None):
        result_data_user = databases.db1.accounting.get_data_user_by_id(user_id)
        roles_user = databases.db1.accounting.get_roles_by_id(user_id)
        # проверка роли пользователя
        self.assertEqual(len(roles_user), count_roles, "ОШИБКА: У пользователя не совпало количество ролей")
        for role_user in roles_user:
            self.assertIn(str(role_user["permission_id"]), roles, "Проверка роли неуспешна.")
        self.assertEqual(result_data_user[0]["account_status"], 'ENABLED')

    def count_recover_passwd(self, name):
        """ Возвращаем количество раз запуска восстановление пароля для пользователя.
        Warning: Нумерация с нуля.
        :param name: тестовое наименование
        :return: количество запусков
        """
        return self.COUNT_RECOVER_PASSWD[name]

    @priority("Must")
    def test_registration_by_phone_correct(self):
        """
        Title: Я могу зарегистрироваться по номеру телефона
        Description:
        1. Заполнить первый этап регистрации, указав имя и корректный мобильный номер и нажав "Выслать пароль"
            * кнопка "Выслать пароль" исчезает со страницы
            * выбор способа регистрации (по email \  телефону) исчезает
            * поле "Моб. телефон" и "Имя Пользователя" становится недоступнынм для редактирования
            * появляется поле "Пароль"
            * появляется кнопка "Зарегистрироваться"
            * появляется кнопка "Не приходит пароль"
            * отображается текст "Пароль отправлен на указанный номер. Введите его в течение 5 минут"
            * на введенный моб. телефон приходит сгенерированный пароль, состоящий из 5и чисел. Проверить,
            что в базу так же записан хеш пароля.
            * в базу сохранен новый пользователь. Статус пользователя: "Ждет активации"
        3. Нажать кнопку "Зарегистрироваться"
            * Произошел вход в систему под созданной учетной записью, в  профиле (справа-сверху) корректно отображается
            имя пользователя в соответствии с созданным
            * на странице настроек профиля  корректно отображается информация в соответствии с введеным при регистрации
            * В БД проверить, что создалась запись с заполненными в соответствии с созданным полями и проверить что
            данная запись имеет правильную роль
            * Проверить наличие иконки двух сообщений в мессенджере.
        """
        service_log.run(self)
        type_user_name = 'VALID'
        telephone = str(random.randrange(1000000000, 7007777777, 1))

        # Переходим на страницу авторизации и далее на страницу регистрации
        self.go_authorization_page(self.driver)
        self.go_registration_page(self.driver)
        self.click_to_phone(self.driver)

        obj_phone, obj_username, obj_submit_button = self.get_data_registration(self.driver)

        # Вводим имя пользователя, номер телефона и регистрируемся
        user_name = self.get_user_name(type_user_name)
        obj_username.send_keys(user_name)
        obj_phone.send_keys(telephone)
        self.click_button(obj_submit_button)

        # проверемя сообщение об успешной высылке пароля на регистрацию
        self.check_form_sent_passwd(self.get_form_note_passwd(self.driver))

        # Находим пользователя по номеру телефона, проверемям что пароль, соль, телефон соответствуют требованиям
        info_user = databases.db1.accounting.get_data_user_by_phone('7' + telephone)
        self.check_correct_writing_phone_salt_passwd(info_user)
        info_user = info_user[0]  # телефон пользователя уникален, берём единственную запись, что бы не таскать список

        # Запоминаем исходный пароль пользователя и генерируем новый
        AccountingMethods.save_user_password(info_user["id"], info_user["code_value"], info_user["salt"])

        # генерируем новый пароль и подменяем на него
        default_new_passwd = AccountingMethods.get_default_password(4)
        hash_res_new = generate_sha256(default_new_passwd, info_user["salt"])
        databases.db1.accounting.update_user_password(info_user["id"], hash_res_new)
        databases.db1.accounting.update_user_salt(info_user["id"], info_user["salt"])

        # вводим пароль
        self.write_passwd_and_click_button(default_new_passwd)

        # восстанавливаем пароль и указываем тип аккаунта = продавец
        self.check_page_registration_after_add_passwd(user_id=info_user["id"], name=user_name, phone=telephone)

        Navigate.element_click(self.driver, self.get_reg_submit_not_disable(self.driver), change_page_url=True)
        self.check_count_roles_and_status(user_id=info_user["id"], count_roles=2, roles='1,2')

        # проверка, что зарегистрированный юзер залогинен
        self.check_menu_profile_widget_total(self.driver, info_user["display_name"])
        self.check_menu_profile_widget_my_shop(self.driver)
        self.user_profile_menu(self.driver, info_user)

    @priority("High")
    def test_registration_by_phone_incorrect_password(self):
        """
        Title: Я не могу зарегистрироваться, если некорректно введу полученный пароль.
        Отобразится сообщение "Пароль неверен"
        """
        service_log.run(self)
        user_name = 'Vasya vvedet parol 6 simvolov'
        login = str(random.randrange(1000000000, 7007777777, 1))
        self.get_page(self.driver, self.path_reg.URL_REG)
        self.click_to_phone(self.driver)
        obj_phone, obj_username, obj_submit_button = self.get_data_registration(self.driver)

        # Вводим имя пользователя, пароль
        obj_username.send_keys(user_name)
        obj_phone.send_keys(login)
        self.click_button(obj_submit_button)

        info_user = databases.db1.accounting.get_data_user_by_phone('7' + login)[0]  # salt
        password_field = self.get_name_pass(self.driver)  # password
        AccountingMethods.save_user_password(info_user["id"], info_user["code_value"], info_user["salt"])

        # генерируем новый пароль и подменяем на него
        password = AccountingMethods.get_default_password(5)
        hash_res_new = generate_sha256(password, info_user["salt"])
        databases.db1.accounting.update_user_password(info_user["id"], hash_res_new)
        databases.db1.accounting.update_user_salt(info_user["id"], info_user["salt"])

        # вставляем пароль и пробуем зарегистрироваться
        password_field.send_keys(password)
        ok_button = self.get_submit_ok(self.driver)
        self.click_button(ok_button)
        self.check_not_right_password(self.driver)

    @priority("High")
    def test_registration_by_phone_incorrect_already_in_db(self):
        """
        Title: Я не могу зарегистрироваться по номеру телефона, если на этот телефон уже регистрировались ранее
        Description:
        * Отображается сообщение "Пользователь с указанным телефоном уже зарегистрирован"
        """
        service_log.run(self)
        # Ищем зарегистрированного пользователя
        status_user = 'ENABLED'
        type_user_name = 'VALID'
        user_info = databases.db1.accounting.get_users_with_status(status=status_user)[0]

        # Переходим на страницу авторизации и далее на страницу регистрации
        self.get_page(self.driver, self.path_reg.URL_REG)
        self.click_to_phone(self.driver)

        obj_phone, obj_username, obj_submit_button = self.get_data_registration(self.driver)

        # Вводим имя пользователя, номер телефона и регистрируемся
        user_name = self.get_user_name(type_user_name)
        obj_username.send_keys(user_name)
        obj_phone.send_keys(user_info["phone"][1:])
        self.click_button(obj_submit_button)
        self.check_msg_user_exist(self.driver)

    @priority("High")
    def test_registration_by_phone_correct_user_wait_for_registration(self):
        """
        Title: Я могу зарегистрироваться по номеру телефона, если мой пользователь не окончил регистрацию в прошлый раз
        (WAIT_FOR_REGISTRATION)
        """
        service_log.run(self)
        type_user_name = 'VALID'
        telephone = str(random.randrange(1000000000, 7577777777, 1))

        # Переходим на страницу авторизации и далее на страницу регистрации
        self.get_page(self.driver, self.path_reg.URL_REG)
        self.click_to_phone(self.driver)

        obj_phone, obj_username, obj_submit_button = self.get_data_registration(self.driver)

        # Вводим имя пользователя, номер телефона и регистрируемся
        user_name = self.get_user_name(type_user_name)
        obj_username.send_keys(user_name)
        obj_phone.send_keys(telephone)
        self.click_button(obj_submit_button)

        # проверемя сообщение об успешной высылке пароля на регистрацию
        self.check_form_sent_passwd(self.get_form_note_passwd(self.driver))

        # Находим пользователя по номеру телефона, проверемям что пароль, соль, телефон соответствуют требованиям
        info_user = databases.db1.accounting.get_data_user_by_phone('7' + telephone)
        self.check_correct_writing_phone_salt_passwd(info_user)
        info_user = info_user[0]  # телефон пользователя уникален, берём единственную запись, что бы не таскать список

        # Запоминаем исходный пароль пользователя и генерируем новый
        AccountingMethods.save_user_password(info_user["id"], info_user["code_value"], info_user["salt"])

        # генерируем новый пароль и подменяем на него
        default_new_passwd = AccountingMethods.get_default_password(4)
        hash_res_new = generate_sha256(default_new_passwd, info_user["salt"])
        databases.db1.accounting.update_user_password(info_user["id"], hash_res_new)
        databases.db1.accounting.update_user_salt(info_user["id"], info_user["salt"])

        # вводим пароль
        self.write_passwd_and_click_button(default_new_passwd)

        # восстанавливаем пароль и указываем тип аккаунта = покупатель
        self.check_page_registration_after_add_passwd(user_id=info_user["id"], name=user_name, phone=telephone)

        # Зарегистрировали пользователя, статус пользователя = WAIT_FOR_REGISTRATION
        # Регестрируем пользователя с тем же номером телефона

        # Переходим на страницу авторизации и далее на страницу регистрации
        self.get_page(self.driver, self.path_reg.URL_REG)
        self.click_to_phone(self.driver)

        obj_phone, obj_username, obj_submit_button = self.get_data_registration(self.driver)

        # Вводим имя пользователя, номер телефона и регистрируемся
        user_name = self.get_user_name(type_user_name)
        obj_username.send_keys(user_name)
        obj_phone.send_keys(telephone)
        self.click_button(obj_submit_button)

        # проверемя сообщение об успешной высылке пароля на регистрацию
        self.check_form_sent_passwd(self.get_form_note_passwd(self.driver))

        # Находим пользователя по номеру телефона, проверемям что пароль, соль, телефон соответствуют требованиям
        info_user = databases.db1.accounting.get_data_user_by_phone('7' + telephone)
        self.check_correct_writing_phone_salt_passwd(info_user)
        info_user = info_user[0]  # телефон пользователя уникален, берём единственную запись, что бы не таскать список

        # Запоминаем исходный пароль пользователя и генерируем новый
        AccountingMethods.save_user_password(info_user["id"], info_user["code_value"], info_user["salt"])

        # генерируем новый пароль и подменяем на него
        default_new_passwd = AccountingMethods.get_default_password(4)
        hash_res_new = generate_sha256(default_new_passwd, info_user["salt"])
        databases.db1.accounting.update_user_password(info_user["id"], hash_res_new)
        databases.db1.accounting.update_user_salt(info_user["id"], info_user["salt"])

        # вводим пароль
        self.write_passwd_and_click_button(default_new_passwd)

        # восстанавливаем пароль и указываем тип аккаунта = покупатель
        self.check_page_registration_after_add_passwd(user_id=info_user["id"], name=user_name, phone=telephone)

        # Нажимаем создать аккаунт
        Navigate.element_click(self.driver, self.get_reg_submit_not_disable(self.driver))
        self.check_count_roles_and_status(user_id=info_user["id"], count_roles=2, roles='1,2')

        # проверка, что зарегистрированный юзер залогинен
        self.check_profile_widget(self.driver)
        self.user_profile_menu(self.driver, info_user)

    @priority("Medium")
    def test_registration_by_phone_incorrect_user_disabled(self):
        """
        Title: Я не могу зарегистрироваться по номеру телефона, если мой пользователь ранее был заблокирован (DISABLED)
        Description:
        * Отображается соответствующее сообщение
        """
        service_log.run(self)
        # Ищем заблокированного пользователя
        status_user = 'DISABLED'
        type_user_name = 'VALID'
        user_info = databases.db1.accounting.get_users_with_status(status=status_user)[0]

        # Переходим на страницу авторизации и далее на страницу регистрации
        self.get_page(self.driver, self.path_reg.URL_REG)
        self.click_to_phone(self.driver)

        obj_phone, obj_username, obj_submit_button = self.get_data_registration(self.driver)

        # Вводим имя пользователя, номер телефона и регистрируемся
        user_name = self.get_user_name(type_user_name)
        obj_username.send_keys(user_name)
        obj_phone.send_keys(user_info["phone"][1:])
        self.click_button(obj_submit_button)
        self.check_msg_user_exist(self.driver)

    @skip('manual')
    @priority("Must")
    def test_registration_by_phone_resend_password(self):
        """
        Title: Я могу запросить Повторную отправку пароля, при регистрации по телефону
        Description:
        1. Проверить, что при нажатии на "Не приходит пароль":
            * кнопка "не приходит пароль" исчезает
            * отображаются информационные тексты
            * есть счетчик обратного отсчета
            * по окончании отсчета счетчика появляется кнопка "Отправить пароль повторно"
            * Поля "Имя" и "Телефон" залочены для изменения
            * Поле "Пароль" активно для ввода
        2. Нажать на "Отправить пароль повторно"
            * отображается текст "Пароль отправлен"
            * в базу сохранен новый пользователь, отправленный ему пароль. Статус пользователя: "Ждет активации"
        3. Ввести старый пароль и нажать "Ок"
            * Отображается текст "Пароль неверен"
        4. Вести новый полученный пароль и завершить процесс регистрации:
            * Произошел вход в систему под созданной учетной записью, в  профиле (справа-сверху) корректно отображается
            имя пользователя в соответствии с созданным
            * на странице настроек профиля  корректно отображается информация в соответствии с введеным при регистрации
            (сразу после создания отображается, номер телефона, роль и имя)
            * В БД проверить, что создалась запись с заполненными в соответствии с созданным полями и проверить
            что данная запись имеет права "Продавец"
            * Проверить наличие двух сообщений в мессенджере.
            * Открыть и прочитать их.
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_registration_by_phone_check_sms_language(self):
        """
        Title: Смс с паролем приходит на том языке, на котором выполняется регистрация
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

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class TestRegistrationByPhoneForm(HelpRegCheckMethods, HelpAuthCheckMethods, HelpLifeCycleCheckMethods, Navigate):
    """
    Story: Форма регистрации по телефону
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        Navigate.get_page(cls.driver, Navigate.path_reg.URL_REG)
        cls.click_to_phone(cls.driver)
        service_log.preparing_env(cls)

    @priority("High")
    def test_registration_by_phone_form_empty_password(self):
        """
        Title: Я не могу зарегистрироваться по телефону, если не ввел полученный пароль.
        Отобразится сообщение "Введите пароль"
        """
        service_log.run(self)
        obj_phone, obj_username, obj_submit_button = self.get_data_registration(self.driver)
        obj_username.send_keys('Vasya ne budet vvodit parol')
        obj_phone.send_keys(str(random.randrange(1000000000, 7007777777, 1)))
        self.click_button(obj_submit_button)
        self.password_send(self.driver)
        ok_button = self.get_submit_ok(self.driver)
        self.click_button(ok_button)
        self.check_need_password(self.driver)

    @priority("Medium")
    def test_registration_by_phone_form_empty_name(self):
        """
        Title: Я не могу зарегистрироваться по телефону, если не ввел Имя. Отображается сообщение "Введите имя"
        """
        service_log.run(self)
        obj_phone, obj_username, obj_submit_button = self.get_data_registration(self.driver)
        obj_phone.send_keys(str(random.randrange(1000000000, 7007777777, 1)))
        obj_submit_button.click()
        self.check_need_name(self.driver)
        self.check_not_need_phone(self.driver)

    @priority("Medium")
    def test_registration_by_phone_form_empty_phone(self):
        """
        Title: Я не могу зарегистрироваться по телефону, если не ввел Телефон. Отображается сообщение "Введите телефон"
        """
        service_log.run(self)
        obj_phone, obj_username, obj_submit_button = self.get_data_registration(self.driver)
        obj_username.send_keys('Vasya')
        obj_submit_button.click()
        self.check_need_phone_only(self.driver)

    @skip('manual')
    @priority("Low")
    def test_registration_by_phone_form_negative_checks(self):
        """
        Title: Валидация полей формы Регистрации: Моб. телефон и Имя пользователя: Негативные
        Description:
        По Таблице Сущностей проверить, для каждого КРАСНОГО :
            * невозможность создать данную уч. запись
            * выдачу соответствующего предупреждающего сообщения или невозможность ввода в поля данного значения
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_registration_by_phone_form_positive_checks(self):
        """
        Title: Валидация полей формы Регистрации: Моб. телефон и Имя пользователя: Позитивные
        Description:
        По Таблице Сущностей проверить, для каждог ЗЕЛЕНОГО:
            * корректность создания и отображения пользователя в виджете "Профиль пользователя" в шапке
            * корректность создания и отображения пользователя на странице Настройки пользователя
            * корректность создания и отображения пользователя в бек-офисе
        * корректность сохранения в БД
        """
        pass

    @priority("High")
    def test_registration_form_link_to_registration_page(self):
        """
        Title: Я могу перейти на страницу авторизации, нажав на "Вход"
        """
        service_log.run(self)
        authorization_button = self.get_authorization_page(self.driver)
        self.click_button(authorization_button)
        self.check_page_authorization(self.driver)

    @priority("High")
    def test_registration_form_site_rules(self):
        """
        Title: На форме регистрации отображается текст и ссылка на правила пользования сайтом
        Description:
            * При клике на ссылку на правила, они открываются в новом окне (/rules)
        """
        rules = self.element_is_present(self.driver, self.click_reg.LINK_RULES)
        self.click_button(rules)
        self.get_new_window(self.driver)
        self.element_is_present(self.driver, self.check_help.T_RULES)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()