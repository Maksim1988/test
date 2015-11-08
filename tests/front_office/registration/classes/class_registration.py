# -*- coding: utf-8 -*-
import random
import time
import datetime

from support import service_log
from support.utils import common_utils
from support.utils.db import databases
from tests.MainClass import MainClass
from tests.front_office.data_navigation import HelpPage
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods as Front

__author__ = 's.trubachev'


class HelpRegData(MainClass):
    check_help = HelpPage.Check

    # количество запусков получения пароля
    COUNT_RECOVER_PASSWD = {"single": 0, "double": 1, "triple": 2}
    POSITIVE_REG_NAMES = {"minus": "-", "underscore": "_"}
    NEGATIVE_REG_NAMES = {"space": " ", "figure": "{", "lesser": "<", "dollar": "$", "tags": "/>", "and": "&"}
    NEGATIVE_REG_PHONE = {"phone_less": str(random.randrange(100000000, 999999999, 1)),
                          "cyrillic": u'абв', "latin": u'abc', "spec_symbol": '%'}

    NAME_PASS = "//input[@name='pass']"
    #SUBMIT_OK = "//button[@type='submit' and text()='OK']"
    PASSWD_CONFIRM = "//span[text()='Пароль подтвержден']"

    REG_FIELD_PHONE = "//input[@name='phone' and @disabled]"
    REG_FIELD_USERNAME = "//input[@name='username' and @disabled]"
    REG_FIELD_PASSWD = "//input[@name='pass' and @disabled]"
    REG_BUTTON_DISABLE = "//button[@type='submit' and @disabled]"
    REG_BUTTON_OK = "//button[@type='submit' and not(@disabled)]"

    RADIOBUTTON_SELLER_BUYER_NOT_FOCUS = "//span[@class='radio-set__area']/input[@name='typeUser' and not(@checked)]"
    REG_RADIO_SET_BUYER = "//label[@class='radio-set__button']/span[text()='Покупать']"
    REG_RADIO_SET_SELLER = "//label[@class='radio-set__button']/span[text()='Продавать']"

    BY_CLICK_CREATE_ACCOUNT = "//p/span[contains(.,'Нажимая кнопку \"Зарегистрироваться\", вы подтверждаете свое " \
                              "согласие с условиями предоставления услуг (Пользовательское соглашение)')]"
    CONFIRMATION_AGREEMENT = "//fieldset[@class='form__fieldset']/div[5]//p/span[text()]"
    REG_LICENSE_OPTION = "//a[@href='/rules' and text()='Условиями УУРРАА']"
    FORM_NOTE_PASSWORD = "//div[@class='form__row form__row_note']/div[@class='form__help clearfix']/span[2]"

    NAME_PHONE = "//input[@name='phone']"
    NAME_USERNAME = "//input[@name='username' and @maxlength='200']"
    BUTTON_SUBMIT = "//button[@type='submit']"

    REG_NOT_SENT_PASSWD = "//span[contains(.,'Не приходит пароль?')]"
    REG_REPEAT_PASSWD = "//span[contains(.,'Отправить пароль повторно')]"
    REG_OK_SENT_PASSWD = "//span[contains(.,'Пароль отправлен')]"
    REG_LIST_REPEAT = [REG_NOT_SENT_PASSWD, REG_REPEAT_PASSWD]
    LIST_CHECK_REPEAT_PASSWD = {REG_NOT_SENT_PASSWD: REG_REPEAT_PASSWD, REG_REPEAT_PASSWD: REG_OK_SENT_PASSWD}

    REG_HELP_PAGE = "//a[@href='/help-1']/span[contains(.,'Помощь')]"


    PASSWORD_SEND = "//span[text()='Пароль отправлен на указанный номер.']"
    MSG_NOT_RIGHT_PASSWD = 'Неверный пароль'
    MSG_ERROR_FORM = "//span[@class='form__error' and contains(.,'%s')]"
    NOT_RIGHT_PASSWD = MSG_ERROR_FORM % MSG_NOT_RIGHT_PASSWD

    TEXT_NEED_NAME = "Введите имя"
    GO_TO_AUTHORIZATION_PAGE = "//a[@href='/login' and contains(.,'Вход')]"
    FORM_PHONE_CODE = "//span[@class='form__phone-code']"

    LIST_REG_PAGE1 = [#"//header[@class='header']",               # проверка хедера
                      "//a[@class='header__logo header__cell']",  # проверка логотипа
                      # проверка "Создайте свой аккаунт на уурраа"
                      #"//h1[@class='title__name' and contains(.,'Создайте свой аккаунт на УУРРАА')]",
                      "//div[@class='registration']",      # проверка формы авторизации
                      "//input[@name='phone' and @placeholder='(800) 000-00-00']",
                      # проверка формы Мобильные телефон
                      "//span[@class='form__text' and contains(.,'Мобильный телефон:')]",
                      "//span[contains(.,'Ваше имя:')]",          # проверка формы Имя пользователя
                      #"//div[@class='sidebar__reg']",
                      #"//h2/span[contains(.,'Уже есть аккаунтна УУРРАА?')]",  # проверка загловка 'Уже есть аккаунт на УУРРАА?'
                      #"//div[@class='sidebar__reg-cover']",    # проверка блока Уже есть аккаунт на УУРРАА?'
                      "//a[@href='/login' and contains(.,'Вход')]",          # проверка кнопки Авторизация
                      #"//a[@href='/help-1']/span[contains(.,'Помощь')]",                                # кнопка Помощь
                      "//footer[@class='footer']",                               # проверка подвала
                      "//input[@name='phone']",
                      "//input[@name='username' and @maxlength='200']",
                      "//button[@type='submit']/span[contains(.,'Выслать пароль')]",  # проверка кнопки Выслать пароль
                      ]
    LIST_REG_PAGE2 = ["//input[@class='search__input']",  # проверка отсутствия поиска
                      "//ul[@class='cat__list']",         # проверка отсутствия 6 рутовых категорий
                      "//nav[@class='cat']",              # проверка отсутствия Каталог товаров
                      ]

    CHECK_MSG = "//fieldset[@class='form__fieldset']/div[3]/label/span[1]"
    TEXT_USER_EXIST_MSG = 'Пользователь с указанными данными уже зарегистрирован'
    USER_EXIST_MSG = MSG_ERROR_FORM % TEXT_USER_EXIST_MSG
    HOW_GET_PROMO_CODE = "//span[text()='Как получить пригласительный код?']"
    BUTTON_SUBMIT_DISABLED = "//button[@type='submit' and @disabled]"
    RULES_HREF = "//div[@class='form__note']/p//a[@href='/rules']"
    CLICKING_CREATE_ACCOUNT = "//fieldset[@class='form__fieldset']//p/span[contains(.,'Нажимая создать аккаунт" \
                              ",я соглашаюсь с Условиями УУРРАА')]"
    REG_INSTRUCTION = "//div[@class='form_manual']/div[@class='form_manual' and contains(.,'1. Зарегистрируйтесь как покупатель.2. Зайдите в настройки.3. Рядом с указанной ролью нажмите \"Хочу зарегистрироваться как продавец\".4. Результат рассмотрения заявки будет отправлен Вам сообщением в \"Личный кабинет\".')]"
    NAME_PROMO = "//input[@name='promo']"
    TEXT_ERROR_ACTIVATION_PROMO_CODE = 'Ошибка активации пригласительного кода'
    TEXT_EXPIRED_PROMO_CODE = 'Указанный пригласительный код просрочен'
    TEXT_REVOKED_PROMO_CODE = 'Указанный пригласительный код недействителен'
    TEXT_NOT_CORRECT_PROMO_CODE = 'Указан неверный пригласительный код'


