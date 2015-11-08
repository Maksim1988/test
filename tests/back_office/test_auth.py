# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
#         	Tests .
#--------------------------------------------------------------------
from ddt import ddt, data

from support import service_log
from support.utils.common_utils import priority
from support.utils.db import databases
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleMethods
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods as FrontAuthCheckMethods
from tests.back_office.class_auth import HelpAuthCheckMethods


__author__ = 'm.senchuk'


@ddt
class TestAuth(HelpLifeCycleMethods, HelpAuthCheckMethods, FrontAuthCheckMethods):
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)
        # Переходим на страницу авторизации бэка
        cls.get_back_page(cls.driver)
        cls.obj_login, cls.obj_pass, cls.obj_submit = cls.get_back_auth_data(cls.driver)

    @priority("medium")
    @data(*HelpAuthCheckMethods.ROLE)
    def test_auth(self, role):
        """ Тест на проверку успешного входа в бек-офис под учеткой админа/модератора и наличие пунктов меню
        :return:
        """
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        self.check_back_login(self.driver)
        self.check_default_page(self.driver)
        self.check_menu_items(self.driver, self.MENU_ITEMS[role])

    @priority("low")
    def test_auth_seller(self):
        """ Тест на проверку не успешного входа в бек-офис под учеткой продавца
        :return:
        """
        self.back_auth('seller', self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        self.check_back_login_failed(self.driver)

    @priority("low")
    def test_auth_buyer(self):
        """ Тест на проверку не успешного входа в бек-офис под учеткой покупателя
        :return:
        """
        self.back_auth('buyer', self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        self.check_back_login_failed(self.driver)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestNavigationMenu(HelpLifeCycleMethods, HelpAuthCheckMethods, FrontAuthCheckMethods):
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)
        # Переходим на страницу авторизации бэка
        cls.get_back_page(cls.driver)
        cls.obj_login, cls.obj_pass, cls.obj_submit = cls.get_back_auth_data(cls.driver)

    @priority("medium")
    @data(*HelpAuthCheckMethods.ROLE)
    def test_menu_navigation(self, role):
        """ Тест на проверку навигации по меню под ролью админа/модератора
        :return:
        """
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        self.check_back_login(self.driver)
        self.check_default_page(self.driver)
        self.MENU_ITEMS[role].reverse()
        for item in self.MENU_ITEMS[role]:
            self.check_navigate(self.driver, self.NAVIGATE_MENU_ITEM[item])

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()