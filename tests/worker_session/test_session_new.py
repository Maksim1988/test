# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Тесты для SessionWorker.
#--------------------------------------------------------------------
import random
from unittest import expectedFailure
from ddt import ddt, data, unpack
import time
from support import service_log
from support.utils.db import databases
from support.utils.thrift4req import services
from tests.worker_session.class_session import SessionCheckMethods

__author__ = 's.trubachev'


class AuxiliarySession(SessionCheckMethods):

    def get_contexts_from_redis(self, context_id):
        """ Получить данные контекста из Redis по его идентификатору.
        :param context_id: идентификатор контекста
        :return: мета контекста, контекст данных
        """
        meta_context = databases.nutcracker.shards.session.get_context_meta(context_id)
        service_log.put("Get meta_context after invalidate: %s" % meta_context)
        data_context = databases.nutcracker.shards.session.get_context_data(context_id)
        service_log.put("Get data_context after invalidate: %s" % data_context)
        return meta_context, data_context

    def get_information_about_session(self, session_id):
        """ Получить информацию по сессии.
        :param session_id: идентификатор сессии
        :return: данные сессии, список идентификаторов контекстов
        """
        this_session = databases.nutcracker.shards.session.get_data_by_session(session_id)
        service_log.put("Get data session: %s" % str(this_session))
        list_context_ids = databases.nutcracker.shards.session.get_contexts_by_session(session_id)
        service_log.put("Get list context id's for session: %s" % list_context_ids)
        return this_session, list_context_ids


class TestSessionInit(AuxiliarySession):

    @classmethod
    def setUp(cls):
        service_log.preparing_env(cls)

    def test_initSession_simple(self):
        """ Тест на инициализацию сессии.
        Генерируем запрос и отправляем в воркер.
        Сравниваем с данными из redis.
        """
        service_log.run(self)
        params_req = self.get_SessionContextRequestDto(**self.generate_default_session())
        result = services.session.root.tframed.initSession(params_req)
        this_session, list_context_ids = self.get_information_about_session(result.sessionId)
        self.check_session(this_session, result)
        msg_count = "The number of visits from the service is not equal to data from redis."
        msg_one = "Too many contexts"
        self.assertEqual(len(result.contexts), len(list_context_ids), msg_count)
        self.assertEqual(len(result.contexts), 1, msg_one)
        for context in result.contexts:
            meta_context, data_context = self.get_contexts_from_redis(context.contextId)
            self.check_context(result.sessionId, context, meta_context, data_context)

    @classmethod
    def tearDown(cls):
        service_log.end()


