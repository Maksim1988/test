# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Tests accounting worker.
#--------------------------------------------------------------------
import random
from unittest import skip, expectedFailure
from ddt import ddt, data
import funky
import time
from support.utils.common_utils import run_on_prod, generate_sha256, random_string
from support.utils.db import databases
from support.utils.thrift4req import services
from support import service_log
from tests.worker_accounting.class_accounting import AccountingCheckMethods

__author__ = 's.trubachev'


@ddt
class TestAccountingBackOfficeWorkerUpdate(AccountingCheckMethods):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        # выбираем пользователя
        user = int(cls.get_default_user_id("seller"))
        # достаём его текущи пароль и запоминаем его
        cls.user = databases.db1.accounting.get_user_by_account_id(user)[0]
        cls.save_user_password(user_id=user, hash_passwd=cls.user["code_value"], salt=cls.user["salt"])
        cls.recover_user_password(databases.db1)
        service_log.preparing_env(cls)

    @run_on_prod(False)
    def test_updateUserPwd(self):
        """ Обновление пароля пользователя.
        метод updateUserPwd - при обновлении берется значение из таблички "auths" ассоциированное с данным
        пользователем, в выборке учавствует тип AuthType.AUTHORIZATION и поле "userId". Returns updated User DTO.
        """
        new_passwd = random_string()
        user_password_request = self.get_UserPasswordRequest(user_id=self.user["account_details_id"],
                                                             new_passwd=new_passwd,
                                                             send_to_user=False)
        user_before_changed = databases.db1.accounting.get_user_by_account_id(self.user["account_details_id"])[0]
        services.accounting_back.root.tframed.updateUserPwd(request=user_password_request)
        user_after_changed = databases.db1.accounting.get_user_by_account_id(self.user["account_details_id"])[0]
        new_hash_passwd = generate_sha256(new_passwd, user_after_changed["salt"])
        self.assertNotEqual(self.user["salt"], user_after_changed["salt"], "Salt passwd is equal.")
        self.assertNotEqual(self.user["code_value"], user_after_changed["code_value"], "Hash passwd is equal.")
        self.assertEqual(self.user["salt"], user_before_changed["salt"], "Salt passwd is not equal.")
        self.assertEqual(self.user["code_value"], user_before_changed["code_value"], "Hash passwd is not equal.")
        self.assertEqual(new_hash_passwd, user_after_changed["code_value"], "Generation SHA256 no equal.")

    @run_on_prod(False)
    @skip
    def test_updateUserPwd_sms(self):
        # TODO: смс. https://jira.oorraa.net/browse/RT-450
        pass

    @run_on_prod(False)
    @skip
    def test_updateUserFields_all_fields(self):
        """ Обновление полей пользователя.

        :return:
        """
        dto = self.get_UserDto()
        user_fields_request = self.get_UserFieldsRequest()
        services.accounting_back.root.tframed.updateUserFields(request=user_fields_request)
        pass

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        cls.recover_user_password(databases.db1)
        service_log.end()


