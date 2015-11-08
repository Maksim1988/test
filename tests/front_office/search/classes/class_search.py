# -*- coding: utf-8 -*-
import math

from support import service_log
from tests.MainClass import MainClass
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate

__author__ = 'm.senchuk'


class SearchData(MainClass):
    USER_NAME = "пользователь"
    F_MAP = {
        True: False,
        False: True
    }


class SearchMethods(SearchData):
    @staticmethod
    def search_form(driver):
        """
        Метод получает объекты формы поиска
        :param driver:
        :return: словарь объектов формы поиска
        """
        search_form = {
            "input": Navigate.element_is_present(driver, Navigate.input_main.SEARCH),
            "btn": Navigate.element_is_present(driver, Navigate.click_main.SEARCH_BTN)
        }
        service_log.put('Получены объекты формы поиска')
        return search_form

    @staticmethod
    def left_menu(driver):
        """
        Метод получает объекты меню слева на странице поиска и количество найденных товаров и пользователей
        :param driver:
        :return: словарь объектов формы меню
        """
        active_url = driver.current_url.encode('utf-8')
        type_search = active_url[active_url.rfind('/') + 1:active_url.rfind('?')]
        menu = {
            "title": Navigate.element_is_present(driver, Navigate.check_search.TITLE_SEARCH),
            "goods": Navigate.element_is_present(driver, Navigate.click_search.GOODS_MENU[type_search]),
            "users": Navigate.element_is_present(driver, Navigate.click_search.USERS_MENU[type_search]),
        }
        menu.update({"count_goods": menu["goods"].text.encode('utf-8').strip("Товары ")})
        menu.update({"count_users": menu["users"].text.encode('utf-8').strip("Пользователи ")})
        service_log.put("Получены объекты левого меню на странице поиска")
        return menu

    @staticmethod
    def good_card_short(driver, good):
        """
        Метод получает объект короткая карточка товара по заданным данным
        :param good: данные товара
        :return:
        """
        main_picture = good["content"][u'pictures'][u'value'][0].encode('utf-8')
        title = good["content"][u'title'][u'value'].encode('utf-8')
        min_stock = good["content"][u'min_stock'][u'value']
        try:
            price = str(good["content"][u'price'][u'value'][u'significand'])
            if 3 < len(price) < 7:
                price = price[:-3] + " " + price[-3:]   # здесь в кавычках неразрывные пробелы
            elif len(price) >= 7:
                price = price[:-6] + " " + price[-6:-3] + " " + price[-3:]
        except Exception:
            price = "---"
        g_card = {
            "card": Navigate.element_is_present(driver, Navigate.click_search.GOOD_CARD_BY_ID % good["ware_id"]),
            "picture": Navigate.element_is_present(driver, Navigate.click_search.GOOD_PICTURE % (good["ware_id"],
                                                                                                 main_picture)),
            "title": Navigate.element_is_present(driver, Navigate.click_search.GOOD_TITLE % (good["ware_id"], title)),
            "price": Navigate.element_is_present(driver, Navigate.click_search.GOOD_PRICE % (good["ware_id"], price)),
            "min_stock": Navigate.element_is_present(driver, Navigate.click_search.GOOD_MIN_STOCK % (good["ware_id"],
                                                                                                     min_stock)),
        }
        service_log.put("Короткая карточка товара найдена. Id: %s" % good["ware_id"])
        return g_card

    @staticmethod
    def none_found(driver, test_string):
        """
        Метод получает форму пользователей и товаров не найдено
        :param driver:
        :param test_string:
        """
        form = {
            'title': Navigate.element_is_present(driver, Navigate.check_search.CATALOG_ALL_EMPTY % test_string),
            'description': Navigate.element_is_present(driver, Navigate.check_search.CATALOG_EMPTY_DESC),
            'btn_catalog': Navigate.element_is_present(driver, Navigate.click_search.BTN_CATALOG)
        }
        return form

    @staticmethod
    def found_only_users(driver, test_string):
        """
        Метод получает форму товаров не найдено но найдены пользователи
        :param driver:
        :param test_string:
        :return:
        """
        form = {
            'title': Navigate.element_is_present(driver, Navigate.check_search.CATALOG_GOOD_EMPTY % test_string),
            'description': Navigate.element_is_present(driver, Navigate.check_search.CATALOG_GOOD_EMPTY_DESC),
            'btn_to_users': Navigate.element_is_present(driver, Navigate.click_search.BTN_TO_USERS % test_string)
        }
        return form

    @staticmethod
    def found_only_goods(driver, test_string):
        """
        Метод получает форму пользователей не найдено но найдены товары
        :param driver:
        :param test_string:
        :return:
        """
        form = {
            'title': Navigate.element_is_present(driver, Navigate.check_search.CATALOG_USER_EMPTY % test_string),
            'description': Navigate.element_is_present(driver, Navigate.check_search.CATALOG_USER_EMPTY_DESC),
            'btn_to_goods': Navigate.element_is_present(driver, Navigate.click_search.BTN_TO_GOODS % test_string)
        }
        return form

    @staticmethod
    def get_good_ids(driver, len_id=32):
        """
        Получить идентификаторы товаров со страницы
        :param driver:
        :param len_id: длина идентификатора товара
        :return:
        """
        source_page = driver.page_source.encode('utf-8')
        list_source = source_page.split('/goods/')
        list_source = list_source[1:]
        list_ids = ["'" + i[:len_id] + "'" for i in list_source]
        str_ids = ','.join(list_ids)
        return str_ids

    @staticmethod
    def get_user_ids(driver):
        source_page = driver.page_source.encode('utf-8')
        list_source = source_page.split(Navigate.path_search.PATH_FIND_USER)
        list_source = list_source[1:]
        list_ids = [i[:i.find('"')] for i in list_source]
        str_ids = ','.join(list_ids)
        return str_ids


