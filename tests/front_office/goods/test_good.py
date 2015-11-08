# -*- coding: utf-8 -*-
"""
Feature: Товары
Description: Набор тестов для проверки функционала страницы товаров и операций с товарами
"""
import random
import time
from unittest import skip
from ddt import ddt
from support import service_log
from support.utils import common_utils
from support.utils.db import databases
from support.utils.common_utils import generate_sha256, priority, dict_to_json
from support.utils.thrift4req import services
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateData
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods
from tests.worker_warehouse.class_warehouse import WarehouseCheckMethods
from tests.front_office.settings.classes.class_profile_settings import HelpProfileSettingsCheckMethods
from tests.front_office.goods.classes.class_good import HelpGoodCheckMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods
from tests.front_office.messages_and_contacts.classes.class_chat_and_deals import HelpChatAndDealsCheckMethods
from tests.front_office.not_sorted.classes.class_user_card import HelpUserCardCheckMethods

__author__ = 'm.senchuk'


@ddt
class TestGoodPage(HelpAuthCheckMethods, HelpProfileSettingsCheckMethods, HelpGoodCheckMethods, WarehouseCheckMethods):
    """
    Story: Страница товара
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        databases.db1.accounting.update_account_details_by_criteria(default_user_id, "locale='ru'")
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        cls.shop = databases.db1.accounting.get_shop_details_by_shop_id(cls.user["shop_id"])[0]

        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        # Переходим на страницу авторизации
        cls.get_auth_page(cls.driver)
        cls.click_to_phone(cls.driver)

        obj_phone, obj_password, obj_submit_button = cls.get_data_authorization(cls.driver)

        # Вводим данные на авторизацию
        cls.send_phone(phone_object=obj_phone, phone_number=cls.user["phone"][1:])
        cls.send_password(password_object=obj_password, password_number=default_new_passwd)
        # Нажатие на кнопку авторизации
        cls.submit_button(obj_submit_button)

    @skip('deprecated')
    @priority('low')
    def test_check_delivery_address_full(self, test_data=HelpNavigateData.SHP_TO_GOOD):
        """
        Title: Для продавца, у которого адрес магазина заполнен,
        в карточке товара в пункте Доставка отображается "Самовывоз, %Адрес магазина%"
        """
        self.get_page(self.driver, self.path_settings.URL_SHOP_INFO)
        test_address = common_utils.random_string(length=20)
        self.clear_input_row(self.driver, self.get_obj_input(self.driver, value=self.shop["address"],
                                                             path_block=self.path_settings.PATH_COMMON_INFO,
                                                             path_input=self.input_settings.FORM_SHOP_ADDRESS))
        shop_address = self.get_obj_input(self.driver, value=self.shop["address"],
                                          path_block=self.path_settings.PATH_COMMON_INFO,
                                          path_input=self.input_settings.FORM_SHOP_ADDRESS)
        shop_address.send_keys(test_address)
        # Получаем объект кнопки Сохранить
        common_info_submit = self.get_submit_button(self.driver, self.path_settings.PATH_COMMON_INFO)
        # Нажимаем Сохранить
        common_info_submit.click()

        self.get_page(self.driver, self.path_shop.URL_SHOP % self.user['id'])
        self.check_navigate_in_good_page(self.driver, test_data, 1)
        self.get_element_navigate(self.driver, self.check_good.DELIVERY_ADDRESS_FULL % test_address)

    @skip('deprecated')
    @priority('low')
    def test_check_delivery_address_empty(self, test_data=HelpNavigateData.SHP_TO_GOOD):
        """
        Title: Для продавца, у которого адрес магазина не заполнен,
        в карточке товара в пункте Доставка отображается "Самовывоз"
        """
        self.get_page(self.driver, self.path_settings.URL_SHOP_INFO)
        self.clear_input_row(self.driver, self.get_obj_input(self.driver, value=self.shop["address"],
                                                             path_block=self.path_settings.PATH_COMMON_INFO,
                                                             path_input=self.input_settings.FORM_SHOP_ADDRESS))
        # Получаем объект кнопки Сохранить и сохраняем
        common_info_submit = self.get_submit_button(self.driver, self.path_settings.PATH_COMMON_INFO)
        common_info_submit.click()

        self.get_page(self.driver, self.path_shop.URL_SHOP % self.user['id'])
        self.check_navigate_in_good_page(self.driver, test_data, 1)
        self.get_element_navigate(self.driver, self.check_good.DELIVERY_ADDRESS_EMPTY)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()



@ddt
class TestGoodBreadcrumbs(HelpAuthCheckMethods, HelpProfileSettingsCheckMethods, HelpGoodCheckMethods,
                          WarehouseCheckMethods):
    """
    Story: Хлебные крошки
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        databases.db1.accounting.update_account_details_by_criteria(default_user_id, "locale='ru'")
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        cls.shop = databases.db1.accounting.get_shop_details_by_shop_id(cls.user["shop_id"])[0]

        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

        # Устанавливаем новый пароль для пользователя
        cls.default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(cls.default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

    @priority("medium")
    def test_check_go_breadcrumbs(self, test_good=HelpNavigateData.SHP_TO_GOOD):
        """
        Title: Хлебные крошки отображают путь до товара в каталоге. Я могу перейти в каталог в
        Раздел/Категорию/Подкатегорию к которой принадлежит данный товар, используя хлебные крошки.
        """
        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.user["id"])
        self.check_navigate_in_good_page(self.driver, test_good, 1)
        bread_list = self.get_breadcrumb_list(self.driver)
        self.check_bread_navigate(self.driver, bread_list)

    @priority("medium")
    def test_change_breadcrumbs(self, test_good=HelpNavigateData.SHP_TO_GOOD):
        """
        Title: При изменении расположения товара в каталоге - соответствующим образом меняются хлебные крошки.
        """
        # Авторизуемся
        self.go_main(self.driver, phone=self.user["phone"], passwd=self.default_new_passwd, flag_auth=True)

        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.user["id"])
        time.sleep(self.time_sleep)
        self.check_navigate_in_good_page(self.driver, test_good, 1)
        bread_old_list = self.get_breadcrumb_list(self.driver)
        good_url = self.driver.current_url
        good_id = good_url[good_url.rfind('/')+1:].encode('utf-8')
        self.get_page(self.driver, self.path_my_goods.URL_EDIT_GOOD % good_id)
        time.sleep(self.time_sleep)
        service_log.put("Root category in good %s" % bread_old_list[0])
        cat_list = self.set_categories(self.driver, new_category_not=bread_old_list[0])
        obj_publish = self.element_is_present(self.driver, self.click_my_goods.ADD_GOOD_BTN_PUBLISH)
        self.element_click(self.driver, obj_publish, change_page_url=True)
        self.get_page(self.driver, self.path_good.URL_GOOD % good_id)
        bread_new_dict = self.get_breadcrumbs(self.driver)
        self.check_breads(bread_new_dict, cat_list)

    @skip('deprecated')
    @priority('low')
    def test_simple(self):
        """
        Title: Проверка сообщений в поп-апе при нажатии кнопки Связаться с продавцом
        """
        examples = [
            u"Здравствуйте. Хочу приобрести партию этого товара, сколько будет стоить доставка?",
            u"Здравствуйте, подскажите, как можно приобрести партию этого товара?",
            u"Здравствуйте, какие у Вас условия оплаты и доставки?",
            u"Здравствуйте. Расскажите, пожалуйста, как купить у Вас товар.",
            u"Подскажите, пожалуйста, какие у Вас условия заказа?",
            u"Здравствуйте. Хочу купить у Вас партию этого товара. Как это сделать?",
            u"Здравствуйте. Очень заинтересовал этот товар. Расскажите, пожалуйста, как происходит оплата и доставка?",
            u"Здравствуйте. У Вас действуют скидки на крупные партии?",
            u"Здравствуйте. Какая у Вас минимальная сумма заказа?",
            u"Подскажите, пожалуйста, каким способом Вы принимаете оплату? Хочу купить у вас партию товара.",
        ]
        # Авторизуемся
        self.go_main(self.driver, phone=self.user["phone"], passwd=self.default_new_passwd, flag_auth=True)
        self.get_page(self.driver, '/goods/fa1d0218efbdf6385b9e7d7b4186bb00')
        do_time = time.time()
        stat = dict()
        text_list = list()
        f = open('text_list.txt', 'w')
        i = 0
        while i < 1000:
            self.element_click(self.driver, self.click_good.BTN_CALL_SELLER2, change_page_url=False)
            txt = self.element_is_present(self.driver, self.check_good.POPUP_MSG_FROM_GOOD % '').text
            text_list.append(txt)
            self.element_click(self.driver, self.click_good.BTN_CANCEL_CALL, change_page_url=False)
            i += 1
        for e in examples:
            count = text_list.count(e)
            stat.update({e: count})
        for index in text_list:
            index = index.encode('utf-8')
            f.write(index + '\n')
        f.close()
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestGoodPageToShop(HelpAuthCheckMethods, HelpProfileSettingsCheckMethods, HelpGoodCheckMethods,
                         WarehouseCheckMethods):
    """
    Story: Переход в магазин со страницыв товара
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        cls.shop = databases.db1.accounting.get_shop_details_by_shop_id(cls.user["shop_id"])[0]
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)
        # Подготовка тестовых данных
        cls.test_good = HelpNavigateData.SHP_TO_GOOD
        # Переход на страницу магазина
        cls.get_page(cls.driver, HelpNavigateData.path_shop.URL_SHOP % cls.user["id"])

    @priority("medium")
    def test_btn_in_shop(self, good_to_shop=HelpNavigateCheckMethods.GP_IN_SHOP_BTN):
        """
        Title: Я могу перейти в магазин данного продавца, нажав на "В магазин" в профиле продавца
        """
        self.check_navigate_in_good_page(self.driver, self.test_good, 1)
        good_to_shop['start_click'] = good_to_shop['start_click'] % self.user["id"]
        self.check_navigate(self.driver, good_to_shop)
        self.assertEqual(self.driver.current_url, self.ENV_BASE_URL + "/store/%s" % self.user["id"])

    @priority("medium")
    def test_click_user_card(self, good_to_shop=HelpNavigateCheckMethods.GP_LINK_AVATAR):
        """
        Title: Я могу перейти в магазин данного продавца, нажав на Карточку продавца, в профиле продавца
        """
        self.check_navigate_in_good_page(self.driver, self.test_good, 1)
        good_to_shop['start_click'] = good_to_shop['start_click'] % self.user["id"]
        self.check_navigate(self.driver, good_to_shop)
        self.assertEqual(self.driver.current_url, self.ENV_BASE_URL + "/store/%s" % self.user["id"])

    @skip('deprecated')
    @priority("medium")
    def test_btn_show_more(self, good_to_shop=HelpNavigateCheckMethods.GP_SHOW_MORE_BTN):
        """
        Title: Я могу перейти в магазин данного продавца, нажав "Показать больше" в Других товарах продавца
        """
        self.check_navigate_in_good_page(self.driver, self.test_good, 1)
        good_to_shop['start_click'] = good_to_shop['start_click'] % self.user["id"]
        self.check_navigate(self.driver, good_to_shop)
        self.assertEqual(self.driver.current_url, self.ENV_BASE_URL + "/store/%s" % self.user["id"])

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()

@ddt
class TestGoodPageToOtherGood(HelpAuthCheckMethods, HelpProfileSettingsCheckMethods, HelpGoodCheckMethods,
                              WarehouseCheckMethods):
    """
    Story: Переход в другие товары продавца со страницы товара
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        cls.shop = databases.db1.accounting.get_shop_details_by_shop_id(cls.user["shop_id"])[0]
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()

        # Подготовка тестовых данных
        cls.test_good = HelpNavigateData.SHP_TO_GOOD
        # Переход на страницу магазина
        cls.get_page(cls.driver, HelpNavigateData.path_shop.URL_SHOP % cls.user["id"])
        service_log.preparing_env(cls)

    @priority("medium")
    def test_click_other_good(self):
        """
        Title: Я могу перейти в другой товар продавца, кликнув на него в блоке Другие товары продавца.
        При этом товар на который я перешел не будет отображаться в блоке Другие товары продавца.
        """
        self.check_navigate_in_good_page(self.driver, self.test_good, 1)
        # получаем идентификаторы других товаров продавца
        good_id_list = self.get_good_id_from_page_source(self.driver, self.path_good.PATH_OTHER_GOOD)
        good_id = random.choice(good_id_list)
        navigate = {"start_xpath_good": self.click_good.OTHER_GOOD_BY_ID,
                    "finish_xpath_good": self.check_good.TITLE_GOOD}
        # переход на другой товар продавца
        self.check_navigate_in_good_page(self.driver, navigate, good_id)
        # получаем идентификаторы других товаров продавца
        good_id_list_new = self.get_good_id_from_page_source(self.driver, self.path_good.PATH_OTHER_GOOD)
        self.assertNotIn(good_id, good_id_list_new)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