class TestAccountingBackOfficeWorkerCreateUser(AccountingCheckMethods):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        service_log.preparing_env(cls)

    @run_on_prod(False)
    def test_createWithPwd(self):
        """ Создать пользователя с паролем.
        Метод createWithPwd - создает информацию о новом пользователе.
        Возвращает объект пользователя с проставленным новым userId.
        Пользователь будет создан со статусом WAIT_FOR_REGISTRATION
        """

        # создаем пользователя на основе дубликата
        choice_user = random.choice(databases.db1.accounting.get_users())
        params_new_user = self.create_params_by_duplicate_for_UserDto(choice_user)

        new_user = self.get_UserDto(**params_new_user)
        new_user.phone = self.create_unique_phone(databases.db1)

        # создаём пароль для пользователя
        password = random_string("letters")
        service_log.put("New user: %s" % str(new_user))
        user_from_worker = services.accounting_back.root.tframed.createWithPwd(user=new_user, password=password)
        user_from_db = databases.db1.accounting.get_users_by_phone(new_user.phone)

        # проверяем основные поля пользователя
        self.assertEqual(len(user_from_db), 1, "Find several user with phone: %s" % new_user.phone)
        self.check_UserDto_and_account_details(user_dto=user_from_worker, account_details=user_from_db[0])
        self.assertEqual(user_from_db[0]['id'], user_from_worker.userId, "Ids not equal.")
        # TODO: сравнить не только с account_details (провести полное сравнение полей)

        # проверяем пароль
        data_auths = databases.db1.accounting.get_auths(user_id=user_from_worker.userId)
        self.assertEqual(len(data_auths), 1, "Find several id with phone: %s" % user_from_worker.userId)
        self.assertIsNotNone(data_auths[0]["salt"], "Salt is None!")
        passwd_sha256 = generate_sha256(source_str=password, salt=data_auths[0]["salt"])
        self.assertEqual(passwd_sha256, data_auths[0]["code_value"], "Password is not correct!")

    @run_on_prod(False)
    def test_createUser_with_sig(self):
        """ Создать пользователя с сигнатурой.
        Метод createWithPwd - создает информацию о новом пользователе.
        Возвращает объект пользователя с проставленным новым userId.
        Пользователь будет создан со статусом WAIT_FOR_REGISTRATION
        """

        # создаем пользователя на основе дубликата
        choice_user = random.choice(databases.db1.accounting.get_users())
        params_new_user = self.create_params_by_duplicate_for_UserDto(choice_user)
        new_user = self.get_UserDto(**params_new_user)
        new_user.phone = self.create_unique_phone(databases.db1)

        # создаём пароль для пользователя
        password = random_string("letters")

        # создаем сигнатуру пользователя
        uuid = "%s_%s" % (int(time.time()), random_string(length=5))
        user_ip = "125.125.125.125"
        sig = self.get_Signature(uuid=uuid, from_user_ip=user_ip)

        request = self.get_CreateUserRequest(user=new_user, password=password, sig=sig)
        response_from_worker = services.accounting_back.root.tframed.createUser(request=request)
        user_from_worker = response_from_worker.user

        # ищем пользователя по телефона после его создания
        user_from_db = databases.db1.accounting.get_users_by_phone(new_user.phone)

        # получаем пароль и его соль
        data_auths = databases.db1.accounting.get_auths(user_id=user_from_worker.userId)
        passwd_sha256 = generate_sha256(source_str=password, salt=data_auths[0]["salt"])

        # проверяем сигнатуру
        self.check_signature(sig=response_from_worker.sig, user_ip=user_ip, uuid=uuid)

        # проверяем основные поля пользователя
        self.assertEqual(len(user_from_db), 1, "Find several user with phone: %s" % new_user.phone)
        self.check_UserDto_and_account_details(user_dto=user_from_worker, account_details=user_from_db[0])
        self.assertEqual(user_from_db[0]['id'], user_from_worker.userId, "Ids not equal.")
        # TODO: сравнить не только с account_details (провести полное сравнение полей)

        # проверяем пароль
        self.assertEqual(len(data_auths), 1, "Find several id with phone: %s" % user_from_worker.userId)
        self.assertIsNotNone(data_auths[0]["salt"], "Salt is None!")
        self.assertEqual(passwd_sha256, data_auths[0]["code_value"], "Password is not correct!")

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        service_log.end()


