# -*- coding: utf-8 -*-
"""
Feature: Сообщения
"""
import random
import time
import json
from unittest import skip

from support import service_log
from support.utils import common_utils
from support.utils.db import databases
from support.utils.common_utils import generate_sha256, priority
from support.utils.thrift4req import services
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods
from tests.front_office.settings.classes.class_profile_settings import HelpProfileSettingsCheckMethods as Settings
from tests.front_office.messages_and_contacts.classes.class_chat import HelpChatCheckMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods
from tests.worker_warehouse.class_warehouse import WarehouseCheckMethods

__author__ = 'm.senchuk'


class SendMessageFromGoodPage(HelpNavigateCheckMethods, HelpAuthCheckMethods, HelpChatCheckMethods,
                              WarehouseCheckMethods):
    """
    Story: Отправить сообщение со страницы товара
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.default_seller_id = AccountingMethods.get_default_user_id(role='seller')
        cls.default_seller_own_id = AccountingMethods.get_default_user_id(role='seller_alien')
        cls.moderator_id = int(AccountingMethods.get_default_user_id(role='moderator'))

    @skip('deprecated')
    @priority("medium")
    def test_as_buyer_to_good(self, test_good=HelpNavigateCheckMethods.SHP_TO_GOOD):
        """Title: Написать текст продавцу от покупателя по поводу его активного товара и остаться в карточки товара.
        Description: Я, как Покупатель, могу написать продавцу сообщение по Активному товару,
        нажав на "Связаться с продавцом" и оставив текст, по умолчанию. После этого я остаюсь на карточке товара (...)
        """
        databases.db1.accounting.update_account_details_by_criteria(self.default_user_id, "locale='ru'")
        self.user = databases.db1.accounting.get_user_by_account_id(self.default_user_id)[0]
        self.shop = databases.db1.accounting.get_shop_details_by_shop_id(self.user["shop_id"])[0]

        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        self.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(self.default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=self.default_new_passwd, flag_auth=True)

        self.get_page(self.driver, self.path_shop.URL_SHOP % self.default_seller_id)
        self.check_navigate_in_good_page(self.driver, test_good, random.randrange(1, 10, 1))
        self.data_good, good_str = self.get_good_data(self.driver)
        btn_to_call = self.get_element_navigate(self.driver, self.click_good.BTN_CALL_SELLER)
        self.click_button(btn_to_call)
        # ищем товар с нужным id
        obj_good = self.get_element_navigate(self.driver, self.click_good.GOOD_BY_ID_POPUP % self.data_good['good_id'])
        self.check_express_card_good(obj_good, good_str)
        # проверяем фото товара
        self.get_element_navigate(self.driver, (self.click_good.GOOD_BY_ID_POPUP % self.data_good['good_id']) +
                                  (self.path_category.PATH_IMG % self.data_good['image']))
        # Проверка текста в попапе
        obj_text = self.get_element_navigate(self.driver, self.check_good.POPUP_MSG_FROM_GOOD % '')
        str_msg_to_good = obj_text.text.encode('utf-8').replace(' ', '')
        obj_send = self.get_element_navigate(self.driver, self.click_good.BTN_SEND)
        self.click_button(obj_send)
        # После отправки сообщения отображается окно "Сообщение отправлено"
        btn_to_good, btn_to_chat = self.get_sent_success_btn(self.driver)
        self.click_button(btn_to_good)
        #После нажатия на "На карточку" я остаюсь на карточке этого же товара
        self.assertEqual(self.data_good["good_id"], self.driver.current_url[self.driver.current_url.rfind('/') + 1:].
                         encode('utf-8'))
        # Кнопка "Связаться с продавцом" на карточке товара активна.
        self.get_element_navigate(self.driver, self.click_good.BTN_CALL_SELLER)
        # В чате с продавцом есть отправленное от меня сообщение и карточка товара. Проверить соответствие.
        self.get_page(self.driver, self.path_chat.URL_CHAT_WITH_USER % self.default_seller_id)
        last_msg = self.get_last_msg(self.driver)
        self.assertIn(good_str, last_msg, "Экспресс карточка='%s' не совпадает с последним сообщением='%s'" %
                      (good_str, last_msg))
        self.assertIn(str_msg_to_good, last_msg, "Стандартное сообщение о товаре='%s' не совпадает с последним "
                                                 "сообщением='%s'" % (str_msg_to_good, last_msg))

    @skip('deprecated')
    @priority("must")
    def test_as_buyer_to_chat(self, test_good=HelpNavigateCheckMethods.SHP_TO_GOOD):
        """
        Title: Написать текст от покупателя продавцу по поводу его активного товара и перейти в чат с ним.
        Description: Я, как Покупатель, могу написать продавцу сообщение по Активному товару,
        нажав на "Связаться с продавцом" и ввести свой текст. После этого я могу перейти в чат с продавцом (...)
        """
        databases.db1.accounting.update_account_details_by_criteria(self.default_user_id, "locale='ru'")
        self.user = databases.db1.accounting.get_user_by_account_id(self.default_user_id)[0]
        self.shop = databases.db1.accounting.get_shop_details_by_shop_id(self.user["shop_id"])[0]

        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        self.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(self.default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=self.default_new_passwd, flag_auth=True)

        self.get_page(self.driver, self.path_shop.URL_SHOP % self.default_seller_id)
        self.check_navigate_in_good_page(self.driver, test_good, random.randrange(1, 10, 1))
        self.data_good, good_str = self.get_good_data(self.driver)
        btn_to_call = self.get_element_navigate(self.driver, self.click_good.BTN_CALL_SELLER)
        self.click_button(btn_to_call)
        # ищем товар с нужным id
        obj_good = self.get_element_navigate(self.driver, self.click_good.GOOD_BY_ID_POPUP % self.data_good['good_id'])
        self.check_express_card_good(obj_good, good_str)
        # проверяем фото товара
        self.get_element_navigate(self.driver, (self.click_good.GOOD_BY_ID_POPUP % self.data_good['good_id']) +
                                  (self.path_category.PATH_IMG % self.data_good['image']))
        # Проверка текста в попапе
        popup_text = self.get_element_navigate(self.driver, self.check_good.POPUP_MSG_FROM_GOOD % '')
        Settings.clear_input_row(self.driver, popup_text)
        text = common_utils.random_string(length=50)
        popup_text.send_keys(text)
        obj_send = self.get_element_navigate(self.driver, self.click_good.BTN_SEND)
        self.click_button(obj_send)
        # После отправки сообщения отображается окно "Сообщение отправлено"
        btn_to_good, btn_to_chat = self.get_sent_success_btn(self.driver)
        self.click_button(btn_to_chat)
        # После нажатия на "Перейти в чат" я перехожу на страницу чата с данным продавцом
        self.assertEqual(self.ENV_BASE_URL + self.path_chat.URL_CHAT_WITH_USER % self.default_seller_id,
                         self.driver.current_url)
        # В чате с продавцом есть отправленное от меня сообщение и карточка товара. Проверить соответствие текста и товара.
        last_msg = self.get_last_msg(self.driver)
        self.assertIn(good_str, last_msg, "Экспресс карточка='%s' не совпадает с последним сообщением='%s'" %
                      (good_str, last_msg))
        str_msg_to_good = self.TEXT_MSG_TO_GOOD.replace(' ', '')
        self.assertIn(text, last_msg, "Свое сообщение о товаре='%s' не совпадает с последним "
                                      "сообщением='%s'" % (str_msg_to_good, last_msg))

    @skip('update')
    @priority("medium")
    def test_as_visitor_to_chat(self, number_good=1, test_data=HelpNavigateCheckMethods.CATALOG_TO_GOOD):
        #TODO: обновить
        """
        Title: Я, как Гость, при нажатии на "Связаться с продавцом" увижу страницу Авторизации
        """
        self.driver.delete_all_cookies()
        self.driver.refresh()
        HelpNavigateCheckMethods.progress(self.driver)
        self.go_main(self.driver, flag_auth=False)
        # Выбираем товар и сохраняем его имя
        service_log.put("Выбираем товар и сохраняем его имя")
        good_name = self.get_name(self.get_element_navigate(self.driver, test_data["start_xpath_good"] % number_good))
        # Переход на страницу товара
        service_log.put("Переход на страницу товара")
        self.check_navigate_in_good_page(self.driver, test_data, number_good)
        # Жмем кнопку
        service_log.put("Жмем кнопку Связаться с продавцом")
        btn_to_call = self.get_element_navigate(self.driver, self.click_good.BTN_CALL_SELLER)
        btn_to_call.click()
        obj_send = self.get_element_navigate(self.driver, self.click_good.BTN_SEND)
        self.click_button(obj_send)
        # Проверяем, что перекинуло на авторизацию
        service_log.put("Проверяем, что перекинуло на авторизацию")
        #self.click_to_phone(self.driver)
        self.check_page_authorization(self.driver)

    @priority("medium")
    def test_as_seller_own_good(self, test_good=HelpNavigateCheckMethods.SHP_TO_GOOD):
        """
        Title: Я, как Продавец на картчоке по своему Активному товару, не могу "Связаться с продавцом" т.к. кнопка залочена
        """
        databases.db1.accounting.update_account_details_by_criteria(self.default_seller_id, "locale='ru'")
        self.user = databases.db1.accounting.get_user_by_account_id(self.default_seller_id)[0]
        self.shop = databases.db1.accounting.get_shop_details_by_shop_id(self.user["shop_id"])[0]

        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        self.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(self.default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=self.default_new_passwd, flag_auth=True)

        self.get_page(self.driver, self.path_shop.URL_SHOP % self.default_seller_id)
        self.check_navigate_in_good_page(self.driver, test_good, 1)
        self.data_good, good_str = self.get_good_data(self.driver)
        self.get_element_navigate(self.driver, self.click_good.BTN_CALL_SELLER_HOLD)

    @priority("low")
    def test_as_buyer_to_inactive_good(self):
        """
        Title: Я, как Покупатель, не могу написать продавцу сообщение по Не активному товару, т.к. "Связаться с продавцом" залочена
        """
        databases.db1.accounting.update_account_details_by_criteria(self.default_user_id, "locale='ru'")
        self.user = databases.db1.accounting.get_user_by_account_id(self.default_user_id)[0]
        self.shop = databases.db1.accounting.get_shop_details_by_shop_id(self.user["shop_id"])[0]

        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        self.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(self.default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=self.default_new_passwd, flag_auth=True)

        self.get_page(self.driver, self.path_shop.URL_SHOP % self.default_seller_id)
        list_good_id = self.get_good_id_from_page_source(self.driver, self.path_shop.TO_FIND_GOODS)
        self.good_id = list_good_id[0]
        ware_cassandra = databases.db7.warehouse.get_wares_by_ware_id(self.good_id)[0]
        self.update_data_content(ware_cassandra, self.deserialize_content(ware_cassandra['content']))
        # Меняем статус на BANNED
        services.warehouse.root.tframed.makeModeration(self.good_id, False, self.moderator_id)

        self.get_page(self.driver, self.path_good.URL_GOOD % self.good_id)
        self.data_good, good_str = self.get_good_data(self.driver)
        self.get_element_navigate(self.driver, self.click_good.BTN_CALL_SELLER_HOLD)

    @priority("medium")
    def test_as_buyer_cancel_msg(self, test_good=HelpNavigateCheckMethods.SHP_TO_GOOD):
        """
        Title: Я, как Покупатель, могу не Связываться с продавцом, выбрав Отменить, на форме ввода текста сообщения
        """
        databases.db1.accounting.update_account_details_by_criteria(self.default_user_id, "locale='ru'")
        self.user = databases.db1.accounting.get_user_by_account_id(self.default_user_id)[0]
        self.shop = databases.db1.accounting.get_shop_details_by_shop_id(self.user["shop_id"])[0]

        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        self.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(self.default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=self.default_new_passwd, flag_auth=True)

        self.get_page(self.driver, self.path_shop.URL_SHOP % self.default_seller_id)
        self.check_navigate_in_good_page(self.driver, test_good, 1)
        self.data_good, good_str = self.get_good_data(self.driver)
        btn_to_call = self.get_element_navigate(self.driver, self.click_good.BTN_CALL_SELLER)
        self.click_button(btn_to_call)

        # ищем товар с нужным id
        obj_good = self.get_element_navigate(self.driver, self.click_good.GOOD_BY_ID_POPUP % self.data_good['good_id'])
        self.check_express_card_good(obj_good, good_str)

        # проверяем фото товара
        good = (self.click_good.GOOD_BY_ID_POPUP % self.data_good['good_id'])
        img = (self.path_category.PATH_IMG % self.data_good['image'])
        self.get_element_navigate(self.driver, good + img)

        # Проверка текста в попапе
        popup_text = self.element_is_present(self.driver, self.check_good.POPUP_MSG_FROM_GOOD % '')
        Settings.clear_input_row(self.driver, popup_text)
        text = common_utils.random_string(length=50)
        popup_text.send_keys(text)
        obj_cancel = self.element_is_present(self.driver, self.click_good.BTN_CANCEL_CALL)
        self.click_button(obj_cancel)

        #После нажатия на "Отмена" я остаюсь на карточке этого же товара
        data_url = self.driver.current_url[self.driver.current_url.rfind('/') + 1:].encode('utf-8')
        self.assertIn(self.data_good["good_id"], data_url)

        # В чате с продавцом есть отправленное от меня сообщение и карточка товара. Проверить соответствие.
        self.get_page(self.driver, self.path_chat.URL_CHAT_WITH_USER % self.default_seller_id)
        last_msg = self.get_last_msg(self.driver)
        msg = "Свое сообщение о товаре='%s' совпадает с последним сообщением='%s'" % (text, last_msg)
        self.assertNotIn(text, last_msg, msg)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


#TODO: RT-876 Автотесты на 6.2 СООБЩЕНИЯ
class ChatPageMoveTo(HelpNavigateCheckMethods, HelpAuthCheckMethods, HelpChatCheckMethods):
    """
    Story: Переходы на странице чатов пользователя
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.default_seller_id = AccountingMethods.get_default_user_id(role='seller')
        cls.default_seller_own_id = AccountingMethods.get_default_user_id(role='seller_alien')
        cls.moderator_id = int(AccountingMethods.get_default_user_id(role='moderator'))

        databases.db1.accounting.update_account_details_by_criteria(cls.default_seller_id, "locale='ru'")
        cls.user = databases.db1.accounting.get_user_by_account_id(cls.default_seller_id)[0]

        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"],
                                             salt=cls.user["salt"])

        # Устанавливаем новый пароль для пользователя
        cls.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(cls.default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=cls.default_new_passwd, flag_auth=True)
        service_log.preparing_env(cls)

    @priority("must")
    def test_select_chat_from_chat_list(self):
        """
        Title: Я могу выбрать карточку контакта в списке чатов и увижу переписку с ним.
        """
        url_main = self.driver.current_url.encode('utf-8')
        header_chat = self.get_element_navigate(self.driver, self.click_main.HEADER_WIDGET_CHATS)
        self.element_click(self.driver, header_chat, change_page_url=True)
        url_chat = self.driver.current_url.encode('utf-8')
        self.assertNotEqual(url_main, url_chat, "Переход на страницу Сообщения не произошел, текущий урл:%s" % url_chat)
        self.progress(self.driver)
        recipient_id = url_chat[url_chat.rfind('/') + 1:]
        sender, recipient = self.get_sender_recipient_ids(self.user["id"], recipient_id)
        dialogs = databases.nutcracker.shards.messaging.get_all_message(sender, recipient)
        self.assertNotEqual(list(), dialogs, "Список диалогов пуст")
        service_log.put("В БД %s диалогов с пользователем" % len(dialogs))
        counter_dialogs = 0
        dialogs_web = self.driver.find_elements_by_xpath(self.check_chat.DIALOGS)
        count_dialogs_web = len(dialogs_web)
        #self.assertEqual(len(dialogs), count_dialogs_web, "Кол-во диалогов в БД=%s ,кол-во диалогов веб=%s" %
        #                 (len(dialogs), count_dialogs_web))
        position_dialog = count_dialogs_web
        for dialog in dialogs:
            txt_db = self.element_is_present(self.driver, self.check_chat.DIALOG % dialog).text
            txt_web = self.element_is_present(self.driver, self.check_chat.DIALOG_BY_POSITION % position_dialog).text
            txt_db_str = txt_db.encode('utf-8')
            self.assertEqual(txt_db, txt_web, "Сообщение '%s' находится не на %s месте" % (txt_db_str, position_dialog))
            messages_str = databases.nutcracker.shards.messaging.get_message(dialog)
            self.assertNotEqual(list(), messages_str, "Список сообщений пуст")
            msg_dict = json.loads(messages_str)
            messages = msg_dict[u'baseMessage'][u'items']
            msg_info = msg_dict[u'messageId']
            read_timestamp = str(msg_dict[u'readTimestamp'])
            read_time = self.timestamp_to_hm(read_timestamp)
            for message in messages:
                self.check_message(self.driver, dialog, message, databases.db7, databases.db1, msg_info, read_time, self.user['id'])
            counter_dialogs += 1
            position_dialog -= 1
            if counter_dialogs == 50:
                service_log.put("Успешно проверено 50 сообщений")
                break
        service_log.put("Проверено %s диалогов с пользователем" % counter_dialogs)

    @priority("medium")
    def test_move_to_shop(self):
        """
        Title: Я могу перейти в магазин контакта-продавца, кликнув на его аватар в области переписки
        """
        url_main = self.driver.current_url.encode('utf-8')
        header_chat = self.get_element_navigate(self.driver, self.click_main.HEADER_WIDGET_CHATS)
        self.element_click(self.driver, header_chat, change_page_url=True)
        url_chat = self.driver.current_url.encode('utf-8')
        self.assertNotEqual(url_main, url_chat, "Переход на страницу Сообщения не произошел, текущий урл:%s" % url_chat)
        self.progress(self.driver)
        recipient_id = url_chat[url_chat.rfind('/') + 1:]
        input_msg = self.get_element_navigate(self.driver, self.input_chat.SEND_CHAT)
        test_msg = time.ctime()
        input_msg.send_keys(test_msg)
        send_btn = self.get_element_navigate(self.driver, self.click_chat.BTN_SEND)
        self.element_click(self.driver, send_btn, change_page_url=False)
        time.sleep(self.time_sleep)
        self.driver.refresh()
        time.sleep(self.time_sleep)
        last_msg = self.element_is_present(self.driver, self.check_chat.LAST_MSG, wait=10).text.encode('utf-8')
        self.assertIn(test_msg, last_msg, "Последнее сообщение, не тестовое сообщение.")
        link_avatar_xpath = self.check_chat.LAST_MSG + self.check_chat.SENDER_AVATAR % ''
        link_avatar = self.get_element_navigate(self.driver, link_avatar_xpath)
        self.click_button(link_avatar)
        url_shop = self.driver.current_url.encode('utf-8')
        self.assertNotEqual(url_chat, url_shop, "Переход в магазин продавца не произошел. Текущий урл %s" % url_shop)
        self.get_element_navigate(self.driver, self.check_shop.INFO_URL % self.user["id"])

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class SearchUserInChatList(HelpNavigateCheckMethods, HelpAuthCheckMethods, HelpChatCheckMethods):
    """
    Story: Поиск пользователя в списке чатов
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.default_seller_id = AccountingMethods.get_default_user_id(role='seller')
        cls.default_seller_own_id = AccountingMethods.get_default_user_id(role='seller_alien')
        cls.moderator_id = int(AccountingMethods.get_default_user_id(role='moderator'))

        databases.db1.accounting.update_account_details_by_criteria(cls.default_seller_id, "locale='ru'")
        cls.user = databases.db1.accounting.get_user_by_account_id(cls.default_seller_id)[0]

        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        cls.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(cls.default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)
        # Переходим на страницу авторизации
        cls.get_auth_page(cls.driver)
        cls.click_to_phone(cls.driver)

        obj_phone, obj_password, obj_submit_button = cls.get_data_authorization(cls.driver)

        # Вводим данные на авторизацию
        cls.send_phone(phone_object=obj_phone, phone_number=cls.user["phone"][1:])
        cls.send_password(password_object=obj_password, password_number=cls.default_new_passwd)
        # Нажатие на кнопку авторизации
        cls.submit_button(obj_submit_button)

        url_main = cls.driver.current_url.encode('utf-8')
        header_chat = cls.get_element_navigate(cls.driver, cls.click_main.HEADER_WIDGET_CHATS)
        cls.click_button(header_chat)
        url_chat = cls.driver.current_url.encode('utf-8')
        cls.assertNotEqual(url_main, url_chat, "Переход на страницу Сообщения не произошел, текущий урл:%s" % url_chat)
        cls.progress(cls.driver)

    @skip('need_auto')
    @priority("medium")
    def test_full_name_search(self):
        """
        Title: Я могу найти пользователя по полному имени и посмотреть чат с ним, выбрав его в результатах поиска.
        Очистив условия поиска я снова увижу все чаты своего чат-листа.
        """
        name_users = self.driver.find_elements_by_xpath(self.check_chat.GET_NAME_OPPONENTS)

    @skip('need_auto')
    @priority("medium")
    def test_part_name_search(self):
        """
        Title: Я могу найти всех пользователей из моего чат-листа в имени которых есть введенные мною символы и посмотреть
        один из найденных чатов, выбрав его карточку в результатах поиска
        """
        pass

    @skip('need_auto')
    @priority("medium")
    def test_not_found_name_search(self):
        """
        Title: Если по условиям поиска не найдено чатов, то в моем контакт-листе, отображается соответствующий текст.
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()

