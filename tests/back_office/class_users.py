# -*- coding: utf-8 -*-
import random
import time

from support import service_log
from support.utils.db import databases
from support.utils import common_utils
from tests.MainClass import MainClass
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as HNCK
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods as FrontAuthCheckMethods
from tests.front_office.registration.classes.class_registration_email import RegEmailCheckMethods as Reg
from tests.front_office.settings.classes.class_profile_settings import HelpProfileSettingsCheckMethods as HPSCM

__author__ = 'm.senchuk'


class HelpUsersData(MainClass):
    USER_FORM_TITLES = [
        'Имя',
        'Пол',
        'Роль в системе',
        'E-mail',
        'Город',
        'Телефон',
        'Пароль'
    ]

    CREATE_USER_ROLE = {
        "admin": {"name": "Администратор", "id": "3"},
        "moderator": {"name": "Модератор", "id": "4"},
        "seller": {"name": "Продавец", "id": "1,2,1"},
        "buyer": {"name": "Покупатель", "id": "1"},
    }

    MAPPING_ROLE = {
        "admin": "Администратор",
        "moderator": "Модератор",
        "seller": "Продавец",
        "buyer": "Покупатель",
        "Администратор": "Администратор",
        "Модератор": "Модератор",
        "Продавец": "Продавец",
        "Покупатель": "Покупатель",
        "want_seller": "Заявка на продавца",
        "trusted_seller": "Проверенный продавец"
    }

    MAPPING_ACCOUNT_STATUS = {
        "WAIT_FOR_REGISTRATION": "Ждет активации",
        "ENABLED": "Активный",
        "DISABLED": "Заблокирован"
    }

    MAPPING_ENABLED_STATUS = {
        "ENABLED": "Заблокировать",
        "DISABLED": "Разблокировать",
        "WAIT_FOR_REGISTRATION": "Заблокировать"
    }

    ROLES = {
        "admin": {"role_name": "Администратор", "query": "permission_id in (3, 7)"},
        "moderator": {"role_name": "Модератор", "query": "permission_id in (4, 8)"},
        #"seller": {"role_name": "Продавец", "query": "permission_id in (2, 6)"},
        #"buyer": {"role_name": "Покупатель", "query": "permission_id in (1, 5)"},
        "want_seller": {"role_name": "Заявка на продавца", "query": "wants_to_be_seller=True"}
    }


