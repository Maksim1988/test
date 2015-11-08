# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Файл с классами для работы с Messaging worker.
#--------------------------------------------------------------------
import random
import funcy
from gen_py.Common.ttypes import CurrencyAmount
from gen_py.CommonConstants.ttypes import CurrencyType
from gen_py.InstantMessagesContent.ttypes import ContentItemDto, TextContentDto
from gen_py.InstantMessagesContent.ttypes import DealContentDto
from gen_py.InstantMessagesContentConstants.ttypes import ContentType, DealContentType
from gen_py.InstantMessagingWorker.ttypes import BaseInstantMessageDto
from gen_py.InstantMessagingWorkerConstants.ttypes import SendMessageErrorStatus
from support import service_log
from tests.MainClass import MainClass

__author__ = 's.trubachev'


class MessagingData(MainClass):
    """
    Статические данные свойственные только MessagingWorker: переменные, константы, названия классов и т.д.
    """
    pass


class MessagingMethods(MessagingData):

    @staticmethod
    def get_name_ContentType(number):
        """ Получить имя типа контента по номеру.
        :param number: номер типа контента
        :return: наименование типа контента
        """
        # todo: deprecated
        content_type_name = ContentType._VALUES_TO_NAMES[number]
        service_log.put("Get content type name: %s" % content_type_name)
        return content_type_name

    @staticmethod
    def get_number_ContentType(name):
        """ Получить номер типа контента по имени.
        :param name: имя типа контента
        :return: номер типа контента
        """
        # todo: deprecated
        content_type_number = ContentType._NAMES_TO_VALUES[name]
        service_log.put("Get content type number: %s" % content_type_number)
        return content_type_number

    @staticmethod
    def get_ContentType(param):
        """ Получить тип контента.
        :param param: номер контента или имя типа контента
        :return: имя типа или номер контента
        """
        # todo: deprecated
        if type(param) == str:
            return MessagingMethods.get_number_ContentType(param)
        elif type(param) == int:
            return MessagingMethods.get_name_ContentType(param)

    @staticmethod
    def get_TextContentDto(text, locale):
        """ Получить объект для создания объекта текста.
        :param text: текст сообщения
        :param locale: локаль сообщения, type(string) [http://en.wikipedia.org/wiki/IETF_language_tag]
        :return: объект TextContentDto
        """
        # todo: deprecated
        text_cont = TextContentDto(text=text, locale=locale)
        service_log.put("Created ContentItemDto: %s" % str(text_cont))
        return text_cont

    #@staticmethod
    #def get_PictureContentDto(pictureId):
    #    """ Получить объект изображения.
    #    :param pictureId: идентификатор изображения
    #    :return: объект PictureContentDto
    #    """
    #    pict_cont = PictureContentDto(pictureId=pictureId)
    #    service_log.put("Created PictureContentDto: %s" % str(pict_cont))
    #    return pict_cont

    @staticmethod
    def get_number_CurrencyType(name, all_item=False):
        """ Получить номер типа валюты по наименованию.
        :param name: наименование валюты
        :return: номер валюты
        """
        if all_item is True:
            service_log.put("Get CurrencyType numbers: %s" % CurrencyType._NAMES_TO_VALUES.keys())
            return CurrencyType._NAMES_TO_VALUES.keys()
        else:
            currency_type_number = CurrencyType._NAMES_TO_VALUES[name]
            service_log.put("Get CurrencyType number: %s" % currency_type_number)
            return currency_type_number

    @staticmethod
    def get_name_CurrencyType(number, all_item=False):
        """ Получить имя типа валюты по номеру.
        :param number: номер валюты
        :return: наименование валюты
        """
        if all_item is True:
            service_log.put("Get CurrencyType names: %s" % CurrencyType._VALUES_TO_NAMES.keys())
            return CurrencyType._VALUES_TO_NAMES.keys()
        else:
            currency_type_name = CurrencyType._VALUES_TO_NAMES[number]
            service_log.put("Get CurrencyType name: %s" % currency_type_name)
            return currency_type_name

    @staticmethod
    def get_CurrencyType(data, all_item=False):
        """ Получить тип валюты.
        :param data: строка или число
        :return: число или строка
        """
        if type(data) == str:
            return MessagingMethods.get_number_CurrencyType(data, all_item)
        elif type(data) == int:
            return MessagingMethods.get_name_CurrencyType(data, all_item)


    @staticmethod
    def get_CurrencyAmount(currency, significand, exponent):
        """ Получить объект денежной суммы. В десятичном экспоненциальном формате.
        :param currency: валюта, см.CurrencyType
        :param significand: мантисса денежной суммы
        :param exponent: экспонента денежной суммы
        :return: объект pricePerUnit
        """
        price_per = CurrencyAmount(currency=currency, significand=significand, exponent=exponent)
        service_log.put("Created CurrencyAmount: %s" % str(price_per))
        return price_per

    @staticmethod
    def get_number_DealContentType(name):
        """ Получить номер типа контента сделки по наименованию.
        :param name: наименование контента сделки
        :return: номер контента сделки
        """
        currency_type_number = DealContentType._NAMES_TO_VALUES[name]
        service_log.put("Get DealContentType number: %s" % currency_type_number)
        return currency_type_number

    @staticmethod
    def get_name_DealContentType(number):
        """ Получить имя типа контента сделки по номеру.
        :param number: номер контента сделки
        :return: наименование контента сделки
        """
        currency_type_name = DealContentType._VALUES_TO_NAMES[number]
        service_log.put("Get DealContentType name: %s" % currency_type_name)
        return currency_type_name

    @staticmethod
    def get_DealContentType(data):
        """ Получить типа контента сделки.
        :param data: строка или число
        :return: число или строка
        """
        if type(data) == str:
            return MessagingMethods.get_number_DealContentType(data)
        elif type(data) == int:
            return MessagingMethods.get_name_DealContentType(data)


    @staticmethod
    def get_DealContentDto(wareId, count, pricePerUnit, contentType):
        """ Получить объект контента сделки.
        Содержит в себе информацию с ценой и количеством штук товара.
        :param wareId: идентификатор товара
        :param count: количество товара
        :param pricePerUnit: цена, type(pricePerUnit)
        :param contentType: тип контекнта, type(DealContentType)
        :return: объект DealContentDto
        """
        deal_cont = DealContentDto(wareId=wareId, count=count, pricePerUnit=pricePerUnit, contentType=contentType)
        service_log.put("Created DealContentDto: %s" % str(deal_cont))
        return deal_cont

    @staticmethod
    def get_ContentItemDto(contentType, text=None, picture=None, dealContent=None, flag_compact=True):
        """ Элемент сообщения.
        В зависимости от тип содержимого должно быть заполнено один из др.параметров.
        :param contentType: тип контента, type(ContentType)
        :param text: текст, type(TextContentDto)
        :param picture: изоюражение, type(PictureContentDto)
        :param dealContent: сделка, type(DealContentDto)
        :param flag_compact: флаг определяет будут ли отсылаться параметры со значением None
        :return:
        """
        # todo: deprecated
        params = dict(contentType=contentType, text=text, picture=picture, dealContent=dealContent)
        if flag_compact is True:
            params = funcy.compact(params)
        content_item = ContentItemDto(**params)
        service_log.put("Created ContentItemDto: %s" % str(content_item))
        return content_item

    @staticmethod
    def get_BaseInstantMessageDto(ownerId, items):
        """ Создание объекта BaseInstantMessageDto, базового для отправки сообщения.
        :param ownerId: владелец сообщения
        :param items: содержимое сообщения, list(type(ContentItemDto))
        :return: объект BaseInstantMessageDto
        """
        # todo: deprecated
        base_inst = BaseInstantMessageDto(ownerId=ownerId, items=items)
        service_log.put("Created BaseInstantMessageDto: %s" % str(base_inst))
        return base_inst

    @staticmethod
    def get_number_SendMessageErrorStatus(name):
        """ Получить номер типа ошибки.
        :param name: наименование ошибки
        :return: номер ошибки
        """
        currency_type_number = SendMessageErrorStatus._NAMES_TO_VALUES[name]
        service_log.put("Get SendMessageErrorStatus number: %s" % currency_type_number)
        return currency_type_number

    @staticmethod
    def get_name_SendMessageErrorStatus(number):
        """ Получить имя типа ошибки.
        :param number: номер ошибки
        :return: наименование наименование
        """
        currency_type_name = SendMessageErrorStatus._VALUES_TO_NAMES[number]
        service_log.put("Get SendMessageErrorStatus name: %s" % currency_type_name)
        return currency_type_name

    @staticmethod
    def get_SendMessageErrorStatus(data):
        """ Получить тип ошибки.
        :param data: строка или число
        :return: число или строка
        """
        if type(data) == str:
            return MessagingMethods.get_number_SendMessageErrorStatus(data)
        elif type(data) == int:
            return MessagingMethods.get_name_SendMessageErrorStatus(data)

    @staticmethod
    def get_send_message_exception(tx):
        """ Получить тип ошибки.
        :param tx: исключение
        :return: статус ошибки, type(int)
        """
        return tx.status

    @staticmethod
    def create_simple_text_message(owner_id, text_message, text_locale, cont_type=1):
        """ Создаём простое текстовое сообщение.
        :return: объект сообщения
        """
        text_cont = MessagingMethods.get_TextContentDto(text=text_message, locale=text_locale)
        item_cont = MessagingMethods.get_ContentItemDto(contentType=cont_type, text=text_cont)
        items_cont = [item_cont]  # один элемент в сообщении
        message = MessagingMethods.get_BaseInstantMessageDto(owner_id, items_cont)
        service_log.put("Create simple text message: %s" % str(message))
        return message

    @staticmethod
    def create_simple_picture_message(owner_id, pict_id, cont_type=2):
        """ Создаём простое сообщение с изображением.
        :return: объект сообщения
        """
        pict_cont = MessagingMethods.get_PictureContentDto(pict_id)
        item_cont = MessagingMethods.get_ContentItemDto(contentType=cont_type, picture=pict_cont)
        items_cont = [item_cont]  # один элемент в сообщении
        message = MessagingMethods.get_BaseInstantMessageDto(owner_id, items_cont)
        service_log.put("Create simple picture message: %s" % str(message))
        return message

    @staticmethod
    def create_simple_deal_message(owner_id, ware_id, count, price, cont_deal, cont_type=3):
        """ Создаём простое сделочное сообщение сообщение.
        :param owner_id: идентификатор владельца
        :param ware_id: иждентификатор товара
        :param count: количество товаров
        :param price: цена товара
        :param cont_deal: тип сделочного сообщения
        :param cont_type: тип контента
        :return: объект сообщения
        """
        deal_content = MessagingMethods.get_DealContentDto(ware_id, count, price, cont_deal)
        item_cont = MessagingMethods.get_ContentItemDto(contentType=cont_type, dealContent=deal_content)
        items_cont = [item_cont]  # один элемент в сообщении
        message = MessagingMethods.get_BaseInstantMessageDto(owner_id, items_cont)
        service_log.put("Create simple deal message: %s" % str(message))
        return message

    @staticmethod
    def create_users_for_dialog(count_users=2):
        """ Создать новых пользователей для диалога.
        По факту идентификатор никак не привязан к пользователю. Это просто номер.
        # Warning: на больших данных есть шанс пересечения пользователей
        :param count_users: количество пользователей
        :return: список идентификаторов для диалога
        """
        # todo: deprecated
        ids = [random.randint(1000000, 2000000) for i in range(count_users)]
        service_log.put("Generate user id's: %s" % str(ids))
        return ids

    @staticmethod
    def organize_users(*users_id):
        """ Упорядочить элементы.
        Для текста и изображений, из которых формируется диалог.
        Группировка происходит от меньшего к большему.
        :param users_id: идентификаторы пользователей
        :return: список элементов
        """
        users_id = list(users_id)
        users_id.sort()
        service_log.put("Organize users: %s" % str(users_id))
        return users_id


