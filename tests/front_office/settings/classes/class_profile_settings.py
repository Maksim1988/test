# -*- coding: utf-8 -*-
import time
import random

import funky
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.utils.db import databases
from tests.front_office.registration.classes.class_registration_email import RegEmailCheckMethods as Reg
from support import service_log
from support.utils import common_utils
from support.utils.common_utils import generate_sha256
from tests.front_office.authorization.classes.class_front import HelpAuthMethods, HelpAuthCheckMethods
from tests.MainClass import MainClass
from tests.front_office.data_navigation import ProfileSettingsPage as PSP
from tests.front_office.data_navigation import ShopPage as SHP
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate
from tests.front_office.registration.classes.class_registration import HelpRegCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods

__author__ = 'm.senchuk'


class HelpProfileSettingsData(MainClass):
    GENDER_MAP = {
        "MALE": "Мужской",
        "FEMALE": "Женский"
    }
    ROLE_LIST_PRIORITY = {"BUYER_PERMISSION": 1,
                          "SELLER_PERMISSION": 2,
                          "MODERATOR_PERMISSION": 3,
                          "ADMIN_PERMISSION": 4,
                          "BUYERS": 1,
                          "SELLERS": 2,
                          "MODERATORS": 3,
                          "ADMINS": 4}

    # Тест-данные для позитивных кейсов блока "Общая информация" из таблицы сущности
    COMMON_INFO_ETALON_CASE = dict(display_name=u"Тестовый продавец %s" % str(random.randrange(10000000, 99999999, 1)),
                                   gender_user='man',
                                   email=Reg.get_new_email(databases.db1).lower(),
                                   shop_address=u"Линия %s, Павильон %s" % (str(random.randrange(100000000,
                                                                                                 999999999, 1)),
                                                                            str(random.randrange(100000000,
                                                                                                 999999999, 1)))
    )

    COMMON_INFO_REQUIRE_CASE = dict(display_name=u"Тестовый_продавец- %s"
                                                 % str(random.randrange(10000000, 99999999, 1)),
                                    gender_user='woman',
                                    email="",
                                    shop_address=u""
    )

    COMMON_INFO_MAX_CASE = dict(display_name=(u"Test Seller %s" % str(random.randrange(10000000, 99999999, 1))) * 10,
                                gender_user='man',
                                email=Reg.get_new_email(databases.db1).lower(),
                                shop_address=(u"Линия %s, Павильон %s" % (str(random.randrange(100000000,
                                                                                               999999999, 1)),
                                                                          str(random.randrange(100000000,
                                                                                               999999999, 1)))) * 5
    )

    COMMON_INFO_MIN_CASE = dict(display_name="%s" % str(random.randrange(1, 9, 1)),
                                gender_user='woman',
                                email=Reg.get_new_email(databases.db1).lower(),
                                shop_address="%s" % str(random.randrange(1, 9, 1)),
    )

    COMMON_INFO_TEST_SUITE = [COMMON_INFO_ETALON_CASE, COMMON_INFO_REQUIRE_CASE, COMMON_INFO_MAX_CASE,
                              COMMON_INFO_MIN_CASE]


    # Тест-данные для позитивных кейсов блока "Информация о магазине" из таблицы сущности
    SHOP_INFO_ETALON_CASE = dict(name=u"Тестовый магазин %s" % str(random.randrange(10000000, 99999999, 1)),
                                 description=u"Тестовое описание %s" % common_utils.random_string(length=100),
                                 address=u"Линия %s, Павильон %s" % (str(random.randrange(100000000, 999999999, 1)),
                                                                     str(random.randrange(100000000, 999999999, 1)))
    )

    SHOP_INFO_REQUIRE_CASE = dict(name=u"",
                                  description=u"",
                                  address=u""
    )

    SHOP_INFO_MAX_CASE = dict(name=u"Тестовый магазин %s" % common_utils.random_string(length=183),
                              description=u"Тестовое описание %s" % common_utils.random_string(length=182),
                              address=u"Линия 11, Павильон %s" % common_utils.random_string(length=181)
    )

    SHOP_INFO_MIN_CASE = dict(name=u"%s" % common_utils.random_string(length=1),
                              description=u"%s" % common_utils.random_string(length=1),
                              address=u"%s" % common_utils.random_string(length=1)
    )

    SHOP_INFO_TEST_SUITE = {"etalon": SHOP_INFO_ETALON_CASE,
                            "require": SHOP_INFO_REQUIRE_CASE,
                            "max": SHOP_INFO_MAX_CASE,
                            "min": SHOP_INFO_MIN_CASE}


    # Тест-данные для негативных кейсов блока "Общая информация" поля "Имя" из таблицы сущности
    COMMON_INFO_NEGATIVE_DISPLAY_NAME_TEST_SUITE = ["\\", "/", ":", "*", "?", '"', "<", ">", "|", "!", u"№", "@",
                                                    ";", "#", "$", "%", "^", "&", "(", ")", "+"]

    TEXT_ERROR_MESSAGE_DISPLAY_NAME = "Имя пользователя может содержать латинские буквы и буквы кириллицы, пробел, " \
                                      "дефис, подчеркивание, цифры и не должно быть более 200"

    COMMON_INFO_DISPLAY_NAME_NEGATIVE_SUITE = dict(data=COMMON_INFO_NEGATIVE_DISPLAY_NAME_TEST_SUITE,
                                                   msg=TEXT_ERROR_MESSAGE_DISPLAY_NAME)


    # Тест-данные для негативных кейсов блока "Общая информация" поля "Email" из таблицы сущности
    COMMON_INFO_NEGATIVE_EMAIL_TEST_SUITE = [u"русский@емайл.ру", "test.ivanov.ru", "test.ivanov"]

    TEXT_ERROR_MESSAGE_EMAIL = "Неверный email"

    COMMON_INFO_EMAIL_NEGATIVE_SUITE = dict(data=COMMON_INFO_NEGATIVE_EMAIL_TEST_SUITE,
                                            msg=TEXT_ERROR_MESSAGE_EMAIL)


    # Тест-данные для позитивных кейсов блока "О компании" из таблицы сущности.
    ABOUT_COMPANY_ETALON_CASE = dict(legal_name=u"Полное, наименование юр. лица %s"
                                                % str(random.randrange(10000000, 99999999, 1)),
                                     inn=str(random.randrange(10000000000, 99999999999, 1)),
                                     kpp=str(random.randrange(100000000, 999999999, 1)),
                                     ogrn=str(random.randrange(1000000000000, 9999999999999, 1)),
                                     legal_address=u"Юридический, адрес. %s"
                                                   % str(random.randrange(10000000, 99999999, 1)),
                                     actual_address=u"Фактический, адрес. %s" % str(random.randrange(10000000,
                                                                                                     99999999, 1))
    )

    ABOUT_COMPANY_MAX_CASE = dict(legal_name=u"Полное, наименование юр. лица %s"
                                             % ((str(random.randrange(10000000, 99999999, 1))) * 120),
                                  inn=str(random.randrange(100000000000, 999999999999, 1)),
                                  kpp=str(random.randrange(100000000, 999999999, 1)),
                                  ogrn=str(random.randrange(1000000000000, 9999999999999, 1)),
                                  legal_address=u"Юридический, адрес. %s"
                                                % ((str(random.randrange(10000000, 99999999, 1))) * 120),
                                  actual_address="%s" % str(random.randrange(1, 9, 1))
    )

    ABOUT_COMPANY_MIN_CASE = dict(legal_name="%s" % str(random.randrange(1, 9, 1)),
                                  inn=str(random.randrange(1000000000, 9999999999, 1)),
                                  kpp=str(random.randrange(100000000, 999999999, 1)),
                                  ogrn=str(random.randrange(1000000000000, 9999999999999, 1)),
                                  legal_address="%s" % str(random.randrange(1, 9, 1)),
                                  actual_address=u"Фактический, адрес. %s" % ((str(random.randrange(10000000,
                                                                                                    99999999,
                                                                                                    1))) * 120)
    )

    ABOUT_COMPANY_TEST_SUITE = [ABOUT_COMPANY_ETALON_CASE, ABOUT_COMPANY_MAX_CASE,
                                ABOUT_COMPANY_MIN_CASE]


    # Тест-данные для проверки негативных кейсов блока "О компании" в таблице сущностей - русские и английские буквы
    # для полей ИНН, КПП, ОГРН.
    ABOUT_COMPANY_NEGATIVE_LITTERS_SUITE = dict(inn=["english symbol", u"русские буквы", u"123456789A",
                                                     "\\", "/",
                                                     ":", "*", "?", '"', "<", ">", "|", "!", u"№", "@", ";", "#",
                                                     "$", "%",
                                                     "^", "&", "(", ")", "+"
    ],
                                                kpp=["english symbol", u"12345678A"],
                                                ogrn=["english symbol", u"русские буквы", u"123456789012A",
                                                      "\\", "/", ":", "*", "?", '"', "<", ">", "|", "!", u"№", "@",
                                                      ";", "#",
                                                      "$", "%", "^", "&", "(", ")", "+"
                                                ])
    ABOUT_COMPANY_ERR_MSG_LITTERS = "Поле должно содержать только цифры"


    # Тест-данные для проверки негативных кейсов блока "О компании" в таблице сущностей - нехватка цифр
    # для полей ИНН, КПП, ОГРН.
    ABOUT_COMPANY_NEGATIVE_NUMBER_SUITE = dict(inn=["123456789"],
                                               kpp=["12345678"],
                                               ogrn=["123456789012"])
    ABOUT_COMPANY_ERR_MSG_NUMBER = dict(inn="Поле должно содержать от 10 до 12 цифр",
                                        kpp="Поле должно содержать 9 цифр",
                                        ogrn="Поле должно содержать 13 цифр")


    # Тест-данные для проверки негативных кейсов блока "О компании" в таблице сущностей - английские буквы
    # для полей Полное наименование юр. лица, Юридический адрес, Фактический адрес.
    ABOUT_COMPANY_NEGATIVE_ENGLISH_SUITE = dict(legal_name=["English language name"],
                                                legal_address=["english symbol"],
                                                actual_address=["english symbol"])
    ABOUT_COMPANY_ERR_MSG_ENGLISH = "Поле не должно содержать буквы латинского алфавита"


    # Тест-данные для проверки кейса "Позитивный" блока "О компании" в таблице сущностей
    # для полей Полное наименование юр. лица, Юридический адрес
    ABOUT_COMPANY_POSITIVE_SYMBOL_SUITE = u"""\/:*?"<>|!№@;#$%^&()+]"""


    # Тест-данные для проверки кейса "Эталонный" блока "Банковские реквизиты" в таблице сущностей.
    BANK_INFO_ETALON_CASE = dict(bank_bic="%s" % str(random.randrange(100000000, 999999999, 1)),
                                 bank_name_and_address=u"Наименование, и местоположение. банка/ %s"
                                                       % str(random.randrange(1000000000, 9999999999, 1)),
                                 bank_account=(str(random.randrange(1000000000, 9999999999, 1))) * 2,
                                 bank_correspondent_account=(str(random.randrange(1000000000, 9999999999, 1))) * 2
    )


    # Тест-данные для проверки кейса "Позитивный" блока "Банковские реквизиты" в таблице сущностей - длинное занчение
    # в поле "Наименование и местоположение банка"
    BANK_INFO_POSITIVE_CASE = dict(bank_name_and_address=u"Наименование, и местоположение. банка/ %s"
                                                         % ((str(random.randrange(1000000000, 9999999999, 1))) * 20))


    # Тест-данные для проверки кейса "Негативный" блока "Банковские реквизиты" в таблице сущностей - английские буквы,
    # русские буквы, символы для полей БИК, Номер счета, Корреспондентский счет.
    BANK_INFO_NEGATIVE_LITTERS_SUITE = dict(bank_bic=["english", u"русские", u"1234567A",
                                                      "\\", "/",
                                                      ":", "*", "?", '"', "<", ">", "|", "!", u"№", "@", ";", "#",
                                                      "$", "%",
                                                      "^", "&", "(", ")", "+"
    ],
                                            bank_account=["english symbol", u"русские буквы", u"1234567890121416019A",
                                                          "\\", "/", ":", "*", "?", '"', "<", ">", "|", "!", u"№",
                                                          "@", ";", "#", "$", "%", "^", "&", "(", ")", "+"
                                            ],
                                            bank_correspondent_account=["english symbol", u"русские буквы",
                                                                        u"1234567890121416019A",
                                                                        "\\", "/", ":", "*", "?", '"', "<", ">", "|",
                                                                        "!", u"№", "@", ";", "#", "$", "%", "^", "&",
                                                                        "(", ")", "+"
                                            ])
    BANK_INFO_ERR_MSG_LITTERS = "Поле должно содержать только цифры"


    # Тест-данные для проверки негативных кейсов блока "Банковские реквизиты" в таблице сущностей - нехватка цифр
    # для полей БИК, Номер счета, Корреспондентский счет.
    BANK_INFO_NEGATIVE_NUMBER_SUITE = dict(bank_bic=["12345678"],
                                           bank_account=["1234567890121416019"],
                                           bank_correspondent_account=["1234567890121416019"])
    BANK_INFO_ERR_MSG_NUMBER = dict(bank_bic="Поле должно содержать 9 цифр",
                                    bank_account="Поле должно содержать 20 цифр",
                                    bank_correspondent_account="Поле должно содержать 20 цифр")


    # Тест-данные для проверки негативных кейсов блока "О компании" в таблице сущностей - английские буквы
    # для поля Наименование и местоположение банка.
    BANK_INFO_NEGATIVE_ENGLISH_SUITE = dict(bank_name_and_address=["English language name"])
    BANK_INFO_ERR_MSG_ENGLISH = "Поле не должно содержать буквы латинского алфавита"


    # Тест-данные для проверки кейсов "Эталонный", "Обязательный" и "Позитивный" для блока "Смена пароля"
    # в таблице сущностей
    PASSWD_CHANGE_ETALON_CASE = dict(passwd_old="54268",
                                     passwd_new="aZc5!r",
                                     passwd_new_repeat="aZc5!r")
    PASSWD_CHANGE_REQUIRE_CASE = dict(passwd_old="123",
                                      passwd_new="nbrHRTmnj54",
                                      passwd_new_repeat="nbrHRTmnj54")
    PASSWD_CHANGE_POSITIVE_1_CASE = dict(passwd_old="123",
                                         passwd_new="ABCDE1",
                                         passwd_new_repeat="ABCDE1")
    PASSWD_CHANGE_POSITIVE_2_CASE = dict(passwd_old="123",
                                         passwd_new="12345A",
                                         passwd_new_repeat="12345A")
    PASSWD_CHANGE_POSITIVE_3_CASE = dict(passwd_old="123",
                                         passwd_new=("12345ATRHRDTGSE75843" * 5),
                                         passwd_new_repeat=("12345ATRHRDTGSE75843" * 5))
    PASSWD_CHANGE_POSITIVE_SUITE = [PASSWD_CHANGE_ETALON_CASE, PASSWD_CHANGE_REQUIRE_CASE,
                                    PASSWD_CHANGE_POSITIVE_1_CASE, PASSWD_CHANGE_POSITIVE_2_CASE,
                                    PASSWD_CHANGE_POSITIVE_3_CASE]


    # Тест-данные для проверки кейсов "Негативный" в таблице сущностей - пустые поля.
    PASSWD_CHANGE_NEGATIVE_ALL_EMPTY_CASE = dict(passwd_old="Пароли не должны совпадать",
                                                 passwd_new="Введите новый пароль",
                                                 passwd_new_repeat="Подтвердите новый пароль")


    # Тест-данные для проверки кейсов "Негативный" в таблице сущностей - текущий пароль.
    PASSWD_CHANGE_NEGATIVE_PASSWD_OLD_CASE = dict(passwd_new="Qwerty1",
                                                  passwd_new_repeat="Qwerty1")
    PASSWD_CHANGE_NEGATIVE_OLD_CASE = dict(passwd_old="Введите текущий пароль")

    # Тест-данные для проверки кейсов "Негативный" для блока "Смена пароля" - подтвердите пароль
    # в таблице сущностей
    PASSWD_CHANGE_PASSWD_NEW_REPEAT_INVALID_CASE = dict(passwd_new="Qwerty1",
                                                        passwd_new_repeat="Qwerty!",
                                                        err_passwd_new_repeat="Пароли должны совпадать")
    PASSWD_CHANGE_PASSWD_NEW_REPEAT_INVALID_LOWER_CASE = dict(passwd_new="Qwerty1",
                                                              passwd_new_repeat="qwerty1",
                                                              err_passwd_new_repeat="Пароли должны совпадать")

    PASSWD_CHANGE_PASSWD_NEW_REPEAT_INVALID_SUITE = [PASSWD_CHANGE_PASSWD_NEW_REPEAT_INVALID_CASE,
                                                     PASSWD_CHANGE_PASSWD_NEW_REPEAT_INVALID_LOWER_CASE]


    # Тест-данные для проверки кейсов "Негативный" в таблице сущностей - подтвердите пароль пустой.
    PASSWD_CHANGE_PASSWD_NEW_REPEAT_EMPTY_CASE = dict(passwd_new="Qwerty1",
                                                      err_passwd_new_repeat="Подтвердите новый пароль")


    # Тест-данные для проверки кейсов "Негативный" в таблице сущностей - Новый пароль пустой.
    PASSWD_CHANGE_PASSWD_NEW_EMPTY_CASE = dict(passwd_new_repeat="Qwerty1",
                                               err_passwd_new="Введите новый пароль",
                                               err_passwd_new_repeat="Пароли должны совпадать")


    # Тест-данные для проверки кейсов "Негативный" в таблице сущностей - Новый пароль не соответствует требованиям.
    PASSWD_CHANGE_PASSWD_NEW_CASE = dict(passwd_new=["aZc5s", "azc5sr", "aZcdsr", u"фZc5sr"])
    ERR_PASSWD_CHANGE_PASSWD_NEW_CASE = "Пароль не соответствует требованиям"


    # Тест-данные для проверки кейсов "Негативный" в таблице сущностей - Новый пароль совпадает с текущим паролем.
    PASSWD_CHANGE_PASSWD_NEW_EQUAL_OLD = dict(passwd_old="Qwerty1", passwd_new="Qwerty1", passwd_new_repeat="Qwerty1")
    ERR_PASSWD_CHANGE_PASSWD_NEW_EQUAL_OLD = "Пароли не должны совпадать"

    # Имя слитно или имя с пробелом
    NAME_WITH = {'join': '', 'space': ' '}

    # По русским , английским и цифрам должен работать поиск
    SEARCH_SYMBOLS = {'rus_symbol': u'а', 'eng_symbol': 'a', 'number': '1'}


