# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Tests.
#--------------------------------------------------------------------
import random
from ddt import ddt, data
from support import service_log
from support.utils.common_utils import run_on_prod, json_to_dict
from support.utils.db import databases
from support.utils.thrift4req import services
from tests.worker_messaging.class_messaging import MessagingCheckMethods


__author__ = 's.trubachev'

# ---------------------------------------------------------------------------------------------------------------------
# Список по приоритетам:
# 1) sendChatMessageToUser - Послать сообщение юзеру и создать чат если его не существуетю
# 2) sendDealMessage - Посылка сделочного сообщения
#
# 3) getConversationsByUser - Получить все "разговоры" (conversations) пользователя - это чаты и сделки пользователя.
# 4) getUnreadReport - Получить отчет о непрочитанных сообщениях для данного юзера
# 5) getDealsWithUser - Получить сделочные диалоги с данным оппонентом
# 6) getDealById - Получить информацию об отдельной сделке по ее идентификатору
# 7) getMessageHistory - получить историю
# 8) getChatWithUser - Получить информацию по диалогу пользователя с другим пользователем.
#
# 9) markMessagesAsRead - Пометить список сообщений как прочитанные
# 10) markDialogAsRead - Пометить все сообщения для данного юзера в данном диалоге как прочитанные
# 11) moveDealToArchive - диалог в архив
# ---------------------------------------------------------------------------------------------------------------------


@ddt
class TestSendChatMessageToUserText(MessagingCheckMethods):

    @classmethod
    def setUp(cls):
        """ Задаём параметры по умолчанию для тестов.
        """
        generate_text = lambda: "Autotest_sendChatMessageToUser_" + str(random.randint(1, 10000000000000))
        cls.locale = "ru"
        cls.cont_type_name = "TEXT"
        cls.owner_id, cls.opponent_id = cls.create_users_for_dialog(2)
        cls.cont_type = cls.get_ContentType(cls.cont_type_name)
        cls.text = generate_text()
        cls.text_old1 = generate_text()
        cls.text_old2 = generate_text()
        cls.pack_text = {'locale': cls.locale, 'text': cls.text}
        cls.msg1 = "The encoding is incorrect."
        cls.msg2 = "The locale is incorrect."

    @run_on_prod(False)
    def test_sendChatMessageToUser_only_text(self):
        """ Проверка метода на отправку сообщения в уже существующий диалог, содержащего только текст.
        Элемент сообщения один - текст.
        1) Проверяем FOLDER_DIALOGS и результат от воркера.
        2) Проверяем FOLDER_MESSAGES и результат от воркера.
        3) Проверяем FOLDER_MESSAGES и заданные в тесте данные.
        """
        # Создаём новый диалог и несколько сообщений для него
        message_old1 = self.create_simple_text_message(self.owner_id, self.text_old1, self.locale)
        message_old2 = self.create_simple_text_message(self.owner_id, self.text_old2, self.locale)
        services.messaging.root.tframed.sendChatMessageToUser(message_old1, self.opponent_id)
        services.messaging.root.tframed.sendChatMessageToUser(message_old2, self.opponent_id)
        # Отправляем сообщение с которым будем работать
        message = self.create_simple_text_message(self.owner_id, self.text, self.locale)
        result = services.messaging.root.tframed.sendChatMessageToUser(message, self.opponent_id)

        users_id = self.organize_users(self.owner_id, self.opponent_id)
        self.assertEqual("%s_%s" % (users_id[0], users_id[1]), result.dialogId, "Not right form dialog.")

        dialog_data = json_to_dict(databases.db2.messaging.get_dialog(users_id[0], users_id[1]))
        dialog_messages = databases.db2.messaging.get_all_message(users_id[0], users_id[1])
        message_data = json_to_dict(databases.db2.messaging.get_message(result.messageId))

        self.check_dialog_data(dialog_data, result, self.owner_id, self.opponent_id)
        self.check_message_in_messages(result, dialog_messages)
        self.check_item(message.items[0], message_data['baseMessage']['items'][0], self.cont_type_name,
                        text=self.pack_text)
        self.assertEqual(message_data['readTimestamp'], 0, "Not correct readTimestamp")  # 0 - т.к. не прочитано
        self.check_base_message_data(message_data, self.owner_id, 1)

    @run_on_prod(False)
    def test_sendChatMessageToUser_only_text_for_new_dialog(self):
        """ Проверка метода на отправку сообщения в уже существующий диалог, содержащего только текст.
        Элемент сообщения один - текст.
        1) Проверяем FOLDER_DIALOGS и результат от воркера.
        2) Проверяем FOLDER_MESSAGES и результат от воркера.
        3) Проверяем FOLDER_MESSAGES и заданные в тесте данные.
        """
        # Одновременно создаём новый диалог
        message = self.create_simple_text_message(self.owner_id, self.text, self.locale)
        result = services.messaging.root.tframed.sendChatMessageToUser(message, self.opponent_id)
        users_id = self.organize_users(self.owner_id, self.opponent_id)
        dialog_data = json_to_dict(databases.db2.messaging.get_dialog(users_id[0], users_id[1]))
        dialog_messages = databases.db2.messaging.get_all_message(users_id[0], users_id[1])
        message_data = json_to_dict(databases.db2.messaging.get_message(result.messageId))
        self.assertEqual("%s_%s" % (users_id[0], users_id[1]), result.dialogId, "Not right form dialog.")
        self.check_dialog_data(dialog_data, result, self.owner_id, self.opponent_id)
        self.check_message_in_messages(result, dialog_messages)
        self.check_item(message.items[0], message_data['baseMessage']['items'][0], self.cont_type_name,
                        text=self.pack_text)
        self.assertEqual(message_data['readTimestamp'], 0, "Not correct readTimestamp")  # 0 - т.к. не прочитано
        self.check_base_message_data(message_data, self.owner_id, 1)

    @run_on_prod(False)
    @data({"ch": "科技园太极图研究院军乐"},
          {"vi": "tự động thử nghiệm."},
          {"ru": "Тестирование."})
    def tests_sendChatMessageToUser_text_national_language(self, locale_text):
        """ Тестирование отправки сообщений на различных языках.
        1) Китай
        2) Вьетнам
        3) Кирилица
        :param locale_text: текст сообщения
        """
        # TODO: https://youtrack.home.oorraa.net/issue/M-193
        created_message = self.create_simple_text_message(self.owner_id, locale_text.values()[0], locale_text.keys()[0])
        result = services.messaging.root.tframed.sendChatMessageToUser(created_message, self.opponent_id)
        message = json_to_dict(databases.db2.messaging.get_message(result.messageId))
        # Сравнить заданные значения и значения в redis
        self.assertEqual(locale_text.values()[0], message['baseMessage']['items'][0]['text']['text'], self.msg1)
        self.assertEqual(locale_text.keys()[0], message['baseMessage']['items'][0]['text']['locale'], self.msg2)
        # Сравнить заданные значения и вернувшиеся значения от воркера
        self.assertEqual(locale_text.values()[0], result.message.items[0].text.text, self.msg1)
        self.assertEqual(locale_text.keys()[0], result.message.items[0].text.locale, self.msg2)