@ddt
class TestCtxInit(AuxiliarySession):

    @classmethod
    def setUp(cls):
        service_log.preparing_env(cls)

    @expectedFailure  # TODO: https://jira.oorraa.net/browse/RT-734
    def test_initContext(self):
        """ Тест на инициализацию нового контекста для сессии.
        Создаем новый контекст, запоминаем данные по нему. Добавляем новый контекст того же типа.
        Проверяем, что данные по контекстам обновились.
        """
        service_log.run(self)
        # создаем новую сессию и получаем список контекстов
        params_req = self.get_SessionContextRequestDto(**self.generate_default_session())
        result = services.session.root.tframed.initSession(params_req)
        list_context_ids_before = databases.nutcracker.shards.session.get_contexts_by_session(result.sessionId)
        service_log.put("Get list context id's for session before new context: %s" % list_context_ids_before)

        # создаем новый контекст и получаем список контекстов
        params = self.generate_default_session()
        params.update({"session_id": result.sessionId})
        params['context_data'].update({"Autotest": 'new_' + params['context_data']['Autotest']})
        req_new_ctx = self.get_SessionContextRequestDto(**params)
        result_ctx = services.session.root.tframed.initContext(req_new_ctx)
        list_context_ids_after = databases.nutcracker.shards.session.get_contexts_by_session(result.sessionId)

        # Получаем данные первого и второго контекстов
        first_meta_context, first_data_context = self.get_contexts_from_redis(list_context_ids_after[0])
        second_meta_context, second_data_context = self.get_contexts_from_redis(list_context_ids_after[1])

        # проверяем, что количество контекстов не изменилось
        msg_error1 = "The number of 'contexts' is not consistent with the stated"
        msg_error2 = "The number of contexts before and after the upgrade the same"
        msg_error3 = "Type contests not equal"
        self.assertEqual(len(list_context_ids_after), 2, msg_error1)
        self.assertNotEqual(len(list_context_ids_after), len(list_context_ids_before), msg_error2)

        # проверяем, что только один из контектов активен и типы контекстов равны
        self.assertEqual(second_meta_context['contextStatus'], "ACTIVE", "New context not Active")
        self.assertNotEqual(first_meta_context['contextStatus'], "ACTIVE", "Old context is Active")
        self.assertEqual(first_meta_context['contextType'], second_meta_context['contextType'], msg_error3)

        # проверяем, что новый контекст присутствует в списке после его инцициализации и его нет до неё
        self.assertTrue(result_ctx.contextId in list_context_ids_after, "Not found context!")
        self.assertFalse(result_ctx.contextId in list_context_ids_before, "Found context!")

        # сраниваем новый контекст от метода с теми параметрами, которые мы задали
        self.check_SessionContextDto(result.sessionId, result_ctx, req_new_ctx)
        self.check_context(result.sessionId, result.contexts[0], first_meta_context, first_data_context)
        self.check_context(result.sessionId, result_ctx, second_meta_context, second_data_context)

    def test_replaceContextData_refresh(self):
        """ Проверка метод replaceContextData на обновление данных.
        Заменяет всю contextData данного контекста на новую. Возвращает новое состояние контекста.
        Все старые значения затираются. Эквивалентно oldData = newData;
        Если значение не изменилось, контекст не рефрешится.
        """
        service_log.run(self)
        # создаем новую сессию
        params_req = self.get_SessionContextRequestDto(**self.generate_default_session())
        session = services.session.root.tframed.initSession(params_req)
        before_meta_context = databases.nutcracker.shards.session.get_context_meta(session.contexts[0].contextId)

        # рефрешем контекст и получаем данные о контекстах после этого
        params_ctx = {"Autotest_refresh": str(random.randint(1, 10000000000))}
        result = services.session.root.tframed.replaceContextData(session.contexts[0].contextId, params_ctx)
        list_context_ids_after = databases.nutcracker.shards.session.get_contexts_by_session(session.sessionId)
        after_meta_context, after_data_context = self.get_contexts_from_redis(list_context_ids_after[0])

        self.assertIsNone(result)
        self.assertEqual(len(list_context_ids_after), 1, "The number of contexts has changed")
        self.assertDictEqual(after_data_context, params_ctx)
        self.check_context_meta_data(after_meta_context, before_meta_context)

    def test_replaceContextData_not_refresh(self):
        """ Проверка метод replaceContextData на игнорировапние обновления.
        Заменяет всю contextData данного контекста на новую. Возвращает новое состояние контекста.
        Все старые значения затираются. Эквивалентно oldData = newData;
        Если значение не изменилось, контекст не рефрешится.
        """
        service_log.run(self)
        # создаем новую сессию
        params_req = self.get_SessionContextRequestDto(**self.generate_default_session())
        session = services.session.root.tframed.initSession(params_req)
        before_meta_context = databases.nutcracker.shards.session.get_context_meta(session.contexts[0].contextId)

        # рефрешем контекст с теми же данными и получаем данные о контекстах после этого
        params_ctx = params_req.contextData
        result = services.session.root.tframed.replaceContextData(session.contexts[0].contextId, params_ctx)
        list_context_ids_after = databases.nutcracker.shards.session.get_contexts_by_session(session.sessionId)
        after_meta_context, after_data_context = self.get_contexts_from_redis(list_context_ids_after[0])

        self.assertIsNone(result)
        self.assertEqual(len(list_context_ids_after), 1, "The number of contexts has changed")
        self.assertDictEqual(after_data_context, params_ctx)
        self.check_context_meta_data(after_meta_context, before_meta_context)

    @data(1, 2, 5, 50)
    def test_replaceContextsData_for_one_session(self, count=5):
        """ Проверка замены всех contextData указанных контекстов на новые для одной сессии.
        Создаем сессию. С помощью метода initContext добавлем новые контексты.
        Изменяем через replaceContextsData контексты данных и выполняем проверку.
        :param count: количество создаваемых контекстов
        """
        service_log.run(self)
        # создаем новую сессию
        params_req = self.get_SessionContextRequestDto(**self.generate_default_session())
        session = services.session.root.tframed.initSession(params_req)

        # создаем новые контексты для сессии
        contexts_data = {session.contexts[0].contextId: session.contexts[0].contextData}
        meta = databases.nutcracker.shards.session.get_context_meta(session.contexts[0].contextId)
        contexts_meta = {session.contexts[0].contextId: meta}
        for index in range(count):
            req_new_ctx = self.create_new_ctx(session.sessionId)
            res = services.session.root.tframed.initContext(req_new_ctx)
            meta_context, data_context = self.get_contexts_from_redis(res.contextId)
            contexts_data.update({'%s' % res.contextId: data_context})
            contexts_meta.update({'%s' % res.contextId: meta_context})
        count_ctxs = databases.nutcracker.shards.session.get_contexts_by_session(session.sessionId)

        # Создаём данные для обновления контекстов
        new_contexts_data = self.create_refresh_new_ctx(contexts_data)

        # обновляем информацию контекста данных и получаем контексты сессии
        result = services.session.root.tframed.replaceContextsData(new_contexts_data)
        after_count_ctxs = databases.nutcracker.shards.session.get_contexts_by_session(session.sessionId)

        self.assertIsNone(result)
        for index in contexts_data.keys():
            meta_context, data_context = self.get_contexts_from_redis(index)
            self.check_context_meta_data(meta_context, contexts_meta[index])
            self.assertDictEqual(data_context, new_contexts_data[index])
        self.assertEqual(len(count_ctxs), len(after_count_ctxs), "The number of contexts has changed")

    def test_replaceContextsData_for_different_sessions(self, count=3):
        """ Проверка замены всех contextData указанных контекстов на новые для разных сессии.
        Создаем несколько сессий с различным количеством контекстов.
        Изменяем через replaceContextsData контексты данных и выполняем проверку.
        :param count: количество создаваемых сессий
        """
        service_log.run(self)

        # создаем новые сессии
        params_reqs = map(lambda n: self.get_SessionContextRequestDto(**self.generate_default_session()), range(count))
        sessions = map(services.session.root.tframed.initSession, params_reqs)

        # Запоминаем существующие контексты сессий
        contexts_data = dict()
        contexts_meta = dict()
        for session in sessions:
            contexts_data.update({session.contexts[0].contextId: session.contexts[0].contextData})
            meta = databases.nutcracker.shards.session.get_context_meta(session.contexts[0].contextId)
            contexts_meta.update({session.contexts[0].contextId: meta})

        # Добавляем контексты к сессиям (для первой +1 контекст, для второй +2 и т.д.)
        new_contexts = list()
        for num, session in enumerate(sessions, start=1):
            for add_contexts in range(num):
                new_contexts.append(self.create_new_ctx(session.sessionId))
        res = map(services.session.root.tframed.initContext, new_contexts)

        # запоминаем все значения контекстов и количество контекстов до замены контекстов данных
        for index in res:
            meta_context, data_context = self.get_contexts_from_redis(index.contextId)
            contexts_data.update({'%s' % index.contextId: data_context})
            contexts_meta.update({'%s' % index.contextId: meta_context})
        count_ctxs = list()
        for session in sessions:
            count_ctxs.append(databases.nutcracker.shards.session.get_contexts_by_session(session.sessionId))

        # обновляем информацию контекста данных и запоминаем новое количество контекстов сессий
        new_contexts_data = self.create_refresh_new_ctx(contexts_data)
        result = services.session.root.tframed.replaceContextsData(new_contexts_data)
        after_count_ctxs = list()
        for session in sessions:
            after_count_ctxs.append(databases.nutcracker.shards.session.get_contexts_by_session(session.sessionId))

        self.assertIsNone(result)
        for index in contexts_data.keys():
            meta_context, data_context = self.get_contexts_from_redis(index)
            self.check_context_meta_data(meta_context, contexts_meta[index])
            self.assertDictEqual(data_context, new_contexts_data[index])
        msg1 = "The number of contexts has changed from session"
        msg2 = "One of the contexts the number has changed from session"
        self.assertEqual(len(count_ctxs), len(after_count_ctxs), msg1)
        self.assertTrue(all(len(count_ctxs[num]) == len(after_count_ctxs[num]) for num in range(len(count_ctxs))), msg2)

    @classmethod
    def tearDown(cls):
        service_log.end()