@ddt
class TestGoodPageBtnComplain(HelpAuthCheckMethods, HelpProfileSettingsCheckMethods, HelpGoodCheckMethods,
                              HelpChatAndDealsCheckMethods, WarehouseCheckMethods):
    """
    Story: Пожаловаться на товар
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        cls.shop = databases.db1.accounting.get_shop_details_by_shop_id(cls.user["shop_id"])[0]
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        # Берем покупателя
        buyer_user_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.buyer = databases.db1.accounting.get_user_by_account_id(buyer_user_id)[0]
        service_log.preparing_env(cls)

    @priority("medium")
    def test_buyer_btn_complain(self):
        """
        Title: Я как Покупатель, могу отправить жалобу на товар Модератору, нажав на "Пожаловаться на товар"(...)
        """
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.buyer["salt"])
        databases.db1.accounting.update_user_password(self.buyer["id"], hash_res_new)

        self.go_main(self.driver, phone=self.buyer["phone"], passwd=default_new_passwd, flag_auth=True)

        # Подготовка тестовых данных
        self.test_good = HelpNavigateData.SHP_TO_GOOD
        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.user["id"])
        good_id_list = self.get_good_id_from_page_source(self.driver, self.path_shop.TO_FIND_GOODS)
        good_id = random.choice(good_id_list)
        navigate = {"start_xpath_good": self.click_shop.GOOD_NAME_BY_ID,
                    "finish_xpath_good": self.check_good.TITLE_GOOD}

        # переход на товар продавца
        self.check_navigate_in_good_page(self.driver, navigate, good_id)
        good_name = self.get_element_navigate(self.driver, self.check_good.TITLE_GOOD).text.encode('utf-8')
        btn_complain = self.get_element_navigate(self.driver, self.click_good.BTN_COMPLAIN)
        btn_complain.click()
        time_complain = HelpUserCardCheckMethods.need_time(time.time())
        self.get_element_navigate(self.driver, self.check_good.BTN_COMPLAIN_HOLD)
        self.check_success_complain(self.driver)
        self.driver.refresh()
        HelpNavigateCheckMethods.progress(self.driver)
        self.get_element_navigate(self.driver, self.click_good.BTN_COMPLAIN)
        self.driver.delete_all_cookies()

        # Берем тестового продавца на магазине которого будут проводиться проверки
        self.moderator_id = AccountingMethods.get_default_user_id(role='moderator')
        self.moderator = databases.db1.accounting.get_user_by_account_id(self.moderator_id)[0]
        AccountingMethods.save_user_password(user_id=self.moderator["id"], hash_passwd=self.moderator["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.moderator["salt"])
        databases.db1.accounting.update_user_password(self.moderator["id"], hash_res_new)

        # Авторизуемся модератором
        self.go_main(self.driver, phone=self.moderator["phone"], passwd=default_new_passwd, flag_auth=True)

        self.get_page(self.driver, self.path_chat.URL_CHAT_WITH_USER % self.buyer["id"])
        self.check_moderator_complain(self.driver, good_id, good_name, time_complain)

    @priority("medium")
    def test_visitor_btn_complain(self):
        """
        Title: Я как Гость, при нажатии на "Пожаловаться на товар" увижу страницу Авторизации
        """
        # Подготовка тестовых данных
        self.test_good = HelpNavigateData.SHP_TO_GOOD
        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.user["id"])
        good_id_list = self.get_good_id_from_page_source(self.driver, self.path_shop.TO_FIND_GOODS)
        good_id = random.choice(good_id_list)
        navigate = {"start_xpath_good": self.click_shop.GOOD_NAME_BY_ID,
                    "finish_xpath_good": self.check_good.TITLE_GOOD}

        # переход на товар продавца
        self.check_navigate_in_good_page(self.driver, navigate, good_id)
        # click complain button
        self.check_navigate(self.driver, self.GOOD_COMPLAIN_TO_AUTH)

    @priority("medium")
    def test_seller_own_btn_complain(self):
        """
        Title: Я как Продавец не могу пожаловаться на свой товар, т.к не вижу данной кнопки
        """
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)

        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_auth=True)

        self.check_profile_widget(self.driver, mode=None)
        # Подготовка тестовых данных
        self.test_good = HelpNavigateData.SHP_TO_GOOD
        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.user["id"])
        good_id_list = self.get_good_id_from_page_source(self.driver, self.path_shop.TO_FIND_GOODS)
        good_id = random.choice(good_id_list)
        navigate = {"start_xpath_good": self.click_shop.GOOD_NAME_BY_ID,
                    "finish_xpath_good": self.check_good.TITLE_GOOD}

        # переход на товар продавца
        self.check_navigate_in_good_page(self.driver, navigate, good_id)
        test_xpath = {'xpath': self.click_good.BTN_COMPLAIN,
                      'err_msg': "У продавца-свой товар есть кнопка 'Пожаловаться на товар'"}
        self.check_no_such_element(self.driver, test_xpath)

    @priority("medium")
    def test_buyer_btn_complain_inactive_good(self):
        """
        Title: Я как Покупатель могу пожаловаться на неактивный товар, нажав на "Пожаловаться на товар"
        """
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.buyer["salt"])
        databases.db1.accounting.update_user_password(self.buyer["id"], hash_res_new)

        self.go_main(self.driver, phone=self.buyer["phone"], passwd=default_new_passwd, flag_auth=True)

        # Подготовка тестовых данных
        self.test_good = HelpNavigateData.SHP_TO_GOOD
        # Переход на страницу магазина
        self.get_page(self.driver, HelpNavigateData.path_shop.URL_SHOP % self.user["id"])
        good_id_list = self.get_good_id_from_page_source(self.driver, self.path_shop.TO_FIND_GOODS)
        good_id = random.choice(good_id_list)
        navigate = {"start_xpath_good": self.click_shop.GOOD_NAME_BY_ID,
                    "finish_xpath_good": self.check_good.TITLE_GOOD}

        # Тестовый товар преводим в статус НЕАКТИВНЫЙ
        name_stock_state = 'HIDDEN'
        stock_state = self.get_StockState(name_stock_state)
        services.warehouse.root.tframed.makePublication(good_id, stock_state)
        # Проверяем, что товар перешел в статус HIDDEN
        ware_cassandra = databases.db7.warehouse.get_wares_by_ware_id(good_id)[0]
        self.assertEqual(ware_cassandra['stock_state_id'], stock_state, "Статус товара не равен 3 - неактивному товару")
        # переход на товар продавца
        self.check_navigate_in_good_page(self.driver, navigate, good_id)
        good_name = self.get_element_navigate(self.driver, self.check_good.TITLE_GOOD).text.encode('utf-8')
        btn_complain = self.get_element_navigate(self.driver, self.click_good.BTN_COMPLAIN)
        btn_complain.click()
        time_complain = HelpUserCardCheckMethods.need_time(time.time())
        self.get_element_navigate(self.driver, self.check_good.BTN_COMPLAIN_HOLD)
        self.check_success_complain(self.driver)
        self.driver.refresh()
        HelpNavigateCheckMethods.progress(self.driver)
        self.get_element_navigate(self.driver, self.click_good.BTN_COMPLAIN)
        self.driver.delete_all_cookies()

        # Берем тестового продавца на магазине которого будут проводиться проверки
        self.moderator_id = AccountingMethods.get_default_user_id(role='moderator')
        self.moderator = databases.db1.accounting.get_user_by_account_id(self.moderator_id)[0]
        AccountingMethods.save_user_password(user_id=self.moderator["id"], hash_passwd=self.moderator["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.moderator["salt"])
        databases.db1.accounting.update_user_password(self.moderator["id"], hash_res_new)

        # Переходим на страницу авторизации
        self.get_auth_page(self.driver)
        #self.click_to_phone(self.driver)

        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)

        # Вводим данные на авторизацию
        self.send_phone(phone_object=obj_phone, phone_number=self.moderator["phone"])
        self.send_password(password_object=obj_password, password_number=default_new_passwd)
        # Нажатие на кнопку авторизации
        self.element_click(self.driver, obj_submit_button, change_page_url=True)

        self.get_page(self.driver, self.path_chat.URL_CHAT_WITH_USER % self.buyer["id"])
        self.check_moderator_complain(self.driver, good_id, good_name, time_complain)
        # Тестовый товар преводим в статус АКТИВНЫЙ
        stock_state = self.get_StockState('PUBLISHED')
        services.warehouse.root.tframed.makePublication(good_id, stock_state)
        # Проверяем, что товар перешел в статус PUBLISHED
        ware_cassandra = databases.db7.warehouse.get_wares_by_ware_id(good_id)[0]
        self.assertEqual(ware_cassandra['stock_state_id'], stock_state, "Stock-state ware not PUBLISHED.")


    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


@ddt
class TestCardGoodInAllPages(HelpGoodCheckMethods, HelpAuthCheckMethods):
    """
    Story: Карточки товара на сайте
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='buyer')
        databases.db1.accounting.update_account_details_by_criteria(default_user_id, "locale='ru'")
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]

        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        # Авторизуемся
        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)
        cls.db_good = databases.db1.warehouse.get_wares_by_criteria("stock_state_id=2 order by random() limit 5;")[0]
        cls.get_page(cls.driver, cls.path_good.URL_GOOD %cls.db_good["ware_id"])
        category_id = cls.get_category_id_from_page_source(cls.driver,
                                                           cls.path_good.PATH_IMG_ID_START,
                                                           cls.path_good.PATH_IMG_ID_END)[0]
        title = cls.get_element_navigate(cls.driver, cls.check_good.TITLE_GOOD).text.encode('utf-8').replace(' ', '')
        min_stock = cls.get_element_navigate(cls.driver, cls.check_good.MIN_STOCK).text.encode('utf-8').replace(' ', '')
        price = cls.get_element_navigate(cls.driver, cls.check_good.PRICE).text.encode('utf-8').replace(' ', '')
        current_url = cls.driver.current_url[cls.driver.current_url.rfind('/') + 1:].encode('utf-8')
        cls.data_good = dict(image=category_id, title=title, min_stock=min_stock, price=price, good_id=current_url)
        time.sleep(cls.time_sleep)

    @priority("medium")
    def test_card_good_final_category_page(self):
        """
        Title: Тест проверяет экспресс карточку товара на странице финальной категории
        """
        #price = self.set_price_for_good_by_id(self.data_good['good_id'], self.PRICE_GOOD[test_method])
        #self.data_good['price'] = str(price) + "руб."
        count_bc = len(self.elements_is_present(self.driver, self.click_good.BREADCRUMB_LIST))
        # переходим по хлебной крошке в финальную категорию
        obj_bread_final_category = self.element_is_present(self.driver, self.click_good.BREADCRUMBS % count_bc)
        self.element_click(self.driver, obj_bread_final_category, change_page_url=True)
        self.element_is_present(self.driver, self.check_catalog.FINAL_CATEGORY_ABSTRACT)

        obj_good = None
        # ищем товар с нужным id
        while obj_good is None:
            try:
                obj_good = self.element_is_present(self.driver, self.click_catalog.GOOD_BY_ID % self.data_good['good_id'])
            except Exception:
                #если товар не найден на перовй странице листаем дальше
                current_pag = self.element_is_present(self.driver, self.click_shop.PAG_ACTIVE).text.encode('utf-8')
                next_page = int(current_pag) + 1
                pag = self.element_is_present(self.driver, self.click_shop.PAG_BY_NUMBER % next_page)
                self.element_click(self.driver, pag, change_page_url=True)

        # получаем данные с экспресс карточки товара
        good = obj_good.text.encode('utf-8').replace(' ', '').replace('\n', '')

        # проверяем текстовые данные: название, мин. партия, цена
        good_in_page_good = self.data_good['title'].replace(' ', '')# + "Заштуку"
        #good_in_page_good = good_in_page_good + self.data_good['price'] + "Мин.заказ" + self.data_good['min_stock']

        self.assertEqual(good, good_in_page_good, "Текстовые данные не совпадают")
        # проверяем фото товара
        good_id = self.click_catalog.GOOD_IMG % self.data_good['good_id']
        image = self.path_category.PATH_IMG % self.data_good['image']
        check_photo_ware = good_id + image
        self.get_element_navigate(self.driver, check_photo_ware)

    @priority("medium")
    def test_card_good_store_page(self):
        """
        Title: Тест проверяет экспресс карточку товара на странице магазина
        """
        # переходим на страницу магазина продавца
        obj_to_shop = self.element_is_present(self.driver, self.click_good.BTN_IN_SHOP_ABSTRACT)
        self.element_click(self.driver, obj_to_shop, change_page_url=True)
        self.element_is_present(self.driver, self.check_shop.TITLE_SHOP)

        obj_good = None
        # ищем товар с нужным id
        while obj_good is None:
            try:
                obj_good = self.element_is_present(self.driver, self.click_shop.GOOD_BY_ID % self.data_good['good_id'])
            except Exception:
                #если товар не найден на перовй странице листаем дальше
                current_pag = self.element_is_present(self.driver, self.click_shop.PAG_ACTIVE).text.encode('utf-8')
                next_page = int(current_pag) + 1
                pag = self.element_is_present(self.driver, self.click_shop.PAG_BY_NUMBER % next_page)
                self.element_click(self.driver, pag, change_page_url=True)

        # получаем данные с экспресс карточки товара
        good = obj_good.text.encode('utf-8').replace(' ', '').replace('\n', '')

        # проверяем текстовые данные: название, мин. партия, цена
        good_in_page_good = self.data_good['title'] + "Заштуку"
        good_in_page_good = good_in_page_good + self.data_good['price'] + "Мин.заказ" + self.data_good['min_stock']

        self.assertEqual(good, good_in_page_good, "Текстовые данные не совпадают")

        # проверяем фото товара
        good_id = self.click_shop.GOOD_BY_ID % self.data_good['good_id']
        image = self.path_shop.PATH_IMG % self.data_good['image']
        check_photo_ware = good_id + image
        self.get_element_navigate(self.driver, check_photo_ware)

    @priority("medium")
    def test_card_good_favorite_page(self):
        """
        Title: Тест проверяет экспресс карточку товара на странице избранные
        """
        # добавляем товар в избранное и переходим в Избранные товары
        obj_add_favorite = self.get_element_navigate(self.driver, self.click_good.ADD_FAVORITE)
        self.click_button(obj_add_favorite)
        self.get_page(self.driver, self.path_favorites.URL_FAVORITES_GOODS)

        # ищем товар с нужным id
        xpath_to_good = self.click_favorite.GOOD_NAME_BY_ID % self.data_good['good_id']
        good_name = self.get_element_navigate(self.driver, xpath_to_good)
        good_name_origin = good_name.text.encode('utf-8')
        good_name = good_name.text.encode('utf-8').replace(' ', '')

        #xpath_to_good_min_stock =  self.check_favorite.MIN_STOCK_BY_GOOD_ID % self.data_good['good_id']
        #good_min_stock = self.get_element_navigate(self.driver, xpath_to_good_min_stock)
        #good_min_stock = good_min_stock.text.encode('utf-8').replace(' ', '')
