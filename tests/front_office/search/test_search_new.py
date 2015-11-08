# -*- coding: utf-8 -*-
"""
Feature: ПОИСК
Description: Набор тестов для проверки функционала поиск на сайте
"""
from unittest import skip

from support import service_log
from support.utils.db import databases
from support.utils import common_utils
from support.utils.common_utils import generate_sha256
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.search.classes.class_search import SearchCheckMethods as Search
from tests.front_office.settings.classes.class_profile_settings import HelpProfileSettingsCheckMethods
from tests.worker_warehouse.class_warehouse import WarehouseCheckMethods
from support.utils.common_utils import priority


class Test_I_can_Find_User(WarehouseCheckMethods, HelpAuthCheckMethods, HelpProfileSettingsCheckMethods, Search):
    """
    Story: Я могу найти пользователя
    """
    
    @classmethod
    def setUp(cls):
        """ Подготовка окружения """
        cls.driver = HelpLifeCycleMethods.get_driver()
        cls.go_to_main_page(cls.driver)  # Переходим на главную
        service_log.preparing_env(cls)
        
    @priority("Must")
    def test_search_active_seller(self):
        """
        Title: Я могу найти только Продавцов & Активный. Остальные не попадают в результаты поиска
        (Продавец & Disabled, Покупатель & Ждёт активации, Модератор & Активный, Администратор & Активный)
        """
        service_log.run(self)
        seller_id = AccountingMethods.get_default_user_id(role='seller')
        seller = databases.db1.accounting.get_user_by_account_id(seller_id)[0]
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=seller["display_name"])
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.element_click(self.driver, l_menu["users"], change_page_url=True)
        e_msg = "Пользователь не найден в результатах поиска"
        self.search_by_user(self.driver, seller, l_menu["count_users"], e_msg=e_msg)
        self.user_card_in_search(self.driver, seller)

    @priority("High")
    def test_search_disabled_seller(self):
        """
        Title: Я не могу найти Продавец & Disabled не попадают в результаты поиска
        """
        service_log.run(self)
        seller = databases.db1.accounting.get_user_by_criteria("DISABLED", "shop_id is not NULL")[0]
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=seller["display_name"])
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.element_click(self.driver, l_menu["users"], change_page_url=True)
        e_msg = "Пользователь найден в результатах поиска"
        self.search_by_no_user(self.driver, seller, l_menu["count_users"], e_msg=e_msg)

    @priority("high")
    def test_search_moderator(self):
        """
        Title: Я не могу найти Модератор & Активный не попадают в результаты поиска
        """
        service_log.run(self)
        moder_id = AccountingMethods.get_default_user_id(role='moderator')
        moder = databases.db1.accounting.get_user_by_account_id(moder_id)[0]
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=moder["display_name"])
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.element_click(self.driver, l_menu["users"], change_page_url=True)
        e_msg = "Пользователь найден в результатах поиска"
        self.search_by_no_user(self.driver, moder, l_menu["count_users"], e_msg=e_msg)

    @priority("High")
    def test_search_admin(self):
        """
        Title: Я не могу найти Администратор & Активный не попадают в результаты поиска
        """
        service_log.run(self)
        admin_id = AccountingMethods.get_default_user_id(role='admin')
        admin = databases.db1.accounting.get_user_by_account_id(admin_id)[0]
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=admin["display_name"])
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.element_click(self.driver, l_menu["users"], change_page_url=True)
        e_msg = "Пользователь найден в результатах поиска"
        self.search_by_no_user(self.driver, admin, l_menu["count_users"], e_msg=e_msg)

    @priority("Must")
    def test_full_name(self):
        """
        Title: Я могу найти пользователя по  полному совпадению с Именем пользователя
        """
        service_log.run(self)
        criteria = "shop_id is not NULL and length(display_name)>8"
        seller = databases.db1.accounting.get_user_by_criteria("ENABLED", criteria)[0]
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=seller["display_name"])
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.element_click(self.driver, l_menu["users"], change_page_url=True)
        e_msg = "Пользователь не найден в результатах поиска"
        self.search_by_user(self.driver, seller, l_menu["count_users"], e_msg=e_msg)

    @priority("High")
    def test_part_name(self):
        """
        Title: Я могу найти пользователя по  частичному совпадению с Именем пользователя
        """
        service_log.run(self)
        criteria = "shop_id is not NULL and length(display_name)>10 and display_name like '% %'"
        seller = databases.db1.accounting.get_user_by_criteria("ENABLED", criteria)[0]
        s_form = self.search_form(self.driver)
        name = seller["display_name"].split(' ')
        part_name = name[0]
        self.input_str(s_form["input"], string=part_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.element_click(self.driver, l_menu["users"], change_page_url=True)
        e_msg = "Пользователь не найден в результатах поиска"
        self.search_by_user(self.driver, seller, l_menu["count_users"], e_msg=e_msg)

    @priority("High")
    def test_part_shop_name(self):
        """
        Title: Я могу найти пользователя по фрагменту текста из Названия магазина
        """
        service_log.run(self)
        shops = databases.db1.accounting.get_shop_details_by_criteria("length(name) > 16 and name like '% %'")
        shop_ids = [str(i["shop_id"]) for i in shops]
        shop_ids_str = ','.join(shop_ids)
        seller = databases.db1.accounting.get_user_by_criteria("ENABLED", "shop_id in (%s)" % shop_ids_str)[0]
        s_form = self.search_form(self.driver)
        shop_info = databases.db1.accounting.get_shop_details_by_criteria("shop_id=%s" % seller["shop_id"])[0]
        name = shop_info["name"]
        shop_name = name.split(' ')
        part_name = shop_name[0]
        self.input_str(s_form["input"], string=part_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.element_click(self.driver, l_menu["users"], change_page_url=True)
        e_msg = "Пользователь не найден в результатах поиска"
        self.search_by_user(self.driver, seller, l_menu["count_users"], e_msg=e_msg)

    @priority("High")
    def test_part_shop_description(self):
        """
        Title: Я могу найти пользователя по фрагменту текста из Описания магазина
        """
        service_log.run(self)
        shops = databases.db1.accounting.get_shop_details_by_criteria("length(description) > 10 and "
                                                                      "description like '% %'")
        shop_ids = [str(i["shop_id"]) for i in shops]
        shop_ids_str = ','.join(shop_ids)
        seller = databases.db1.accounting.get_user_by_criteria("ENABLED", "shop_id in (%s)" % shop_ids_str)[0]
        s_form = self.search_form(self.driver)
        shop_info = databases.db1.accounting.get_shop_details_by_criteria("shop_id=%s" % seller["shop_id"])[0]
        description = shop_info["description"].split(' ')
        part_description = description[0]
        self.input_str(s_form["input"], string=part_description)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.element_click(self.driver, l_menu["users"], change_page_url=True)
        e_msg = "Пользователь не найден в результатах поиска"
        self.search_by_user(self.driver, seller, l_menu["count_users"], e_msg=e_msg)

    @skip('manual')
    @priority("Low")
    def test_not_search_by_phoe_email_id(self):
        """
        Title: Я не могу найти пользователя по номеру телефона, e-mail или id_пользователя
        """
        service_log.run(self)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class Test_I_can_Find_Good(WarehouseCheckMethods, HelpAuthCheckMethods, HelpProfileSettingsCheckMethods, Search):
    """
    Story: Я могу найти Товар
    """
    
    @classmethod
    def setUp(cls):
        """ Подготовка окружения """
        cls.driver = HelpLifeCycleMethods.get_driver()
        cls.go_to_main_page(cls.driver)  # Переходим на главную
        service_log.preparing_env(cls)
    
    @priority("Must")
    def test_search_active_good(self, stock_state='PUBLISHED'):
        """
        Title: Я могу найти только активные товары, неактивные товары не попадают в результаты поиска
        """
        service_log.run(self)
        stock_state_id = databases.db1.warehouse.get_id_stock_state_by_name(stock_state)[0]["id"]
        criteria = "stock_state_id=%s and length(content->'title'->>'value') > 16" % str(stock_state_id)
        good = databases.db1.warehouse.get_wares_by_criteria(criteria)[0]
        c_good = good["content"]
        good_name = c_good["title"]["value"].encode('utf-8').strip()
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=good_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        e_msg = "Товар не найден в результатах поиска"
        self.search_by_good(self.driver, good, l_menu["count_goods"], e_msg=e_msg)

    @priority("Must")
    def test_search_inactive_good(self, stock_state='HIDDEN'):
        """
        Title: Неактивные товары не попадают в результаты поиска
        """
        service_log.run(self)
        stock_state_id = databases.db1.warehouse.get_id_stock_state_by_name(stock_state)[0]["id"]
        criteria = "stock_state_id=%s and length(content->'title'->>'value') > 16" % str(stock_state_id)
        good = databases.db1.warehouse.get_wares_by_criteria(criteria)[0]
        c_good = good["content"]
        good_name = c_good["title"]["value"].encode('utf-8').strip()
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=good_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        e_msg = "Товар найден в результатах поиска"
        self.search_by_no_good(self.driver, good, l_menu["count_goods"], e_msg=e_msg)

    @priority("Must")
    def test_full_good_title(self, stock_state='PUBLISHED'):
        """
        Title: Я могу найти товар по полному совпадению с Названием товара
        """
        service_log.run(self)
        stock_state_id = databases.db1.warehouse.get_id_stock_state_by_name(stock_state)[0]["id"]
        criteria = "stock_state_id=%s and length(content->'title'->>'value') > 7" % str(stock_state_id)
        good = databases.db1.warehouse.get_wares_by_criteria(criteria)[0]
        c_good = good["content"]
        good_name = c_good["title"]["value"].encode('utf-8').strip()
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=good_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        e_msg = "Товар не найден в результатах поиска"
        self.search_by_good(self.driver, good, l_menu["count_goods"], e_msg=e_msg)

    @priority("High")
    def test_part_good_title(self, stock_state='PUBLISHED'):
        """
        Title: Я могу найти товар по частичному совпадению с Названием товара
        """
        service_log.run(self)
        stock_state_id = databases.db1.warehouse.get_id_stock_state_by_name(stock_state)[0]["id"]
        criteria = "stock_state_id=%s and length(content->'title'->>'value') > 24 and " \
                   "content->'title'->>'value' like '%s'" % (str(stock_state_id), '% %')
        good = databases.db1.warehouse.get_wares_by_criteria(criteria)[0]
        c_good = good["content"]
        good_name = c_good["title"]["value"].encode('utf-8').strip()
        name = good_name.split(' ')
        part_name = name[0]
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=part_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        e_msg = "Товар не найден в результатах поиска"
        self.search_by_good(self.driver, good, l_menu["count_goods"], e_msg=e_msg)

    @priority("High")
    def test_part_good_description(self, stock_state='PUBLISHED'):
        """
        Title: Я могу найти товар по фрагменту текста из Описания товара
        """
        service_log.run(self)
        stock_state_id = databases.db1.warehouse.get_id_stock_state_by_name(stock_state)[0]["id"]
        criteria = "stock_state_id=%s and length(content->'description'->>'value') > 50 and " \
                   "content->'description'->>'value' like '%s'" % (str(stock_state_id), '% %')
        good = databases.db1.warehouse.get_wares_by_criteria(criteria)[0]
        c_good = good["content"]
        good_description = c_good["description"]["value"].encode('utf-8').strip()
        description = good_description.split(' ')
        part_description = description[0]
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=part_description)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        e_msg = "Товар не найден в результатах поиска"
        self.search_by_good(self.driver, good, l_menu["count_goods"], e_msg=e_msg)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()
        

class Test_If_search_result_empty(WarehouseCheckMethods, HelpAuthCheckMethods, HelpProfileSettingsCheckMethods, Search):
    """
    Story: Если результаты поиска пустые, то отображается заглушка
    """
    
    @classmethod
    def setUp(cls):
        """ Подготовка окружения """
        cls.driver = HelpLifeCycleMethods.get_driver()
        cls.go_to_main_page(cls.driver)  # Переходим на главную
        service_log.preparing_env(cls)
    
    @priority("High")
    def test_on_request_none_found(self):
        """
        Title: Если по запросу поиска не найдено ни товаров, ни пользователей - то отображается соответствующая заглушка.
        Description:
        * Текст заглушки "По запросу %запрос% пользователей и товаров не найдено Пожалуйста, проверьте правильность написания или воспользуйтесь каталогом"
        * Счетчики кол-ва товаров и кол-ва пользователей по нулям
        * Я могу перейти в каталог по кнопке "Перейти в каталог"
        """
        service_log.run(self)
        s_form = self.search_form(self.driver)
        test_str = common_utils.random_string(length=20)
        self.input_str(s_form["input"], string=test_str)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.assertEqual(int(l_menu['count_goods']), 0, "Количество товаров не 0")
        self.assertEqual(int(l_menu['count_users']), 0, "Количество пользователей не 0")
        none_form = self.none_found(self.driver, test_str)
        self.element_click(self.driver, none_form['btn_catalog'], change_page_url=True)

    @priority("Medium")
    def test_only_users_found(self):
        """
        Title: Если по запросу поиска не найдено товаров, но найдены пользователи - то отображается соответствующая заглушка.
        Description:
        * Текст заглушки "По запросу %запрос% товаров не найдено. Зато мы нашли [n] пользователей по этому запросу"
        * Счетчик кол-ва товаров равен нулю.
        * Я могу перейти на вкладку "Пользователи" по кнопке "Смотреть пользователей"
        """
        service_log.run(self)
        # Берем тестового продавца на магазине которого будут проводиться проверки
        test_seller_id = AccountingMethods.get_default_user_id(role='seller')
        user = databases.db1.accounting.get_user_by_account_id(test_seller_id)[0]

        # Подготавливаем тестовое мия
        test_name = common_utils.random_string(length=20)

        AccountingMethods.save_user_password(user_id=user["id"], hash_passwd=user["code_value"], salt=user["salt"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, user["salt"])
        databases.db1.accounting.update_user_password(user["id"], hash_res_new)

        self.go_main(self.driver, phone=user["phone"], passwd=default_new_passwd, flag_auth=True)

        # Переход на настройки пользователя и изменение имени на тестовое
        self.get_page(self.driver, self.path_settings.PATH_PROFILE_SETTINGS)

        # Получаем объекты input оформ
        display_name = self.get_obj_input(self.driver, user["display_name"],
                                          path_block=self.path_settings.PATH_COMMON_INFO,
                                          path_input=self.input_settings.FORM_DISPLAY_NAME)

        self.clear_input_row(self.driver, display_name)  # Очистка введенных данных из input форм
        display_name.send_keys(test_name)  # Ввод тестовых данных

        # Получаем объект кнопки Сохранить и нажимаем Сохранить
        common_info_submit = self.get_submit_button(self.driver, self.path_settings.PATH_COMMON_INFO)
        self.element_click(self.driver, common_info_submit, change_page_url=False)
        self.go_to_main_page(self.driver)
        u_user = databases.db1.accounting.get_user_by_account_id(test_seller_id)[0]
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=test_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.assertEqual(int(l_menu['count_goods']), 0, "Количество товаров не 0")
        self.assertEqual(int(l_menu['count_users']), 1, "Количество пользователей не 1")
        only_users_form = self.found_only_users(self.driver, test_name)
        self.element_click(self.driver, only_users_form['btn_to_users'])
        self.search_by_user(self.driver, u_user, l_menu['count_users'])

    @priority("Medium")
    def test_only_goods_found(self):
        """
        Title: Если по запросу поиска не найдено пользователей, но найдены товары- то отображается соответствующая заглушка (...)
        Description:
        * Текст заглушки "По запросу %запрос% пользователей не найдено. Зато мы нашли [n] товаров по этому запросу"
        * Счетчик кол-ва пользователей равен нулю.
        * Я могу перейти на вкладку "Товары" по кнопке "Смотреть товары"
        """
        service_log.run(self)
        service_log.run(self)
        # Берем тестового продавца на магазине которого будут проводиться проверки
        test_seller_id = AccountingMethods.get_default_user_id(role='seller')
        user = databases.db1.accounting.get_user_by_account_id(test_seller_id)[0]

        # Подготавливаем тестовое мия
        test_name = common_utils.random_string(length=20)

        AccountingMethods.save_user_password(user_id=user["id"], hash_passwd=user["code_value"], salt=user["salt"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, user["salt"])
        databases.db1.accounting.update_user_password(user["id"], hash_res_new)

        self.go_main(self.driver, phone=user["phone"], passwd=default_new_passwd, flag_auth=True)
        good = databases.db1.warehouse.get_wares_by_criteria(criteria="shop_id=%s and stock_state_id=2" % user['id'])[0]
        # Переход на едактирование товара и изменение названия на тестовое
        self.get_page(self.driver, self.path_my_goods.URL_EDIT_GOOD % good['ware_id'])
        # Получаем объекты input оформ
        display_name = self.element_is_present(self.driver, self.input_my_goods.ADD_GOOD_NAME)
        self.clear_input_row(self.driver, display_name)  # Очистка введенных данных из input форм
        display_name.send_keys(test_name)  # Ввод тестовых данных

        # Получаем объект кнопки Сохранить и нажимаем Сохранить
        self.element_click(self.driver, self.click_my_goods.ADD_GOOD_BTN_PUBLISH, change_page_url=True)
        self.go_to_main_page(self.driver)
        u_good = databases.db1.warehouse.get_wares_by_criteria(criteria="ware_id='%s'" % good['ware_id'])[0]
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=test_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.assertEqual(int(l_menu['count_goods']), 1, "Количество товаров не 1")
        self.assertEqual(int(l_menu['count_users']), 0, "Количество пользователей не 0")
        self.element_click(self.driver, l_menu['users'])
        only_users_form = self.found_only_goods(self.driver, test_name)
        self.element_click(self.driver, only_users_form['btn_to_goods'])
        self.search_by_good(self.driver, u_good, l_menu['count_goods'])

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()
        

class Test_Good_Listing_Result_Search(WarehouseCheckMethods, HelpAuthCheckMethods, HelpProfileSettingsCheckMethods,
                                      Search):
    """
    Story: Листинг результатов поиска (Товары) + Пагинатор
    """
    
    @classmethod
    def setUp(cls):
        """ Подготовка окружения """
        cls.driver = HelpLifeCycleMethods.get_driver()
        cls.go_to_main_page(cls.driver)  # Переходим на главную
        service_log.preparing_env(cls)
    
    @priority("Low")
    def test_default_tab_goods(self, stock_state="PUBLISHED"):
        """
        Title: В результатах поиска по-умолчанию открыта вкладка "Товары"
        """
        service_log.run(self)
        stock_state_id = databases.db1.warehouse.get_id_stock_state_by_name(stock_state)[0]["id"]
        criteria = "stock_state_id=%s and length(content->'title'->>'value') > 16" % str(stock_state_id)
        good = databases.db1.warehouse.get_wares_by_criteria(criteria)[0]
        c_good = good["content"]
        good_name = c_good["title"]["value"].encode('utf-8').strip()
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=good_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        self.left_menu(self.driver)
        self.element_is_present(self.driver, self.check_search.SECTION_GOODS)

    @priority("Medium")
    def test_count_found_goods_equal_tab_goods(self, stock_state="PUBLISHED"):
        """
        Title: Количество найденных товаров на странице соответствует числу, указанному напротив раздела
        """
        service_log.run(self)
        stock_state_id = databases.db1.warehouse.get_id_stock_state_by_name(stock_state)[0]["id"]
        criteria = "stock_state_id=%s and length(content->'title'->>'value') > 30" % str(stock_state_id)
        good = databases.db1.warehouse.get_wares_by_criteria(criteria)[0]
        c_good = good["content"]
        good_name = c_good["title"]["value"].encode('utf-8').strip()
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=good_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        c_goods = len(self.driver.find_elements_by_xpath(self.check_search.SECTION_GOODS))
        e_msg = "Количество найденных товаров на странице [%s] не равно указанному напротив раздела [%s]"
        self.assertEqual(int(l_menu["count_goods"]), c_goods, e_msg % (l_menu["count_goods"], c_goods))

    @priority("Medium")
    def test_pagination_goods(self, good_name='пла', good_on_page=40):
        """
        Title: На страницу с результатами поиска помещается 40 экспресс карточек товара, а остальное скрыто пагинацией (...)
        Description:
        * Если товаров 40 - пагинатор не отображается
        * Если товаров 41 - отображается вторая страница пагинатора
        """
        service_log.run(self)
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=good_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.assertNotEqual(l_menu["count_goods"], '', "Не получены результаты поиска")
        self.pagination(self.driver, int(l_menu["count_goods"]), self.check_search.SECTION_GOODS, good_on_page)

    @priority("Medium")
    def test_goods_belived_accepted(self, good_name='пла', good_on_page=40):
        """
        Title: Отображаются только товары: Active & (Belived or Accepted)
        """
        service_log.run(self)
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=good_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.assertNotEqual(l_menu["count_goods"], '', "Не получены результаты поиска")
        self.good_state_pagination(self.driver, int(l_menu["count_goods"]), databases.db1, good_on_page)

    @priority("High")
    def test_switch_between_tabs(self, test_string='п'):
        """
        Title: Click: Я могу переключаться между вкладками Товары и Пользователи, чтобы смотреть результаты в этих категориях
        """
        service_log.run(self)
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=test_string)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.assertGreater(int(l_menu["count_goods"]), 0, "Не получены результаты поиска о товарам")
        self.assertGreater(int(l_menu["count_users"]), 0, "Не получены результаты поиска о пользователям")
        self.elements_is_present(self.driver, self.check_search.SECTION_GOODS)
        self.element_click(self.driver, l_menu['users'])
        self.elements_is_present(self.driver, self.check_search.SECTION_USERS)

    @priority("High")
    def test_to_good_card(self, stock_state="PUBLISHED"):
        """
        Title: Click: Я могу перейти к карточке товара кликом по товару в результатах поиска
        """
        service_log.run(self)
        stock_state_id = databases.db1.warehouse.get_id_stock_state_by_name(stock_state)[0]["id"]
        criteria = "stock_state_id=%s and length(content->'title'->>'value') > 16" % str(stock_state_id)
        good = databases.db1.warehouse.get_wares_by_criteria(criteria)[0]
        c_good = good["content"]
        good_name = c_good["title"]["value"].encode('utf-8').strip()
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=good_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        e_msg = "Товар не найден в результатах поиска"
        self.search_by_good(self.driver, good, l_menu["count_goods"], e_msg=e_msg)
        search_good_obj = self.element_is_present(self.driver, self.click_search.GOOD_BY_ID % good["ware_id"])
        self.element_click(self.driver, search_good_obj)
        self.element_is_present(self.driver, self.check_good.NAME_GOOD % good_name)

    @priority("High")
    def test_go_pagination_goods(self, good_name='пла', good_on_page=40):
        """
        Title: Click: Я могу перейти на вторую страницу пагинатора и увидеть вторые 40 штук товаров
        """
        service_log.run(self)
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=good_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.assertNotEqual(l_menu["count_goods"], '', "Не получены результаты поиска")
        self.good_state_pagination(self.driver, int(l_menu["count_goods"]), databases.db1, good_on_page)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()
        

class Test_User_Listing_Result_Search(WarehouseCheckMethods, HelpAuthCheckMethods, HelpProfileSettingsCheckMethods,
                                      Search):
    """
    Story: Листинг результатов поиска (Пользователи) + Пагинатор
    """
    
    @classmethod
    def setUp(cls):
        """ Подготовка окружения """
        cls.driver = HelpLifeCycleMethods.get_driver()
        cls.go_to_main_page(cls.driver)  # Переходим на главную
        service_log.preparing_env(cls)
    
    @priority("Medium")
    def test_count_found_users_equal_tab_users(self):
        """
        Title: Количество найденных пользователей на странице соответствует числу, указанному напротив раздела
        """
        service_log.run(self)
        seller_id = AccountingMethods.get_default_user_id(role='seller')
        seller = databases.db1.accounting.get_user_by_account_id(seller_id)[0]
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=seller["display_name"])
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.element_click(self.driver, l_menu['users'])
        self.pagination(self.driver, int(l_menu["count_users"]), self.check_search.SECTION_USERS)

    @priority("Medium")
    def test_users_pagination(self, user_name='п', user_on_page=40):
        """
        Title: На страницу с результатами поиска помещается 40 карточек пользователя, а остальное скрыто пагинацией
        Description:
        * Если пользователей 40 - пагинатор не отображается
        * Если пользователей 41 - отображается вторая страница пагинатора
        """
        service_log.run(self)
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=user_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.assertNotEqual(l_menu["count_users"], '', "Не получены результаты поиска")
        self.element_click(self.driver, l_menu['users'])
        self.pagination(self.driver, int(l_menu["count_users"]), self.check_search.SECTION_USERS, user_on_page)

    @priority("Medium")
    def test_users_active_seller(self, user_name='ст', user_on_page=40):
        """
        Title: Отображаются только пользователи: Продавец & Активный
        """
        service_log.run(self)
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=user_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.assertNotEqual(l_menu["count_users"], '', "Не получены результаты поиска")
        self.element_click(self.driver, l_menu['users'])
        self.user_state_pagination(self.driver, int(l_menu["count_users"]), databases.db1, user_on_page)

    @priority("High")
    def test_go_pagination_users(self, user_name='п', user_on_page=40):
        """
        Title: Click: Я могу перейти на вторую страницу пагинатора и увидеть вторые 40 штук товаров
        """
        service_log.run(self)
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=user_name)
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.assertNotEqual(l_menu["count_users"], '', "Не получены результаты поиска")
        self.element_click(self.driver, l_menu['users'])
        self.user_state_pagination(self.driver, int(l_menu["count_users"]), databases.db1, user_on_page)

    @priority("High")
    def test_to_shop_page(self):
        """
        Title: Click: Я могу перейти в магазин пользователя кликом по его имени в результатах поиска
        """
        service_log.run(self)
        seller_id = AccountingMethods.get_default_user_id(role='seller')
        seller = databases.db1.accounting.get_user_by_account_id(seller_id)[0]
        s_form = self.search_form(self.driver)
        self.input_str(s_form["input"], string=seller["display_name"])
        self.element_click(self.driver, s_form["btn"], change_page_url=True)
        l_menu = self.left_menu(self.driver)
        self.element_click(self.driver, l_menu['users'])
        e_msg = "Пользователь не найден в результатах поиска"
        self.search_by_user(self.driver, seller, int(l_menu["count_users"]), e_msg)
        user_obj = self.element_is_present(self.driver, self.click_search.SELLER_NAME_WITH_ID %
                                           (seller_id, seller['display_name']))
        self.element_click(self.driver, user_obj)
        self.element_is_present(self.driver, self.check_shop.USER_NAME % seller['display_name'])
    
    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()
    

class Test_Search_Other(WarehouseCheckMethods, HelpAuthCheckMethods, HelpProfileSettingsCheckMethods):
    """
    Story: Прочее
    """
    
    @classmethod
    def setUp(cls):
        """ Подготовка окружения """
        cls.driver = HelpLifeCycleMethods.get_driver()
        cls.go_to_main_page(cls.driver)  # Переходим на главную
        service_log.preparing_env(cls)
    
    @skip('manual')
    @priority("Low")
    def test_16(self):
        """
        Title: Я могу запустить поиск, находясь на вкладке "Пользователи", и останусь на этой вкладке
        """
        service_log.run(self)
    
    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()