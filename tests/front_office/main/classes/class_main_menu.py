# coding=utf-8
from support import service_log
from tests.MainClass import MainClass
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods as Auth
from support.utils import common_utils

__author__ = 'm.senchuk'


class MainMenuData(MainClass):
    xpath_section_menu = Navigate.check_main.MAIN_MENU_SECTION_MENU
    xpath_section = Navigate.click_main.MAIN_MENU_SECTION
    xpath_category = Navigate.click_main.MAIN_MENU_CATEGORY
    xpath_category_icon = Navigate.click_main.MAIN_MENU_CATEGORY_ICON
    xpath_menu = Navigate.check_main.MAIN_MENU

    ROLE_TO_MENU = {
        'visitor': {
            'main': True,
            'auth': False,
            'reg': False,
            'restore': False,
            'help': False,
            '404': True
        },
        'seller': {
            'main': True,
            'help': False,
            '404': True,
            'favorite': True,
            'chat': False,
            'contacts': False,
            'settings': False,
            'my_goods': False,
            'add_good': False
        }
    }

    ROLE_TO_MENU_PARAM = {
        'visitor': {
            'section': True,
            'category': True,
            'sub-category': True,
            #'good': True,
            'shop': True,
            #'search': True,
        },
        'seller': {
            'section': True,
            'category': True,
            'sub-category': True,
            #'good': True,
            'shop': True,
            #'search': True,
        }
    }

    MAIN_MENU_TO_SITE = {
        'main': True,
        'help': True,
        '404': True,
        'section': True,
        'category': True,
        'sub-category': True,
        'shop': True,
    }

    base_url = MainClass.ENV_BASE_URL
    SITE_MAP = {
        'main': '',                                                     # урл
        'section': Navigate.path_category.URL_PATH_ROOT_CATEGORY,       # урл с парам
        'category': Navigate.path_category.URL_PATH_ROOT_CATEGORY,      # урл с парам
        'sub-category': Navigate.path_category.URL_PATH_ROOT_CATEGORY,  # урл с парам
        'good': True,                                                   # логика
        'shop': Navigate.path_shop.URL_SHOP,                            # урл с парам
        'search': True,                                                 # логика
        'auth': Navigate.path_auth.PATH_AUTH,                           # урл
        'reg': Navigate.path_reg.URL_REG,                               # урл
        'restore': Navigate.path_restore.URL_RESTORE_PHONE,             # урл
        'help': Navigate.path_help.UH_HOW_BUY,                          # урл
        '404': '/' + common_utils.random_string(),                      # урл
        'favorite': Navigate.path_favorites.URL_FAVORITES_GOODS,        # урл
        'chat': Navigate.path_chat.URL_CHAT,                            # урл
        'contacts': Navigate.path_user_contact.URL_FAVORITES_USERS,     # урл
        'settings': Navigate.path_settings.PATH_PROFILE_SETTINGS,       # урл
        'my_goods': Navigate.path_my_goods.URL_MY_GOODS,                # урл
        'add_good': Navigate.path_my_goods.URL_ADD_GOOD                 # урл
    }


class MainMenuMethods(MainMenuData):
    @staticmethod
    def get_page_with_param(driver, url_path, param):
        """
        Выполнить переход на страницу по урлу с параметром (например подставить идентификатор магазина)
        :param driver:
        :param url_path:
        :param param:
        :return:
        """
        url = url_path + param
        Navigate.get_page(driver, url)

    @staticmethod
    def get_categories_list(category_dict):
        """
        Получить список категорий у родительской категории
        :return:
        """
        # Множество категорий преобразовываем в список
        cat_set = category_dict.childCategories
        cat_list = [item for item in cat_set]
        return cat_list

    @staticmethod
    def get_categories_tree(category_dict, category_id_list):
        """
        Получить дерево категорий
        :return:
        """
        # Составляем дерево разделов
        category_tree = [category_dict[i] for i in category_id_list]
        return category_tree

    @staticmethod
    def get_sections(driver):
        """
        Получить разделы из главного меню
        :param driver:
        :return:
        """
        return driver.find_elements_by_xpath(Navigate.check_main.MAIN_MENU_SECTION_ABSTRACT)

    @staticmethod
    def get_categories(driver):
        """
        Получить категории из раздела
        :param driver:
        :return:
        """
        return driver.find_elements_by_xpath(Navigate.check_main.MAIN_MENU_CATEGORY_ABSTRACT)

    @staticmethod
    def get_sub_categories(driver):
        """
        Получить под-категории из категории раздела
        :param driver:
        :return:
        """
        Navigate.get_element_navigate(driver, Navigate.check_main.MAIN_MENU_SUB_CATEGORY, mode=None)
        return driver.find_elements_by_xpath(Navigate.check_main.MAIN_MENU_SUB_CATEGORY_ABSTRACT)


