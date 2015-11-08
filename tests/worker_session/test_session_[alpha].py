# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Tests.
#--------------------------------------------------------------------

from ddt import ddt, data
from support import service_log
from support.utils.common_utils import run_on_prod
from support.utils.db import databases
from support.utils.thrift4req import services
from tests.worker_session.class_session import SessionCheckMethods


__author__ = 's.trubachev'



@ddt
class TestSessionInit(SessionCheckMethods):

    @run_on_prod(False)
    def test_initSession_simple(self):
        """ Тест на инициализацию сессии.
        Генерируем запрос и отправляем в воркер.
        Сравниваем с данными из redis.
        """
        params_req = self.get_SessionContextRequestDto(**self.generate_default_session())
        result = services.session.root.tframed.initSession(params_req)
        this_session = databases.db0.session.get_data_by_session(result.sessionId)
        service_log.put("Get session data: %s" % this_session)
        list_context_ids = databases.db0.session.get_contexts_by_session(result.sessionId)
        service_log.put("Get list context id's for session: %s" % list_context_ids)
        self.check_session(this_session, result)
        msg_count = "The number of visits from the service is not equal to data from redis."
        msg_one = "Too many contexts"
        self.assertEqual(len(result.contexts), len(list_context_ids), msg_count)
        self.assertEqual(len(result.contexts), 1, msg_one)
        for context in result.contexts:
            meta_context = databases.db0.session.get_context_meta(context.contextId)
            service_log.put("Get meta_context: %s" % meta_context)
            data_context = databases.db0.session.get_context_data(context.contextId)
            service_log.put("Get data_context: %s" % data_context)
            self.check_context(result.sessionId, context, meta_context, data_context)

    def test_initSession_without_context(self):
        pass

    def test_initSession_several_context(self):
        pass

    def test_replaceContextData(self):
        pass

    def test_replaceContextsData(self):
        pass

    def test_invalidateSession(self):
        pass


class TestSessionGetSessionById(SessionCheckMethods):

    @classmethod
    def setUpClass(cls):
        """ Делаем выборку тестовых данных.
        Сессию с двумя контекстами, один из которых точно в статусе REVOKE.
        Что означает, что для теста с only_active=False, точно проверим,
        что он вернёт все контексты, в не зависимости от статуса.
        А в случае с only_active=True, воркер вернёт либо 0 контекстов (случай когда они все не активны),
        либо вернёт количество count-1, т.к. один из контекстов точно в статусе REVOKE.
        """

        context_status = cls.get_context_status(2)  # один из контекстов в статусе REVOKE
        count_contexts = 2  # количество контекстов в сессии не меньше 2-ух
        cls.msg_count = "The number of visits from the service is not equal to data from redis."
        cls.session_id = cls.data_preparation_session(status=context_status, count=count_contexts)
        cls.fail_session_id(cls.session_id)

    def test_getSessionById(self):
        """ Проверяем метод getSessionById.
        Делаем выборку информации от redis по идентифиактору сессии.
        Находим все контексты сессии в redis по идентификатору сессии.
        Делаем запрос воркеру сессий на выборку нужной сессии по идентификатору.
        Проверяем полученные данные от ворекра и от redis.
        Если onlyActive == false, возвращаются все контексты.
        """
        this_session = databases.db0.session.get_data_by_session(self.session_id)
        service_log.put("Get session data: %s" % this_session)
        list_context_ids = databases.db0.session.get_contexts_by_session(self.session_id)
        service_log.put("Get list context id's for session: %s" % list_context_ids)
        result = services.session.root.tframed.getSessionById(self.session_id, onlyActive=False)
        service_log.put("Method getSessionById returned result: %s" % result)
        self.check_session(this_session, result)
        self.assertEqual(len(result.contexts), len(list_context_ids), self.msg_count)
        for context in result.contexts:
            meta_context = databases.db0.session.get_context_meta(context.contextId)
            service_log.put("Get meta_context: %s" % meta_context)
            data_context = databases.db0.session.get_context_data(context.contextId)
            service_log.put("Get data_context: %s" % data_context)
            self.check_context(self.session_id, context, meta_context, data_context)

    def test_getSessionById_only_active(self):
        """ Проверяем метод getSessionById с активными сессиями.
        Делаем выборку информации от redis по идентифиактору сессии.
        Находим все контексты сессии в redis по идентификатору сессии.
        Делаем запрос воркеру сессий на выборку нужной сессии по идентификатору.
        Проверяем полученные данные от ворекра и от redis.
        Если onlyActive == true, контекст будет возвращен только если он активен.
        """
        status = self.get_context_status(0)
        this_session = databases.db0.session.get_data_by_session(self.session_id)
        service_log.put("Get session data: %s" % this_session)
        list_context_ids = databases.db0.session.get_contexts_by_session_with_status(self.session_id, status)
        service_log.put("Get list context id's for session: %s" % list_context_ids)
        result = services.session.root.tframed.getSessionById(self.session_id, onlyActive=True)
        service_log.put("Method getSessionById returned result: %s" % result)
        self.check_session(this_session, result)
        self.assertEqual(len(result.contexts), len(list_context_ids), self.msg_count)
        for context in result.contexts:
            meta_context = databases.db0.session.get_context_meta(context.contextId)
            service_log.put("Get meta_context: %s" % meta_context)
            data_context = databases.db0.session.get_context_data(context.contextId)
            service_log.put("Get data_context: %s" % data_context)
            self.check_context(self.session_id, context, meta_context, data_context)


class TestSessionGetContextForSession(SessionCheckMethods):

    @classmethod
    def setUpClass(cls):
        context_status = cls.get_context_status(2)  # один из контекстов в статусе REVOKE
        cls.context_type = cls.CONTEXT_TYPE[0]  # тип контекста 'auth'
        count_contexts = 3  # количество контекстов в сессии не меньше 2-ух
        # TODO: Необходима другая логика для получения тестовых данных
        cls.session_id = cls.data_preparation_session(status=context_status, count=count_contexts)
        cls.fail_session_id(cls.session_id)

    def test_getContextForSession(self):
        """ Взять контексты сессии, выборка по типу и статусу контекста.
        :param only_active: Если only_active == true, контекст будет возвращен только если он активен.
        """
        # TODO: https://youtrack.home.oorraa.net/issue/M-143
        result = services.session.root.tframed.getContextForSession(self.session_id, self.context_type, False)
        service_log.put("Method getContextForSession returned result: %s" % result)




