# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Класс работы с Redis для воркера Session.
#
# P.S: — Какая-то нездоровая нынче активность в коде.
#      — Дык! Луна в скорпионе. (с)
#--------------------------------------------------------------------
from support import service_log
from support.utils.common_utils import run_on_prod
from support.utils.db_redis import ClassSaveLinkRedis, execute_nosql
from string import ascii_lowercase
from string import digits

__author__ = 's.trubachev'


class ClassSessionData(ClassSaveLinkRedis):

    # Название папок для SessionWorker
    FOLDER_SESSION = "session"
    FOLDER_CONTEXTS = "ctx"
    FOLDER_CONTEXT = "ctx"

    # Название полей для SessionWorker
    SESSION_ID = "sessionId"
    CREATION_TIME = "creationTime"
    TIME_STAMP = "lastAccessTimeStamp"
    CONTEXT_IDs = "contextIds"

    # постфиксы контекста
    CTX_META = "meta"
    CTX_DATA = "data"

    # Если количество перебранных ключей превышает эту цифру, считаем, что данные не найдены
    COUNT_ITERATION = 2000

    # Типы сравнения контекстов ('равно', 'больше или равно', 'меньше' -  заданного количества)
    TYPE_COMPARE = ["Equal", "GreaterEqual", "Less"]


