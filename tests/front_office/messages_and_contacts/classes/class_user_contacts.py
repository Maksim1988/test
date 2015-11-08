# coding=utf-8
import random
import time

import clipboard
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys

from support import service_log
from tests.MainClass import MainClass
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate
from tests.front_office.not_sorted.classes.class_user_card import HelpUserCardCheckMethods

__author__ = 'm.senchuk'


class HelpUserContacts(MainClass):
    TXT_EMPTY_SECTION_SEARCH = "Поиск контактов по номеру телефона\n+7"


class HelpUserContactsMethods(HelpUserContacts):

    @staticmethod
    def get_user_card_photo_in_cont(driver, path, photo_xpath, avatar_id):
        if avatar_id is None:
            p = Navigate.get_element_navigate(driver, path + Navigate.check_good.USER_NO_PHOTO, sleep=0.1, mode=None)
        else:
            p = Navigate.get_element_navigate(driver, path + photo_xpath % avatar_id, sleep=0.1, mode=None)
        return p

    @staticmethod
    def get_user_store_photo_in_cont(driver, path, photo_xpath, logo_id):
        if logo_id is None:
            p = Navigate.get_element_navigate(driver, path + Navigate.check_user_contact.US_LOGO_STUB, sleep=0.1,
                                              mode=None)
        else:
            p = Navigate.get_element_navigate(driver, path + photo_xpath % logo_id, sleep=0.1, mode=None)
        return p

    @staticmethod
    def get_user_store_name(driver, path, name_xpath, name):
        if name is None:
            p = Navigate.get_element_navigate(driver, path + Navigate.check_user_contact.US_WITHOUT_NAME, sleep=0.1,
                                              mode=None)
        else:
            Navigate.get_element_navigate(driver, path + Navigate.check_user_contact.US_LABEL_NAME, sleep=0.1, mode=None)
            p = Navigate.get_element_navigate(driver, path + name_xpath % name, sleep=0.1, mode=None)
        return p

    @staticmethod
    def get_user_store_address(driver, path, name_xpath, address):
        p = False
        if address is None:
            try:
                Navigate.get_element_navigate(driver, path + Navigate.check_user_contact.US_LABEL_ADDRESS, sleep=0.1,
                                              mode=None)
                Navigate.get_element_navigate(driver, path + name_xpath % '', sleep=0.1, mode=None)
                p =True
            except Exception:
                pass
            assert p is False, "Найдено поле адрес магазина, в базе адрес пуст, поля не должно быть"
        else:
            Navigate.get_element_navigate(driver, path + Navigate.check_user_contact.US_LABEL_ADDRESS, sleep=0.1,
                                          mode=None)
            p = Navigate.get_element_navigate(driver, path + name_xpath % address, sleep=0.1, mode=None)
        return p

    @staticmethod
    def get_user_store_description(driver, path, name_xpath, description):
        p = False
        if description is None:
            try:
                Navigate.get_element_navigate(driver, path + name_xpath % '', sleep=0.1, mode=None)
                p = True
            except Exception:
                pass
            assert p is False, "Найдено поле описание, в базе поле описание пусто, поля не должно быть"
        else:
            p = Navigate.get_element_navigate(driver, path + name_xpath % description, sleep=0.1, mode=None)
        return p

    @staticmethod
    def get_count_contacts(driver):
        """ Получить количество пользоватлей в контакт-листе
        :param driver:
        :return:
        """
        count = 0
        try:
            user_id_list = driver.find_elements_by_xpath(Navigate.check_user_contact.COUNT_USERS)
            count = len(user_id_list)
        except Exception:
            pass
        return count

    @staticmethod
    def click_in_contact(driver, user_id):
        """ Нажимаем кнопку в контакты.
        :param driver: ссылка на драйвер
        :param user_id: идентификатор пользователя
        :return: type(bool)
        """
        result = False
        try:
            Navigate.get_page(driver, Navigate.path_buyer.URL_BUYER % user_id)
            in_contact = Navigate.click_user_contact.IN_CONTACT_USER
            btn = Navigate.get_element_navigate(driver, in_contact, sleep=0.1, mode=None)
            HelpAuthCheckMethods.click_button(btn, sleep=0.1)
            result = True
        except Exception:
            result = False
        return result

    @staticmethod
    def get_user_id_contacts(driver):
        """
        Получить список идентификаторов пользователей в контакт-листе
        :param driver:
        :return:
        """
        user_id_list = Navigate.get_category_id_from_page_source(driver, Navigate.path_user_contact.CONTACT_USER_START,
                                                                 Navigate.path_user_contact.CONTACT_USER_END)
        return user_id_list

    @staticmethod
    def add_users_strategy(link_db, mode='all'):
        """

        :param driver:
        :param count:
        :param mode:
        :return:
        """
        users_list = list()
        criteria = "account_status = 'ENABLED' AND id in (%s) AND phone like '7%s' AND length(phone)=11 AND " \
                   "display_name is not NULL"
        if mode == 'all':
            users_list = link_db.accounting.get_user_by_role('1,2,3,4', '100')
            value_list = [str(value["account_details_id"]) for value in users_list]
            string = ','.join(value_list)
            users_list = link_db.accounting.get_user_by_criteria_only(criteria % (string, '%'))
        elif mode == 'buyer':
            users_list = link_db.accounting.get_user_by_role('1', '2,3,4')
            value_list = [str(value["account_details_id"]) for value in users_list]
            string = ','.join(value_list)
            users_list = link_db.accounting.get_user_by_criteria_only(criteria % (string, '%'))
        elif mode == 'seller':
            users_list = link_db.accounting.get_user_by_role('2', '3,4')
            value_list = [str(value["account_details_id"]) for value in users_list]
            string = ','.join(value_list)
            users_list = link_db.accounting.get_user_by_criteria_only(criteria % (string, '%'))
        elif mode == 'disabled':
            users_list = link_db.accounting.get_accounts_by_criteria(criteria="account_status='DISABLED'")
        else:
            service_log.error("Undefined mode='%s'" % mode)
        return users_list

    @staticmethod
    def delete_user_in_contacts(driver, link_db, user_id):
        """
        Удалить пользователей из списка контактов
        :param driver:
        :param count:
        :return:
        """
        Navigate.get_page(driver, Navigate.path_user_contact.URL_FAVORITES_USERS)
        fav_users_list = link_db.accounting.get_fav_user_by_user_id(user_id)
        l = lambda l: list() if l is None else l
        count = len(l(fav_users_list))
        while count != 0:
            btn_user = Navigate.get_element_navigate(driver, Navigate.click_user_contact.LAST_USER, sleep=1)
            HelpAuthCheckMethods.click_button(btn_user, sleep=0.1)
            btn_delete = Navigate.get_element_navigate(driver, Navigate.click_user_contact.BTN_DELETE, sleep=0.1)
            HelpAuthCheckMethods.click_button(btn_delete, sleep=1)
            fav_users_list = link_db.accounting.get_fav_user_by_user_id(user_id)
            count = len(l(fav_users_list))

    @staticmethod
    def delete_first_user_in_cl(driver, fav_user):
        """
        Удалить первого пользователя из списка контактов
        :param driver:
        :return:
        """
        #Navigate.get_page(driver, Navigate.path_user_contact.URL_FAVORITES_USERS)
        usr = Navigate.get_element_navigate(driver, Navigate.check_user_contact.USER_CARD_BY_ID % fav_user["id"])
        HelpAuthCheckMethods.click_button(usr)
        Navigate.get_element_navigate(driver, Navigate.check_user_contact.ACTIVE_USER_CARD_BY_ID % fav_user["id"])
        btn_delete = Navigate.get_element_navigate(driver, Navigate.click_user_contact.BTN_DELETE, sleep=0.1)
        HelpAuthCheckMethods.click_button(btn_delete, sleep=1)
        Navigate.get_element_navigate(driver, Navigate.check_user_contact.MSG_DELETE_USR % fav_user["display_name"])

    @staticmethod
    def set_user_to_contacts(driver, link_db, current_count, need_count=20, mode='all'):
        """
        Наполнить список контактов пользователями
        :param driver:
        :return:
        """
        user_added = list()
        count_add_users = 0
        fail = 0
        service_log.put("Start filling the contact list")
        diff_count = need_count-current_count
        if diff_count <= 0:
            service_log.put("Contact list is full!")
        else:
            users_list = HelpUserContactsMethods.add_users_strategy(link_db, mode)
            random.shuffle(users_list)
            for user in users_list:
                result = HelpUserContactsMethods.click_in_contact(driver, user["account_details_id"])
                if result is True:
                    count_add_users += 1
                    user_added.append(user["account_details_id"])
                    service_log.put("Add user='%s' to contact list" % user["account_details_id"])
                else:
                    fail += 1
                    assert fail == 50, "Пользователи не добавляются."
                if diff_count == count_add_users:
                    service_log.put("End filling the contact list")
                    Navigate.get_page(driver, Navigate.path_user_contact.URL_FAVORITES_USERS)
                    break
        return user_added

    @staticmethod
    def copy_input_str(driver, xpath=None):
        """
        Скопировать строку из input поля
        :param driver:
        :param xpath:
        :return:
        """
        e = lambda driver, xpath: None if xpath is None else Navigate.get_element_navigate(driver, xpath, mode=None)
        element = e(driver, xpath)
        ActionChains(driver).key_down(Keys.CONTROL, element).send_keys("a").key_up(Keys.CONTROL).perform()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys("c").key_up(Keys.CONTROL).perform()

    @staticmethod
    def get_store_list(store):
        if not store:
            store_list = {
                "logo_id": None,
                "name": None,
                "description": None,
                "address": None
            }
        else:
            store_list = store[0]
        return store_list

    @staticmethod
    def generate_phone_not_in_db(link_db):
        """
        Генератор телефона которого нет в базе
        :return:
        """
        f = False
        r = lambda x: True if len(x) == 0 else False
        phone = None
        while f is not True:
            phone = str(random.randrange(70000000000, 75000000000, 1))
            result_db = link_db.accounting.get_user_by_criteria_only(criteria="phone='%s'" % phone)
            f = r(result_db)
        return phone

    @staticmethod
    def find_user_by_name(driver, name, sleep):
        """
        поиск пользователя в контактах по имени
        :param driver:
        :param name:
        :return:
        """
        input_name = Navigate.get_element_navigate(driver, Navigate.input_user_contact.NAME)
        input_name.send_keys(name.decode('utf-8'))
        ActionChains(driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
        time.sleep(sleep)

    @staticmethod
    def clear_input_by_name(driver, sleep=2):
        """
        Удалить введенные данные в поле поиска по имени пользователя в контактах
        :param driver:
        :return:
        """
        ipt = Navigate.get_element_navigate(driver, Navigate.input_user_contact.NAME)
        ipt.click()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).key_down(Keys.DELETE).\
            key_up(Keys.DELETE).perform()
        time.sleep(sleep)

