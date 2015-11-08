# coding=utf-8
import time

from selenium.webdriver.common.action_chains import ActionChains

from tests.MainClass import MainClass
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate

__author__ = 'm.senchuk'


class HelpUserCardData(MainClass, ActionChains):
    pass


class HelpUserCardMethods(HelpUserCardData):

    @staticmethod
    def get_user_card_photo(driver, photo_xpath, avatar_id):
        if avatar_id is None:
            p = driver.find_element_by_xpath(Navigate.check_good.USER_NO_PHOTO)
        else:
            p = driver.find_element_by_xpath(photo_xpath % avatar_id)
        return p

    @staticmethod
    def get_shop_card_photo(driver, photo_xpath, avatar_id):
        if avatar_id is None:
            p = driver.find_element_by_xpath(Navigate.check_good.SHOP_NO_LOGO)
        else:
            p = driver.find_element_by_xpath(photo_xpath % avatar_id)
        return p


    @staticmethod
    def get_user_card_name(driver, user_xpath, display_name):
        return Navigate.element_is_present(driver, user_xpath % display_name)


    @staticmethod
    def get_user_card_web_status(driver, web_status_xpath, user_info, online_status='В сети'):
        if user_info["online_status"] == 'ONLINE':
            p = Navigate.get_element_navigate(driver, web_status_xpath % online_status)
        else:
            p = Navigate.get_element_navigate(driver, web_status_xpath %
                                              HelpUserCardMethods.need_time(user_info['last_activity_timestamp']))
        return p

    @staticmethod
    def get_user_card_on_off_line(driver, web_status_xpath, user_info, online_status='В сети', offline='Не в сети'):
        if user_info["online_status"] == 'ONLINE':
            p = Navigate.get_element_navigate(driver, web_status_xpath % online_status, mode=None)
        else:
            p = Navigate.get_element_navigate(driver, web_status_xpath % offline, mode=None)
        return p


    @staticmethod
    def need_time(unix_time):
        tm = time.localtime(float(str(unix_time)[:-3]))
        date = time.strftime("%H:%M", tm)
        if date[0] == '0':
            date = date[1:]
        return date


    @staticmethod
    def get_user_card_link(driver, link_xpath):
        return driver.find_element_by_xpath(link_xpath)

    @staticmethod
    def search_user(driver, user, sleep=2):
        Navigate.element_is_present(driver, Navigate.input_main.SEARCH).send_keys(user.decode('utf-8'))
        Navigate.element_click(driver, Navigate.click_main.BTN_SEARCH)
        time.sleep(sleep)
        Navigate.element_click(driver, Navigate.click_search.USER_MENU)
        time.sleep(sleep)

    @staticmethod
    def go_lot_user(driver, num_lot):
        driver.find_element_by_xpath(Navigate.path_main.PATH_USER_LOT % num_lot).click()

    @staticmethod
    def go_favorites_to_user(driver, num_lot, path):
        driver.find_element_by_xpath((Navigate.path_favorites.PATH_FAVORITE % num_lot) + path).click()

    @staticmethod
    def click_and_transition_to_page(driver, xpath, sleep=2):
        start_url = driver.current_url
        driver.find_element_by_xpath(xpath).click()
        finish_url = driver.current_url
        assert start_url != finish_url, "ERROR: start_url and finish_url is equal"
        tx = None
        #time.sleep(sleep)
        try:
            driver.find_element_by_xpath(xpath)
        except Exception, tx:
            pass
        if tx is None:
            driver.refresh()
            Navigate.progress(driver)
            time.sleep(sleep)

    @staticmethod
    def move_to_elem(driver, xpath):
        action = ActionChains(driver)
        obj_elm = Navigate.get_element_navigate(driver, xpath)
        action.move_to_element(obj_elm).perform()
        obj_elm.click()


