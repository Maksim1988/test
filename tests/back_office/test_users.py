# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
#         	Tests .
#--------------------------------------------------------------------
import datetime
import math
import time

from ddt import ddt, data

from support import service_log
from support.utils.db import databases
from support.utils.common_utils import generate_sha256, priority
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods as FrontAuthCheckMethods
from tests.back_office.class_auth import HelpAuthCheckMethods
from tests.back_office.class_users import HelpUsersCheckMethods
from tests.front_office.goods.classes.class_good import HelpGoodCheckMethods
from tests.front_office.settings.classes.class_profile_settings import HelpProfileSettingsCheckMethods as HPSCM

__author__ = 'm.senchuk'

@ddt
class TestUsersVisualLook(HelpLifeCycleMethods, HelpAuthCheckMethods, FrontAuthCheckMethods, HelpGoodCheckMethods,
                          HelpUsersCheckMethods):
    @classmethod
    def setUp(cls):
        # Подготовка данных для теста
        user_id = AccountingMethods.get_default_user_id(role='seller')
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)
        # Переходим на страницу авторизации бэка
        cls.get_back_page(cls.driver)
        cls.obj_login, cls.obj_pass, cls.obj_submit = cls.get_back_auth_data(cls.driver)

    @priority("medium")
    @data(*HelpAuthCheckMethods.ROLE)
    def test_users_page(self, role='admin'):
        """
        Проверка важных элементов на странице Учетные записи
        :return:
        """
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        self.check_navigate(self.driver, self.NAVIGATE_MENU_ITEM["Учетные записи"])
        self.get_element_navigate(self.driver, self.click_back_users.BTN_CREATE_USER)
        self.check_find_from_submit(self.driver)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()