class ClassSessionNoSql(ClassSessionData):

    @staticmethod
    def str_session(key):
        """ Добавляем к ключу название папки сессии.
        :param key: название ключа
        :return: session:< название ключа >
        """
        return ClassSessionNoSql.FOLDER_SESSION + ":" + str(key)

    @staticmethod
    def str_context(key):
        """ Добавляем к ключу название папки контекста.
        :param key: название ключа
        :return: session:< название ключа >
        """
        return ClassSessionNoSql.FOLDER_CONTEXT + ":" + str(key)

    @execute_nosql
    def get_context_id_by_session(self, session_id):
        """ Получить идентификаторы контекста по идентификатору сессии.
        :param session_id: hash-номер сессии
        :return: значение ключа context_id
        """
        return dict(type="hget", name=self.str_session(session_id), key=self.CONTEXT_IDs)

    @execute_nosql
    def get_create_time_by_session(self, session_id):
        """ Получить время создания сессии.
        :param session_id: hash-номер или имя
        :return: значение ключа
        """
        return dict(type="hget", name=self.str_session(session_id), key=self.CREATION_TIME)

    @execute_nosql
    def get_time_stamp_by_session(self, session_id):
        """ Получить время последнего визита сессии.
        :param session_id: hash-номер или имя
        :return: значение ключа
        """
        return dict(type="hget", name=self.str_session(session_id), key=self.TIME_STAMP)

    # --------------------------------------------------------------------------------------------
    @execute_nosql
    def get_data_by_session(self, session_id):
        """ Получить все данные в таблице сессии.
        :param session_id: hash-номер сессии
        :return: значение ключа context_id
        """
        return dict(type="hgetall", name=self.str_session(session_id))

    @execute_nosql
    def get_contexts_by_session(self, session_id, start=0, end=-1):
        """ Получить все контексты сессии.
        :param session_id: hash-номер сессии
        :param start: с какого элемента выборка
        :param end: по какой элемент выборка
        :return: список контекстов
        """
        name = self.form_key_redis(self.FOLDER_SESSION, self.FOLDER_CONTEXTS, session_id)
        return dict(type="lrange", name=name, start=start, end=end)

    def get_contexts_by_session_with_status(self, session_id, status = 'ACTIVE'):
        """ Получить только активные контексты сессии.
        :param session_id: идентификатор сессии.
        :return: список идентификаторов контекстов
        """
        list_contexts = self.get_contexts_by_session(session_id)
        return [index for index in list_contexts if self.get_context_meta(index)['contextStatus'] == status]

    @execute_nosql
    def get_context_meta(self, context_id):
        """ Получить мета-информацию контекста
        :param context_id: идентификатор контекста
        :return: словарь с данными
        """
        name = self.form_key_redis(self.FOLDER_CONTEXT, context_id, self.CTX_META)
        return dict(type="hgetall", name=name)

    @execute_nosql
    def get_context_data(self, context_id):
        """ Получить data-информацию контекста.
        :param context_id: идентификатор контекста
        :return: словарь с данными
        """
        name = self.form_key_redis(self.FOLDER_CONTEXT, context_id, self.CTX_DATA)
        return dict(type="hgetall", name=name)

    @execute_nosql
    def get_context_keys_by_pattern(self, pattern="0*"):
        """ Взять ключ контекста по паттерну
        :param pattern: паттерн
        :return: список ключей контекста с meta-информацией, подходящих под условие паттерна
        """
        name = self.form_key_redis(self.FOLDER_CONTEXT, pattern, self.CTX_META)
        return dict(type="keys", pattern=name)

    @staticmethod
    def check_count_contexts(count_contexts, len_contexts, flag, compare):
        """ Метод проверяющий наличие определённого количества контекстов у сессии.
        :param compare: тип сравнения количества контекстов
        :param count_contexts: количество контекстов в сессии, которое должно быть
        :param len_contexts: количество контекстов
        :param flag: флаг успешности сравнения
        :return: флаг flag_checked
        """
        # Методы сравнения ("равно", "меньше", "больше или равно")
        count_Equal = lambda param, count_keys, flag: flag if param is None else flag if param == count_keys else False
        count_Less = lambda param, count_keys, flag: flag if param is None else flag if param > count_keys else False
        count_GEqual = lambda param, count_keys, flag: flag if param is None else flag if param <= count_keys else False

        # проверяем условие по которому определяем необходимое количество контекстов, см.type_compare
        if compare.lower() == ClassSessionNoSql.TYPE_COMPARE[0].lower():
            flag = count_Equal(count_contexts, len_contexts, flag)
        elif compare.lower() == ClassSessionNoSql.TYPE_COMPARE[1].lower():
            flag = count_GEqual(count_contexts, len_contexts, flag)
        elif compare.lower() == ClassSessionNoSql.TYPE_COMPARE[2].lower():
            flag = count_Less(count_contexts, len_contexts, flag)
        return flag

    def get_session_with_param_context(self, context_type=None, context_status=None, count_contexts=1,
                                       count_compare="GreaterEqual", only_meta=None):
        """ Получить идентификатор сессии по информации в контексте.
        Одному из списка контекстов сессии точно соответствуют все заданные параметры.
        :param context_type: тип контекста
        :param context_status: статус контекста
        :param count_contexts: количество контекстов в сессии, которое должно быть
        :param count_compare: типы сравнения количества контекстов
        :return: идентификатор сессии удовлетворяющий условию
        """

        msg = "Warning: Not found test-data for this params for test!"
        symbols = list(ascii_lowercase) + list(digits)  # символы для формирования паттерна
        count_iteration = 0  # количество ключей, которые были проверенны

        # метод для проверки: если параметр не None и поле не равно соответств.параметру, возвращаем False
        check_field = lambda param, key_field, flag: flag if param is None else False if param != key_field else flag

        for symbol in symbols:
            keys_cont = self.get_context_keys_by_pattern(symbol + "*")
            count_iteration += len(keys_cont)
            for key_cont in keys_cont:
                flag_checked = True  # если состояние флага равно True, следует, что все условия соблюдены
                meta_cont = self.get_hashtable(key_cont)
                exist_data = self.check_exists(key_cont)
                service_log.put("Context-meta=%s." % meta_cont)
                len_contexts = len(self.get_contexts_by_session(meta_cont['sessionId']))
                service_log.put("Len contexts=%s." % len_contexts)
                # Проверяем что, контекст соответствует заданному статусу
                flag_checked = check_field(context_status, meta_cont['contextStatus'], flag_checked)
                service_log.put("Check contextStatus.")
                # Проверяем что, тип контекста принадлежит заданному типу
                flag_checked = check_field(context_type, meta_cont['contextType'], flag_checked)
                service_log.put("Check contextType.")
                # проверяем условие по которому определяем необходимое количество контекстов у сессии, см.type_compare
                flag_checked = self.check_count_contexts(count_contexts=count_contexts, len_contexts=len_contexts,
                                                         flag=flag_checked, compare=count_compare)
                service_log.put("Check count contexts.")
                # Проверяем, что у контекста отсутствует context-data
                flag_checked = check_field(only_meta, exist_data, flag_checked)
                service_log.put("Check context-data.")
                # если контекст подпадает под все заданные параметры, возвращаем идентификатор сессии
                if flag_checked is True:
                    service_log.put("Return session_id=%s." % meta_cont['sessionId'])
                    return meta_cont['sessionId']
            else:
                # Если заданно self.COUNT_ITERATION = -1, то это условие не проверяется
                # Если количество ключей было проверенно больше, чем заданно, считаем, что данные не найдены
                if self.COUNT_ITERATION != -1:
                    if count_iteration > self.COUNT_ITERATION:
                        service_log.put(msg)
                        return None
        else:
            service_log.put(msg)
            return None

    @run_on_prod(False)
    def create_session(self, session_id):
        """ Создание сессии.
        :param session_id: идентификатор сессии, если он равен None, создать новую сессию.
        :return: идентификатор сессии
        """
        if session_id is None:
            # создаём сессию
            # TODO: добавить методы на добавления тестовых данных
            service_log.put("Return session_id=%s." % session_id)
            return session_id
        else:
            service_log.put("Return session_id=%s." % session_id)
            return session_id


    @run_on_prod(False)
    @execute_nosql
    def create_context_data(self, session_id, context_data):
        """ Создание контекста с данными.
        :return:
        """
        pass

    def create_context_meta(self):
        # TODO
        pass



