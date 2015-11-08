# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Файл с классами для работы с Accounting worker.
#--------------------------------------------------------------------
import random
from gen_py.AccountingBackOfficeWorker.ttypes import UserPasswordRequest, UserFieldsRequest, FindUserRequest, \
    CreateUserRequest, PermissionParamsRequest
from gen_py.AccountingWorker.ttypes import UserProfileDto, FindUserRequestDto, UserDto
from gen_py.AccountingWorkerConstants.ttypes import Gender, AccountStatus
from gen_py.Common.ttypes import Signature, PaginationDto
from gen_py.CommonConstants.ttypes import OrderingDirection
from support import service_log
from support.utils.common_utils import run_on_prod
from support.utils.db import databases
from support.utils.thrift4req import services
from support.utils.variables import EVariable
from tests.MainClass import MainClass

__author__ = 's.trubachev'


class AccountingData(MainClass):
    """
    Статические данные свойственные только AccountingWorker: переменные, константы, названия классов и т.д.
    """

    # Пользователи по умолчанию
    USER_SELLER_ID = {
        "www.oorraa": None,
        "front1.test.oorraa": '51',
        "front2.test.oorraa": '51',
    }

    USER_SELLER_ALIEN_ID = {
        "www.oorraa": None,
        "front1.test.oorraa": '26',
        "front2.test.oorraa": '26',

    }

    USER_BUYER_ID = {
        "www.oorraa": None,
        "front1.test.oorraa": '40',
        "front2.test.oorraa": '40',

    }

    USER_ADMIN_ID = {
        "www.oorraa": None,
        "front1.test.oorraa": '1',
        "front2.test.oorraa": '1',
    }

    USER_MODERATOR_ID = {
        "www.oorraa": None,
        "front1.test.oorraa": '28',
        "front2.test.oorraa": '28',

    }

    DEFAULT_USERS = {
        'seller': USER_SELLER_ID,
        'seller_alien': USER_SELLER_ALIEN_ID,
        'buyer': USER_BUYER_ID,
        'admin': USER_ADMIN_ID,
        'moderator': USER_MODERATOR_ID,
    }

    USER_LOCALE = 'ru'
    SAVE_HASH_USER_ID = None
    SAVE_HASH_USER_PASSWORD = None
    SAVE_HASH_USER_SALT = None

    DEFAULT_USER_PASSWORDS = {
        1: '123',
        2: '987',  # Warning: Не применять этот пароль для создания тестовых данных
        3: 'Balabuha',
        4: '12345',
        5: '123456'
    }

    USER_STATUS = ["ENABLED", "WAIT_FOR_REGISTRATION", "DISABLED"]