@ddt
class TestUsersFiltration(HelpLifeCycleMethods, HelpAuthCheckMethods, FrontAuthCheckMethods, HelpGoodCheckMethods,
                          HelpUsersCheckMethods):
    @classmethod
    def setUp(cls):
        # Подготовка данных для теста
        cls.user_id = AccountingMethods.get_default_user_id(role='seller')
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)
        # Переходим на страницу авторизации бэка
        cls.get_back_page(cls.driver)
        cls.obj_login, cls.obj_pass, cls.obj_submit = cls.get_back_auth_data(cls.driver)

    @priority("medium")
    def test_filtration_by_creation_date(self, role='admin'):
        """
        Фильтрация по дате создания
        :return:
        """
        # login
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        # go to users
        self.check_navigate(self.driver, self.NAVIGATE_MENU_ITEM["Учетные записи"])
        # input date from
        self.click_button(self.get_element_navigate(self.driver, self.click_back_users.DATE_FROM))
        obj_date_from, date_1 = self.get_day_active(self.driver, self.click_back_users.DATE_FROM)
        self.click_button(obj_date_from)
        # input date to
        self.click_button(self.get_element_navigate(self.driver, self.click_back_users.DATE_TO))
        obj_date_to, date_2 = self.get_day_active(self.driver, self.click_back_users.DATE_TO)
        self.click_button(obj_date_to)
        # click Find button
        self.click_button(self.get_element_navigate(self.driver, self.click_back_users.BTN_FIND))
        # get date today and convert to timestamp
        date_from = int(str(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d')))[:-2]+"000")
        # get date today end
        date_to = date_from + 86399000
        # criteria for SQL query
        criteria = "registration_timestamp >= %s and registration_timestamp <=%s" % (date_from, date_to)
        # get users from table accounts
        users_account = databases.db1.accounting.get_accounts_by_criteria(criteria)
        # get count users in back-office after search
        count_users = int(self.get_element_navigate(self.driver, self.check_back_users.COUNT_USERS).text.encode('utf-8'))
        self.assertEqual(len(users_account), count_users, "Кол-во юзеров из базы '%s' и из бэк-офиса '%s' не совпадает"
                         % (len(users_account), count_users))
        pages = int(math.ceil(count_users/10.0))
        self.check_users(self.driver, pages, users_account)

    @priority("medium")
    @data(*HelpUsersCheckMethods.ROLES)
    def test_filtration_by_role(self, test_role, role='admin'):
        """Проверка фильтрации по ролям (админ,модер, заявка на роль)
        :param test_role:
        :param role:
        :return:
        """
        # login
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        # go to users
        self.check_navigate(self.driver, self.NAVIGATE_MENU_ITEM["Учетные записи"])
        # set role
        #role_list = self.get_element_navigate(self.driver, self.click_back_users.ROLE_LIST)
        #self.click_button(role_list)
        role = self.get_element_navigate(self.driver, self.click_back_users.SELECT_ROLE % self.ROLES[test_role]["role_name"])
        self.click_button(role)
        # click Find button
        self.click_button(self.get_element_navigate(self.driver, self.click_back_users.BTN_FIND))
        users_account = self.get_users_by_role(test_role, self.ROLES[test_role]["query"])

        # get count users in back-office after search
        count_users = int(self.get_element_navigate(self.driver, self.check_back_users.COUNT_USERS).text.encode('utf-8'))
        self.assertEqual(len(users_account), count_users, "Кол-во юзеров из базы '%s' и из бэк-офиса '%s' не совпадает"
                         % (len(users_account), count_users))
        pages = int(math.ceil(count_users/10.0))
        self.check_users(self.driver, pages, users_account, stop_test_pages=1)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestUsersSearch(HelpLifeCycleMethods, HelpAuthCheckMethods, FrontAuthCheckMethods, HelpGoodCheckMethods,
                      HelpUsersCheckMethods):
    @classmethod
    def setUp(cls):
        # Подготовка данных для теста
        cls.user_id = AccountingMethods.get_default_user_id(role='seller')
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)
        # Переходим на страницу авторизации бэка
        cls.get_back_page(cls.driver)
        cls.obj_login, cls.obj_pass, cls.obj_submit = cls.get_back_auth_data(cls.driver)

    @priority("medium")
    @data(*HelpAuthCheckMethods.ROLE)
    def test_search_by_name(self, role='admin', test_role='seller', param='Телефон/Имя'):
        """
        Поиск пользователя по имени (под модер, админ)
        :param role:
        :param param:
        :return:
        """
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        default_user_id = AccountingMethods.get_default_user_id(test_role)
        user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        user_account = databases.db1.accounting.get_user_account_info_by_id(user["id"])[0]
        self.check_navigate(self.driver, self.NAVIGATE_MENU_ITEM["Учетные записи"])
        input_field = self.get_input_field_find(self.driver)
        select_params_name_phone = self.get_select_param(self.driver, param)
        input_field.send_keys(user["display_name"].decode('utf-8'))
        self.click_button(select_params_name_phone)
        btn_find = self.get_element_navigate(self.driver, self.click_back_users.BTN_FIND)
        self.click_button(btn_find)
        count = self.get_info_line(self.driver, user)
        self.assertEqual(len(count), 1, "Найдено %s строк с упоминаниме номера телефона %s" % (len(count), user["phone"]))
        info_user_back = self.get_info_user_by_line(self.driver, count[0])
        info_user_db = self.get_info_user_by_db(user, user_account, test_role)
        self.assertEqual(info_user_back, info_user_db, "Данные из бэк офиса: '%s' не совпали с данными и базы: '%s'" %
                         (info_user_back, info_user_db))

    @priority("medium")
    @data(*HelpAuthCheckMethods.ROLE)
    def test_search_by_id(self, role, test_role='seller', param='ID'):
        """
        Поиск пользователя по ID (под модер, админ)
        :param role:
        :param param:
        :return:
        """
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        default_user_id = AccountingMethods.get_default_user_id(test_role)
        user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        user_account = databases.db1.accounting.get_user_account_info_by_id(user["id"])[0]
        self.check_navigate(self.driver, self.NAVIGATE_MENU_ITEM["Учетные записи"])
        input_field = self.get_input_field_find(self.driver)
        select_params_name_phone = self.get_select_param(self.driver, param)
        input_field.send_keys(user["id"])
        self.click_button(select_params_name_phone)
        btn_find = self.get_element_navigate(self.driver, self.click_back_users.BTN_FIND)
        self.click_button(btn_find)
        count = self.get_info_line(self.driver, user)
        self.assertEqual(len(count), 1, "Найдено %s строк с упоминаниме номера телефона %s" % (len(count), user["phone"]))
        info_user_back = self.get_info_user_by_line(self.driver, count[0])
        info_user_db = self.get_info_user_by_db(user, user_account, test_role)
        self.assertEqual(info_user_back, info_user_db, "Данные из бэк офиса: '%s' не совпали с данными и базы: '%s'" %
                         (info_user_back, info_user_db))

    @priority("medium")
    @data(*HelpAuthCheckMethods.ROLE)
    def test_search_by_phone(self, role, test_role='seller', param='Телефон/Имя'):
        """
        Поиск пользователя по номеру телефона (под модер, админ)
        :param role:
        :param param:
        :return:
        """
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        default_user_id = AccountingMethods.get_default_user_id(test_role)
        user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        user_account = databases.db1.accounting.get_user_account_info_by_id(user["id"])[0]
        self.check_navigate(self.driver, self.NAVIGATE_MENU_ITEM["Учетные записи"])
        input_field = self.get_input_field_find(self.driver)
        select_params_name_phone = self.get_select_param(self.driver, param)
        input_field.send_keys(user["phone"])
        self.click_button(select_params_name_phone)
        btn_find = self.get_element_navigate(self.driver, self.click_back_users.BTN_FIND)
        self.click_button(btn_find)
        count = self.get_info_line(self.driver, user)
        self.assertEqual(len(count), 1, "Найдено %s строк с упоминаниме номера телефона %s" % (len(count), user["phone"]))
        info_user_back = self.get_info_user_by_line(self.driver, count[0])
        info_user_db = self.get_info_user_by_db(user, user_account, test_role)
        self.assertEqual(info_user_back, info_user_db, "Данные из бэк офиса: '%s' не совпали с данными и базы: '%s'" %
                         (info_user_back, info_user_db))


    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestUsersCreation(HelpLifeCycleMethods, HelpAuthCheckMethods, FrontAuthCheckMethods, HelpGoodCheckMethods,
                        HelpUsersCheckMethods, HPSCM):
    @classmethod
    def setUp(cls):
        # Подготовка данных для теста
        user_id = AccountingMethods.get_default_user_id(role='seller')
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)
        # Переходим на страницу авторизации бэка
        cls.get_back_page(cls.driver)
        cls.obj_login, cls.obj_pass, cls.obj_submit = cls.get_back_auth_data(cls.driver)

    @priority("medium")
    @data(*HelpUsersCheckMethods.CREATE_USER_ROLE)
    def test_create_user_by_role(self, test_role="seller", role='admin'):
        """
        Создание пользователя через бэк и авторизация на фронте (админ/модер/покупатель/продавец)
        :return:
        """
        test_data = self.generate_test_data
        # login
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        # go to users
        self.check_navigate(self.driver, self.NAVIGATE_MENU_ITEM["Учетные записи"])
        # get and click button create user
        btn_create = self.get_element_navigate(self.driver, self.click_back_users.BTN_CREATE_USER)
        self.click_button(btn_create)
        # check form create user
        fields = self.get_fields_user_create_form(self.driver)
        self.check_form_create_user(self.driver)
        # set fields and submit create user
        self.set_input_fields_user_create_form(fields, test_data)
        obj_role = self.get_role(self.driver, self.CREATE_USER_ROLE[test_role]["name"])
        self.click_button(obj_role)
        self.click_button(fields['save'])
        # check user in db
        criteria = "display_name='%s' and gender='%s' and email='%s' and city='%s' and phone='%s'" % \
                   (test_data['name'], test_data['gender'], test_data['email'], test_data['city'], test_data['phone'])
        user = databases.db1.accounting.get_user_by_criteria("ENABLED", criteria)[0]
        # check success create in back
        self.check_success_create(self.driver, user["id"])
        # go auth in front
        self.get_page(self.driver, self.path_auth.PATH_AUTH)
        #self.click_to_phone(self.driver)
        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        # Вводим данные на авторизацию
        self.send_phone(phone_object=obj_phone, phone_number=user["phone"])
        self.send_password(password_object=obj_password, password_number=test_data['passwd'])
        # Нажатие на кнопку авторизации
        self.element_click(self.driver, obj_submit_button, change_page_url=True)
        # Переход на страницу "Настройки пользователя"
        HPSCM.go_profile_settings_page(self.driver)
        # Получаем инфо из базы о пользователе
        self.user_info = databases.db1.accounting.get_all_user_info_by_id(user_id=user["id"])[0]
        # Получаем список ролей пользователя
        self.user_roles = databases.db1.accounting.get_user_role_by_id(user_id=user["id"])
        role_list = [str(role["id"]) for role in self.user_roles]
        role_str = ','.join(role_list)
        self.assertIn(role_str, self.CREATE_USER_ROLE[test_role]["id"], "Роли не совпадают")
        self.check_common_info_all_roles(driver=self.driver, user_info=self.user_info, user_roles=self.user_roles)
        #self.get_element_navigate(self.driver, self.check_settings.FORM_ROLE_USER % self.CREATE_USER_ROLE[test_role]["name"])

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestUsersEdition(HelpLifeCycleMethods, HelpAuthCheckMethods, FrontAuthCheckMethods, HelpGoodCheckMethods,
                       HelpUsersCheckMethods, HPSCM):
    @classmethod
    def setUp(cls):
        # Подготовка данных для теста
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.test_user_id = AccountingMethods.get_default_user_id(role='seller_alien')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]

        cls.display_name = cls.user["display_name"]
        cls.user_roles_1 = databases.db1.accounting.get_user_role_by_id(user_id=cls.user["id"])
        cls.role_str_1 = ""
        for role in cls.user_roles_1:
            cls.role_str_1 += str(role["id"]) + ","
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"],
                                             salt=cls.user["salt"])
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)
        # Переходим на страницу авторизации бэка
        cls.get_back_page(cls.driver)
        cls.obj_login, cls.obj_pass, cls.obj_submit = cls.get_back_auth_data(cls.driver)

    @priority("medium")
    @data(*HelpAuthCheckMethods.ROLE)
    def test_edit_user(self, role='admin', param='ID'):
        """
        Редактирование пользователя через бэк и авторизация на фронте (смена пароля и имени под ролью админ/модер)
        :return:
        """
        test_data = self.generate_test_data_edit
        # login
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        # go to users
        self.check_navigate(self.driver, self.NAVIGATE_MENU_ITEM["Учетные записи"])
        input_field = self.get_input_field_find(self.driver)
        select_params_name_phone = self.get_select_param(self.driver, param)
        input_field.send_keys(self.user["id"])
        self.click_button(select_params_name_phone)
        btn_find = self.get_element_navigate(self.driver, self.click_back_users.BTN_FIND)
        self.click_button(btn_find)
        btn_edit = self.get_element_navigate(self.driver, self.click_back_users.BTN_EDIT % self.user["id"])
        self.click_button(btn_edit)
        fields = self.get_fields_user_edit_form(self.driver)
        self.clear_input_row(self.driver, fields["name"])
        self.set_input_fields_user_edit_form(fields, test_data)
        self.click_button(fields["save"])
        self.check_success_edit(self.driver)
        # go auth in front
        self.go_to_main_page(self.driver, env_base_url=self.ENV_BASE_URL)
        self.get_page(self.driver, self.path_auth.PATH_AUTH)
        #self.click_to_phone(self.driver)
        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        # Вводим данные на авторизацию
        self.send_phone(phone_object=obj_phone, phone_number=self.user["phone"])
        self.send_password(password_object=obj_password, password_number=test_data['passwd'])
        # Нажатие на кнопку авторизации
        self.element_click(self.driver, obj_submit_button, change_page_url=True)
        self.check_profile_widget(self.driver)
        # Переход на страницу "Настройки пользователя"
        HPSCM.go_profile_settings_page(self.driver)
        # Получаем инфо из базы о пользователе
        self.user_info = databases.db1.accounting.get_all_user_info_by_id(user_id=self.user["id"])[0]
        # Получаем список ролей пользователя
        self.user_roles_2 = databases.db1.accounting.get_user_role_by_id(user_id=self.user["id"])
        role_str_2 = ""
        for role in self.user_roles_2:
            role_str_2 += str(role["id"]) + ","
        self.assertIn(self.role_str_1, role_str_2)
        self.assertNotEqual(self.display_name, self.user_info["display_name"])

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()