#
        #xpath_to_good_price = self.check_favorite.PRICE_BY_GOOD_ID % self.data_good['good_id']
        #good_price = self.get_element_navigate(self.driver, xpath_to_good_price)
        #good_price = good_price.text.encode('utf-8').replace(' ', '')

        # проверяем текстовые данные: название, мин. партия, цена
        self.assertEqual(good_name, self.data_good['title'], "Название товара не совпадает")
        #good_in_good_page_min_stock = "Мин.заказ:" + self.data_good['min_stock']
        #self.assertIn(good_in_good_page_min_stock, good_min_stock,  "Мин. партия товара не совпадает")
        #good_in_good_page_price = "Ценазаштуку:" + self.data_good['price']
        #self.assertEqual(good_price, good_in_good_page_price, "Цена товара не совпадает")
#
        ## проверяем фото товара
        #xpath_to_good_id = self.click_favorite.GOOD_BY_ID % self.data_good['good_id']
        #xpath_to_image = self.path_favorites.PATH_IMG % self.data_good['image']
        #xpath_to_photo = xpath_to_good_id + xpath_to_image
        #self.get_element_navigate(self.driver, xpath_to_photo)
        xpath_del_fav = self.click_favorite.DEL_FAVORITE % (good_name_origin, self.data_good['good_id'])
        obj_del_favorite = self.element_is_present(self.driver, xpath_del_fav)
        self.click_button(obj_del_favorite)
        #time.sleep(4)

    @priority("medium")
    def test_card_good_search_page(self):
        """
        Title: Тест проверяет экспресс карточку товара на странице поиска
        """
        # ищем через форму поиска товар по названию
        good_title = self.element_is_present(self.driver, self.check_good.TITLE_GOOD).text
        obj_search_input = self.element_is_present(self.driver, self.input_main.SEARCH)
        obj_search_input.send_keys(good_title)
        obj_search_btn = self.element_is_present(self.driver, self.click_main.BTN_SEARCH)
        self.click_button(obj_search_btn)
        self.element_is_present(self.driver, self.check_search.TITLE_SEARCH)
        # ищем товар с нужным id
        obj_good = self.element_is_present(self.driver, self.click_search.GOOD_BY_ID % self.data_good['good_id'])
        # получаем данные с экспресс карточки товара
        good = obj_good.text.encode('utf-8').replace(' ', '').replace('\n', '')
        # проверяем текстовые данные: название, мин. партия, цена
        good_in_page_good = self.data_good['title'] + "Заштуку"
        good_in_page_good = good_in_page_good + self.data_good['price'] + "Мин.заказ" + self.data_good['min_stock']
        self.assertEqual(good, good_in_page_good, "Текстовые данные не совпадают")
        # проверяем фото товара
        xpath_good_id = self.click_search.GOOD_BY_ID % self.data_good['good_id']
        xpath_image = self.path_search.PATH_IMG % self.data_good['image']
        xpath = xpath_good_id + xpath_image
        self.element_is_present(self.driver, xpath)

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class TestGoodMoveToModeration(HelpGoodCheckMethods, HelpAuthCheckMethods,
                               HelpLifeCycleCheckMethods, WarehouseCheckMethods, HelpProfileSettingsCheckMethods):
    """
    Story: Модерация товара
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.moderator_id = int(AccountingMethods.get_default_user_id(role='moderator'))
        databases.db1.accounting.update_account_details_by_criteria(default_user_id, "locale='ru'")
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]

        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"])

        # Подготовка работы с selenium
        cls.driver = cls.get_driver()

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, cls.user["salt"])
        databases.db1.accounting.update_user_password(cls.user["id"], hash_res_new)

        cls.go_main(cls.driver, phone=cls.user["phone"], passwd=default_new_passwd, flag_auth=True)

        #cls.get_page(cls.driver, cls.path_shop.URL_SHOP % cls.user["id"])
        #list_good_id = cls.get_good_id_from_page_source(cls.driver, cls.path_shop.TO_FIND_GOODS)
        #cls.good_id = list_good_id[0]
        #ware_cassandra = databases.db7.warehouse.get_wares_by_ware_id(cls.good_id)[0]
        #cls.update_data_content(ware_cassandra, cls.deserialize_content(ware_cassandra['content']))
        crt1 = "ww.shop_id=%s and " % str(cls.user["id"])
        criteria = crt1 + "ww.stock_state_id=2 and json_array_length(ww.content->'pictures'->'value')=3 " \
                          "ORDER BY RANDOM() limit 20;"
        cls.goods = databases.db1.warehouse.get_wares_by_criteria_and_moderation_state('2', criteria)
        for good in cls.goods:
            pict = good['content'][u'pictures'][u'value'][0]
            if pict != good['content'][u'pictures'][u'value'][1] and pict != good['content'][u'pictures'][u'value'][2]:
                cls.good = good
                break
        cls.good_id = cls.good["ware_id"]
        # Меняем статус на ACCEPTED
        services.warehouse.root.tframed.makeModeration(cls.good_id, True, cls.moderator_id)

        # добавляем фото, чтобы их было 2 или больше
        #cls.set_photo(ware_cassandra, cls.good_id)

        # Переходим на страницу редактирования товара
        cls.get_page(cls.driver, cls.path_my_goods.URL_EDIT_GOOD % cls.good_id)
        time.sleep(cls.time_sleep)

    @priority("medium")
    def test_change_name(self):
        """
        Title: Тест проверяет отправку на модерацию товара при изменении названия товара
        """
        obj_input_name = self.get_element_navigate(self.driver, self.input_my_goods.ADD_GOOD_NAME)
        self.clear_input_row(self.driver, obj_input_name)
        obj_input_name.send_keys(common_utils.random_string())
        obj_publish = self.get_element_navigate(self.driver, self.click_my_goods.ADD_GOOD_BTN_PUBLISH)
        self.click_button(obj_publish)
        time.sleep(self.time_sleep)
        ware_cassandra = databases.db7.warehouse.get_wares_by_ware_id(self.good_id)[0]
        o_moderate = databases.db7.warehouse.get_moderation_state_by_ware_id(ware_cassandra["id"])[0]
        self.assertEqual(o_moderate['moderation_state_id'], 1, "Товар не отправлен на модерацию")

    @priority("medium")
    def test_change_photo(self):
        """
        Title: Тест проверяет отправку на модерацию товара при удалении фото
        """
        obj_delete = self.element_is_present(self.driver, self.click_my_goods.DELETE_PHOTO % 1)
        self.click_button(obj_delete)
        obj_publish = self.element_is_present(self.driver, self.click_my_goods.ADD_GOOD_BTN_PUBLISH)
        self.element_click(self.driver, obj_publish, change_page_url=True)
        time.sleep(self.time_sleep)
        ware_cassandra = databases.db7.warehouse.get_wares_by_ware_id(self.good_id)[0]
        o_moderate = databases.db7.warehouse.get_moderation_state_by_ware_id(ware_cassandra["id"])[0]
        self.assertEqual(o_moderate['moderation_state_id'], 1, "Товар не отправлен на модерацию")

    @priority("medium")
    def test_change_description(self):
        """
        Title: Тест проверяет отправку на модерацию товара при изменении описания товара
        """
        obj_input_description = self.element_is_present(self.driver, self.input_my_goods.DESCRIPTION)
        self.clear_input_row(self.driver, obj_input_description)
        obj_input_description.send_keys(common_utils.random_string(length=50))
        obj_publish = self.element_is_present(self.driver, self.click_my_goods.ADD_GOOD_BTN_PUBLISH)
        self.click_button(obj_publish)
        time.sleep(self.time_sleep)
        ware_cassandra = databases.db7.warehouse.get_wares_by_ware_id(self.good_id)[0]
        o_moderate = databases.db7.warehouse.get_moderation_state_by_ware_id(ware_cassandra["id"])[0]
        self.assertEqual(o_moderate['moderation_state_id'], 1, "Товар не отправлен на модерацию")

    @classmethod
    def tearDown(cls):
        databases.db1.warehouse.update_content_by_ware_id(shop_id=cls.user["id"],
                                                          ware_id=cls.good_id,
                                                          content=dict_to_json(cls.good['content']))
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()