# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Tests.
#--------------------------------------------------------------------

from ddt import ddt, data
from support.utils.common_utils import run_on_prod, generate_sha256, generation_items_pairwise
from support.utils.db import databases
from support.utils.thrift4req import services
from support import service_log
import unittest
import random
import funcy
from tests.worker_accounting.class_accounting import AccountingCheckMethods

__author__ = 's.trubachev'


@ddt
class TestAccountingSearchMethods(AccountingCheckMethods):

    """
    Тестирование методов поиска пользователя.
    Info: используем динамические данные
    """

    @classmethod
    def setUp(cls):
        service_log.preparing_env(cls)
        cls.user = dict(random.choice(databases.db1.accounting.get_users_by_status()))
        service_log.user(cls.user)

    def test_getUserDetailsById_for_exist_user(self):
        """ Тестирование работы метода getUserDetailsById на существующем пользователе.
        Выбираем произвольного пользователя, берём его идентификатор и подставляем в запрос к сервису.
        Сравниваем данные от сервиса, с данными из БД.
        """
        service_log.run(self)
        result = services.accounting.root.tframed.getUserDetailsById(self.user["id"], self.get_default_locale())
        service_log.put("Method getUserDetailsById returned result: %s" % result)
        self.check_user(result, self.user)

    def test_getUserDetailsByLogin_for_exist_user(self):
        """ Тестирование работы метода getUserDetailsByLogin на существующем пользователе.
        Выбираем произвольного пользователя, берём его логин и подставляем в запрос к сервису.
        Сравниваем данные от сервиса, с данными из БД.
        Warning: логин является уникальным полем
        """
        service_log.run(self)
        result = services.accounting.root.tframed.getUserDetailsByLogin(self.user["login"], self.get_default_locale())
        service_log.put("Method getUserDetailsByLogin returned result: %s" % result)
        self.check_user(result, self.user)

    def test_getUserDetailsByPhone_for_exist_user(self):
        """ Тестирование работы метода getUserDetailsByPhone на существующем пользователе.
        Выбираем произвольного пользователя, берём его номер телефона и подставляем в запрос к сервису.
        Сравниваем данные от сервиса, с данными из БД.
        Warning: номер телефона является уникальным полем
        """
        service_log.run(self)
        result = services.accounting.root.tframed.getUserDetailsByPhone(self.user["phone"], self.get_default_locale())
        service_log.put("Method getUserDetailsByPhone returned result: %s" % result)
        self.check_user(result, self.user)

    @data(*range(1, 10))
    def test_findUserDetails_for_exist_part_phone_for_all_users(self, iteration=None):
        """ Тестирование работы метода findUserDetails на существующем пользователе.
        Выбираем существующего пользователя и берём часть его номера телефона.
        Делаем выборку всех пользователей у которых совпадает часть номера телефона.
        Выборка части телефона производиться произвольным образом, поэтому делаем несколько итераций теста.
        """
        service_log.run(self)
        part_phone = self.user["phone"][:random.randint(1, len(self.user["phone"]))]
        self.assertNotEqual(len(self.user["phone"]), 0, "Find user without phone!!!")
        service_log.put("Get part phone user's: %s" % part_phone)
        users_with_part_phone = databases.db1.accounting.get_users_by_part_phone(part_phone)
        result = services.accounting.root.tframed.findUserDetails(self.get_FindUserRequestDto(part_phone))
        service_log.put("Method findUserDetails returned result: %s" % result)
        self.assertEqual(len(result), len(users_with_part_phone), "Does not match number of detected users.")
        for index in result:
            user = funcy.where(users_with_part_phone, id=index.userId)[0]
            self.check_user(index, user)

    @classmethod
    def tearDown(cls):
        services.accounting.root.close()
        service_log.end()