@ddt
class TestUsersChangeStatus(HelpLifeCycleMethods, HelpAuthCheckMethods, FrontAuthCheckMethods, HelpGoodCheckMethods,
                            HelpUsersCheckMethods, HPSCM):
    @classmethod
    def setUp(cls):
        # Подготовка данных для теста
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.test_user_id = AccountingMethods.get_default_user_id(role='seller_alien')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]

        cls.display_name = cls.user["display_name"]
        cls.user_roles_1 = databases.db1.accounting.get_user_role_by_id(user_id=cls.user["id"])
        cls.role_str_1 = ""
        for role in cls.user_roles_1:
            cls.role_str_1 += str(role["id"]) + ","
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"],
                                             salt=cls.user["salt"])
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)
        # Переходим на страницу авторизации бэка
        cls.get_back_page(cls.driver)
        cls.obj_login, cls.obj_pass, cls.obj_submit = cls.get_back_auth_data(cls.driver)

    @priority("medium")
    @data(*HelpAuthCheckMethods.ROLE)
    def test_user_change_status(self, role='admin', param='ID'):
        """
        Заблокировать/разблокировать пользователя
        :return:
        """
        # login
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        # go to users
        self.check_navigate(self.driver, self.NAVIGATE_MENU_ITEM["Учетные записи"])
        input_field = self.get_input_field_find(self.driver)
        select_params_name_phone = self.get_select_param(self.driver, param)
        input_field.send_keys(self.test_user_id)
        self.click_button(select_params_name_phone)
        btn_find = self.get_element_navigate(self.driver, self.click_back_users.BTN_FIND)
        self.click_button(btn_find)
        user_old = databases.db1.accounting.get_user_by_criteria_only("id=%s" % self.test_user_id)[0]
        old_status = user_old["account_status"]
        change_status = self.get_element_navigate(self.driver, self.click_back_users.CHANGE_STATUS %
                                                  self.MAPPING_ENABLED_STATUS[old_status])
        self.click_button(change_status)
        self.change_status(self.driver, old_status)
        user_new = databases.db1.accounting.get_user_by_criteria_only("id=%s" % self.test_user_id)[0]
        new_status = user_new["account_status"]
        err_msg = "Статус пользователя не изменился. Старый статус %s, новый статус %s" % (old_status, new_status)
        self.assertNotEqual(old_status, new_status, err_msg)
        self.get_element_navigate(self.driver, self.click_back_users.CHANGE_STATUS %
                                  self.MAPPING_ENABLED_STATUS[new_status])

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()