class TestInvalidate(AuxiliarySession):

    @classmethod
    def setUp(cls):
        service_log.preparing_env(cls)

    def test_invalidateContext(self):
        """ Проверка инвалидации контекста.
        Возвращает сессию по ID. Сессия включает все свои контексты.
        Если onlyActive == true, возвращаются только активные контексты.
        """
        service_log.run(self)
        # Создаем новую сессию
        params_req = self.get_SessionContextRequestDto(**self.generate_default_session())
        session = services.session.root.tframed.initSession(params_req)
        service_log.put("Get session data: %s" % session)

        # собираем информацию о сессии и контекстах до инвалидации
        before_meta_context, before_data_context = self.get_contexts_from_redis(session.contexts[0].contextId)

        result = services.session.root.tframed.invalidateContext(session.contexts[0].contextId)
        service_log.put("Get session data after invalidate context: %s" % session)

        # собираем информацию о сессии и контекстах после инвалидации
        this_session, list_context_ids = self.get_information_about_session(session.sessionId)
        after_meta_context, after_data_context = self.get_contexts_from_redis(session.contexts[0].contextId)

        # проверка, что данные кроме статуса не изменились (и кроме некоторых таймеров)
        self.assertIsNone(result)
        self.check_session(this_session, session)
        self.check_context_meta_data_without_status_and_not_changed_expiration(after_meta_context, before_meta_context)
        self.assertEqual(len(session.contexts), len(list_context_ids), "Not equal to data from redis.")
        self.assertEqual(len(list_context_ids), 1, "Too many contexts")
        self.assertDictEqual(after_data_context, before_data_context)
        self.assertEqual(self.get_context_status(after_meta_context['contextStatus']), 2, "Status context not REVOKED.")

    def test_invalidateSession(self):
        """ Проверка инвалидации всех активных контекстов сессии.
        """
        service_log.run(self)
        # Создаем новую сессию, дополнительные котексты для неё
        params_req = self.get_SessionContextRequestDto(**self.generate_default_session())
        session = services.session.root.tframed.initSession(params_req)
        service_log.put("Get session data: %s" % session)

        # собираем информацию о контекстах до инвалидации и инвалидируем контектсы сессии
        before_meta_context, before_data_context = self.get_contexts_from_redis(session.contexts[0].contextId)
        result = services.session.root.tframed.invalidateSession(session.sessionId)
        service_log.put("Get session data after invalidate context: %s" % session)

        # собираем информацию о сессии и контекстах после инвалидации
        this_session, list_context_ids = self.get_information_about_session(session.sessionId)
        after_meta_context, after_data_context = self.get_contexts_from_redis(session.contexts[0].contextId)

        # проверка, что данные кроме статуса не изменились (и кроме некоторых таймеров)
        self.assertIsNone(result)
        self.check_session(this_session, session)
        self.check_context_meta_data_without_status_and_not_changed_expiration(after_meta_context, before_meta_context)
        self.assertEqual(len(session.contexts), len(list_context_ids), "Not equal to data from redis.")
        self.assertEqual(len(list_context_ids), 1, "Too many contexts")
        self.assertDictEqual(after_data_context, before_data_context)
        self.assertEqual(self.get_context_status(after_meta_context['contextStatus']), 2, "Status context not REVOKED.")

    def test_invalidateSession_with_several_context(self):
        # TODO: инвалидировать сессию с разными состояниями контекстов
        service_log.run(self)
        pass

    @classmethod
    def tearDown(cls):
        service_log.end()