class SearchCheckMethods(SearchMethods):
    def search_by_user(self, driver, user, count_users, e_msg=''):
        """
        Метод проверяет наличие пользователя в результатах поиска с использованием пагинации
        :param driver:
        :param user:
        """
        fail = True
        page = 1
        self.assertNotEqual(int(count_users), 0, "Не найдено пользователей")
        all_pages = int(math.ceil(int(count_users) / 40.0))
        while all_pages >= 1:
            try:
                Navigate.element_is_present(driver, Navigate.click_search.LINK_SELLER_AVATAR % user["id"], wait=2)
                Navigate.element_is_present(driver, Navigate.click_search.SELLER_NAME_WITH_ID % (user['id'],
                                                                                                 user["display_name"])
                                            )
                fail = False
                break
            except Exception:
                all_pages -= 1
                if all_pages >= 1:
                    page += 1
                    Navigate.element_click(driver, Navigate.click_search.PAG_PAGE % page)
        self.assertFalse(fail, e_msg)

    def search_by_good(self, driver, good, count_goods, e_msg=''):
        """
        Метод проверяет наличие товара в результатах поиска с использованием пагинации
        :param driver:
        :param good:
        """
        fail = True
        page = 1
        self.assertNotEqual(int(count_goods), 0, "Не найдено товаров")
        all_pages = int(math.ceil(int(count_goods) / 40.0))
        while all_pages >= 1:
            try:
                self.good_card_short(driver, good)
                fail = False
                break
            except Exception:
                all_pages -= 1
                if all_pages >= 1:
                    page += 1
                    Navigate.element_click(driver, Navigate.click_search.PAG_PAGE % page)
        self.assertFalse(fail, e_msg)

    def search_by_no_user(self, driver, user, count_users, e_msg=''):
        """
        Метод проверяет отсутствие пользователя в результатах поиска с использованием пагинации
        :param driver:
        :param user:
        """
        fail = False
        page = 1
        all_pages = int(math.ceil(int(count_users) / 40.0))
        while all_pages >= 1:
            try:
                Navigate.element_is_present(driver, Navigate.click_search.LINK_SELLER_AVATAR % user["id"], wait=2)
                Navigate.element_is_present(driver, Navigate.click_search.SELLER_NAME_WITH_ID % (user['id'],
                                                                                                 user["display_name"])
                                            )
                fail = True
                break
            except Exception:
                all_pages -= 1
                if all_pages >= 1:
                    page += 1
                    Navigate.element_click(driver, Navigate.click_search.PAG_PAGE % page)
        self.assertFalse(fail, e_msg)

    def search_by_no_good(self, driver, good, count_goods, e_msg=''):
        """
        Метод проверяет отсутствие товара в результатах поиска с использованием пагинации
        :param driver:
        :param good:
        """
        fail = False
        page = 1
        all_pages = int(math.ceil(int(count_goods) / 40.0))
        while all_pages >= 1:
            try:
                self.good_card_short(driver, good)
                fail = True
                break
            except Exception:
                all_pages -= 1
                if all_pages >= 1:
                    page += 1
                    Navigate.element_click(driver, Navigate.click_search.PAG_PAGE % page)
        self.assertFalse(fail, e_msg)

    def pagination(self, driver, count, section_xpath, items_in_page=40, e_msg=''):
        """
        Проверка пагинации
        :param driver:
        :param count:
        :param section_xpath:
        :param e_msg:
        :return:
        """
        current_page = 1
        all_pages = int(math.ceil(int(count) / (items_in_page + 0.0)))
        remaining_pages = all_pages - current_page
        if remaining_pages == 0:
            Navigate.element_is_none(driver, Navigate.click_search.PAG_PAGE % current_page)
            obj_on_page = Navigate.elements_is_present(driver, section_xpath)
            on_page = len(obj_on_page)
            self.assertEqual(count, on_page, e_msg)
        elif remaining_pages >= 1:
            count_on_pages = 0
            while remaining_pages >= 0:
                obj_on_page = Navigate.elements_is_present(driver, section_xpath)
                on_page = len(obj_on_page)
                next_page = current_page + 1
                if remaining_pages != 0:
                    self.assertEqual(items_in_page, on_page, e_msg)
                    Navigate.element_click(driver, Navigate.click_search.PAG_PAGE % next_page)
                else:
                    self.assertEqual(count-count_on_pages, on_page, e_msg)
                count_on_pages += on_page
                current_page += 1
                remaining_pages -= 1
            self.assertEqual(count, count_on_pages, e_msg)
        else:
            self.assertGreaterEqual(remaining_pages, 0, "Кол-во оставшихся страниц [%s] отрицательно" % remaining_pages)

    def good_state_pagination(self, driver, count, db_link, goods_on_page=40, e_msg=''):
        """
        Проверка что товары только в статусе accepted, belived
        :param driver:
        :param count:
        :param goods_on_page:
        :param e_msg:
        :return:
        """
        current_page = 1
        all_pages = int(math.ceil(int(count) / (goods_on_page + 0.0)))
        remaining_pages = all_pages - current_page
        count_on_pages = 0
        obj_s = ''
        while remaining_pages >= 0:
            str_ids = self.get_good_ids(driver)
            self.assertNotEqual(obj_s, str_ids, "Переход на след. страницу не произошел, товары совпадают")
            goods = db_link.warehouse.get_wares_by_id_and_moderation_state(str_ids, '1,2')
            next_page = current_page + 1
            if remaining_pages != 0:
                self.assertEqual(goods_on_page, len(goods), e_msg)
                Navigate.element_click(driver, Navigate.click_search.PAG_PAGE % next_page)
            else:
                self.assertEqual(count-count_on_pages, len(goods), e_msg)
            count_on_pages += len(goods)
            obj_s = str_ids
            current_page += 1
            remaining_pages -= 1
        self.assertEqual(count, count_on_pages, e_msg)

    def user_state_pagination(self, driver, count, db_link, users_on_page=40, e_msg=''):
        """
        Проверка что пользователи только активные продавцы
        :param driver:
        :param count:
        :param goods_on_page:
        :param e_msg:
        :return:
        """
        current_page = 1
        all_pages = int(math.ceil(int(count) / (users_on_page + 0.0)))
        remaining_pages = all_pages - current_page
        count_on_pages = 0
        obj_s = ''
        while remaining_pages >= 0:
            str_ids = self.get_user_ids(driver)
            self.assertNotEqual(obj_s, str_ids, "Переход на след. страницу не произошел, пользователи совпадают")
            users = db_link.accounting.get_users_by_id_and_permissions(str_ids, '2,6', '3,4,7,8')
            next_page = current_page + 1
            if remaining_pages != 0:
                self.assertEqual(users_on_page, len(users), e_msg)
                Navigate.element_click(driver, Navigate.click_search.PAG_PAGE % next_page)
            else:
                self.assertEqual(count-count_on_pages, len(users), e_msg)
            count_on_pages += len(users)
            obj_s = str_ids
            current_page += 1
            remaining_pages -= 1
        self.assertEqual(count, count_on_pages, e_msg)

    def user_card_in_search(self, driver, user):
        """
        Метод проверяет карточку пользователя на странице поиска
        :param driver:
        :param user:
        """
        pass