class HelpRegMethods(HelpRegData):

    @staticmethod
    def get_authorization_page(driver):
        """ Взять ссылку для перехода со страницы регистрации на авторизацию.
        :param driver: ссфлка на драйвер
        """
        return Navigate.element_is_present(driver, HelpRegData.GO_TO_AUTHORIZATION_PAGE)

    @staticmethod
    def get_new_phone(db_link):
        """
        Получить новый номер телефона, которого нет в БД
        :return: Номер телефона, пример: 71112223344
        """
        f = True
        phone = None
        input_phone = str(random.randrange(1000000000, 6999999999, 1))
        while f is True:
            phone = '7' + input_phone
            u = db_link.accounting.get_user_by_criteria_only("phone='%s'" % phone)
            if len(u) == 0:
                f = False
            else:
                input_phone = str(random.randrange(1000000000, 6999999999, 1))
        return phone

    @staticmethod
    def get_user_name(name_validate):
        """ Вернуть имя пользователя.
        :param name_validate: тип валидации имени пользователя.
        :return: имя пользователя
        """
        if name_validate == 'VALID':
            return u"Test -User_ %s" % random.randrange(1, 10000000, 1)
        elif name_validate == 'MAX':
            return 'Test' * 50
        elif name_validate == 'MIN':
            return 'A'

    @staticmethod
    def get_data_registration(driver):
        """ Получить данные со стрины регистрации.
        :param driver: ссылка на драйвер
        :return: телефон, имя пользователя, кнопка "зарегистрироваться"
        """
        phone = driver.find_element_by_xpath(HelpRegData.NAME_PHONE)
        username = driver.find_element_by_xpath(HelpRegData.NAME_USERNAME)
        submit_button = driver.find_element_by_xpath(HelpRegData.BUTTON_SUBMIT)
        return phone, username, submit_button

    @staticmethod
    def get_name_pass(driver):
        driver.find_element_by_xpath(HelpRegData.NAME_PASS)
        driver.find_element_by_xpath(HelpRegData.NAME_PASS).is_enabled()
        driver.find_element_by_xpath(HelpRegData.NAME_PASS).is_displayed()
        return driver.find_element_by_xpath(HelpRegData.NAME_PASS)

    @staticmethod
    def get_submit_ok(driver):
        """ Вернуть объект для нажатия "ОК".
        :param driver: ссылка на драйвер
        :return: ссылка на элемент
        """
        return driver.find_element_by_xpath(HelpRegData.BUTTON_SUBMIT)

    @staticmethod
    def get_radio_set_byuer(driver):
        """ Получить элемент кнопки продавца.
        :param driver: ссылка на драйвер
        :return: ссылка на элемент
        """
        return driver.find_element_by_xpath(HelpRegData.REG_RADIO_SET_BUYER)

    @staticmethod
    def get_radio_set_seller(driver):
        """ Получить элемент кнопки покуппателя.
        :param driver: ссылка на драйвер
        :return: ссылка на элемент
        """
        return driver.find_element_by_xpath(HelpRegData.REG_RADIO_SET_SELLER)

    @staticmethod
    def get_form_note_passwd(driver, sleep=5):
        """
        Получаем форму "Пароль выслан на указанный вами номер."
        :param driver:
        :param sleep:
        :return:
        """
        try:
            note_passwd = driver.find_element_by_xpath(HelpRegData.FORM_NOTE_PASSWORD)
        except Exception:
            time.sleep(sleep)
            try:
                note_passwd = driver.find_element_by_xpath(HelpRegData.FORM_NOTE_PASSWORD)
            except Exception:
                raise AssertionError("ОШИБКА: Форма 'Пароль выслан на указанный номер' не появилась.")
        return note_passwd

    @staticmethod
    def get_reg_submit_not_disable(driver):
        """ Вернуть кнопку.
        :param driver: ссылка на драйвер
        """
        return driver.find_element_by_xpath(HelpRegData.REG_BUTTON_OK)

    @staticmethod
    def get_xpath_repeat_passwd(count_recover):
        """ Выражение генератор для получение xpath смены пароля
        :param count_recover: количество восстановлений
        :return: xpath-элемента
        """
        return (HelpRegData.REG_LIST_REPEAT[index] for index in range(count_recover))

    @staticmethod
    def get_check_repeat_passwd(driver, key_xpath, sleep=2):
        """ Проверка после отправки пароля.
        :param count_recover: количество восстановлений
        :return: xpath-элемента
        """
        #time.sleep(sleep)
        return driver.find_element_by_xpath(HelpRegData.LIST_CHECK_REPEAT_PASSWD[key_xpath])

    @staticmethod
    def get_not_right_passwd(driver):
        """ Вернуть сообщение об ошибке.
        :param driver: ссылка на драйвер
        :return: сообщение об ошибке.
        """
        return driver.find_element_by_xpath(HelpRegData.NOT_RIGHT_PASSWD).text


    @staticmethod
    def click_repeat_send_passwd(driver, xpath_passwd, sleep=30):
        """ Кликнуть - Не приходит пароль.
        :param driver: ссылка на драйвер
        """
        not_sent_password = driver.find_element_by_xpath(xpath_passwd)
        not_sent_password.click()
        time.sleep(sleep)

    @staticmethod
    def password_send(driver):
        """ Пароль отправлен на указанный номер.
        """
        return Navigate.get_element_navigate(driver, HelpRegData.PASSWORD_SEND, mode=None)

    @staticmethod
    def get_check_msg(driver):
        # TODO
        return Navigate.get_element_navigate(driver, HelpRegData.CHECK_MSG, mode=None).text

    @staticmethod
    def get_msg_user_exist(driver):
        """ Возвращаем текст о существовании пользователя.
        :param driver: ссылка на драйвер
        :return: текст о существовании пользователя
        """
        return Navigate.get_element_navigate(driver, HelpRegData.USER_EXIST_MSG, mode=None).text

    @staticmethod
    def get_how_get_promo_code(driver):
        """ Ссылка на элемент "как получить промокод"
        :param driver: ссылка на драйвер
        :return: элемент получения промокода
        """
        service_log.put("Get element for get promo code ")
        return driver.find_element_by_xpath(HelpRegData.HOW_GET_PROMO_CODE)

    @staticmethod
    def get_instruction(driver):
        """ Получить инструкции по регистрации продавца.
        :param driver: ссылка на драйвер
        :return: инструкции
        """
        return driver.find_element_by_xpath(HelpRegData.REG_INSTRUCTION)

    @staticmethod
    def get_name_promo(driver):
        name_promo = driver.find_element_by_xpath(HelpRegData.NAME_PROMO)
        name_promo.is_displayed()
        name_promo.is_enabled()
        return name_promo

    @staticmethod
    def get_promo_code_by_status(status_promo_code):
        """ Метод, которывй инсертит в таблицу promo_code запись с промо кодом,
        в зависимости от параметра statusPromoCode (ACTIVATED, WAITING)
        :param status_promo_code: статус промо-кода, WAITING-неиспользованный, ACTIVATED-использованный
        :return: newPromo - возвращает промо-код
        """
        result_count = databases.db1.accounting.select_next_val()[0]
        new_id = int(result_count["nextval"])
        new_promo = str(random.randrange(10000, 99999, 1))

        if status_promo_code == 'ACTIVATED':
            databases.db1.accounting.insert_promo_code(new_id=new_id, status=status_promo_code, promo=new_promo)
            return new_promo
        elif status_promo_code == 'EXPIRED':
            databases.db1.accounting.insert_promo_code(new_id=new_id, status=status_promo_code, promo=new_promo)
            return new_promo
        elif status_promo_code == 'WAITING_BUT_ONETIME_ACTIVE':
            status_promo_code = 'WAITING'
            databases.db1.accounting.insert_promo_code(new_id=new_id, status=status_promo_code, promo=new_promo,
                                                       registration_count=1)
            return new_promo
        elif status_promo_code == 'WAITING':
            databases.db1.accounting.insert_promo_code(new_id=new_id, status=status_promo_code, promo=new_promo)
            return new_promo
        elif status_promo_code == 'REVOKED':
            databases.db1.accounting.insert_promo_code(new_id, status_promo_code, promo=new_promo)
            return new_promo
        elif status_promo_code == 'ENDS_TODAY':
            t = time.strptime(datetime.date.today().strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S')
            current_date = int(str(int(time.mktime(t)))+'000')
            current_date_to = str(current_date + 86399000)
            status_promo_code = 'WAITING'
            databases.db1.accounting.insert_promo_code(new_id=new_id, status=status_promo_code,
                                                       valid_to_timestamp=current_date_to, promo=new_promo)
            return new_promo
        elif status_promo_code == 'START_TODAY':
            t = time.strptime(datetime.date.today().strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S')
            current_date = int(str(int(time.mktime(t)))+'000')
            current_date_from = str(current_date)
            status_promo_code = 'WAITING'
            databases.db1.accounting.insert_promo_code(new_id=new_id, status=status_promo_code,
                                                       valid_from_timestamp=current_date_from, promo=new_promo)
            return new_promo
        elif status_promo_code == 'START_TOMORROW':
            t = time.strptime(datetime.date.today().strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S')
            current_date = int(str(int(time.mktime(t)))+'000')
            current_date_from = str(current_date + 86400000)
            status_promo_code = 'WAITING'
            databases.db1.accounting.insert_promo_code(new_id=new_id, valid_from_timestamp=current_date_from,
                                                       status=status_promo_code, promo=new_promo)
            return new_promo
        elif status_promo_code == 'INVALID':
            return 'invalid_' + new_promo


class HelpRegCheckMethods(HelpRegMethods):

    def check_need_name(self, driver):
        """ Проверка окна ошибки "введите пароль".
        :param driver: ссылка на драйвер
        """
        msg = "Не вывелось сообщение об ошибке 'Вы ввели неверный пароль. Пожалуйста попробуйте еще раз.'"
        self.assertIsNotNone(Navigate.element_is_present(driver, Front.ERROR_AUTH % self.TEXT_NEED_NAME), msg)

    def check_form_sent_passwd(self, form_note):
        """ Проверяем форму, что пароль выслан.
        :param form_note: ссылка на форму.
        """
        msg = u"Пароль отправлен на указанный номер.\nВведите его в течение 5 минут."
        self.assertIn(form_note.text, msg)

    def check_passwd_confirm(self, driver, sleep=5):
        """ Проверить сообщение "Пароль подтверждён".
        :param driver: ссылка на драйвер
        :return: ссылка на элемент
        """
        try:
            pass_confirm = driver.find_element_by_xpath(HelpRegData.PASSWD_CONFIRM)
        except Exception:
            time.sleep(sleep)
            try:
                pass_confirm = driver.find_element_by_xpath(HelpRegData.PASSWD_CONFIRM)
            except Exception:
                raise AssertionError("ОШИБКА: Сообщение 'Пароль подтвержден' не появилось.")
        return self.assertIsNotNone(pass_confirm)

    def check_disable_fields_by_registration_page(self, driver):
        """ Проверка, что поля стали нередактируемыми на странице регистрации.
        :param driver: ссылка на драйвер
        """
        self.assertIsNotNone(driver.find_element_by_xpath(HelpRegData.REG_FIELD_PHONE))
        self.assertIsNotNone(driver.find_element_by_xpath(HelpRegData.REG_FIELD_USERNAME))
        #self.assertIsNotNone(driver.find_element_by_xpath(HelpRegData.REG_FIELD_PASSWD))

    def check_click_create_account(self, driver):
        """ Проверить нажатие создать аккаунт.
        :param driver: ссфлка на драйвер.
        """
        self.assertIsNotNone(driver.find_element_by_xpath(HelpRegData.BY_CLICK_CREATE_ACCOUNT))

    def check_button_not_focus(self, driver):
        """ Проверить что кнопки Продавец и Покупатель должны быть по умолчанию не выбранными.
        """
        self.assertIsNotNone(driver.find_element_by_xpath(HelpRegData.RADIOBUTTON_SELLER_BUYER_NOT_FOCUS))

    def check_confirm_agreement(self, driver):
        """ Поверить "я соглашаюсь с пользовательским соглашением."
        :param driver: ссылка на драйвер
        """
        service_log.put("check 'I agree'.")
        self.assertEqual(driver.find_element_by_xpath(HelpRegData.CONFIRMATION_AGREEMENT).text.encode('utf-8'),
                         'Нажимая создать аккаунт,\nя соглашаюсь с Условиями УУРРАА')

    def check_license_option(self, driver):
        """ Проверить лицензионное соглашение.
        :param driver: ссылка на драйвер
        """
        return self.assertIsNotNone(driver.find_element_by_xpath(HelpRegData.BY_CLICK_CREATE_ACCOUNT))

    def check_disable_button(self, driver):
        """ Проверить, что кнопка была заблокированна.
        :param driver: ссылка на драйвер
        """
        return self.assertIsNotNone(driver.find_element_by_xpath(HelpRegData.REG_BUTTON_DISABLE))

    def check_correct_writing_phone_salt_passwd(self, res):
        """ Проверяем, что пароль, соль, записываются в БД корректно и телефон в БД уникален.
        :param res: выборка записей из БД.
        """
        self.assertEqual(len(res), 1, "Found several telephone!")  # номер телефона уникальный
        self.assertEqual(len(res[0]["salt"]), 20, "The salt is less than specified.")
        self.assertEqual(len(res[0]["code_value"]), 64, "The hash of the password is less than specified.")

    def check_page_help(self, driver):
        """ Проверяет переход на страницы, Помощь
        :param driver: ссылка на драйвер
        """
        msg_error = "Нет страницы Помощь. Не могу перейти на страницу помощи"
        self.assertIsNotNone(driver.find_element_by_xpath(HelpRegData.REG_HELP_PAGE), msg_error)
        driver.get("http://front1.tst.oorraa.net" + "/help-1")
        #time.sleep(2)
        self.assertIsNotNone(driver.find_element_by_xpath(self.check_help.REG_HELP_CENTER))

    def check_not_right_password(self, driver):
        """ Проверка сообщения о неправильном пароле.
        :param driver: ссылка на драйвер
        """
        msg = "Не вывелось сообщение об ошибке 'Неверный пароль'. Ввелись 6 символов пароля. Регистрация продолжается."
        self.assertIsNotNone(driver.find_element_by_xpath(HelpRegData.NOT_RIGHT_PASSWD), msg)

    def check_registration_page(self, driver):
        """ Проверка страницы регистрации.
        :param driver: ссылка на драйвер
        """

        for index in self.LIST_REG_PAGE1:
            self.assertIsNotNone(Navigate.get_element_navigate(driver, index))

        for index in self.LIST_REG_PAGE2:
            Navigate.element_is_none(driver, index)

        # проверка что можно вводить только российские номера
        self.assertEqual(driver.find_element_by_xpath(self.FORM_PHONE_CODE).text, u'+7')

    def check_registration_seller(self, driver):
        """ Проверяем элементы при создании продавца.
        :param driver:
        """
        #self.assertIsNotNone(driver.find_element_by_xpath(self.RULES_HREF))
        self.assertIsNotNone(driver.find_element_by_xpath(self.BY_CLICK_CREATE_ACCOUNT))

    def check_instruction(self, instruction):
        """ Проверка инструкций.
        :param instruction: текст инструкций
        """
        msg1 = u'1. Зарегистрируйтесь как покупатель\n'
        msg2 = u'2. Зайдите в настройки\n'
        msg3 = u'3. Рядом с указанной ролью нажмите\n"Хочу зарегистрироваться как продавец"\n'
        msg4 = u'4. Результат рассмотрения заявки будет отправлен Вам сообщением в Личный кабинет'
        msg = msg1 + msg2 + msg3 + msg4
        self.assertEqual(instruction.decode('utf-8'), msg, "Не совпадают")

    def check_msg_user_exist(self, driver):
        """ Возвращаем текст о существовании пользователя.
        :param driver: ссылка на драйвер
        :return: текст о существовании пользователя
        """
        Navigate.get_element_navigate(driver, HelpRegData.USER_EXIST_MSG, mode=None)

    def check_activation_promo_code(self, driver):
        """ Проверка ошибки 'Ошибка активации пригласительного кода'.
        :return: None
        """
        self.assertIsNotNone(driver.find_element_by_xpath(self.MSG_ERROR_FORM % self.TEXT_ERROR_ACTIVATION_PROMO_CODE))

    def check_expired_promo_code(self, driver):
        """  Проверка 'Указанный пригласительный код просрочен'
        :return: None
        """
        self.assertIsNotNone(driver.find_element_by_xpath(self.MSG_ERROR_FORM % self.TEXT_EXPIRED_PROMO_CODE))

    def check_revoked_promo_code(self, driver):
        """  Проверка 'Указанный пригласительный код недействителен'
        :return: None
        """
        self.assertIsNotNone(driver.find_element_by_xpath(self.MSG_ERROR_FORM % self.TEXT_REVOKED_PROMO_CODE))

    def check_not_correct_promo_code(self, driver):
        """  Проверка 'Указан неверный пригласительный код'
        :return: None
        """
        self.assertIsNotNone(driver.find_element_by_xpath(self.MSG_ERROR_FORM % self.TEXT_NOT_CORRECT_PROMO_CODE))