@ddt
class TestSessionGetContext(AuxiliarySession):

    @classmethod
    def setUp(cls):
        service_log.preparing_env(cls)

    @data(True, False)
    def test_getContextById_one_active_ctx(self, only_active=False):
        """ Проверка возвращения контекста для одной сессии с одним активным контекстом, onlyActive = False и True.
        Если onlyActive == true, контекст будет возвращен только если он активен.
        Если контекст активен и refresh == true, его lastAccessTimestamp и expirationTimestamp будут обновлены.
        """
        service_log.run(self)
        # Создаем новую сессию, дополнительные котексты для неё
        params_req = self.get_SessionContextRequestDto(**self.generate_default_session())
        session = services.session.root.tframed.initSession(params_req)
        service_log.put("Get session data: %s" % session)

        # собираем информацию о контекстах до инвалидации и получаем контекс сессии по его идентификатору
        before_meta_context, before_data_context = self.get_contexts_from_redis(session.contexts[0].contextId)
        result = services.session.root.tframed.getContextById(session.contexts[0].contextId, only_active)

        # собираем информацию о контекстах после инвалидации
        this_session, list_context_ids = self.get_information_about_session(session.sessionId)
        after_meta_context, after_data_context = self.get_contexts_from_redis(session.contexts[0].contextId)

        self.check_session_changed_last_timestamp(this_session, session)
        self.assertEqual(len(session.contexts), len(list_context_ids), "Not equal to data from redis.")
        self.assertEqual(len(list_context_ids), 1, "Too many contexts")
        self.assertDictEqual(after_data_context, before_data_context)
        self.check_context_meta_data(after_meta_context, before_meta_context)
        self.check_context(session.sessionId, result, meta_context=after_meta_context, data_context=after_data_context)

    def test_getContextById_one_inactive_ctx_onlyActive_false(self):
        """ Проверка возвращения контекста для одной сессии с одним не активным контекстом, onlyActive = False.
        Если onlyActive == true, контекст будет возвращен только если он активен.
        Если контекст активен и refresh == true, его lastAccessTimestamp и expirationTimestamp будут обновлены.
        """
        only_active = False
        service_log.run(self)
        # Создаем новую сессию, дополнительные котексты для неё
        params_req = self.get_SessionContextRequestDto(**self.generate_default_session())
        session = services.session.root.tframed.initSession(params_req)
        service_log.put("Get session data: %s" % session)
        # инвалидируем контекст
        result = services.session.root.tframed.invalidateContext(session.contexts[0].contextId)
        service_log.put("Get session data after invalidate context: %s" % session)

        # собираем информацию о контекстах до инвалидации и получаем контекс сессии по его идентификатору
        before_meta_context, before_data_context = self.get_contexts_from_redis(session.contexts[0].contextId)
        result = services.session.root.tframed.getContextById(session.contexts[0].contextId, only_active)

        # собираем информацию о контекстах после инвалидации
        this_session, list_context_ids = self.get_information_about_session(session.sessionId)
        after_meta_context, after_data_context = self.get_contexts_from_redis(session.contexts[0].contextId)

        self.check_session_changed_last_timestamp(this_session, session)
        self.assertEqual(len(session.contexts), len(list_context_ids), "Not equal to data from redis.")
        self.assertEqual(len(list_context_ids), 1, "Too many contexts")
        self.assertDictEqual(after_data_context, before_data_context)
        self.check_context_meta_data(after_meta_context, before_meta_context)
        self.check_context(session.sessionId, result, meta_context=after_meta_context, data_context=after_data_context)

    @expectedFailure  # TODO: https://jira.oorraa.net/browse/RT-760
    def test_getContextById_one_inactive_ctx_onlyActive_true(self):
        """ Проверка возвращения контекста для одной сессии с одним контекстом, onlyActive флаг = False и True.
        Если onlyActive == true, контекст будет возвращен только если он активен.
        Если контекст активен и refresh == true, его lastAccessTimestamp и expirationTimestamp будут обновлены.
        """
        service_log.run(self)
        only_active = True
        # Создаем новую сессию, дополнительные котексты для неё
        params_req = self.get_SessionContextRequestDto(**self.generate_default_session())
        session = services.session.root.tframed.initSession(params_req)
        service_log.put("Get session data: %s" % session)
        # инвалидируем контекст
        services.session.root.tframed.invalidateContext(session.contexts[0].contextId)
        service_log.put("Get session data after invalidate context: %s" % session)

        # собираем информацию о контекстах до инвалидации и получаем контекс сессии по его идентификатору
        before_meta_context, before_data_context = self.get_contexts_from_redis(session.contexts[0].contextId)
        result = services.session.root.tframed.getContextById(session.contexts[0].contextId, only_active)

        # собираем информацию о контекстах после инвалидации
        this_session, list_context_ids = self.get_information_about_session(session.sessionId)
        after_meta_context, after_data_context = self.get_contexts_from_redis(session.contexts[0].contextId)

        self.assertIsNone(result)
        self.check_session_changed_last_timestamp(this_session, session)
        self.assertEqual(len(session.contexts), len(list_context_ids), "Not equal to data from redis.")
        self.assertEqual(len(list_context_ids), 1, "Too many contexts")
        self.assertDictEqual(after_data_context, before_data_context)
        self.check_context_meta_data(after_meta_context, before_meta_context)

    @data(["agent", False], ["auth", False], ["agent", True], ["auth", True])
    @unpack
    def test_getContextForSession_one_ctx(self, context_type="auth", only_active=True):
        """ Проверка getContextForSession с одним контекстом и разнами типа контекстов.
        Возвращает контекст данного типа для данной сессии.
        Если onlyActive == true, контекст будет возвращен только если он активен.
        """
        service_log.run(self)
        # Создаем новую сессию, дополнительные котексты для неё
        context_params = self.generate_default_session(context_type)
        params_req = self.get_SessionContextRequestDto(**context_params)
        session = services.session.root.tframed.initSession(params_req)
        service_log.put("Get session data: %s" % session)

        # собираем информацию о контекстах до инвалидации и получаем контекс сессии по его идентификатору
        before_meta_context, before_data_context = self.get_contexts_from_redis(session.contexts[0].contextId)
        result = services.session.root.tframed.getContextForSession(session.sessionId, context_type, only_active)

        # собираем информацию о контекстах и сессии после инвалидации
        after_meta_context, after_data_context = self.get_contexts_from_redis(session.contexts[0].contextId)
        this_session, list_context_ids = self.get_information_about_session(session.sessionId)

        self.check_session_changed_last_timestamp(this_session, session)
        self.assertEqual(len(session.contexts), len(list_context_ids), "Not equal to data from redis.")
        self.assertEqual(len(list_context_ids), 1, "Too many contexts")
        self.assertDictEqual(after_data_context, before_data_context)
        self.check_context_meta_data(after_meta_context, before_meta_context)
        self.check_context(session.sessionId, result, meta_context=after_meta_context, data_context=after_data_context)

    def test_test_getContextForSession_several_ctx(self):
        # TODO: несколько контекстов
        pass

    @data(True, False)
    def test_getSessionById_one_ctx(self, only_active=True):
        """ Проверка getSessionById с одним контекстом.
        Возвращает сессию по ID. Сессия включает все свои контексты.
        Если onlyActive == true, возвращаются только активные контексты.
        :return:
        """
        service_log.run(self)
        # Создаем новую сессию, дополнительные котексты для неё
        context_params = self.generate_default_session()
        params_req = self.get_SessionContextRequestDto(**context_params)
        session = services.session.root.tframed.initSession(params_req)
        service_log.put("Get session data: %s" % session)

        # собираем информацию о контекстах до инвалидации и получаем контекс сессии по его идентификатору
        before_meta_context, before_data_context = self.get_contexts_from_redis(session.contexts[0].contextId)
        result = services.session.root.tframed.getSessionById(session.sessionId, only_active)

        # собираем информацию о контекстах и сессии после инвалидации
        after_meta_context, after_data_context = self.get_contexts_from_redis(session.contexts[0].contextId)
        this_session, list_context_ids = self.get_information_about_session(session.sessionId)

        self.check_session_changed_last_timestamp(this_session, session)
        self.assertEqual(len(session.contexts), len(list_context_ids), "Not equal to data from redis.")
        self.assertEqual(len(list_context_ids), 1, "Too many contexts")
        self.assertDictEqual(after_data_context, before_data_context)
        self.check_context_meta_data(after_meta_context, before_meta_context)
        self.check_context(session.sessionId, result.contexts[0], meta_context=after_meta_context, data_context=after_data_context)

    @classmethod
    def tearDown(cls):
        service_log.end()


