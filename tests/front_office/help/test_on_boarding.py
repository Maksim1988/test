# -*- coding: utf-8 -*-
"""
Feature: On-boarding
"""
from unittest import skip
from support import service_log
from support.utils.common_utils import priority
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateData
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.help.classes.class_on_boarding import HelpOnBoardingCheckMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods




class OnBoardingOnManageGoodsPageFirstVisit():
    """
    Story: OnBoarding на странице Управление товарами (Мой магазин), при первом заходе на страницу
    Description:
    OnBoarding дает подсказки как управлять своим магазином (3и шага, на каждом шаге по подсказке), есть возможность пропустить
    """

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass




class OnBoardingOnManageGoodsPageAfterCreateFirstGood():
    """
    Story: OnBoarding на странице Управление товарами (Мой магазин), сразу после создания первого товара
    Description:
    OnBoarding дает подсказки как управлять товарами
    """

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass




class OnBoardingOnManageGoodsPageAfterCreateSecondtGood():
    """
    Story: OnBoarding на странице Управление товарами (Мой магазин), сразу после создания второго товара
    Description:
    OnBoarding дает подсказки как изменять порядок следования товаров (настраивать витрину)
    """

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass




class OnBoardingOnCatalogSubcategoryPage():
    """
    Story: OnBoarding на странице Подкатегории в Каталоге (Режим отображения Больше \ Меньше о товаре)
    Description:
    OnBoarding дотображается на страницах подкатегории в Каталоге у кнопок Больше \ Меньше о товаре
    """

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass













