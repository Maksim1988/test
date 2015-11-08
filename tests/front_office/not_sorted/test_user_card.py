# -*- coding: utf-8 -*-
"""
Feature: Карточка пользователя на сайте
Description: Набор тестов для проверки карточек пользователя на сайте
"""
import time
from unittest import skip

from ddt import ddt, data

from support import service_log
from support.utils import common_utils
from tests.worker_accounting.class_favorites import FavoritesCheckMethods as Favorite
from support.utils.common_utils import generate_sha256, priority
from support.utils.db import databases
from support.utils.thrift4req import services
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateData as HND
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods
from tests.front_office.not_sorted.classes.class_user_card import HelpUserCardCheckMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods
from tests.front_office.settings.classes.class_profile_settings import HelpProfileSettingsCheckMethods as Settings
__author__ = 'm.senchuk'


class TestGoodPageUserCard(HelpUserCardCheckMethods, HelpAuthCheckMethods, HND):
    """
    Story: Карточка пользователя на странице товара
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

        # Берем тестового продавца на магазине которого будут проводиться проверки
        cls.default_test_seller_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                                 criteria='id=%s' % cls.default_test_seller_id)[0]
        cls.shop = databases.db1.accounting.get_shop_details_by_shop_id(cls.user["shop_id"])[0]

    @priority("medium")
    def test_seller_card_for_visitor(self, test_good=HND.SHP_TO_GOOD):
        """
        Title: Проверка карточки магазина на странице товара для посетителя
        """
        # Переход на страницу магазина
        self.get_page(self.driver, HND.path_shop.URL_SHOP % self.default_test_seller_id)
        self.check_navigate_in_good_page(self.driver, test_good, 1)
        self.check_shop_card_in_good_page(self.driver, self.shop, self.user["id"])

    @priority("medium")
    def test_seller_card_for_seller(self, test_good=HND.SHP_TO_GOOD):
        """
        Title: Проверка карточки магазина на странице товара для продавца своего товара
        """
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_auth=True)

        # Переход на страницу магазина
        self.get_page(self.driver, HND.path_shop.URL_SHOP % self.default_test_seller_id)
        self.check_navigate_in_good_page(self.driver, test_good, 1)
        self.user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                                  criteria='id=%s' % self.default_test_seller_id)[0]
        self.check_shop_card_in_good_page_for_seller(self.driver, self.shop, self.user["id"])

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class TestShopPageUserCard(HelpUserCardCheckMethods, HelpAuthCheckMethods, HND):
    """
    Story: Карточка пользователя на странице магазина
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

        # Берем тестового продавца на магазине которого будут проводиться проверки
        cls.default_test_seller_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                                 criteria='id=%s' % cls.default_test_seller_id)[0]

    @priority("medium")
    def test_seller_card_for_visitor(self):
        """
        Title: Проверка карточки продавца на странице магазина для посетителя
        """
        # Переход на страницу магазина
        self.get_page(self.driver, self.path_shop.URL_SHOP % self.default_test_seller_id)
        self.check_user_card_in_shop_page(self.driver, self.user)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class TestSearchPageUserCard(HelpUserCardCheckMethods, HelpAuthCheckMethods, HND):
    """
    Story: Карточка пользователя на странице поиска
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

        # Берем тестового продавца на магазине которого будут проводиться проверки
        cls.default_test_id = AccountingMethods.get_default_user_id(role='seller')
        cls.default_new_password = AccountingMethods.get_default_password()
        cls.user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                                 criteria='id=%s' % cls.default_test_id)[0]

    @priority("medium")
    def test_seller_card_for_visitor(self):
        """
        Title: Проверка карточки продавца на странице поиска для посетителя
        """
        self.go_main(self.driver, phone=self.user["phone"], passwd=self.default_new_password, flag_auth=True)
        self.get_page(self.driver, self.path_settings.PATH_PROFILE_SETTINGS)
        profile = Settings.get_user_profile_form(self.driver, self.user)
        Settings.clear_input_row(self.driver, profile["name_input"])
        new_name = common_utils.random_string()
        profile["name_input"].send_keys(new_name)
        self.element_click(self.driver, profile["save_btn"], change_page_url=False)
        time.sleep(self.timeout)
        self.driver.delete_all_cookies()
        self.go_to_main_page(self.driver)
        u_user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                             criteria='id=%s' % self.default_test_id)[0]
        self.search_user(self.driver, u_user['display_name'])
        self.check_user_card_in_search_page(self.driver, u_user)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()

   #14.06.2015 все пользователи стали продавцами
@ddt
class TestBuyerPageUserCard(HelpUserCardCheckMethods, HelpAuthCheckMethods, HND):
    """
    Story: Карточка пользователя на странице пользователя
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('low')
    def test_user_card_for_visitor(self, user_role='buyer'):
        """
        Title: Проверка карточки покупателя на странице покупателя для посетителя
        """
        self.default_user_id = AccountingMethods.get_default_user_id(role=user_role)
        self.user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                                  criteria='id=%s' % self.default_user_id)[0]
        self.get_page(self.driver, path_url=self.path_buyer.URL_BUYER % self.user["id"])
        self.check_user_card_in_buyer_page(self.driver, self.user)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestMainPageUserCard(HelpUserCardCheckMethods, HelpAuthCheckMethods, HND):
    """
    Story: Карточка пользователя на главной странице
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority('low')
    @data(*range(1, 2))
    def test_user_card_in_good(self, num_lot):
        """
        Title: Проверка карточки продавца на главной странице в лоте товара для посетителя
        """
        self.go_lot_user(self.driver, num_lot)
        url = self.get_current_url(self.driver)
        user_id = url[url.rfind("/")+1:]
        self.user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                                  criteria="id='%s'" % user_id)[0]
        self.go_to_main_page(self.driver)
        self.check_user_card_in_lot_main_page(self.driver, self.user, num_lot)

    @priority("medium")
    def test_user_card_seller(self):
        """
        Title: Виджет "Профиль пользователя" - продавец
        """
        # Берем тестового продавца на магазине которого будут проводиться проверки
        self.default_test_seller_id = AccountingMethods.get_default_user_id(role='seller')
        self.user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                                 criteria='id=%s' % self.default_test_seller_id)[0]
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_auth=True)
        time.sleep(5)
        self.move_to_elem(self.driver, self.path_main.WIDGET_USER)
        self.check_user_card_in_widget_seller(self.driver, self.user)

    @priority("medium")
    def test_user_card_buyer(self):
        """
        Title: Виджет "Профиль пользователя" - покупатель
        """
        # Берем тестового окупателя на магазине которого будут проводиться проверки
        self.default_test_seller_id = AccountingMethods.get_default_user_id(role='buyer')
        self.user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                                 criteria='id=%s' % self.default_test_seller_id)[0]
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_auth=True)
        time.sleep(5)
        self.move_to_elem(self.driver, self.path_main.WIDGET_USER)
        self.check_user_card_in_widget_buyer(self.driver, self.user)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class TestFavoritesPageUserCard(HelpUserCardCheckMethods, HelpAuthCheckMethods, HND):
    """
    Story: Карточка пользователя на странице Избранные товары
    """
    driver = None

    @staticmethod
    def set_fav_wares(user_id, fav_wares):
        """ Очистить избранные товары пользователя, если таковые имеются.
        :param user_id: идентификатор пользователя
        :param fav_type: тип избранного
        :param wares: список идентификаторов товаров
        """
        if fav_wares is None:
            wares = databases.db0.warehouse.get_wares_with_limit(limit=5)
            ware_ids = [index["ware_id"] for index in wares]
            dto_list = Favorite.generate_dto_list_equal_fav_ware(user_id, ware_ids)
            param = Favorite.get_FavoritesAddRequest(dto_list)
            services.favorites.root.tframed.addFavorites(param)

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

        # Берем тестового продавца на магазине которого будут проводиться проверки
        cls.default_test_seller_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                                 criteria='id=%s' % cls.default_test_seller_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)

    @skip('update')
    @priority("medium")
    def test_user_card_favorites_goods_seller(self, num_lot=1):
        """
        Title: Проверка карточки продавца на странице Избранное товары для продавца
        """
        fav_wares = databases.db5.favorites.get_fav_wares_by_user_id(self.user['id'])
        self.set_fav_wares(self.user['id'], fav_wares)
        self.get_page(self.driver, self.path_favorites.URL_FAVORITES_GOODS)
        self.go_favorites_to_user(self.driver, num_lot, self.path_favorites.PATH_FG_USERS)
        url = self.get_current_url(self.driver)
        user_id = url[url.rfind("/")+1:]
        self.user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                                  criteria="id='%s'" % user_id)[0]
        self.get_page(self.driver, self.path_favorites.URL_FAVORITES_GOODS)
        self.check_user_card_in_favorite_goods_page(self.driver, self.user, num_lot)

    @priority("medium")
    def test_user_card_favorites_users_seller(self, num_lot=1):
        """
        Title: Проверка карточки продавца на странице Избранное пользователи/Контакты для продавца
        """
        self.get_page(self.driver, self.path_favorites.URL_FAVORITES_USERS)
        list_user_id = self.get_category_id_from_page_source(self.driver, self.path_user_contact.TO_FIND_USER_ID_START,
                                                             self.path_user_contact.TO_FIND_USER_ID_END, 1)
        #url = self.get_current_url(self.driver)
        user_id = list_user_id[0]
        self.user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                                  criteria="id='%s'" % user_id)[0]
        #self.get_page(self.driver, self.path_favorites.URL_FAVORITES_USERS)
        self.check_user_card_in_favorite_users_page(self.driver, self.user, num_lot)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class TestChatPageUserCard(HelpUserCardCheckMethods, HelpAuthCheckMethods, HND):
    """
    Story: Карточка пользователя в чате
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

        # Берем тестового продавца на магазине которого будут проводиться проверки
        cls.default_test_seller_id = AccountingMethods.get_default_user_id(role='seller_alien')
        cls.user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                                 criteria='id=%s' % cls.default_test_seller_id)[0]
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)

    @priority("medium")
    def test_user_card_chats_seller(self, num_lot=1):
        """
        Title: Проверка карточки продавца на странице чаты для продавца
        """
        self.get_page(self.driver, self.path_chat.URL_CHAT)
        time.sleep(HelpNavigateCheckMethods.time_sleep)
        url = self.get_current_url(self.driver)
        user_id = url[url.rfind("/")+1:]
        self.user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                                  criteria="id='%s'" % user_id)[0]
        self.get_page(self.driver, self.path_chat.URL_CHAT)
        self.check_user_card_in_chat_page(self.driver, self.user, num_lot)

    @skip('deprecated')
    @priority('low')
    def test_user_card_deals_seller(self, num_lot=1):
        """
        Title: Проверка карточки продавца на странице Сделки для продавца
        """
        self.get_page(self.driver, self.path_chat.URL_CHAT)
        self.click_and_transition_to_page(self.driver, self.path_chat.PATH_CHAT_USER_CARD % num_lot)
        self.click_and_transition_to_page(self.driver, self.path_chat.PATH_DEAL_USER_CARD)
        url = self.get_current_url(self.driver)
        user_id = url[url.rfind("/")+1:]
        self.user = databases.db1.accounting.get_user_by_criteria(account_status='ENABLED',
                                                                  criteria="id='%s'" % user_id)[0]
        self.get_page(self.driver, self.path_chat.URL_CHAT)
        self.click_and_transition_to_page(self.driver, self.path_chat.PATH_CHAT_USER_CARD % num_lot)
        self.check_user_card_in_deal_page(self.driver, self.user)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()