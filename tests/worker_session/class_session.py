# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Файл с классами для работы с Accounting worker.
#--------------------------------------------------------------------

from copy import deepcopy
import platform
import random
import socket
import datetime
from gen_py.SessionWorker.ttypes import SessionContextRequestDto
from gen_py.SessionWorkerConstants.ttypes import ContextStatus
from support import service_log
from support.utils.common_utils import run_on_prod
from support.utils.db import databases
from tests.MainClass import MainClass

__author__ = 's.trubachev'


class SessionData(MainClass):
    """
    Статические данные свойственные только SessionWorker: переменные, константы, названия классов и т.д.
    """

    # Типы контекстов. Уточнять у разработчиков Node.js
    CONTEXT_TYPE = ['agent', 'auth']


class SessionMethods(SessionData):

    @staticmethod
    def generate_agent_data_context():
        """ Генерирование данных для контекста данных типа "agent".
        """
        data = dict(ip=socket.gethostbyname(socket.gethostname()),
                    agent=str({"name": "Python client for autotest", "os": platform.uname()[0]}),
                    headers=str({"host": "test-app.oorraa.pro"}),
                    stamp=datetime.datetime.now().isoformat())
        service_log.put("Generated data context, type=agent.")
        return data

    @staticmethod
    def generate_auth_data_context():
        """ Генерирование данных для контекста данных типа "auth".
        """
        data = {"Autotest": str(random.randint(1, 10000000000))}
        service_log.put("Generated data context, type=auth.")
        return data

    @staticmethod
    def generate_context_data(context_type):
        if context_type == "auth":
            return SessionMethods.generate_auth_data_context()
        elif context_type == "agent":
            return SessionMethods.generate_agent_data_context()
        else:
            msg = "Unknown context type %s!" % str(context_type)
            service_log.error(msg)
            raise AssertionError(msg)

    @staticmethod
    def generate_default_session(context_type="auth"):
        """ Сгенериовать данные для сессии.
        :return: словарь с данными.
        """
        params = dict(session_id=None,
                      context_type=context_type,
                      period_millis=500,
                      context_data=SessionMethods.generate_context_data(context_type),
                      refresh_on_get=True,
                      refresh_on_set=True)
        service_log.put("Generate default session: %s" % params)
        return params

    @staticmethod
    def get_SessionContextRequestDto(session_id, context_type, period_millis, context_data,
                                     refresh_on_get=True, refresh_on_set=True):
        """ Взять объект SessionContextRequestDto.
        Создаём запрос на создание пользовательского контекста.
        Warning: При создании новой сессии не указывается ID сессии.
        :param session_id: ID сессии, к которой прикрепляется контекст
        :param context_type: тип контекста
        :param period_millis: срок годности контекста, в мс.
        :param context_data: данные контекста, type(ContextData)
        :param refresh_on_get: флаг, нужно ли обновлять контекст при его получении
        :param refresh_on_set: флаг, нужно ли обновлять контекст при его изменении
        :return: объект SessionContextRequestDto
        """
        params = dict(sessionId=session_id,
                      contextType=context_type,
                      expirationPeriodMillis=period_millis,
                      contextData=context_data,
                      refreshOnGet=refresh_on_get,
                      refreshOnSet=refresh_on_set)
        params_without_none = dict((index, val) for index, val in params.iteritems() if params[index] is not None)
        session_cont = SessionContextRequestDto(**params_without_none)
        service_log.put("Created SessionContextRequestDto: %s" % str(session_cont))
        return session_cont

    @staticmethod
    def get_ContextData(key, value):
        """ Получить ContextData.
        :param key: ключ по которому хранятся данные
        :param value: значение по которому хранятся данные
        :return: словарь с данными контекста
        """
        cont_data = {key: value}
        service_log.put("Created SessionContextRequestDto: %s" % str(cont_data))
        return cont_data

    @staticmethod
    def get_context_status_by_number(number):
        """ Взять название стутуса по его номеру.
        :param number: номер статуса
        :return: наименование статуса
        """
        service_log.put("Number context status: %s" % ContextStatus._VALUES_TO_NAMES[number])
        return ContextStatus._VALUES_TO_NAMES[number]

    @staticmethod
    def get_context_status_by_name(name):
        """  Взять номер стутуса по его имени.
        :param name: наименование статуса
        :return: номер статуса
        """
        service_log.put("Name context status: %s" % ContextStatus._NAMES_TO_VALUES[name])
        return ContextStatus._NAMES_TO_VALUES[name]

    @staticmethod
    def get_context_status(data):
        """ Взять статус контекста.
        :param data: номер или наименование
        :return: наименование или номер
        """
        if type(data) is str:
            return SessionMethods.get_context_status_by_name(data)
        else:
            return SessionMethods.get_context_status_by_number(data)

    @staticmethod
    def fail_session_id(session_id):
        """ Проверяем идентификатор сессии.
        Метод для предусловия теста. (Методы SetUp и SetUpClass)
        Если идентификатор равен None, т.е. не был найден - вызываем исключение.
        :param session_id: идентификатор сессии
        :return: None
        """
        if session_id is None:
            msg = "Fail! Not found test-data for this params for test!"
            service_log.put(msg)
            raise AssertionError(msg)

    @run_on_prod(False)
    @staticmethod
    def data_preparation_session(status, count):
        """ Подготовка тестовых данных.
        Ищем сессию с нужным статусом одного из контекстов и общим наличием нужного количества контекстов.
        Если не найдено, то создаём свою сессию с заданными параметрами.
        Warning: Сначала ищет в Redis, это занимает определённое время. Плюс сессия не будет создаваться для прода.
        :param status: статус контекста
        :param count: количество контекстов в сессии
        :return: Идентификатор сессии
        """
        session_id = databases.nutcracker.shards.session.get_session_with_param_context(context_status=status,
                                                                                        count_contexts=count)
        session_id = databases.nutcracker.shards.session.create_session(session_id)
        return session_id

    @staticmethod
    def create_new_ctx(session_id):
        """ Создать новый контекст.
        :param session_id: идентификатор сессии
        :return: новый контекст
        """
        params = SessionMethods.generate_default_session()
        params.update({'session_id': session_id})
        params['context_data'].update({'Autotest': 'new_' + params['context_data']['Autotest']})
        return SessionMethods.get_SessionContextRequestDto(**params)

    @staticmethod
    def create_refresh_new_ctx(contexts_data):
        """ Создаём данные для обновления контекстов.
        :param contexts_data: данные существующих контекстов
        :return: словарь обновленных контекстов
        """
        new_contexts_data = deepcopy(contexts_data)
        for index in contexts_data.keys():
            new_contexts_data.update({'%s' % index: {"Autotest_refresh": str(random.randint(1, 10000000000))}})
        return new_contexts_data

    @run_on_prod(False)
    @staticmethod
    def set_active_session(user_id):
        session_id = None
        SessionMethods.fail_session_id(session_id)
        return session_id


