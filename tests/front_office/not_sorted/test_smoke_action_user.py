# -*- coding: utf-8 -*-
"""
Feature: Набор авто-smoke сценариев
Description: https://confluence.oorraa.net/pages/viewpage.action?pageId=6914393
"""
import random
import time

from support import service_log
from support.utils import common_utils
from support.utils.common_utils import run_on_prod, priority
from support.utils.db import databases
from support.utils.thrift4req import services
from tests.front_office.authorization.classes.class_authorization import AuthCheckMethods
from tests.front_office.messages_and_contacts.classes.class_chat import HelpChatMethods
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.goods.classes.class_good import HelpGoodCheckMethods
from tests.front_office.goods.classes.class_good_create import HelpGoodCreateMethods
from tests.front_office.main.classes.class_main_menu import MainMenuCheckMethods
from tests.front_office.settings.classes.class_profile_settings import HelpProfileSettingsMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate
from tests.front_office.messages_and_contacts.classes.class_user_contacts import HelpUserContactsMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods
from tests.front_office.data_navigation import MainPage, GoodPage
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.worker_messaging.class_new_messaging import NewMessagingMethods
from tests.worker_warehouse.class_warehouse import WarehouseMethods

__author__ = 's.trubachev'


class TestSmokeUserWork(HelpAuthCheckMethods, HelpLifeCycleCheckMethods, HelpGoodCheckMethods, AccountingMethods,
                        WarehouseMethods, MainMenuCheckMethods):
    """
    Story: Работа пользователя с сайтом
    """
    driver = None

    @run_on_prod(False)
    def check_menu_no_prod(self):
        """ Проверка главного меню.
        WARNING: Не запускается на проде.
        """
        # Составляем дерево разделов
        category_dict = services.categories.root.tframed.getVisibleLiteCatalogTree('ru')
        # Получаем данные корня "Каталог"
        sections = category_dict[1]
        section_id_list = self.get_categories_list(sections)  # Получаем список ID разделов
        section_tree = self.get_categories_tree(category_dict, section_id_list)
        self.check_main_menu_section(self.driver, section_tree)

    @classmethod
    def setUp(cls):
        """ Настройка окружения и вспомогательные параметры """
        cls.wares = cls.get_static_wares()
        cls.default_user = cls.get_default_user_id(role='seller_alien')
        cls.default_passwd = cls.get_default_password(1)
        cls.data_auths = databases.db1.accounting.get_data_user_by_id(user_id=int(cls.default_user))
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

    @priority("medium")
    def test_smoke_user_work(self):
        """
        Title: Тест сценария работы пользователя.
        Description: 1. Зайти на сайт oorraa.com.:
            Проверить наличие кнопки "Вход"
            Логотипа УУРРАА
            Пунктов меню, главного меню (Одежда | Обувь и акссесуары | и пр.)
        2. Кликнуть на карточку любого товара на странице:
            Проверить что перешли на нужный товар (название и наличие всех фото)
            Проверить что хлебные крошки отображаются корректно
            Проверить что имя продавца отображается корректно
            Проверить что кнопка "Связаться с продавцом" активная
        3. Кликнуть на "Вход" ---> выбрать авторизацию по телефону ---> ввести корректные данные:
            Проверить что зашли под нужным пользователем (имя и телефон)
            Проверить наличие иконок "Сообщения" и "Контакты"
        4. Выполнить поиск товара
            Проверить что товар найден в результатах поиска
            Кликнуть на его карточку:
        5. Связаться с продавцом
            По окончанию перейти в чат и проверить то в области переписки есть сообщение
        6. Добавить контакт в контакт-лист
            Проверить что контакт добавился
            По окончании нужно удалить добавленный в избранное, контакт
        7.  Выполнить Logout
            Проверить что логаут выполнен, есть кнопка "Вход"
        """
        service_log.run(self)
        ware_for_search = self.wares[0]

        # 1. Заходим на сайт и выполняем проверку главной страницы.
        self.go_to_main_page(self.driver)
        self.check_header_widget_visitor(self.driver)
        logo_main_page = self.driver.find_element_by_xpath(self.LOGO_HEADER_MAIN_PAGE)
        self.assertIsNotNone(logo_main_page, u"Not found logo in main page.")
        self.check_menu_no_prod()

        # 2. Кликнуть на карточку любого товара на странице
        # выбираем первый товар в разделе "Одежда"
        num_element = 1
        clothing_ware_1 = MainPage.Path.BLOCK_CLOTHING % num_element
        obj_clothing_ware_1 = self.get_element_navigate(self.driver, clothing_ware_1)
        name_ware_from_main_page = obj_clothing_ware_1.text
        obj_clothing_ware_1.click()

        breadcrumb_list = self.get_breadcrumb_list(self.driver)  # запоминаем хлебные крошки
        # выковыриваем идентификатор товара из url и берем по нему и по продовцу инфу из БД
        name_ware = self.get_element_navigate(self.driver, GoodPage.Check.TITLE_WARE)
        ware_id = name_ware.parent.current_url.split('/')[-1]
        db_ware_data = databases.db1.warehouse.get_wares_by_ware_id(ware_id)
        data_user = databases.db1.accounting.get_data_user_by_id(db_ware_data[0]["shop_id"])
        name = self.driver.find_element_by_xpath(GoodPage.Check.USER_NAME_SELLER)
        button = self.driver.find_element_by_xpath(GoodPage.Click.BTN_CALL_SELLER2)
        # проверка имени продавца, названия товара, наличия
        self.assertEqual(data_user[0]["display_name"], name.text)
        self.assertEqual(len(db_ware_data), 1, u"Find several ware with one id.")
        self.assertEqual(name_ware_from_main_page, name_ware.text)
        self.assertEqual(len(breadcrumb_list), 3, u"Does not match the number of levels of categories.")
        self.assertTrue(button.is_displayed(), u"Button is not active.")

        # 3. Переходим на страницу авторизации
        self.do_login(self.driver)
        #self.click_to_phone(self.driver)
        self.check_page_authorization(self.driver)  # Проверка страница авторизации
        # вводим данные на авторизацию и авторизовываемся
        user_phone = self.data_auths[0]["phone"][1:]
        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        self.send_password(password_object=obj_password, password_number=self.default_passwd)
        self.send_phone(phone_object=obj_phone, phone_number=user_phone)
        self.submit_button(obj_submit_button, sleep=3)

        # 4. Выполнить поиск товара
        # Получаем инпут поиска, кнопку поиска с главной страницы, вводим данные и жмем кнопку поиска
        input_search = self.get_element_navigate(self.driver, self.input_main.SEARCH)
        btn_search = self.get_element_navigate(self.driver, self.click_main.BTN_SEARCH)
        input_search.send_keys(ware_for_search["name"].decode('utf-8'))
        btn_search.click()
        # Проверяем, что перешли в результаты поиска
        self.get_element_navigate(self.driver, self.check_search.TITLE_SEARCH)
        # Ищем на странице товар, заданный в поиске и переходим на страницу товара, проверяем урл страницы и название
        path_ware = self.click_search.LNK_GOOD_WITH_HREF % (ware_for_search["id"], ware_for_search["name"])
        ware_in_search = self.get_element_navigate(self.driver, path_ware)
        ware_in_search.click()
        self.check_url_ware(ware_for_search["id"], self.driver.current_url)
        obj_ware_title = self.get_element_navigate(self.driver, self.check_good.TITLE_GOOD)
        self.assertEqual(self.get_name(obj_ware_title), ware_for_search["name"])

        # 5. Связаться с продавцом
        data_good, good_str = HelpChatMethods.get_good_data(self.driver)
        button_call = self.driver.find_element_by_xpath(GoodPage.Click.BTN_CALL_SELLER2)
        button_call.click()
        dialog_window = self.driver.find_element_by_xpath(GoodPage.Check.POPUP_MESSAGE_TO_SELLER)
        button_answer = self.driver.find_element_by_xpath(GoodPage.Click.BTN_ANSWER_TO_SELLER)

        self.assertIsNotNone(dialog_window, "Not found dialog window for answer seller!")
        self.assertTrue(button_answer.is_displayed(), "Button is not active.")
        text = common_utils.random_string(length=50)
        link_popup = self.check_good.POPUP_MSG_FROM_GOOD % HelpChatMethods.TEXT_MSG_TO_GOOD
        popup_text = self.get_element_navigate(self.driver, link_popup)

        HelpProfileSettingsMethods.clear_input_row(self.driver, popup_text) # очищаем сообщение
        popup_text.send_keys(text)
        button_answer.click()
        time.sleep(3)
        button_go_to_chat = self.driver.find_element_by_xpath(GoodPage.Click.BTN_GO_TO_CHAT)
        button_go_to_good_page = self.driver.find_element_by_xpath(GoodPage.Click.BTN_GO_TO_GOOD_PAGE)
        self.assertTrue(button_go_to_chat.is_displayed(), "Button 'go to chat' is not active.")
        self.assertTrue(button_go_to_good_page.is_displayed(), "Button 'go to good page' is not active.")
        button_go_to_chat.click()

        # В чате с продавцом есть отправленное сообщение и карточка товара. Проверить соответствие текста и товара.
        last_msg = HelpChatMethods.get_last_msg(self.driver)
        msg_error1 = "Экспресс карточка='%s' не совпадает с последним сообщением='%s'" % (good_str, last_msg)
        self.assertIn(good_str, last_msg, msg_error1)
        str_msg_to_good = HelpChatMethods.TEXT_MSG_TO_GOOD.replace(' ', '')
        msg_error2 = "Сообщение о товаре='%s' не совпадает с последним сообщением='%s'" % (str_msg_to_good, last_msg)
        self.assertIn(text, last_msg, msg_error2)

        # 6. Добавить контакт в контакт-лист
        HelpUserContactsMethods.click_in_contact(self.driver, ware_for_search["store_id"])

        # переходим в избранное и удаляем пользователя
        self.get_page(self.driver, self.path_user_contact.URL_FAVORITES_USERS)
        data_user = databases.db1.accounting.get_data_user_by_id(ware_for_search["store_id"])
        HelpUserContactsMethods.delete_first_user_in_cl(self.driver, fav_user=data_user[0])

        # 7.  Выполнить Logout и выполнить проверку.
        self.driver.refresh()
        Navigate.progress(self.driver)
        self.logout(self.driver)
        logo_main_page = self.driver.find_element_by_xpath(self.LOGO_HEADER_PAGE)
        self.assertIsNotNone(logo_main_page, u"Not found logo in main page.")
        self.go_to_main_page(self.driver)
        self.check_header_widget_visitor(self.driver)
        self.check_menu_no_prod()

    @classmethod
    def tearDown(cls):
        """ Завершение работы тестов """
        cls.driver.quit()
        service_log.end()


