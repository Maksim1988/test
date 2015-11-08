# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Класс работы с Redis для воркера Session.
#--------------------------------------------------------------------
from support.utils.db_redis import ClassSaveLinkRedis, execute_nosql

__author__ = 's.trubachev'


class ClassMessagesData(ClassSaveLinkRedis):

    # Название папок для MessagingWorker
    FOLDER_NULL = ""
    FOLDER_DEALS = "deals"
    FOLDER_DIALOGS = "dialogs"
    FOLDER_MESSAGES = "messages"
    FOLDER_USER_OPPONENTS = "user_opponents"

    # Название постфиксов ключей для FOLDER_DEALS
    FD_OPPONENTS = "opponent_ids"

    # Название постфиксов ключей для FOLDER_DIALOGS
    FDS_ALL_MESSAGES = "all_messages"
    FDS_DIALOG = "dialog"

    # Название постфиксов ключей для FOLDER_MESSAGES
    FM_MESSAGE = "message"


class ClassMessagingNoSql(ClassMessagesData):

    # Методы для работы с FOLDER_DEALS -> FOLDER_USER_OPPONENTS
    @execute_nosql
    def get_user_opponents(self, user_id, start=0, end=0, desc=False, withscores=False, score_cast_func=float):
        """ Получить список оппонентов с идентификаторами диалогов.
        :param user_id: идентификатор пользователя
        :param start: начало писка
        :param end: конец списка
        :param desc: направление сортировки
        :param withscores: указывает, вернуть ли идентификаторы со значениями
        :param score_cast_func: функция обрабатывающая результат
        :return: массив с данными
        """
        name = self.form_key_redis(self.FOLDER_DEALS, self.FOLDER_USER_OPPONENTS, user_id, self.FD_OPPONENTS)
        return {"type": "zrange", "name": name, "start": start, "end": end, "desc": desc,
                "withscores": withscores, "score_cast_func": score_cast_func}

    # Методы для работы с FOLDER_DIALOGS
    @execute_nosql
    def get_dialog(self, owner_id, opponent_id):
        """ Получить данные диалога.
        :param owner_id: владелец диалога
        :param opponent_id: оппонент владельца диалога
        :return: данные по диалогу
        """
        name = self.form_key_redis(self.FOLDER_DIALOGS, "%s_%s" % (owner_id, opponent_id), self.FDS_DIALOG)
        return {"type": "get", "name": name}

    # Методы для работы с FOLDER_DIALOGS
    @execute_nosql
    def get_dialog_by_id(self, dialog_id):
        """ Получить данные диалога.
        :param owner_id: владелец диалога
        :param opponent_id: оппонент владельца диалога
        :return: данные по диалогу
        """
        name = self.form_key_redis(self.FOLDER_DIALOGS, dialog_id, self.FDS_DIALOG)
        return {"type": "get", "name": name}

    @execute_nosql
    def get_all_message(self, owner_id, opponent_id, start=0, end=-1):
        """ Получить список сообщений диалога.
        :param owner_id: владелец диалога
        :param opponent_id: оппонент владельца диалога
        :param start: начало писка
        :param end: конец списка
        :return: список идентификаторов сообщений
        """
        name = self.form_key_redis(self.FOLDER_DIALOGS, "%s_%s" % (owner_id, opponent_id), self.FDS_ALL_MESSAGES)
        return dict(type="lrange", name=name, start=start, end=end)

    @execute_nosql
    def get_all_message_by_id(self, dialog_id, start=0, end=-1):
        """ Получить список сообщений диалога.
        :param owner_id: владелец диалога
        :param opponent_id: оппонент владельца диалога
        :param start: начало писка
        :param end: конец списка
        :return: список идентификаторов сообщений
        """
        name = self.form_key_redis(self.FOLDER_DIALOGS, dialog_id, self.FDS_ALL_MESSAGES)
        return dict(type="lrange", name=name, start=start, end=end)

    # Методы для работы с FOLDER_MESSAGES
    @execute_nosql
    def get_message(self, message_id):
        """ Получить данные сообщений.
        :param message_id: идентификатор сообщений
        :return: данные сообщения, type(json)
        """
        name = self.form_key_redis(self.FOLDER_MESSAGES, message_id, self.FM_MESSAGE)
        return dict(type="get", name=name)