class HelpUserContactsCheckMethods(HelpUserContactsMethods):
    def check_count_contacts(self, driver, link_db, need_count=20, mode='all'):
        count = self.get_count_contacts(driver)
        service_log.put("The number of contacts='%s'" % count)
        self.set_user_to_contacts(driver, link_db, count, need_count, mode)

    def check_delete_users(self, driver, link_db, count):
        self.delete_user_in_contacts(driver, link_db, count)

    def check_card_user_in_contacts(self, driver, user):
        path_fg = Navigate.check_user_contact.USER_CARD_BY_ID % user["id"]
        service_log.put("Start checking user card by user_id='%s'" % user["id"])
        self.assertIsNotNone(Navigate.get_element_navigate(driver, path_fg))
        self.assertIsNotNone(self.get_user_card_photo_in_cont(driver, path_fg, Navigate.check_user_contact.FU_USER_PHOTO,
                                                              user["avatar_id"]))
        self.assertIsNotNone(HelpUserCardCheckMethods.get_user_card_name(driver, path_fg + Navigate.check_user_contact.
                                                                         FU_USER_NAME, user["display_name"]))
        self.assertIsNotNone(HelpUserCardCheckMethods.get_user_card_on_off_line(driver, path_fg + Navigate.
                                                                                check_user_contact.FU_USER_STATUS, user))
        service_log.put("Success checking user card by user_id='%s'" % user["id"])

    def check_active_card_user_in_contacts(self, driver, user):
        path_fg = Navigate.check_user_contact.ACTIVE_USER_CARD_BY_ID % user["id"]
        service_log.put("Start checking user card by user_id='%s'" % user["id"])
        self.assertIsNotNone(Navigate.get_element_navigate(driver, path_fg))
        self.assertIsNotNone(self.get_user_card_photo_in_cont(driver, path_fg, Navigate.check_user_contact.FU_USER_PHOTO,
                                                              user["avatar_id"]))
        self.assertIsNotNone(HelpUserCardCheckMethods.get_user_card_name(driver, path_fg + Navigate.check_user_contact.
                                                                         FU_USER_NAME, user["display_name"]))
        self.assertIsNotNone(HelpUserCardCheckMethods.get_user_card_on_off_line(driver, path_fg + Navigate.
                                                                                check_user_contact.FU_USER_STATUS, user))
        service_log.put("Success checking user card by user_id='%s'" % user["id"])

    def check_card_user_in_search_contact(self, driver, user):
        path_fg = Navigate.check_user_contact.USER_IN_SEARCH
        service_log.put("Start checking user card in search contact by user_id='%s'" % user["id"])
        Navigate.get_element_navigate(driver, path_fg, mode=None, e_msg="Не найдена карточка пользователя в поисковй выдаче")
        self.get_user_card_photo_in_cont(driver, path_fg, Navigate.check_user_contact.FU_USER_PHOTO_IN_SEARCH,
                                         user["avatar_id"])
        HelpUserCardCheckMethods.get_user_card_name(driver, path_fg + Navigate.check_user_contact.FU_USER_NAME,
                                                    user["display_name"])
        HelpUserCardCheckMethods.get_user_card_on_off_line(driver, path_fg + Navigate.check_user_contact.FU_USER_STATUS,
                                                           user)
        service_log.put("Success checking user card in search contact by user_id='%s'" % user["id"])

    def check_active_user_info(self, driver, link_db, user, role):
        path_fg = Navigate.check_user_contact.USER_INFO
        service_log.put("Start checking user card in active contact by user_id='%s'" % user["id"])
        Navigate.get_element_navigate(driver, path_fg, mode=None, e_msg="Не найден блок инфо пользователя у активного "
                                                                        "контакта")
        self.get_user_card_photo_in_cont(driver, path_fg, Navigate.check_user_contact.FU_USER_PHOTO_IN_SEARCH,
                                         user["avatar_id"])
        HelpUserCardCheckMethods.get_user_card_name(driver, path_fg + Navigate.check_user_contact.UI_USER_NAME,
                                                    user["display_name"])
        HelpUserCardCheckMethods.get_user_card_web_status(driver, path_fg + Navigate.check_user_contact.UI_USER_STATUS,
                                                          user)
        Navigate.get_element_navigate(driver, Navigate.click_user_contact.SEND_MSG % user["id"])
        Navigate.get_element_navigate(driver, Navigate.click_user_contact.BTN_DELETE)
        service_log.put("Success checking user card in active contact by user_id='%s'" % user["id"])
        mode = lambda sf, d, ldb, r, u: HelpUserContactsCheckMethods.check_user_store(sf, d, ldb, u) if r is 'seller' else None
        mode(self, driver, link_db, role, user)

    def check_user_store(self, driver, link_db, user):
        sh = lambda u: 0 if u['shop_id'] is None else u['shop_id']
        st = link_db.accounting.get_shop_details_by_shop_id(sh(user))
        store = self.get_store_list(st)
        path_fg = Navigate.check_user_contact.USER_STORE
        service_log.put("Start checking user store in active contact by user_id='%s'" % user['id'])
        Navigate.get_element_navigate(driver, path_fg, sleep=1, mode=None, e_msg="Не найден блок инфо о магазине")
        self.get_user_store_photo_in_cont(driver, path_fg, Navigate.check_user_contact.US_LOGO, store['logo_id'])
        self.get_user_store_name(driver, path_fg, Navigate.check_user_contact.US_NAME, store["name"])
        self.get_user_store_address(driver, path_fg, Navigate.check_user_contact.US_ADDRESS, store["address"])
        self.get_user_store_description(driver, path_fg, Navigate.check_user_contact.US_DESCRIPTION, store["description"])
        Navigate.get_element_navigate(driver, Navigate.click_user_contact.IN_SHOP % user['id'])

    def check_not_found_user(self, driver):
        Navigate.get_element_navigate(driver, Navigate.check_user_contact.NOT_FOUND_USER, mode=None)
        f = False
        try:
            Navigate.get_element_navigate(driver, Navigate.click_user_contact.BTN_ADD_CONTACT, mode=None, sleep=0.1)
            f = True
        except Exception:
            pass
        self.assertFalse(f, "Появилась кнопка добавить пользователя")

    def check_no_add_contact_btn(self, driver):
        f = False
        try:
            Navigate.get_element_navigate(driver, Navigate.click_user_contact.BTN_ADD_CONTACT, mode=None, sleep=0.1)
            f = True
        except Exception:
            pass
        self.assertFalse(f, "Появилась кнопка добавить пользователя")

    def check_can_not_add_yourself(self, driver, user):
        path_fg = Navigate.check_user_contact.USER_IN_SEARCH
        service_log.put("Start checking user card in search contact by user_id='%s'" % user["id"])
        Navigate.get_element_navigate(driver, path_fg, mode=None, e_msg="Не найдена карточка пользователя в поисковй выдаче")
        self.get_user_card_photo_in_cont(driver, path_fg, Navigate.check_user_contact.FU_USER_PHOTO_IN_SEARCH,
                                         user["avatar_id"])
        HelpUserCardCheckMethods.get_user_card_name(driver, path_fg + Navigate.check_user_contact.FU_USER_NAME,
                                                    user["display_name"])
        Navigate.get_element_navigate(driver, path_fg + Navigate.check_user_contact.ITS_YOU, mode=None)
        f = False
        try:
            Navigate.get_element_navigate(driver, Navigate.click_user_contact.BTN_ADD_CONTACT, mode=None, sleep=0.1)
            f = True
        except Exception:
            pass
        self.assertFalse(f, "Появилась кнопка добавить пользователя")

    def check_empty_search_section(self, driver, check_txt=HelpUserContacts.TXT_EMPTY_SECTION_SEARCH):
        txt = Navigate.get_element_navigate(driver, Navigate.check_user_contact.SECTION_SEARCH).text.encode('utf-8')
        self.assertEqual(txt, check_txt, "Форма поиска содержит неверный текст: '%s'" % txt)

    def check_scroll_in_contacts(self, driver, user_last):
        path_fu = Navigate.check_user_contact.COUNT_USERS + '[1]'
        path_lu = Navigate.check_user_contact.USER_CARD_BY_ID % user_last["id"]
        Navigate.get_element_navigate(driver, path_fu).click()
        status_last = False
        try:
            obj_last = Navigate.get_element_navigate(driver, path_lu, sleep=0.1, mode=None)
            self.assertFalse(obj_last.is_displayed())
            status_last = True
        except Exception:
            pass
        self.assertFalse(status_last, "Последний пользователь виден с начала списка")
        for i in range(5):
            ActionChains(driver).key_down(Keys.END).key_up(Keys.END).perform()
            time.sleep(1)
        obj_last = Navigate.get_element_navigate(driver, path_lu)
        self.assertTrue(obj_last.is_displayed())

    def check_input_string(self, driver, check_str, input_xpath=None):
        self.copy_input_str(driver, input_xpath)
        copies_str = clipboard.paste()
        c = lambda c: c.encode('utf-8').replace("(", '').replace(')', '').replace(' ', '').replace('-', '')
        copy_str = c(copies_str)
        self.assertEqual(copy_str, check_str, "Скопированная строка: '%s' не совпадает с введенной: '%s'" %
                         (copy_str, check_str))

    def check_user_added(self, driver, user_name):
        Navigate.get_element_navigate(driver, Navigate.check_user_contact.MSG_SUCCESS_ADD_USER % user_name, mode=None)

    def check_alert_message(self, driver):
        Navigate.get_element_navigate(driver, Navigate.check_user_contact.MSG_ALERT, mode=None)

    def check_buyer_no_btn_in_shop(self, driver, user_id):
        try:
            e = Navigate.get_element_navigate(driver, Navigate.click_user_contact.IN_SHOP % user_id, sleep=0.1,
                                              mode=None)
            self.assertIsNone(e, "У пользователя id='%s' есть кнопка в магазин" % user_id)
        except Exception:
            service_log.put("Пользователь нет кнопки в магазин")

    def check_user_no_in_cl(self, driver, user_id):
        try:
            e = Navigate.get_element_navigate(driver, Navigate.check_user_contact.USER_CARD_BY_ID % user_id, sleep=0.1,
                                              mode=None)
            self.assertIsNone(e, "Пользователь id='%s' остался в контакт листе" % user_id)
        except Exception:
            service_log.put("Пользователь нет в списке контактов")

    def check_delete_first_user_in_cl(self, driver, user_id, fav_usr, link_db):
        fav_users_list_old = link_db.accounting.get_fav_user_in_cl_user(user_id, fav_usr["id"])
        self.assertNotEqual(len(fav_users_list_old), 0 , "Пользователя нет в БД контактах")
        self.delete_first_user_in_cl(driver, fav_usr)
        fav_users_list_new = link_db.accounting.get_fav_user_in_cl_user(user_id, fav_usr["id"])
        self.assertEqual(len(fav_users_list_new), 0, "Пользователь есть в БД контактах: '%s'" % fav_users_list_new)
        HelpUserContactsCheckMethods.check_user_no_in_cl(self, driver, fav_usr["id"])
        driver.refresh()
        Navigate.progress(driver)
        HelpUserContactsCheckMethods.check_user_no_in_cl(self, driver, fav_usr["id"])
        Navigate.get_page(driver, Navigate.path_buyer.URL_BUYER % fav_usr["id"])
        Navigate.get_element_navigate(driver, Navigate.click_user_contact.IN_CONTACT_USER, sleep=0.1, mode=None)
        driver.back()

    def check_find_full_name(self, driver, user, sleep=2):
        self.find_user_by_name(driver, user["display_name"], sleep)
        user = Navigate.get_element_navigate(driver, Navigate.check_user_contact.USER_CARD_BY_ID % user["id"])
        HelpAuthCheckMethods.click_button(user)

    def check_find_part_name(self, driver, part_name, sleep=2):
        count_contacts_old = self.get_count_contacts(driver)
        self.find_user_by_name(driver, part_name, sleep)
        count_contacts_new = self.get_count_contacts(driver)
        self.assertGreater(count_contacts_old, count_contacts_new, "После ввода части имени количество контактов "
                                                                   "уменьшилось")
        user = Navigate.get_element_navigate(driver, Navigate.click_user_contact.LAST_USER)
        HelpAuthCheckMethods.click_button(user)