class TestAccountingBackOfficeWorkerFind(AccountingCheckMethods):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        service_log.preparing_env(cls)

    def test_findUserByPhone(self):
        """ Найти пользователя по номеру телефона.
        """
        user = random.choice(databases.db1.accounting.get_users())
        phone = user["phone"]
        result = services.accounting_back.root.tframed.findUserByPhone(phone=phone)
        self.check_UserDto_and_account_details(user_dto=result, account_details=user)
        # TODO: метод может быть удалён

    def test_findUser_without_sig(self):
        """ Найти пользователя по запросу.
        запрос без сигнатуры пользователя
        """
        user = random.choice(databases.db1.accounting.get_users())
        phone = user["phone"]
        request = self.get_FindUserRequest(phone=phone)
        result = services.accounting_back.root.tframed.findUser(request=request)
        self.check_UserDto_and_account_details(user_dto=result.user, account_details=user)
        self.assertIsNone(result.sig, "Signature user is not None.")

    def test_findUser_with_sig(self):
        """ Найти пользователя по запросу.
        запрос без сигнатуры пользователя
        """
        user = random.choice(databases.db1.accounting.get_users())
        phone = user["phone"]
        uuid = "%s_%s" % (int(time.time()), random_string(length=5))
        user_ip = "125.125.125.125"
        user_id = user["id"]
        sig = self.get_Signature(uuid=uuid, from_user_ip=user_ip, from_user_id=user_id)

        request = self.get_FindUserRequest(phone=phone, sig=sig)
        result = services.accounting_back.root.tframed.findUser(request=request)
        self.check_UserDto_and_account_details(user_dto=result.user, account_details=user)
        self.assertEqual(result.sig.fromUserId, user_id, "Not equal user_id in sig")
        self.assertEqual(result.sig.fromUserIP, user_ip, "Not equal user_ip in sig")
        self.assertEqual(result.sig.uuid, uuid, "Not equal uuid in sig")

    @run_on_prod(False)
    def test_findAllAccountIds_check_by_postgresql(self):
        """ Поиск идентификаторов всех пользователей, проверка через БД.
        Внимание: запрос может создавать большую нагрузку на сервер.
        """
        result = services.accounting_back.root.tframed.findAllAccountIds()
        users = databases.db1.accounting.get_all_user_ids()
        list_ids = funky.pluck(users, "id")
        missing_ids = list()
        for user_id in list_ids:
            if user_id not in result:
                missing_ids.append(user_id)
        self.assertEqual(len(missing_ids), 0, "Missing user_ids=%s" % str(missing_ids))
        self.assertEqual(len(list_ids), len(result), "Not equals user by BD and Worker (%s != %s)" % (len(list_ids),
                                                                                                      len(result)))

    @run_on_prod(False)
    @skip
    def test_findAllAccountIds_check_by_elasticsearch(self):
        """ Поиск идентификаторов всех пользователей, проверка через Elasticsearch.
        Внимание: запрос может создавать большую нагрузку на сервер.
        """
        # TODO: возможно следует написать тест (или включить тест-сьюты на проверку Elasticsearch)
        pass

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        service_log.end()


