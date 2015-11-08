# -*- coding: utf-8 -*-
from support.utils.common_utils import generate_sha256
from support.utils.db import databases
from support.utils.thrift4req import services
from tests.MainClass import MainClass
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as HNCK
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods as FrontAuthCheckMethods
from tests.worker_warehouse.class_warehouse import WarehouseMethods

__author__ = 'm.senchuk'


class HelpAuthData(MainClass):
    ROLE = [
        'admin',
        'moderator',
    ]

    MENU_ITEMS = {
        'admin': [
            "Товары",
            "Загрузка товаров",
            "Учетные записи",
            "Промо-Коды",
            "Одноразовые",
            "Многоразовые",
        ],
        'moderator': [
            "Товары",
            "Загрузка товаров",
            "Учетные записи",
        ]
    }

    NAVIGATE_MENU_ITEM = {
        "Товары": {
            "start_click": HNCK.click_back_auth.MENU_ITEM % "Товары",
            "finish_page": HNCK.click_back_wares.BTN_START_MODERATION
        },
        "Загрузка товаров": {
            "start_click": HNCK.click_back_auth.MENU_ITEM % "Загрузка товаров",
            "finish_page": HNCK.check_back_load_wares.TITLE
        },
        "Учетные записи": {
            "start_click": HNCK.click_back_auth.MENU_ITEM % "Учетные записи",
            "finish_page": HNCK.click_back_users.BTN_CREATE_USER
        },
        "Промо-Коды": {
            "start_click": HNCK.click_back_auth.MENU_ITEM % "Промо-Коды",
            "finish_page": HNCK.check_back_invites_wares.BTN_TITLE
        },
        "Одноразовые": {
            "start_click": HNCK.click_back_auth.MENU_ITEM % "Одноразовые",
            "finish_page": HNCK.check_back_invites_wares.TITLE_SINGLE
        },
        "Многоразовые": {
            "start_click": HNCK.click_back_auth.MENU_ITEM % "Многоразовые",
            "finish_page": HNCK.check_back_invites_wares.TITLE_MULTI
        },
        #"Добавление товаров": {
        #    "start_click": HNCK.click_back_auth.MENU_ITEM % "Добавление товаров",
        #    "finish_page": HNCK.click_back_cms_wares_wares.BTN_ADD_WARE
        #},
    }

    GO_TO_NAVIGATE_GOOD = {
        "start_click": HNCK.click_back_wares.BTN_START_MODERATION,
        "finish_page": HNCK.click_back_wares.BTN_DO_ACCEPT
    }

    VALUE_OR_NOT_VALUE = {
        True: "not(@disabled)",
        False: "@disabled"
    }


class HelpAuthMethods(HelpAuthData, HNCK):
    @staticmethod
    def back_auth(role, obj_login, obj_pass, obj_submit, link_db):
        """
        Авторизация в бэк-офисе
        :param role:
        :param obj_login:
        :param obj_pass:
        :param obj_submit:
        :return:
        """
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role=role)
        user = link_db.accounting.get_user_by_account_id(default_user_id)[0]
        #AccountingMethods.save_user_password(user_id=user["id"], hash_passwd=user["code_value"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, user["salt"])
        databases.db1.accounting.update_user_password(user["id"], hash_res_new)

        # Вводим данные на авторизацию
        FrontAuthCheckMethods.send_phone(phone_object=obj_login, phone_number=user["phone"][1:])
        FrontAuthCheckMethods.send_password(password_object=obj_pass, password_number=default_new_passwd)
        # Нажатие на кнопку авторизации
        FrontAuthCheckMethods.submit_button(obj_submit)
        return user

    @staticmethod
    def get_total_count_moderation_wares():
        """
        Получение общего количества товаров на модерацию
        :return:
        """
        search_req1 = WarehouseMethods.get_SearchRequestDto(stock_states=[2], moderation_states=[1])
        search_req2 = WarehouseMethods.get_SearchRequestDto(stock_states=[3], moderation_states=[3])
        result1 = services.warehouse_index.root.tframed.search(search_req1)
        result2 = services.warehouse_index.root.tframed.search(search_req2)
        total_count = result1.totalCount + result2.totalCount
        return total_count

    @staticmethod
    def get_back_page(driver, env_back_url=MainClass.ENV_BASE_BACK_URL, path_back=''):
        """
        Перход на страницу бек-офиса по path
        :param driver:
        :param env_back_url:
        :param path_back:
        :return:
        """
        HNCK.get_page(driver=driver, path_url=path_back, env_base_url=env_back_url)

    @staticmethod
    def get_back_auth_data(driver):
        """
        Получение форм и кнопки войти на странице авторизации бэк-офиса
        :param driver:
        :return:
        """
        obj_login = HNCK.get_element_navigate(driver, HNCK.input_back_auth.FORM_LOGIN)
        obj_pass = HNCK.get_element_navigate(driver, HNCK.input_back_auth.FORM_PASS)
        obj_submit = HNCK.get_element_navigate(driver, HNCK.click_back_auth.BTN_SUBMIT)
        return obj_login, obj_pass, obj_submit

    @staticmethod
    def set_ware_to_moderate(shop_id, link_db):
        """
        Создание нового товара
        :return:
        """
        ware = WarehouseMethods.get_random_ware(link_db.warehouse.get_wares_by_shop_id(shop_id))
        # создаём товар, статус товара BELIEVED (по умолчанию - Доверенный)
        ware_req = WarehouseMethods.duplicate_ware_req(ware['shop_id'], ware['managed_category_id'], ware["content"], ware['stock_state_id'])
        wh_ware_st1_0 = services.warehouse.root.tframed.createWare(ware_req)
        stock_state = WarehouseMethods.get_StockState('PUBLISHED')
        wh_ware_st1_0 = services.warehouse.root.tframed.makePublication(wh_ware_st1_0.wareId, stock_state)
        return wh_ware_st1_0