class AccountingMethods(AccountingData):

    @staticmethod
    def get_gender(name):
        """ Взять гендерное имя.
        :param name: гендерное имя {'MALE': 1, 'FEMALE': 2}
        :return: идентификатор гендерного имени
        """
        gender_name = Gender._NAMES_TO_VALUES[name] if name is not None else None
        service_log.put("Gender name: %s" % gender_name)
        return gender_name

    @staticmethod
    def get_status_id(name):
        """ Взять идентификатор аккаунт статуса пользователя.
        :param name: наименование статуса
        :return: идантификатор статуса
        """
        service_log.put("Name account status: %s" % AccountStatus._NAMES_TO_VALUES[name])
        return AccountStatus._NAMES_TO_VALUES[name]

    @staticmethod
    def get_default_locale():
        """ Взять локаль по умолчанию.
        :return: локаль
        """
        service_log.put("Get default user locale: %s" % AccountingMethods.USER_LOCALE)
        return AccountingMethods.USER_LOCALE

    @staticmethod
    def get_default_password(num=1):
        """ Взять пароль по умолчанию.
        :param num: номер пароля по умолчанию
        :return: пароль
        """
        msg = "Get default user password: %s"
        passwd = AccountingMethods.DEFAULT_USER_PASSWORDS[num]
        service_log.put(msg % passwd)
        return passwd

    @staticmethod
    def get_default_user_id(role='seller'):
        """ Взять идентификатор пользователя нужной роли.
        :param role: номер пароля по умолчанию
        :return: пароль
        """
        chars = '://'
        base_url = EVariable.front_base.url.strip()
        base_env = base_url[(base_url.find(chars) + len(chars)):base_url.rfind('.')]
        user_id = AccountingMethods.DEFAULT_USERS[role][base_env]
        service_log.put("Get default user Id: '%s' with role: '%s'" % (user_id, role))
        return user_id

    @staticmethod
    def get_FindUserRequestDto(part_phone, offset=0, limit=0, locale=AccountingData.USER_LOCALE):
        """ Получить объект FindUserRequestDto.
        :param part_phone: часть от номера телефона
        :param offset: смещение на количество записей
        :param limit: количество записей
        :param locale: локаль
        :return: FindUserRequestDto
        """
        request = FindUserRequestDto(phone_part=part_phone, limit=limit, offset=offset, locale=locale)
        service_log.put("Get request FindUserRequestDto for worker: %s" % request)
        return request

    @staticmethod
    def get_Signature(uuid=None, from_user_id=None, from_user_ip=None):
        """ Получить объект Signature.
        Сигнатура - системная информация для того, что бы отслеживать действия пользователя.
        :param uuid: уникальный идентификатор запроса
        :param from_user_id: ID пользователя в платформе
        :param from_user_ip:
        :return: Signature
        """
        sig = Signature(uuid=uuid, fromUserId=from_user_id, fromUserIP=from_user_ip)
        return sig

    @staticmethod
    def get_FindUserRequest(sig=None, phone=None):
        """ Получить объект FindUserRequest.
        sig(Signature) - никак не влияет на поиск, это процесс отслеживания действий пользователей.
        :param sig: сигнатура пользователя
        :param phone: телефон пользователя
        :return: FindUserRequest
        """
        request = FindUserRequest(sig=sig, phone=phone)
        service_log.put("Get request FindUserRequest for worker: %s" % request)
        return request


    @staticmethod
    def get_UserPasswordRequest(user_id=None, new_passwd=None, send_to_user=None):
        """ Получить объект UserPasswordRequest.
        :param user_id: идентификатор пользователя
        :param new_passwd: новый пароль
        :param send_to_user: type(bool) - отсылать ли сообщение пользователю
        :return: type(UserPasswordRequest)
        """
        request = UserPasswordRequest(userId=user_id, newPassword=new_passwd, sendToUser=send_to_user)
        service_log.put("Created obj UserPasswordRequest: %s" % request)
        return request

    @staticmethod
    def get_UserDto(user_id=None, reg_time=None, login_time=None, activ_time=None, a_status=None, online_status=None,
                    auth=None, login=None, auth_type=None, avatar_id=None, gender=None, phone=None, email=None,
                    name1=None, name2=None, name3=None, city=None, country=None, shop_address=None, inn=None, kpp=None,
                    ogrn=None, legal_address=None, actual_address=None, b_bic=None, b_contact=None, b_account=None,
                    b_corr=None, name4=None, r_news=None, r_notifications=None, r_reminders=None,
                    wants_seller=None, a_nonexpired=None, a_nonlocked=None, locale=None, shop=None):
        """ Получить объект UserDto.
        :param user_id: идентификатор пользователя
        :param reg_time: время регистрации
        :param login_time: время последнего залогинивания
        :param activ_time: время последней активности
        :param a_status: статус аккаунта
        :param online_status: онлайн статус
        :param auth: авторизация
        :param login: логин
        :param auth_type: тип аторизации
        :param avatar_id: идентификатор аватара
        :param gender: гендерная принадлежность
        :param phone: телефон
        :param email: электронная почта
        :param name1: имя
        :param name2: фамилия
        :param name3: отображаемое имя
        :param city: город
        :param country: страна
        :param shop_address: адрес магазина
        :param inn: идентификационный номер налогоплательщика (гос.номер)
        :param kpp: кодом причины постановки на учет (гос.номер)
        :param ogrn: основной государственный регистрационный номер (гос.номер)
        :param legal_address: легальный адрес
        :param actual_address: актуальный адрес
        :param b_bic: БИК банка
        :param b_contact: имя и адрес банка
        :param b_account: акканут банка
        :param b_corr: акканут кореспонденции банка
        :param name4: легальное имя
        :param r_news: получать новости сайта
        :param r_notifications: получать уведомления
        :param r_reminders: получать напоминания
        :param wants_seller: флаг - стать продавцом
        :param a_nonexpired: срок аккаунт истек
        :param a_nonlocked: аккаунт не заблокирован
        :param locale: локаль
        :param shop: магазин
        :return: type(UserDto)
        """
        p = UserDto(userId=user_id,
                    registrationTimestamp=reg_time, lastLoginTimestamp=login_time, lastActivityTimestamp=activ_time,
                    accountStatus=a_status, onlineStatus=online_status,
                    authorities=auth, login=login,
                    authType=auth_type, avatarId=avatar_id, gender=gender, phone=phone, email=email,
                    firstName=name1, lastName=name2, displayName=name3,
                    city=city, country=country, shopAddress=shop_address,
                    inn=inn, kpp=kpp, ogrn=ogrn,
                    legalAddress=legal_address, actualAddress=actual_address,
                    bankBic=b_bic, bankNameAndAddress=b_contact, bankAccount=b_account, bankCorrespondentAccount=b_corr,
                    legalName=name4,
                    receiveSiteNews=r_news, receiveNotifications=r_notifications, receiveReminders=r_reminders,
                    wantsToBeSeller=wants_seller,
                    accountNonExpired=a_nonexpired, accountNonLocked=a_nonlocked,
                    locale=locale,
                    shop=shop)
        service_log.put("Created obj UserDto: %s" % p)
        return p

    @staticmethod
    def get_UserFieldsRequest(dto=None, fields_to_remove=None):
        """ Получить объект UserFieldsRequest.
        :param dto: объект UserDto
        :param fields_to_remove:  - набор имен полей, чтобы удалить из БД
        :return: type(UserFieldsRequest)
        """
        request = UserFieldsRequest(dto=dto, fieldsToRemove=fields_to_remove)
        service_log.put("Created obj UserPasswordRequest: %s" % request)
        return request

    @staticmethod
    def get_CreateUserRequest(sig=None, user=None, password=None):
        """ Получить объект CreateUserRequest.
        :param sig: сигнатура пользователя
        :param user: объект UserDto
        :param password: пароль
        :return: type(CreateUserRequest)
        """
        request = CreateUserRequest(sig=sig, user=user, password=password)
        service_log.put("Created obj CreateUserRequest: %s" % request)
        return request

    @staticmethod
    def get_name_OrderingDirection(name, all_item):
        """ Получить имя направления выборки.
        :param name: имя выборки
        :param all_item: флаг, взять все значения
        :return: номер
        """
        if all_item is True:
            service_log.put("Get OrderingDirection names: %s" % OrderingDirection._VALUES_TO_NAMES.keys())
            return OrderingDirection._VALUES_TO_NAMES.keys()
        else:
            moderation_state_name = OrderingDirection._VALUES_TO_NAMES[name]
            service_log.put("Get OrderingDirection name: %s" % moderation_state_name)
            return moderation_state_name

    @staticmethod
    def get_number_OrderingDirection(number, all_item):
        """ Получить номер направления выборки.
        :param number: номер
        :param all_item: флаг, взять все значения
        :return: название направления выборки
        """
        if all_item is True:
            service_log.put("Get OrderingDirection number: %s" % OrderingDirection._NAMES_TO_VALUES.keys())
            return OrderingDirection._NAMES_TO_VALUES.keys()
        else:
            moderation_state_number = OrderingDirection._NAMES_TO_VALUES[number]
            service_log.put("Get OrderingDirection number: %s" % moderation_state_number)
            return moderation_state_number

    @staticmethod
    def get_OrderingDirection(data, all_item=False):
        """ Получить направление выборки.
        :param data: строка или число
        :return: число или строка
        """
        if type(data) == str:
            return AccountingMethods.get_number_OrderingDirection(data, all_item)
        elif type(data) == int:
            return AccountingMethods.get_name_OrderingDirection(data, all_item)

    @staticmethod
    def get_PaginationDto(direction=1, limit=None, offset=None):
        """ Получить объект PaginationDto.
        :param direction: направления, type(OrderingDirection)
        :param limit: лимит
        :param offset: сдвиг
        :return: type(PaginationDto)
        """
        p = PaginationDto(direction=direction, limit=limit, offset=offset)
        service_log.put("Created obj PaginationDto: %s" % p)
        return p

    @staticmethod
    def get_PermissionParamsRequest(pagination=None, id_set=None, name_set=None):
        """ Получить объект PermissionParamsRequest.
        :param pagination: объект пагинации, type(PaginationDto)
        :param id_set: список идентификаторов прав
        :param name_set: список названия прав
        :return: type(PermissionParamsRequest)
        """
        request = PermissionParamsRequest(pagination=pagination, idSet=id_set, nameSet=name_set)
        service_log.put("Created obj PermissionParamsRequest: %s" % request)
        return request

    @staticmethod
    def get_direction_for_sql(val):
        """ Вернуть название сортировки для соотв. с SQL.
        :param val: значение OrderingDirection
        :return: значение SQL
        """
        p = {"DESCENDING": "DESC", "ASCENDING": "ASC"}
        return p[val]

    @staticmethod
    def generate_session_id():
        """ Сгенерировать идентификатор сессии.
        :return: строка
        """
        session_id = str(random.randint(1000000000, 100000000000000))
        service_log.put("Session id for user: %s" % session_id)
        return session_id

    @staticmethod
    def generate_default_profile():
        """ Сгенерировать профиль по умолчанию
        :return: UserProfileDto
        """
        key_autotest = random.randint(1000000000, 1000000000000000)
        profile = {"locale": AccountingMethods.USER_LOCALE,
                   "login": "Autotest_%i" % key_autotest,
                   "phone": str(key_autotest),
                   "email": "mail_%s@autotest_oorraa.net" % key_autotest,
                   "gender": AccountingMethods.get_gender("MALE"),
                   "displayName": "DN_Autotest_%i" % key_autotest,
                   "firstName": "FN_Autotest_%i" % key_autotest,
                   "lastName": "LN_Autotest_%i" % key_autotest,
                   "city": "Москва",
                   "country": "Россия",
                   #"avatarUrl": "http://oorraa.net/static/app/images/oorraa_logo_lg.png" TODO: это удалено
        }
        user_profile = UserProfileDto(**profile)
        service_log.put("Get profile for worker: %s" % user_profile)
        return user_profile

    @staticmethod
    def save_user_password(user_id, hash_passwd, salt=None):
        """ Сохранить идентификатор и пароль пользователя.
        :param user_id: идентификатор пользователя
        :param hash_passwd: хеш-пароля
        :return: True
        """
        AccountingMethods.SAVE_HASH_USER_ID = user_id
        AccountingMethods.SAVE_HASH_USER_PASSWORD = hash_passwd
        AccountingMethods.SAVE_HASH_USER_SALT = salt
        return True

    @staticmethod
    @run_on_prod(False)
    def recover_user_password(link_db):
        """ Восстановить пароль пользователя и соль пользователя.
        Если переменная с паролем и идентификатором пользователь не пустые, обновлем пароль у этого пользователя.
        Если переменная с солью пользователя не пустая, восстанавливаем и её (обратная совеместимость).
        Если переменная с паролем и идентификатором пользователь были пустые, возвращаем False.
        :param link_db: ссылка на коннектор БД, например: databases.db1 (для гибкости схем запуска автотестов)
        :return: type(bool)
        """
        # TODO: Т.к. номер БД влияет на корректность запросов, передаем линк на коннектор БД для заданной схемы
        if AccountingMethods.SAVE_HASH_USER_PASSWORD and AccountingMethods.SAVE_HASH_USER_ID is not None:
            service_log.put("Try recover password hash for user ID's: %s" % AccountingMethods.SAVE_HASH_USER_ID)
            # databases.db1.accounting.update_user_password(AccountingMethods.SAVE_HASH_USER_ID,
            # AccountingMethods.SAVE_HASH_USER_PASSWORD)
            link_db.accounting.update_user_password(AccountingMethods.SAVE_HASH_USER_ID,
                                                    AccountingMethods.SAVE_HASH_USER_PASSWORD)
            service_log.put("Recovered password hash: %s" % AccountingMethods.SAVE_HASH_USER_PASSWORD)

            # если соль была сохранена
            if AccountingMethods.SAVE_HASH_USER_SALT is not None:
                service_log.put("Try recover salt for user ID's: %s" % AccountingMethods.SAVE_HASH_USER_SALT)
                # databases.db1.accounting.update_user_salt(AccountingMethods.SAVE_HASH_USER_ID,
                # AccountingMethods.SAVE_HASH_USER_SALT)
                link_db.accounting.update_user_salt(AccountingMethods.SAVE_HASH_USER_ID,
                                                    AccountingMethods.SAVE_HASH_USER_SALT)
                service_log.put("Recovered salt: %s" % AccountingMethods.SAVE_HASH_USER_SALT)

            AccountingMethods.SAVE_HASH_USER_ID = None
            AccountingMethods.SAVE_HASH_USER_PASSWORD = None
            AccountingMethods.SAVE_HASH_USER_SALT = None
            return True
        else:
            service_log.put("The variable with the user's password or ID is empty. Password recovery user cancelled.")
            return False

    @staticmethod
    @run_on_prod(False)
    def create_user_with_status(user_status):
        """ Создать пользователя с заданным статусом.
        WARNING: не работает в проде
        :param user_status: название статуса
        :return: идентификатор пользователя
        """
        service_log.put("*** Create new user with status: %s ***" % user_status)
        user_profile = AccountingCheckMethods.generate_default_profile()
        service_log.put("Generated user's profile: %s" % user_profile)
        user_with_status = services.accounting.root.tframed.createUserAndSendCredentials(user_profile)
        service_log.put("Created user: %s." % user_with_status)
        databases.db1.accounting.update_user_status(user_with_status.userId, user_status)
        service_log.put("Changed user's status: %s." % user_status)
        return user_with_status.userId

    @staticmethod
    def create_unique_phone(link_db, limit=1000):
        """ Получить уникальный номер телефона для БД.
        :param link_db: ссылка на БД из которой будут браться значения
        :param limit: количество попыток
        :return: номер телефона
        """
        count = 0
        while count != limit:
            new_phone = '7' + str(random.randint(1000000000, 8999999999))
            ph = link_db.accounting.get_users_by_phone(new_phone)
            service_log.put("Generate new phone for new user: %s BD return: %s" % (new_phone, str(ph)))
            if len(ph) == 0:
                return new_phone
            count = ++count
        assert AssertionError("Warning: The phone is not picked up.")

    @staticmethod
    def create_params_by_duplicate_for_UserDto(user_db):
        """ Создаём общие параметры для UserDto.
        :param user_db: дубликат пользователя
        :return: словарь с данными
        """
        import time
        pr_name = int(time.time())
        mas = {"user_id": None,
               "reg_time": pr_name, "login_time": None, "activ_time": None,
               "a_status": None,
               "online_status": None,
               "auth": None, "login": None,
               "auth_type": None,
               "avatar_id": user_db['avatar_id'],
               "gender": 1,
               "phone": None,
               "email": "autotest_%s%s@autotest.com" % (str(pr_name), random.randint(0, 1000)),
               "name1": str(pr_name),
               "name2": str(pr_name),
               "name3": "autotest_" + str(pr_name),
               "city": user_db['city'],
               "country": user_db['country'],
               "shop_address": user_db['shop_address'],
               "inn": user_db['inn'], "kpp": user_db['kpp'], "ogrn": user_db['ogrn'],
               "legal_address": user_db['legal_address'], "actual_address": user_db['actual_address'],
               "b_bic": user_db['bank_bic'], "b_contact": user_db['bank_name_and_address'],
               "b_account": user_db['bank_account'], "b_corr": user_db['bank_correspondent_account'],
               "name4": str(user_db['legal_name']) + str(pr_name),
               "r_news": user_db['receive_site_news'], "r_notifications": user_db['receive_notifications'],
               "r_reminders": user_db['receive_reminders'], "wants_seller": user_db['wants_to_be_seller'],
               "a_nonexpired": user_db['account_non_expired'], "a_nonlocked": user_db['account_non_locked'],
               "locale": user_db['locale'],
               "shop": None}
        service_log.put("Dict for obj: %s" % str(mas))
        return mas

    @staticmethod
    def is_the_permission_have_group_inner(data):
        """ Определяем, имеет ли разрешение в качестве наследников другие группы.
        Если имеет - возвращаем True, иначе возвращаем False.
        :param data: данные таблица inner_permissions
        :return: type(bool)
        """
        if data is not None:
            if len(data) != 0:
                return True
            else:
                return False
        else:
            return False



