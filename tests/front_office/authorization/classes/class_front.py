# -*- coding: utf-8 -*-
import time

from tests.MainClass import MainClass
from tests.front_office.data_navigation import MainPage, AuthorizationPage, RestorePage
from support import service_log
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods

__author__ = 's.trubachev'


class HelpAuthData(MainClass):
    click_main = MainPage.Click
    check_auth = AuthorizationPage.Check
    check_restore = RestorePage.Check

    HEADER_USER = "//div[@class='header__user']"

    XPATH_ERROR = "//span[@class='form__error']"
    ERROR_AUTH = "//span[@class='form__error' and contains(.,'%s')]"
    GET_ERROR_MESSAGE = "//span[@class='form__error' and text()]"
    FORM_PHONE_CODE = "//span[@class='form__phone-code']"
    FORM_PASS = "//input[@class='form__input' and @name='pass']"
    FORM_NOTE = "//div[@class='form__note']/.."

    TEXT_USER_BLOCKED = "Пользователь заблокирован. Для уточнения причин свяжитесь с нами по почте help@oorraa.com"
    TEXT_USER_UNREG = "Регистрация пользователя не закончена. Повторите регистрацию с указанным номером телефона"
    TEXT_CHECK_PHONE_OR_PASS = "Проверьте правильность ввода номера телефона и пароля"
    TEXT_NEED_PASSWORD = "Введите пароль"
    TEXT_NEED_PHONE = "Введите телефон"
    TEXT_NEED_PHONE_EMAIL = "Введите телефон или email"
    TEXT_ERROR_NEW_PASSWD = "Пользователь с таким номером телефона не зарегистрирован"
    TEXT_SENT_PASSWD = "Новый пароль выслан Вам на указанный номер с помощью SMS"

    LIST_ERROR_FOR_STATUS = {"DISABLED": TEXT_USER_BLOCKED,
                             "WAIT_FOR_REGISTRATION": TEXT_USER_UNREG}

    MENU_MY_SHOP = "//a[@href='/store/%s']/span[text()='Мой магазин']"
    MENU_PROFILE_MY_GOODS = "//a[@href='/user/goods']//span[contains(.,'Мои товары')]"
    MENU_PROFILE_SETTINGS = "//a[@href='/user/settings/profile']/span[contains(.,'Настройки')]"
    MENU_PROFILE_ACTION_HEADER = "//span[@class='header__action header__action_exit']"

    REGISTRATION_PAGE = "//a[@href='/registration' and contains(.,'Регистрация')]"
    REGISTRATION_PAGE2 = "//button[contains(.,'Регистрация и вход')]"

    # проверка формы регистрации, объеденена с формой авторизации (build 14.05.2015)
    #REGISTRATION_PAGE_TITLE = "//h1[@class='title__name' and text()='Создайте свой аккаунт на УУРРАА']"
    REGISTRATION_PAGE_TITLE = """//span[contains(.,'Нажимая кнопку "Зарегистрироваться",""" \
                              """ вы подтверждаете свое согласие с условиями предоставления услуг (')]"""

    SENT_PASSWD = "//span[@class='notification__title' and contains(.,'%s')]"
    MENU_LOGIN = "//button[@type='submit']/span[text()='Войти']"

    HAVE_NOT_RECEIVER_PASSWD = "//span[text()='Не приходит пароль?']"
    REPEAT_SEND_PASSWD = "//span[text()='Отправить пароль повторно']"
    CHECK_INSTRUCT_NOT_PASSWD = "Проверьте правильность введенного номера. Если номер указан неверно, повторите ввод"
    CHECK_OBJ_INSTRUCT_NOT_PASSWD = "//div[@class='form__note']/p/span[contains(.,'%s')]"
    OBJ_NOT_RECEIVER_PASSWD = "//div[@class='form__note']/p/span[contains(.,'%s')]"
    LIST_INSTRUCT_NOT_PASSWD = ["Если Вы уверены в правильности ввода, воспользуйтесь повторной отправкой пароля.",
                                "Если перечисленные способы не помогают, свяжитесь с нами по почте help@oorraa.com"]

    LOGO_HEADER_MAIN_PAGE = "//a[@class='header__logo header__cell active']"
    LOGO_HEADER_PAGE = "//a[@class='header__logo header__cell']"


    SMS_STATUS = dict(
        # новое SMS-сообщение
        NEW=10,
        # сообщение отправлено провайдеру
        SENT=20,
        # сообщение отправлено провайдеру и получен ответ о подтверждении принятия сообщения
        ACKNOWLEDGED=30,
        # сообщение было отправлено провайдеру, но НЕ БЫЛО ПОЛУЧЕНО подтверждение принятия сообщения провайдером
        NOT_ACKNOWLEDGED=35,
        # сообщение было доставлено (получен подтверждающий результат от провайдера)
        DELIVERED=40,
        # сообщение не доставлено (сообщение пришло к провайдеру, но не было доставлено абоненту)
        NOT_DELIVERED=45,
        # сообщение устарело
        EXPIRED=50,
        # номер получателя сообщения не прошел валидацию
        REJECTED_BY_NUMBER=60,
        # содержимое сообщения не прошло валидацию
        REJECTED_BY_CONTENT=65,
        # превышен суточный лимит сообщений на один номер
        REJECTED_BY_LIMIT=66,
        # Баланс пуст (проверьте баланс)
        REJECTED_BY_BALANCE=68,
        # отклонено провайдером по специфичной причине
        REJECTED_BY_PROVIDER=69,
        # произошла внутренняя ошибка в нашей системе при отправке сообщения
        INTERNAL_ERROR=70,
        # произошла ошибка на стороне провайдера при отправке сообщения
        EXTERNAL_ERROR=75
    )

    # COOKIE для идентификации пользователей на сайте минуя процесс авториации
    COOKIE_AUTH_FRONT1 = {"28": {},
                          "1":  [],
                          "40": [],
                          "26": [],
                          "51": {"sid": "c36bdbf8-ce33-4492-b219-c81bddddc36b"}}

    COOKIE_AUTH_FRONT2 = {'28': [],
                          '1': [],
                          '40': [],
                          '26': [],
                          '51': {"sid": "c797dd08-b25b-48a1-b2e2-f539a128e866"}}

    COOKIE_AUTH_PROD = {}
    COOKIE_AUTH_DEV3 = {}

    COOKIE_AUTH = {
        "http://www.oorraa.com": COOKIE_AUTH_PROD,
        "http://front1.test.oorraa.net": COOKIE_AUTH_FRONT1,
        "http://front2.test.oorraa.net": COOKIE_AUTH_FRONT2,
        "http://front3.dev.oorraa.pro": COOKIE_AUTH_DEV3
    }


