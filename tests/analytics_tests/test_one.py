# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
#         	Тесты на проверку счетчиков аналитики.
#--------------------------------------------------------------------

from ddt import ddt, data

from support import service_log
from support.utils.common_utils import run_on_prod, generate_sha256
from support.utils.db import databases
from support.utils.webserver import start_WebServer, get_response_by_WebServer
from class_analytics import HelpAnalyticsCheckMethods
from tests.front_office.authorization.classes.class_front import HelpAuthMethods
from tests.front_office.class_navigate import HelpNavigateMethods, HelpNavigateCheckMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleMethods, HelpLifeCycleCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods


@ddt
class TestsMainPage(HelpAnalyticsCheckMethods, HelpLifeCycleMethods, HelpAuthMethods):

    driver = None

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

    def test_first_visit_main_page_for_not_auth_user(self):
        """ Проверка главной страницы для не зарегистрированного пользователя.
        Переходим на главную страницу.
        Интегрируем в неё скрипт для перехвата сообщений и отправки их на наш тестовый сервер.
        Получаем ответ и проверяем его.
        """
        service_log.run(self)
        server = start_WebServer()

        self.go_main(self.driver, flag_auth=False)
        self.inclusion_js_script(self.driver)
        output_server = get_response_by_WebServer(server, 1)

        segment_data = self.parsing_segment_data(output_server[0]["body"])
        self.check_first_visit(segment_data=segment_data, page="index")

    @run_on_prod(False)
    @data("buyer", "seller")
    def test_first_visit_login(self, role="seller"):
        """ Проверка авторизации на сайте.
        Переходим на главную страницу. Переходим на страницк авторизации.
        Интегрируем в неё скрипт для перехвата сообщений и отправки их на наш тестовый сервер.
        Авторизуемся под пользователем.
        Получаем ответ и проверяем его.
        """
        service_log.run(self)

        # делаем выборку пользователя и устанавливаем новый пароль для пользователя
        user_id = AccountingMethods.get_default_user_id(role=role)
        user = databases.db1.accounting.get_user_by_account_id(user_id)[0]
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, user["salt"])
        databases.db1.accounting.update_user_password(user["id"], hash_res_new)

        # переходим на страницу авторизации
        HelpAuthMethods.go_authorization_page(self.driver)

        # интегрируем скрипт, запускаем сервер
        self.inclusion_js_script(self.driver)
        server = start_WebServer()

        self.auth_to_website(passwd=default_new_passwd, phone=user["phone"])

        output_server = get_response_by_WebServer(server, 2)
        segment_data1 = self.parsing_segment_data(output_server[0]["body"])
        segment_data2 = self.parsing_segment_data(output_server[1]["body"])
        self.check_login(role=role, segment_data=segment_data1)
        self.check_first_visit_for_auth(segment_data=segment_data2, role=role, page="index")

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class TestsHelpPage(HelpAnalyticsCheckMethods, HelpLifeCycleMethods, HelpAuthMethods):

    def test_visit_auth_user(self):
        """ Посещение страницы авторизованным пользователем.
        :return:
        """
        pass

    def test_visit_anonymous(self):
        """ Посещение страницы не зарегистрированным пользователем.
        :return:
        """
        pass

    def test_anonymous_direct_link(self):
        """ Посещение страницы не зарегистрированным пользователем по прямой ссылке.
        :return:
        """
        pass

    def test_auth_user_direct_link(self):
        """ Посещение страницы авторизованным пользователем по прямой ссылке.
        :return:
        """
        pass


class TestsStorePage(HelpAnalyticsCheckMethods, HelpLifeCycleMethods, HelpAuthMethods):

    def test_visit_auth_user(self):
        """ Посещение страницы авторизованным пользователем.
        :return:
        """
        pass

    def test_visit_anonymous(self):
        """ Посещение страницы не зарегистрированным пользователем.
        :return:
        """
        pass

    def test_anonymous_direct_link(self):
        """ Посещение страницы не зарегистрированным пользователем по прямой ссылке.
        :return:
        """
        pass

    def test_auth_user_direct_link(self):
        """ Посещение страницы авторизованным пользователем по прямой ссылке.
        :return:
        """
        pass


class TestsGoodPage(HelpAnalyticsCheckMethods, HelpLifeCycleMethods, HelpAuthMethods):

    def test_visit_auth_user(self):
        """ Посещение страницы авторизованным пользователем.
        :return:
        """
        pass

    def test_visit_anonymous(self):
        """ Посещение страницы не зарегистрированным пользователем.
        :return:
        """
        pass

    def test_anonymous_direct_link(self):
        """ Посещение страницы не зарегистрированным пользователем по прямой ссылке.
        :return:
        """
        pass

    def test_auth_user_direct_link(self):
        """ Посещение страницы авторизованным пользователем по прямой ссылке.
        :return:
        """
        pass


class TestsLogin(HelpAnalyticsCheckMethods, HelpLifeCycleMethods, HelpAuthMethods):

    def test_success_login(self):
        """ Успешная авторизация.
        :return:
        """
        pass

    def test_fail_login(self):
        """ Авторизация провалилась.
        :return:
        """
        pass


class TestsLogout(HelpAnalyticsCheckMethods, HelpLifeCycleMethods, HelpAuthMethods):

    def test_success_logout(self):
        """ Успешное разлогинивание.
        :return:
        """
        pass


class TestsRegistration(HelpAnalyticsCheckMethods, HelpLifeCycleMethods, HelpAuthMethods):

    def test_success_reg(self):
        """ Успешная регистрация пользователя.
        :return:
        """
        pass

    def test_fail_reg(self):
        """ Регистрация пользователя провалилась.
        :return:
        """
        pass