@ddt
class TestSendChatMessage(MessagingCheckMethods):

    @run_on_prod(False)
    def test_sendChatMessageToUser_several_items(self):
        pass

    @run_on_prod(False)
    def test_sendChatMessageToUser_equal_owner_and_opponent(self):
        """ Тест на то, что получатель и отправитель должны быть всегда разные люди.
        Создаём необходимый запрос, где ownerId = opponentId.
        Должна воспроизвестись ошибка.
        """
        text = "Autotest_sendChatMessageToUser_" + str(random.randint(1, 10000000000000))
        locale = "ru"
        cont_type_name = "TEXT"
        tx = None

        opponent_id = self.create_users_for_dialog(1)[0]
        owner_id = opponent_id
        cont_type = self.get_ContentType(cont_type_name)
        message = self.create_simple_text_message(owner_id, text, locale, cont_type)
        try:
            services.messaging.root.tframed.sendChatMessageToUser(message, opponent_id)
        except Exception, tx:
            service_log.put("Expected error: %s" % str(tx))
        self.assertIsNotNone(tx, "Not found error for 'ownerId = opponentId'.")


class TestSendChatMessageToUserPicture(MessagingCheckMethods):

    @classmethod
    def setUp(cls):
        generate_pict_id = lambda: "autotest_picture_" + str(random.randint(1000000, 2000000))
        cls.owner_id, cls.opponent_id = cls.create_users_for_dialog(2)
        cls.cont_type_name = "PICTURE"
        cls.pict_id = generate_pict_id()
        cls.pict_id_old1 = generate_pict_id()
        cls.pict_id_old2 = generate_pict_id()
        cls.pack_pict = {'pictureId': cls.pict_id}

    @run_on_prod(False)
    def test_sendChatMessageToUser_only_picture_for_new_dialog(self):
        """Проверка метода на отправку сообщения в новый диалог, содержащего только изображение.
        Элемент сообщения один - изображение.
        1) Проверяем FOLDER_DIALOGS и результат от воркера.
        2) Проверяем FOLDER_MESSAGES и результат от воркера.
        3) Проверяем FOLDER_MESSAGES и заданные в тесте данные.
        """
        # Одновременно создаём новый диалог
        message = self.create_simple_picture_message(self.owner_id, self.pict_id)
        result = services.messaging.root.tframed.sendChatMessageToUser(message, self.opponent_id)
        users_id = self.organize_users(self.owner_id, self.opponent_id)
        self.assertEqual("%s_%s" % (users_id[0], users_id[1]), result.dialogId, "Not right form dialog.")

        dialog_data = json_to_dict(databases.db2.messaging.get_dialog(users_id[0], users_id[1]))
        dialog_messages = databases.db2.messaging.get_all_message(users_id[0], users_id[1])
        message_data = json_to_dict(databases.db2.messaging.get_message(result.messageId))

        self.check_dialog_data(dialog_data, result, self.owner_id, self.opponent_id)
        self.check_message_in_messages(result, dialog_messages)
        self.check_item(message.items[0], message_data['baseMessage']['items'][0], self.cont_type_name,
                        picture=self.pack_pict)
        self.assertEqual(message_data['readTimestamp'], 0, "Not correct readTimestamp")  # 0 - т.к. не прочитано
        self.check_base_message_data(message_data, self.owner_id, 1)

    @run_on_prod(False)
    def test_sendChatMessageToUser_only_picture(self):
        """Проверка метода на отправку сообщения в новый диалог, содержащего только изображение.
        Элемент сообщения один - изображение.
        1) Проверяем FOLDER_DIALOGS и результат от воркера.
        2) Проверяем FOLDER_MESSAGES и результат от воркера.
        3) Проверяем FOLDER_MESSAGES и заданные в тесте данные.
        """
        # Создаём новый диалог и несколько сообщений для него
        message1 = self.create_simple_picture_message(self.owner_id, self.pict_id)
        message2 = self.create_simple_picture_message(self.owner_id, self.pict_id)
        services.messaging.root.tframed.sendChatMessageToUser(message1, self.opponent_id)
        services.messaging.root.tframed.sendChatMessageToUser(message2, self.opponent_id)

        message = self.create_simple_picture_message(self.owner_id, self.pict_id)
        result = services.messaging.root.tframed.sendChatMessageToUser(message, self.opponent_id)
        users_id = self.organize_users(self.owner_id, self.opponent_id)
        self.assertEqual("%s_%s" % (users_id[0], users_id[1]), result.dialogId, "Not right form dialog.")

        dialog_data = json_to_dict(databases.db2.messaging.get_dialog(users_id[0], users_id[1]))
        dialog_messages = databases.db2.messaging.get_all_message(users_id[0], users_id[1])
        message_data = json_to_dict(databases.db2.messaging.get_message(result.messageId))

        self.check_dialog_data(dialog_data, result, self.owner_id, self.opponent_id)
        self.check_message_in_messages(result, dialog_messages)
        self.check_item(message.items[0], message_data['baseMessage']['items'][0], self.cont_type_name,
                        picture=self.pack_pict)
        self.assertEqual(message_data['readTimestamp'], 0, "Not correct readTimestamp")  # 0 - т.к. не прочитано
        self.check_base_message_data(message_data, self.owner_id, 1)


