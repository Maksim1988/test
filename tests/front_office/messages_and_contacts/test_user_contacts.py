# -*- coding: utf-8 -*-
"""
Feature: Контакты пользователя
"""
from copy import deepcopy
import random
from unittest import skip, expectedFailure
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from support import service_log
from support.utils import common_utils
from support.utils.db import databases
from support.utils.common_utils import generate_sha256, priority
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate
from tests.front_office.messages_and_contacts.classes.class_user_contacts import HelpUserContactsCheckMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods

__author__ = 'm.senchuk'


class TestContactListView(HelpAuthCheckMethods, Navigate, HelpUserContactsCheckMethods):
    """
    Story: Отображение списка избранных пользователей
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        databases.db1.accounting.update_account_details_by_criteria(cls.default_user_id, "locale='ru'")
        cls.user = databases.db1.accounting.get_user_by_account_id(cls.default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        cls.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(cls.default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=cls.default_new_passwd, flag_auth=True)
        cls.get_page(cls.driver, cls.path_user_contact.URL_FAVORITES_USERS)

    @priority("medium")
    def test_user_cards(self):
        """
        Title: Контакт-лист состоит из контактов - карточек пользователей.
        Каждая {Картчока пользователя} отображает: Аватар, Имя и Статус (В сети \ Не в сети)
        """
        self.check_count_contacts(self.driver, databases.db1, need_count=5)
        fav_users_list = databases.db1.accounting.get_fav_user_by_user_id(self.user["id"])
        for user in fav_users_list:
            user = databases.db1.accounting.get_data_user_by_id(user["favorites_account_id"])[0]
            self.check_card_user_in_contacts(self.driver, user)

    @priority("medium")
    def test_scroll_contacts(self):
        """
        Title: При большом кол-ве контактов появляется слайдер и возможность скролить контакт-лист
        """
        last_user_id = None
        fav_users_list_old = databases.db1.accounting.get_fav_user_by_user_id(self.user["id"])
        if fav_users_list_old is None: fav_users_list_old = list()
        self.set_user_to_contacts(self.driver, databases.db1, len(fav_users_list_old), need_count=30, mode='seller')
        fav_users_list = databases.db1.accounting.get_fav_user_by_user_id(self.user["id"])
        min_time = fav_users_list[0]["create_date"]
        last_user_id = fav_users_list[0]["favorites_account_id"]
        for fav in fav_users_list:
            if fav["create_date"] < min_time:
                min_time = fav["create_date"]
                last_user_id = fav["favorites_account_id"]
        user_last = databases.db1.accounting.get_data_user_by_id(last_user_id)[0]
        self.check_scroll_in_contacts(self.driver, user_last)

    @priority("medium")
    def test_check_disabled_user(self):
        """
        Title: В контакт-листе я вижу всех добавленных в контакты пользователей:
        Роль(любая) & статус(Активен OR Заблокирован) & принадлежат контакт-листу CurrentUser
        """
        self.check_count_contacts(self.driver, databases.db1, need_count=5)
        fav_users_list_old = databases.db1.accounting.get_fav_user_by_user_id(self.user["id"])
        self.set_user_to_contacts(self.driver, databases.db1, 0, 1, mode='disabled')
        fav_users_list = databases.db1.accounting.get_fav_user_by_user_id(self.user["id"])
        self.assertGreater(len(fav_users_list), len(fav_users_list_old))
        for user in fav_users_list:
            user = databases.db1.accounting.get_data_user_by_id(user["favorites_account_id"])[0]
            self.check_card_user_in_contacts(self.driver, user)

    @priority("medium")
    def test_add_contact_from_shop_page(self):
        """
        Title: Я могу добавить новый контакт в контакт-лист со страницы магазина продавца
        """
        fav_users_list_old = databases.db1.accounting.get_fav_user_by_user_id(self.user["id"])
        fav_old = lambda fav: list() if fav_users_list_old is None else fav_users_list_old
        self.set_user_to_contacts(self.driver, databases.db1, 0, 1, mode='seller')
        fav_users_list = databases.db1.accounting.get_fav_user_by_user_id(self.user["id"])
        self.assertGreater(len(fav_users_list), len(fav_old(fav_users_list_old)))

    @classmethod
    def tearDown(cls):
        HelpUserContactsCheckMethods.delete_user_in_contacts(cls.driver, databases.db1, cls.user["id"])
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class TestAddContactByPhoneView(HelpAuthCheckMethods, Navigate, HelpUserContactsCheckMethods):
    """
    Story: Отображение добавления пользователя в список контактов
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        databases.db1.accounting.update_account_details_by_criteria(cls.default_user_id, "locale='ru'")
        cls.user = databases.db1.accounting.get_user_by_account_id(cls.default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        cls.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(cls.default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=cls.default_new_passwd, flag_auth=True)
        cls.get_page(cls.driver, cls.path_user_contact.URL_FAVORITES_USERS)

    @priority("medium")
    def test_phone_validate_length(self):
        """
        Title: Поле поиска контактов по номеру телефона имеет маску для ввода номера телефона,
        не принимает больше чем 10 чисел (без +7)
        """
        self.element_click(self.driver, self.click_user_contact.BTN_NEW_CONTACT, change_page_url=False)
        inp = self.get_element_navigate(self.driver, self.input_user_contact.PHONE)
        input_str = self.user["phone"][1:] + common_utils.random_string(params='digits', length=3)
        inp.send_keys(input_str)
        check_str = self.user["phone"][1:]
        self.check_input_string(self.driver, check_str)

    @priority("medium")
    def test_phone_validate_symbols(self):
        """
        Title: Поле поиска контактов по номеру телефона не позволяет ввести ничего кроме чисел:
        буквы, символы, знаки препинания, пробелы
        """
        self.element_click(self.driver, self.click_user_contact.BTN_NEW_CONTACT, change_page_url=False)
        inp = self.get_element_navigate(self.driver, self.input_user_contact.PHONE)
        input_str = u"q,./-()! @#${}|[]" + self.user["phone"][1:]
        inp.send_keys(input_str)
        check_str = self.user["phone"][1:]
        self.check_input_string(self.driver, check_str)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class TestAddContactByPhoneLogic(HelpAuthCheckMethods, Navigate, HelpUserContactsCheckMethods):
    """
    Story: Логика добавления пользователя в список контактов
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        databases.db1.accounting.update_account_details_by_criteria(cls.default_user_id, "locale='ru'")
        cls.user = databases.db1.accounting.get_user_by_account_id(cls.default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        cls.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(cls.default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=cls.default_new_passwd, flag_auth=True)
        # Переход в Контакты
        cls.get_page(cls.driver, cls.path_user_contact.URL_FAVORITES_USERS)
        # Переход по кнопке Новый контакт
        cls.element_click(cls.driver, cls.click_user_contact.BTN_NEW_CONTACT, change_page_url=False)
        cls.input_phone = cls.get_element_navigate(cls.driver, cls.input_user_contact.PHONE)
        # Получить список пользователей в контактах у пользователя
        cls.fav_users_list = databases.db1.accounting.get_fav_user_by_user_id(cls.user["id"])
        l = lambda l: list() if cls.fav_users_list is None else cls.fav_users_list
        cls.fav_list = [str(value["favorites_account_id"]) for value in l(cls.fav_users_list)]
        # чтобы исключить попадание себя в список контактов
        cls.fav_list.append(str(cls.user['id']))

    @priority("medium")
    def test_add_new_contact_seller(self):
        """
        Title: Я могу добавить новый контакт (Продавец) в контакт-лист, введя полностью его номер телефона (...)
        """
        # Получить список пользователей с ролью продавец
        seller_id_list = databases.db1.accounting.get_user_by_role(need_role='2', not_role='3,4')
        value_list = [str(value["account_details_id"]) for value in seller_id_list]
        # Убрать из списка продавцов пользователей, которые есть в контактах
        diff = lambda l1, l2: filter(lambda x: x not in l2, l1)
        value_list = diff(value_list, self.fav_list)
        # Выбрать продавца для добавления в список контактов
        value_str = ','.join(value_list)
        crt = "id in (%s) AND phone like '7%s' AND length(phone)=11 AND display_name is not NULL LIMIT 100"
        sellers = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED', criteria=crt % (value_str, '%'))
        seller = random.choice(sellers)
        # Ввод номер телефона
        self.input_phone.send_keys(seller["phone"][1:])
        # Проверка карточки найденного пользователя
        self.check_card_user_in_search_contact(self.driver, seller)
        add_cnt_btn = self.get_element_navigate(self.driver, self.click_user_contact.BTN_ADD_CONTACT)
        self.click_button(add_cnt_btn, sleep=0.5)
        self.check_user_added(self.driver, seller["display_name"])
        self.check_active_card_user_in_contacts(self.driver, seller)
        self.check_active_user_info(self.driver, databases.db1, seller, role='seller')

    #   14.06.2015 все пользователи продавцы
    @skip('deprecated')
    @priority('low')
    def test_add_new_contact_buyer(self):
        """
        Title: Я могу добавить новый контакт (Покупатель) в контакт-лист, введя полностью номер телефона
        """
        # Получить список пользователей с ролью покупатель
        buyer_id_list = databases.db1.accounting.get_user_by_role(need_role='1', not_role='2,3,4')
        value_list = [str(value["account_details_id"]) for value in buyer_id_list]
        # Убрать из списка покупателей пользователей, которые есть в контактах
        diff = lambda l1, l2: filter(lambda x: x not in l2, l1)
        value_list = diff(value_list, self.fav_list)
        # Выбрать покупателя для добавления в список контактов
        value_str = ','.join(value_list)
        crt = "id in (%s) AND phone like '7%s' AND length(phone)=11 AND display_name is not NULL LIMIT 100"
        buyers = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED', criteria=crt % (value_str, '%'))
        buyer = random.choice(buyers)
        # Ввод номер телефона
        self.input_phone.send_keys(buyer["phone"][1:])
        # Проверка карточки найденного пользователя
        self.check_card_user_in_search_contact(self.driver, buyer)
        add_cnt_btn = self.get_element_navigate(self.driver, self.click_user_contact.BTN_ADD_CONTACT)
        self.click_button(add_cnt_btn, sleep=0.5)
        self.check_user_added(self.driver, buyer["display_name"])
        self.check_active_card_user_in_contacts(self.driver, buyer)
        self.check_active_user_info(self.driver, databases.db1, buyer, role='buyer')

    @skip('deprecated')
    @priority('low')
    def test_add_new_contact_buyer_disabled(self):
        """
        Title: Я могу добавить новый контакт (заблокированный пользователь) в контакт-лист, введя полностью номер телефона
        """
        # Получить список пользователей с ролью покупатель
        buyer_id_list = databases.db1.accounting.get_user_by_role(need_role='1', not_role='2,3,4')
        value_list = [str(value["account_details_id"]) for value in buyer_id_list]
        # Убрать из списка покупателей пользователей, которые есть в контактах
        diff = lambda l1, l2: filter(lambda x: x not in l2, l1)
        value_list = diff(value_list, self.fav_list)
        # Выбрать покупателя для добавления в список контактов
        value_str = ','.join(value_list)
        crt = "id in (%s) AND phone like '7%s' AND length(phone)=11 AND display_name is not NULL LIMIT 100"
        buyers = databases.db1.accounting.get_user_by_criteria(account_status='DISABLED', criteria=crt % (value_str, '%'))
        buyer = random.choice(buyers)
        # Ввод номер телефона
        self.input_phone.send_keys(buyer["phone"][1:])
        # Проверка карточки найденного пользователя
        self.check_card_user_in_search_contact(self.driver, buyer)
        add_cnt_btn = self.get_element_navigate(self.driver, self.click_user_contact.BTN_ADD_CONTACT)
        self.click_button(add_cnt_btn, sleep=0.5)
        self.check_user_added(self.driver, buyer["display_name"])
        self.check_active_card_user_in_contacts(self.driver, buyer)
        self.check_active_user_info(self.driver, databases.db1, buyer, role='buyer')

    @skip('deprecated')
    @priority('low')
    def test_add_new_contact_buyer_wait_for_registration(self):
        """
        Title: Я НЕ могу добавить новый контакт (ожидает активации) в контакт-лист, введя полностью номер телефона.
        Он не находится.
        """
        # Получить список пользователей с ролью покупатель
        buyer_id_list = databases.db1.accounting.get_user_by_role(need_role='1', not_role='2,3,4')
        value_list = [str(value["account_details_id"]) for value in buyer_id_list]
        # Убрать из списка покупателей пользователей, которые есть в контактах
        diff = lambda l1, l2: filter(lambda x: x not in l2, l1)
        value_list = diff(value_list, self.fav_list)
        # Выбрать покупателя для добавления в список контактов
        value_str = ','.join(value_list)
        crt = "id in (%s) AND phone like '7%s' AND length(phone)=11 AND display_name is not NULL LIMIT 100"
        buyers = databases.db1.accounting.get_user_by_criteria(account_status='WAIT_FOR_REGISTRATION', criteria=
                                                               crt % (value_str, '%'))
        buyer = random.choice(buyers)
        # Ввод номер телефона
        self.input_phone.send_keys(buyer["phone"][1:])
        # Проверка что пользователь не найден
        self.check_not_found_user(self.driver)

    @priority("medium")
    def test_add_new_contact_close(self):
        """
        Title: Я могу не добавлять найденного пользователя и вернуться на страницу "Мои контакты", закрыв окно.
        """
        # Получить список пользователей с ролью покупатель
        buyer_id_list = databases.db1.accounting.get_user_by_role(need_role='2', not_role='3,4')
        value_list = [str(value["account_details_id"]) for value in buyer_id_list]
        # Убрать из списка покупателей пользователей, которые есть в контактах
        diff = lambda l1, l2: filter(lambda x: x not in l2, l1)
        value_list = diff(value_list, self.fav_list)
        # Выбрать покупателя для добавления в список контактов
        value_str = ','.join(value_list)
        crt = "id in (%s) AND phone like '7%s' AND length(phone)=11 AND display_name is not NULL LIMIT 100"
        buyers = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED', criteria=crt % (value_str, '%'))
        buyer = random.choice(buyers)
        fav_users_list_old = databases.db1.accounting.get_fav_user_by_user_id(self.user["id"])
        # Ввод номер телефона
        self.input_phone.send_keys(buyer["phone"][1:])
        # Проверка, что пользователь нашелся
        self.check_card_user_in_search_contact(self.driver, buyer)
        # Закрываем окно добавления телефона
        cls_add_contact = self.get_element_navigate(self.driver, self.click_user_contact.BTN_CLOSE_ADD_CONTACT)
        self.click_button(cls_add_contact)
        # Проверка что пользователь не добавился
        fav = lambda fav: list() if fav is None else fav
        fav_users_list = databases.db1.accounting.get_fav_user_by_user_id(self.user["id"])
        self.assertEqual(len(fav(fav_users_list)), len(fav(fav_users_list_old)))

    @priority("medium")
    def test_add_new_contact_yourself(self):
        """
        Title: Я не могу добавить в контакт-лист себя, введя свой номер телефона. Отобразится текст "Это вы"
        """
        fav_users_list_old = databases.db1.accounting.get_fav_user_by_user_id(self.user["id"])
        # Ввод номер телефона
        self.input_phone.send_keys(self.user["phone"][1:])
        # Проверка, что пользователь нашелся и его нельзя добавить
        self.check_can_not_add_yourself(self.driver, self.user)
        # Закрываем окно добавления телефона
        cls_add_contact = self.get_element_navigate(self.driver, self.click_user_contact.BTN_CLOSE_ADD_CONTACT)
        self.click_button(cls_add_contact)
        # Проверка что пользователь не добавился в базе
        fav = lambda fav: list() if fav is None else fav
        fav_users_list = databases.db1.accounting.get_fav_user_by_user_id(self.user["id"])
        self.assertEqual(len(fav(fav_users_list)), len(fav(fav_users_list_old)))

    @priority("medium")
    def test_add_new_contact_by_character_phone(self):
        """
        Title: Если номер телефона введен не полностью, то результаты поиска не отображаются,
        до тех пор, пока номер телефона не будет введен полностью
        """
        # Ввод номер телефона по одной цифре
        for i in str(self.user["phone"][1:]):
            # Проверка что пользователь не найден
            self.check_empty_search_section(self.driver)
            self.input_phone.send_keys(i)
        # Нажатие ENTER
        ActionChains(self.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
        # Проверка, что пользователь нашелся и его нельзя добавить
        self.check_can_not_add_yourself(self.driver, self.user)

    @priority("medium")
    def test_add_new_contact_part_phone(self):
        """
        Title: Если номер телефона введен не полностью и нажат Ввод, то отобразится сообщение
        "Введите номер телефона полностью"
        """
        # Ввод части номера телефона
        self.input_phone.send_keys(self.user["phone"][1:5])
        # Нажатие ENTER
        ActionChains(self.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
        # Проверка, что появилось предупреждающее сообщение
        self.check_alert_message(self.driver)

    @priority("medium")
    def test_add_new_contact_without_phone(self):
        """
        Title: Если номер телефона не введен(пусто), и нажат Ввод, то отображается сообщение
        "Введите номер телефона полностью"
        """
        # Нажатие ENTER
        ActionChains(self.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
        # Проверка, что появилось предупреждающее сообщение
        self.check_alert_message(self.driver)

    @priority("medium")
    def test_add_new_contact_no_user_in_db(self):
        """
        Title: Если номер телефона не зарегистрирован в системе, то отображается соответствующее сообщение о результатах поиска
        """
        # Ввод номера телефона
        self.input_phone.send_keys(self.generate_phone_not_in_db(databases.db1)[1:])
        # Нажатие ENTER
        ActionChains(self.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
        # Проверка, что появилось предупреждающее сообщение
        self.check_not_found_user(self.driver)

    @priority("medium")
    def test_add_contact_from_contact_list(self):
        """
        Title: Если пользователь уже присутствует в контакт-листе, то он находится в результатах поиска,
        кнопка залочена и имеет текст "Уже в контатах". Я могу перейти на его карточку в контакт-листе выбрав
        карточку в поиске.
        """
        #f_users = databases.db1.accounting.get_fav_user_by_user_id(self.user["id"])
        # добавить пользователя
        added_user = self.set_user_to_contacts(self.driver, databases.db1, 0, 1, mode='seller')
        buyer = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED', criteria="id in (%s)" %
                                                                                                 added_user[0])[0]
        self.get_element_navigate(self.driver, self.click_user_contact.BTN_NEW_CONTACT).click()
        input_phone = self.get_element_navigate(self.driver, self.input_user_contact.PHONE)
        input_phone.send_keys(buyer["phone"][1:])
        # Проверка, что пользователь нашелся и есть сообщение Уже в контактах
        self.check_card_user_in_search_contact(self.driver, buyer)
        self.get_element_navigate(self.driver, self.check_user_contact.ALREADY_IN_CONTACT_LIST)
        self.check_no_add_contact_btn(self.driver)

    @classmethod
    def tearDown(cls):
        HelpUserContactsCheckMethods.delete_user_in_contacts(cls.driver, databases.db1, cls.user["id"])
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class TestDeleteContact(HelpAuthCheckMethods, Navigate, HelpUserContactsCheckMethods):
    """
    Story: Удалить пользователя из списка контактов
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        databases.db1.accounting.update_account_details_by_criteria(cls.default_user_id, "locale='ru'")
        cls.user = databases.db1.accounting.get_user_by_account_id(cls.default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        cls.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(cls.default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=cls.default_new_passwd, flag_auth=True)
        # Переход в Контакты
        #cls.get_page(cls.driver, cls.path_user_contact.URL_FAVORITES_USERS)
        # Переход по кнопке Новый контакт
        #cls.get_element_navigate(cls.driver, cls.click_user_contact.BTN_NEW_CONTACT).click()
        #cls.input_phone = cls.get_element_navigate(cls.driver, cls.input_user_contact.PHONE)
        # Получить список пользователей в контактах у пользователя
        cls.fav_users_list = databases.db1.accounting.get_fav_user_by_user_id(cls.user["id"])
        l = lambda l: list() if cls.fav_users_list is None else cls.fav_users_list
        cls.fav_list = [str(value["favorites_account_id"]) for value in l(cls.fav_users_list)]
        # чтобы исключить попадание себя в список контактов
        cls.fav_list.append(str(cls.user['id']))

    @priority("medium")
    def test_btn_delete_contact(self):
        """
        Title: Я могу удалить контакт из контакт-листа, нажав на кнопку "Удалить контакт" (...)
        """
        # добавить пользователя
        added_user = self.set_user_to_contacts(self.driver, databases.db1, 0, 1, mode='seller')[0]
        fav_user = databases.db1.accounting.get_user_by_criteria_only(criteria="id in (%s)" % added_user)[0]
        self.check_delete_first_user_in_cl(self.driver, self.user['id'], fav_user, databases.db1)

    @priority("medium")
    def test_add_deleted_contact(self):
        """
        Title: Я могу снова добавить удаленный контакт в контакт лист
        """
        # добавить пользователя
        added_user = self.set_user_to_contacts(self.driver, databases.db1, 0, 1, mode='seller')[0]
        fav_user = databases.db1.accounting.get_user_by_criteria_only(criteria="id in (%s)" % added_user)[0]
        # Удалить пользователя
        self.delete_first_user_in_cl(self.driver, fav_user)
        # Добавить обратно этого же пользователя
        self.click_in_contact(self.driver, added_user)
        # Перейти в контакты
        self.get_page(self.driver, self.path_user_contact.URL_FAVORITES_USERS)
        #Проверить,что пользователь в контактах
        self.get_element_navigate(self.driver, self.check_user_contact.USER_CARD_BY_ID % fav_user["id"])

    @priority("medium")
    def test_delete_contact_from_user_page(self):
        """
        Title: Я могу удалить контакт из контакт-листа, используя кнопку на странице контакта
        """
        # добавить пользователя
        added_user = self.set_user_to_contacts(self.driver, databases.db1, 0, 1, mode='seller')[0]
        fav_user = databases.db1.accounting.get_user_by_criteria_only(criteria="id in (%s)" % added_user)[0]
        #Проверить,что пользователь в контактах
        self.get_element_navigate(self.driver, Navigate.check_user_contact.USER_CARD_BY_ID % fav_user["id"])
        # Перейти на страницу пользователя и нажать В контактах
        self.get_page(self.driver, self.path_buyer.URL_BUYER % fav_user["id"])
        btn = self.get_element_navigate(self.driver, self.click_user_contact.OUT_CONTACT_USER, sleep=0.1, mode=None)
        self.click_button(btn)
        self.get_element_navigate(self.driver, self.click_user_contact.IN_CONTACT_USER, sleep=0.1, mode=None)
        self.driver.back()
        self.check_user_no_in_cl(self.driver ,fav_user["id"])

    @classmethod
    def tearDown(cls):
        HelpUserContactsCheckMethods.delete_user_in_contacts(cls.driver, databases.db1, cls.user["id"])
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class TestContactMoveTo(HelpAuthCheckMethods, Navigate, HelpUserContactsCheckMethods):
    """
    Story: Переходы из/на избранные контакты
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        databases.db1.accounting.update_account_details_by_criteria(cls.default_user_id, "locale='ru'")
        cls.user = databases.db1.accounting.get_user_by_account_id(cls.default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        cls.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(cls.default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=cls.default_new_passwd, flag_auth=True)
        # Получить список пользователей в контактах у пользователя
        cls.fav_users_list = databases.db1.accounting.get_fav_user_by_user_id(cls.user["id"])
        l = lambda l: list() if cls.fav_users_list is None else cls.fav_users_list
        cls.fav_list = [str(value["favorites_account_id"]) for value in l(cls.fav_users_list)]
        # чтобы исключить попадание себя в список контактов
        cls.fav_list.append(str(cls.user['id']))

    @priority("medium")
    def test_go_to_contacts(self):
        """
        Title: Перейти из хедера на страницу Контакты
        """
        time.sleep(5)
        self.element_click(self.driver, self.click_main.USER_MENU, change_page_url=False)
        head_cl = self.get_element_navigate(self.driver, self.click_main.HEADER_CONTACTS)
        self.click_button(head_cl)
        self.get_element_navigate(self.driver, self.click_user_contact.BTN_NEW_CONTACT)

    @priority("medium")
    def test_contacts_go_to_chat(self):
        """
        Title: Я могу перейти на страницу чата с контактом, выбрав его в списке контактов и нажав "Написать сообщение"
        """
        # добавить пользователя
        added_user = self.set_user_to_contacts(self.driver, databases.db1, 0, 1, mode='seller')[0]
        fav_user = databases.db1.accounting.get_user_by_criteria_only(criteria="id in (%s)" % added_user)[0]
        #Проверить,что пользователь в контактах
        usr = self.get_element_navigate(self.driver, self.check_user_contact.USER_CARD_BY_ID % fav_user["id"])
        self.click_button(usr)
        # Переход в чат и проверка что активен чат с пользователем
        chat = self.get_element_navigate(self.driver, self.click_user_contact.SEND_MSG % fav_user["id"])
        self.click_button(chat)
        url = self.driver.current_url.encode('utf-8')
        self.assertEqual(url, self.ENV_BASE_URL + self.path_chat.URL_CHAT_WITH_USER % fav_user["id"],
                         "Не произошел переход на страницу чата с пользователем, урл='%s'" % url)
        self.get_element_navigate(self.driver, self.check_chat.ACTIVE_USER_BY_ID % fav_user["id"])
        self.get_element_navigate(self.driver, self.click_chat.BTN_SEND)

    @priority("medium")
    def test_contact_seller_go_to_shop(self):
        """
        Title: Если выбранный контакт-продавец, Я могу перейти в магазин продавца, нажав на кнопку "В магазин"
        """
        # добавить пользователя
        added_user = self.set_user_to_contacts(self.driver, databases.db1, 0, 1, mode='seller')[0]
        fav_user = databases.db1.accounting.get_user_by_criteria_only(criteria="id in (%s)" % added_user)[0]
        #Проверить,что пользователь в контактах
        usr = self.get_element_navigate(self.driver, self.check_user_contact.USER_CARD_BY_ID % fav_user["id"])
        self.click_button(usr)
        # Переход в магазин
        shop = self.get_element_navigate(self.driver, self.click_user_contact.IN_SHOP % fav_user["id"])
        self.click_button(shop)
        url = self.driver.current_url.encode('utf-8')
        self.assertEqual(url, self.ENV_BASE_URL + self.path_shop.URL_SHOP % fav_user["id"],
                         "Не произошел переход на страницу магазина пользователя, урл='%s'" % url)
        self.get_element_navigate(self.driver, self.check_shop.USER_NAME % fav_user["display_name"])

    @priority("medium")
    def test_contact_buyer_no_btn_shop(self):
        """
        Title: Если выбранный контакт-покупатель, кнопки "В магазин" нет на форме
        """
        # добавить пользователя
        added_user = self.set_user_to_contacts(self.driver, databases.db1, 0, 1, mode='seller')[0]
        fav_user = databases.db1.accounting.get_user_by_criteria_only(criteria="id in (%s)" % added_user)[0]
        #Проверить,что пользователь в контактах
        usr = self.get_element_navigate(self.driver, self.check_user_contact.USER_CARD_BY_ID % fav_user["id"])
        self.click_button(usr)
        # Проверка что нет кнопки в магазин
        self.check_buyer_no_btn_in_shop(self.driver, fav_user["id"])

    @classmethod
    def tearDown(cls):
        HelpUserContactsCheckMethods.delete_user_in_contacts(cls.driver, databases.db1, cls.user["id"])
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class TestSearchByContactList(HelpAuthCheckMethods, Navigate, HelpUserContactsCheckMethods):
    """
    Story: Поиск пользователя в списке контактов
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        databases.db1.accounting.update_account_details_by_criteria(cls.default_user_id, "locale='ru'")
        cls.user = databases.db1.accounting.get_user_by_account_id(cls.default_user_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        cls.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(cls.default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=cls.default_new_passwd, flag_auth=True)
        # Переход в Контакты
        #cls.get_page(cls.driver, cls.path_user_contact.URL_FAVORITES_USERS)
        # Переход по кнопке Новый контакт
        #cls.get_element_navigate(cls.driver, cls.click_user_contact.BTN_NEW_CONTACT).click()
        #cls.input_phone = cls.get_element_navigate(cls.driver, cls.input_user_contact.PHONE)
        # Получить список пользователей в контактах у пользователя
        cls.fav_users_list = databases.db1.accounting.get_fav_user_by_user_id(cls.user["id"])
        l = lambda l: list() if cls.fav_users_list is None else cls.fav_users_list
        cls.fav_list = [str(value["favorites_account_id"]) for value in l(cls.fav_users_list)]
        # чтобы исключить попадание себя в список контактов
        cls.fav_list.append(str(cls.user['id']))

    @priority("medium")
    def test_find_full_user_name(self):
        """
        Title: Я могу найти пользователя по полному имени и посмотреть контакт,
        выбрав его карточку в результатах поиска. Очистив условия поиска я снова увижу всех контактов своего
        контакт-листа.
        """
        self.check_count_contacts(self.driver, databases.db1, need_count=5, mode='seller')
        fav_users_list = databases.db1.accounting.get_fav_user_by_user_id(self.user["id"])
        fav_users_id = [str(fav_user["favorites_account_id"]) for fav_user in fav_users_list]
        fav_users_str = ','.join(fav_users_id)
        fav_user = databases.db1.accounting.get_user_by_criteria_only(criteria="id in (%s)" % fav_users_str)
        count_contacts_old = self.get_count_contacts(self.driver)
        self.check_find_full_name(self.driver, fav_user[0])
        self.check_active_user_info(self.driver, databases.db1, fav_user[0], role='seller')
        self.clear_input_by_name(self.driver)
        count_contacts_new = self.get_count_contacts(self.driver)
        self.assertEqual(count_contacts_old, count_contacts_new, "После очистки поля поиска по имени количество "
                                                                 "контактов изменилось")

    @priority("medium")
    def test_find_users_by_symbol(self):
        """
        Title: Я могу найти всех пользователей из моего контакт-листа в имени которых есть введенные мною символы
        и посмотреть один из найденных контактов, выбрав его карточку в результатах поиска
        """
        self.check_count_contacts(self.driver, databases.db1, need_count=10, mode='seller')
        fav_users_list = databases.db1.accounting.get_fav_user_by_user_id(self.user["id"])
        fav_users_id = [str(fav_user["favorites_account_id"]) for fav_user in fav_users_list]
        fav_users_str = ','.join(fav_users_id)
        fav_user_accounts = databases.db1.accounting.get_user_by_criteria_only(criteria="id in (%s)" % fav_users_str)
        names = [user['display_name'] for user in fav_user_accounts]
        p = str()
        for name in names:
            names_copy = deepcopy(names)
            names_copy.remove(name)
            for i in name.decode('utf-8'):
                for name_c in names_copy:
                    k = name_c.decode('utf-8').find(i)
                    if k != -1:
                        p += i
        letter = random.choice(p.replace(u' ', u''))
        self.check_find_part_name(self.driver, letter.encode('utf-8'))
        path_fg = Navigate.check_user_contact.USER_INFO
        self.get_element_navigate(self.driver, path_fg, mode=None, e_msg="Не найден блок инфо пользователя у активного "
                                                                         "контакта")
        name = self.get_element_navigate(self.driver, self.check_user_contact.FU_ACTIVE_USER_ABSTRACT).text.encode('utf-8')
        self.get_element_navigate(self.driver, self.check_user_contact.UI_USER_NAME % name)

    @priority("medium")
    def test_not_find_users(self):
        """
        Title: Если по условиям поиска не найдено пользователей в моем контакт-листе, отображается соответствующий текст
        """
        self.check_count_contacts(self.driver, databases.db1, need_count=1, mode='seller')
        fav_users_list = databases.db1.accounting.get_fav_user_by_user_id(self.user["id"])
        fav_users_id = [str(fav_user["favorites_account_id"]) for fav_user in fav_users_list]
        fav_users_str = ','.join(fav_users_id)
        fav_user = databases.db1.accounting.get_user_by_criteria_only(criteria="id in (%s)" % fav_users_str)
        self.find_user_by_name(self.driver, fav_user[0]["display_name"]*2, sleep=2)
        self.get_element_navigate(self.driver, self.check_user_contact.NOT_FOUND_BY_NAME)

    @classmethod
    def tearDown(cls):
        HelpUserContactsCheckMethods.delete_user_in_contacts(cls.driver, databases.db1, cls.user["id"])
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()