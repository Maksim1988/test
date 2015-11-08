# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Файл с классами для работы с Messaging worker.
#--------------------------------------------------------------------
import random
import funcy
from gen_py.InstantMessagesContent.ttypes import ContentItemDto, TextContentDto
from gen_py.InstantMessagesContentConstants.ttypes import ContentType
from gen_py.InstantMessagingWorker.ttypes import BaseInstantMessageDto, MarkDialogAsReadRequestDto
from support import service_log
from tests.MainClass import MainClass

__author__ = 's.trubachev'


class NewMessagingData(MainClass):
    """
    Статические данные свойственные только MessagingWorker: переменные, константы, названия классов и т.д.
    """
    pass


class NewMessagingMethods(NewMessagingData):

    @staticmethod
    def get_TextContentDto(text, locale="ru"):
        """ Получить объект для создания объекта текста.
        :param text: текст сообщения
        :param locale: локаль сообщения, type(string) [http://en.wikipedia.org/wiki/IETF_language_tag]
        :return: объект TextContentDto
        """
        text_cont = TextContentDto(text=text, locale=locale)
        service_log.put("Created ContentItemDto: %s" % str(text_cont))
        return text_cont

    @staticmethod
    def get_name_ContentType(number):
        """ Получить имя типа контента по номеру.
        :param number: номер типа контента
        :return: наименование типа контента
        """
        content_type_name = ContentType._VALUES_TO_NAMES[number]
        service_log.put("Get content type name: %s" % content_type_name)
        return content_type_name

    @staticmethod
    def get_number_ContentType(name):
        """ Получить номер типа контента по имени.
        :param name: имя типа контента
        :return: номер типа контента
        """
        content_type_number = ContentType._NAMES_TO_VALUES[name]
        service_log.put("Get content type number: %s" % content_type_number)
        return content_type_number

    @staticmethod
    def get_ContentType(param):
        """ Получить тип контента.
        :param param: номер контента или имя типа контента
        :return: имя типа или номер контента
        """
        if type(param) == str:
            return NewMessagingMethods.get_number_ContentType(param)
        elif type(param) == int:
            return NewMessagingMethods.get_name_ContentType(param)

    @staticmethod
    def create_dialog_id(user1=None, user2=None, users=None):
        """ Создать диалог для двух пользователей.
        Можно задать двух пользователей по отдельности или через список.
        WARNING: для чата пользователей действует правило: БольшийИдентификатор_МеньшийИдентификатор,
        :param user1: идентификатор пользователя отправляющего сообщение
        :param user2: идентификатор пользователя, которому было отправлено сообщение
        :param users: список пользователей (беруться только первые два пользователя)
        :return: идентификатор диалога
        """
        dialog_id = None
        if users is not None and user1 and user2 is None:
            users.sort()
            dialog_id = "%s_%s" % (users[0], users[1])
        elif users is None and user1 and user2 is not None:
            if int(user1) < int(user2):
                dialog_id = "%s_%s" % (user1, user2)
            else:
                dialog_id = "%s_%s" % (user2, user1)
        else:
            msg_error = "Not the correct format"
            service_log.error(msg_error)
            raise AssertionError(msg_error)
        service_log.put("Create dialog id = %s" % dialog_id)
        return dialog_id

    @staticmethod
    def parse_form_messageId(message_id):
        """ Распарсить идентификатор сообщения.
        :param message_id: идентификатор сообщения
        :return: словарь с данными
        """
        part_msg = message_id.split("@")
        data = part_msg[1].split("_")
        parse = {"dialog_id": part_msg[0],
                 "participant_id": data[0],
                 "sending_timestamp": data[1],
                 "hash": data[2]}
        service_log.put("Parse messageId: %s" % str(parse))
        return parse


    @staticmethod
    def get_BaseInstantMessageDto(owner_id, items):
        """ Создание объекта BaseInstantMessageDto, базового для отправки сообщения.
        :param owner_id: владелец сообщения
        :param items: содержимое сообщения, list(type(ContentItemDto))
        :return: объект BaseInstantMessageDto
        """

        base_inst = BaseInstantMessageDto(ownerId=owner_id, items=items)
        service_log.put("Created BaseInstantMessageDto: %s" % str(base_inst))
        return base_inst

    @staticmethod
    def get_ContentItemDto(cont_type, text=None, pict_id=None, user_id=None, deal_cont=None, ware_id=None,
                           flag_compact=True):
        """ Элемент сообщения.
        В зависимости от тип содержимого должно быть заполнено один из др.параметров.
        :param cont_type: тип контента, type(ContentType)
        :param text: текст, type(TextContentDto)
        :param pict_id: идентификатор изоюражения
        :param user_id: идентификатор пользователя
        :param deal_cont: сделка, type(DealContentDto)
        :param ware_id: идентификатор товара
        :param flag_compact: флаг определяет будут ли отсылаться параметры со значением None
        :return: type(ContentItemDto)
        """
        params = dict(contentType=cont_type, text=text, pictureId=pict_id, userId=user_id, dealContent=deal_cont,
                      wareId=ware_id)
        if flag_compact is True:
            params = funcy.compact(params)
        content_item = ContentItemDto(**params)
        service_log.put("Created ContentItemDto: %s" % str(content_item))
        return content_item

    def get_MarkDialogAsReadRequestDto(self, user_id=None, dialog_id=None, last_read_timestamp=None):
        """ Получить объект MarkDialogAsReadRequestDto.
        :param user_id: владелец диалога
        :param dialog_id: идентификатор диалога
        :param last_read_timestamp: время последнего прочитанного сообщения
        :return: объект MarkDialogAsReadRequestDto
        """
        p = MarkDialogAsReadRequestDto(user_id, dialog_id, last_read_timestamp)
        service_log.put("Created MarkDialogAsReadRequestDto: %s" % str(p))
        return p


