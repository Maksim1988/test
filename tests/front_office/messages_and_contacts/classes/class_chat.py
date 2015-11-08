# coding=utf-8
import time

from support import service_log
from tests.MainClass import MainClass
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate


__author__ = 'm.senchuk'


class HelpChatData(MainClass):
    TEXT_MSG_TO_GOOD = "Меня интересует товар, как мне с вами связаться, чтобы приобрести партию?"


class HelpChatMethods(HelpChatData):

    @staticmethod
    def get_good_data(driver):
        """ Получить данные о товаре.
        :param driver: ссылка на драйвер
        :return: данные о товаре
        """
        path_img1 = Navigate.path_good.PATH_IMG_ID_START
        path_img2 = Navigate.path_good.PATH_IMG_ID_END
        img = Navigate.get_category_id_from_page_source(driver, path_img1, path_img2)[0]

        path_title = Navigate.check_good.TITLE_GOOD
        title = Navigate.get_element_navigate(driver, path_title).text.encode('utf-8').replace(' ', '')

        path_stock = Navigate.check_good.MIN_STOCK
        min_stock = Navigate.get_element_navigate(driver, path_stock).text.encode('utf-8').replace(' ', '')

        path_price = Navigate.check_good.PRICE
        price = Navigate.get_element_navigate(driver, path_price).text.encode('utf-8').replace(' ', '')

        good = driver.current_url[driver.current_url.rfind('/') + 1:].encode('utf-8')
        data_good = dict(image=img, title=title, min_stock=min_stock, price=price, good_id=good)
        good_str = data_good['title'] + "Заштуку" + data_good['price'] + "Мин.заказ" + data_good['min_stock']
        return data_good, good_str

    @staticmethod
    def get_sent_success_btn(driver):
        """
        Получить объекты кнопок На страницу товара и В чат
        Проверка сообщения об успешной отправке
        :param driver:
        :return:
        """
        Navigate.get_element_navigate(driver, Navigate.check_good.MSG_SENT_SUCCESS, mode=None)
        btn_to_good = Navigate.get_element_navigate(driver, Navigate.click_good.BTN_TO_CARD_GOOD, mode=None)
        btn_to_chat = Navigate.get_element_navigate(driver, Navigate.click_good.BTN_TO_CHAT, mode=None)
        return btn_to_good, btn_to_chat

    @staticmethod
    def get_last_msg(driver):
        """ Получить последние сообщение чата (удаляем пробелы и перенос строки)
        :param driver: ссфлка на драйвер
        :return:
        """
        link_msg = Navigate.check_chat.LAST_MSG
        return Navigate.get_element_navigate(driver, link_msg).text.encode('utf-8').replace(' ', '').replace('\n', '')

    @staticmethod
    def get_last_msg2(driver):
        """ Получить последние сообщение чата (не удаляем пробелы и переносы строки)
        :param driver: ссфлка на драйвер
        :return:
        """
        link_msg = Navigate.check_chat.LAST_MSG
        return Navigate.get_element_navigate(driver, link_msg).text.encode('utf-8')

    @staticmethod
    def timestamp_to_hm(timestamp):
        """
        Timestamp времени в чч:мм
        :param timestamp:
        :return:
        """
        if timestamp == '0' or timestamp == 0 or timestamp == '':
            return 0
        t = lambda x: x[1:] if x[0] == '0' else x
        hm_time = time.strftime("%H:%M", time.localtime(int(str(timestamp)[:-3])))
        hm_time = t(hm_time)
        return hm_time

    @staticmethod
    def get_sender_recipient_ids(id1, id2):
        """
        Возвращает идентификаторы владельца диалога и оппонетна диалога, по возрастанию.
        Меньший идентификатор владелец, больший оппонент
        :param id1:
        :param id2:
        :return:
        """
        if int(id1) < int(id2):
            sender = id1
            recipient = id2
        else:
            sender = id2
            recipient = id1
        return sender, recipient


