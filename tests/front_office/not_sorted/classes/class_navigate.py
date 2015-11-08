# -*- coding: utf-8 -*-
import time
from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException, StaleElementReferenceException, \
    WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
from support import service_log
from tests.MainClass import MainClass
from selenium.webdriver.common.action_chains import ActionChains
from tests.front_office.data_navigation import MyGoodsPage, ShopPage, ProfileSettingsPage, SearchPage, BackAuthPage
from tests.front_office.data_navigation import HelpPage, OorraaNetPage, AboutPage, GoodPage, ChatPage, FavoritePage
from tests.front_office.data_navigation import MainPage, AuthorizationPage, RegistrationPage, CatalogCategoryPage
from tests.front_office.data_navigation import BackWaresPage, BackLoadWaresPage, BackUsersPage, BackInvitesPage
from tests.front_office.data_navigation import BackCmsWaresPage, ContactsPage, UserContactsPage, BuyerPage, RestorePage
from tests.front_office.data_navigation import DeliveryPage, PaymentsPage

__author__ = 'm.senchuk'


class HelpNavigateData(MainClass, ActionChains):

    timeout = 2
    email_timeout = 120
    time_sleep = 5

    click_auth = AuthorizationPage.Click
    click_reg = RegistrationPage.Click
    click_favorites = FavoritePage.Click
    click_chat = ChatPage.Click
    click_main = MainPage.Click
    click_catalog = CatalogCategoryPage.Click
    click_my_goods = MyGoodsPage.Click
    click_good = GoodPage.Click
    click_help = HelpPage.Click
    click_shop = ShopPage.Click
    click_favorite = FavoritePage.Click
    click_search = SearchPage.Click
    click_back_auth = BackAuthPage.Click
    click_back_wares = BackWaresPage.Click
    click_back_load_wares = BackLoadWaresPage.Click
    click_back_users = BackUsersPage.Click
    click_back_invites_wares = BackInvitesPage.Click
    click_back_cms_wares_wares = BackCmsWaresPage.Click
    click_contacts = ContactsPage.Click
    click_user_contact = UserContactsPage.Click
    click_settings = ProfileSettingsPage.Click
    click_restore = RestorePage.Click

    check_auth = AuthorizationPage.Check
    check_reg = RegistrationPage.Check
    check_catalog = CatalogCategoryPage.Check
    check_help = HelpPage.Check
    check_oorraa_net = OorraaNetPage.Check
    check_delivery = DeliveryPage.Check
    check_payments = PaymentsPage.Check
    check_about = AboutPage.Check
    check_good = GoodPage.Check
    check_chat = ChatPage.Check
    check_favorite = FavoritePage.Check
    check_my_goods = MyGoodsPage.Check
    check_shop = ShopPage.Check
    check_main = MainPage.Check
    check_settings = ProfileSettingsPage.Check
    check_search = SearchPage.Check
    check_back_auth = BackAuthPage.Check
    check_back_wares = BackWaresPage.Check
    check_back_load_wares = BackLoadWaresPage.Check
    check_back_users = BackUsersPage.Check
    check_back_invites_wares = BackInvitesPage.Check
    check_back_cms_wares_wares = BackCmsWaresPage.Check
    check_contacts = ContactsPage.Check
    check_user_contact = UserContactsPage.Check
    check_buyer = BuyerPage.Check
    check_favorites = FavoritePage.Check
    check_restore = RestorePage.Check

    input_auth = AuthorizationPage.Input
    input_reg = RegistrationPage.Input
    input_chat = ChatPage.Input
    input_good = GoodPage.Input
    input_main = MainPage.Input
    input_settings = ProfileSettingsPage.Input
    input_my_goods = MyGoodsPage.Input
    input_contacts = ContactsPage.Input
    input_back_auth = BackAuthPage.Input
    input_back_wares = BackWaresPage.Input
    input_back_load_wares = BackLoadWaresPage.Input
    input_back_users = BackUsersPage.Input
    input_back_invites_wares = BackInvitesPage.Input
    input_back_cms_wares_wares = BackCmsWaresPage.Input
    input_user_contact = UserContactsPage.Input
    input_restore = RestorePage.Input

    path_main = MainPage.Path
    path_auth = AuthorizationPage.Path
    path_reg = RegistrationPage.Path
    path_my_goods = MyGoodsPage.Path
    path_help = HelpPage.Path
    path_category = CatalogCategoryPage.Path
    path_shop = ShopPage.Path
    path_favorites = FavoritePage.Path
    path_search = SearchPage.Path
    path_settings = ProfileSettingsPage.Path
    path_good = GoodPage.Path
    path_contacts = ContactsPage.Path
    path_restore = RestorePage.Path
    path_back_auth = BackAuthPage.Path
    path_back_wares = BackWaresPage.Path
    path_back_load_wares = BackLoadWaresPage.Path
    path_back_users = BackUsersPage.Path
    path_back_invites_wares = BackInvitesPage.Path
    path_back_cms_wares_wares = BackCmsWaresPage.Path
    path_user_contact = UserContactsPage.Path
    path_buyer = BuyerPage.Path
    path_chat = ChatPage.Path

    MAIN_TO_AUTH = dict(start_click=click_main.BUTTON_LOGIN, finish_page=check_auth.TITLE_AUTH_PAGE)
    MAIN_TO_REG = dict(start_click=click_main.REGISTRATION_PAGE2, finish_page=check_reg.TITLE_REGISTRATION_PAGE)
    MAIN_TO_CHAT = dict(start_click=click_main.HEADER_WIDGET_CHATS, finish_page=check_chat.TITLE_CHAT)
    MAIN_TO_FAVORITE = dict(start_click=click_main.HEADER_FAVORITES, finish_page=check_favorite.TITLE_FAVORITE)
    MAIN_MY_GOODS = dict(start_click=click_main.HEADER_MY_GOODS, finish_page=check_my_goods.TITLE_MY_GOODS)

    # MCR ~ MAIN TO CATEGORY ROOT
    MCR_GARMENT = dict(start_click=click_main.CM_GARMENT, finish_page=click_catalog.LRC_GARMENT)
    MCR_SHOES = dict(start_click=click_main.CM_SHOES, finish_page=click_catalog.LRC_SHOES)
    MCR_UNDERWEAR = dict(start_click=click_main.CM_UNDERWEAR, finish_page=click_catalog.LRC_UNDERWEAR)
    MCR_ACCESSORY = dict(start_click=click_main.CM_ACCESSORY, finish_page=click_catalog.LRC_ACCESSORY)
    MCR_TEXTILE = dict(start_click=click_main.CM_TEXTILE, finish_page=click_catalog.LRC_TEXTILE)
    MCR_CHILD = dict(start_click=click_main.CM_CHILD, finish_page=click_catalog.LRC_CHILD)

    # MB - MAIN BANNER
    MB_VIDEO = dict(start_click=click_main.MBV_VIDEO, finish_page=check_help.TITLE_VIDEO)
    MB_START_SALE = dict(start_click=click_main.MBV_START_SALE, finish_page=check_reg.TITLE_REGISTRATION_PAGE)
    MB_HOW_JOB = dict(start_click=click_main.MBV_HOW_JOB, finish_page=check_help.TITLE_FAQ)
    MB_COLLECTION = dict(start_click=click_main.MBB_COLLECTION, finish_page=check_catalog.FC_JACKET)
    MB_ADD_GOOD = dict(start_click=click_main.MBS_ADD_GOOD, finish_page=check_my_goods.TITLE_ADD_GOOD)
    MB_CREATE_SITE = dict(start_click=click_main.MBS_CREATE_SITE, finish_page=check_help.TITLE_SELLER_PAGE)

    MB_NEW_GARMENT = dict(start_click=click_main.MBV_NEW_GARMENT, finish_page=check_catalog.FC_COATS)
    MB_FOR_CHILD = dict(start_click=click_main.MBV_FOR_CHILD, finish_page=click_catalog.LRC_CHILD)
    MB_NEW_FOOTWEAR = dict(start_click=click_main.MBV_NEW_FOOTWEAR, finish_page=click_catalog.LRC_SHOES)

    # MSC - MAIN TO SPECIAL CATEGORY
    MSC_LAST_DEALS = dict(start_click=click_main.TB_LAST_DEALS, finish_page=check_catalog.TCS_LAST_DEALS)
    MSC_NEW_GOODS = dict(start_click=click_main.TB_NEW_GOODS, finish_page=check_catalog.TCS_NEW_GOODS)
    MSC_POPULAR_GOODS = dict(start_click=click_main.TB_POPULAR_GOODS, finish_page=check_catalog.TCS_POPULAR_GOODS)
    MSC_GOODS_BEST_SELLERS = dict(start_click=click_main.TB_GOODS_BEST_SELLERS,
                                  finish_page=check_catalog.TCS_GOODS_BEST_SELLERS)

    # MB ~ MAIN TO BANNER RIGHT
    MB_SUBSCRIBE = dict(start_click=click_main.BR_SUBSCRIBE, finish_page=check_help.TITLE_SUBSCRIBE)
    MB_AVAIL_SERVICE = dict(start_click=click_main.BR_TRADE_ALL, finish_page=check_help.TITLE_AVAIL_SERVICE)
    MB_SOME_STORE = dict(start_click=click_main.BR_SOME_STORE, finish_page=click_catalog.FC_CLOTHING)
    MB_TAKE_SELLER = dict(start_click=click_main.BR_TAKE_SELLER, finish_page=check_help.TITLE_TAKE_SELLER)
    MB_FAVORITES = dict(start_click=click_main.BR_FAVORITES, finish_page=check_help.TITLE_FAVORITES)
    MB_SELL_ALL = dict(start_click=click_main.BR_SELL_ALL, finish_page=check_help.TITLE_AVAIL_SERVICE)
    MB_START_SELL = dict(start_click=click_main.BR_START_SELL, finish_page=check_my_goods.TITLE_ADD_GOOD)
    MB_START_SELL_VISITOR = dict(start_click=click_main.BR_START_SELL, finish_page=check_auth.TITLE_AUTH_PAGE)
    MB_IN_CENTER = dict(start_click=click_main.BR_IN_CENTER, finish_page=check_help.TITLE_FILL_PROFILE)

    # MBW ~ MAIN TO BANNER WIDTH
    MBW_MAN_ACCESS = dict(start_click=click_main.BW_MAN_ACCESS, finish_page=check_catalog.FC_BAGS)
    MBW_CATALOG_DRESS = dict(start_click=click_main.BW_CATALOG_DRESS, finish_page=check_catalog.FC_DRESS)
    MBW_AUTUMN = dict(start_click=click_main.BW_AUTUMN, finish_page=check_catalog.FC_JACKET)

    MBW_TEXTILE = dict(start_click=click_main.BW_TEXTILE, finish_page=click_catalog.LRC_TEXTILE)

    # MFB ~ MAIN TO FOOTER BUTTON
    MFB_GARMENT = dict(start_click=click_main.FB_GARMENT, finish_page=click_catalog.LRC_GARMENT)
    MFB_SHOES_AND_ACCESSORY = dict(start_click=click_main.FB_SHOES_AND_ACCESSORY, finish_page=click_catalog.LRC_SHOES_AND_ACCESSORY)
    MFB_CHILD = dict(start_click=click_main.FB_CHILD, finish_page=click_catalog.LRC_CHILD)
    MFB_HOUSE = dict(start_click=click_main.FB_HOUSE, finish_page= click_catalog.LRC_HOUSE)
    MFB_GARDEN = dict(start_click=click_main.FB_GARDEN, finish_page=click_catalog.LRC_GARDEN) 
    MFB_TRADE_EQUIPMENT = dict(start_click=click_main.FB_TRADE_EQUIPMENT, finish_page=click_catalog.LRC_TRADE_EQUIPMENT)

    MFB_TEXTILE = dict(start_click=click_main.FB_TEXTILE, finish_page=click_catalog.LRC_TEXTILE)
    
    MFB_ABOUT_COMPANY = dict(start_click=click_main.FB_ABOUT_COMPANY, finish_page=check_help.TITLE_ABOUT_COMPANY)
    MFB_JOB = dict(start_click=click_main.FB_JOB, finish_page=check_oorraa_net.TITLE_JOB)
    MFB_CONTACTS = dict(start_click=click_main.FB_CONTACTS, finish_page=check_contacts.TITLE_CONTACTS)
    MFB_FAQ = dict(start_click=click_main.FB_FAQ, finish_page=check_help.TITLE_HOW_REG)
    MFB_RULES = dict(start_click=click_main.FB_RULES, finish_page=check_help.TITLE_RULES)
    MFB_CONFIDENTIAL = dict(start_click=click_main.FB_CONFIDENTIAL, finish_page=check_help.TITLE_CONFIDENTIAL)
    MFB_DELIVERY = dict(start_click=click_main.FB_DELIVERY, finish_page=check_delivery.FIRST_VISIT_MSG)
    MFB_PAYMENTS = dict(start_click=click_main.FB_PAYMENTS, finish_page=check_payments.TITLE_MAIN)

    # Блоки с товарами на главной
    MAIN_LAST_DEALS_TO_GOOD = dict(start_xpath_good=path_main.BLOCK_LAST_DEALS + click_main.PATH_GOOD,
                                   finish_xpath_good=check_good.TITLE_GOOD)
    MAIN_GOOD_BEST_SELLERS_TO_GOOD = dict(start_xpath_good=path_main.BLOCK_GOOD_BEST_SELLERS + click_main.PATH_GOOD,
                                          finish_xpath_good=check_good.TITLE_GOOD)
    MAIN_NAME_BEST_SELLERS_TO_SHOP = dict(start_xpath_good=path_main.BLOCK_GOOD_BEST_SELLERS + click_main.PATH_NAME_BS,
                                          finish_xpath_good=check_shop.NAME_SELLER)
    MAIN_NEW_GOOD_TO_GOOD = dict(start_xpath_good=path_main.BLOCK_NEW_GOOD + click_main.PATH_GOOD,
                                 finish_xpath_good=check_good.TITLE_GOOD)
    MAIN_POPULAR_GOOD_TO_GOOD = dict(start_xpath_good=path_main.BLOCK_POPULAR_GOOD + click_main.PATH_GOOD,
                                     finish_xpath_good=check_good.TITLE_GOOD)

    CATALOG_TO_GOOD = dict(start_xpath_good=click_catalog.PATH_GOOD, finish_xpath_good=check_good.TITLE_GOOD)

    # MG ~ MY GOODS PAGE
    MG_TO_ADD_GOOD_PAGE = dict(start_click=click_my_goods.BUTTON_ADD_GOOD, finish_page=check_my_goods.TITLE_ADD_GOOD)
    MG_TO_DIT_GOOD_PAGE = dict(start_click=click_my_goods.BUTTON_EDIT, finish_page=check_my_goods.TITLE_EDIT_GOOD)


    # HP ~ HELP PAGE
    HP_HOW_BUY_REG = dict(start_click=click_help.BTN_HOW_BUY_REG, finish_page=check_reg.TITLE_REGISTRATION_PAGE)
    HP_BE_SELLER = dict(start_click=click_help.BTN_HOW_BE_SELLER_REG, finish_page=check_reg.TITLE_REGISTRATION_PAGE)

    # Тест данные для проверки переходов с главной странице для посетителя.
    SUITE_MAIN_HEADER = [MAIN_TO_AUTH,
                         MAIN_TO_REG]

    SUITE_MAIN_BANNER_V = [MB_NEW_GARMENT,
                           MB_FOR_CHILD,
                           MB_NEW_FOOTWEAR]

    SUITE_MAIN_ROOT_CATEGORY = [MCR_GARMENT,
                                MCR_SHOES,
                                MCR_UNDERWEAR,
                                MCR_ACCESSORY,
                                MCR_TEXTILE,
                                MCR_CHILD]

    SUITE_MAIN_SPECIAL_CATEGORY = [MSC_LAST_DEALS,
                                   MSC_GOODS_BEST_SELLERS,
                                   MSC_NEW_GOODS,
                                   MSC_POPULAR_GOODS]

    SUITE_MAIN_BANNER_RIGHT = [MB_START_SELL_VISITOR,
                               MB_TAKE_SELLER,
                               MB_FAVORITES,
                               MB_IN_CENTER]

    SUITE_MAIN_BANNER_WIDTH = [MBW_MAN_ACCESS,
                               MBW_CATALOG_DRESS,
                               MBW_TEXTILE]

    SUITE_MAIN_FOOTER_CATALOG = [MFB_GARMENT,
                                 MFB_SHOES_AND_ACCESSORY,
                                 MFB_CHILD,
                                 MFB_HOUSE,
                                 MFB_GARDEN,
                                 MFB_TRADE_EQUIPMENT]

    SUITE_MAIN_FOOTER_COMPANY = [MFB_ABOUT_COMPANY,
                                 MFB_CONTACTS]

    SUITE_MAIN_FOOTER_COMPANY_NEW_WINDOW = [MFB_JOB]

    SUITE_MAIN_FOOTER_SUPPORT = [MFB_FAQ,
                                 MFB_RULES,
                                 MFB_CONFIDENTIAL]

    SUITE_MAIN_FOOTER_SUPPORT_NEW_WINDOW = [MFB_DELIVERY,
                                            MFB_PAYMENTS]

    SUITE_MAIN_FOOTER_NEW_WINDOW = [MFB_JOB]

    # Тест данные для проверки переходов с главной страницы для покупателя.
    # B ~ BUYER
    B_SUITE_MAIN_HEADER = [MAIN_TO_CHAT,
                           MAIN_TO_FAVORITE]

    SUITE_MAIN_BANNER_B = [MB_VIDEO,
                           MB_HOW_JOB,
                           MB_COLLECTION]

    SUITE_MAIN_BANNER_RIGHT_B = [MB_SUBSCRIBE,
                                 MB_TAKE_SELLER,
                                 MB_FAVORITES,
                                 MB_SOME_STORE]


    # Тест данные для проверки переходов с главной страницы для продавца.
    SELLER_SPECIAL_CATEGORY = [MSC_LAST_DEALS,
                               MSC_NEW_GOODS,
                               MSC_POPULAR_GOODS]

    SELLER_BANNER_RIGHT = [MB_START_SELL,
                           MB_SELL_ALL,
                           MB_IN_CENTER]

    SELLER_MAIN_HEADER = [MAIN_TO_CHAT,
                          MAIN_TO_FAVORITE,
                          MAIN_MY_GOODS]

    SUITE_MAIN_BANNER_S = [MB_VIDEO,
                           MB_ADD_GOOD,
                           MB_CREATE_SITE]

    # Тест данные для проверки перехода с страницы Мои товары на добавление товара и редактирование товара
    # MG ~ MY GOODS
    SUITE_ADD_EDIT = [MG_TO_ADD_GOOD_PAGE,
                      MG_TO_DIT_GOOD_PAGE]

    # Тест данные для проверки перехода с страницы Мои товары на страницу товара
    # MG ~ MY GOODS
    MG_TO_GOOD = dict(start_xpath_good=click_my_goods.NAME_CARD_GOOD, finish_xpath_good=check_good.TITLE_GOOD)
    MG_GOOD = dict(check_1=check_good.NOTIFY_MY_GOOD, check_2=click_good.NOTIFY_MY_GOOD_EDIT)

    # Тест проверяет переход по кнопкам со страниц поиска "Как покупать на уурраа!" для продавца и покупателя
    HELP_PAGE_GO_SUITE = dict(start_click=click_help.BTN_GO_CATALOG, finish_page=check_catalog.TITLE_ALL_CATALOG)

    # Тест проверяет переход по кнопкам со страниц поиска "Как покупать на уурраа!" для посетителя
    HELP_PAGE_VISITOR_SUITE = [HELP_PAGE_GO_SUITE,
                               HP_HOW_BUY_REG]

    # Тест данные для проверки дерева категорий в каждой рутовой категории.
    ROOT_CATEGORY_SUITE = ['576', '670', '251', '433', '498', '553']

    # Тест данные для проверки витрин Все товары и Бестселлеры в рутовой категории
    WINDOW_CATEGORY_SUITE = [{'category_id': '2', 'window_category': 'Все товары'},
                             {'category_id': '2', 'window_category': 'Бестселлеры'}]

    # Тест данные для проверки кнопки Сообщение для посетителя на странице магазина тестового продавца.
    SHOP_TO_CHAT_VISITOR = dict(start_click=click_shop.CHAT_BUTTON, finish_page=check_auth.TITLE_AUTH_PAGE)

    CHAT_BUTTON_SELLER = dict(xpath=click_shop.CHAT_BUTTON, err_msg="ОШИБКА: Кнопка есть на странице магазина под "
                                                                    "ролью продавец-свой магазин")
    EMPTY_SHOP_ADDRESS_CASE = dict(xpath=check_shop.INFO_ADDRESS_ABSTRACT, err_msg="ОШИБКА: Поле адрес магазина есть "
                                                                                   "на странице магазина при пустом "
                                                                                   "адресе магазина в базе")
    MY_SHOP_CASE = dict(xpath=check_shop.NOTIFY_MY_SHOP, err_msg="ОШИБКА: Плашка есть под другими ролями, кроме "
                                                                 "продавец - свой магазин")

    # SHP ~ SHOP PAGE
    SHP_TO_GOOD = dict(start_xpath_good=click_shop.GOOD, finish_xpath_good=check_good.TITLE_GOOD)
    SHP_TO_SETTINGS = dict(start_click=click_shop.ADD_GOOD, finish_page=check_my_goods.TITLE_ADD_GOOD)
    SHP_TO_ADD_GOOD = dict(start_click=click_shop.SETTINGS, finish_page=check_settings.TITLE_PROFILE_SETTINGS)
    SHP_TO_SELLER_BTN = [SHP_TO_SETTINGS, SHP_TO_ADD_GOOD]


    # Тест данные для проверки перехода со страницы товара на страницу магазина
    GP_IN_SHOP_BTN = dict(start_click=click_good.BTN_IN_SHOP, finish_page=check_shop.TITLE_SHOP)
    GP_SHOW_MORE_BTN = dict(start_click=click_good.BTN_SHOW_MORE, finish_page=check_shop.TITLE_SHOP)
    GP_LINK_AVATAR = dict(start_click=click_good.LINK_SELLER_AVATAR, finish_page=check_shop.TITLE_SHOP)
    GOOD_PAGE_IN_SHOP_PAGE_SUITE = [GP_IN_SHOP_BTN,
                                    GP_SHOW_MORE_BTN,
                                    GP_LINK_AVATAR]

    # Тест данные для проверки перехода со страницы товара на другой товар этого продавца
    GOOD_PAGE_TO_GOOD_CASE = dict(start_xpath_good=click_good.ANY_GOOD, finish_xpath_good=check_good.TITLE_GOOD)

    # Тест данные для проверки хлебных крошек со страницы товара
    BRC_ROOT_CATEGORY = dict(start_xpath_good=click_good.BREADCRUMBS,
                             finish_xpath_good=check_catalog.ROOT_CATEGORY_ABSTRACT, brc_num=1)
    BRC_CATEGORY = dict(start_xpath_good=click_good.BREADCRUMBS,
                        finish_xpath_good=check_catalog.CATEGORY_ABSTRACT, brc_num=2)
    BRC_FINAL_CATEGORY = dict(start_xpath_good=click_good.BREADCRUMBS,
                              finish_xpath_good=check_catalog.FINAL_CATEGORY_ABSTRACT, brc_num=3)
    BREADCRUMB_ABSTRACT = dict(start_xpath_good=click_good.BREADCRUMBS,
                               finish_xpath_good=check_catalog.CATEGORY_ALL, brc_num=3)
    BREADCRUMBS_SUITE = {
        "root_category": BRC_ROOT_CATEGORY,
        "category": BRC_CATEGORY,
        "final_category": BRC_FINAL_CATEGORY
    }

    # Тест данные для проверки перехода по кнопке задать вопрос по товару
    ASK_BTN_VISITOR = dict(start_click=click_good.ASK_BTN, finish_page=check_auth.TITLE_AUTH_PAGE)


    # Тест данные для проверки перехода по кнопке задать знать цену
    KNOW_PRICE_VISITOR = dict(start_click=click_good.KNOW_PRICE_BTN, finish_page=check_auth.TITLE_AUTH_PAGE)

    # Тест данные для проверки перехода по кнопке добавить в избранное
    ADD_FAVORITE_VISITOR = dict(start_click=click_good.ADD_FAVORITE, finish_page=check_auth.TITLE_AUTH_PAGE)

    # Тест данные для проверки перехода по кнопке пожаловаться на товар для посетителя
    GOOD_COMPLAIN_TO_AUTH = dict(start_click=click_good.BTN_COMPLAIN, finish_page=check_auth.TITLE_AUTH_PAGE)

    # Тест данные для проверки перехода по клику на товар в Избранных товарах на страницу товара
    FAV_GOOD_TO_GOOD_PAGE = dict(start_xpath_good=click_favorite.FAV_GOOD_NAME, finish_xpath_good=check_good.TITLE_GOOD)

    # Тест данные для проверки перехода по клику на имя продавца в Избранных товарах на страницу магазина
    FAV_GOOD_SELLER_TO_SHOP = dict(start_xpath_good=click_favorite.FG_USER_NAME_ABSTRACT,
                                   finish_xpath_good=check_shop.USER_NAME_ABSTRACT)

    # Тест данные для проверки хлебных крошек со страницы Избранные товары
    FAV_BRC_ROOT_CAT = dict(start_xpath_good=click_favorite.BREADCRUMBS,
                            finish_xpath_good=check_catalog.ROOT_CATEGORY_ABSTRACT, brc_num=1)
    FAV_BRC_FINAL_CAT = dict(start_xpath_good=click_favorite.BREADCRUMBS,
                             finish_xpath_good=check_catalog.FINAL_CATEGORY_ABSTRACT, brc_num=2)
    FAV_GOOD_TO_BREAD_CATEGORY_SUITE = [FAV_BRC_ROOT_CAT,
                                        FAV_BRC_FINAL_CAT]

    # Тест данные для проверки перехода по клику на имя продавца в Избранных товарах на страницу магазина
    FAV_USER_USER_TO_SHOP = dict(start_xpath_good=click_favorite.FU_SELLER_NAME_ABSTRACT,
                                 finish_xpath_good=check_shop.USER_NAME_ABSTRACT)