@ddt
class TestSendChatMessageToUserDeal(MessagingCheckMethods):

    @classmethod
    def setUp(cls):
        generate_ware_id = lambda: "autotest_ware_" + str(random.randint(1000000, 2000000))
        cls.owner_id, cls.opponent_id = cls.create_users_for_dialog(2)
        cls.cont_type_name = "DEAL"
        cls.cont_type = cls.get_ContentType(cls.cont_type_name)
        cls.ware_id = generate_ware_id()
        cls.currency = random.choice(cls.get_CurrencyType(str(), True))
        cls.count = random.randint(1, 5000)
        cls.exponent = 2
        cls.significand = random.randint(1000, 10000)

    @run_on_prod(False)
    @data("DEAL_OFFER", "DEAL_ACCEPTION", "DEAL_COMPLETION", "DEAL_REJECTION", "PRICE_REQUEST")
    def test_sendDealMessage_deal_type(self, cont_deal_name="DEAL_OFFER"):
        """ Проверяем метод sendChatMessageToUser на создание различных сделочных сообщений.
        :param cont_deal_name: тип сделочного сообщения
        """
        self.cont_deal = self.get_DealContentType(cont_deal_name)
        self.pack_ware = {'wareId': self.ware_id, "contentType": cont_deal_name, "count": self.count,
                          "pricePerUnit": {"currency": self.currency,
                                           "exponent": self.exponent,
                                           "significand": self.significand}}
        price = self.get_CurrencyAmount(self.get_CurrencyType(self.currency), self.significand, self.exponent)
        message = self.create_simple_deal_message(self.owner_id, self.ware_id, self.count, price, self.cont_deal)
        result = services.messaging.root.tframed.sendChatMessageToUser(message, self.opponent_id)

        users_id = self.organize_users(self.owner_id, self.opponent_id)
        self.assertEqual("%s_%s" % (users_id[0], users_id[1]), result.dialogId, "Not right form dialog.")
        dialog_data = json_to_dict(databases.db2.messaging.get_dialog(users_id[0], users_id[1]))
        dialog_messages = databases.db2.messaging.get_all_message(users_id[0], users_id[1])
        message_data = json_to_dict(databases.db2.messaging.get_message(result.messageId))
        self.check_dialog_data(dialog_data, result, self.owner_id, self.opponent_id)
        self.check_message_in_messages(result, dialog_messages)
        self.check_item(message.items[0], message_data['baseMessage']['items'][0], self.cont_type_name,
                        deal=self.pack_ware)
        self.assertEqual(message_data['readTimestamp'], 0, "Not correct readTimestamp")  # 0 - т.к. не прочитано
        self.check_base_message_data(message_data, self.owner_id, 1)