class TestSmokeUserMessage(HelpAuthCheckMethods, HelpLifeCycleCheckMethods, HelpGoodCheckMethods, AccountingMethods,
                           MainMenuCheckMethods, AuthCheckMethods, NewMessagingMethods, HelpChatMethods):
    """
    Story: Работа с сообщениями пользователем
    """
    driver = None

    @classmethod
    def send_text_message(cls, owner_id, recipient_id):
        """
        Title: Отправить текстовое сообщение.
        Description: Генерируем произвольное текстовое сообщение, создаем объекты и отправляем воркеру.
        """
        cont_type = cls.get_ContentType("TEXT")
        text_message = u"Autotest_%s" % random.randint(1000, 1000000) + " testing message"
        cont_text = cls.get_TextContentDto(text_message, "ru")
        items = [cls.get_ContentItemDto(cont_type, text=cont_text)]
        message = cls.get_BaseInstantMessageDto(owner_id, items)
        services.messaging.root.tframed.sendChatMessageToUser(message, recipient_id)
        return text_message

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()

        # Настройка окружения и вспомогательные параметры
        cls.default_owner_id = int(cls.get_default_user_id(role='seller'))
        cls.default_user1_id = int(cls.get_default_user_id(role='buyer'))
        cls.default_user2_id = int(cls.get_default_user_id(role='seller_alien'))
        cls.new_messages = 2  # т.к. посылается по одному сообщения от двух разных пользователей
        cls.owner = databases.db1.accounting.get_user_by_account_id(cls.default_owner_id)[0]
        cls.user1 = databases.db1.accounting.get_user_by_account_id(cls.default_user1_id)[0]
        cls.user2 = databases.db1.accounting.get_user_by_account_id(cls.default_user2_id)[0]
        cls.default_passwd = cls.get_default_password(1)
        result = services.messaging.root.tframed.getUnreadReport(cls.default_owner_id)
        cls.unread_message = result.unreadChatMessagesCount
        cls.message1 = cls.send_text_message(cls.default_user1_id, cls.default_owner_id)
        cls.message2 = cls.send_text_message(cls.default_user2_id, cls.default_owner_id)
        service_log.preparing_env(cls)

    @run_on_prod(False)
    @priority("medium")
    def test_smoke_user_message(self):
        """
        Title: Тест сценарий отправки сообщения пользователем.
        Description: Предусловие:
            Перед тестом отправить (через api), пользователю под которым будет выполняться тест (Пользователь),
            два сообщения с текстом от разных контактов (Собеседник1 и Собеседник2)
            Есть два пользователя, от которых будет отправляться сообщения пользователю,
            под которым проходим тест (Собеседник 1 и Собеседник2)
            Существует пользователь зарегистрированный по e-mail - под ним будет выполняться тест (Пользователь).
        Шаги:
            1) Авторизоваться Пользователем через e-mail
                - Проверить, что отображается главная страница
                - Проверить наличие иконки 2х непрочитанных сообщений
            2) Перейти в "Сообщения":
                - Проверяем, что находимся на странице Сообщения с пользователем из предусловия,
                    который последним отправил сообщение (Собеседник2)
                - Проверяем, что в области переписки есть это сообщение и имя пользователя сообщения
                Проверяем, что счетчик непрочитанных сообщений в шапке, уменьшился на 1
                Проверяем, что в карточке с Собеседником2 нет иконки непрочитанных сообщений
                Проверяем, что  есть иконка 1 непрочитанного сообщения в карточке пользователя,
                    который первым отправлял сообщение (Собеседник1)
            3) Перейти на карточку Собеседника1
                Проверяем, что находимся на странице Сообщения с (Собеседник1)
                Проверяем, что в области переписки есть это сообщение  и имя пользователя сообщения
                Проверяем, что счетчик непрочитанных сообщений в шапке, исчез
                Проверяем, что в карточке с Собеседником1 нет иконки непрочитанных сообщений
                Проверяем, что  среди контактов нет иконок непрочитанных сообщений
            4) Написать сообщение Собеседнику1 и отправить
                Проверить, что сообщение отображается в области переписки, есть две галочки (сообщение пришло на сервер)
                Удостовериться что сообщение пришло на сервер.
            5) Выйти из аккаунта, со страницы "Сообщения"
                Проверить, что отображается страница Вход по электронная почта
        """
        service_log.run(self)

        # 1) Авторизоваться Пользователем через e-mail и проверить успешность операции.
        self.go_to_main_page(self.driver)
        self.click_reg_and_auth(self.driver)
        self.click_tab_login(self.driver)
        auth_form = self.get_auth_email_form(self.driver)
        auth_form["email_input"].send_keys(self.owner['email'])
        auth_form["password_input"].send_keys(self.default_passwd)
        self.element_click(self.driver, auth_form["login_btn"])
        self.check_header_widget_seller(self.driver, self.owner["id"])

        # Проверка количества новых сообщений в мессенждере
        msg_error1 = u"The message counter is not increased by %s" % self.new_messages
        msg_error2 = u"The message counter is decreased by 1"

        result = self.get_element_navigate(self.driver, self.check_main.ALL_NUMERATE_MSG)
        self.assertEqual(int(self.unread_message) + int(self.new_messages), int(result.text), msg_error1)

        # 2) Перейти в "Сообщения"
        self.driver.refresh()
        Navigate.progress(self.driver)
        obj_msgs = self.get_element_navigate(self.driver, self.check_main.ABSTRACT_MSG)
        obj_msgs.click()
        time.sleep(3)
        last_msg_for_user2 = self.get_last_msg2(self.driver)
        info_msg = last_msg_for_user2.split("\n")
        self.assertEqual(self.message2, info_msg[2], u"Not found message %s" % self.message2)
        #self.assertEqual(self.unread_message + (self.new_messages-1), int(result.text), msg_error2) # TODO
        self.assertEqual(self.user2['display_name'], info_msg[1], "Not found user2 %s" % self.user2['display_name'])

        # Warning: пользователи в чате нумеруются с нуля
        obj_counter_msgs_user2 = self.element_is_none(self.driver, self.check_main.COUNTER_MSG_USER % 0)
        obj_counter_msgs_user1 = self.get_element_navigate(self.driver, self.check_main.COUNTER_MSG_USER % 1)
        self.assertGreaterEqual(int(obj_counter_msgs_user1.text), 1)
        self.assertIsNone(obj_counter_msgs_user2)

        # 3) Перейти на карточку Собеседника1
        obj_counter_msgs_user1.click()
        time.sleep(3)
        last_msg_for_user1 = self.get_last_msg2(self.driver)
        info_msg = last_msg_for_user1.split("\n")
        self.assertEqual(self.message1, info_msg[2], u"Not found message %s" % self.message2)
        #self.assertEqual(self.unread_message, int(result.text), msg_error2) # TODO
        self.assertEqual(self.user1['display_name'], info_msg[1], u"Not found user2 %s" % self.user1['display_name'])

        obj_counter_msgs_user1 = self.element_is_none(self.driver, self.check_main.COUNTER_MSG_USER % 0)
        obj_counter_msgs_user2 = self.element_is_none(self.driver, self.check_main.COUNTER_MSG_USER % 1)
        self.assertIsNone(obj_counter_msgs_user1)
        self.assertIsNone(obj_counter_msgs_user2)

        # 4) Написать сообщение Собеседнику1 и отправить
        obj_area_text = self.get_element_navigate(self.driver, self.check_main.AREA_FOR_SEND_MSG)
        message_answer = "Autotests answer %s" % int(random.randint(10, 10000000))
        obj_area_text.send_keys(message_answer)
        obj_area_text = self.get_element_navigate(self.driver, self.click_chat.BTN_ANSWER)
        obj_area_text.click()
        time.sleep(3)
        last_msg_for_owner = self.get_last_msg2(self.driver)
        info_msg = last_msg_for_owner.split("\n")
        self.assertEqual(message_answer, info_msg[2], u"Not found message %s" % self.message2)
        self.assertEqual(self.owner['display_name'], info_msg[1], u"Not found owner %s" % self.owner['display_name'])

        # 5) Выйти из аккаунта, со страницы "Сообщения"
        self.driver.refresh()
        Navigate.progress(self.driver)
        self.logout(self.driver)
        logo_main_page = self.driver.find_element_by_xpath(self.LOGO_HEADER_PAGE)
        self.assertIsNotNone(logo_main_page, u"Not found logo in main page.")
        self.get_auth_email_form(self.driver)

    @classmethod
    def tearDown(cls):
        """ Завершение работы тестов """
        cls.driver.quit()
        service_log.end()


