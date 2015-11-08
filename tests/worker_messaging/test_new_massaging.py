# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Tests for messaging worker.
#  Удалено:
#       getDealById,
#       getConversationsByUser,
#       getUserDeals,
#       getDealsWithUser,
#       sendDealMessage,
#       moveDealToArchive,
#       getAllWaresDeal,
#       getBuyerDeals
#
# Действующие методы:
#       markMessagesAsRead,
#       markDialogAsRead,
#       getMessageHistory,
#       getChatWithUser,
#       sendChatMessageToUser,
#       getUnreadReport,
#       getUserChats,
#       findAllOpponents,
#       generateTotalsReport,
#       generateTotalsReportPerDay,
#
# P.S: info by Fedor L. : 25.05.2015
#--------------------------------------------------------------------
import random
import time
from support import service_log
from support.utils.common_utils import json_to_dict
from support.utils.db import databases
from support.utils.thrift4req import services
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.worker_messaging.class_new_messaging import NewMessagingCheckMethods

__author__ = 's.trubachev'


class ClassSendChatMessageToUser(NewMessagingCheckMethods):

    @classmethod
    def setUp(cls):
        """ Настройка окружения и вспомогательные параметры """
        service_log.preparing_env(cls)

    def test_send_message_to_user_only_text(self):
        """ Проверка отправки тектового сообщения пользователю.
        Метод sendChatMessageToUser:
          Послать сообщение юзеру и создать чат если его не существует
          - Если при посылке произошли внутренние ошибки то будет  выброшено UnavailableException.
          - На некорректный запрос бужет выброшено BadRequestException.
          - Если сообщение будет послано в несуществующий диалог то будет выброшено NoSuchResourceException.
          - Ошибки посылки сообщения SendMessageException
        """
        service_log.run(self)

        # формируем и отправляем текстовое сообщение
        user1 = AccountingMethods.get_default_user_id("seller_alien")
        user2 = AccountingMethods.get_default_user_id("buyer")
        dialog_id = self.create_dialog_id(user1=user1, user2=user2)
        parse_dialog_id = dialog_id.split("_")
        owner_id = int(parse_dialog_id[0])
        recipient_id = int(parse_dialog_id[1])

        text_message = "Autotest_%s" % random.randint(1000, 1000000) + " testing message"
        name_cont_type = "TEXT"
        locale_name = "ru"

        cont_type = self.get_ContentType(name_cont_type)
        cont_text = self.get_TextContentDto(text_message, locale_name)
        items = [self.get_ContentItemDto(cont_type, text=cont_text)]
        message = self.get_BaseInstantMessageDto(owner_id, items)
        start_timestamp_msg = int(str(time.time()).replace(".", "") + "0")
        time.sleep(5)  # делаем задержку явной
        result = services.messaging.root.tframed.sendChatMessageToUser(message, recipient_id)

        # делаем выборку информации из БД
        end_timestamp_msg = int(str(time.time()).replace(".", "") + "0")
        info_dialog_not_parse = databases.nutcracker.shards.messaging.get_dialog_by_id(dialog_id)
        info_message_not_parse = databases.nutcracker.shards.messaging.get_message(result.messageId)

        # объявляем переменные для проверок
        info_dialog = json_to_dict(info_dialog_not_parse)
        info_message = json_to_dict(info_message_not_parse)

        item_iterator = info_message['baseMessage']["itemsIterator"][0]
        item = info_message['baseMessage']["items"][0]
        item_result = result.message.items[0]
        message_meta = info_message['messageId']

        parsed_message_id = self.parse_form_messageId(result.messageId)
        count_msg = 0

        # проверка информации диалога с заданной
        self.check_dialog_data(info_dialog, owner_id, recipient_id, count_msg, start_timestamp_msg,  end_timestamp_msg)

        # проверка общей информации сообщения
        self.check_message_info_for_text(info_message['baseMessage'], owner_id, count_message=1)
        self.check_message_meta(message_meta, owner_id, recipient_id, start_timestamp_msg, end_timestamp_msg)

        # проверка элемента сообщения только с текстом (в данном случае элемент только один)
        self.assertEqual(info_message['readTimestamp'], 0, "The message was someone to read.")
        self.check_item_message_info_for_text(item, name_cont_type, text_message, locale_name)
        self.check_item_message_info_for_text(item_iterator, name_cont_type, text_message, locale_name)

        # проверка информации диалога и информации вернувшейся из воркера
        msg1 = "The last added message time of the message not equal time creating dialog."
        msg2 = "Not the same owners of the dialogue"
        msg3 = "The message is not found in unread"
        self.assertEqual(info_dialog["lastAddedMessageTimestamp"], result.creationTimestamp, msg1)
        self.assertEqual(info_dialog["dialogId"]["sender"], result.message.ownerId, msg2)
        self.assertTrue(result.messageId in info_dialog["unreadMessages"], msg3)

        # проверка информации сообщения и информации вернувшийся от воркера
        self.assertEqual(result.readTimestamp, info_message['readTimestamp'])
        self.assertEqual(result.dialogId, dialog_id)
        self.assertEqual(parsed_message_id["hash"], message_meta["hash"])
        self.assertEqual(parsed_message_id["sending_timestamp"], str(message_meta["sendingTimestamp"]))
        self.assertEqual(parsed_message_id["participant_id"], str(message_meta["participantId"]))
        self.assertEqual(parsed_message_id["dialog_id"], dialog_id)

        self.assertEqual(result.message.ownerId, owner_id)

        # проверка элемента сообщения вернувшего воркером (в данном случае он один)
        self.assertEqual(item_result.contentType, cont_type)
        self.assertEqual(item_result.text.locale, locale_name)
        self.assertEqual(item_result.text.text, text_message)
        self.assertIsNone(item_result.dealContent)
        self.assertIsNone(item_result.pictureId)
        self.assertIsNone(item_result.userId)
        self.assertIsNone(item_result.wareId)

    @classmethod
    def tearDown(cls):
        """ Завершение работы тестов """
        service_log.end()