class HelpNavigateMethods(HelpNavigateData):
    @staticmethod
    def get_date():
        """
        Получить время
        :return:
        """
        return time.strftime("%a, %d/%b/%Y %H:%M:%S +0000", time.localtime())

    @staticmethod
    def go_to_main_page(driver, env_base_url=MainClass.ENV_BASE_URL):
        """ Переходим на главную страницу.
        :param driver: ссылка на драйвер
        :param env_base_url: адрес перехода
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
        time.sleep(2)

    @staticmethod
    def logout(driver, sleep=2):
        """ Разлогинивание через меню
        :param driver: ссылка на драйвер
        :param sleep: время на обработку разлогинивания
        """
        #user_menu = driver.find_element_by_xpath(HelpNavigateData.check_main.CHECK_MENU_USER)
        user_menu = HelpNavigateMethods.get_element_navigate(driver, HelpNavigateData.check_main.CHECK_MENU_USER)
        user_menu.click()
        #user_menu.submit()
        #ActionChains(driver).click().perform()
        time.sleep(sleep)
        exit_btn = driver.find_element_by_xpath(HelpNavigateData.click_main.MENU_PROFILE_EXIT)
        exit_btn.click()
        time.sleep(sleep)

    @staticmethod
    def get_element(driver, xpath):
        """ Простой метод, что бы получить элемент со страницы.
        :param driver: ссылка на драйвер
        :param xpath: xpath-элемента для поиска
        :return: None
        """
        service_log.put("Find element with xpath: %s." % str(xpath))
        obj_navigate = driver.find_element_by_xpath(xpath)
        return obj_navigate

    @staticmethod
    def get_element_navigate(driver, xpath, sleep=4, mode='refresh', e_msg='Element object is None'):
        """
        Метод возвращает объект элемента по его xpath
        :param driver:
        :param xpath: - xpath искомого элемента, например //button[contains(.,'Войти')]
        :param sleep: - время задержки в секундах
        :param mode: - режим, что делать если элемент не найден с первого раза на странице (обновить страницу или установить задержку)
        :param e_msg: - сообщение о ошибке если элемент не найден
        :return:
        """
        service_log.put("...Start find element with xpath: %s." % str(xpath))
        obj_navigate = None
        do_time = time.time()
        try:
            obj_navigate = driver.find_element_by_xpath(xpath)
            #assert True == obj_navigate.is_displayed()
        except WebDriverException:
            service_log.put("...Element not find. Refresh page and sleep='%s' sec." % sleep)
            m = lambda m, d: d.refresh() if m is 'refresh' else None
            m(mode, driver)
            HelpNavigateMethods.progress(driver)
            time.sleep(sleep)
            service_log.put("...Repeat find element after sleep='%s' sec, with xpath: '%s'." % (sleep, str(xpath)))
            try:
                obj_navigate = driver.find_element_by_xpath(xpath)
                if obj_navigate.is_displayed() is True:
                    return obj_navigate
                else:
                    service_log.put("...NOT VISIBLE! Element find: %s." % str(xpath))
            except NoSuchElementException:
                service_log.put("...ERROR: Element not find: %s." % str(xpath))
        url = driver.current_url.encode('utf-8')
        assert obj_navigate is not None, "ERROR: '%s' in page %s, xpath='%s'." % (e_msg, url, xpath)
        work_time = HelpNavigateMethods.work_time(do_time)
        service_log.put("...Success! Search time of the element: [%s]. Element find: %s." % (work_time, str(xpath)))
        return obj_navigate

    @staticmethod
    def element_is_none(driver, xpath):
        """
        Проверка, что элемента нет на странице
        :param driver:
        :param xpath:
        :return: None
        """
        tx = None
        service_log.put("Start! Finding element not present in page. xpath='%s'" % xpath)
        try:
            tx = driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            pass
        assert tx is None, "Element present in page, %s" % xpath
        service_log.put("Success! Element is not present in page.")
        return None

    @staticmethod
    def element_is_present(driver, xpath, wait=10):
        """
        проверка, что элемент появляется на странице, актуально для сообщений о успешном измении настроек
        :param driver:
        :param xpath:
        :param wait:
        :return:
        """
        obj = None
        do_time = time.time()
        while time.time() - do_time < wait:
            try:
                obj = driver.find_element_by_xpath(xpath)
                break
            except NoSuchElementException:
                pass
        url = driver.current_url.encode('utf-8')
        assert obj is not None, "Element %s not present in page %s within %s sec." % (xpath, url, wait)
        service_log.put("Success! Element is present in page.")
        return obj

    @staticmethod
    def elements_is_present(driver, xpath, wait=10):
        """
        Проверка, что элементы появляется на странице, актуально для сообщений о успешном измении настроек
        :param driver:
        :param xpath:
        :param wait:
        :return:
        """
        obj_list = None
        do_time = time.time()
        while time.time() - do_time < wait:
            try:
                objs = driver.find_elements_by_xpath(xpath)
                obj_list = objs
                break
            except NoSuchElementException:
                pass
        url = driver.current_url.encode('utf-8')
        assert obj_list is not None, "Elements %s not present in page %s within %s sec." % (xpath, url, wait)
        service_log.put("Success! Elements is present in page.")
        return obj_list

    @staticmethod
    def change_url(driver, url_start, url_end=None, wait_changing=15):
        """

        :param url_start:
        :param url_end:
        :return:
        """
        change_page = False
        do_time = time.time()
        while time.time() - do_time < wait_changing:
            url_end = driver.current_url.encode('utf-8')
            if url_end != url_start:
                change_page = True
                service_log.put("Page url changed. Success!")
                break
        assert change_page is True, "Page not changed within %s sec. Current page %s" % (wait_changing, url_end)

    @staticmethod
    def change_source(driver, source, wait_changing=15):
        """

        :param url_start:
        :param url_end:
        :return:
        """
        change_page = False
        url = 'Empty'
        do_time = time.time()
        while time.time() - do_time < wait_changing:
            source_end = driver.page_source
            if source_end != source:
                change_page = True
                url = driver.current_url.encode('utf-8')
                service_log.put("Page source changed. Success!")
                break
        assert change_page is True, "Page not changed within %s sec. Current page %s" % (wait_changing, url)

    @staticmethod
    def element_type(e):
        """
        Метод определяет, что он получил объект или xpath
        :param e:
        :return:
        """
        if isinstance(e, basestring):
            service_log.put("Element type is sting")
            return 'xpath'
        elif isinstance(e, object):
            service_log.put("Element type is object")
            return 'object'
        else:
            service_log.error("Element type is UNKNOWN")
            assert "Unknown type"

    @staticmethod
    def element_click(driver, element, url_end=None, change_page_url=True):
        """

        :param driver:
        :param xpath:
        :param change_page_url:
        :return:
        """
        e_type = HelpNavigateMethods.element_type(element)
        if e_type is 'xpath':
            service_log.put("Begin search element by xpath %s" % element)
            obj = HelpNavigateMethods.element_is_present(driver, element)
        else:
            obj = element
        url_s = driver.current_url.encode('utf-8')
        source_1 = driver.page_source
        obj.click()
        service_log.put("Click element.")
        if change_page_url is True:
            service_log.put("Begin changing page url.")
            HelpNavigateMethods.change_url(driver, url_s, url_end)
            HelpNavigateMethods.progress(driver)
        else:
            HelpNavigateMethods.change_source(driver, source_1)

    @staticmethod
    def find_element_by_xpath_fast(driver, value, by=By.XPATH):
        """
        Поиск объекта на странице по xpath без подсветки
        :param driver: ссылка на драйвер
        :param by: посиковый тип
        :param value: xpath
        :return:
        """
        if not By.is_valid(by) or not isinstance(value, str):
            raise InvalidSelectorException("Invalid locator values passed in")
        element = driver.execute(Command.FIND_ELEMENT,
                                 {'using': by, 'value': value})['value']
        return element

    @staticmethod
    def work_time(do_time, end_time=None):
        """
        Время выполнения
        :param do_time:
        :param end_time:
        :return:
        """
        if end_time is None:
            end_time = time.time()
        diff_time = end_time - do_time
        dot_pos = str(diff_time).rfind('.')
        milli = str(diff_time)[dot_pos + 1:dot_pos + 4]
        work_time = time.strftime('%H:%M:%S', time.gmtime(diff_time)) + "," + milli
        return str(diff_time)

    @staticmethod
    def progress(driver, wait=15):
        """
        Проверка появления прогресс бара
        :param driver:
        :return:
        """
        work_time = None
        progress_end = False
        service_log.put("Page loading...")
        do_time = time.time()
        while time.time() - do_time < wait:
            try:
                HelpNavigateMethods.find_element_by_xpath_fast(driver, value=HelpNavigateData.check_main.PROGRESS_BAR)
            except Exception:
                work_time = HelpNavigateMethods.work_time(do_time)
                progress_end = True
                break
        if progress_end is True:
            service_log.put("Page loaded. Load time: [%s]" % work_time)
        else:
            work_time = '00:00:%s' % wait
            service_log.put("Page  not loaded. Load time: [%s]" % work_time)
            driver.get_screenshot_as_file('tmp/progress_not_load_%s.png' % str(time.ctime()).replace(' ', '_'))
        return work_time

    @staticmethod
    def go_to_page(obj_navigate, sleep=2):
        service_log.put("...Start click element: %s." % str(obj_navigate))
        obj_navigate.click()
        time.sleep(sleep)
        service_log.put("...Finish click. Success!")

    @staticmethod
    def get_current_url(driver):
        url = None
        try:
            url = driver.current_url
        except Exception:
            service_log.put("...ERROR: Can't get url.")
            raise AssertionError("ОШИБКА: Не могу получить текущий урл.")
        service_log.put("...Success! get url: %s." % url)
        return url

    @staticmethod
    def get_new_window(driver):
        driver.switch_to.window(driver.window_handles[1])
        service_log.put("...Change window success.")

    @staticmethod
    def get_name(obj_good):
        good_name = obj_good.text.encode('utf-8')
        return good_name

    @staticmethod
    def get_auth_page(driver, env_base_url=MainClass.ENV_BASE_URL):
        url = env_base_url + HelpNavigateData.path_auth.PATH_AUTH
        service_log.put("Get page: %s" % url)
        do_get_work = time.time()
        driver.get(url)
        work_get_time = HelpNavigateCheckMethods.work_time(do_get_work)
        service_log.put("Onload event time: [%s]" % work_get_time)
        HelpNavigateCheckMethods.progress(driver)
        work_load_time = HelpNavigateCheckMethods.work_time(do_get_work)
        service_log.put("Page received: %s" % url)
        service_log.put("Page received time: %s" % work_load_time)

    @staticmethod
    def get_my_goods_page(driver, env_base_url=MainClass.ENV_BASE_URL, sleep=2):
        url = env_base_url + HelpNavigateData.path_my_goods.URL_MY_GOODS
        service_log.put("Get page: %s" % url)
        do_get_work = time.time()
        driver.get(url)
        work_get_time = HelpNavigateCheckMethods.work_time(do_get_work)
        service_log.put("Onload event time: [%s]" % work_get_time)
        HelpNavigateCheckMethods.progress(driver)
        work_load_time = HelpNavigateCheckMethods.work_time(do_get_work)
        service_log.put("Page received: %s" % url)
        service_log.put("Page received time: %s" % work_load_time)

    @staticmethod
    def get_page(driver, path_url='', env_base_url=MainClass.ENV_BASE_URL):
        """ Перейти на указанную страницу.
        :param driver: ссылка на драйвер
        :param path_url: url перехода
        :param env_base_url: базовый url
        :param sleep: таймер ожидания, дождать загрузки
        """
        url = env_base_url + path_url
        service_log.put("Get page: %s" % url)
        do_get_work = time.time()
        driver.get(url)
        work_get_time = HelpNavigateCheckMethods.work_time(do_get_work)
        service_log.put("Onload event time: [%s]" % work_get_time)
        HelpNavigateCheckMethods.progress(driver)
        work_load_time = HelpNavigateCheckMethods.work_time(do_get_work)
        service_log.put("Page received: %s" % url)
        service_log.put("Page received time: %s" % work_load_time)

    @staticmethod
    def get_paginator_items(driver, paginators_xpath):
        return driver.find_elements_by_xpath(paginators_xpath)

    @staticmethod
    def get_paginator_active(driver, position):
        return driver.find_elements_by_xpath(HelpNavigateData.path_my_goods.PAGINATOR_ACTIVE % position)

    @staticmethod
    def get_list_elements(driver, xpath):
        """
        Получаем список объектов элементов
        :param driver:
        :param xpath:
        :return:
        """
        return driver.find_elements_by_xpath(xpath)

    @staticmethod
    def move_to_element(driver, obj_move):
        action = ActionChains(driver)
        action.move_to_element(obj_move).perform()
        # time.sleep(2)

    @staticmethod
    def get_position_in_page_source(driver, find_template):
        """
        Метод получает идентификатор первого вхождения шаблона на странице
        :param driver:
        :param find_template:
        :return:
        """
        page_html = driver.page_source
        position = page_html.find(find_template)
        return position

    @staticmethod
    def get_count_goods_in_page(source, find_template):
        """
        Метод ычисляет количество товаров на странице
        :param source: - код страницы
        :param find_template: - html код товара
        :return:
        """
        good_count = source.count(find_template)
        return good_count

    @staticmethod
    def get_good_id_from_page_source(driver, find_template, good_count=None, len_good_id=32, cont=1):
        """
        Метод получает все идентификаторы на странице
        :param driver:
        :param find_template: кусок html-кода,который находится перед каждым идентификатором товара,например /good/
        :param len_good_id: длина идентификатора товара
        :param cont: позиция, с которой начинается поиск идентификаторов
        :return:
        """
        # Получаем исходник страницы
        source = driver.page_source
        # Вычисляем количество товаров на странице
        if good_count is None:
            good_count = HelpNavigateMethods.get_count_goods_in_page(source, find_template)
        # Вычисляем длину шаблона
        len_temple = len(find_template)
        # Создаем пустой список для ID товаров
        list_good_id = []
        for count in range(good_count):
            start_good_id_index = source.find(find_template, cont) + len_temple
            end_good_id_index = start_good_id_index + len_good_id
            list_good_id.append(source[start_good_id_index:end_good_id_index].encode('utf-8'))
            cont = start_good_id_index + 1
        assert list_good_id is not [], "Not find IDs"
        return list_good_id

    @staticmethod
    def get_category_id_from_page_source(driver, find_template_start, find_template_end, cont=1):
        """
        Метод получает все идентификаторы категорий на странице
        :param driver:
        :param find_template_start:
        :param find_template_end:
        :param cont: позиция начала поиска
        :return:
        """
        page_html = driver.page_source
        count_finder = HelpNavigateMethods.get_count_goods_in_page(page_html, find_template_start)
        len_temple = len(find_template_start)
        list_cat_id = []
        for count in range(count_finder):
            start_category_index = page_html.find(find_template_start, cont) + len_temple
            end_category_index = page_html.find(find_template_end, start_category_index)
            list_cat_id.append(page_html[start_category_index:end_category_index].encode('utf-8'))
            cont = start_category_index + 1
        assert list_cat_id is not []
        return list_cat_id

    @staticmethod
    def get_all_id_ware(driver, find_template_start, find_template_end, cont=1):
        """
        Метод получает все идентификаторы товаров на странице создания товара.
        :param driver: ссылка на драйвер
        :param find_template_start:
        :param find_template_end:
        :param cont: позиция начала поиска
        :return:
        """
        page_html = driver.page_source
        count_finder = HelpNavigateMethods.get_count_goods_in_page(page_html, find_template_start)
        len_temple = len(find_template_start)
        list_ware_id = []
        for count in range(count_finder):
            start_index = page_html.find(find_template_start, cont) + len_temple
            end_index = page_html.find(find_template_end, start_index)
            list_ware_id.append(page_html[start_index:end_index].encode('utf-8'))
            cont = start_index + 1
        #list_ware_id.pop(0)  # todo: иногда возвращается аватар, удаляем аватар
        return list_ware_id

    @staticmethod
    def get_count_good_in_block(count_good, max_count):
        """
        Метод ограничивает количство товаров в блоке равным max_count
        :param count_good:
        :return:
        """
        if count_good > max_count:
            count_good = max_count
        return count_good

    @staticmethod
    def input_str(obj, string):
        """
        Метод для ввода данных в инпут поля
        :param driver:
        :param obj:
        :param string:
        :return:
        """
        s = string
        if isinstance(string, str):
            string = s.decode('utf-8')
            service_log.put("Конвертируем строку в unicode")
        elif isinstance(string, unicode):
            s = string.encode('utf-8')
            service_log.put("Строка получена в unicode, не требует конвертации")
        service_log.put("Вводим символы [%s]" % s)
        obj.send_keys(string)
        service_log.put("В input поле введены символы")


class HelpNavigateCheckMethods(HelpNavigateMethods):

    def check_navigate(self, driver, navigate, sleep=2):
        service_log.put("STEP 1. Start check visible element: %s." % navigate["start_click"])
        obj_start_click = self.get_element_navigate(driver, navigate["start_click"])
        if not obj_start_click.is_displayed():
            service_log.put("Element is not visible. Sleep='%s' sec." % sleep)
            time.sleep(sleep)
            service_log.put("Repeat check visible before sleep='%s' sec, element: %s." %
                            (sleep, navigate["start_click"]))
            obj_start_click = self.get_element_navigate(driver, navigate["start_click"], sleep)
        self.assertTrue(obj_start_click.is_displayed(), "ERROR: Element is not visible: %s" % navigate["start_click"])
        service_log.put("Success! Element is visible: %s." % navigate["start_click"])

        service_log.put("STEP 1.1. Find current url.")
        start_url = self.get_current_url(driver)

        service_log.put("STEP 2. Click element: %s." % obj_start_click)
        self.go_to_page(obj_start_click)

        service_log.put("STEP 2.1. Find current url before click.")
        finish_url = self.get_current_url(driver)

        service_log.put("STEP 2.2. Compare 'finish_url' with 'start_url'.")
        self.assertNotEqual(finish_url, start_url, "ОШИБКА: Урлы совпадают, переход не произошел")
        service_log.put("Success! Compare 'finish_url' with 'start_url'.")

        service_log.put("STEP 3. Start find Finish element: %s." % navigate["finish_page"])
        self.get_element_navigate(driver, navigate["finish_page"])
        service_log.put("Success! Finish element is find: %s." % navigate["finish_page"])

    def check_navigate_in_new_window(self, driver, navigate, sleep=2):
        service_log.put("STEP 1. Start check visible element: %s." % navigate["start_click"])
        obj_start_click = self.get_element_navigate(driver, navigate["start_click"])
        if not obj_start_click.is_displayed():
            service_log.put("Element is not visible. Sleep='%s' sec." % sleep)
            time.sleep(sleep)
            service_log.put("Repeat check visible before sleep='%s' sec, element: %s." %
                            (sleep, navigate["start_click"]))
            obj_start_click = self.get_element_navigate(driver, navigate["start_click"], sleep)
        self.assertTrue(obj_start_click.is_displayed(), "ERROR: Element is not visible: %s" % navigate["start_click"])
        service_log.put("Success! Element is visible: %s." % navigate["start_click"])

        service_log.put("STEP 1.1. Find current url.")
        start_url = self.get_current_url(driver)

        service_log.put("STEP 2. Click element: %s." % obj_start_click)
        self.go_to_page(obj_start_click)

        service_log.put("STEP 2.1. Find current url before click.")
        finish_url = self.get_current_url(driver)

        self.get_new_window(driver)

        service_log.put("STEP 3. Start find Finish element: %s." % navigate["finish_page"])
        self.get_element_navigate(driver, navigate["finish_page"])
        service_log.put("End test! Success! Finish element is find: %s." % navigate["finish_page"])

    def check_navigate_in_good_page(self, driver, navigate, num_good, sleep=2):
        start_click = navigate["start_xpath_good"] % num_good
        service_log.put("STEP 1. Start check visible element: %s." % start_click)
        obj_start_click = self.get_element_navigate(driver, start_click)
        if not obj_start_click.is_displayed():
            service_log.put("Element is not visible. Sleep='%s' sec." % sleep)
            time.sleep(sleep)
            service_log.put("Repeat check visible before sleep='%s' sec, element: %s." % (sleep, start_click))
            obj_start_click = self.get_element_navigate(driver, start_click, sleep)
        self.assertTrue(obj_start_click.is_displayed(), "ERROR: Element is not visible: %s" % start_click)
        service_log.put("Success! Element is visible: %s." % start_click)

        service_log.put("STEP 1.1. Find current url.")
        start_url = self.get_current_url(driver)

        good_name = self.get_name(obj_start_click)
        service_log.put("STEP 2. Click element: %s." % obj_start_click)
        self.go_to_page(obj_start_click)

        service_log.put("STEP 2.1. Find current url before click.")
        finish_url = self.get_current_url(driver)

        service_log.put("STEP 2.2. Compare 'finish_url' with 'start_url'.")
        self.assertNotEqual(finish_url, start_url, "ОШИБКА: Урлы совпадают, переход не произошел")
        service_log.put("Success! Compare 'finish_url' with 'start_url'.")

        service_log.put("STEP 3. Start find Finish element: %s." % navigate["finish_xpath_good"])
        obj_finish = self.get_element_navigate(driver, navigate["finish_xpath_good"], sleep)
        good_name_in_good_page = self.get_name(obj_finish)
        self.assertEqual(good_name, good_name_in_good_page)

    def check_navigate_two_click(self, driver, navigate, sleep=2):
        service_log.put("STEP 1. Start check visible element: %s." % navigate["start_click"])
        obj_start_click = self.get_element_navigate(driver, navigate["start_click"])
        if not obj_start_click.is_displayed():
            service_log.put("Element is not visible. Sleep='%s' sec." % sleep)
            time.sleep(sleep)
            service_log.put("Repeat check visible before sleep='%s' sec, element: %s." %
                            (sleep, navigate["start_click"]))
            obj_start_click = self.get_element_navigate(driver, navigate["start_click"], sleep)
        self.assertTrue(obj_start_click.is_displayed(), "ERROR: Element is not visible: %s" % navigate["start_click"])
        service_log.put("Success! Element is visible: %s." % navigate["start_click"])

        service_log.put("STEP 1.1. Find current url.")
        start_url = self.get_current_url(driver)

        service_log.put("STEP 2. Click element: %s." % obj_start_click)
        self.go_to_page(obj_start_click)

        obj_second_click = self.get_element_navigate(driver, navigate["second_click"])
        service_log.put("STEP 2.1. Click element: %s." % obj_second_click)
        self.go_to_page(obj_second_click)

        service_log.put("STEP 2.2. Find current url before click.")
        finish_url = self.get_current_url(driver)

        service_log.put("STEP 2.3. Compare 'finish_url' with 'start_url'.")
        self.assertNotEqual(finish_url, start_url, "ОШИБКА: Урлы совпадают, переход не произошел")
        service_log.put("Success! Compare 'finish_url' with 'start_url'.")

        service_log.put("STEP 3. Start find Finish element: %s." % navigate["finish_page"])
        self.get_element_navigate(driver, navigate["finish_page"])
        service_log.put("Success! Finish element is find: %s." % navigate["finish_page"])

    def check_navigate_active_inactive(self, driver, navigate):
        self.assertIsNotNone(driver.find_element_by_xpath(self.check_my_goods.MENU_ACTIVE % navigate['active']))
        self.assertIsNotNone(driver.find_element_by_xpath(self.check_my_goods.MENU_INACTIVE % navigate['inactive']))
        start_url = self.get_current_url(driver)
        first_good = self.get_name(self.get_element_navigate(driver, self.check_my_goods.SHOT_INFO_GOOD % 1))

        obj_inactive = self.get_element_navigate(driver, self.click_my_goods.INACTIVE_PAGE)
        self.go_to_page(obj_inactive)

        finish_url = self.get_current_url(driver)
        first_good_new = self.get_name(self.get_element_navigate(driver, self.check_my_goods.SHOT_INFO_GOOD % 1))
        self.assertNotEqual(finish_url, start_url, "ОШИБКА: Урлы совпадают, переход не произошел")
        self.assertNotEqual(first_good, first_good_new, "ОШИБКА: Товары совпадают, переход не произошел")
        self.assertIsNotNone(driver.find_element_by_xpath(self.check_my_goods.MENU_ACTIVE % navigate['inactive']))
        self.assertIsNotNone(driver.find_element_by_xpath(self.check_my_goods.MENU_INACTIVE % navigate['active']))

        obj_active = self.get_element_navigate(driver, self.click_my_goods.ACTIVE_PAGE)
        self.go_to_page(obj_active)

        restart_url = self.get_current_url(driver)
        first_good_one = self.get_name(self.get_element_navigate(driver, self.check_my_goods.SHOT_INFO_GOOD % 1))
        self.assertNotEqual(finish_url, restart_url, "ОШИБКА: Урлы совпадают, переход не произошел")
        self.assertNotEqual(first_good_one, first_good_new, "ОШИБКА: Товары совпадают, переход не произошел")
        self.assertIsNotNone(driver.find_element_by_xpath(self.check_my_goods.MENU_ACTIVE % navigate['active']))
        self.assertIsNotNone(driver.find_element_by_xpath(self.check_my_goods.MENU_INACTIVE % navigate['inactive']))

    def check_navigate_good_user_favorite(self, driver, navigate):
        self.assertIsNotNone(driver.find_element_by_xpath(self.check_favorite.MENU_ACTIVE % navigate['goods']))
        self.assertIsNotNone(driver.find_element_by_xpath(self.check_favorite.MENU_INACTIVE % navigate['users']))
        start_url = self.get_current_url(driver)

        obj_users = self.get_element_navigate(driver, self.click_favorite.USERS_PAGE)
        self.go_to_page(obj_users)

        finish_url = self.get_current_url(driver)
        self.assertNotEqual(finish_url, start_url, "ОШИБКА: Урлы совпадают, переход не произошел")
        self.assertIsNotNone(driver.find_element_by_xpath(self.check_favorite.MENU_ACTIVE % navigate['users']))
        self.assertIsNotNone(driver.find_element_by_xpath(self.check_favorite.MENU_INACTIVE % navigate['goods']))

        obj_goods = self.get_element_navigate(driver, self.click_favorite.GOODS_PAGE)
        self.go_to_page(obj_goods)

        restart_url = self.get_current_url(driver)
        self.assertNotEqual(finish_url, restart_url, "ОШИБКА: Урлы совпадают, переход не произошел")
        self.assertIsNotNone(driver.find_element_by_xpath(self.check_favorite.MENU_ACTIVE % navigate['goods']))
        self.assertIsNotNone(driver.find_element_by_xpath(self.check_favorite.MENU_INACTIVE % navigate['users']))

    def check_mini(self, driver, list_navigate):
        for key in list_navigate:
            self.get_element_navigate(driver, list_navigate[key])

    def check_paginator_items(self, driver, items, info_good):
        self.assertNotEqual(items, [], "ОШИБКА: Нет елементов для пагинации")
        for item in items:
            start_url = self.get_current_url(driver)
            first_good = self.get_name(self.get_element_navigate(driver, info_good))
            self.go_to_page(item)
            self.get_paginator_active(driver, item.text)
            finish_url = self.get_current_url(driver)
            first_good_new = self.get_name(self.get_element_navigate(driver, info_good))
            self.assertNotEqual(finish_url, start_url, "ОШИБКА: Урлы совпадают, переход не произошел")
            self.assertNotEqual(first_good, first_good_new, "ОШИБКА: Товары совпадают, переход не произошел")

    def check_paginator_next_prev(self, driver, leng, info_good, sleep=2):
        #self.get_element_navigate(driver, self.check_my_goods.PAG_PREV_PASSIVE)
        self.assertNotEqual(leng, 0, "ОШИБКА: Нет елементов для пагинации")
        for count in range(leng):
            start_url = self.get_current_url(driver)
            first_good = self.get_name(self.get_element_navigate(driver, info_good))
            self.go_to_page(self.get_element_navigate(driver, self.click_my_goods.PAG % str(count + 2)))
            time.sleep(sleep)
            self.get_paginator_active(driver, str(count + 1))
            finish_url = self.get_current_url(driver)
            first_good_new = self.get_name(self.get_element_navigate(driver, info_good))
            self.assertNotEqual(finish_url, start_url, "ОШИБКА: Урлы совпадают, переход не произошел")
            self.assertNotEqual(first_good, first_good_new, "ОШИБКА: Товары совпадают, переход не произошел")
        #self.get_element_navigate(driver, self.check_my_goods.PAG_NEXT_PASSIVE)
        for count in range(leng):
            start_url = self.get_current_url(driver)
            first_good = self.get_name(self.get_element_navigate(driver, info_good))
            self.go_to_page(self.get_element_navigate(driver, self.click_my_goods.PAG % str(leng - count)))
            time.sleep(sleep)
            self.get_paginator_active(driver, str(leng - count - 1))
            finish_url = self.get_current_url(driver)
            first_good_new = self.get_name(self.get_element_navigate(driver, info_good))
            self.assertNotEqual(finish_url, start_url, "ОШИБКА: Урлы совпадают, переход не произошел")
            self.assertNotEqual(first_good, first_good_new, "ОШИБКА: Товары совпадают, переход не произошел")
        #self.get_element_navigate(driver, self.check_my_goods.PAG_PREV_PASSIVE)

    def check_footer_copyright(self, driver):
        self.get_element_navigate(driver, self.click_main.FC_LOGO)
        cr_text = self.get_name(self.get_element_navigate(driver, self.check_main.FC_COPYRIGHT))
        self.assertEqual(self.check_main.FC_COPYRIGHT_TEXT, cr_text, "ОШИБКА: Получен другой текст: %s" % cr_text)


    def check_header_widget_visitor(self, driver):
        """ Проверка шапки виджета для не залогиненного пользователя (посетителя).
        :param driver: ссылка на драйвер
        """
        self.get_element_navigate(driver, self.click_main.BUTTON_REG_AND_LOGIN)
        self.get_element_navigate(driver, self.click_main.HEADER_LANG_SELECTOR)
        self.element_is_none(driver, self.click_main.HEADER_WIDGET_CHATS)
        self.element_is_none(driver, self.click_main.HEADER_FAVORITES)
        self.element_is_none(driver, self.click_main.HEADER_MY_SHOP)
        self.element_is_none(driver, self.check_main.CHECK_MENU_USER)

    def check_header_widget_buyer(self, driver, user_id):
        """ Проверка виджета у покупателя.
        :param driver: ссылка на драйвер
        :param user_id: идентификатор пользователя
        """
        self.get_element_navigate(driver, self.click_main.HEADER_WIDGET_CHATS)
        self.get_element_navigate(driver, self.click_main.HEADER_FAVORITES)
        self.get_element_navigate(driver, self.check_main.CHECK_MENU_USER)
        self.get_element_navigate(driver, self.click_main.MENU_PROFILE_SETTINGS)
        self.get_element_navigate(driver, self.click_main.MENU_PROFILE_EXIT)
        self.element_is_none(driver, self.click_main.BUTTON_REG_AND_LOGIN)
        self.element_is_none(driver, self.click_main.HEADER_MY_SHOP)
        self.element_is_none(driver, self.click_main.MENU_MY_SHOP % user_id)

    def check_header_widget_seller(self, driver, user_id):
        """ Проверка виджета у продавца.
        :param driver: ссылка на драйвер
        :param user_id: идентификатор пользователя
        """
        self.get_element_navigate(driver, self.click_main.HEADER_WIDGET_CHATS)
        self.get_element_navigate(driver, self.click_main.HEADER_MY_SHOP)
        self.get_element_navigate(driver, self.click_main.HEADER_FAVORITES)
        self.get_element_navigate(driver, self.check_main.CHECK_MENU_USER)
        self.get_element_navigate(driver, self.click_main.MENU_PROFILE_SETTINGS)
        #self.get_element_navigate(driver, self.click_main.MENU_MY_SHOP % user_id)
        self.get_element_navigate(driver, self.click_main.MENU_PROFILE_EXIT)
        self.element_is_none(driver, self.click_main.BUTTON_REG_AND_LOGIN)

    def check_header_widget_seller_all(self, driver, user):
        """ Проверка виджета у продавца.
        :param driver: ссылка на драйвер
        :param user_id: идентификатор пользователя
        """
        self.get_element_navigate(driver, self.click_main.HEADER_WIDGET_CHATS, mode='')
        self.get_element_navigate(driver, self.click_main.HEADER_CONTACTS, mode='')
        menu = self.get_element_navigate(driver, self.check_main.CHECK_MENU_USER, mode='')
        menu.click()
        self.get_element_navigate(driver, self.check_main.WU_NAME % user["display_name"], mode='')
        #self.get_element_navigate(driver, self.click_main.MENU_MY_SHOP % user["id"], mode='')
        self.get_element_navigate(driver, self.click_main.HEADER_MY_SHOP, mode='')
        self.get_element_navigate(driver, self.click_main.HEADER_FAVORITES, mode='')
        self.get_element_navigate(driver, self.click_main.MENU_PROFILE_SETTINGS, mode='')
        self.get_element_navigate(driver, self.click_main.MENU_PROFILE_EXIT, mode='')
        self.element_is_none(driver, self.click_main.BUTTON_REG_AN_LOGIN)

    def check_shop_to_chat(self, driver, seller_id):
        obj_chat_btn = self.get_element_navigate(driver, HelpNavigateData.click_shop.CHAT_BUTTON % seller_id)
        service_log.put("STEP 1.1. Find current url.")
        start_url = self.get_current_url(driver)

        self.go_to_page(obj_chat_btn)

        service_log.put("STEP 2.1. Find current url before click.")
        finish_url = self.get_current_url(driver)
        service_log.put("STEP 2.2. Compare 'finish_url' with 'start_url'.")

        self.assertNotEqual(finish_url, start_url, "ОШИБКА: Урлы совпадают, переход не произошел")
        service_log.put("Success! Compare 'finish_url' with 'start_url'.")
        self.assertIsNotNone(self.get_element_navigate(driver, HelpNavigateData.check_chat.TITLE_USER_IN_CHAT
                                                       % seller_id))
        self.assertIsNotNone(self.get_element_navigate(driver, HelpNavigateData.check_chat.CHAT_SECTION_CHAT
                                                       % seller_id))
        self.assertIsNotNone(self.get_element_navigate(driver, HelpNavigateData.input_chat.CHAT_INPUT_ABSTRACT))


    def check_no_such_element(self, driver, test_data):
        tx = None
        try:
            driver.find_element_by_xpath(test_data['xpath'])
        except Exception, tx:
            pass
        self.assertIsNotNone(tx, test_data['err_msg'])