class TestOnBoardingVisitor(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods, HelpOnBoardingCheckMethods):
    """
    Story: Старый OnBoarding, выпилинный с сайта еще в марте
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        cls.default_user_id = AccountingMethods.get_default_user_id(role='seller')

        # Переходим на страницу авторизации
        cls.go_to_main_page(cls.driver)

    @skip('deprecated')
    @priority('low')
    def test_on_boarding_registration(self):
        """
        Title: Гость. Впервые. Проверить отображение всех элементов On Boarding'a (расположение) - registration. Гость.
        Впервые. Просмотр каждого элемента OnBording'a [...] (кликабельность и текст)
        """
        obj_hint_reg = self.get_element_navigate(self.driver, self.click_main.ON_BOARDING_REGISTRATION)
        self.click_button(obj_hint_reg)
        self.get_element_navigate(self.driver, self.check_main.ON_BOARDING_MSG_REG)
        self.check_key_in_local_storage(self.driver, self.LOCAL_STORAGE_KEY)
        self.check_items_in_local_storage(self.driver, self.LOCAL_STORAGE_KEY, self.LOCAL_REGISTRATION)
        self.driver.refresh()
        msg = "On Boarding показывается после первого просмотра."
        self.check_no_such_element(self.driver, test_data=dict(xpath=self.click_main.ON_BOARDING_REGISTRATION,
                                                               err_msg=msg))

    @skip('deprecated')
    @priority('low')
    def test_on_boarding_language(self):
        """
        Title: Гость. Впервые. Проверить отображение всех элементов On Boarding'a (расположение) - language Гость.
        Впервые. Просмотр каждого элемента OnBording'a [...] (кликабельность и текст)
        """
        obj_language = self.get_element_navigate(self.driver, self.click_main.LANGUAGE_BTN % 'Русский')
        self.click_button(obj_language)
        obj_language = self.get_element_navigate(self.driver, self.click_main.LANGUAGE_BTN % 'English')
        self.click_button(obj_language)
        obj_hint_lang = self.get_element_navigate(self.driver, self.click_main.ON_BOARDING_LANGUAGE)
        self.click_button(obj_hint_lang)
        self.get_element_navigate(self.driver, self.check_main.ON_BOARDING_MSG_LANG)
        self.check_key_in_local_storage(self.driver, self.LOCAL_STORAGE_KEY)
        self.check_items_in_local_storage(self.driver, self.LOCAL_STORAGE_KEY, self.LOCAL_LANGUAGE)
        self.driver.refresh()
        msg = "On Boarding показывается после первого просмотра."
        self.check_no_such_element(self.driver, test_data=dict(xpath=self.click_main.ON_BOARDING_LANGUAGE,
                                                               err_msg=msg))

    @skip('deprecated')
    @priority('low')
    def test_on_boarding_catalog(self):
        """
        Title: Гость. Впервые. Проверить отображение всех элементов On Boarding'a (расположение) - catalog Гость.
        Впервые. Просмотр каждого элемента OnBording'a [...] (кликабельность и текст)
        """
        self.get_page(self.driver, self.path_category.URL_ALL_CATALOG)
        obj_hint_catalog = self.get_element_navigate(self.driver, self.click_catalog.ON_BOARDING_CATALOG)
        self.click_button(obj_hint_catalog)
        self.get_element_navigate(self.driver, self.check_catalog.ON_BOARDING_MSG_CAT)
        self.check_key_in_local_storage(self.driver, self.LOCAL_STORAGE_KEY)
        self.check_items_in_local_storage(self.driver, self.LOCAL_STORAGE_KEY, self.LOCAL_CATALOG)
        self.driver.refresh()
        msg = "On Boarding показывается после первого просмотра."
        self.check_no_such_element(self.driver, test_data=dict(xpath=self.click_catalog.ON_BOARDING_CATALOG,
                                                               err_msg=msg))

    @skip('deprecated')
    @priority('low')
    def test_on_boarding_know_price(self, go_to_good = HelpNavigateData.MAIN_NEW_GOOD_TO_GOOD):
        """
        Title: Гость. Впервые. Проверить отображение всех элементов On Boarding'a (расположение) - know_price Гость.
        Впервые. Просмотр каждого элемента OnBording'a [...] (кликабельность и текст)
        """
        self.check_navigate_in_good_page(self.driver, go_to_good, 1)
        obj_hint_know_price = self.get_element_navigate(self.driver, self.click_good.ON_BOARDING_KNOW_PRICE)
        self.click_button(obj_hint_know_price)
        self.get_element_navigate(self.driver, self.check_good.ON_BOARDING_MSG_KNOW_PRICE)
        self.check_key_in_local_storage(self.driver, self.LOCAL_STORAGE_KEY)
        self.check_items_in_local_storage(self.driver, self.LOCAL_STORAGE_KEY, self.LOCAL_KNOW_PRICE)
        self.driver.refresh()
        msg = "On Boarding показывается после первого просмотра."
        self.check_no_such_element(self.driver, test_data=dict(xpath=self.click_good.ON_BOARDING_KNOW_PRICE,
                                                               err_msg=msg))

    @skip('deprecated')
    @priority('low')
    def test_on_boarding_in_shop(self, go_to_good = HelpNavigateData.MAIN_NEW_GOOD_TO_GOOD):
        """
        Title: Гость. Впервые. Проверить отображение всех элементов On Boarding'a (расположение) - in_shop Гость.
        Впервые. Просмотр каждого элемента OnBording'a [...] (кликабельность и текст)
        """
        self.check_navigate_in_good_page(self.driver, go_to_good, 1)
        obj_hint_in_shop = self.get_element_navigate(self.driver, self.click_good.ON_BOARDING_IN_SHOP)
        self.click_button(obj_hint_in_shop)
        self.get_element_navigate(self.driver, self.check_good.ON_BOARDING_MSG_IN_SHOP)
        self.check_key_in_local_storage(self.driver, self.LOCAL_STORAGE_KEY)
        self.check_items_in_local_storage(self.driver, self.LOCAL_STORAGE_KEY, self.LOCAL_IN_SHOP)
        self.driver.refresh()
        msg = "On Boarding показывается после первого просмотра."
        self.check_no_such_element(self.driver, test_data=dict(xpath=self.click_good.ON_BOARDING_IN_SHOP,
                                                               err_msg=msg))

    @skip('deprecated')
    @priority('low')
    def test_on_boarding_shop_address(self):
        """
        Title: Гость. Впервые. Проверить отображение всех элементов On Boarding'a (расположение) - shop_address Гость.
        Впервые. Просмотр каждого элемента OnBording'a [...] (кликабельность и текст)
        """
        self.get_page(self.driver, self.path_shop.URL_SHOP % self.default_user_id)
        obj_hint_catalog = self.get_element_navigate(self.driver, self.click_shop.ON_BOARDING_ADDRESS)
        self.click_button(obj_hint_catalog)
        self.get_element_navigate(self.driver, self.check_shop.ON_BOARDING_MSG_ADDRESS)
        self.check_key_in_local_storage(self.driver, self.LOCAL_STORAGE_KEY)
        self.check_items_in_local_storage(self.driver, self.LOCAL_STORAGE_KEY, self.LOCAL_SHOP_ADDRESS)
        self.driver.refresh()
        msg = "On Boarding показывается после первого просмотра."
        self.check_no_such_element(self.driver, test_data=dict(xpath=self.click_shop.ON_BOARDING_ADDRESS,
                                                               err_msg=msg))

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()