class TestAccountingMethodsAuthenticate(AccountingCheckMethods):

    """
    Тестирование методов аутентификации.
    Warning: необходим доступ на внесение изменений в БД
    """

    @classmethod
    def setUp(cls):
        service_log.preparing_env(cls)
        cls.user = random.choice(databases.db1.accounting.get_users_by_status())
        service_log.user(cls.user)

    @run_on_prod(False)
    def test_authenticate_for_exist_user(self):
        """ Тестирование метода аутентификации authenticate.
        Выбираем произвольного пользователя со статусом акаунта "ENABLE".
        Подменяем хеш его пароля в БД на заданный.
        Делаем запрос на аутентификацию и проверяем, что запрос отработал корректно.
        По завершении теста (не зависимо от результата) возвращаем хеш пользователя на первоночальный.
        """
        service_log.run(self)
        hash_res_new = generate_sha256(self.get_default_password())
        AccountingCheckMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["password"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)
        result = services.accounting.root.tframed.authenticate(self.user["phone"],
                                                               self.get_default_password(),
                                                               self.generate_session_id())
        service_log.put("Method authenticate returned result: %s" % result)
        self.check_user(result, self.user)

    @run_on_prod(False)
    def test_checkUserPassword_for_exist_user(self):
        """ Тестирование метода checkUserPassword.
        Выбираем произвольного пользователя со статусом акаунта "ENABLE".
        Подменяем хеш его пароля в БД на заданный.
        Делаем запрос на проверку пароля и проверяем, что запрос отработал корректно.
        По завершении теста (не зависимо от результата) возвращаем хеш пользователя на первоночальный.
        """
        service_log.run(self)
        hash_res_new = generate_sha256(self.get_default_password())
        AccountingCheckMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["password"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)
        result = services.accounting.root.tframed.checkUserPassword(self.user["phone"], self.get_default_password())
        service_log.put("Method checkUserPassword returned result: %s" % result)
        self.assertTrue(result, "Password for user - is not correct.")

    @run_on_prod(False)
    def test_createUserAndSendCredentials_with_all_fields(self):
        """ Тестирование метода createUserAndSendCredentials.
        Генерируем данные для профиля и создаём пользователя.
        Сравниваем результат из БД и возвращаемый результат метода.
        Сравниваем заданные поля и возвращаемый результат метода.
        """
        service_log.run(self)
        user_profile = self.generate_default_profile()
        result = services.accounting.root.tframed.createUserAndSendCredentials(user_profile)
        service_log.put("Method createUserAndSendCredentials returned result: %s" % result)
        user = dict(databases.db1.accounting.get_user_by_login(user_profile.login)[0])
        self.check_user(result, user)
        self.check_data_users_without_id(result, user_profile)

    @classmethod
    def tearDown(cls):
        service_log.end()
        AccountingCheckMethods.recover_user_password()
        services.accounting.root.close()


@ddt
class TestAccountingMethodUpdateStatus(AccountingCheckMethods):
    """
    Тестирование метода обновления статуса.
    Warning: необходим доступ на внесение изменений в БД
    """

    STATUSES_USER_IDS = dict()

    @classmethod
    def setUpClass(cls):
        """ Создаём тестовые данные.
        Создаём пользователей с заданными статусами.
        """
        statuses = AccountingCheckMethods.USER_STATUS
        cls.STATUSES_USER_IDS = {index: AccountingCheckMethods.create_user_with_status(index) for index in statuses}
        cls.msg_error_0 = "Changed the behavior of the method."
        cls.msg_error_1 = "The status must not be the same."
        cls.msg_error_2 = "The status must be same."

    @classmethod
    def setUp(cls):
        service_log.preparing_env(cls)

    @data(*generation_items_pairwise(AccountingCheckMethods.USER_STATUS))
    @run_on_prod(False)
    def test_updateUserStatus_for_new_users(self, combination_statuses):
        """ Тестирование метода обновления статуса.
        Создаём тестовые данные, пользователей с разными статусами.
        Берём пользователя с заданным статусом и изменяем его через метод API.
        Проверяем, что статус пользователя изменился.
        """
        service_log.run(self)
        # Определяем переменные статуса
        new_status = combination_statuses[1]
        new_status_id = self.get_status_id(new_status)
        user_id = self.STATUSES_USER_IDS[combination_statuses[0]]
        service_log.put("Combination of status: %s" % combination_statuses)
        service_log.put("ID user: %s" % user_id)

        # Запоминаем статус до внесения изменений
        account_before = dict(databases.db1.accounting.get_user_account_info_by_id(user_id)[0])
        service_log.put("Status before change: %s" % account_before)
        result = services.accounting.root.tframed.updateUserStatus(user_id, new_status_id)
        self.assertIsNone(result, self.msg_error_0)

        # Сравниваем статус после внесения изменений
        account_after = dict(databases.db1.accounting.get_user_account_info_by_id(user_id)[0])
        service_log.put("Status after change: %s" % account_before)
        self.assertNotEqual(account_before["account_status"], account_after["account_status"], self.msg_error_1)
        self.assertEqual(account_after["account_status"], new_status, self.msg_error_2)

    @classmethod
    def tearDown(cls):
        services.accounting.root.close()
        service_log.end()

    @classmethod
    def tearDownClass(cls):
        cls.STATUSES_USER_IDS = None


