# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
#         	Tests .
#--------------------------------------------------------------------
"""
Feature: Главное меню
"""
from ddt import ddt, data
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from support import service_log
from support.utils.common_utils import generate_sha256, priority
from support.utils.db import databases
from support.utils.thrift4req import services
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate
from tests.front_office.main.classes.class_main_menu import MainMenuCheckMethods as MainMenu
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods

__author__ = 'm.senchuk'


class TestMainMenuView(Navigate, MainMenu):
    """
    Story: Отображение главного меню
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Переходим на главную
        cls.go_to_main_page(cls.driver)
        # Получаем дерево категорий
        cls.category_dict = services.categories.root.tframed.getVisibleLiteCatalogTree('ru')
        # Получаем данные корня "Каталог"
        sections = cls.category_dict[1]
        # Получаем список ID разделов
        cls.section_id_list = cls.get_categories_list(sections)
        # Составляем дерево разделов
        cls.section_tree = cls.get_categories_tree(cls.category_dict, cls.section_id_list)

    @priority("Must")
    def test_menu_include_sections(self):
        """
        Title: Проверка наличия всех пунктов разделов в главном меню
        Description: Главное меню состоит из следующих пунктов: "Одежда", "Обувь и аксессуары", Товары для детей",
        "Товары для дома", "Товары для сада", "Торговое оборудование"
        """
        self.check_main_menu_section(self.driver, self.section_tree)

    @priority("Must")
    def test_section_include_categories(self):
        """
        Title: Выпадающее меню раздела содержит перечень категорий данного раздела, у каждой из категории есть картинка
        (проверить для каждого раздела)
        """
        self.check_main_menu_category(self.driver, self.section_tree, self.category_dict)

    @priority("Must")
    def test_category_include_sub_categories(self):
        """
        Title: Првоерка что выпадающее меню раздела, содержит правильные категории
        Description: Выпадающее меню раздела, для каждой из выделенных категорий содержит перечень подкатегорий,
        удовлетворяющих условию [подкатегория принадлежит данной категории] &
        [подкатегория содержит не менее 1-го активного товара]
        """
        self.check_main_menu_sub_category(self.driver, self.section_tree, self.category_dict)

    @priority("Medium")
    def test_main_menu_view_main_page(self):
        """
        Title: Главное меню отображает мое текущее местонахождение в каталоге.
        На главной странице - в главном меню выделен "домик"
        """
        self.get_element_navigate(self.driver, self.check_main.MAIN_MENU_HOME_ACTIVE)

    @priority("Medium")
    def test_main_menu_view_section_page(self):
        """
        Title: Главное меню отображает мое текущее местонахождение в каталоге.
        На странице Раздела - в главном меню выделен раздел в котором я нахожусь
        """
        section = self.section_tree[0]
        self.get_page(self.driver, self.path_category.URL_PATH_ROOT_CATEGORY % section.categoryId)
        self.get_element_navigate(self.driver, self.check_main.MAIN_MENU_SECTION_ACTIVE % section.localizedName)

    @priority("Medium")
    def test_main_menu_view_category_page(self):
        """
        Title: Главное меню отображает мое текущее местонахождение в каталоге.
        На странице Категории - в главном меню выделен раздел в котором я нахожусь
        """
        # Получить раздел
        section = self.section_tree[0]
        # Получить спиок категорий у которых есть под категории
        cat_id_list = self.get_categories_list(section)
        cat_tree = self.get_categories_tree(self.category_dict, cat_id_list)
        categories = [item for item in cat_tree if item.childCategories is not None]
        category = categories[0]
        self.get_page(self.driver, self.path_category.URL_PATH_ROOT_CATEGORY % category.categoryId)
        self.get_element_navigate(self.driver, self.check_main.MAIN_MENU_SECTION_ACTIVE % section.localizedName)

    @priority("Medium")
    def test_main_menu_view_sub_category_page(self):
        """
        Title: Главное меню отображает мое текущее местонахождение в каталоге.
        На странице Подкатегории - в главном меню выделен раздел в котором я нахожусь
        """
        # Получить раздел
        section = self.section_tree[0]
        # Получить спиок категорий у которых есть под категории
        cat_id_list = self.get_categories_list(section)
        cat_tree = self.get_categories_tree(self.category_dict, cat_id_list)
        categories = [item for item in cat_tree if item.childCategories is not None]
        category = categories[0]
        # Получить список подкатегорий
        sub_cat_id_list = self.get_categories_list(category)
        sub_cat_tree = self.get_categories_tree(self.category_dict, sub_cat_id_list)
        sub_category = sub_cat_tree[0]
        self.get_page(self.driver, self.path_category.URL_PATH_ROOT_CATEGORY % sub_category.categoryId)
        self.get_element_navigate(self.driver, self.check_main.MAIN_MENU_SECTION_ACTIVE % section.localizedName)

    @priority("Medium")
    def test_main_menu_view_good_page(self):
        """
        Title: Главное меню отображает мое текущее местонахождение в каталоге.
        На странице Карточки товара - в главном меню не выделен ни один раздел
        """
        # Получить раздел
        section = self.section_tree[0]
        # Получить спиок категорий у которых есть под категории
        cat_id_list = self.get_categories_list(section)
        cat_tree = self.get_categories_tree(self.category_dict, cat_id_list)
        categories = [item for item in cat_tree if item.childCategories is not None]
        category = categories[0]
        # Получить список подкатегорий
        sub_cat_id_list = self.get_categories_list(category)
        sub_cat_tree = self.get_categories_tree(self.category_dict, sub_cat_id_list)
        sub_category = sub_cat_tree[0]
        self.get_page(self.driver, self.path_category.URL_PATH_ROOT_CATEGORY % sub_category.categoryId)
        self.get_element_navigate(self.driver, self.check_main.MAIN_MENU_SECTION_ACTIVE % section.localizedName)
        clk_good = self.get_element_navigate(self.driver, self.click_catalog.GOOD_NEW_LNK % 1)
        self.element_click(self.driver, clk_good, change_page_url=True)
        url = self.driver.current_url
        self.assertIn('/goods/', url, "Не произошел переход на страницу товара")
        self.get_element_navigate(self.driver, self.check_main.MAIN_MENU_SECTION_ACTIVE % section.localizedName)

    @priority("Medium")
    def test_main_menu_view_shop_page(self):
        """
        Title: Главное меню отображает мое текущее местонахождение в каталоге.
        На странице Магазина продавца - в главном меню не выделен ни один раздел
        """
        seller_id = AccountingMethods.get_default_user_id(role='seller')
        self.get_page(self.driver, self.path_shop.URL_SHOP % seller_id)
        url = self.driver.current_url
        self.assertIn('/store/', url, "Не произошел переход на страницу магазина")
        self.element_is_none(self.driver, self.check_main.MAIN_MENU_SECTION_ACTIVE % '')

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class MainMenuDisplayed(Navigate, MainMenu, HelpAuthCheckMethods):
    """
    Story: Видимость главного меню на страницах сайта
    """
    def auth(self, role):
        # Настройка окружения и вспомогательные параметры
        self.default_user_id = AccountingMethods.get_default_user_id(role=role)
        databases.db1.accounting.update_account_details_by_criteria(self.default_user_id, "locale='ru'")
        self.user = databases.db1.accounting.get_user_by_account_id(self.default_user_id)[0]
        AccountingMethods.save_user_password(user_id=self.user["id"], hash_passwd=self.user["code_value"])

        # Устанавливаем новый пароль для пользователя
        self.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(self.default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)
        self.go_main(self.driver, phone=self.user["phone"], passwd=self.default_new_passwd, flag_auth=True)
        return self.user

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Переходим на главную
        cls.go_to_main_page(cls.driver)
        # Получаем дерево категорий
        cls.category_dict = services.categories.root.tframed.getVisibleLiteCatalogTree('ru')
        # Получаем данные корня "Каталог"
        cls.sections = cls.category_dict[1]
        # Получаем список ID разделов
        cls.section_id_list = cls.get_categories_list(cls.sections)
        # Составляем дерево разделов
        cls.section_tree = cls.get_categories_tree(cls.category_dict, cls.section_id_list)
        # Получить раздел
        cls.section = cls.section_tree[0]
        # Получить спиок категорий у которых есть подкатегории
        cls.cat_id_list = cls.get_categories_list(cls.section)
        cls.cat_tree = cls.get_categories_tree(cls.category_dict, cls.cat_id_list)
        cls.categories = [item for item in cls.cat_tree if item.childCategories is not None]
        cls.category = cls.categories[0]
        # Получить список подкатегорий
        cls.sub_cat_id_list = cls.get_categories_list(cls.category)
        cls.sub_cat_tree = cls.get_categories_tree(cls.category_dict, cls.sub_cat_id_list)
        cls.sub_category = cls.sub_cat_tree[0]

    @priority("Medium")
    @data('seller', 'visitor')
    def test_menu_in_site_to_url(self, role):
        """
        Title: Главное меню отображается не на всех страницах сайта (...)
        Description: простые проверки переходом по урлу
        :return:
        """
        user = lambda x: self.auth(x) if x == 'seller' else None
        user(role)
        self.check_main_menu_to_url(self.driver, self.ROLE_TO_MENU, role)

    @priority("Medium")
    @data('seller', 'visitor')
    def test_menu_in_site_to_url_param(self, role):
        """
        Title: Главное меню отображается не на всех страницах сайта. простые проверки переходом по урлу с параметром
        """
        user = lambda x: self.auth(x) if x == 'seller' else None
        user(role)
        parameters = {
            'section': str(self.section.categoryId),
            'category': str(self.category.categoryId),
            'sub-category': str(self.sub_category.categoryId),
            'shop': AccountingMethods.get_default_user_id('seller'),
        }
        self.check_main_menu_to_url(self.driver, self.ROLE_TO_MENU_PARAM, role, param=parameters)

    @priority("Medium")
    @data('seller', 'visitor')
    def test_menu_in_good(self, role):
        """
        Title: Главное меню отображается не на всех страницах сайта (...) - страница товара
        """
        user = lambda x: self.auth(x) if x == 'seller' else None
        user(role)
        good = databases.db1.accounting.get_all_goods_psql("stock_state_id=2 LIMIT 5")[0]
        good_id = good["ware_id"]
        self.get_page(self.driver, self.path_good.URL_GOOD % good_id)
        self.get_element_navigate(self.driver, self.xpath_menu)

    @priority("Medium")
    @data('seller', 'visitor')
    def test_menu_in_search(self, role):
        """
        Title: Главное меню отображается не на всех страницах сайта (...) - поисковая выдача
        """
        user = lambda x: self.auth(x) if x == 'seller' else None
        user(role)
        input_search = self.get_element_navigate(self.driver, self.input_main.SEARCH)
        input_search.send_keys('a')
        ActionChains(self.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
        self.get_element_navigate(self.driver, self.xpath_menu)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class TestMainMenuLogic(Navigate, MainMenu):
    """
    Story: Логика работы главного меню
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Переходим на главную
        cls.go_to_main_page(cls.driver)
        # Получаем дерево категорий
        cls.category_dict = services.categories.root.tframed.getVisibleLiteCatalogTree('ru')
        # Получаем данные корня "Каталог"
        cls.sections = cls.category_dict[1]
        # Получаем список ID разделов
        cls.section_id_list = cls.get_categories_list(cls.sections)
        # Составляем дерево разделов
        cls.section_tree = cls.get_categories_tree(cls.category_dict, cls.section_id_list)
        # Получить раздел
        cls.section = cls.section_tree[0]
        # Получить список категорий у которых есть подкатегории
        cls.cat_id_list = cls.get_categories_list(cls.section)
        cls.cat_tree = cls.get_categories_tree(cls.category_dict, cls.cat_id_list)
        cls.categories = [item for item in cls.cat_tree if item.childCategories is not None]
        cls.category = cls.categories[0]
        # Получить список подкатегорий
        cls.sub_cat_id_list = cls.get_categories_list(cls.category)
        cls.sub_cat_tree = cls.get_categories_tree(cls.category_dict, cls.sub_cat_id_list)
        cls.sub_category = cls.sub_cat_tree[0]

    @priority("Must")
    def test_click_home(self):
        """
        Title: Я могу находясь на любой странице сайта перейти на главную кликнув на "домик" в главном меню.
        """
        parameters = {
            '404': '',
            'section': str(self.section.categoryId),
            'category': str(self.category.categoryId),
            'sub-category': str(self.sub_category.categoryId),
            'shop': AccountingMethods.get_default_user_id('seller'),
        }
        url = lambda sm, p, ps: sm[p] if ps[p] is '' else sm[p] % ps[p]
        for param in parameters:
            service_log.put("Checking...['%s']" % param)
            base_url = self.driver.current_url
            source = self.driver.page_source
            url_page = url(self.SITE_MAP, param, parameters)
            self.get_page(self.driver, url_page)
            source_new = self.driver.page_source
            self.assertNotEqual(source, source_new, "Переход по url='%s' не произошел" % url)
            btn_home = self.get_element_navigate(self.driver, self.click_main.MAIN_MENU_HOME)
            HelpAuthCheckMethods.click_button(btn_home, sleep=3)
            current_url = self.driver.current_url
            source_home = self.driver.page_source
            self.assertEqual(base_url, current_url, "Переход на главную не произошел")
            self.assertNotEqual(source_home, source_new, "Переход на главную не произошел")
            service_log.put("PASS...['%s']" % param)

    @priority("Must")
    def test_go_to_section(self):
        """
        Title: Я могу перейти на страницу выбранного Раздела, кликнув на "Все разделы" в выпадающем меню выбранного раздела
        Description:
            * Проверить, xто я нахожусь на странице соответствующего раздела
        """
        for section in self.section_tree:
            if section.localizedName == "Торговое оборудование":
                continue
            # Кликаем на раздел, чтобы открыть меню раздела
            xpath_section = self.xpath_section % section.localizedName
            section_clk_menu = self.get_element_navigate(self.driver, xpath_section, mode=None)
            HelpAuthCheckMethods.click_button(section_clk_menu)
            # кликаем на ссылку в меню раздела "Все разделы"
            all_cat_btn = self.get_element_navigate(self.driver, self.click_main.ALL_CATEGORIES, mode=None)
            page_source = self.driver.page_source
            HelpAuthCheckMethods.click_button(all_cat_btn)
            url_ui = self.driver.current_url.encode('utf-8')
            page_source_new = self.driver.page_source
            url_need = self.ENV_BASE_URL + self.path_category.URL_PATH_ROOT_CATEGORY % section.categoryId
            err_msg_1 = "Переход не произошел, полученный урл: %s не совпадает с целевым: %s"
            self.assertEqual(url_ui, url_need, err_msg_1 % (url_ui, url_need))
            err_msg_2 = "Тело страницы не измненилось, переход в раздел '%s' не произошел"
            self.assertNotEqual(page_source, page_source_new, err_msg_2 % section.localizedName)

    @priority("Must")
    def test_go_to_category_all_goods(self):
        """
        Title: Я могу перейти на страницу выбранной Категории.Все товары, кликнув на "Все категории" в выпадающем меню
        выбранного раздела
        Description:
            * Проверить, что я нахожусь на странице соответствующей категории в пункте "Все товары"
        """
        for section in self.section_tree:
            # Получить список категорий у которых есть подкатегории
            cat_id_list = self.get_categories_list(section)
            cat_tree = self.get_categories_tree(self.category_dict, cat_id_list)
            # Кликаем на раздел, чтобы открыть меню раздела
            xpath_section = self.xpath_section % section.localizedName
            section_clk_menu = self.get_element_navigate(self.driver, xpath_section, mode=None)
            HelpAuthCheckMethods.click_button(section_clk_menu)
            name_ui = section.localizedName
            category_id = section.categoryId
            # Для раздела Тороговое оборудования используется логика без переходв категорию, т.к. у него их нет
            if section.localizedName != "Торговое оборудование":
                # Получить объекты категорий меню
                cat_iu_list = self.get_categories(self.driver)
                name_ui_list = [category.text.encode('utf-8') for category in cat_iu_list]
                # Берем максимум 6 категорий отображаемых в меню
                names_ui = name_ui_list[:6]
                # кликаем на первую категорию
                name_ui = names_ui[0]
                xpath_category = self.xpath_category % name_ui
                cat_btn = self.get_element_navigate(self.driver, xpath_category, mode=None)
                HelpAuthCheckMethods.click_button(cat_btn)
                category_db = [item for item in cat_tree if item.localizedName == name_ui]
                category_id = category_db[0].categoryId
            # кликаем на ссылку в меню атегории "Все категории"
            all_sub_cat_btn = self.get_element_navigate(self.driver, self.click_main.ALL_SUB_CATEGORIES, mode=None)
            page_source = self.driver.page_source
            HelpAuthCheckMethods.click_button(all_sub_cat_btn)
            self.get_element_navigate(self.driver, self.check_catalog.ACTIVE_TREE_CATEGORY % 'Все товары')
            self.get_element_navigate(self.driver, self.check_catalog.PARENT_CAT_IN_SUB_CAT_LISTING % name_ui)
            url_ui = self.driver.current_url.encode('utf-8')
            page_source_new = self.driver.page_source
            url_need = self.ENV_BASE_URL + self.path_category.URL_ALL_IN_CATEGORY % category_id
            err_msg_1 = "Переход не произошел, полученный урл: %s не совпадает с целевым: %s"
            self.assertEqual(url_ui, url_need, err_msg_1 % (url_ui, url_need))
            err_msg_2 = "Тело страницы не измненилось, переход на все подкатегории категории: '%s' не произошел"
            self.assertNotEqual(page_source, page_source_new, err_msg_2 % name_ui)

    @priority("Must")
    def test_go_to_final_category(self):
        """
        Title: Я могу перейти на страницу выбранной Подкатегории, кликнув на название подкатегории в выпадающем меню
        выбранного раздела и выбранной категории (...)
        Description:
            * Проверить, что я нахожусь на странице соответствующей подкатегории в пункте "Все товары"
        """
        for section in self.section_tree:
            # Получить список категорий у которых есть подкатегории
            cat_id_list = self.get_categories_list(section)
            cat_tree = self.get_categories_tree(self.category_dict, cat_id_list)
            # Кликаем на раздел, чтобы открыть меню раздела
            xpath_section = self.xpath_section % section.localizedName
            section_clk_menu = self.get_element_navigate(self.driver, xpath_section, mode=None)
            HelpAuthCheckMethods.click_button(section_clk_menu)
            name_ui = section.localizedName
            category_in_sub = section
            # Для раздела Тороговое оборудования используется логика без переходв категорию, т.к. у него их нет
            if section.localizedName != "Торговое оборудование":
                # Получить объекты категорий меню
                cat_iu_list = self.get_categories(self.driver)
                name_ui_list = [category.text.encode('utf-8') for category in cat_iu_list]
                # Берем максимум 6 категорий отображаемых в меню
                names_ui = name_ui_list[:6]
                # кликаем на первую категорию
                name_ui = names_ui[0]
                xpath_category = self.xpath_category % name_ui
                cat_btn = self.get_element_navigate(self.driver, xpath_category, mode=None)
                HelpAuthCheckMethods.click_button(cat_btn)
                category_db = [item for item in cat_tree if item.localizedName == name_ui]
                category_in_sub = category_db[0]
            # Проверка возвращенных апи и показанных подкатегорий
            obj_ui_sub = self.get_sub_categories(self.driver)
            names_ui_sub = [obj.text.encode('utf-8') for obj in obj_ui_sub]
            # имя подкатегории
            name_ui_sub = names_ui_sub[0]
            sub_cat_id_list = self.get_categories_list(category_in_sub)
            sub_cat_tree = self.get_categories_tree(self.category_dict, sub_cat_id_list)
            sub_category_db = [item for item in sub_cat_tree if item.localizedName == name_ui_sub]
            sub_category_id = sub_category_db[0].categoryId
            xpath_sub_cat = self.click_main.MAIN_MENU_SUB_CATEGORY_BY_NAME % name_ui_sub
            # кликаем на ссылку подкатегориив меню категории
            sub_cat_btn = self.get_element_navigate(self.driver, xpath_sub_cat, mode=None)
            page_source = self.driver.page_source
            HelpAuthCheckMethods.click_button(sub_cat_btn)
            self.get_element_navigate(self.driver, self.check_catalog.ACTIVE_TREE_CATEGORY % name_ui_sub)
            self.get_element_navigate(self.driver, self.check_catalog.PARENT_CAT_IN_SUB_CAT_LISTING % name_ui)
            url_ui = self.driver.current_url.encode('utf-8')
            page_source_new = self.driver.page_source
            url_need = self.ENV_BASE_URL + self.path_category.URL_PATH_ROOT_CATEGORY % sub_category_id
            err_msg_1 = "Переход не произошел, полученный урл: %s не совпадает с целевым: %s"
            self.assertEqual(url_ui, url_need, err_msg_1 % (url_ui, url_need))
            err_msg_2 = "Тело страницы не измненилось, переход на подкатегорию: '%s' не произошел"
            self.assertNotEqual(page_source, page_source_new, err_msg_2 % name_ui_sub)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()