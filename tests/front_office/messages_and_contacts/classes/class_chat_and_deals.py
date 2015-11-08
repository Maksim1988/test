# coding=utf-8
import time

from selenium.webdriver.common.action_chains import ActionChains

from support import service_log
from tests.MainClass import MainClass
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate
from tests.front_office.data_navigation import GoodPage, ShopPage, MainPage, SearchPage, BuyerPage, FavoritePage, \
    ChatPage

__author__ = 'm.senchuk'


class HelpChatAndDealsData(MainClass, ActionChains):

    click_shop = ShopPage.Click
    click_main = MainPage.Click
    click_search = SearchPage.Click
    click_good = GoodPage.Click
    click_favorites = FavoritePage.Click
    click_chat = ChatPage.Click
    check_shop = ShopPage.Check
    check_good = GoodPage.Check
    check_search = SearchPage.Check
    check_buyer = BuyerPage.Check
    check_main = MainPage.Check
    check_favorites = FavoritePage.Check
    check_chat = ChatPage.Check
    input_main = MainPage.Input
    path_search = SearchPage.Path
    path_buyer = BuyerPage.Path
    path_main = MainPage.Path
    path_favorites = FavoritePage.Path
    path_chat = ChatPage.Path

    NEED_STOCK_NEGATIVE = [u'ру',
                           'en',
                           '!',
                           '/',
                           '*',
                           '-',
                           '+',
                           '(',
                           ')',
                           '=',
                           '%',
                           '@',
                           '<']


class HelpChatAndDealsMethods(HelpChatAndDealsData):
    @staticmethod
    def get_notification_msg(driver, xpath_msg):
        return Navigate.get_element_navigate(driver, xpath_msg, mode=None)

    @staticmethod
    def get_min_stock_good(driver, xpath_min_stock):
        min_stock_str = Navigate.get_element_navigate(driver, xpath_min_stock, mode=None).text.encode('utf-8')
        min_stock = int(min_stock_str[0:-6])
        return min_stock

    @staticmethod
    def set_need_stock(driver, xpath_need_stock, need_stock, sleep=1):
        need_stock_input = Navigate.get_element_navigate(driver, xpath_need_stock, mode=None)
        need_stock_input.clear()
        need_stock_input.send_keys(need_stock)
        time.sleep(sleep)


class HelpChatAndDealsCheckMethods(HelpChatAndDealsMethods):
    def check_success_complain(self, driver):
        self.get_notification_msg(driver, self.check_good.COMPLAIN_SUCCESS)

    def check_moderator_complain(self, driver, good_id, good_name, time_complain):
        Navigate.get_element_navigate(driver, self.check_chat.COMPLAIN_1_MSG, mode=None)
        #self.assertGreaterEqual(Navigate.get_element_navigate(driver, self.check_chat.COMPLAIN_TIME, mode=None).text.
        #                        encode('utf-8'), time_complain)
        Navigate.get_element_navigate(driver, self.check_chat.COMPLAIN_GOOD_LINK % good_id, mode=None)
        Navigate.get_element_navigate(driver, self.check_chat.COMPLAIN_GOOD_NAME % good_name, mode=None)

    def check_err_msg(self, driver, xpath_err_msg):
        tx1 = None
        tx2 = None
        service_log.put("STEP: CHECK ERROR MESSAGE")
        try:
            service_log.put("...Start find abstract warning message.")
            driver.find_element_by_xpath(self.check_good.ERR_NEED_STOCK_ABSTRACT)
            service_log.put("...Success! Abstract warning message is found.")
        except Exception, tx1:
            service_log.error("...Abstract warning message is not found.")
            self.assertIsNone(tx1, "Warning message '%s' is not found." % xpath_err_msg)
        try:
            driver.find_element_by_xpath(xpath_err_msg)
            service_log.put("...Success! Warning message '%s' is found." % xpath_err_msg)
        except Exception, tx2:
            service_log.error("...Warning message '%s' is not found." % xpath_err_msg)
            self.assertIsNone(tx2, "Warning message '%s' is not found. %s" % (xpath_err_msg, tx2))