class NewMessagingCheckMethods(NewMessagingMethods):

    def check_dialog_data(self, info_dialog, owner_id, recipient_id, count_message, start_timestamp_message,
                          end_timestamp_message, subject=None, start_timestamp=0):
        """ Проверка общей информации диалога.
        :param info_dialog:
        :param owner_id: отправитель
        :param recipient_id: получатель
        :param count_message: количество сообщений в отправленном диалоге
        :param start_timestamp_message: начальная точка диапазона
        :param end_timestamp_message: конечная точка диапазона
        :param subject:
        :param start_timestamp:
        """
        self.assertEqual(info_dialog["dialogId"]["sender"], owner_id)
        self.assertEqual(info_dialog["dialogId"]["receiver"], recipient_id)
        self.assertEqual(info_dialog["dialogId"]["subject"], subject)
        self.assertEqual(info_dialog["dialogId"]["startTimestamp"], start_timestamp)  # todo ???
        self.assertLessEqual(start_timestamp_message, int(info_dialog["lastAddedMessageTimestamp"]))
        #self.assertGreaterEqual(end_timestamp_message, int(info_dialog["lastAddedMessageTimestamp"])) # todo
        self.assertNotEqual(info_dialog["unreadMessages"], count_message)

    def check_message_info_for_text(self, info_message, owner_id, count_message=1):
        """ Проверка общей информации сообщения только для текстового сообщения
        :param info_message: данные из БД
        :param owner_id: отправитель сообщения
        :param item_size: количество сообщений
        :param count_message: количество сообщений
        """
        self.assertEqual(info_message["itemsSize"], count_message)
        self.assertEqual(info_message["ownerId"], owner_id)
        self.assertTrue(info_message["setItems"])
        self.assertTrue(info_message["setOwnerId"])
        self.assertEqual(len(info_message["items"]), count_message)

    def check_item_message_info_for_text(self, elem, name_cont_type, text_message, locale_name):
        """ Проверка элемента сообщения только с текстом.
        :param elem: данные из БД
        :param name_cont_type: название типа сообщения
        :param text_message: текст сообщения
        :param locale_name: локаль сообщения
        """
        self.assertEqual(elem["contentType"], name_cont_type)
        self.assertEqual(elem["userId"], 0)

        self.assertIsNone(elem["dealContent"])
        self.assertIsNone(elem["pictureId"])
        self.assertIsNone(elem["wareId"])

        self.assertFalse(elem["setDealContent"])
        self.assertFalse(elem["setPictureId"])
        self.assertFalse(elem["setUserId"])  # todo???
        self.assertFalse(elem["setWareId"])

        self.assertTrue(elem["setContentType"])
        self.assertTrue(elem["setText"])

        self.assertTrue(elem["text"]["setLocale"])
        self.assertTrue(elem["text"]["setText"])
        self.assertEqual(elem["text"]["locale"], locale_name)
        self.assertEqual(elem["text"]["text"], text_message)

    def check_message_meta(self, message_meta, owner_id, recipient_id, start_timestamp_message, end_timestamp_message,
                           start_timestamp=0, subject=None):
        """ Проверка мета информации сообщения.
        :param message_meta: метаданные сообщения
        :param owner_id: отправитель
        :param recipient_id: получатель
        :param start_timestamp_message: начальная точка диапазона
        :param end_timestamp_message: конечная точка диапазона
        :param start_timestamp:
        :param subject:
        """
        self.assertEqual(message_meta["receiver"], recipient_id)
        self.assertEqual(message_meta["sender"], owner_id)
        self.assertEqual(message_meta["subject"], subject)
        self.assertEqual(message_meta["startTimestamp"], start_timestamp)  # todo ??? равно 0
        self.assertLessEqual(start_timestamp_message, int(message_meta['sendingTimestamp']))
        #self.assertGreaterEqual(end_timestamp_message, int(message_meta['sendingTimestamp'])) # todo
        self.assertEqual(message_meta["participantId"], owner_id)