class HelpUsersMethods(HelpUsersData):
    @property
    def generate_test_data(self):
        CREATE_USER_DATA = {
            'name': 'Test_666_%s' % common_utils.random_string(params='letters', length=5),
            'gender': "MALE",
            'email': Reg.get_new_email(databases.db1).lower(),
            'city': u'Москва',
            'phone': str(random.randrange(70000000000, 70999999999, 1)),
            'passwd': '123',
        }
        return CREATE_USER_DATA

    @property
    def generate_test_data_edit(self):
        EDIT_USER_DATA = {
            'name': 'Test_%s' % common_utils.random_string(params='letters', length=10),
            'gender': "MALE",
            'passwd': str(random.randrange(10000, 99999, 1)),
        }
        return EDIT_USER_DATA

    @staticmethod
    def get_input_field_find(driver):
        """
        Получить строку поиска
        :param driver:
        :return:
        """
        return HNCK.get_element_navigate(driver, HNCK.input_back_users.FIELD_FIND)

    @staticmethod
    def get_select_role(driver, role=''):
        """
        Получить роль для поиска пользователя
        :param driver:
        :return:
        """
        return HNCK.get_element_navigate(driver, HNCK.click_back_users.SELECT_ROLE % role)

    @staticmethod
    def get_select_role_options(driver):
        """
        Получить список ролей для поиска пользователя
        :param driver:
        :return:
        """
        return driver.find_elements_by_xpath(HNCK.click_back_users.SELECT_ROLE % '').text.encode('utf-8')

    @staticmethod
    def get_select_param(driver, param=''):
        """
        Получить параметр для поиска пользователя
        :param driver:
        :return:
        """
        return HNCK.get_element_navigate(driver, HNCK.click_back_users.SELECT_PARAM % param)

    @staticmethod
    def get_select_param_options(driver):
        """
        Получить список параметров для поиска пользователя
        :param driver:
        :return:
        """
        return driver.find_elements_by_xpath(HNCK.click_back_users.SELECT_PARAM % '').text.encode('utf-8')

    @staticmethod
    def get_info_line(driver, user):
        """
        получение номера строки в которой находятся данные пользователя
        :param driver:
        :param user:
        :return:
        """
        lines = driver.find_elements_by_xpath(HNCK.check_back_users.LINES)
        count = list()
        for num, line in enumerate(lines):
            info = line.text.encode('utf-8')
            if info.count("ID: " + str(user["id"])) > 0:
                count.append(num+1)
        return count

    @staticmethod
    def get_day_active(driver, calendar):
        """
        Метод получает активный день из календаря
        :param driver:
        :return:
        """
        obj_day = HNCK.get_element_navigate(driver, calendar+HNCK.click_back_users.BTN_DAY_ACTIVE)
        day = obj_day.text.encode('utf-8')
        return obj_day, day

    @staticmethod
    def get_day_first_in_calendar(driver, calendar):
        """
        Метод получает первый день в календаре
        :param driver:
        :param calendar: какой испошльзуется календарь (дата от, дата до)
        :return:
        """
        obj_day = HNCK.get_element_navigate(driver, calendar+HNCK.click_back_users.BTN_DAY_FIRST_IN_CALENDAR)
        day = obj_day.text.encode('utf-8')
        return obj_day, day

    @staticmethod
    def get_info_user_by_line(driver, line):
        """
        получение информации из строки в которой находятся данные пользователя
        :param driver:
        :param user:
        :return:
        """
        return HNCK.get_element_navigate(driver, HNCK.check_back_users.LINE % line).text.encode('utf-8')

    @staticmethod
    def want_seller(user, test_role):
        """
        Получаем флаг заявка на роль продавца в бэк-офисе
        :param user:
        :return:
        """
        if user["wants_to_be_seller"] is True and test_role == "Покупатель":
            want_seller = "Заявка на продавца\n"
        else:
            want_seller = ''
        return want_seller

    @staticmethod
    def get_user_name(name):
        """
        получение имени из базы для бек-офиса
        :param name:
        :return:
        """
        if name is None or name == '':
            name = ''
        elif name[-1] == ' ':
            name = name[:-1]
            name += "\n"
        else:
            name += "\n"
        return name

    @staticmethod
    def get_info_user_by_db(user, user_account, test_role):
        """
        получение информации из базы и приведение ее к виду строки полученной из бек-офиса
        :param user:
        :param user_account:
        :param test_role:
        :return:
        """
        p = lambda x: '' if x is None else x
        if user["trusted_seller"] is True:
            user_role = HelpUsersData.MAPPING_ROLE["trusted_seller"]
        else:
            user_role = HelpUsersData.MAPPING_ROLE[test_role]
        date_create = time.strftime("%d.%m.%Y", time.localtime(long(str(user_account['registration_timestamp'])[:-3])))
        info_user_db = HelpUsersMethods.get_user_name(user["display_name"]) + "ID: " + str(user["id"]) + "\n+" + \
                       p(user["phone"]) + "\n" + \
                       user_role + "\n" + HelpUsersMethods.want_seller(user, test_role) + \
                       HelpUsersData.MAPPING_ACCOUNT_STATUS[user_account["account_status"]] + " " +\
                       date_create + "\nРедактировать\n" + \
                       HelpUsersData.MAPPING_ENABLED_STATUS[user_account["account_status"]]
        return info_user_db

    @staticmethod
    def get_users_by_role(role, criteria):
        """

        :param role:
        :return:
        """
        # get users from table accounts
        if role != 'want_seller':
            users_account = databases.db1.accounting.get_account_details_permissions_by_criteria(criteria)
        else:
            users_account = databases.db1.accounting.get_account_details_by_criteria(criteria)
        return users_account

    @staticmethod
    def get_role(driver, role):
        """
        Получить роль пользователя
        :param driver:
        :param role:
        :return:
        """
        return HNCK.get_element_navigate(driver, HNCK.input_back_users.FIELD_ROLE % role)

    @staticmethod
    def get_fields_user_create_form(driver):
        """
        Получить объекты полей для формы создания пользователя
        :param driver:
        :return:
        """
        fields = {
            'name': HNCK.get_element_navigate(driver, HNCK.input_back_users.FIELD_NAME),
            'gender': {
                "MALE": HNCK.get_element_navigate(driver, HNCK.input_back_users.RADIO_MAN),
                "FEMALE": HNCK.get_element_navigate(driver, HNCK.input_back_users.RADIO_WOMAN),
            },
            'role': HNCK.input_back_users.FIELD_ROLE,
            'email': HNCK.get_element_navigate(driver, HNCK.input_back_users.FIELD_EMAIL),
            'city': HNCK.get_element_navigate(driver, HNCK.input_back_users.FILED_CITY),
            'phone': HNCK.get_element_navigate(driver, HNCK.input_back_users.FIELD_PHONE),
            'passwd': HNCK.get_element_navigate(driver, HNCK.input_back_users.FIELD_PASS),
            'save': HNCK.get_element_navigate(driver, HNCK.click_back_users.BTN_SAVE)
        }
        return fields

    @staticmethod
    def get_fields_user_edit_form(driver):
        """
        Получить объекты полей для формы редактирования пользователя
        :param driver:
        :return:
        """
        fields = {
            'name': HNCK.get_element_navigate(driver, HNCK.input_back_users.FIELD_NAME),
            'gender': {
                "MALE": HNCK.get_element_navigate(driver, HNCK.input_back_users.RADIO_MAN),
                "FEMALE": HNCK.get_element_navigate(driver, HNCK.input_back_users.RADIO_WOMAN),
            },
            'role': HNCK.input_back_users.FIELD_ROLE,
            'email': HNCK.get_element_navigate(driver, HNCK.input_back_users.FIELD_EMAIL),
            'city': HNCK.get_element_navigate(driver, HNCK.input_back_users.FILED_CITY),
            'phone': HNCK.get_element_navigate(driver, HNCK.input_back_users.FIELD_PHONE),
            'passwd': HNCK.get_element_navigate(driver, HNCK.input_back_users.FIELD_PASS_EDIT),
            'save': HNCK.get_element_navigate(driver, HNCK.click_back_users.BTN_SAVE)
        }
        return fields

    @staticmethod
    def set_input_fields_user_create_form(fields, data):
        """
        Установить значения в input полях формы создания пользователя
        :param driver:
        :return:
        """
        fields['name'].send_keys(data['name'])
        fields['gender'][data['gender']].click()
        fields['email'].send_keys(data['email'])
        fields['city'].send_keys(data['city'])
        fields['phone'].send_keys(data['phone'])
        fields['passwd'].send_keys(data['passwd'])

    @staticmethod
    def set_input_fields_user_edit_form(fields, data):
        """
        Установить значения в input полях формы редактирования пользователя
        :param driver:
        :return:
        """
        fields['name'].send_keys(data['name'])
        fields['gender'][data['gender']].click()
        fields['passwd'].send_keys(data['passwd'])

    @staticmethod
    def change_status(driver, status, wait=50):
        """
        зменить статус пользхователя заблокировать/разблокировать
        :param driver:
        :param status:
        :return:
        """
        success = False
        service_log.put("User status is %s. Begin change status." % status)
        if status == 'ENABLED':
            HNCK.get_element_navigate(driver, HNCK.check_back_users.MODAL_BODY, mode=None)
            disabled = HNCK.get_element_navigate(driver, HNCK.check_back_users.MODAL_DISABLED_BTN, mode=None)
            cancel = HNCK.get_element_navigate(driver, HNCK.check_back_users.MODAL_CANCEL_BTN, mode=None)
            FrontAuthCheckMethods.click_button(disabled)
            do_time = time.time()
            while time.time() - do_time < wait:
                try:
                    driver.find_element_by_xpath(HNCK.check_back_users.DISABLED_SUCCESS)
                    success = True
                    break
                except Exception:
                    pass
            assert success is not False, "Не получено сообщение о успешном изменении статуса"
        service_log.put("User status is changed.")