class AccountingCheckMethods(AccountingMethods):

    def check_data_users_without_id(self, user1, user2):
        """ Сравнение данных пользователя от сервиса, с данными из БД без его идентификатора.
        :param user1: данные полученные от сервиса
        :param user2: сгенерированные данные
        :return: None or Exception
        """
        service_log.put("Compare field user logins, %s and %s" % (user1.profile.login, user2.login))
        self.assertEqual(user1.profile.login, user2.login, "Do not match the user login.")
        self.assertEqual(user1.profile.firstName, user2.firstName, "Do not match the user's firstName.")
        self.assertEqual(user1.profile.lastName, user2.lastName, "Do not match the user's lastName.")
        self.assertEqual(user1.profile.gender, user2.gender, "Do not match the user's gender.")
        self.assertEqual(user1.profile.phone, user2.phone, "Do not match the user phone.")
        self.assertEqual(user1.profile.email, user2.email, "Do not match the user email.")
        self.assertEqual(user1.profile.city, user2.city, "Do not match the user's city.")
        self.assertEqual(user1.profile.country, user2.country, "Do not match the user's country.")
        self.assertEqual(user1.profile.displayName, user2.displayName, "Do not match the user's displayName.")
        #self.assertEqual(user1.profile.avatarUrl, user2.avatarUrl, "Do not match the user's avatarUrl.")
        # TODO: от этого поля планируют избавиться, вместо него будет id Аватара, url будет генериться на стороне ноды.
        self.assertEqual(user1.profile.locale, user2.locale, "Do not match the locale user.")  # TODO: Баг

    def check_user(self, result, user):
        """ Сравнение данных пользователя от сервиса, с данными из БД.
        :param result: данный пользователя от сервиса
        :param user: данные пользователя из БД
        :return: None or Exception
        """
        service_log.put("Compare field user IDs, %s and %s" % (result.userId, user["id"]))
        self.assertEqual(result.userId, user["id"], "Do not match the user IDs.")
        self.assertEqual(result.profile.login, user["login"], "Do not match the user login.")
        self.assertEqual(result.profile.firstName, user["first_name"], "Do not match the user's firstName.")
        self.assertEqual(result.profile.lastName, user["last_name"], "Do not match the user's lastName.")
        self.assertEqual(result.profile.locale, user["locale"], "Do not match the locale user.")
        self.assertEqual(result.profile.gender, self.get_gender(user["gender"]), "Do not match the user's gender.")
        self.assertEqual(result.profile.phone, user["phone"], "Do not match the user phone.")
        self.assertEqual(result.profile.email, user["email"], "Do not match the user email.")
        self.assertEqual(result.profile.city, user["city"], "Do not match the user's city.")
        self.assertEqual(result.profile.country, user["country"], "Do not match the user's country.")
        self.assertEqual(result.profile.displayName, user["display_name"], "Do not match the user's displayName.")
        # TODO: от этого поля планируют избавиться, вместо него будет id Аватара, url будет генериться на стороне ноды.
        #self.assertEqual(result.profile.avatarUrl, user["avatar_url"], "Do not match the user's avatarUrl.")

    def check_UserDto_and_account_details(self, user_dto, account_details):
        """ Сравнение данных таблицы account_details и возвращаемого объекта UserDto.

        Внимание!
        Т.к. в account_details и UserDto храниться только часть инфы, то сравнение следующих данных не происходит -
        Для UserDto:
            accountStatus, authorities, authType, lastActivityTimestamp, lastLoginTimestamp,
            onlineStatus, registrationTimestamp, shop
        Для account_details:
            credentials_non_expired, enabled, id, shop_id

        :param user_dto: объект UserDto
        :param account_details: словарь данных account_details
        """
        self.assertEqual(user_dto.accountNonExpired, account_details["account_non_expired"])
        self.assertEqual(user_dto.accountNonLocked, account_details["account_non_locked"])
        self.assertEqual(user_dto.actualAddress, account_details["actual_address"])
        self.assertEqual(user_dto.avatarId, account_details["avatar_id"])
        self.assertEqual(user_dto.bankAccount, account_details["bank_account"])
        self.assertEqual(user_dto.bankBic, account_details["bank_bic"])
        self.assertEqual(user_dto.bankCorrespondentAccount, account_details["bank_correspondent_account"])
        self.assertEqual(user_dto.bankNameAndAddress, account_details["bank_name_and_address"])
        self.assertEqual(user_dto.city, account_details["city"])
        self.assertEqual(user_dto.country, account_details["country"])
        self.assertEqual(user_dto.displayName, account_details["display_name"])
        self.assertEqual(user_dto.email, account_details["email"])
        self.assertEqual(user_dto.firstName, account_details["first_name"])
        self.assertEqual(user_dto.gender, self.get_gender(account_details["gender"]))
        self.assertEqual(user_dto.inn, account_details["inn"])
        self.assertEqual(user_dto.kpp, account_details["kpp"])
        self.assertEqual(user_dto.lastName, account_details["last_name"])
        self.assertEqual(user_dto.legalAddress, account_details["legal_address"])
        self.assertEqual(user_dto.legalName, account_details["legal_name"])
        self.assertEqual(user_dto.locale, account_details["locale"])
        self.assertEqual(user_dto.login, account_details["login"])
        self.assertEqual(user_dto.ogrn, account_details["ogrn"])
        self.assertEqual(user_dto.phone, account_details["phone"])
        self.assertEqual(user_dto.receiveNotifications, account_details["receive_notifications"])
        self.assertEqual(user_dto.receiveReminders, account_details["receive_reminders"])
        self.assertEqual(user_dto.receiveSiteNews, account_details["receive_site_news"])
        self.assertEqual(user_dto.shopAddress, account_details["shop_address"])
        self.assertEqual(user_dto.wantsToBeSeller, account_details["wants_to_be_seller"])

    def check_signature(self, sig, user_id=0, user_ip=None, uuid=None):
        """ Проверяем сигнатуру пользователя.
        :param sig: полученная сигнатура
        :param user_id: идентификатор пользователя
        :param ip: ip-адрес
        :param uuid: уникальный идентификатор
        """
        self.assertEqual(sig.fromUserId, user_id, "Not equal user_id")
        self.assertEqual(sig.fromUserIP, user_ip, "Not equal user_ip")
        self.assertEqual(sig.uuid, uuid, "Not equal uuid")

    def check_permission(self, permission_db, permission_worker):
        """ Проверяем данные из табл. permission с данными из  воркера.
        :param permission_db:
        :param permission_worker:
        """
        self.assertEqual(permission_db["id"], permission_worker.id, "Permission id is not equal.")
        self.assertEqual(permission_db["description"], permission_worker.description, "Description is not equal.")
        self.assertEqual(permission_db["name"], permission_worker.name, "Permission name is not equal.")