class SessionCheckMethods(SessionMethods):

    def check_session(self, session_from_redis, session_from_serv):
        """ Проверяем данные сессии без контекстов.
        :param session_from_redis: данные от Redis
        :param session_from_serv: данные от сервиса
        """
        service_log.put("Check session:")
        self.assertEqual(long(session_from_redis['creationTime']), long(session_from_serv.creationTimestamp))
        self.assertEqual(long(session_from_redis['lastAccessTimeStamp']), long(session_from_serv.lastAccessTimestamp))
        self.assertEqual(session_from_redis['sessionId'], session_from_serv.sessionId)

    def check_session_changed_last_timestamp(self, session_from_redis, session_from_serv):
        """ Проверяем данные сессии без контекстов.
        Время последнего доступа изменено
        :param session_from_redis: данные от Redis
        :param session_from_serv: данные от сервиса
        """
        service_log.put("Check session:")
        self.assertEqual(long(session_from_redis['creationTime']), long(session_from_serv.creationTimestamp))
        self.assertGreater(long(session_from_redis['lastAccessTimeStamp']), long(session_from_serv.lastAccessTimestamp))
        self.assertEqual(session_from_redis['sessionId'], session_from_serv.sessionId)

    def check_context(self, session_id, context, meta_context, data_context):
        """ Проверяем контекст.
        :param session_id: идентификатор сессии
        :param context: данные контекста
        :param meta_context: meta-информация контекста
        :param data_context: data-информация контекста
        """
        service_log.put("Check context:")
        self.assertEqual(meta_context['contextId'], context.contextId)
        self.assertEqual(meta_context['contextType'], context.contextType)
        self.assertEqual(long(meta_context['creationTimeStamp']), long(context.creationTimestamp))
        self.assertEqual(long(meta_context['expirationTime']), long(context.expirationTime))
        self.assertEqual(long(meta_context['expirationTimeStamp']), long(context.expirationTimestamp))
        self.assertEqual(long(meta_context['lastAccessTimeStamp']), long(context.lastAccessTimestamp))
        self.assertEqual(long(meta_context['contextRevision']), long(context.revision))
        self.assertEqual(session_id, context.sessionId)
        self.assertEqual(meta_context['contextStatus'], self.get_context_status(context.status))
        self.assertDictEqual(data_context, context.contextData)

    def check_SessionContextDto(self, session_id, result_ctx, req_ctx, status=0, revision=0):
        """ Сравнить SessionContextDto заданное и полученное значения.
        :param session_id: идентификатор сессии
        :param result_ctx: результат в формате SessionContextDto
        :param req_ctx: запрос в SessionContextDto
        :param status: т.к. статус задаётся только при ответе, указываем принудительно
        :param revision: т.к. ревизия задаётся только при ответе, указываем принудительно
        """
        self.assertDictEqual(result_ctx.contextData, req_ctx.contextData)
        self.assertEqual(result_ctx.sessionId, session_id)
        self.assertEqual(result_ctx.contextType, req_ctx.contextType)
        self.assertEqual(result_ctx.expirationTime, req_ctx.expirationPeriodMillis)
        self.assertEqual(result_ctx.status, status)
        self.assertEqual(result_ctx.revision, revision)

    def check_context_meta_data(self, meta_context1, meta_context2):
        """ Сравниваем метаданные данные двух контекстов. Обновленного и старого.
        :param meta_context1: обновленные данные
        :param meta_context2: старые данные
        """
        self.assertEqual(meta_context1['contextId'], meta_context2['contextId'])
        self.assertEqual(meta_context1['contextRevision'], meta_context2['contextRevision'])
        self.assertEqual(meta_context1['contextStatus'], meta_context2['contextStatus'])
        self.assertEqual(meta_context1['contextType'], meta_context2['contextType'])
        self.assertEqual(meta_context1['creationTimeStamp'], meta_context2['creationTimeStamp'])
        self.assertEqual(meta_context1['expirationTime'], meta_context2['expirationTime'])
        self.assertEqual(meta_context1['refreshOnGet'], meta_context2['refreshOnGet'])
        self.assertEqual(meta_context1['refreshOnSet'], meta_context2['refreshOnSet'])
        self.assertEqual(meta_context1['sessionId'], meta_context2['sessionId'])
        self.assertLess(meta_context2['expirationTimeStamp'], meta_context1['expirationTimeStamp'])
        self.assertLess(meta_context2['lastAccessTimeStamp'], meta_context1['lastAccessTimeStamp'])

    def check_context_meta_data_without_status(self, meta_context1, meta_context2):
        """ Сравниваем метаданные данные двух контекстов. Обновленного и старого, кроме статуса.
        :param meta_context1: обновленные данные
        :param meta_context2: старые данные
        """
        self.assertEqual(meta_context1['contextId'], meta_context2['contextId'])
        self.assertEqual(meta_context1['contextRevision'], meta_context2['contextRevision'])
        self.assertEqual(meta_context1['contextType'], meta_context2['contextType'])
        self.assertEqual(meta_context1['creationTimeStamp'], meta_context2['creationTimeStamp'])
        self.assertEqual(meta_context1['expirationTime'], meta_context2['expirationTime'])
        self.assertEqual(meta_context1['refreshOnGet'], meta_context2['refreshOnGet'])
        self.assertEqual(meta_context1['refreshOnSet'], meta_context2['refreshOnSet'])
        self.assertEqual(meta_context1['sessionId'], meta_context2['sessionId'])
        self.assertLess(meta_context2['expirationTimeStamp'], meta_context1['expirationTimeStamp'])
        self.assertLess(meta_context2['lastAccessTimeStamp'], meta_context1['lastAccessTimeStamp'])

    def check_context_meta_data_without_status_and_not_changed_expiration(self, meta_context1, meta_context2):
        """ Сравниваем метаданные данные двух контекстов. Обновленного и старого, кроме статуса.
        :param meta_context1: обновленные данные
        :param meta_context2: старые данные
        """
        self.assertEqual(meta_context1['contextId'], meta_context2['contextId'])
        self.assertEqual(meta_context1['contextRevision'], meta_context2['contextRevision'])
        self.assertEqual(meta_context1['contextType'], meta_context2['contextType'])
        self.assertEqual(meta_context1['creationTimeStamp'], meta_context2['creationTimeStamp'])
        self.assertEqual(meta_context1['expirationTime'], meta_context2['expirationTime'])
        self.assertEqual(meta_context1['refreshOnGet'], meta_context2['refreshOnGet'])
        self.assertEqual(meta_context1['refreshOnSet'], meta_context2['refreshOnSet'])
        self.assertEqual(meta_context1['sessionId'], meta_context2['sessionId'])
        self.assertEqual(meta_context2['expirationTimeStamp'], meta_context1['expirationTimeStamp'])
        self.assertEqual(meta_context2['lastAccessTimeStamp'], meta_context1['lastAccessTimeStamp'])