class HelpUsersCheckMethods(HelpUsersMethods):
    def check_find_from_submit(self, driver):
        """
        Проверка блока поиска пользователя
        :param driver:
        :return:
        """
        self.get_select_role(driver)
        HNCK.get_element_navigate(driver, HNCK.click_back_users.DATE_FROM)
        HNCK.get_element_navigate(driver, HNCK.click_back_users.DATE_TO)
        self.get_input_field_find(driver)
        self.get_select_param(driver)
        HNCK.get_element_navigate(driver, HNCK.click_back_users.BTN_FIND)

    def check_user_in_db_query(self, user, users_account):
        """
        Проверка, что пользователь полученный из бек-офиса есть в выборке из БД по дате
        :param user:
        :param users_account:
        :return:
        """
        user_success_in_db = False
        for user_account in users_account:
            if user["id"] == user_account["account_details_id"]:
                user_success_in_db = True
        self.assertTrue(user_success_in_db, "Пользователь не найден по выборке из базы")

    def check_users(self, driver, pages, users_account, stop_test_pages=None):
        """
        Проверка всей информации в бек-офисе о пользователе построчно
        :param driver:
        :param pages:
        :param users_account:
        :return:
        """
        count_page = 0
        for page in range(pages):
            count_page += 1
            ids = driver.find_elements_by_xpath(HNCK.check_back_users.IDS)
            for id in ids:
                id = id.text.encode('utf-8')[4:]
                user = databases.db1.accounting.get_user_by_account_id(id)[0]
                self.check_user_in_db_query(user, users_account)
                user_account = databases.db1.accounting.get_user_account_info_by_id(user["id"])[0]
                count = self.get_info_line(driver, user)
                msg_count = "Найдено %s строк с упоминанием ID %s"
                self.assertEqual(len(count), 1, msg_count % (len(count), user["id"]))
                info_user_back = self.get_info_user_by_line(driver, count[0])
                user_roles = databases.db1.accounting.get_user_role_by_id(user_id=user["id"])
                info_user_db = self.get_info_user_by_db(user, user_account, HPSCM.get_user_role_ui(user_roles))
                msg_check = "Данные из бэк офиса: '%s' не совпали с данными и базы: '%s'"
                self.assertEqual(info_user_back, info_user_db, msg_check % (info_user_back, info_user_db))
            if stop_test_pages == count_page:
                break
            if pages > 1:
                next_pag = HNCK.get_element_navigate(driver, HNCK.click_back_users.PAG_NEXT)
                FrontAuthCheckMethods.click_button(next_pag)

    def check_form_create_user(self, driver):
        """
        Проверка формы Создание пользователя в бэк-офисе
        :param driver:
        :return:
        """
        for title in self.USER_FORM_TITLES:
            HNCK.get_element_navigate(driver, HNCK.check_back_users.NAME_FIELDS % title)

    def check_success_create(self, driver, user_id):
        """
        Проверка успешного создания пользователя
        :param driver:
        :return:
        """
        return HNCK.get_element_navigate(driver, HNCK.check_back_users.CREATED_USER_ID % user_id)

    def check_success_edit(self, driver):
        """

        :param driver:
        :return:
        """
        result = False
        do_time = time.time()
        while time.time() - do_time < 3:
            try:
                obj = HNCK.get_element_navigate(driver, HNCK.check_back_users.MSG_SUCCESS, mode=None, sleep=0.1)
                result = True
                service_log.put("Получено сообщение об успешном сохранении")
            except Exception:
                pass
        self.assertTrue(result, "Не получено сообщение 'Изменения сохранены'")