class HelpAuthCheckMethods(HelpAuthMethods):
    def check_back_login(self, driver):
        """
        Проверка, что пользователь залогинился в бэк-офис
        :param driver:
        :return:
        """
        self.get_element_navigate(driver, self.check_back_auth.NAV_BAR_TOP)

    def check_back_login_cycle_redirect(self, driver):
        """
        Проверка, что нет циклической переадресации
        :param driver:
        :return:
        """
        title = driver.title.encode('utf-8')
        self.assertNotIn(self.check_back_auth.MSG_FAILED, title, msg="Циклическая переадресация")

    def check_back_login_failed(self, driver):
        """
        Проверка, что есть сообщение об ошибке авторизации
        :param driver:
        :return:
        """
        self.get_element_navigate(driver, self.check_back_auth.FAIL_LOGIN)

    def check_default_page(self, driver):
        """
        Проверка, что при логине пользователь оказывается на странице по умолчанию - Начать модерацию товаров
        :param driver:
        :return:
        """
        msg = "После входа в бек-офис не произошел переход на страницу Товары, текущий урл: %s"
        url = driver.current_url.encode('utf-8')
        self.assertEqual(url, self.ENV_BASE_BACK_URL + self.path_back_wares.URL_WARES, msg % url)
        # проверка количества товаров на модерацию
        total = self.get_total_count_moderation_wares()
        self.get_element_navigate(driver, self.check_back_wares.COUNT_WARES % total)
        self.get_element_navigate(driver, self.click_back_wares.BTN_START_MODERATION_STATUS %
                                  self.VALUE_OR_NOT_VALUE[bool(total)])

    def check_menu_items(self, driver, menu_items):
        """
        Проверка наличия пунктов меню для разных ролей пользователей в бэк-офисе
        :param driver:
        :return:
        """
        for item in menu_items:
            self.get_element_navigate(driver, self.click_back_auth.MENU_ITEM % item)

    def check_next_moderation_ware(self, driver, total_wares, good_id):
        """
        Провека, что появляется следующий товар после одобрения или отклонения предыдущего или если товаров нет
        стартовая страница модерации
        :param driver:
        :param total_wares:
        :return:
        """
        if total_wares != 0:
            good_id_next = self.get_good_id_from_page_source(driver, self.path_back_wares.TO_FIND_GOOD %
                                                             self.ENV_BASE_URL[7:])
            self.assertNotEqual(good_id, good_id_next, "Переход на новый товар после модерации предыдущего не произошло")
            # проверка кнопок Утвердить/Отклонить
            self.get_element_navigate(driver, self.click_back_wares.BTN_DO_ACCEPT)
            self.get_element_navigate(driver, self.click_back_wares.BTN_DO_DECLINE)
        else:
            self.check_default_page(driver)