class TestAccountingMethodUpdatedPass(AccountingCheckMethods):
    """
    Тестирование методов обновления пароля.
    Warning: необходим доступ на внесение изменений в БД
    """

    @classmethod
    def setUp(cls):
        service_log.preparing_env(cls)
        # Делаем выборку пользователя в статусе ENABLE и подменяем пароль на другой, с которым будем работать.
        cls.user = dict(random.choice(databases.db1.accounting.get_users_by_status()))
        service_log.user(cls.user)

        cls.old_pass_user = cls.get_default_password(2)
        cls.new_pass_user = cls.get_default_password(1)
        hash_res_rep = generate_sha256(cls.old_pass_user)

        # Ставим пароль по умолчанию №2, т.к. первый может встречаться в "тестовых пользователях".
        AccountingCheckMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["password"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_rep)

    @run_on_prod(False)
    @unittest.expectedFailure  # bug: M-105
    def test_updateUserPassword_for_exist_user(self):
        """  Тестирование метода updateUserPassword.
        Выбираем произвольного пользователя в статусе ENABLE и запоминаем его пароль.
        Меняем его пароль на пароль №2.
        Делаем запрос к сервису на изменение пароля N2 на пароль № 1.
        Проверяем изменения в БД.
        Возвращаем первоночальный пароль пользователя.
        """
        # Меняем пароль при помощи сервиса
        result = services.accounting.root.tframed.updateUserPassword(userId=self.user["id"],
                                                                     oldPassword=self.old_pass_user,
                                                                     newPassword=self.new_pass_user)
        # Делаем проверку, что пароль изменился
        changed_user = databases.db1.accounting.get_user_by_id(self.user["id"])[0]
        service_log.user(changed_user)
        self.assertEqual(changed_user["password"], generate_sha256(self.new_pass_user), "The password is not changed.")
        self.assertIsNone(result, "Service not return None, service return: %s." % result)

    @run_on_prod(False)
    def test_updateUserPassword_same_password_for_exist_user(self):
        """  Тестирование метода updateUserPassword.
        Выбираем произвольного пользователя в статусе ENABLE и запоминаем его пароль.
        Меняем его пароль на пароль №2.
        Делаем запрос к сервису на изменение пароля N1 на такой же пароль № 1.
        Проверяем, что возвращается ошибка.
        Возвращаем первоночальный пароль пользователя.
        """
        self.tx = None
        try:
            # Меняем пароль при помощи сервиса
            services.accounting.root.tframed.updateUserPassword(self.user["id"], self.old_pass_user, self.old_pass_user)
        except Exception, self.tx:
            # TODO:  Ошибка, которая возвращается должна быть более информативная.
            pass
        finally:
            self.assertIsNotNone(self.tx, "Not found error for the same password")

    @unittest.expectedFailure
    @run_on_prod(False)
    def test_updateUserPasswordWithoutVerification_for_exist_user(self):
        """ Тестирование метода updateUserPasswordWithoutVerification.
        Warning: Поле sendToUser - отвечает за отправку смс. Состояение: False
        """
        service_log.run(self)
        # Меняем пароль при помощи сервиса
        user_id = self.user["id"]
        new_pass = self.get_default_password(1)
        result = services.accounting.root.tframed.updateUserPasswordWithoutVerification(user_id, new_pass,
                                                                                        sendToUser=False)

        # Делаем проверку, что пароль изменился
        changed_user = databases.db1.accounting.get_user_by_id(self.user["id"])[0]
        service_log.user(changed_user)
        self.assertEqual(changed_user["password"], generate_sha256(new_pass), "The password is not changed.")
        self.assertIsNone(result, "Service not return None, service return: %s." % result)

    @classmethod
    def tearDown(cls):
        services.accounting.root.close()
        AccountingCheckMethods.recover_user_password()
        service_log.end()