# -*- coding: utf-8 -*-
from support import service_log
from tests.MainClass import MainClass
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods as Front

__author__ = 'm.senchuk'


class AuthData(MainClass):
    URL_RESTORE_EMAIL = "/reset-password?token=%s"
    NO_AVA_MALE = 'no_ava_male'
    NO_AVA_FEMALE = 'no_ava_female'


class AuthMethods(AuthData):
    @staticmethod
    def click_reg_and_auth(driver):
        """ Нажать на кнопку Зарегистрироваться и войти.
        :param driver: ссылка на драйвер
        """
        btn = Navigate.get_element_navigate(driver, Navigate.click_main.BUTTON_REG_AND_LOGIN)
        Front.click_button(btn)

    @staticmethod
    def click_tab_login(driver):
        """ Перейти на Вход.
        :param driver: ссылка на драйвер
        """
        btn = Navigate.get_element_navigate(driver, Navigate.click_reg.TAB_LOGIN)
        Front.click_button(btn)

    @staticmethod
    def click_tab_reg(driver):
        """ Перейти на Регистрацию
        :param driver: ссылка на драйвер
        """
        btn = Navigate.get_element_navigate(driver, Navigate.click_auth.TAB_REG)
        Front.click_button(btn)

    @staticmethod
    def auth_click_switch_phone(driver):
        """ Перейти на авторизацию с помощью телефона
        :param driver:  ссылка на драйвер
        """
        btn = Navigate.get_element_navigate(driver, Navigate.click_auth.SWITCH_PHONE)
        Front.click_button(btn)

    @staticmethod
    def auth_click_switch_email(driver):
        """ Перейти на авторизацию с помощью email
        :param driver: ссылка на драйвер
        """
        btn = Navigate.get_element_navigate(driver, Navigate.click_auth.SWITCH_EMAIL)
        Front.click_button(btn)

    @staticmethod
    def get_auth_email_form(driver):
        """ Получить элементы формы авторизации по емайлу
        :param driver: ссылка на драйвер
        :return: словарь со ссылками на элементы формы авторизации
        """
        auth_email = {
            "registration_tab": Navigate.get_element_navigate(driver, Navigate.click_auth.TAB_REG),
            "login_tab": Navigate.get_element_navigate(driver, Navigate.check_auth.TAB_LOGIN_ACTIVE),
            #"email_switch": Navigate.get_element_navigate(driver, Navigate.click_auth.SWITCH_EMAIL),
            #"phone_switch": Navigate.get_element_navigate(driver, Navigate.click_auth.SWITCH_PHONE),
            "email_label": Navigate.get_element_navigate(driver, Navigate.check_auth.LABEL_EMAIL),
            "email_input": Navigate.get_element_navigate(driver, Navigate.input_auth.INPUT_EMAIL),
            "password_label": Navigate.get_element_navigate(driver, Navigate.check_auth.LABEL_PASSWORD),
            "password_input": Navigate.get_element_navigate(driver, Navigate.input_auth.INPUT_PASSWORD),
            "login_btn": Navigate.get_element_navigate(driver, Navigate.click_auth.BTN_LOGIN),
            "restore_btn": Navigate.get_element_navigate(driver, Navigate.click_auth.BTN_RESTORE),
        }
        service_log.put("Get elements form authorization by email %s" % str(auth_email))
        return auth_email

    @staticmethod
    def get_reg_email_form(driver):
        """ Получить элементы формы регистрации по емайлу
        :param driver: ссылка на драйвер
        :return: словарь со ссылками на элементы формы регистрации
        """
        reg_email = {
            "registration_tab": Navigate.get_element_navigate(driver, Navigate.check_reg.TAB_REG_ACTIVE),
            "login_tab": Navigate.get_element_navigate(driver, Navigate.click_reg.TAB_LOGIN),
            "email_switch": Navigate.get_element_navigate(driver, Navigate.click_reg.SWITCH_EMAIL),
            "phone_switch": Navigate.get_element_navigate(driver, Navigate.click_reg.SWITCH_PHONE),
            "name_label": Navigate.get_element_navigate(driver, Navigate.check_reg.LABEL_NAME),
            "name_input": Navigate.get_element_navigate(driver, Navigate.input_reg.E_INPUT_NAME),
            "email_label": Navigate.get_element_navigate(driver, Navigate.check_reg.LABEL_EMAIL),
            "email_input": Navigate.get_element_navigate(driver, Navigate.input_reg.E_INPUT_EMAIL),
            "password_label": Navigate.get_element_navigate(driver, Navigate.check_reg.LABEL_PASSWORD),
            "password_input": Navigate.get_element_navigate(driver, Navigate.input_reg.E_INPUT_PASSWORD),
            "reg_btn": Navigate.get_element_navigate(driver, Navigate.click_reg.BTN_REG),
            "rules": Navigate.get_element_navigate(driver, Navigate.check_reg.RULES),
        }
        service_log.put("Get elements form registration by email %s" % str(reg_email))
        return reg_email

    @staticmethod
    def get_restore_email_form(driver):
        """ Получить элементы формы восстановления пароля по емайл
        :param driver: ссылка на драйвер
        :return: словарь со ссылками на элементы формы восстановления пароля
        """
        restore_email = {
            "restore_title": Navigate.get_element_navigate(driver, Navigate.check_restore.TITLE_RESTORE_PAGE),
            "email_label": Navigate.get_element_navigate(driver, Navigate.check_restore.LABEL_EMAIL),
            "email_input": Navigate.get_element_navigate(driver, Navigate.input_restore.INPUT_EMAIL),
            "restore_btn": Navigate.get_element_navigate(driver, Navigate.click_restore.BTN_RESTORE),
        }
        service_log.put("Get elements form restore %s" % str(restore_email))
        return restore_email

    @staticmethod
    def get_restore_email_sent_form(driver):
        """ Получить элементы формы восстановления пароля по емайл, письмо тправлено
        :param driver: ссылка на драйвер
        :return: словарь со ссылками на элементы формы восстановления пароля
        """
        restore_email = {
            "restore_title": Navigate.get_element_navigate(driver, Navigate.check_restore.TITLE_RESTORE_PAGE),
            "restore_text": Navigate.get_element_navigate(driver, Navigate.check_restore.TEXT_SENT_TO_EMAIL),
            "to_main_btn": Navigate.get_element_navigate(driver, Navigate.click_restore.BTN_TO_MAIN),
        }
        service_log.put("Get elements form restore %s" % str(restore_email))
        return restore_email

    @staticmethod
    def get_restore_email_input_pass_form(driver, email):
        """ Получить элементы формы восстановления пароля по емайл где можно ввести нвый пароль
        :param driver: ссылка на драйвер
        :return: словарь со ссылками на элементы формы восстановления пароля
        """
        restore_email = {
            "restore_title": Navigate.get_element_navigate(driver, Navigate.check_restore.TITLE_INPUT_PASS_PAGE),
            "email_label": Navigate.get_element_navigate(driver, Navigate.check_restore.LABEL_EMAIL),
            "email_input": Navigate.get_element_navigate(driver, Navigate.check_restore.INPUT_EMAIL_HOLD % email),
            "password_label": Navigate.get_element_navigate(driver, Navigate.check_restore.LABEL_PASSWORD),
            "password_input": Navigate.get_element_navigate(driver, Navigate.input_restore.INPUT_PASSWORD),
            "password_repeat_label": Navigate.get_element_navigate(driver, Navigate.check_restore.LABEL_R_PASSWORD),
            "password_repeat_input": Navigate.get_element_navigate(driver, Navigate.input_restore.INPUT_R_PASSWORD),
            "set_pass_btn": Navigate.get_element_navigate(driver, Navigate.click_restore.BTN_SET_PASS),
        }
        service_log.put("Get elements form restore input password %s" % str(restore_email))
        return restore_email

    @staticmethod
    def get_restore_password_by_email_success(driver):
        """ Получить элементы формы восстановления пароля по емайл, письмо тправлено
        :param driver: ссылка на драйвер
        :return: словарь со ссылками на элементы формы восстановления пароля
        """
        restore_email = {
            "restore_title": Navigate.get_element_navigate(driver, Navigate.check_restore.TITLE_INPUT_PASS_PAGE),
            "restore_text": Navigate.get_element_navigate(driver, Navigate.check_restore.TEXT_NEW_PASS_SET),
            "start_work_btn": Navigate.get_element_navigate(driver, Navigate.click_restore.BTN_START_WORK),
        }
        service_log.put("Get elements form restore %s" % str(restore_email))
        return restore_email


