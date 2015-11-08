# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
#         	Tests .
#--------------------------------------------------------------------
import random

from ddt import ddt, data

from support import service_log
from support.utils.common_utils import priority
from support.utils.db import databases
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods as FrontAuthCheckMethods
from tests.back_office.class_auth import HelpAuthCheckMethods
from tests.worker_warehouse.class_warehouse import WarehouseMethods
from tests.front_office.goods.classes.class_good import HelpGoodCheckMethods


__author__ = 'm.senchuk'


@ddt
class TestModerationWare(HelpLifeCycleMethods, HelpAuthCheckMethods, FrontAuthCheckMethods, WarehouseMethods,
                         HelpGoodCheckMethods):
    @classmethod
    def setUp(cls):
        # Подготовка данных для теста
        user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.set_ware_to_moderate(user_id, databases.db7)
        # Подготовка работы с selenium
        cls.driver = cls.get_driver()
        service_log.preparing_env(cls)
        # Переходим на страницу авторизации бэка
        cls.get_back_page(cls.driver)
        cls.obj_login, cls.obj_pass, cls.obj_submit = cls.get_back_auth_data(cls.driver)

    @priority("medium")
    @data(*HelpAuthCheckMethods.ROLE)
    def test_start_moderation_page(self, role='admin'):
        """ Тест проверяет, страницу Начать модерацию, проверка активности кнопки в зависимости от кол-ва товаров на модерацию
        :param role:
        :return:
        """
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        self.check_back_login(self.driver)
        self.check_default_page(self.driver)

    @priority("medium")
    @data(*HelpAuthCheckMethods.ROLE)
    def test_navigate_moderation(self, role='admin'):
        """ Переход со страницы Начать модерации к модерации товаров
        :param role:
        :return:
        """
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        self.check_back_login(self.driver)
        self.check_default_page(self.driver)
        self.check_navigate(self.driver, self.GO_TO_NAVIGATE_GOOD)

    @priority("medium")
    @data(*HelpAuthCheckMethods.ROLE)
    def test_ware(self, role='admin'):
        """ Проверка элементов товара при модерации товара
        :param role:
        :return:
        """
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        self.check_back_login(self.driver)
        self.check_default_page(self.driver)
        self.check_navigate(self.driver, self.GO_TO_NAVIGATE_GOOD)
        env_base = self.ENV_BASE_URL[self.ENV_BASE_URL.find("//") + len('//'):]
        good_id = self.get_good_id_from_page_source(self.driver, self.path_back_wares.TO_FIND_GOOD % env_base)
        ware_cassandra = databases.db7.warehouse.get_wares_by_ware_id(good_id[0])[0]
        self.update_data_content(ware_cassandra, self.deserialize_content(ware_cassandra['content']))
        self.driver.switch_to.frame(self.driver.find_elements_by_tag_name("iframe")[0])
        # проверка названия товара
        self.get_element_navigate(self.driver, self.check_back_wares.WARE_TITLE %
                                  ware_cassandra['content']['title']['value'])
        # проверка превью фотографий товара
        img_list = ware_cassandra['content']['pictures']['value']
        xpath_img_list = self.get_xpath_img_list(self.check_good.GALLERY_PREVIEW_PHOTO, img_list,
                                                 self.path_good.PATH_IMG_ID_END)
        self.check_image_in_card(self.driver, xpath_img_list)
        # проверка главного фото товара
        self.get_element_navigate(self.driver, self.check_good.GALLERY_MAIN_PHOTO % img_list[0])
        # проверка кнопок Утвердить/Отклонить
        obj_accept = self.get_element_navigate(self.driver, self.click_back_wares.BTN_DO_ACCEPT)
        obj_decline = self.get_element_navigate(self.driver, self.click_back_wares.BTN_DO_DECLINE)

    @priority("medium")
    @data(*HelpAuthCheckMethods.ROLE)
    def test_ware_moderation_accept(self, role='admin'):
        """ Модерация товара - утвердить
        :param role:
        :return:
        """
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        self.check_back_login(self.driver)
        total = self.get_total_count_moderation_wares()
        self.check_default_page(self.driver)
        self.check_navigate(self.driver, self.GO_TO_NAVIGATE_GOOD)
        env_base = self.ENV_BASE_URL[self.ENV_BASE_URL.find("//") + len('//'):]
        good_id = self.get_good_id_from_page_source(self.driver, self.path_back_wares.TO_FIND_GOOD % env_base)
        ware_cassandra = databases.db7.warehouse.get_wares_by_ware_id(good_id[0])[0]
        self.update_data_content(ware_cassandra, self.deserialize_content(ware_cassandra['content']))
        # проверка кнопок Утвердить/Отклонить
        obj_accept = self.get_element_navigate(self.driver, self.click_back_wares.BTN_DO_ACCEPT)
        obj_decline = self.get_element_navigate(self.driver, self.click_back_wares.BTN_DO_DECLINE)
        # переключение на фрейм товара
        self.driver.switch_to.frame(self.driver.find_elements_by_tag_name("iframe")[0])
        # проверка названия товара
        self.get_element_navigate(self.driver, self.check_back_wares.WARE_TITLE %
                                  ware_cassandra['content']['title']['value'])
        # проверка превью фотографий товара
        img_list = ware_cassandra['content']['pictures']['value']
        xpath_img_list = self.get_xpath_img_list(self.check_good.GALLERY_PREVIEW_PHOTO, img_list,
                                                 self.path_good.PATH_IMG_ID_END)
        self.check_image_in_card(self.driver, xpath_img_list)
        # проверка главного фото товара
        self.get_element_navigate(self.driver, self.check_good.GALLERY_MAIN_PHOTO % img_list[0])
        # Жмем Утвердить, проверяем, что товар перешел в статус ACCEPTED
        self.driver.switch_to.parent_frame()
        self.click_button(obj_accept)
        ware_cassandra = databases.db7.warehouse.get_wares_by_ware_id(good_id[0])[0]
        moderation = databases.db7.warehouse.get_moderation_by_ware_id(ware_cassandra["id"])[0]
        self.assertEqual(moderation['moderation_state_id'], 2, "Товар не перешел в статус ACCEPTED")
        self.assertEqual(ware_cassandra['stock_state_id'], 2, "Товар не в статусе PUBLISHED")
        # проверяем, что после одобрения товара, показывается следующий товар если он есть
        self.check_next_moderation_ware(self.driver, total, good_id)

    @priority("medium")
    @data(*HelpAuthCheckMethods.ROLE)
    def test_ware_moderation_decline(self, role='admin'):
        """ Модерация товара - отклонить
        :param role:
        :return:
        """
        self.back_auth(role, self.obj_login, self.obj_pass, self.obj_submit, databases.db1)
        self.check_back_login(self.driver)
        total = self.get_total_count_moderation_wares()
        self.check_default_page(self.driver)
        self.check_navigate(self.driver, self.GO_TO_NAVIGATE_GOOD)
        env_base = self.ENV_BASE_URL[self.ENV_BASE_URL.find("//") + len('//'):]
        good_id = self.get_good_id_from_page_source(self.driver, self.path_back_wares.TO_FIND_GOOD % env_base)
        ware_cassandra = databases.db7.warehouse.get_wares_by_ware_id(good_id[0])[0]
        self.update_data_content(ware_cassandra, self.deserialize_content(ware_cassandra['content']))
        # проверка кнопок Утвердить/Отклонить
        obj_accept = self.get_element_navigate(self.driver, self.click_back_wares.BTN_DO_ACCEPT)
        obj_decline = self.get_element_navigate(self.driver, self.click_back_wares.BTN_DO_DECLINE)
        # переключение на фрейм товара
        self.driver.switch_to.frame(self.driver.find_elements_by_tag_name("iframe")[0])
        # проверка названия товара
        self.get_element_navigate(self.driver, self.check_back_wares.WARE_TITLE %
                                  ware_cassandra['content']['title']['value'])
        # проверка превью фотографий товара
        img_list = ware_cassandra['content']['pictures']['value']
        xpath_img_list = self.get_xpath_img_list(self.check_good.GALLERY_PREVIEW_PHOTO, img_list,
                                                 self.path_good.PATH_IMG_ID_END)
        self.check_image_in_card(self.driver, xpath_img_list)
        # проверка главного фото товара
        self.get_element_navigate(self.driver, self.check_good.GALLERY_MAIN_PHOTO % img_list[0])
        # Жмем Отклонить, проверяем, что товар перешел в статус DECLINE
        self.driver.switch_to.parent_frame()
        self.click_button(obj_decline)
        obj_list_reason = self.driver.find_elements_by_xpath(self.click_back_wares.LIST_REASON_DECLINE)
        reasons = []
        for reason_text in obj_list_reason:
            reasons.append(reason_text.text.encode('utf-8'))
        reasons.remove('')
        count_reasons = len(reasons) - 1
        num_reason = random.randrange(0, count_reasons, 1)
        obj_reason = self.get_element_navigate(self.driver, self.click_back_wares.REASON_DECLINE %
                                               reasons[num_reason])
        self.click_button(obj_reason)
        obj_declined = self.get_element_navigate(self.driver, self.click_back_wares.BTN_DECLINE)
        self.click_button(obj_declined)
        ware_cassandra = databases.db7.warehouse.get_wares_by_ware_id(good_id[0])[0]
        moderation = databases.db7.warehouse.get_moderation_by_ware_id(ware_cassandra["id"])[0]
        self.assertEqual(moderation['moderation_state_id'], 4, "Товар не перешел в статус BANNED")
        self.assertEqual(ware_cassandra['stock_state_id'], 3, "Товар не в статусе HIDDEN")
        # проверяем, что после одобрения товара, показывается следующий товар если он есть
        self.check_next_moderation_ware(self.driver, total, good_id)


    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()