class TestSmokeUserSettings(HelpAuthCheckMethods, HelpLifeCycleCheckMethods, HelpGoodCheckMethods, AccountingMethods,
                            AuthCheckMethods, HelpChatMethods, HelpProfileSettingsMethods, HelpGoodCreateMethods):
    """
    Story: Работа пользователя с настройками
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()

        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = int(cls.get_default_user_id(role='seller_alien'))
        cls.user = databases.db1.accounting.get_user_by_account_id(cls.default_user_id)[0]
        cls.default_passwd = cls.get_default_password(1)

    @run_on_prod(False)
    @priority("medium")
    def test_smoke_user_settings(self):
        """
        Title: Тест сценарий изменений настроек пользователя.
        Description:
            1) Авторизоваться пользователем
            2) Перейти на страницу "Настройки"
                - Проверить, что отображаемые данные  = тому что в базе (включая аватар)
                - Проверить, что Имя и Аватар отображаемом в виджете "Профиль пользователя" = тому что в базе
            3) Изменить Имя пользователя и пол
                - Проверить что изменения отображаются и в базе и в интерфейсе
            4) Изменить аватар (старый удалить)
                - Проверить, что отображается заглушка фото (в настройках и в профиле продавца)
            5) Изменить аватар (добавить новый)
                - Проверить, что отображается новая фото (в настройках и в профиле продавца)
        """

        # 1) Авторизоваться Пользователем через e-mail и проверить успешность операции.
        self.go_to_main_page(self.driver)
        self.click_reg_and_auth(self.driver)
        self.click_tab_login(self.driver)
        auth_form = self.get_auth_email_form(self.driver)
        auth_form["email_input"].send_keys(self.user['email'])
        auth_form["password_input"].send_keys(self.default_passwd)
        self.click_button(auth_form["login_btn"])

        # Перейти на страницу "Настройки"
        self.get_page(self.driver, self.path_settings.PATH_PROFILE_SETTINGS)
        profile = self.get_user_profile_form(self.driver, self.user)
        gender = self.get_gender_user2(self.driver, self.user["gender"])

        # Изменить Имя пользователя и пол
        self.clear_input_row(self.driver, profile["name_input"])
        new_name = common_utils.random_string()
        profile["name_input"].send_keys(new_name)
        gender_ui = self.set_gender(gender, self.user["gender"])
        self.click_button(profile["save_btn"])

        # Проверяем, что изменения вступили в силу, как в БД, так и в интерфейсе
        criteria = "gender='%s' and display_name='%s' and id=%s" % (gender_ui, new_name, self.user["id"])
        user_updated = databases.db1.accounting.get_user_by_criteria_only(criteria)[0]
        self.driver.refresh()
        Navigate.progress(self.driver)
        self.get_user_profile_form(self.driver, user_updated)
        self.get_gender_user(self.driver, user_updated["gender"])

        # Изменить аватар (старый удалить)
        btn_avatar = self.get_delete_avatar_button(self.driver)  # TODO: У пользователя уже должен быть аватар!
        btn_avatar.click()

        # Изменить аватар (добавить новый)
        img_path = self.IMG_AVATAR[0]
        add_img_btn = self.get_element_navigate(self.driver, self.click_my_goods.ADD_AVATAR)
        add_img_btn.click()
        self.add_photo(img_path)
        self.assertIsNotNone(self.get_delete_avatar_button(self.driver))

    @classmethod
    def tearDown(cls):
        """ Завершение работы тестов """
        cls.driver.quit()
        service_log.end()


class TestSmokeUserAddWare(HelpAuthCheckMethods, HelpLifeCycleCheckMethods, HelpGoodCheckMethods, AccountingMethods,
                           AuthCheckMethods, HelpChatMethods, HelpProfileSettingsMethods, HelpGoodCreateMethods):
    """
    Story: Добавление товара пользователем
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()

        # Настройка окружения и вспомогательные параметры
        cls.default_user_id = int(cls.get_default_user_id(role='seller_alien'))
        cls.user = databases.db1.accounting.get_user_by_account_id(cls.default_user_id)[0]
        cls.default_passwd = cls.get_default_password(1)
        cls.moderator_id = int(cls.get_default_user_id('moderator'))

    @run_on_prod(False)
    @priority("medium")
    def test_smoke_user_add_ware(self):
        """
        Title: Тест сценарий добавления пользователем товара.
        Description:
        1) Авторизоваться пользователем.
        2) Перейти на страницу "Мои товары", нажать "Добавить товар":
            - Проверить, что отображается форма добавления товара;
        3) Создать товар со всеми заполненными полями + 5 фоток и нажать "Отправить" (Цена = 10 000р):
            - Проверить, что отображается страница "Мои товары"->"Активные" и добавленный товар в верхней позиции;
            - Проверить что товар в базу записаны все параметры товара, включая moderation_state и stock_state;
            - Проверить, что на карточке товара данные совпадают с БД. + фотки + профиль пользователя + хлебные крошки;
            - Проверить, что кнопка "Связаться с продавцом" не активная;
            - Проверить, что есть плашка "Это ваш товар";
            - Проверить что товар отображается в каталоге, в своей подкатегории;
            - Проверить, что товар не отображается на "Главной".
        4) Через базу или api эмулировать, что товар прошел модерацию (Изменить moderation_state):
            - Проверить, что товар отображается на главной странице.
        5) Через "Мои товары"  перенести товар в неактивные:
            - Проверить, что товар присутствует в "Мои Товары"->"Неактивные";
            - Проверить, что в базе изменилось состояние товара stock_state;
            - Проверить, что товар не отображается на "Главной";
            - Проверить, что товар не отображается в своей подкатегории.
        """

        # 1) Авторизоваться Пользователем через e-mail
        self.go_to_main_page(self.driver)
        self.click_reg_and_auth(self.driver)
        self.click_tab_login(self.driver)
        auth_form = self.get_auth_email_form(self.driver)
        auth_form["email_input"].send_keys(self.user['email'])
        auth_form["password_input"].send_keys(self.default_passwd)
        self.click_button(auth_form["login_btn"])

        # 2) Перейти на страницу "Мой магазин", нажать "Добавить товар"
        self.get_page(self.driver, self.path_shop.URL_SHOP % self.user["id"])
        add_ware = self.get_element_navigate(self.driver, self.click_shop.ADD_WARE_FROM_MY_SHOP)
        add_ware.click()

        # 3) Создать товар со всеми заполненными полями + 5 фоток и нажать "Отправить" (Цена = 10 000р)
        require_fields = self.REQUIRE_FIELDS_ETALON
        select_country = self.COUNTRY
        select_color = self.SELECT_COLOR
        select_material = self.SELECT_MATERIAL
        require_category = self.REQUIRE_CATEGORY
        text_input = self.LIST_TEXT_INPUT
        text_input['price']['data'] = "10000"

        # добавляем фото
        for img_path in self.IMG_PATH_LIST_MAX:
            add_img_btn = self.get_element_navigate(self.driver, self.click_my_goods.ADD_PHOTO)
            add_img_btn.click()
            self.add_photo(img_path)

        # выбираем категорию
        xpath_category = self.click_my_goods.PATH_REQUIRE_FIELDS + self.click_my_goods.FIELD_CATEGORY
        self.select_category(self.driver, require_category, xpath_category)

        # заполняем имя и минимальную партию
        xpath_name = self.click_my_goods.PATH_REQUIRE_FIELDS + self.input_my_goods.ADD_GOOD_NAME
        xpath_min_stock = self.click_my_goods.PATH_REQUIRE_FIELDS + self.input_my_goods.ADD_GOOD_MIN_STOCK
        name = self.get_element_navigate(self.driver, xpath_name)
        min_stock = self.get_element_navigate(self.driver, xpath_min_stock)
        name.send_keys(require_fields['name'])
        min_stock.send_keys(require_fields['min_stock'])
        self.check_name_fields(self.driver)

        # выбираем страну изготовитель
        xpath_country = self.click_my_goods.PATH_FIELDS + self.click_my_goods.FIELD_CATEGORY
        self.select_category(self.driver, select_country, xpath_country)

        # выбираем цвет
        xpath_color = self.click_my_goods.PATH_FIELDS + self.click_my_goods.SELECT_COLOR
        self.select_multi_cast(self.driver, select_color, xpath_color, self.click_my_goods.PLUS_BTN)

        # выбираем материал
        xpath_material = self.click_my_goods.PATH_FIELDS + self.click_my_goods.SELECT_MATERIAL
        self.select_multi_cast(self.driver, select_material, xpath_material, self.click_my_goods.PLUS_BTN)
        self.set_input_fields(self.driver, list_data=text_input)

        # парсим страницу добавления товара, чтобы получить идентификаторы фотографий товара
        params1 = self.driver, self.path_my_goods.PATH_IMG_ID_START, self.path_my_goods.PATH_IMG_ID_END
        list_img_id_source = self.get_all_id_ware(*params1)

        # Отсеиваем аватар:
        list_img_id = [index for index in list_img_id_source if len(index) < 33]

        self.get_category_id_from_page_source(*params1)

        # жмем опубликовать и проверяем, что перешли в "Активные"
        btn_publish = self.get_element_navigate(self.driver, self.click_my_goods.ADD_GOOD_BTN_PUBLISH)
        time.sleep(3)
        self.click_button(btn_publish)
        self.get_element_navigate(self.driver, self.check_my_goods.MENU_ACTIVE % "Активные")

        # проверяем короткую карточку товара в "Активных"
        price = text_input['price']['data']
        remains = text_input['remains']['data']
        data_good = self.get_data_add_good(require_category, require_fields, list_img_id, price, remains)
        self.check_shot_card_good(self.driver, self.check_my_goods.SHOT_CARD_GOOD_DATA % 1, data_good)

        # проверяем фото в короткой карточке товара
        params2 = self.check_my_goods.SHOT_CARD_GOOD_PHOTO, [list_img_id[0]], self.path_my_goods.PATH_IMG_ID_END
        xpath_img_list_short = self.get_xpath_img_list(*params2)
        # self.check_image_in_card(self.driver, xpath_img_list_short) #  todo!!!

        # переходим на страницу товара
        name_good = self.get_element_navigate(self.driver, self.click_my_goods.NAME_CARD_GOOD % 1)
        self.click_button(name_good)

        # проверяем данные на странице товара
        params3 = self.check_good.GALLERY_PREVIEW_PHOTO, list_img_id, self.path_good.PATH_IMG_ID_END
        xpath_img_list = self.get_xpath_img_list(*params3)
        self.check_image_in_card(self.driver, xpath_img_list)
        #xpp = "//div[@class='gallery__list']/div[@class='gallery__slide'][%s]/span/img[@class='gallery__preview']/@src"
        #for index in range(1, 4):
        #    res = self.get_element_navigate(self.driver, xpp % index)
        #    self.assertEqual(str(res) + "_s150x150", )

        self.check_card_good_require_fields(self.driver, data_good)
        self.check_card_good_text_fields(self.driver)
        self.check_selected_field(self.driver, select_color, self.check_good.COLOR)
        self.check_selected_field(self.driver, select_material, self.check_good.MATERIAL)

        # 4) Через базу или api эмулировать, что товар прошел модерацию (Изменить moderation_state)
        # Возьмём значение из БД только что созданного товара №1 по его идентификатору
        ware_id = self.get_current_url(self.driver).split('/')[-1]
        ware_data = databases.db1.warehouse.get_wares_by_ware_id(ware_id)
        ware_believed_postgresql = databases.db1.warehouse. get_moderation_by_ware_id(ware_data[0]["id"])
        service_log.put("Ware created from BD: %s" % ware_believed_postgresql)
        # Проверяем, что статус товара - BELIEVED.
        self.assertEqual(ware_believed_postgresql[0]['moderation_state_id'], 1, u"Ware moderation status not BELIEVED.")
        # Меняем статус
        ware_warehouse = services.warehouse.root.tframed.makeModeration(ware_id, True, self.moderator_id)
        # Возьмём значение из БД только что созданного товара №1 по его идентификатору
        ware_data2 = databases.db1.warehouse.get_wares_by_ware_id(ware_warehouse.wareId)
        ware_accepted_warehouse = databases.db1.warehouse. get_moderation_by_ware_id(ware_data2[0]["id"])

        service_log.put("Ware created from BD: %s" % ware_accepted_warehouse)
        # Проверяем, что статус изменился на ACCEPTED.
        self.assertEqual(ware_accepted_warehouse[0]['moderation_state_id'], 2, "Ware moderation status not ACCEPTED by BD")
        self.assertEqual(ware_warehouse.moderationState, 2, u"Ware moderation status not ACCEPTED by service")

        # Проверить, что товар отображается на главной странице
        time.sleep(60)  # добавленно кеширование на стороне backend'а - поэтому ставим задержку в 60 сек.
        self.go_to_main_page(self.driver)
        num_element = 1
        clothing_ware_1 = MainPage.Path.BLOCK_CLOTHING % num_element
        obj_clothing_ware_1 = self.get_element_navigate(self.driver, clothing_ware_1)
        self.assertEqual(require_fields['name'], obj_clothing_ware_1.text, "Not found ware in main page.")

        # 5) Через "Мои товары"  перенести товар в неактивные
        self.get_page(self.driver, self.path_my_goods.URL_MY_GOODS)
        check_box_ware = self.get_element_navigate(self.driver, self.check_my_goods.CHECKBOX_WARE % 1)
        check_box_ware.click()
        click_to_no_active = self.get_element_navigate(self.driver, self.click_my_goods.BTN_INACTIVE)
        click_to_no_active.click()
        inactive = self.get_element_navigate(self.driver, self.check_my_goods.MENU_INACTIVE % "Неактивные")
        inactive.click()
        time.sleep(3)
        # проверяем, "Мой магазин" -> "Неактивные"
        self.check_shot_card_good(self.driver, self.check_my_goods.SHOT_CARD_GOOD_DATA % 1, data_good)
        # проверяем состояние товара stock_state
        ware_postgresql = databases.db1.warehouse.get_wares_by_ware_id(ware_id)[0]
        service_log.put(u"Ware created from BD: %s" % ware_postgresql)
        self.assertEqual(ware_postgresql["stock_state_id"], 3, u"Ware stock state is not HIDDEN.")
        # Проверить, что товар не отображается на главной странице
        time.sleep(60)  # добавленно кеширование на стороне backend'а - поэтому ставим задержку в 60 сек.
        self.go_to_main_page(self.driver)
        num_element = 1
        clothing_ware_1 = MainPage.Path.BLOCK_CLOTHING % num_element
        obj_clothing_ware_1 = self.get_element_navigate(self.driver, clothing_ware_1)
        self.assertNotEqual(require_fields['name'], obj_clothing_ware_1.text, u"Ware found in main page.")

        # Переходим в подкатегорию - платья (id=617) и проверяем первый товар в списке
        self.get_page(self.driver, self.path_category.URL_PATH_ROOT_CATEGORY % 617)
        obj_ware = self.get_element_navigate(self.driver, self.click_main.PATH_GOOD % 1)
        self.assertNotEqual(require_fields['name'], obj_ware.text, u"Ware found in category page.")

    @classmethod
    def tearDown(cls):
        """ Завершение работы тестов """
        cls.driver.quit()
        service_log.end()