class AuthCheckMethods(AuthMethods):

    def check_password_mask(self, pass_web, pass_db):
        """ Проверка, что пароль скрывается маской из звездочек
        :param pass_web: пароля с веба
        :param pass_db: пароль с БД
        """
        stars_list = ['*' for i in pass_db]  # Проверка, что пароль скрылся маской из звездочек
        stars = ''.join(stars_list)
        err_msg1 = "Длина введенного пароля %s не совпадает с длиной заданного пароля %s"
        err_msg2 = "Введенный пароль %s не замаскировался звездочками %s"
        err_msg3 = "Введенный пароль %s остался в том же виде %s"

        self.assertEqual(len(pass_web), len(pass_db), err_msg1 % (len(pass_web), len(pass_db)))
        self.assertEqual(pass_web, stars, err_msg2 % (pass_web, stars))
        self.assertNotEqual(pass_web, pass_db, err_msg3 % (pass_web, pass_db))

    def is_logged(self, driver):
        """
        Простая проверка, что пользователь залогинен
        :return:
        """
        Navigate.element_is_present(driver, Navigate.click_main.USER_MENU)

    def is_user_logged(self, driver, user):
        """
        Проверка, что пользователь залогинен. Корректность имени пользователя в хедере
        :param user:
        :return:
        """
        Navigate.element_is_present(driver, Navigate.click_main.MENU_PROFILE_NAME % user['display_name'])

    def user_profile_menu(self, driver, user):
        """
        Проверка выпадающего меню пользователя в хедере
        :param driver:
        :param user:
        :return:
        """
        if (user['gender'] == 'MALE' or user['gender'] is None) and user['avatar_id'] is None:
            avatar_id = self.NO_AVA_MALE
        elif user['gender'] == 'FEMALE' and user['avatar_id'] is None:
            avatar_id = self.NO_AVA_FEMALE
        else:
            avatar_id = user['avatar_id']
        Navigate.element_click(driver, Navigate.click_main.MENU_PROFILE_NAME % user['display_name'], change_page_url=False)
        Navigate.element_is_present(driver, Navigate.click_main.MENU_PROFILE_AVATAR % avatar_id)
        Navigate.element_is_present(driver, Navigate.click_main.MENU_PROFILE_MY_STORE)
        Navigate.element_is_present(driver, Navigate.click_main.MENU_PROFILE_FAVORITES)
        Navigate.element_is_present(driver, Navigate.click_main.MENU_PROFILE_CONTACTS)
        Navigate.element_is_present(driver, Navigate.click_main.MENU_PROFILE_SETTINGS)
        Navigate.element_is_present(driver, Navigate.click_main.MENU_PROFILE_EXIT)