class NewChatInChatPage(HelpNavigateCheckMethods, HelpAuthCheckMethods, HelpChatCheckMethods):
    """
    Story: Я могу начать (добавить) новый чат с контактом из контакт-листа
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.default_seller_id = AccountingMethods.get_default_user_id(role='seller')
        cls.default_seller_own_id = AccountingMethods.get_default_user_id(role='seller_alien')
        cls.moderator_id = int(AccountingMethods.get_default_user_id(role='moderator'))

    @skip('need_auto')
    @priority("medium")
    def test_one(self):
        """
        Title: Новый чат с пользователем из списка избранных контактов
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class SendMessage(HelpNavigateCheckMethods, HelpAuthCheckMethods, HelpChatCheckMethods):
    """
    Story: Я могу отправить Сообщение собеседнику
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.default_seller_id = AccountingMethods.get_default_user_id(role='seller')
        cls.default_seller_own_id = AccountingMethods.get_default_user_id(role='seller_alien')
        cls.moderator_id = int(AccountingMethods.get_default_user_id(role='moderator'))

    @skip('need_auto')
    @priority("medium")
    def test_send_text_message(self):
        """
        Title: Я могу выбрать чат с собеседником и отправить ему текстовое сообщение
        """
        pass

    @skip('need_auto')
    @priority("medium")
    def test_send_empty_message(self):
        """
        Title: Я не могу отправить собеседнику пустое сообщение. Отображается текст "Введите сообщение"
        """
        pass

    @skip('need_auto')
    @priority("medium")
    def test_send_more_max_text_message(self):
        """
        Title: Я не могу отправить собеседнику сообщение в 1001 символ. Отображается предупреждающее сообщение
        (или введенный текст обрезается до 1000 символов)
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class SendGood(HelpNavigateCheckMethods, HelpAuthCheckMethods, HelpChatCheckMethods):
    """
    Story: Я могу отправить Товар собеседнику
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.default_seller_id = AccountingMethods.get_default_user_id(role='seller')
        cls.default_seller_own_id = AccountingMethods.get_default_user_id(role='seller_alien')
        cls.moderator_id = int(AccountingMethods.get_default_user_id(role='moderator'))

    @skip('need_auto')
    @priority("medium")
    def test_send_good_message_from_favorites(self):
        """
        Title: Я могу отправить собеседнику товар из списка товаров Избранное
        """
        pass

    @skip('need_auto')
    @priority("medium")
    def test_send_good_message_from_my_goods(self):
        """
        Title: Я могу отправить собеседнику товар из списка товаров Мои товары
        """
        pass

    @skip('need_auto')
    @priority("medium")
    def test_send_good_message_from_opponent_goods(self):
        """
        Title: Я могу отправить собеседнику товар из списка товаров собеседника
        """
        pass

    @skip('need_auto')
    @priority("medium")
    def test_send_good_message_no_goods(self):
        """
        Title: Если у меня нет товаров в избранном и нет своих товаров, и я пишу пользователю
        у которого тоже нет товаров, то отображается пустой вид диалога "Послать товар"
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class SendContact(HelpNavigateCheckMethods, HelpAuthCheckMethods, HelpChatCheckMethods):
    """
    Story: Я могу отправить Контакт из своего контакт-листа, собеседнику
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.default_seller_id = AccountingMethods.get_default_user_id(role='seller')
        cls.default_seller_own_id = AccountingMethods.get_default_user_id(role='seller_alien')
        cls.moderator_id = int(AccountingMethods.get_default_user_id(role='moderator'))

    @skip('need_auto')
    @priority("medium")
    def test_send_contact_message(self):
        """
        Title: Я могу отправить контакт из своего контакт-листа собеседнику
        """
        pass

    @skip('need_auto')
    @priority("medium")
    def test_send_contact_message_no_contacts(self):
        """
        Title: Если мой контакт-лист пуст, то я не могу отправить контакт собеседнику. Отображается пустой вид
        диалога "Послать контакт"
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class ReceiveMessage(HelpNavigateCheckMethods, HelpAuthCheckMethods, HelpChatCheckMethods):
    """
    Story: Я могу отправить Фото собеседнику
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.default_seller_id = AccountingMethods.get_default_user_id(role='seller')
        cls.default_seller_own_id = AccountingMethods.get_default_user_id(role='seller_alien')
        cls.moderator_id = int(AccountingMethods.get_default_user_id(role='moderator'))

    @skip('need_auto')
    @priority("medium")
    def test_send_photo_message_pc(self):
        """
        Title: Я могу отправить собеседнику фото, с ПК (...) (проверить и для PNG и JPEG до 10мб)
        """
        pass

    @skip('manual')
    @priority("medium")
    def test_send_photo_message_tablet(self):
        """
        Title: Я могу отправить собеседнику фото, с файлового менеджера планшета
        """
        pass

    @skip('manual')
    @priority("medium")
    def test_send_photo_message_tablet_camera(self):
        """
        Title: Я могу отправить собеседнику фото, с камеры планшета
        """
        pass

    @skip('need_auto')
    @priority("medium")
    def test_send_photo_message_incorrect_format(self):
        """
        Title: Я не могу отправить собеседнику фото некорректного формата. Отображается предупреждающее сообщение
        """
        pass

    @skip('need_auto')
    @priority("medium")
    def test_send_photo_message_more_max_large(self):
        """
        Title: Я не могу отправить собеседнику фото размер которого более 10мб . Отображается предупреждающее сообщение
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class ChatListView(HelpNavigateCheckMethods, HelpAuthCheckMethods, HelpChatCheckMethods):
    """
    Story: Чат-лист
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.default_seller_id = AccountingMethods.get_default_user_id(role='seller')
        cls.default_seller_own_id = AccountingMethods.get_default_user_id(role='seller_alien')
        cls.moderator_id = int(AccountingMethods.get_default_user_id(role='moderator'))

    @skip('need_auto')
    @priority("medium")
    def test_chat_with_contacts(self):
        """
        Title: Чат-лист состоит из контактов - карточек пользователей
        """
        pass

    @skip('need_auto')
    @priority("medium")
    def test_format_contact(self):
        """
        Title: Каждая {Карточка пользователя} отображает: Аватар, Имя и Текст последнего сообщения
        """
        pass

    @skip('need_auto')
    @priority("medium")
    def test_chat_list_all_my_opponent(self):
        """
        Title: В чат-листе я вижу всех пользователей с которыми у меня есть чат:
        Роль(любая) & статус(Активен OR Заблокирован) & есть чат с CurrentUser
        """
        pass

    @skip('need_auto')
    @priority("medium")
    def test_scroll_in_chat_list(self):
        """
        Title: При большом кол-ве чатов появляется слайдер и возможность скролить чат-лист
        """
        pass

    @skip('need_auto')
    @priority("medium")
    def test_more_opponent_in_chat_list(self):
        """
        Title: Проверить чат-лист с большим кол-вом чатов (>100шт).
        Чат-лист не должен тормозить и должен корректно грузиться при заходе на страницу
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class ChatView(HelpNavigateCheckMethods, HelpAuthCheckMethods, HelpChatCheckMethods):
    """
    Story: Область чата
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.default_seller_id = AccountingMethods.get_default_user_id(role='seller')
        cls.default_seller_own_id = AccountingMethods.get_default_user_id(role='seller_alien')
        cls.moderator_id = int(AccountingMethods.get_default_user_id(role='moderator'))

    @skip('need_auto')
    @priority("medium")
    def test_isible_last_tree_hundred_messages(self):
        """
        Title: Область чата отображает последние 300 сообщений с собеседником
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class ChatSearchView(HelpNavigateCheckMethods, HelpAuthCheckMethods, HelpChatCheckMethods):
    """
    Story: Чат-лист
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.default_seller_id = AccountingMethods.get_default_user_id(role='seller')
        cls.default_seller_own_id = AccountingMethods.get_default_user_id(role='seller_alien')
        cls.moderator_id = int(AccountingMethods.get_default_user_id(role='moderator'))

    @skip('need_auto')
    @priority("medium")
    def test_max_symbols_in_search_contact_list(self):
        """
        Title: Поле не принимает на поиск более 100 символов
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()