class HelpProfileSettingsMethods(HelpProfileSettingsData):
    @staticmethod
    def get_obj_input(driver, value, path_block, path_input):
        """ Получаем любое input поле кроме password. """
        p = Navigate.get_element_navigate(driver, path_block + path_input
                                          % (PSP.Input.LIST_VALUE_OR_NOT_VALUE[bool(value)] % value))
        p.is_displayed()
        p.is_enabled()
        return p

    @staticmethod
    def get_obj_input_passwd(driver, path_block, path_input):
        """ Получаем любое input поле типа password. """
        p = Navigate.get_element_navigate(driver, path_block + path_input)
        p.is_displayed()
        p.is_enabled()
        return p

    @staticmethod
    def unchecked_checkbox_address(driver, user_info):
        """ Получаем чек-бокс "Совпадает". Если чек-бокс нажат отжимаем """
        # TODO: Оптимизировать метод, избавиться от избыточных if
        checkbox = {}
        if (user_info["legal_address"] is not None) or (user_info["actual_address"] is not None):
            driver.find_element_by_xpath(PSP.Path.PATH_ABOUT_COMPANY +
                                         PSP.Check.STATUS_CHECKBOX_ADDRESS
                                         % (PSP.Check.LIST_CHECKBOX[bool(user_info["legal_address"] ==
                                                                         user_info["actual_address"])]))
            if user_info["legal_address"] == user_info["actual_address"]:
                checkbox['checked'] = driver.find_element_by_xpath(PSP.Path.PATH_ABOUT_COMPANY +
                                                                   PSP.Click.FORM_CHECKBOX_ADDRESS)
                checkbox['checked'].click()
            else:
                checkbox['unchecked'] = driver.find_element_by_xpath(PSP.Path.PATH_ABOUT_COMPANY +
                                                                     PSP.Click.FORM_CHECKBOX_ADDRESS)
        return checkbox

    @staticmethod
    def go_profile_settings_page(driver, env_base_url=MainClass.ENV_BASE_URL, sleep=2):
        """ Переход на страницу "Настройки пользователя". """
        # time.sleep(sleep)
        url = env_base_url + PSP.Path.PATH_PROFILE_SETTINGS
        service_log.put("Get page: %s" % url)
        do_get_work = time.time()
        driver.get(url)
        work_get_time = Navigate.work_time(do_get_work)
        service_log.put("Onload event time: [%s]" % work_get_time)
        Navigate.progress(driver)
        work_load_time = Navigate.work_time(do_get_work)
        service_log.put("Page received: %s" % url)
        service_log.put("Page received time: %s" % work_load_time)

    @staticmethod
    def get_submit_button(driver, path_block):
        """ Получаем кнопку Сохранить для блока path_block. """
        return Navigate.get_element_navigate(driver, path_block + PSP.Click.SAVE_BUTTON)

    @staticmethod
    def get_user_role_ui(roles):
        """ Меппинг ролей из базы к полю Роль в блоке Общая информация. """
        pr = HelpProfileSettingsData.ROLE_LIST_PRIORITY
        sp = [pr[role_x] for role_x in funky.pluck(roles, "name")]
        sp.sort()
        if sp[-1] == pr["ADMIN_PERMISSION"] or sp[-1] == pr["ADMINS"]:
            return "Администратор"
        if sp[-1] == pr["MODERATOR_PERMISSION"] or sp[-1] == pr["MODERATORS"]:
            return "Модератор"
        if sp[-1] == pr["BUYER_PERMISSION"] or sp[-1] == pr["BUYERS"]:
            return "Покупатель"
        if sp[-1] == pr["SELLER_PERMISSION"] or sp[-1] == pr["SELLERS"]:
            return "Продавец"

    @staticmethod
    def get_gender_user(driver, gender_db):
        """ Получаем поля Пол в блоке общая информация. """
        p = {}
        gender = {}
        if gender_db == "FEMALE":
            p['woman'] = PSP.Click.GENDER_CHECKED % 'Женский'
            p['man'] = PSP.Click.GENDER_UNCHECKED % 'Мужской'
        elif gender_db == "MALE":
            p['woman'] = PSP.Click.GENDER_UNCHECKED % 'Женский'
            p['man'] = PSP.Click.GENDER_CHECKED % 'Мужской'
        elif gender_db is None:
            p['woman'] = PSP.Click.GENDER_UNCHECKED % 'Женский'
            p['man'] = PSP.Click.GENDER_UNCHECKED % 'Мужской'

        gender['female'] = driver.find_element_by_xpath(PSP.Click.CLICK_GENDER % p["woman"])
        gender['male'] = driver.find_element_by_xpath(PSP.Click.CLICK_GENDER % p["man"])
        return gender

    @staticmethod
    def get_gender_user2(driver, gender_db):
        """ Получаем поля Пол в блоке общая информация. """
        p = {
            "FEMALE": {'woman': PSP.Click.GENDER_CHECKED % 'Женский',
                       'man': PSP.Click.GENDER_UNCHECKED % 'Мужской'},
            "MALE": {'woman': PSP.Click.GENDER_UNCHECKED % 'Женский',
                     'man': PSP.Click.GENDER_CHECKED % 'Мужской'},
            None: {'woman': PSP.Click.GENDER_UNCHECKED % 'Женский',
                   'man': PSP.Click.GENDER_UNCHECKED % 'Мужской'}
        }
        gender = dict(female=driver.find_element_by_xpath(PSP.Click.CLICK_GENDER % p[gender_db]["woman"]),
                      male=driver.find_element_by_xpath(PSP.Click.CLICK_GENDER % p[gender_db]["man"]))
        return gender

    @staticmethod
    def get_delete_avatar_button(driver):
        """ Получаем кнопку удалить аватар. """
        return driver.find_element_by_xpath(PSP.Click.DELETE_AVATAR_BUTTON)

    @staticmethod
    def clear_input_row(driver, element=None):
        """ Очистка строки от введенного значения """
        ActionChains(driver).key_down(Keys.CONTROL, element).send_keys('a').key_up(Keys.CONTROL).send_keys(
            Keys.DELETE).perform()

    @staticmethod
    def get_button_want_seller_role(driver, wants_to_be_seller):
        """
        Получаем кнопку "Заявка на роль продавца"
        :param driver:
        :param wants_to_be_seller:
        :return:
        """
        time.sleep(Navigate.time_sleep)
        return Navigate.get_element_navigate(driver, PSP.Path.PATH_COMMON_INFO +
                                             PSP.Click.LIST_WANT_ROLE_SELLER[wants_to_be_seller],
                                             sleep=10)

    @staticmethod
    def get_error_message_neg(driver, path_block, msg, sleep=1):
        try:
            obj_error = Navigate.get_element_navigate(driver, path_block + PSP.Check.FORM_ERROR_MESSAGE
                                                      % msg)
        except Exception:
            time.sleep(sleep)
            try:
                obj_error = Navigate.get_element_navigate(driver, path_block +
                                                          PSP.Check.FORM_ERROR_MESSAGE % msg)
            except Exception:
                raise AssertionError("ОШИБКА: Не появилось сообщение об ошибке.")
        return obj_error

    # TODO: Изменения для новых настроек профиля
    @staticmethod
    def get_menu_profile_seller(driver):
        """
        Получить меню настроек продавца
        :param driver:
        :return:
        """
        menu = {
            "title",
            "account_label",
            "profile_menu",
            "password_menu",
            "store_label",
            "info_menu",
            "details_menu",
        }
        return menu

    @staticmethod
    def get_menu_profile_buyer(driver):
        """
        Получить меню настроек покупателя
        :param driver:
        :return:
        """
        menu = {
            "title",
            "account_label",
            "profile_menu",
            "password_menu",
        }
        return menu

    @staticmethod
    def get_user_profile_form(driver, user):
        """
        Получить объекты страницы настроек - Профиль пользователя
        :param driver:
        :return:
        """
        p = lambda x: '' if x is None else " and @value='%s'" % x
        t = lambda x: '' if x is None else "='%s'" % x[1:]
        profile = {
            "title": Navigate.get_element_navigate(driver, Navigate.check_settings.TITLE_COMMON_INFO),
            "name_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_NAME),
            "name_input": Navigate.get_element_navigate(driver,
                                                        Navigate.input_settings.INPUT_NAME % p(user["display_name"])),
            "gender_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_GENDER),
            "phone_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_PHONE),
            "phone_input": Navigate.get_element_navigate(driver,
                                                         Navigate.input_settings.INPUT_PHONE % t(user["phone"])),
            "email_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_EMAIL),
            #"email_input": Navigate.get_element_navigate(driver, Navigate.input_settings.INPUT_EMAIL % p(user["email"])), # TODO: SELL-359
            "uid_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_USER_ID),
            "uid_text": Navigate.get_element_navigate(driver, Navigate.check_settings.TEXT_USER_ID),
            "save_btn": Navigate.get_element_navigate(driver, Navigate.click_settings.BTN_SAVE),
        }
        return profile

    @staticmethod
    def set_gender(obj_genders, gender_db):
        """
        Установить значение пола
        :param driver:
        :param obj_genders:
        :param gender_db:
        :return:
        """
        gender = None
        if gender_db is None:
            obj_genders["male"].click()
            gender = 'MALE'
        elif gender_db == 'MALE':
            obj_genders["female"].click()
            gender = 'FEMALE'
        elif gender_db == 'FEMALE':
            obj_genders["male"].click()
            gender = 'MALE'
        return gender

    @staticmethod
    def get_password_form(driver):
        """
        Получить объекты страницы настроек - сменить пароль
        :param driver:
        :return:
        """
        password = {
            "title": Navigate.get_element_navigate(driver, Navigate.check_settings.TITLE_CHANGE_PASSWORD),
            "password_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_PASSWORD),
            "password_input": Navigate.get_element_navigate(driver, Navigate.input_settings.INPUT_PASSWORD),
            "new_password_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_N_PASSWORD),
            "new_password_input": Navigate.get_element_navigate(driver, Navigate.input_settings.INPUT_N_PASSWORD),
            "repeat_password_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_R_PASSWORD),
            "repeat_password_input": Navigate.get_element_navigate(driver, Navigate.input_settings.INPUT_R_PASSWORD),
            "save_btn": Navigate.get_element_navigate(driver, Navigate.click_settings.BTN_SAVE),
        }
        return password

    @staticmethod
    def get_store_form(driver, user_id, shop):
        """
        Получить объекты страницы настроек - сменить пароль
        :param driver:
        :return:
        """
        p = lambda x: '' if x is None else " and @value='%s'" % x
        t = lambda x: '' if x is None else " and contains(.,'%s')" % x
        xpath_name_input = Navigate.input_settings.INPUT_STORE_NAME % p(shop["name"])
        xpath_address_input = Navigate.input_settings.INPUT_STORE_ADDRESS % p(shop["address"])
        xpath_description_input = Navigate.input_settings.INPUT_DESCRIPTION % t(shop["description"])
        store = {
            "title": Navigate.get_element_navigate(driver, Navigate.check_settings.TITLE_STORE_INFO),
            "store_url_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_STORE_URL % user_id),
            "name_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_STORE_NAME),
            "name_input": Navigate.get_element_navigate(driver, xpath_name_input),
            "address_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_STORE_ADDRESS),
            "address_input": Navigate.get_element_navigate(driver, xpath_address_input),
            "description_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_DESCRIPTION),
            "description_input": Navigate.get_element_navigate(driver, xpath_description_input),
            "save_btn": Navigate.get_element_navigate(driver, Navigate.click_settings.BTN_SAVE),
        }
        return store

    @staticmethod
    def get_details_form(driver, user):
        """
        Получить объекты страницы настроек - Реквизиты компании
        :param driver:
        :return:
        """
        p = lambda x: '' if x is None else " and @value='%s'" % x
        s = lambda x, y: ' and @checked' if x == y and x is not None else ' and not(@checked)'
        xpath_legal_name_input = Navigate.input_settings.INPUT_LEGAL_NAME % p(user["legal_name"])
        xpath_inn_input = Navigate.input_settings.INPUT_INN % p(user["inn"])
        xpath_kpp_input = Navigate.input_settings.INPUT_KPP % p(user["kpp"])
        xpath_ogrn_input = Navigate.input_settings.INPUT_OGRN % p(user["ogrn"])
        xpath_legal_address_input = Navigate.input_settings.INPUT_LEGAL_ADDRESS % p(user["legal_address"])
        xpath_real_address_input = Navigate.input_settings.INPUT_REAL_ADDRESS % p(user["actual_address"])
        xpath_bik_input = Navigate.input_settings.INPUT_BIK % p(user["bank_bic"])
        xpath_name_bank_input = Navigate.input_settings.INPUT_NAME_BANK % p(user["bank_name_and_address"])
        xpath_account_input = Navigate.input_settings.INPUT_ACCOUNT % p(user["bank_account"])
        xpath_correspondent_input = Navigate.input_settings.INPUT_CORRESPONDENT % p(user["bank_correspondent_account"])
        xpath_sovpadaet = Navigate.click_settings.CHECKBOX_SOVPADAET % s(user["legal_address"], user["actual_address"])
        details = {
            "title": Navigate.get_element_navigate(driver, Navigate.check_settings.TITLE_COMPANY_DETAILS),
            "about_company_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_ABOUT_COMPANY),
            "legal_name_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_LEGAL_NAME),
            "legal_name_input": Navigate.get_element_navigate(driver, xpath_legal_name_input),
            "inn_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_INN),
            "inn_input": Navigate.get_element_navigate(driver, xpath_inn_input),
            "kpp_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_KPP),
            "kpp_input": Navigate.get_element_navigate(driver, xpath_kpp_input),
            "ogrn_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_OGRN),
            "ogrn_input": Navigate.get_element_navigate(driver, xpath_ogrn_input),
            "legal_address_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_LEGAL_ADDRESS),
            "legal_address_input": Navigate.get_element_navigate(driver, xpath_legal_address_input),
            "real_address_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_REAL_ADDRESS),
            "real_address_input": Navigate.get_element_navigate(driver, xpath_real_address_input),
            "sovpadaet_label": Navigate.get_element_navigate(driver, xpath_sovpadaet),
            "bank_details_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_BANK_DETAILS),
            "bik_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_BIK),
            "bik_input": Navigate.get_element_navigate(driver, xpath_bik_input),
            "name_bank_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_BANK_NAME),
            "name_bank_input": Navigate.get_element_navigate(driver, xpath_name_bank_input),
            "account_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_BANK_ACCOUNT),
            "account_input": Navigate.get_element_navigate(driver, xpath_account_input),
            "correspondent_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_CORRESPONDENT),
            "correspondent_input": Navigate.get_element_navigate(driver, xpath_correspondent_input),
            "save_btn": Navigate.get_element_navigate(driver, Navigate.click_settings.BTN_SAVE),
        }
        return details

    @staticmethod
    def get_status_payment_options(payment_db):
        """
        Получить словарь настроек статусов для каждого варианта оплаты
        :param payment_db: данные из таблицы payment_info для конкретного пользователя
        :return: pay - словарь вариантов оплаты с указанием статуса варианта оплаты у пользователя
        (активен/неактивен) и текстовой информации если есть
        """
        service_log.put("Create dictionary with payment options and check-box statuses")
        pay = {
            "CARD": {"checked": False, "text": ''},
            "EMONEY": {"checked": False, "text": ''},
            "BANK_ACCOUNT": {"checked": False, "text": ''},
            "CASH_ON_DELIVERY": {"checked": False, "text": ''},
            "CASH": {"checked": False, "text": ''},
        }
        for p in payment_db:
            pay[p['type']]['checked'] = True
            pay[p['type']]['text'] = p['text']
        service_log.put("Dictionary created. Success! Look: %s" % pay)
        return pay

    @staticmethod
    def get_status_delivery_options(delivery_db):
        """
        Получить словарь настроек статусов для каждого варианта доставки
        :param delivery_db: данные из таблицы delivery_info для конкретного пользователя
        :return: delivery - словарь вариантов оплаты с указанием статуса варианта оплаты у пользователя
        (активен/неактивен) и текстовой информации если есть
        """
        service_log.put("Create dictionary with delivery options and check-box statuses")
        delivery = {
            "TRANSPORT_COMPANY": {"checked": False, "text": ''},
            "COURIER": {"checked": False, "text": ''},
            "OWN_DELIVERY_SERVICE": {"checked": False, "text": ''},
            "RUSSIAN_MAIL": {"checked": False, "text": ''},
            "PICKUP": {"checked": False, "text": ''},
        }
        for p in delivery_db:
            delivery[p['type']]['checked'] = True
            delivery[p['type']]['text'] = p['text']
        service_log.put("Dictionary created. Success! Look: %s" % delivery)
        return delivery

    @staticmethod
    def get_payment_form(driver, pay):
        """
        Получить объекты страницы настроек - Варианты оплаты
        :param driver:
        :param pay: словарь настроек статусов для каждого варианта оплаты, получать из метода get_status_payment_options
        :return: payment - словарь объектов формы Варианты оплаты
        """
        c = lambda x: ' and not(@checked)' if x is False else " and @checked"
        t = lambda x: ' and @disabled' if x['checked'] is False else " and not(@disabled) and contains(.,'%s')" \
                                                                     % x['text']
        xpath_cash_box = Navigate.click_settings.CHECKBOX_CASH % c(pay['CASH']['checked'])
        xpath_label_cash_on_delivery = Navigate.check_settings.LABEL_CASH_ON_DELIVERY
        xpath_cash_on_box = Navigate.click_settings.CHECKBOX_CASH_ON_DELIVERY % c(pay['CASH_ON_DELIVERY']['checked'])
        xpath_account_box = Navigate.click_settings.CHECKBOX_BANK_ACCOUNT % c(pay['BANK_ACCOUNT']['checked'])
        xpath_e_money_box = Navigate.click_settings.CHECKBOX_E_MONEY % c(pay['EMONEY']['checked'])
        xpath_card_box = Navigate.click_settings.CHECKBOX_CARD % c(pay['CARD']['checked'])
        xpath_e_money_input = Navigate.input_settings.INPUT_E_MONEY % t(pay['EMONEY'])
        xpath_pay_card_input = Navigate.input_settings.INPUT_PAY_CARD % t(pay['CARD'])
        service_log.put("Create dictionary objects in from Payment")
        payment = {
            "title": Navigate.get_element_navigate(driver, Navigate.check_settings.TITLE_PAYMENT),
            "info_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_PAYMENT_INFO),
            "cash_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_CASH),
            "cash_box": Navigate.get_element_navigate(driver, xpath_cash_box),
            "cash_on_delivery_label": Navigate.get_element_navigate(driver, xpath_label_cash_on_delivery),
            "cash_on_delivery_box": Navigate.get_element_navigate(driver, xpath_cash_on_box),
            "bank_account_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_PAY_BANK_ACCOUNT),
            "bank_account_box": Navigate.get_element_navigate(driver, xpath_account_box),
            "card_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_CARD),
            "card_box": Navigate.get_element_navigate(driver, xpath_card_box),
            "card_input": Navigate.get_element_navigate(driver, xpath_pay_card_input),
            "e_money_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_E_MONEY),
            "e_money_box": Navigate.get_element_navigate(driver, xpath_e_money_box),
            "e_money_input": Navigate.get_element_navigate(driver, xpath_e_money_input),
            "save_btn": Navigate.get_element_navigate(driver, Navigate.click_settings.BTN_SAVE),
        }
        service_log.put("Dictionary objects in from Payment created. Success!")
        return payment

    @staticmethod
    def get_delivery_form(driver, deliv):
        """
        Получить объекты страницы настроек - Варианты доставки
        :param driver:
        :param deliv: словарь настроек статусов для каждого варианта доставки, из метода get_status_delivery_options
        :return: delivery - словарь объектов формы Варианты доставки
        """
        c = lambda x: ' and not(@checked)' if x is False else " and @checked"
        t = lambda x: ' and @disabled' if x['checked'] is False else " and not(@disabled) and contains(.,'%s')" \
                                                                     % x['text']
        xpath_tk_box = Navigate.click_settings.CHECKBOX_TRANSPORT_COMPANY % c(deliv['TRANSPORT_COMPANY']['checked'])
        xpath_courier_box = Navigate.click_settings.CHECKBOX_COURIER % c(deliv['COURIER']['checked'])
        xpath_ods_box = Navigate.click_settings.CHECKBOX_OWN_DEL_SERVICE % c(deliv['OWN_DELIVERY_SERVICE']['checked'])
        xpath_mail_box = Navigate.click_settings.CHECKBOX_RUSSIAN_MAIL % c(deliv['RUSSIAN_MAIL']['checked'])
        xpath_pickup_box = Navigate.click_settings.CHECKBOX_PICKUP % c(deliv['PICKUP']['checked'])
        xpath_tk_input = Navigate.input_settings.INPUT_TK % t(deliv['TRANSPORT_COMPANY'])
        xpath_courier_input = Navigate.input_settings.INPUT_COURIER % t(deliv['COURIER'])
        xpath_pickup_input = Navigate.input_settings.INPUT_PICKUP % t(deliv['PICKUP'])
        service_log.put("Create dictionary objects in from Delivery")
        delivery = {
            "title": Navigate.get_element_navigate(driver, Navigate.check_settings.TITLE_DELIVERY),
            "info_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_DELIVERY_INFO),
            "tk_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_TK),
            "tk_box": Navigate.get_element_navigate(driver, xpath_tk_box),
            "tk_input": Navigate.get_element_navigate(driver, xpath_tk_input),
            "courier_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_COURIER),
            "courier_box": Navigate.get_element_navigate(driver, xpath_courier_box),
            "courier_input": Navigate.get_element_navigate(driver, xpath_courier_input),
            "ods_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_OWN_DEL_SERVICE),
            "ods_box": Navigate.get_element_navigate(driver, xpath_ods_box),
            "mail_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_MAIL),
            "mail_box": Navigate.get_element_navigate(driver, xpath_mail_box),
            "pickup_label": Navigate.get_element_navigate(driver, Navigate.check_settings.LABEL_PICKUP),
            "pickup_box": Navigate.get_element_navigate(driver, xpath_pickup_box),
            "pickup_input": Navigate.get_element_navigate(driver, xpath_pickup_input),
            "save_btn": Navigate.get_element_navigate(driver, Navigate.click_settings.BTN_SAVE),
        }
        service_log.put("Dictionary objects in from Delivery created. Success!")
        return delivery

    @staticmethod
    def change_all_payment_options(driver, pay_info, drop=True):
        """
        Выключить/ключить все варианты оплаты
        :param pay_info: получается в методе get_status_payment_options
        :param drop: если True выключает все чекбоксы, если False - включает все чекбоксы
        :return:
        """
        p = lambda x: "unchecked" if drop is True else "checked"
        service_log.put("Begin change payment options. New checkbox status is '%s' for all." % p(drop))
        c = lambda x: ' and not(@checked)' if x is False else " and @checked"
        xpath_pays = {
            "CASH": Navigate.click_settings.CHECKBOX_CASH % c(pay_info['CASH']['checked']),
            "EMONEY": Navigate.click_settings.CHECKBOX_E_MONEY % c(pay_info['EMONEY']['checked']),
            "BANK_ACCOUNT": Navigate.click_settings.CHECKBOX_BANK_ACCOUNT % c(pay_info['BANK_ACCOUNT']['checked']),
            "CASH_ON_DELIVERY": Navigate.click_settings.CHECKBOX_CASH_ON_DELIVERY % c(pay_info['CASH_ON_DELIVERY']['checked']),
            "CARD": Navigate.click_settings.CHECKBOX_CARD % c(pay_info['CARD']['checked']),
        }
        for pay in pay_info:
            service_log.put("[%s] - Checking payment option." % pay)
            if pay_info[pay]['checked'] is drop:
                service_log.put("[%s] - Need change checkbox status." % pay)
                pay_option = Navigate.get_element_navigate(driver, xpath_pays[pay])
                HelpAuthMethods.click_button(pay_option)
                service_log.put("[%s] - Checkbox status changed to '%s' success." % (pay, p(drop)))
            else:
                service_log.put("[%s] - Payment option already was '%s'." % (pay, p(drop)))
            service_log.put("[%s] - Success option checked!" % pay)
        service_log.put("Finish changing payment options. New checkbox status is '%s' for all." % p(drop))

    @staticmethod
    def change_all_delivery_options(driver, del_info, drop=True):
        """
        Выключить/ключить все варианты доставки
        :param pay_info: получается в методе get_status_delivery_options
        :param drop: если True выключает все чекбоксы, если False - включает все чекбоксы
        :return:
        """
        p = lambda x: "unchecked" if drop is True else "checked"
        service_log.put("Begin change delivery options. New checkbox status is '%s' for all." % p(drop))
        c = lambda x: ' and not(@checked)' if x is False else " and @checked"
        xpath_tk_box = Navigate.click_settings.CHECKBOX_TRANSPORT_COMPANY % c(del_info['TRANSPORT_COMPANY']['checked'])
        xpath_ods_box = Navigate.click_settings.CHECKBOX_OWN_DEL_SERVICE % c(del_info['OWN_DELIVERY_SERVICE']['checked'])
        xpath_pays = {
            "TRANSPORT_COMPANY": xpath_tk_box,
            "COURIER": Navigate.click_settings.CHECKBOX_COURIER % c(del_info['COURIER']['checked']),
            "OWN_DELIVERY_SERVICE": xpath_ods_box,
            "RUSSIAN_MAIL": Navigate.click_settings.CHECKBOX_RUSSIAN_MAIL % c(del_info['RUSSIAN_MAIL']['checked']),
            "PICKUP": Navigate.click_settings.CHECKBOX_PICKUP % c(del_info['PICKUP']['checked']),
        }
        for deliv in del_info:
            service_log.put("[%s] - Checking delivery option." % deliv)
            if del_info[deliv]['checked'] is drop:
                service_log.put("[%s] - Need change checkbox status." % deliv)
                pay_option = Navigate.get_element_navigate(driver, xpath_pays[deliv])
                HelpAuthMethods.click_button(pay_option)
                service_log.put("[%s] - Checkbox status changed to '%s' success." % (deliv, p(drop)))
            else:
                service_log.put("[%s] - Delivery option already was '%s'." % (deliv, p(drop)))
            service_log.put("[%s] - Success option checked!" % deliv)
        service_log.put("Finish changing delivery options. New checkbox status is '%s' for all." % p(drop))