@ddt
class TestSendDealMessage(MessagingCheckMethods):
    @classmethod
    def setUp(cls):
        generate_ware_id = lambda: "5a4a891081228fe5c2caf56b33f3ac77"  # идентификатор товара, задан статически
        cls.owner_dialog = cls.create_users_for_dialog(1)[0]
        cls.seller = 612
        cls.cont_type_name = "DEAL"
        cls.cont_type = cls.get_ContentType(cls.cont_type_name)
        cls.ware_id = generate_ware_id()
        cls.currency = random.choice(cls.get_CurrencyType(str(), True))
        cls.count = 1
        cls.exponent = 2
        cls.significand = random.randint(10000, 10000000)
        cls.status_exp_no_offer = "NO_OFFER_YET"

    @data("DEAL_OFFER", "PRICE_REQUEST")
    def test_sendDealMessage_new_dialog(self, cont_deal_offer_name):
        """ Проверка сделочных сообщений.
        Предложение о сделки для нового диалога.
        Warning: Начать сделочный диалог может только покупатель.
        """
        self.cont_deal_offer = self.get_DealContentType(cont_deal_offer_name)
        self.pack_deal = {"contentType": cont_deal_offer_name, "count": self.count, "wareId": self.ware_id,
                          "pricePerUnit": {"currency": self.currency,
                                           "exponent": self.exponent,
                                           "significand": self.significand}}
        cont_deal = self.cont_deal_offer
        price = self.get_CurrencyAmount(self.get_CurrencyType(self.currency), self.significand, self.exponent)
        message = self.create_simple_deal_message(self.owner_dialog, self.ware_id, self.count, price, cont_deal)

        result = services.messaging.root.tframed.sendDealMessage(message, self.seller, self.ware_id)
        dialog_data = json_to_dict(databases.db2.messaging.get_dialog_by_id(result.dialogId))
        self.check_dialog_data(dialog_data, result, self.owner_dialog, self.seller)
        self.assertEqual(dialog_data['dialogId']['subject'], self.ware_id, "Not correct subject message.")
        # Проверяем, что сообщение в списке всех сообщений диалога
        dialog_messages = databases.db2.messaging.get_all_message_by_id(result.dialogId)
        self.check_message_in_messages(result, dialog_messages)

        message_data = json_to_dict(databases.db2.messaging.get_message(result.messageId))
        params = (self.owner_dialog, self.seller, self.ware_id, dialog_data['dialogId']['startTimestamp'])
        self.assertEqual("%s_%s_%s_%s" % params, result.dialogId, "Not right form dialog.")
        self.check_item(message.items[0], message_data['baseMessage']['items'][0], self.cont_type_name,
                        deal=self.pack_deal)
        self.assertEqual(message_data['readTimestamp'], 0, "Not correct readTimestamp")  # 0 - т.к. не прочитано
        self.check_base_message_data(message_data, self.owner_dialog, 1)

    # TODO: тут есть ошибки: https://youtrack.home.oorraa.net/issue/M-315
    @data("DEAL_ACCEPTION", "DEAL_COMPLETION", "DEAL_REJECTION")
    def test_sendDealMessage_no_offer(self, cont_deal_name="DEAL_ACCEPTION"):
        """ Проверяем возвращаемый тип ошибки от sendDealMessage.
        Если тип сообщения не "DEAL_OFFER", "PRICE_REQUEST" - должен вернуться статус ошибки NO_OFFER_YET.
        Warning: Начать сделочный диалог может только покупатель.
        :param cont_deal_name: тип сделочного сообщения
        """
        self.cont_deal = self.get_DealContentType(cont_deal_name)
        price = self.get_CurrencyAmount(self.get_CurrencyType(self.currency), self.significand, self.exponent)
        message = self.create_simple_deal_message(self.owner_dialog, self.ware_id, self.count, price, self.cont_deal)
        tx = None
        try:
            services.messaging.root.tframed.sendDealMessage(message, self.seller, self.ware_id)
        except Exception, tx:
            status_from_worker = self.get_send_message_exception(tx)
            self.status_exp_no_offer = self.get_SendMessageErrorStatus(self.status_exp_no_offer)
            self.assertEqual(self.status_exp_no_offer, status_from_worker, "Does not match the error status.")
        self.assertIsNotNone(tx, "Not found error.")

    def test_sendDealMessage_not_right_owner(self):
        """ Проверяем возвращаемый тип ошибки от sendDealMessage.
        WARE_OWNER_MISMATCH = 2
        Warning: Начать сделочный диалог может только покупатель.
        :param cont_deal_name: тип сделочного сообщения
        """
        cont_deal_name = "DEAL_OFFER"
        self.seller = random.randint(100000, 10000000)
        self.cont_deal = self.get_DealContentType(cont_deal_name)
        price = self.get_CurrencyAmount(self.get_CurrencyType(self.currency), self.significand, self.exponent)
        message = self.create_simple_deal_message(self.owner_dialog, self.ware_id, self.count, price, self.cont_deal)
        tx = None
        try:
            services.messaging.root.tframed.sendDealMessage(message, self.seller, self.ware_id)
        except Exception, tx:
            status_from_worker = self.get_send_message_exception(tx)
            self.status_exp_no_offer = self.get_SendMessageErrorStatus(self.status_exp_no_offer)
            self.assertEqual(2, status_from_worker, "Does not match the error status 'WARE_OWNER_MISMATCH'.")
        self.assertIsNotNone(tx, "Not found error.")


    @run_on_prod(False)
    @data(0, -1, -30)
    def test_sendDealMessage_negative_number_count(self, count=50):
        """ Проверяем метод sendChatMessageToUser.
         Создание сделочного сообщения с количеством товара меньше 1.
        :param count: количество товаров
        """
        # TODO: M-299
        cont_deal_offer_name = "DEAL_OFFER"
        self.cont_deal_offer = self.get_DealContentType(cont_deal_offer_name)
        self.pack_deal = {"contentType": cont_deal_offer_name, "count": count, "wareId": self.ware_id,
                          "pricePerUnit": {"currency": self.currency,
                                           "exponent": self.exponent,
                                           "significand": self.significand}}
        cont_deal = self.cont_deal_offer
        price = self.get_CurrencyAmount(self.get_CurrencyType(self.currency), self.significand, self.exponent)
        message = self.create_simple_deal_message(self.owner_dialog, self.ware_id, count, price, cont_deal)
        tx = 0
        try:
            res = services.messaging.root.tframed.sendDealMessage(message, self.seller, self.ware_id)
        except Exception, tx:
            service_log.put("Expected error: %s" % str(tx))
            msg = "Not found error incorrect ware."
            self.assertNotEqual(tx.reason.find("Incorrect ware count: %s" % count), -1, msg)
        self.assertIsNotNone(tx, "Not found error for 'count ware < 1'.")

class TestGetChatWithUser(MessagingCheckMethods):
    @run_on_prod(False)
    def test_getChatWithUser(self):
        pass


class TestGetDealById(MessagingCheckMethods):
    @run_on_prod(False)
    def test_getDealById(self):
        pass


class TestGetConversationsByUser(MessagingCheckMethods):
    @run_on_prod(False)
    def test_getConversationsByUser(self):
        pass


class TestGetUnreadReport(MessagingCheckMethods):
    @run_on_prod(False)
    def test_getUnreadReport(self):
        pass


class TestGetDealsWithUser(MessagingCheckMethods):
    @run_on_prod(False)
    def test_getDealsWithUser(self):
        pass


class TestMoveDealToArchive(MessagingCheckMethods):
    @run_on_prod(False)
    def test_moveDealToArchive(self):
        pass