class TestAccountingBackOfficeWorkerPermissions(AccountingCheckMethods):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        см. https://confluence.oorraa.net/pages/viewpage.action?pageId=2785484
        """
        service_log.preparing_env(cls)

    @run_on_prod(False)
    @skip
    def test_createPermission(self):
        """ Название и описание (необязательный) для создания прав.
        """
        permission = None
        result = services.accounting_back.root.tframed.createPermission(permission=permission)
        pass

    @run_on_prod(False)
    @skip
    def test_updatePermission(self):
        """ Установить права.
        Чтобы добавить внутренний разрешения на разрешение типа группа просто установить:
        1. "permission" - права требуется обновить
        2. "innerPermissions" - набор разрешений, для добавления прав требуется обновить
        """
        request = None
        result = services.accounting_back.root.tframed.updatePermission(request=request)
        pass

    @expectedFailure
    def test_findPermissionByParams_number(self, count_permission=5):
        """ Найти permissions по идентификаторам.
        Warning: Ответ, содержит только уникальные значения идентиф.прав.
        """

        direction = self.get_OrderingDirection("DESCENDING")
        pagination = self.get_PaginationDto(direction=direction, limit=100, offset=0)

        # получаем список идентификаторов прав
        ids = databases.db1.accounting.get_permissions()
        set_ids = [random.choice(ids)["id"] for perm in range(count_permission)]

        request = self.get_PermissionParamsRequest(pagination=pagination, id_set=set_ids)
        result = services.accounting_back.root.tframed.findPermissionByParams(request=request)

        # проверяем количество вернувшихся permissions
        self.assertEqual(len(result.permissions), len(set(set_ids)), "Not equals count permissions")
        self.assertEqual(len(result.permissions), result.totalCount, "Not equals totalCount permissions")

        for perm in result.permissions:
            # находим данные необходимые о данном разрешении
            data_permission = databases.db1.accounting.get_permissions_by_id(permission_id=perm.id)[0]
            inner_perms = databases.db1.accounting.get_permissions_inner_by_id(permission_id=perm.id)
            flag_group = self.is_the_permission_have_group_inner(inner_perms)
            self.check_permission(data_permission, perm)
            self.assertEqual(flag_group, perm.group, "Not equal flag group inner permission.")
            self.assertIsNotNone(perm.permissions, "# TODO: https://jira.oorraa.net/browse/RT-486")
            # todo: # TODO: https://jira.oorraa.net/browse/RT-486

    @expectedFailure
    def test_findPermissionByParams_name(self, count_permission=3):
        """ Найти permissions по идентификаторам.
        Warning: Ответ, содержит только уникальные значения идентиф.прав.
        """

        direction = self.get_OrderingDirection("DESCENDING")
        pagination = self.get_PaginationDto(direction=direction, limit=100, offset=0)

        # получаем список идентификаторов прав
        ids = databases.db1.accounting.get_permissions()
        set_names = [random.choice(ids)["name"] for perm in range(count_permission)]

        request = self.get_PermissionParamsRequest(pagination=pagination, name_set=set_names)
        result = services.accounting_back.root.tframed.findPermissionByParams(request=request)

        # проверяем количество вернувшихся permissions
        self.assertEqual(len(result.permissions), len(set(set_names)), "Not equals count permissions")
        self.assertEqual(len(result.permissions), result.totalCount, "Not equals totalCount permissions")

        for perm in result.permissions:
            # находим данные необходимые о данном разрешении
            data_permission = databases.db1.accounting.get_permissions_by_id(permission_id=perm.id)[0]
            inner_perms = databases.db1.accounting.get_permissions_inner_by_id(permission_id=perm.id)
            flag_group = self.is_the_permission_have_group_inner(inner_perms)
            self.check_permission(data_permission, perm)
            self.assertEqual(flag_group, perm.group, "Not equal flag group inner permission.")
            self.assertIsNotNone(perm.permissions, "# TODO: https://jira.oorraa.net/browse/RT-486")
            # todo: # TODO: https://jira.oorraa.net/browse/RT-486

    @expectedFailure
    def test_findPermissionByParams_limitation(self):
        """ Проверка ограничения вывода permissions для метода findPermissionByParams.
        Warning1: Ответ, содержит только уникальные значения идентиф.прав.
        Warning2: объект PaginationDto не использует direction (по умолчанию direction=ASC)
        """
        offset = 1
        count_permission = 5

        # получаем список идентификаторов прав
        ids = databases.db1.accounting.get_permissions_with_sort_by_id(offset=offset, limit=count_permission)
        set_names = [perm["name"] for perm in ids]

        pagination = self.get_PaginationDto(limit=count_permission, offset=offset)
        request = self.get_PermissionParamsRequest(pagination=pagination, name_set=set_names)
        result = services.accounting_back.root.tframed.findPermissionByParams(request=request)
        self.assertEqual(len(result.permissions), count_permission, "todo: https://jira.oorraa.net/browse/RT-495")
        # todo: https://jira.oorraa.net/browse/RT-495

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        service_log.end()


class TestAccountingBackOfficeWorkerSearch(AccountingCheckMethods):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        service_log.preparing_env(cls)

    @run_on_prod(False)
    @skip
    def test_reIndex(self):
        """ Провести переиндексацию пользователей.
        Переиндексировать пользователей системы заново.
        При асинхронном использовании в ReIndexResponse вернется только totalCount.
        При синхронном использовании ReIndexResponse вернется с totalCount и заполненным userIds.
        """
        request = None
        result = services.accounting_back.root.tframed.reIndex(request=request)
        pass

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        cls.recover_user_password(databases.db1)
        service_log.end()


class TestAccountingBackOfficeWorkerReport(AccountingCheckMethods):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        service_log.preparing_env(cls)

    @skip("todo")
    def test_generateTotalsReport(self):
        """ Сгенерировать отчёт с количеством пользователей за всё время и с разбивкой по группам.
        """
        result = services.accounting_back.root.tframed.generateTotalsReport()
        user = databases.db1.accounting.get_all_user_ids()

        # Продавцы отмечаются статусом 2 или 6, что явл.равноценным
        seller1 = databases.db1.accounting.get_user_ids_by_permissions(permissions_id=2)
        seller2 = databases.db1.accounting.get_user_ids_by_permissions(permissions_id=6)

        list_ids = lambda ids, name: funky.pluck(ids, "id")
        user_count = len(list_ids(user, "id"))
        seller_count = len(list_ids(seller1, "account_details_id")) + len(list_ids(seller2, "account_details_id"))
        buyer_count = user_count - seller_count

        self.assertEqual(result.total, user_count, "Not equal count users from BD and Worker.")
        self.assertEqual(result.sellers, seller_count, "Not equal count sellers from BD and Worker.")
        self.assertEqual(result.buyers, buyer_count, "Not equal count buyers from BD and Worker.")

    @expectedFailure
    def test_generateTotalsReportPerDay(self):
        """ Сгенерирует отчёт с количеством пользователей за каждый день и с разбивкой по группам.
        """
        result = services.accounting_back.root.tframed.generateTotalsReportPerDay()
        # TODO: https://jira.oorraa.net/browse/RT-471 метод могут выпилить
        pass

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        service_log.end()