class HelpProfileSettingsCheckMethods(HelpProfileSettingsMethods, HelpAuthMethods, Navigate):
    driver = None

    def registration(self, link_db):
        telephone = HelpRegCheckMethods.get_new_phone(link_db)
        # Переходим на страницу авторизации и далее на страницу регистрации
        HelpAuthMethods.go_registration_page(self.driver, type_xpath=2)
        HelpAuthMethods.click_to_phone(self.driver)
        obj_phone, obj_username, obj_submit_button = HelpRegCheckMethods.get_data_registration(self.driver)
        # Вводим имя пользователя, номер телефона и регистрируемся
        user_name = common_utils.random_string()
        obj_username.send_keys(user_name)
        obj_phone.send_keys(telephone[1:])
        Navigate.element_click(self.driver, obj_submit_button, change_page_url=False)
        time.sleep(3)
        # Находим пользователя по номеру телефона, проверемям что пароль, соль, телефон соответствуют требованиям
        info_user = link_db.accounting.get_data_user_by_phone(telephone)
        self.assertNotEqual(len(info_user), 0, "Не найдено пользователя по номеру телефона: '%s'" % telephone)
        info_user = info_user[0]  # телефон пользователя уникален, берём единственную запись, что бы не таскать список
        # генерируем новый пароль и подменяем на него
        default_new_passwd = AccountingMethods.get_default_password(4)
        hash_res_new = generate_sha256(default_new_passwd, info_user["salt"])
        link_db.accounting.update_user_password(info_user["id"], hash_res_new)
        link_db.accounting.update_user_salt(info_user["id"], info_user["salt"])
        # вводим пароль
        pass_input = Navigate.get_element_navigate(self.driver, Navigate.input_reg.P_INPUT_PASSWORD)
        pass_input.send_keys(default_new_passwd)
        # Нажимаем создать аккаунт
        submit_btn = Navigate.get_element_navigate(self.driver, Navigate.click_reg.BTN_REG)
        Navigate.element_click(self.driver, submit_btn)
        HelpAuthCheckMethods.check_profile_widget(self, self.driver)
        HelpAuthCheckMethods.check_menu_profile_widget_total(self, self.driver, user_name)
        return info_user

    def check_all_payment_options_in_good(self, driver, text_card, text_e_money):
        """
        Проверка вариантов оплаты на странице товара
        :return:
        """
        Navigate.get_element_navigate(driver, Navigate.check_good.BLOCK_PAYMENT_INFO)
        Navigate.get_element_navigate(driver, Navigate.check_good.LABEL_PAYMENT_INFO)
        Navigate.get_element_navigate(driver, Navigate.check_good.CASH)
        Navigate.get_element_navigate(driver, Navigate.check_good.CASH_ON_DELIVERY)
        Navigate.get_element_navigate(driver, Navigate.check_good.BANK_ACCOUNT)
        Navigate.get_element_navigate(driver, Navigate.check_good.CARD)
        Navigate.get_element_navigate(driver, Navigate.check_good.CARD_TEXT % text_card)
        Navigate.get_element_navigate(driver, Navigate.check_good.E_MONEY)
        Navigate.get_element_navigate(driver, Navigate.check_good.E_MONEY_TEXT % text_e_money)

    def check_all_delivery_options_in_good(self, driver, text_tk, text_courier, text_pickup):
        """
        Проверка вариантов доставки на странице товара
        :return:
        """
        Navigate.get_element_navigate(driver, Navigate.check_good.BLOCK_DELIVERY_INFO)
        Navigate.get_element_navigate(driver, Navigate.check_good.LABEL_DELIVERY_INFO)
        Navigate.get_element_navigate(driver, Navigate.check_good.TRANSPORT_COMPANY)
        Navigate.get_element_navigate(driver, Navigate.check_good.TRANSPORT_COMPANY_TEXT % text_tk)
        Navigate.get_element_navigate(driver, Navigate.check_good.COURIER)
        Navigate.get_element_navigate(driver, Navigate.check_good.COURIER_TEXT % text_courier)
        Navigate.get_element_navigate(driver, Navigate.check_good.OWN_DELIVERY_SERVICE)
        Navigate.get_element_navigate(driver, Navigate.check_good.RUSSIAN_MAIL)
        Navigate.get_element_navigate(driver, Navigate.check_good.PICKUP)
        Navigate.get_element_navigate(driver, Navigate.check_good.PICKUP_TEXT % text_pickup)

    def check_hold_submit_btn(self, driver, path):
        """
        Проверка, что кнопка Сохранить заблокирована на время сохранения
        :param driver:
        :return:
        """
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, path + PSP.Click.SAVE_BUTTON)))
        pass

    def check_profile_settings_page(self, driver):
        """ Проверка внешнего вида страницы "Настройки пользователя". """
        try:
            self.get_element_navigate(driver, PSP.Check.TITLE_PROFILE_SETTINGS)
        except NoSuchElementException:
            raise AssertionError("...ERROR: Element not find: %s." % PSP.Check.TITLE_PROFILE_SETTINGS)

    def check_shop_info(self, driver, shop_details):
        """ Проверка блока Информация о магазине. """
        self.get_element_navigate(driver, PSP.Path.PATH_SHOP_INFO + PSP.Check.TEXT_LIST % "Наименование компании:")
        self.get_obj_input(driver, shop_details["name"], PSP.Path.PATH_SHOP_INFO, PSP.Input.FORM_SHOP_NAME)
        driver.find_element_by_xpath(PSP.Path.PATH_SHOP_INFO + PSP.Check.TEXT_LIST % "Адрес магазина:")
        driver.find_element_by_xpath(PSP.Check.PREFIX_SHOP_ADDRESS)
        self.get_obj_input(driver, shop_details["address"], PSP.Path.PATH_SHOP_INFO, PSP.Input.FORM_SHOP_ADDRESS)
        self.get_element_navigate(driver, PSP.Path.PATH_SHOP_INFO + PSP.Check.TEXT_LIST % "Описание:")
        self.get_element_navigate(driver, PSP.Path.PATH_SHOP_INFO, PSP.Input.FORM_SHOP_DESCRIPTION %
                                  shop_details["description"])

    def check_avatar(self, driver, avatar_id):
        """ Проверка аватара. """
        if avatar_id is None:
            driver.find_element_by_xpath(PSP.Path.PATH_COMMON_INFO + PSP.Click.AVATAR_EMPTY_PATH)
            try:
                driver.find_element_by_xpath(PSP.Check.HELP_ADD_AVATAR_TEXT)
            except Exception:
                raise AssertionError("ОШИБКА: Не найдена подсказка под формой добавления аватара.")
        elif avatar_id is not None:
            driver.find_element_by_xpath(PSP.Path.PATH_COMMON_INFO + PSP.Check.AVATAR_PATH %
                                         (MainClass.ENV_STATIC_PATH, avatar_id))
            self.get_delete_avatar_button(driver)

    def check_success_save_message(self, driver, block, sleep=5):
        """ Проверка всплывающего сообщения об успешном изменении данных пользователя. """
        time.sleep(sleep)
        Navigate.get_element_navigate(driver,
                                      PSP.Check.FORM_SUCCESS_CHANGE % PSP.Check.LIST_SAVE_TEXT[block],
                                      sleep=10, mode=None)

    def check_error_save_message(self, driver, block, sleep=5):
        """ Проверка всплывающего сообщения об неуспешном изменении данных пользователя. """
        time.sleep(sleep)
        Navigate.get_element_navigate(driver,
                                      PSP.Check.FORM_ERROR_CHANGE % PSP.Check.LIST_SAVE_TEXT[block],
                                      mode=None)

    def check_error_massage(self, driver, path, msg):
        """ Проверка появления сообщения об ошибке. """
        tx = None
        try:
            driver.find_element_by_xpath(path + PSP.Check.FORM_ERROR_MESSAGE % msg)
        except Exception, tx:
            pass
        sys_msg = "ОШИБКА: Не появилось всплывающее сообщение об ошибке: '%s'" % msg
        self.assertIsNone(tx, sys_msg)

    def check_too_much_negative_case(self, driver, obj_input, list_test_data, path_block, msg, path_submit=None):
        """ Проверка множества однотипных негативнх кейсов с одинаковым сообщением об ошибке. """
        if path_submit is None:
            path_submit = path_block
        # Получаем объект кнопки Сохранить
        submit_button = self.get_submit_button(driver, path_submit)
        for test_data in list_test_data:
            # Очистка введенных данных из input форм
            self.clear_input_row(driver, obj_input)
            # Ввод тестовых данных
            obj_input.send_keys(test_data)
            service_log.put("Send test data: " + test_data)
            # Нажимаем Сохранить
            self.click_button(submit_button)
            service_log.put("Click button: %s" % str(submit_button))
            # Проверка, что появилось предупреждающее сообщение
            err_msg = self.get_error_message_neg(driver, path_block, msg)
            sys_msg = "ОШИБКА: Не появилось всплывающее сообщение об ошибке"
            self.assertIsNotNone(err_msg, sys_msg)
        # Очистка введенных данных из input форм
        self.clear_input_row(driver, obj_input)

    def check_checkbox_legal_actual_address(self):
        """ Проверка чек-бокса Юр. адрес совпадает с факт. адресом. """
        pass

    def check_common_info_all_roles(self, driver, user_info, user_roles):
        """ Проверка общей информации для всех ролей в блоке "Общая информация". """
        Navigate.get_element_navigate(driver, PSP.Check.TITLE_COMMON_INFO)
        name_rows = [
            'Имя',
            'Пол:',
            'Телефон:',
            'Эл. почта:',
            'ID пользователя:',
            # 'Роль в системе:'
        ]
        for name_row in name_rows:
            self.assertIsNotNone(
                driver.find_element_by_xpath(PSP.Path.PATH_COMMON_INFO + PSP.Check.TEXT_LIST % name_row))

        self.get_obj_input(driver, user_info["display_name"], PSP.Path.PATH_COMMON_INFO, PSP.Input.FORM_DISPLAY_NAME)
        self.get_gender_user(driver, user_info["gender"])
        driver.find_element_by_xpath(PSP.Path.PATH_COMMON_INFO + PSP.Check.FORM_PHONE_DISABLED
                                     % str(user_info["phone"][1:]))
        self.get_obj_input(driver, user_info["email"], PSP.Path.PATH_COMMON_INFO, PSP.Input.FORM_EMAIL)
        driver.find_element_by_xpath(PSP.Path.PATH_COMMON_INFO + PSP.Check.FORM_ID_USER % str(user_info["id"]))
        # driver.find_element_by_xpath(PSP.Path.PATH_COMMON_INFO+PSP.Check.FORM_ROLE_USER
        #                             % (self.get_user_role_ui(user_roles)))
        self.get_submit_button(driver, PSP.Path.PATH_COMMON_INFO)

    def check_about_company(self, driver, user_info):
        """ Проверка блока "О компании" (кроме чек-бокса Совпадает с юридическим). """
        Navigate.get_element_navigate(driver, PSP.Path.PATH_ABOUT_COMPANY +
                                      PSP.Check.TITLE_ABOUT_COMPANY)
        name_rows = ['Полное наименование юр',
                     'ИНН',
                     'КПП',
                     'ОГРН',
                     'Юридический адрес',
                     'Фактический адрес']

        for name_row in name_rows:
            self.assertIsNotNone(driver.find_element_by_xpath(PSP.Path.PATH_ABOUT_COMPANY + PSP.Check.TEXT_LIST
                                                              % name_row))

        self.get_obj_input(driver, user_info["legal_name"], PSP.Path.PATH_ABOUT_COMPANY, PSP.Input.FORM_FULL_LEGAL_NAME)
        self.get_obj_input(driver, user_info["inn"], PSP.Path.PATH_ABOUT_COMPANY, PSP.Input.FORM_INN)
        self.get_obj_input(driver, user_info["kpp"], PSP.Path.PATH_ABOUT_COMPANY, PSP.Input.FORM_KPP)
        self.get_obj_input(driver, user_info["ogrn"], PSP.Path.PATH_ABOUT_COMPANY, PSP.Input.FORM_OGRN)
        self.get_obj_input(driver, user_info["legal_address"], PSP.Path.PATH_ABOUT_COMPANY,
                           PSP.Input.FORM_LEGAL_ADDRESS)
        self.get_obj_input(driver, user_info["actual_address"], PSP.Path.PATH_ABOUT_COMPANY,
                           PSP.Input.FORM_ACTUAL_ADDRESS)
        self.get_submit_button(driver, PSP.Path.PATH_ABOUT_COMPANY)

    def check_bank_info(self, driver, user_info):
        """ Проверка блока "Банковские реквизиты". """
        Navigate.get_element_navigate(driver, PSP.Path.PATH_BANKING_INFO + PSP.Check.TITLE_BANKING_INFO)
        name_rows = ['БИК',
                     'Наименование и местоположение банка',
                     'Номер счета',
                     'Корреспондентский счет']

        for name_row in name_rows:
            self.assertIsNotNone(driver.find_element_by_xpath(PSP.Path.PATH_BANKING_INFO + PSP.Check.TEXT_LIST
                                                              % name_row))

        self.get_obj_input(driver, user_info["bank_bic"], PSP.Path.PATH_BANKING_INFO, PSP.Input.FORM_BANK_BIC)
        self.get_obj_input(driver, user_info["bank_name_and_address"], PSP.Path.PATH_BANKING_INFO,
                           PSP.Input.FORM_BANK_NAME_AND_ADDRESS)
        self.get_obj_input(driver, user_info["bank_account"], PSP.Path.PATH_BANKING_INFO, PSP.Input.FORM_BANK_ACCOUNT)
        self.get_obj_input(driver, user_info["bank_correspondent_account"], PSP.Path.PATH_BANKING_INFO,
                           PSP.Input.FORM_BANK_CORR_ACCOUNT)
        self.get_submit_button(driver, PSP.Path.PATH_ABOUT_COMPANY)

    def check_passwd_change(self, driver):
        """ Проверка блока "Изменить пароль". """
        Navigate.get_element_navigate(driver, PSP.Path.PATH_PASSWD_CHANGE +
                                      PSP.Check.TITLE_PASSWD_CHANGE)
        Navigate.get_element_navigate(driver, PSP.Path.PATH_PASSWD_CHANGE +
                                      PSP.Check.FORM_HELP_PASSWD_CHANGE)
        name_rows = ['Текущий пароль',
                     'Новый пароль',
                     'Повторите пароль']

        for name_row in name_rows:
            self.assertIsNotNone(driver.find_element_by_xpath(PSP.Path.PATH_PASSWD_CHANGE + PSP.Check.TEXT_LIST
                                                              % name_row))

        driver.find_element_by_xpath(PSP.Path.PATH_PASSWD_CHANGE + PSP.Input.FORM_PASSWD_OLD)
        driver.find_element_by_xpath(PSP.Path.PATH_PASSWD_CHANGE + PSP.Input.FORM_PASSWD_NEW)
        driver.find_element_by_xpath(PSP.Path.PATH_PASSWD_CHANGE + PSP.Input.FORM_PASSWD_NEW_REPEAT)
        self.get_submit_button(driver, PSP.Path.PATH_PASSWD_CHANGE)

    def check_address_your_page_seller(self, driver, user_id):
        self.assertIsNotNone(driver.find_element_by_xpath(PSP.Check.ADDRESS_YOUR_PAGE))
        link = driver.find_element_by_xpath(PSP.Click.URL_YOUR_PAGE % (user_id, user_id))
        link.click()
        self.assertIsNotNone(driver.find_element_by_xpath(SHP.Check.NOTIFY_MY_SHOP))

    def check_address_your_page_buyer(self, driver, user_id):
        tx = None
        try:
            driver.find_element_by_xpath(PSP.Check.ADDRESS_YOUR_PAGE)
            driver.find_element_by_xpath(PSP.Click.URL_YOUR_PAGE % (user_id, user_id))
        except Exception, tx:
            service_log.put("Success! Address line for buyer not found.")
        self.assertIsNotNone(tx)