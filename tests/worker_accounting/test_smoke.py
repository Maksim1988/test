# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Smoke tests.
#--------------------------------------------------------------------
from gen_py.AccountingWorker.ttypes import FindUserRequestDto
from tests.worker_accounting.class_accounting import AccountingCheckMethods

__author__ = 's.trubachev'

from support.utils.thrift4req import services
from support import service_log
import unittest


class TestSmokeAccountingSearchMethods(AccountingCheckMethods):

    """
    Тестирование методов поиска пользователя.
    Warning: используем статичные данные
    """

    # Данные существующего пользователя
    user_phone = '79111111111'
    user_login = '79111111111'
    user_passwd = '123'
    user_session = '54687654654'

    # Дополнительные параметры поиска
    users_limit = 0
    users_offset = 0

    @classmethod
    def setUp(cls):
        service_log.preparing_env(cls)

    def test_smoke_getUserDetailsById(self):
        """ Тестирование работы метода getUserDetailsById с протоколом Thrift.
        """
        result = services.accounting.root.tframed.getUserDetailsById(int(self.get_default_user_id('seller')),
                                                                     self.get_default_locale())

    def test_smoke_getUserDetailsByLogin(self):
        """ Тестирование работы метода getUserDetailsByLogin с протоколом Thrift.
        """
        result = services.accounting.root.tframed.getUserDetailsByLogin(TestSmokeAccountingSearchMethods.user_login,
                                                                        self.get_default_locale())

    def test_smoke_getUserDetailsByPhone(self):
        """ Тестирование работы метода getUserDetailsByPhone с протоколом Thrift.
        """

        result = services.accounting.root.tframed.getUserDetailsByPhone(TestSmokeAccountingSearchMethods.user_phone,
                                                                        self.get_default_locale())

    def test_smoke_findUserDetails(self):
        """ Тестирование работы метода findUserDetails с протоколом Thrift.
        """

        request = FindUserRequestDto(phone_part=TestSmokeAccountingSearchMethods.user_phone[:2],
                                     limit=TestSmokeAccountingSearchMethods.users_limit,
                                     offset=TestSmokeAccountingSearchMethods.users_offset,
                                     locale=self.get_default_locale())
        result = services.accounting.root.tframed.findUserDetails(request)

    @classmethod
    def tearDown(cls):
        services.accounting.root.close()
        service_log.end()


class TestSmokeAccountingSearchMethodsOfCreatingUser(AccountingCheckMethods):

    """
    Тестирование методов создания пользователя.
    Warning: используем статичные данные
    """

    # Данные существующего пользователя
    user_phone = '79111111111'
    user_login = '79111111111'
    user_passwd = '123'
    user_session = '546816546547654654'
    users_limit = 0
    users_offset = 0

    @classmethod
    def setUpClass(cls):
        service_log.preparing_env(cls)

    def test_smoke_accounting(self):
        """ Тестирование работы метода accounting с протоколом Thrift.
        """
        result = services.accounting.root.tframed.authenticate(TestSmokeAccountingSearchMethods.user_login,
                                                               TestSmokeAccountingSearchMethods.user_passwd,
                                                               TestSmokeAccountingSearchMethods.user_session)

    @classmethod
    def tearDown(cls):
        services.accounting.root.close()
        service_log.end()