class MainMenuCheckMethods(MainMenuMethods):

    def check_main_menu_to_url(self, driver, link_map, role, param=None):
        """
        Проверка наличия меню на страницах сайта путем перехода по урлу
        :param driver:
        :param role:
        :return:
        """
        service_log.put("Checking role -> '%s'" % role)
        menu = lambda x, d, m: Navigate.get_element_navigate(d, m) if x is True else Navigate.element_is_none(d, m)
        url = lambda par, sm, p: sm[p] if par is None else sm[p] % par[p]
        page_map = link_map[role]
        for page in page_map:
            service_log.put("Checking...['%s']" % page)
            source = driver.page_source
            url_page = url(param, self.SITE_MAP, page)
            Navigate.get_page(driver, url_page)
            source_new = driver.page_source
            err_msg = "Переход по урлу='%s' не произошел, содержимое страницы не изменилось"
            self.assertNotEqual(source, source_new, err_msg % url)
            menu(page_map[page], driver, self.xpath_menu)
            service_log.put("PASS...['%s']" % page)
        service_log.put("Checked role -> '%s'" % role)


    def check_main_menu_section(self, driver, section_tree, section_menu_name=None):
        """ Проверка главного меню на наличие нужных разделов и остутсвие ненужных
        :param driver:
        :param section_tree:
        """
        xpath = lambda sn, snm: self.xpath_section_menu % sn if sn == snm else self.xpath_section % sn
        # Проверка, что из апи пришли разделы и они есть в главном меню
        for section in section_tree:
            section_name = section.localizedName
            Navigate.get_element_navigate(driver, xpath(section_name, section_menu_name), mode=None)
        # Проверка количества возвращенных апи и показанных разделов
        count_ui_sections = len(self.get_sections(driver))
        count_db_sections = len(section_tree)
        err_msg = "Количество разделов в главном меню='%d' не совпало с количеством разделов из БД='%d'"
        self.assertEqual(count_ui_sections, count_db_sections, err_msg % (count_ui_sections, count_db_sections))

    def check_main_menu_category(self, driver, section_tree, category_dict):
        """ Проверка категорий и их картинок в меню раздела
        """
        for section in section_tree:
            section_name = section.localizedName
            if section_name == 'Торговое оборудование':
                continue
            # Кликаем на раздел, чтобы открыть меню раздела
            section_clk_menu = Navigate.get_element_navigate(driver, self.xpath_section % section_name, mode=None)
            Auth.click_button(section_clk_menu)
            # Проверка, что раздел стал открытым
            Navigate.get_element_navigate(driver, self.xpath_section_menu % section_name, mode=None)
            # Проверка, что открылось меню раздела
            Navigate.get_element_navigate(driver, Navigate.check_main.SECTION_MENU, mode=None)
            # Получаем категории раздела
            category_id_list = self.get_categories_list(section)
            category_tree = self.get_categories_tree(category_dict, category_id_list)
            cat_name_list = [category.localizedName for category in category_tree]
            # Получить объекты категорий меню
            cat_iu_list = self.get_categories(driver)
            name_ui_list = [category.text.encode('utf-8') for category in cat_iu_list]
            # Проверка количества возвращенных апи и показанных категорий
            count_ui_cat = len(cat_iu_list)
            count_db_cat = len(category_tree)
            err_msg = "Количество разделов в главном меню='%d' больше с количества разделов из БД='%d'"
            self.assertLessEqual(count_ui_cat, count_db_cat, err_msg % (count_ui_cat, count_db_cat))
            sub = lambda db, ui: filter(lambda x: x not in db, ui)
            # Берем максимум 6 категорий отображаемых в меню
            name_ui = name_ui_list[:6]
            sub_cat = sub(cat_name_list, name_ui)
            err_msg = "В разделе '%s' содержится категория '%s', которой нет в ответе АПИ: %s"
            self.assertFalse(sub_cat, err_msg % (section_name, sub_cat, cat_name_list))

    def check_main_menu_sub_category(self, driver, section_tree, category_dict):
        """ Проверка подкатегорий в меню категории раздела
        """
        for section in section_tree:
            section_name = section.localizedName
            service_log.put("CHECK. Section '%s'" % section_name)
            # Кликаем на раздел, чтобы открыть меню раздела
            section_clk_menu = Navigate.get_element_navigate(driver, self.xpath_section % section_name, mode=None)
            Auth.click_button(section_clk_menu)
            # Проверка, что раздел стал открытым
            Navigate.get_element_navigate(driver, self.xpath_section_menu % section_name, mode=None)
            # Проверка, что открылось меню раздела
            Navigate.get_element_navigate(driver, Navigate.check_main.SECTION_MENU, mode=None)
            # Получить объекты категорий меню
            cat_iu_list = self.get_categories(driver)
            name_ui_list = [category.text.encode('utf-8') for category in cat_iu_list]
            # Берем максимум 6 категорий отображаемых в меню
            name_ui = name_ui_list[:6]
            p = lambda d, n, cd, se, sn: self.sub_cat(d, cd, se, sn) if n == list() else self.cat_sub_cat(d, n, cd, se, sn)
            p(driver, name_ui, category_dict, section, section_name)
            service_log.put("PASS. Section '%s'" % section_name)

    def cat_sub_cat(self, driver, name_ui, category_dict, section, section_name):
        """
        Проверка подкатегории у которой родительская категория - категория
        :param driver:
        :param name_ui:
        :param category_dict:
        :param section:
        :param section_name:
        :return:
        """
        # Получаем категории раздела
        category_id_list = self.get_categories_list(section)
        category_tree = self.get_categories_tree(category_dict, category_id_list)
        # Проверка, что из апи пришли категории которые принадлежат секции меню
        for name in name_ui:
            service_log.put("CHECK. Sub-category in category '%s'" % name)
            cat_clk = Navigate.get_element_navigate(driver, self.xpath_category % name, mode=None)
            Auth.click_button(cat_clk)
            category = [cat for cat in category_tree if cat.localizedName == name]
            # Получаем подкатегории из категории раздела
            sub_id_list = self.get_categories_list(category[0])
            sub_tree = self.get_categories_tree(category_dict, sub_id_list)
            sub_name_list = [sub.localizedName for sub in sub_tree]
            # Проверка возвращенных апи и показанных подкатегорий
            obj_ui_sub = self.get_sub_categories(driver)
            name_ui_sub = [obj.text.encode('utf-8') for obj in obj_ui_sub]
            # Получаем названия подкатегорий UI, которых нет в списке подкатегорий полученном из БД
            sub = lambda db, ui: filter(lambda x: x not in db, ui)
            sub_cat = sub(sub_name_list, name_ui_sub)
            err_msg = "В '%s -> %s' содержится подкатегория '%s', которой нет в ответе АПИ: %s"
            self.assertFalse(sub_cat, err_msg % (section_name, name, sub_cat, sub_name_list))
            service_log.put("PASS. Sub-category in category '%s'" % name)

    def sub_cat(self, driver, category_dict, section, section_name):
        """
        Проверка подкатегории у которой раодительская категория - раздел
        :param driver:
        :param category_dict:
        :param section:
        :param section_name:
        :return:
        """
        service_log.put("CHECK. Subcategory in section '%s'" % section_name)
        # Получаем подкатегории из категории раздела
        sub_id_list = self.get_categories_list(section)
        sub_tree = self.get_categories_tree(category_dict, sub_id_list)
        sub_name_list = [sub.localizedName for sub in sub_tree]
        # Проверка возвращенных апи и показанных подкатегорий
        obj_ui_sub = self.get_sub_categories(driver)
        name_ui_sub = [obj.text.encode('utf-8') for obj in obj_ui_sub]
        # Получаем названия подкатегорий UI, которых нет в списке подкатегорий полученном из БД
        sub = lambda db, ui: filter(lambda x: x not in db, ui)
        sub_cat = sub(sub_name_list, name_ui_sub)
        err_msg = "В '%s ' содержится подкатегория '%s', которой нет в ответе АПИ: %s"
        self.assertFalse(sub_cat, err_msg % (section_name, sub_cat, sub_name_list))
        service_log.put("PASS. Sub-category in section '%s'" % section_name)