class HelpChatCheckMethods(HelpChatMethods):
    def check_express_card_good(self, obj_good, good_str):
        """
        Проверка эксрпесс карточки товара
        :param obj_good:
        :param good_str:
        :return:
        """
        good = obj_good.text.encode('utf-8').replace(' ', '').replace('\n', '')
        # проверяем текстовые данные: название, мин. партия, цена
        self.assertEqual(good, good_str, "Текстовые данные не совпадают")

    def check_message(self, driver, dialog, message, link_db_ware, link_db_user, msg_info, read_time, user_id):
        """
        Проверить сообщение. Здесь определяется тип полученного сообщения, в зависимости от типа сообщения. Применяется
        соответствующая модель проверки.
        :param driver: вебдрайвер
        :param dialog: идентификатор диалога
        :param message: идентификатор сообщения
        :param link_db_ware: ссылка на БД товаров
        :param link_db_user: ссылка на БД пользователей
        :param msg_info: информация об отправителе
        :param read_time: информация о времени прочтения сообщения
        """
        self.check_message_info(driver, user_id, link_db_user, msg_info, read_time)
        type_message = message[u'contentType']
        if type_message == u'TEXT':
            self.check_text_message(driver, dialog, message)
        elif type_message == u'WARE':
            self.check_ware_message(driver, dialog, message, link_db_ware)
        elif type_message == u'PICTURE':
            self.check_picture_message(driver, dialog, message)
        elif type_message == u'USER':
            self.check_user_message(driver, dialog, message, link_db_user)
        else:
            service_log.warning("Undefined scheme checking message.")

    def check_message_info(self, driver, user_id, link_db_user, msg_info, read_time):
        """
        Проверить информацию о сообещнии, пользователя отправителя, время отправки , метку о прочтении если пользователь
        отправил сообщение, если получил сообщение метку не проверять
        :param driver: вебдрайвер
        :param dialog: идентификатор диалога
        :param message: идентификатор сообщения
        :param link_db_user: ссылка на БД пользователей
        :param msg_info: информация об отправителе
        :param read_time: информация о времени прочтения сообщения
        """
        user_sender_id = msg_info[u'participantId']
        user_sender = link_db_user.accounting.get_user_by_criteria_only("id=%s" % user_sender_id)[0]
        if user_sender["avatar_id"] is None:
            user_sender["avatar_id"] = 'no_ava'
        if read_time != 0:
            read_flag = Navigate.check_chat.READ_MSG
        else:
            read_flag = Navigate.check_chat.UNREAD_MSG
        send_time = self.timestamp_to_hm(msg_info[u'sendingTimestamp'])
        Navigate.element_is_present(driver, Navigate.check_chat.SENDER_AVATAR % user_sender["avatar_id"])
        Navigate.element_is_present(driver, Navigate.check_chat.SENDER_NAME % user_sender["display_name"])
        Navigate.element_is_present(driver, Navigate.check_chat.SEND_TIME % send_time)
        if user_id == user_sender_id:
            Navigate.element_is_present(driver, read_flag)

    def check_text_message(self, driver, dialog, message):
        """
        Проверить текстовое сообщение
        :param messages:
        :return:
        """
        service_log.put("Checking Text-message")
        text = message[u'text'][u'text'].encode('utf-8')
        Navigate.element_is_present(driver, Navigate.check_chat.TEXT_MSG % (dialog, text))

    def check_ware_message(self, driver, dialog, message, link_db):
        """
        Проверить сообщение-карточка товара
        :param messages:
        :return:
        """
        service_log.put("Checking Ware-message")
        ware_id = message[u'wareId'].encode('utf-8')
        ware = link_db.warehouse.get_wares_by_ware_id(ware_id)[0]
        info = ware[u'content']
        picture = info[u'pictures'][u'value'][0].encode('utf-8')
        title = info[u'title'][u'value'].encode('utf-8')
        p = [str(info[i][u'value'][u'significand']) for i in info if i == u'price']
        p = ''.join(p)
        prc = lambda s: "---" if s == '' else s
        price = prc(p)
        quantity = str(info[u'min_stock'][u'value'])
        Navigate.element_is_present(driver, Navigate.check_chat.WARE_PICTURE % (dialog, ware_id, picture))
        Navigate.element_is_present(driver, Navigate.check_chat.WARE_NAME % (dialog, ware_id, title))
        price_web = Navigate.element_is_present(driver, Navigate.check_chat.WARE_PRICE % (dialog, ware_id)).text
        price_web = price_web.encode('utf-8').replace(' ', '')
        self.assertEqual("Заштуку\n%sруб." % price, price_web, "Цена из БД '%s', цена из web '%s'" % (price, price_web))
        quantity_web = Navigate.element_is_present(driver, Navigate.check_chat.WARE_QUANTITY % (dialog, ware_id)).text
        quantity_web = quantity_web.encode('utf-8').replace(' ', '')
        self.assertEqual("Мин.заказ\n%sшт." % quantity, quantity_web, "Мин. заказ из БД '%s', и из web '%s'" %
                         (quantity, quantity_web))

    def check_user_message(self, driver, dialog, message, link_db):
        """
        Проверить сообщение-карточка пользователя
        :param messages:
        :return:
        """
        service_log.put("Checking User-message")
        user_id = str(message[u'userId'])
        user = link_db.accounting.get_user_by_criteria_only("id=%s" % user_id)[0]
        avatar_xpath = Navigate.check_chat.USER_AVATAR % (dialog, user_id, user["avatar_id"])
        service_log.put("Find avatar xpath=%s" % avatar_xpath)
        Navigate.element_is_present(driver, avatar_xpath)
        Navigate.element_is_present(driver, Navigate.check_chat.USER_NAME % (dialog, user_id, user["display_name"]))
        #Navigate.find_element_by_xpath_fast(driver, Navigate.check_chat.USER_STATUS % (dialog, user_id, user["avatar_id"]))

    def check_picture_message(self, driver, dialog, message):
        """
        Проверить сообщение-картинка
        :param messages:
        :return:
        """
        service_log.put("Checking Picture-message")
        picture_id = message[u'pictureId'].encode('utf-8')
        Navigate.element_is_present(driver, Navigate.check_chat.MSG_PICTURE % (dialog, picture_id))