class TestsMessage(HelpAnalyticsCheckMethods, HelpLifeCycleMethods, HelpAuthMethods):

    def test_simple_txt_msg(self):
        """ Отправка простого текстового сообщения пользователем.
        :return:
        """
        pass


class TestsChatPage(HelpAnalyticsCheckMethods, HelpLifeCycleMethods, HelpAuthMethods):

    def test_visit_user(self):
        """ Посещение чата авторизованным пользователем.
        :return:
        """
        pass

    def test_visit_user_direct_link(self):
        """ Посещение чата авторизованным пользователем по прямой ссылке.
        :return:
        """
        pass


@ddt
class TestsSearch(HelpAnalyticsCheckMethods, HelpLifeCycleMethods, HelpAuthMethods):

    driver = None

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)

    def test_search_not_auth_user(self):
        """ Проверка поиска по сайту, не авторизованным пользователем.
        Ищем заданного пользователя по сайту.
        Свяеряем поисковый запрос и запрос на страницу поиска.
        """
        service_log.run(self)

        # Берем тестового продавца на магазине которого будут проводиться проверки
        default_test_seller_id = AccountingMethods.get_default_user_id(role='seller')
        user = databases.db1.accounting.get_user_by_account_id(default_test_seller_id)[0]

        # Переходим на главную страницу и получаем инпут поиска и кнопку поиска
        self.go_main(self.driver, flag_auth=False)
        input_search = HelpNavigateMethods.get_element_navigate(self.driver, HelpNavigateMethods.input_main.SEARCH)
        btn_search = HelpNavigateMethods.get_element_navigate(self.driver, HelpNavigateMethods.click_main.BTN_SEARCH)

        # Вводим имя продавца и жмем кнопку поиска
        query = user["display_name"].decode('utf-8')
        input_search.send_keys(query)

        # интегрируем скрипт, запускаем сервер
        self.inclusion_js_script(self.driver)
        server = start_WebServer()

        # нажимаем кнопку поиска
        btn_search.click()

        # получаем ответ и проверяем данные счетчиков
        output_server = get_response_by_WebServer(server, 2)
        segment_data_query = self.parsing_segment_data(output_server[0]["body"])
        segment_data_visit = self.parsing_segment_data(output_server[1]["body"])
        self.check_search_query(segment_data=segment_data_query, query=query)
        self.check_search_result(segment_data=segment_data_visit, query=query)

    @run_on_prod(False)
    def test_search_auth_user(self):
        """ Проверка поиска по сайту, авторизованным пользователем.
        Ищем заданного пользователя по сайту.
        Свяеряем поисковый запрос и запрос на страницу поиска.
        """
        service_log.run(self)

        # делаем выборку пользователя и устанавливаем новый пароль для пользователя
        user_id = AccountingMethods.get_default_user_id(role="buyer")
        user = databases.db1.accounting.get_user_by_account_id(user_id)[0]
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, user["salt"])
        databases.db1.accounting.update_user_password(user["id"], hash_res_new)

        self.go_main(self.driver, phone=user["phone"], passwd=default_new_passwd, flag_auth=True)

        # вводим строку для поиска
        input_search = HelpNavigateMethods.get_element_navigate(self.driver, HelpNavigateMethods.input_main.SEARCH)
        btn_search = HelpNavigateMethods.get_element_navigate(self.driver, HelpNavigateMethods.click_main.BTN_SEARCH)
        query = user["display_name"].decode('utf-8')
        input_search.send_keys(query)

        # интегрируем скрипт, запускаем сервер
        self.inclusion_js_script(self.driver)
        server = start_WebServer()

        # нажимаем кнопку поиска
        btn_search.click()

        # получаем ответ и проверяем данные счетчиков
        output_server = get_response_by_WebServer(server, 2)
        segment_data_query = self.parsing_segment_data(output_server[0]["body"])
        segment_data_visit = self.parsing_segment_data(output_server[1]["body"])
        self.check_search_query(segment_data=segment_data_query, query=query, role=u'registered')
        self.check_search_result(segment_data=segment_data_visit, query=query, role=u'registered')

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class AnalyticsScriptsInPage(HelpNavigateCheckMethods, HelpAnalyticsCheckMethods):

    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        service_log.preparing_env(cls)

    def test_page_as_bot(self):
        """
        Открыть страницу, как бот, отсутствие аналитики сегмента и яндеска
        :return:
        """
        AnalyticsScriptsInPage.driver = HelpLifeCycleCheckMethods.get_firefox_driver(manual_user_agent=True)
        self.get_page(self.driver)
        self.element_is_present(self.driver, self.check_main.MAIN_MENU_HOME_ACTIVE)
        source = self.driver.page_source.encode('utf-8')
        self.check_analytics_as_bot(source)

    def test_page_as_user(self):
        """
        Открыть страницу, как обычный пользователь, наличие аналитики сегмента и яндеска
        :return:
        """
        AnalyticsScriptsInPage.driver = HelpLifeCycleCheckMethods.get_firefox_driver(manual_user_agent=False)
        self.get_page(self.driver)
        self.element_is_present(self.driver, self.check_main.MAIN_MENU_HOME_ACTIVE)
        source = self.driver.page_source.encode('utf-8')
        self.check_analytics_as_user(source)

    @classmethod
    def tearDown(cls):
        AnalyticsScriptsInPage.driver.quit()
        service_log.end()