class MessagingCheckMethods(MessagingMethods):

    def check_dialog_data(self, dialog_data, resulting_data, owner, opponent):
        """ Проверить данные записанные в диалог.
        :param dialog_data: данные диалога из redis
        :param resulting_data: данные от воркера
        :param owner: владелец
        :param opponent: оппонент
        """
        # Получить владельца сообщения
        msg = "The creation time of the message not equal time creating dialogue."
        get_owner = lambda res: res[res.rfind('@')+1:][:res[res.rfind('@')+1:].find('_')]

        # TODO: https://youtrack.home.oorraa.net/issue/M-266
        # self.assertEqual(dialog_data["dialogId"]["receiver"], opponent, "Not right opponentId.")
        # self.assertEqual(dialog_data["dialogId"]["sender"], owner, "Not right ownerId.")
        list_users = [dialog_data["dialogId"]["receiver"], dialog_data["dialogId"]["sender"]]
        self.assertTrue(owner in list_users, "Not found user.")
        self.assertTrue(opponent in list_users, "Not found user.")

        self.assertTrue(resulting_data.messageId in dialog_data['unreadMessages'], "Not found message in 'unread'.")
        self.assertEqual(str(owner), get_owner(resulting_data.messageId), "Not correct owner message.")
        self.assertEqual(dialog_data["lastAddedMessageTimestamp"], resulting_data.creationTimestamp, msg)
        # TODO: dialog_data["dialogId"]["subject"]

    def check_message_in_messages(self, resulting_data, dialog_messages):
        """ Проверить, что сообщение добавилось в список сообщений диалога.
        :param resulting_data: данные от воркера
        :param dialog_messages: сообщения диалога из redis
        """
        self.assertTrue(resulting_data.messageId in dialog_messages, "Not found created message.")

    def check_item_redis(self, item_redis, cont_type, deal=None, picture=None, text=None):
        """ Сравниваем данные из redis и заданные начальные данные.
        :param item_redis: данные элемента из redis
        :param cont_type: тип контента, type(string)
        :param deal: информация по сделке
        :param picture: информация о изображении сообщения
        :param text:  информация о тексте сообщения
        """
        for_equals = lambda source, name: (dict(), dict()) if source is None else (source, item_redis[name])
        # производим преобразования объектов изображения в словарь для удобства сравнения
        text, text_redis = for_equals(text, "text")
        picture, picture_redis = for_equals(picture, "picture")
        deal, deal_redis = for_equals(deal, "dealContent")

        self.assertEqual(item_redis['contentType'], cont_type, "Not right content type.")
        #self.assertDictEqual(picture_redis, picture, "Picture not equals.") # TODO: Заменить после бага:
        if (len(picture_redis) and len(picture)) != 0:
            self.assertEqual(picture_redis["pictureId"], picture["pictureId"], "Picture not equals.")
        #self.assertDictEqual(deal_redis, deal, "Deal content not equals.")  # TODO: Заменить после бага:
        if (len(deal_redis) and len(deal)) != 0:
            self.assertEqual(deal_redis["wareId"], deal["wareId"], "Ware not equals.")
            self.assertEqual(deal_redis["count"], deal["count"], "Count ware not equals.")
            msg_currency = "Currency  pricePerUnit ware not equals."
            msg_exponent = "Exponent  pricePerUnit ware not equals."
            msg_sign = "Significand  pricePerUnit ware not equals."
            self.assertEqual(deal_redis["pricePerUnit"]["currency"], deal["pricePerUnit"]["currency"], msg_currency)
            self.assertEqual(deal_redis["pricePerUnit"]["exponent"], deal["pricePerUnit"]["exponent"], msg_exponent)
            self.assertEqual(deal_redis["pricePerUnit"]["significand"], deal["pricePerUnit"]["significand"], msg_sign)

            self.assertEqual(deal_redis["contentType"], deal["contentType"], "ContentType deal ware not equals.")
        #self.assertDictEqual(text_redis, text, "Text not equals.") # TODO: Заменить после бага:
        if (len(text_redis) and len(text)) != 0:
            self.assertEqual(text_redis["locale"], text["locale"], "locale not equals.")
            self.assertEqual(text_redis["text"], text["text"], "Text not equals.")

    def check_item_worker(self, item_worker, cont_type, deal=None, picture=None, text=None):
        """ Сравниваем данные от воркера и заданные начальные данные.
        :param item_worker:  данные элемента от воркера
        :param cont_type: тип контента, type(string)
        :param deal: информация по сделке
        :param picture: информация о изображении сообщения
        :param text:  информация о тексте сообщения
        """
        # производим преобразования объектов текста в словарь для удобства сравнения
        #text_worker, text = (item_worker.text.__dict__, text) if text is not None else (dict(), dict())
        #picture_worker, picture = (item_worker.picture.__dict__, picture) if picture is not None else (dict(), dict())

        if deal is not None:
            msg_count = "Count not equals."
            msg_deal = "ContentType deal not equals."
            msg_ware = "Ware in deal not equals."
            msg_price = "Price currency in deal not equals."
            msg_exp = "Price exponent in deal not equals."
            msg_sign = "Price significand in deal not equals."
            self.assertEqual(item_worker.dealContent.count, deal["count"], msg_count)
            self.assertEqual(item_worker.dealContent.contentType,
                             self.get_DealContentType(deal["contentType"]), msg_deal)
            self.assertEqual(item_worker.dealContent.wareId, deal["wareId"], msg_ware)
            self.assertEqual(item_worker.dealContent.pricePerUnit.currency,
                             self.get_CurrencyType(deal["pricePerUnit"]["currency"]), msg_price)
            self.assertEqual(item_worker.dealContent.pricePerUnit.exponent, deal["pricePerUnit"]["exponent"], msg_exp)
            self.assertEqual(item_worker.dealContent.pricePerUnit.significand,
                             deal["pricePerUnit"]["significand"], msg_sign)

        if text is not None:
            text_worker = item_worker.text.__dict__
            self.assertDictEqual(text_worker, text, "Text not equals.")

        if picture is not None:
            picture_worker = item_worker.picture.__dict__
            self.assertDictEqual(picture_worker, picture, "Picture not equals.")

        self.assertEqual(item_worker.contentType, self.get_ContentType(cont_type), "Not right content type.")

    def check_item(self, item_worker, item_redis, cont_type, deal=None, picture=None, text=None):
        """ Проверяем элементы с заданными данными, данными от воркера и данными из redis.
        :param item_worker: данные элемента от воркера
        :param item_redis: данные элемента из redis
        :param cont_type: тип контентаб type(string)
        :param deal: информация по сделке
        :param picture: информация о изображении сообщения
        :param text:  информация о тексте сообщения
        """
        # TODO: https://youtrack.home.oorraa.net/issue/M-253, излишки данных должны быть удалены
        self.check_item_redis(item_redis, cont_type, deal, picture, text)
        self.check_item_worker(item_worker, cont_type, deal, picture, text)

    def check_message_data(self, message_data, owner, opponent, m_hash, sending_ts, subject):
        """ Проверяем информацию сообщению.
        :param message_data:
        :param owner: владелец
        :param opponent: оппонент
        :param m_hash: соль
        :param sending_ts: премя отправки
        :param subject: название сообщения
        """
        self.assertEqual(message_data['messageId']['hash'], m_hash, "Not correct hash.")
        self.assertEqual(message_data['messageId']['receiver'], opponent, "Not correct 'receiver'.")
        self.assertEqual(message_data['messageId']['sender'], owner, "Not correct sender.")
        self.assertEqual(message_data['messageId']['participantId'], owner, "Not correct participantId.")  # todo: это поле должны переименновать - это владелец
        self.assertEqual(message_data['messageId']['sendingTimestamp'], sending_ts, "Not correct 'sendingTimestamp'.")
        self.assertEqual(message_data['messageId']['startTimestamp'], 0, "Not correct startTimestamp.")  # TODO: https://youtrack.home.oorraa.net/issue/M-249, не должен быть равен нулю
        self.assertEqual(message_data['messageId']['subject'], subject, "Not correct subject.")

    def check_base_message_data(self, message_data, owner, item_count):
        """ Проверяем базовую информацию сообщения.
        :param owner: владелец
        :param item_count: количество элементов в сообщении
        """
        self.assertEqual(message_data['baseMessage']["itemsSize"], item_count, "Not right count items from message.")
        self.assertEqual(message_data['baseMessage']["ownerId"], owner, "Not right owner.")