class HelpAuthMethods(HelpAuthData):

    @staticmethod
    def get_cookies(user_id):
        """ Получить cookies заданного пользователя в зависимости от тестового стенда.
        :param user_id: идентификатор пользователя
        :return: cookies заданного пользователя
        """
        from support.utils.variables import EVariable
        cookies = None
        try:
            cookies = HelpAuthData.COOKIE_AUTH[EVariable.front_base.url.strip()][user_id]
            service_log.put("Get cookies for user Id: '%s' with cookies: '%s'" % (user_id, str(cookies)))
        except ValueError, tx:
            msg_error = "Not found cookies for user Id: '%s'" % user_id
            service_log.error(msg_error)
            service_log.error(str(tx))
            raise AssertionError(msg_error)
        return cookies

    @staticmethod
    def set_cookies(driver, user_id='51', data=0):
        #p = SeleniumMethods.get_all_cookies_items(driver)
        #driver.session_id = HelpAuthMethods.get_cookies(user_id)["sid"]
        #driver.refresh()
        #d = SeleniumMethods.del_session_id(driver, p["sessionId"])
        #val = HelpAuthMethods.get_cookies(user_id)
        #a = SeleniumMethods.add_cookie_item(driver, val)
        pass

    @staticmethod
    def set_authorization_by_phone(driver, phone, passwd):
        """ Произвести авторизацию через
        :return: ответ от сервера
        """
        from support.utils.variables import EVariable
        front_url = EVariable.front_base.url.strip()
        request = front_url + '/api?method=auth.login&params={"phone":"%s","password":"%s"}' % (phone, passwd)
        result = driver.get(request)
        return result

    @staticmethod
    def go_main(driver, phone=None, email=None, passwd=None, flag_auth=True, flag_api=True):
        """ Универсальный переход на главную страницу.
        :param driver: ссылка на драйвер
        :param phone: номер телефона
        :param email: электронная почта
        :param passwd: пароль
        :param flag_auth: флаг авторизации
        """
        from support.utils.variables import EVariable
        env_base_url = EVariable.front_base.url.strip()

        # авторизоваться через API
        if flag_auth:
            service_log.put("To authorization via API")
            if flag_api:
                if email is None and phone is not None:
                    HelpAuthMethods.set_authorization_by_phone(driver, phone, passwd)
                elif email is not None and phone is None:
                    # TODO
                    pass
                else:
                    msg_error = "Not correct params."
                    service_log.error(msg_error)
                    assert AssertionError(msg_error)
            else:
                if email is None and phone is not None:
                    HelpNavigateCheckMethods.get_page(driver, HelpNavigateCheckMethods.path_auth.PATH_AUTH)
                    obj_phone, obj_password, obj_submit_button = HelpAuthCheckMethods.get_data_authorization(driver)

                    # Вводим данные на авторизацию
                    l = lambda e, p:e if p is None else p
                    HelpAuthCheckMethods.send_phone(phone_object=obj_phone, phone_number=l(email, phone))
                    HelpAuthCheckMethods.send_password(password_object=obj_password, password_number=passwd)
                    # Нажатие на кнопку авторизации
                    HelpNavigateCheckMethods.element_click(driver, obj_submit_button, change_page_url=True)
                    time.sleep(HelpNavigateCheckMethods.time_sleep)
                elif email is not None and phone is None:
                    # TODO
                    pass
                else:
                    msg_error = "Not correct params."
                    service_log.error(msg_error)
                    assert AssertionError(msg_error)
            service_log.put("To authorization via API - success.")

        service_log.put("Get page: %s" % env_base_url)
        do_get_work = time.time()
        driver.get(env_base_url)
        work_get_time = HelpNavigateCheckMethods.work_time(do_get_work)
        service_log.put("Onload event time: [%s]" % work_get_time)
        HelpNavigateCheckMethods.progress(driver)
        work_load_time = HelpNavigateCheckMethods.work_time(do_get_work)
        service_log.put("Page received: %s" % env_base_url)
        service_log.put("Page received time: %s" % work_load_time)
        time.sleep(3)

    @staticmethod
    def set_text_xpath_error(text):
        """ Вставляем текст ошибки в XPATh.
        :param text: текст
        :return: xpath с текстом
        """
        return HelpAuthData.ERROR_AUTH % text

    @staticmethod
    def set_store_xpath_by_my_shop(user_id):
        """ Вставляем текст ошибки в XPATh.
        :param user_id:
        :return: xpath с текстом
        """
        return HelpAuthData.MENU_MY_SHOP % user_id

    @staticmethod
    def set_text_xpath_by_menu(buyer):
        """ Вставляем текст.
        :param buyer:
        :return:  xpath с текстом
        """
        return "//div[@class='header__info']/span[contains(.,'%s')]" % buyer

    @staticmethod
    def go_authorization_page(driver, env_base_url=MainClass.ENV_BASE_URL, sleep=2):
        """ Авторизоваться через главную страницу.
        :param driver: ссылка на драйвер
        :param env_base_url: адрес главной страницы
        :param sleep: ожидание пока страница прогрузиться
        """
        service_log.put("Get page: %s" % env_base_url)
        do_get_work = time.time()
        driver.get(env_base_url)
        work_get_time = HelpNavigateCheckMethods.work_time(do_get_work)
        service_log.put("Onload event time: [%s]" % work_get_time)
        HelpNavigateCheckMethods.progress(driver)
        work_load_time = HelpNavigateCheckMethods.work_time(do_get_work)
        service_log.put("Page received: %s" % env_base_url)
        service_log.put("Page received time: %s" % work_load_time)
        reg_log_btn = HelpNavigateCheckMethods.get_element_navigate(driver, HelpAuthData.click_main.BUTTON_REG_AN_LOGIN)
        HelpAuthCheckMethods.click_button(reg_log_btn)
        login_button = HelpNavigateCheckMethods.get_element_navigate(driver, HelpAuthData.click_main.BUTTON_LOGIN, mode=None)
        login_button.is_displayed()
        login_button.is_enabled()
        HelpNavigateCheckMethods.element_click(driver, login_button)

    @staticmethod
    def do_login(driver, sleep=2):
        """ Авторизоваться нажав на кнопку с текущей страницы.
        :param driver: ссылка на драйвер
        :param sleep: ожидание
        """
        # time.sleep(sleep)
        reg_log_btn = HelpNavigateCheckMethods.get_element_navigate(driver, HelpAuthData.click_main.BUTTON_REG_AN_LOGIN)
        HelpAuthCheckMethods.click_button(reg_log_btn)
        login_button = HelpNavigateCheckMethods.get_element_navigate(driver, HelpAuthData.click_main.BUTTON_LOGIN)
        login_button.is_displayed()
        login_button.is_enabled()
        HelpNavigateCheckMethods.element_click(driver, login_button)

    @staticmethod
    def go_registration_page(driver, type_xpath=1, env_base_url=MainClass.ENV_BASE_URL, sleep=2):
        """ Переход на страницу регистрации.
        :param driver: ссылка на драйвер
        :param type_xpath: тип перехода по xpath
        :param sleep: задержка в миллесекундах
        """
        registration_button = None
        if type_xpath == 1:
            registration_button = HelpNavigateCheckMethods.element_is_present(driver, HelpAuthData.REGISTRATION_PAGE)
            # time.sleep(sleep)
        elif type_xpath == 2:
            service_log.put("Get page: %s" % env_base_url)
            do_get_work = time.time()
            driver.get(env_base_url)
            work_get_time = HelpNavigateCheckMethods.work_time(do_get_work)
            service_log.put("Onload event time: [%s]" % work_get_time)
            HelpNavigateCheckMethods.progress(driver)
            work_load_time = HelpNavigateCheckMethods.work_time(do_get_work)
            service_log.put("Page received: %s" % env_base_url)
            service_log.put("Page received time: %s" % work_load_time)
            registration_button = HelpNavigateCheckMethods.element_is_present(driver, HelpAuthData.click_main.BUTTON_REG_AN_LOGIN)
        registration_button.click()
        time.sleep(sleep)

    @staticmethod
    def go_restore_page(driver, sleep=2):
        """ Переход на страницу "Забыли пароль".
        :param driver: ссылка на драйвер
        """
        restore_button = HelpNavigateCheckMethods.element_is_present(driver, HelpAuthData.check_restore.RESTORE_PAGE)
        restore_button.click()
        time.sleep(sleep)

    @staticmethod
    def get_data_authorization(driver):
        """ Получить данные страницы авторизации.
        :param driver: ссылка на драйвер
        :return: телефон, пароль, кнопка "Войти"
        """
        phone = HelpNavigateCheckMethods.element_is_present(driver, "//input[@name='phoneOrEmail']")
        phone.is_displayed()
        phone.is_enabled()
        password = HelpNavigateCheckMethods.element_is_present(driver, "//input[@name='password']")
        password.is_displayed()
        password.is_enabled()
        submit_button = HelpNavigateCheckMethods.element_is_present(driver, "//button[@type='submit']")  # проверка кнопки Войти
        submit_button.is_displayed()
        submit_button.is_enabled()
        return phone, password, submit_button

    @staticmethod
    def get_data_restore(driver):
        """ Получить данные страницы восстановления пароля.
        :param driver: ссылка на драйвер
        :return: телефон, пароль, кнопка "Войти"
        """
        phone = HelpNavigateCheckMethods.element_is_present(driver, "//input[@name='phone' and @placeholder='(800) 000-00-00']")
        sent_pass_button = HelpNavigateCheckMethods.element_is_present(driver, "//span[text()='Выслать пароль']")  # кнопка Выслать пароль
        return phone, sent_pass_button

    @staticmethod
    def get_phone(source_phone, type_phone='PHONE_VALID'):
        """ Вернуть номер телефона.
        :param source_phone: исходный номер телефона
        :param type_phone: тип возвращаемого номера
        :return: строка с изменениями
        """
        if type_phone == 'PHONE_VALID':
            service_log.put("PHONE_VALID: %s" % source_phone)
            return source_phone
        elif type_phone == 'LARGE_PHONE_VALID':
            service_log.put("LARGE_PHONE_VALID: %s" % source_phone)
            return source_phone + '7676'
        elif type_phone == 'PHONE_INVALID':
            service_log.put("PHONE_INVALID: %s" % source_phone)
            return source_phone[1:] + "0"
        else:
            msg_error = "Not fount type phone: %s" % source_phone
            service_log.error(msg_error)
            AssertionError(msg_error)

    @staticmethod
    def get_password(source_passwd, type_passwd='CORRECT'):
        """ Вернуть пароль.
        :param source_passwd: исходный пароль
        :param type_passwd: тип возвращаемого пароля
        :return: строка с изменениями
        """
        if type_passwd == 'CORRECT' or type_passwd == 'LARGE_CORRECT':
            return source_passwd
        elif type_passwd == 'INCORRECT_REGISTER':
            return source_passwd.lower()
        elif type_passwd == 'INCORRECT':
            return source_passwd + '123'
        else:
            msg_error = "Not fount type password: %s" % source_passwd
            service_log.error(msg_error)
            AssertionError(msg_error)

    @staticmethod
    def get_login(driver):
        """ Ссылка на залогинивание.
        :param driver: драйвер
        """
        p = HelpNavigateCheckMethods.element_is_present(driver, HelpAuthData.MENU_LOGIN)
        service_log.put("Submit button find.")
        return p

    @staticmethod
    def get_form_note(driver):
        """ Форма сообщающая, что пароль выслан.
        :param driver: драйвер
        """
        return HelpNavigateCheckMethods.element_is_present(driver, HelpAuthData.FORM_NOTE)

    @staticmethod
    def get_error_message(driver):
        """ Вернуть сообщение об ошибке.
        :param driver: драйвер
        :return: текст ошибки
        """
        return HelpNavigateCheckMethods.element_is_present(driver, HelpAuthData.GET_ERROR_MESSAGE)

    @staticmethod
    def get_pass_input(driver):
        """

        :param driver:
        :return:
        """
        return HelpNavigateCheckMethods.element_is_present(driver, HelpAuthData.FORM_PASS)

    @staticmethod
    def get_message_have_not_receiver_passwd(driver):
        """ Вернуть сообщение о том, что пароль не приходит.
        :param driver: ссылка на драйвер
        :return: ссылка на элемент
        """
        return HelpNavigateCheckMethods.element_is_present(driver, HelpAuthData.HAVE_NOT_RECEIVER_PASSWD)

    @staticmethod
    def get_password_from_log(message):
        """ Выдернуть номер пароля из текста логов.
        :param message: весь текст
        :return: пароль
        """
        return message[-10:-5]

    @staticmethod
    def get_repeat_send_passwd(driver):
        """ Найти кнопку отправить пароль повторно.
        :param driver: ссылка на драйвер
        :return: ссылка на объект
        """
        time.sleep(30)  # стоит задержка в 30 секунд на отсылку паролей
        p = HelpNavigateCheckMethods.element_is_present(driver, HelpAuthData.REPEAT_SEND_PASSWD)
        return p

    @staticmethod
    def send_password(password_object, password_number):
        """ Ввести пароль.
        :param password_number: пароль
        :param password_object: объект формы для ввода пароля
        """
        service_log.put("Send password: %s" % password_number)
        password_object.send_keys(password_number)

    @staticmethod
    def send_phone(phone_object, phone_number):
        """ Ввести номер телефона.
        :param phone_number: номер телефона
        :param phone_object: объект формы для ввода телефона
        """
        service_log.put("Send phone: %s" % phone_number)
        phone_object.send_keys(phone_number)

    @staticmethod
    def send_email(email_object, email_adress):
        """ Ввести e-mail пользователя.
        :param email_adress: e-mail пользователя
        :param email_object: объект формы для ввода e-mail
        """
        service_log.put("Send phone: %s" % email_adress)
        email_object.send_keys(email_adress)

    @staticmethod
    def submit_button(obj_button, sleep=2):
        """ Нажатие на кнопку.
        :param obj_button: объект кнопки
        :return:
        """
        service_log.put("Submit button: %s" % str(obj_button))
        obj_button.click()
        time.sleep(sleep)
        service_log.put("Submit button success.")

    @staticmethod
    def click_button(obj_button, sleep=2):
        """ Нажатие на кнопку.
        :param obj_button: объект кнопки
        :return:
        """
        service_log.put("Click button: %s" % str(obj_button))
        obj_button.click()
        time.sleep(sleep)
        service_log.put("Click button success.")

    @staticmethod
    def click_to_phone(driver):
        """ Нажатие на кнопку авторизации по телефону
        """
        obj_button = HelpNavigateCheckMethods.get_element_navigate(driver, AuthorizationPage.Click.BTN_PHONE, mode=None)
        HelpAuthMethods.submit_button(obj_button=obj_button, sleep=0)

    @staticmethod
    def click_to_email(driver):
        """ Нажатие на кнопку авторизации по email
        """
        obj_button = HelpNavigateCheckMethods.get_element_navigate(driver, AuthorizationPage.Click.BTN_EMAIL)
        HelpAuthMethods.submit_button(obj_button=obj_button, sleep=0)

    @staticmethod
    def get_error_message_xpath(driver, xpath):
        try:
            obj = HelpNavigateCheckMethods.element_is_present(driver, xpath)
        except Exception:
            raise AssertionError("ОШИБКА: Не найдено сообщение об ошибке с path: %s." % xpath)
        return obj