class HelpUserCardCheckMethods(HelpUserCardMethods, Navigate):

    def check_shop_card_in_good_page(self, driver, shop, user_id):
        self.assertIsNotNone(self.get_shop_card_photo(driver, self.check_good.SHOP_LOGO, shop["logo_id"]))
        self.assertIsNotNone(self.get_user_card_name(driver, self.check_good.SHOP_TITLE, shop["name"]))
        self.assertIsNotNone(self.get_user_card_link(driver, self.click_good.LINK_SELLER_AVATAR % user_id))
        
    def check_shop_card_in_good_page_for_seller(self, driver, shop, user_id):
        self.assertIsNotNone(self.get_shop_card_photo(driver, self.check_good.SHOP_LOGO, shop["logo_id"]))
        self.assertIsNotNone(self.get_user_card_name(driver, self.check_good.SHOP_TITLE, shop["name"]))
        self.assertIsNotNone(self.get_user_card_link(driver, self.click_good.LINK_SELLER_AVATAR % user_id))

    def check_user_card_in_shop_page(self, driver, user):
        self.assertIsNotNone(self.get_user_card_photo(driver, self.check_shop.USER_PHOTO, user["avatar_id"]))
        self.assertIsNotNone(self.get_user_card_name(driver, self.check_shop.USER_NAME, user["display_name"]))
        self.assertIsNotNone(self.get_user_card_web_status(driver, self.check_shop.USER_STATUS, user, 'онлайн'))

    def check_user_card_in_search_page(self, driver, user):
        path_user = self.path_search.PATH_SEARCH_USER % user["id"]
        self.assertIsNotNone(self.get_user_card_photo(driver, path_user + self.check_search.USER_PHOTO,
                                                      user["avatar_id"]))
        self.assertIsNotNone(self.get_user_card_name(driver, path_user + self.check_search.USER_NAME,
                                                     user["display_name"]))
        self.assertIsNotNone(self.get_user_card_web_status(driver, path_user + self.check_search.USER_STATUS, user,
                                                           'онлайн'))
        self.assertIsNotNone(self.get_user_card_link(driver, path_user + self.click_search.LINK_SELLER_AVATAR
                                                     % user["id"]))

    def check_user_card_in_buyer_page(self, driver, user):
        self.assertIsNotNone(self.get_user_card_photo(driver, self.check_buyer.USER_PHOTO, user["avatar_id"]))
        self.assertIsNotNone(self.get_user_card_name(driver, self.check_buyer.USER_NAME, user["display_name"]))
        self.assertIsNotNone(self.get_user_card_web_status(driver, self.check_buyer.USER_STATUS, user, 'онлайн'))

    def check_user_card_in_lot_main_page(self, driver, user, num_lot):
        path_main = self.path_main.PATH_USER_LOT % num_lot
        self.assertIsNotNone(self.get_user_card_photo(driver, path_main + self.check_main.USER_PHOTO,
                                                      user["avatar_id"]))
        self.assertIsNotNone(self.get_user_card_name(driver, path_main + self.check_main.USER_NAME_LOT,
                                                     user["display_name"]))
        self.assertIsNotNone(self.get_user_card_link(driver, path_main + self.click_main.LINK_SELLER_AVATAR
                                                     % user["id"]))

    def check_user_card_in_favorite_goods_page(self, driver, user, num_lot):
        path_fg = self.path_favorites.PATH_FAVORITE % num_lot
        self.assertIsNotNone(self.get_user_card_photo(driver, path_fg + self.check_favorites.FG_USER_PHOTO,
                                                      user["avatar_id"]))
        self.assertIsNotNone(self.get_user_card_name(driver, path_fg + self.check_favorites.FG_USER_NAME,
                                                     user["display_name"]))
        self.assertIsNotNone(self.get_user_card_link(driver, path_fg + self.click_favorites.FG_LINK_SELLER_AVATAR
                                                     % user["id"]))

    def check_user_card_in_favorite_users_page(self, driver, user, num_lot):
        path_fg = self.path_user_contact.path_favorites_USER % num_lot
        self.assertIsNotNone(self.get_user_card_photo(driver, path_fg + self.check_user_contact.FU_USER_PHOTO,
                                                      user["avatar_id"]))
        self.assertIsNotNone(self.get_user_card_name(driver, path_fg + self.check_user_contact.FU_USER_NAME,
                                                     user["display_name"]))
        self.assertIsNotNone(self.get_user_card_on_off_line(driver, path_fg + self.check_user_contact.FU_USER_STATUS,
                                                            user))

    def check_user_card_in_chat_page(self, driver, user, num_lot):
        path_ch = self.path_chat.PATH_CHAT_USER % num_lot
        self.assertIsNotNone(self.get_user_card_photo(driver, path_ch + self.check_chat.CH_USER_PHOTO,
                                                      user["avatar_id"]))
        self.assertIsNotNone(self.get_user_card_name(driver, path_ch + self.check_chat.CH_USER_NAME,
                                                     user["display_name"]))

    def check_user_card_in_deal_page(self, driver, user):
        path_dl = self.path_chat.PATH_DEAL_USER_CARD
        self.assertIsNotNone(self.get_user_card_photo(driver, path_dl + self.check_chat.DL_USER_PHOTO,
                                                      user["avatar_id"]))
        self.assertIsNotNone(self.get_user_card_name(driver, path_dl + self.check_chat.DL_USER_NAME,
                                                     user["display_name"]))
        self.assertIsNotNone(self.get_user_card_web_status(driver, path_dl + self.check_chat.DL_USER_STATUS, user))
        self.assertIsNotNone(self.get_user_card_link(driver, path_dl + self.click_chat.DL_LINK_USER_AVATAR
                                                     % user["id"]))

    def check_user_card_in_widget_seller(self, driver, user):
        path_wu = self.path_main.WIDGET_USER
        self.assertIsNotNone(self.get_user_card_photo(driver, path_wu + self.check_main.WU_AVATAR,
                                                      user["avatar_id"]))
        self.assertIsNotNone(self.get_user_card_name(driver, path_wu + self.check_main.WU_NAME,
                                                     user["display_name"]))
        self.assertIsNotNone(self.get_user_card_link(driver, path_wu + self.click_main.HEADER_MY_SHOP))

    def check_user_card_in_widget_buyer(self, driver, user):
        path_wu = self.path_main.WIDGET_USER
        self.assertIsNotNone(self.get_user_card_photo(driver, path_wu + self.check_main.WU_AVATAR,
                                                      user["avatar_id"]))
        self.assertIsNotNone(self.get_user_card_name(driver, path_wu + self.check_main.WU_NAME,
                                                     user["display_name"]))