class TestSessionOther(AuxiliarySession):

    @expectedFailure  # TODO: https://jira.oorraa.net/browse/RT-761
    def test_context_expired_for_one_ctx(self, time_sleep=60):
        """ Проверка перехода контекста в статус EXPIRED.
        Создаем новую сессию с expirationPeriodMillis=1 в SessionContextRequestDto
        Ждем минуту
        Проверяем статус в Redis и что другие данные не изменились
        Проверяем статус через метод getContextById, с параметром onlyActive=False
        Проверяем статус через метод getSessionById, с параметром onlyActive=False
        :param time_sleep: время ожидания перед тем как поменяется статус
        """
        service_log.run(self)
        # Создаем новую сессию с временем жизни контекста 1 мс
        context_params = self.generate_default_session()
        context_params.update({"period_millis": 1})
        params_req = self.get_SessionContextRequestDto(**context_params)
        session = services.session.root.tframed.initSession(params_req)
        service_log.put("Get session data: %s" % session)
        time.sleep(time_sleep)
        # собираем информацию о сессии и контекстах
        meta_context, data_context = self.get_contexts_from_redis(session.contexts[0].contextId)
        this_session, list_context_ids = self.get_information_about_session(session.sessionId)

        # проверка, что данные кроме статуса не изменились (и кроме некоторых таймеров)
        self.check_session(this_session, session)
        self.assertEqual(len(session.contexts), len(list_context_ids), "Not equal to data from redis.")
        self.assertEqual(len(list_context_ids), 1, "Too many contexts")
        self.assertEqual(meta_context['contextId'], session.contexts[0].contextId)
        self.assertEqual(meta_context['contextType'], session.contexts[0].contextType)
        self.assertEqual(int(meta_context['creationTimeStamp']), int(session.contexts[0].creationTimestamp))
        self.assertEqual(int(meta_context['expirationTime']), int(session.contexts[0].expirationTime))
        self.assertEqual(meta_context['refreshOnGet'], str(context_params['refresh_on_get']).lower())
        self.assertEqual(meta_context['refreshOnSet'], str(context_params['refresh_on_set']).lower())
        self.assertEqual(meta_context['sessionId'], session.contexts[0].sessionId)
        self.assertEqual(int(meta_context['expirationTimeStamp']), int(session.contexts[0].expirationTimestamp))
        self.assertEqual(int(meta_context['lastAccessTimeStamp']), int(session.contexts[0].lastAccessTimestamp))
        self.assertDictEqual(data_context, params_req.contextData)

        get_context = services.session.root.tframed.getContextById(session.contexts[0].contextId, False)
        get_session = services.session.root.tframed.getContextForSession(session.sessionId,
                                                                         context_params['context_type'], False)

        self.assertEqual(self.get_context_status(meta_context['contextStatus']), 1, "Status context not EXPIRED.")
        self.assertEqual(get_context.status, 1, "Status context not EXPIRED from getContextById.")
        self.assertEqual(get_session.status, 1, "Status context not EXPIRED from getContextForSession.")

    def test_refresh_on_get_false_getContextById(self):
        """ Проверка что флаг refresh_on_get = False работает для метода getContextById.
        Создаем новую сессию с флагом refresh_on_get = False.
        Вызываем метод getContextById.
        Проверяем, что время не изменилось.
        """
        service_log.run(self)
        # Создаем новую сессию с флагом refresh_on_get = False
        context_params = self.generate_default_session()
        context_params.update({"refresh_on_get": False})
        params_req = self.get_SessionContextRequestDto(**context_params)
        session = services.session.root.tframed.initSession(params_req)

        # собираем информацию о сессии и контекстах до всех операций
        before_meta_context = self.get_contexts_from_redis(session.contexts[0].contextId)[0]
        before_this_session = self.get_information_about_session(session.sessionId)[0]

        result = services.session.root.tframed.getContextById(session.contexts[0].contextId, False)
        self.assertEqual(int(before_meta_context['creationTimeStamp']), int(result.creationTimestamp))
        self.assertEqual(int(before_meta_context['expirationTimeStamp']), int(result.expirationTimestamp))
        self.assertEqual(int(before_meta_context['lastAccessTimeStamp']), int(result.lastAccessTimestamp))

        # собираем информацию о сессии и контекстах после всех операций
        after_this_session = self.get_information_about_session(session.sessionId)[0]
        after_meta_context = self.get_contexts_from_redis(session.contexts[0].contextId)[0]
        self.assertEqual(before_this_session['creationTime'], after_this_session['creationTime'])
        self.assertEqual(before_this_session['lastAccessTimeStamp'], after_this_session['lastAccessTimeStamp'])
        self.assertEqual(before_meta_context['creationTimeStamp'], after_meta_context['creationTimeStamp'])
        self.assertEqual(before_meta_context['expirationTimeStamp'], after_meta_context['expirationTimeStamp'])
        self.assertEqual(before_meta_context['lastAccessTimeStamp'], after_meta_context['lastAccessTimeStamp'])

    def test_refresh_on_get_false_getSessionById(self):
        """ Проверка что флаг refresh_on_get = False работает для метода getSessionById.
        Создаем новую сессию с флагом refresh_on_get = False.
        Вызываем методы getSessionById.
        Проверяем, что время не изменилось.
        """
        service_log.run(self)
        # Создаем новую сессию с флагом refresh_on_get = False
        context_params = self.generate_default_session()
        context_params.update({"refresh_on_get": False})
        params_req = self.get_SessionContextRequestDto(**context_params)
        session = services.session.root.tframed.initSession(params_req)

        # собираем информацию о сессии и контекстах до всех операций
        before_meta_context = self.get_contexts_from_redis(session.contexts[0].contextId)[0]
        before_this_session = self.get_information_about_session(session.sessionId)[0]

        result = services.session.root.tframed.getSessionById(session.sessionId, True)

        self.assertEqual(int(before_this_session['creationTime']), int(result.creationTimestamp))
        self.assertEqual(int(before_this_session['lastAccessTimeStamp']), int(result.lastAccessTimestamp))
        self.assertEqual(int(before_meta_context['creationTimeStamp']), int(result.contexts[0].creationTimestamp))
        self.assertEqual(int(before_meta_context['expirationTimeStamp']), int(result.contexts[0].expirationTimestamp))
        self.assertEqual(int(before_meta_context['lastAccessTimeStamp']), int(result.contexts[0].lastAccessTimestamp))

        # собираем информацию о сессии и контекстах после всех операций
        after_this_session = self.get_information_about_session(session.sessionId)[0]
        after_meta_context = self.get_contexts_from_redis(session.contexts[0].contextId)[0]
        self.assertEqual(before_this_session['creationTime'], after_this_session['creationTime'])
        self.assertEqual(before_this_session['lastAccessTimeStamp'], after_this_session['lastAccessTimeStamp'])
        self.assertEqual(before_meta_context['creationTimeStamp'], after_meta_context['creationTimeStamp'])
        self.assertEqual(before_meta_context['expirationTimeStamp'], after_meta_context['expirationTimeStamp'])
        self.assertEqual(before_meta_context['lastAccessTimeStamp'], after_meta_context['lastAccessTimeStamp'])

    def test_refresh_on_get_false_getContextForSession(self):
        """ Проверка что флаг refresh_on_get = False работает для метода getContextForSession.
        Создаем новую сессию с флагом refresh_on_get = False.
        Вызываем методы getContextForSession.
        Проверяем, что время не изменилось.
        """
        service_log.run(self)
        # Создаем новую сессию с флагом refresh_on_get = False
        context_params = self.generate_default_session()
        context_params.update({"refresh_on_get": False})
        params_req = self.get_SessionContextRequestDto(**context_params)
        session = services.session.root.tframed.initSession(params_req)

        # собираем информацию о сессии и контекстах до всех операций
        before_meta_context = self.get_contexts_from_redis(session.contexts[0].contextId)[0]
        before_this_session = self.get_information_about_session(session.sessionId)[0]

        result03 = services.session.root.tframed.getContextForSession(session.sessionId,
                                                                      context_params["context_type"], False)
        self.assertEqual(int(before_meta_context['creationTimeStamp']), int(result03.creationTimestamp))
        self.assertEqual(int(before_meta_context['expirationTimeStamp']), int(result03.expirationTimestamp))
        self.assertEqual(int(before_meta_context['lastAccessTimeStamp']), int(result03.lastAccessTimestamp))

        # собираем информацию о сессии и контекстах после всех операций
        after_this_session = self.get_information_about_session(session.sessionId)[0]
        after_meta_context = self.get_contexts_from_redis(session.contexts[0].contextId)[0]
        self.assertEqual(before_this_session['creationTime'], after_this_session['creationTime'])
        self.assertEqual(before_this_session['lastAccessTimeStamp'], after_this_session['lastAccessTimeStamp'])
        self.assertEqual(before_meta_context['creationTimeStamp'], after_meta_context['creationTimeStamp'])
        self.assertEqual(before_meta_context['expirationTimeStamp'], after_meta_context['expirationTimeStamp'])
        self.assertEqual(before_meta_context['lastAccessTimeStamp'], after_meta_context['lastAccessTimeStamp'])

    def test_refresh_on_set_false_replaceContextData(self):
        """ Проверка что флаг refresh_on_set = False работает для метода replaceContextData.
        Создаем новую сессию с флагом refresh_on_get = False.
        Вызываем метод replaceContextData.
        Проверяем, что время не изменилось.
        """
        service_log.run(self)
        # Создаем новую сессию с флагом refresh_on_get = False
        context_params = self.generate_default_session()
        context_params.update({"refresh_on_set": False})
        params_req = self.get_SessionContextRequestDto(**context_params)
        session = services.session.root.tframed.initSession(params_req)

        # собираем информацию о сессии и контекстах до всех операций
        before_meta_context = self.get_contexts_from_redis(session.contexts[0].contextId)[0]
        before_this_session = self.get_information_about_session(session.sessionId)[0]

        # рефрешем контекст и получаем данные о контекстах после этого
        params_ctx = {"Autotest_refresh": str(random.randint(1, 10000000000))}
        services.session.root.tframed.replaceContextData(session.contexts[0].contextId, params_ctx)

        # собираем информацию о сессии и контекстах после всех операций
        after_this_session = self.get_information_about_session(session.sessionId)[0]
        after_meta_context = self.get_contexts_from_redis(session.contexts[0].contextId)[0]
        self.assertEqual(before_this_session['creationTime'], after_this_session['creationTime'])
        self.assertEqual(before_this_session['lastAccessTimeStamp'], after_this_session['lastAccessTimeStamp'])
        self.assertEqual(before_meta_context['creationTimeStamp'], after_meta_context['creationTimeStamp'])
        self.assertEqual(before_meta_context['expirationTimeStamp'], after_meta_context['expirationTimeStamp'])
        self.assertEqual(before_meta_context['lastAccessTimeStamp'], after_meta_context['lastAccessTimeStamp'])