class HelpAuthCheckMethods(HelpAuthMethods):

    def check_page_authorization(self, driver):
        """ TestRail: C-27 Внешний вид страницы Авторизации (wide)
        http://test-rails.oorraa.pro/index.php?/cases/view/27
        :param driver: ссылка на дравер
        """

        list_check1 = [#self.check_auth.TITLE_AUTH_PAGE,
                       #self.check_auth.HEADER,  # проверка header.
                       self.check_auth.LOGO,  # проверка логотипа.
                       self.check_auth.FORM_AUTH,  # проверка формы авторизации
                       self.check_auth.FORM_PHONE,  # проверка формы Моб.телефон
                       self.check_auth.FORM_PASS,  # проверка формы Пароль
                       self.check_auth.BTN_RESTORE,  # проверка кнопки Забыли пароль
                       #self.check_auth.BLC_RIGHT,  # блок справа "Впервые на УУРРАА? Регистрация"
                       #self.check_auth.TITLE_RIGHT,  # проверка загловка 'Впервые на УУРРАА?'
                       #self.check_auth.TITLE_BLC,  # загловк 'Впервые на УУРРАА?'
                       self.check_auth.BTN_REGISTRATION,  # проверка кнопки Регистрация
                       self.check_auth.FOOTER,  # проверка подвала
                       self.check_auth.INPUT_PHONE,
                       self.check_auth.INPUT_PASS,
                       self.check_auth.BTN_LOGIN
        ]

        list_check2 = ["//input[@class='search__input']",  # проверка отсутствия поиска
                       "//ul[@class='cat__list']",  # проверка отсутствия 6 рутовых категорий
                       "//nav[@class='cat']",  # проверка отсутствия Каталог товаров
        ]

        # Первый список проверки
        for index in list_check1:
            self.assertIsNotNone(HelpNavigateCheckMethods.get_element_navigate(driver, index))

        # Второй список проверки
        for index in list_check2:
            HelpNavigateCheckMethods.element_is_none(driver, index)

        # проверка что можно вводить только российские номера
        #self.assertEqual(driver.find_element_by_xpath(self.FORM_PHONE_CODE).text, u'+7')

    def check_page_restore_password(self, driver):
        """ TestRail: C-548 Валидации полей формы Восстановления пароля: Негативные
        http://test-rails.oorraa.pro/index.php?/cases/view/548
        :param driver: ссылка на дравер
        """

        list_check1 = [self.check_restore.TITLE_RESTORE_PAGE,
                       #self.check_restore.HEADER,
                       self.check_restore.LOGO,
                       self.check_restore.FORM_RESTORE,
                       self.check_restore.FORM_PHONE,
                       #self.check_restore.BLC_RIGHT,
                       #self.check_restore.TITLE_RIGHT,
                       #self.check_restore.TITLE_BLC,
                       #self.check_restore.BTN_REGISTRATION,
                       self.check_restore.FOOTER,
                       self.check_restore.INPUT_PHONE,
                       self.check_restore.BTN_RESTORE
        ]

        list_check2 = ["//input[@class='search__input']",  # проверка отсутствия поиска
                       "//ul[@class='cat__list']",  # проверка отсутствия 6 рутовых категорий
                       "//nav[@class='cat']",  # проверка отсутствия Каталог товаров
        ]

        # Первый список проверки
        for index in list_check1:
            self.assertIsNotNone(driver.find_element_by_xpath(index))

        # Второй список проверки
        for index in list_check2:
            HelpNavigateCheckMethods.element_is_none(driver, index)

        # проверка что можно вводить только российские номера
        self.assertEqual(driver.find_element_by_xpath(self.FORM_PHONE_CODE).text, u'+7')

    def check_menu_profile_widget_total(self, driver, display_name, sleep=5):
        """ Проверка меню профиля.
        :param driver: ссылка на драйвер
        :param display_name: имя пользователя
        """
        disp_name = None
        try:
            disp_name = HelpNavigateCheckMethods.get_element_navigate(driver, self.set_text_xpath_by_menu(display_name))
        except UnicodeEncodeError:
            name_encode = display_name.encode("utf-8")
            disp_name = HelpNavigateCheckMethods.get_element_navigate(driver, self.set_text_xpath_by_menu(name_encode))
        self.assertIsNotNone(disp_name)
        self.assertIsNotNone(HelpNavigateCheckMethods.get_element_navigate(driver, self.MENU_PROFILE_SETTINGS))
        self.assertIsNotNone(HelpNavigateCheckMethods.get_element_navigate(driver, self.MENU_PROFILE_ACTION_HEADER))

    def check_menu_profile_widget_my_shop(self, driver):
        """ Проверка виджета "Мой магазин" меню профиля.
        :param driver: ссылка на драйвер
        :param accounts_id: идентификатор пользователя
        """
        msg = "ОШИБКА: У продавца в меню из виджета профиля нет пункта 'Мой магазин'"
        self.assertIsNotNone(driver.find_element_by_xpath(self.click_main.HEADER_MY_SHOP), msg)


    def check_menu_profile_widget_without_my_shop(self, driver, accounts_id):
        """ Проверка виджета "Мой магазин" меню профиля.
        :param driver: ссылка на драйвер
        :param accounts_id: идентификатор пользователя
        """
        tx = None
        try:
            driver.find_element_by_xpath(self.click_main.HEADER_MY_SHOP)
            driver.find_element_by_xpath(self.set_store_xpath_by_my_shop(accounts_id))
        except Exception, tx:
            pass
        msg = "ОШИБКА: У покупателя в меню из виджета профиля присутствует пункт 'Мои товары' или 'Мой магазин'."
        self.assertIsNotNone(tx, msg)

    def check_profile_widget(self, driver, mode="refresh"):
        """ Проверка профиля виджета.
        :param driver: ссылка на драйвер
        """
        user_block = HelpNavigateCheckMethods.get_element_navigate(driver=driver, xpath=self.HEADER_USER, mode=mode)
        user_block.is_enabled()
        user_block.click()

    def check_error(self, driver, msg=None):
        """ Проверка наличия ошибки.
        :param driver: ссылка на драйвер
        """
        self.assertIsNotNone(driver.find_element_by_xpath(self.XPATH_ERROR), msg)

    def check_incorrect_passwd_or_phone(self, driver):
        """ Проверяем форму при вводе не корректного пароля.
        :param driver: ссылка на драйвер
        """

        self.check_error(driver)
        HelpNavigateCheckMethods.element_is_present(driver, self.set_text_xpath_error(self.TEXT_CHECK_PHONE_OR_PASS))

    def check_incorrect_passwd(self, driver):
        """ Проверяем форму при вводе не корректного пароля.
        :param driver: ссылка на драйвер
        """
        self.check_error(driver)
        HelpNavigateCheckMethods.element_is_present(driver, self.set_text_xpath_error(self.TEXT_CHECK_PHONE_OR_PASS))

    def check_user_disabled(self, driver):
        """ Проверка бюлокировки пользователя.
        :param driver: ссылка на драйвер
        """
        self.check_error(driver)
        HelpNavigateCheckMethods.element_is_present(driver, self.set_text_xpath_error(self.TEXT_USER_BLOCKED))

    def check_user_wait_for_registration(self, driver):
        """ Проверка пользователя с незаконченной регистрацией.
        :param driver: ссылка на драйвер
        """
        self.check_error(driver)
        self.assertIsNotNone(self.get_error_message_xpath(driver, self.set_text_xpath_error(self.TEXT_USER_UNREG)))

    def check_need_password(self, driver):
        """ Проверка окна ошибки "введите пароль".
        :param driver: ссылка на драйвер
        """
        msg = "Не вывелось сообщение об ошибке 'Вы ввели неверный пароль. Пожалуйста попробуйте еще раз.'"
        self.assertIsNotNone(
            HelpNavigateCheckMethods.element_is_present(driver, self.set_text_xpath_error(self.TEXT_NEED_PASSWORD)), msg)

    def check_not_need_password(self, driver):
        """ Проверка отсутствия окна ошибки "введите телефон".
        :param driver: ссылка на драйвер
        """
        tx = None
        try:
            HelpNavigateCheckMethods.element_is_present(driver, self.set_text_xpath_error(self.TEXT_NEED_PASSWORD))
        except Exception, tx:
            pass
        self.assertIsNotNone(tx, "Found element %s" % self.TEXT_NEED_PASSWORD)

    def check_need_phone(self, driver):
        """ Проверка окна ошибки "введите телефон".
        :param driver: ссылка на драйвер
        """
        HelpNavigateCheckMethods.element_is_present(driver, self.set_text_xpath_error(self.TEXT_NEED_PHONE_EMAIL))

    def check_need_phone_only(self, driver):
        """ Проверка окна ошибки "введите телефон".
        :param driver: ссылка на драйвер
        """
        HelpNavigateCheckMethods.element_is_present(driver, self.set_text_xpath_error(self.TEXT_NEED_PHONE))

    def check_not_need_phone(self, driver):
        """ Проверка отсутствия окна ошибки "введите телефон".
        :param driver: ссылка на драйвер
        """
        tx = None
        try:
            HelpNavigateCheckMethods.element_is_present(driver, self.set_text_xpath_error(self.TEXT_NEED_PHONE_EMAIL))
        except Exception, tx:
            pass
        self.assertIsNotNone(tx, "Found element %s" % self.TEXT_NEED_PHONE_EMAIL)

    def check_restore_page(self, driver):
        """ Проверка формы на странице "Забыли пароль".
        :param driver: ссылка на драйвер
        """
        HelpNavigateCheckMethods.element_is_present(driver, self.check_restore.RESTORE_PAGE_FORM_AUTH)
        HelpNavigateCheckMethods.element_is_present(driver, self.check_restore.INPUT_PHONE)
        HelpNavigateCheckMethods.element_is_present(driver, self.check_restore.BTN_RESTORE)
        HelpNavigateCheckMethods.element_is_present(driver, self.check_restore.FORM_PHONE)

    def check_registration_page(self, driver):
        """ Проверяем, что находимся на странице регистрации.
        :param driver: ссылка на драйвер
        """
        HelpNavigateCheckMethods.element_is_present(driver, self.REGISTRATION_PAGE_TITLE)

    def check_sent_passwd(self, driver):
        """ Проверить ошибку при отправке пароля.
        :param driver: ссылка на драйвер
        """
        HelpNavigateCheckMethods.element_is_present(driver, self.SENT_PASSWD % self.TEXT_ERROR_NEW_PASSWD)

    def check_password_is_sent(self, driver, sleep=1):
        """ Проверка сообщения, что пароль выслан.
        :param driver: ссылка на драйвер
        """
        time.sleep(sleep)
        HelpNavigateCheckMethods.element_is_present(driver, self.SENT_PASSWD % self.TEXT_SENT_PASSWD)

    def check_form_sent_passwd(self, form_note, sleep=2):
        """ Проверяем форму, что пароль выслан.
        :param form_note: ссылка на форму.
        """
        msg = u"Пароль отправлен на указанный номер.\nВведите его в течение 5 минут."
        self.assertIn(form_note.text, msg)
        time.sleep(sleep)

    def check_message_error_by_status_user(self, driver, status):
        """ Проверка текста сообщения для пользователя в статусе DISABLE.
        :param error_message: текст сообщения, которое нам вернул сервер.
        """
        HelpNavigateCheckMethods.element_is_present(driver, self.SENT_PASSWD % self.LIST_ERROR_FOR_STATUS[status])

    def check_instruction_not_receiver_passwd(self, driver):
        """ Проверка текста со списком инструкций, если пароль не пришел.
        :param driver: ссылка на драйвер
        """

        HelpNavigateCheckMethods.element_is_present(driver, self.CHECK_OBJ_INSTRUCT_NOT_PASSWD % self.CHECK_INSTRUCT_NOT_PASSWD)
        for index in self.LIST_INSTRUCT_NOT_PASSWD:
            HelpNavigateCheckMethods.element_is_present(driver, self.OBJ_NOT_RECEIVER_PASSWD % index)

    def check_sms_status(self, data):
        """
        Проверка статуса доставки смс до внешнего провайдера
        :param data:
        :return:
        """
        msg1 = "Внутренняя ошибка в нашей системе при отправке сообщения"
        self.assertNotEqual(self.SMS_STATUS["INTERNAL_ERROR"], data["status_id"], msg1)
        msg2 = "Новое сообщение - отправки сообщения провайдеру не произошло"
        self.assertNotEqual(self.SMS_STATUS["NEW"], data["status_id"], msg2)
        msg3 = "Сообщение отправлено провайдеру - от провайдера не пришел ответ"
        self.assertNotEqual(self.SMS_STATUS["SENT"], data["status_id"], msg3)
        msg4 = "Сообщение было отправлено провайдеру, но НЕ БЫЛО ПОЛУЧЕНО подтверждение принятия сообщения провайдером"
        self.assertNotEqual(self.SMS_STATUS["NOT_ACKNOWLEDGED"], data["status_id"], msg4)


