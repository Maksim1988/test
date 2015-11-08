# -*- coding: utf-8 -*-
"""
Feature: ДОбавление \ Редактирование товара
"""

from unittest import skip
from ddt import ddt, data
from selenium import webdriver
from support import service_log
from support.utils.chromedriver import CHROMEDRIVER_PATH
from support.utils.db import databases
from support.utils.common_utils import generate_sha256, priority
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateData
from tests.front_office.goods.classes.class_good import HelpGoodCheckMethods, HelpGoodData
from tests.worker_warehouse.class_warehouse import WarehouseCheckMethods
from tests.front_office.settings.classes.class_profile_settings import HelpProfileSettingsCheckMethods
from tests.front_office.goods.classes.class_good_create import HelpGoodCreateCheckMethods



@ddt
class CreateGood(HelpGoodCheckMethods, HelpGoodData, HelpAuthCheckMethods, WarehouseCheckMethods, HelpNavigateData,
                     HelpGoodCreateCheckMethods):
    """
    Story: Добавить новый товар
    """

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        driver = webdriver.Chrome(CHROMEDRIVER_PATH)
        driver.implicitly_wait(time_to_wait=HelpNavigateData.timeout)
        driver.maximize_window()
        cls.driver = driver
        service_log.preparing_env(cls)

        # Берем тестового продавца на магазине которого будут проводиться проверки
        test_seller_id = AccountingMethods.get_default_user_id(role='seller')
        user = databases.db1.accounting.get_user_by_account_id(test_seller_id)[0]

        AccountingMethods.save_user_password(user_id=user["id"], hash_passwd=user["code_value"], salt=user["salt"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, user["salt"])
        databases.db1.accounting.update_user_password(user["id"], hash_res_new)

        cls.go_main(cls.driver, phone=user["phone"], passwd=default_new_passwd, flag_auth=True)
        cls.get_page(cls.driver, cls.path_my_goods.URL_ADD_GOOD)

    @skip('update')
    @priority("Must")
    def test_create_good_etalon(self, require_category=HelpGoodData.REQUIRE_CATEGORY,
                                require_fields=HelpGoodData.REQUIRE_FIELDS_ETALON,
                                img_path_list=HelpGoodData.IMG_PATH_LIST, select_country=HelpGoodData.COUNTRY,
                                select_color=HelpGoodData.SELECT_COLOR, select_material=HelpGoodData.SELECT_MATERIAL,
                                text_input=HelpGoodData.LIST_TEXT_INPUT):
        """
        Title: Я могу Добавить и Опубликовать новый товар, заполнив все поля эталонными значениями
        Description:
        Проверить:
        * При создании товара не возникло ошибок и предупреждений
        * После нажатия кнопки "Отправить" выполнен переход на страницу "Мои товары": "Активные"
        * Созданный товар отображается в списке Активных товаров
        * Проверить, что товар создан как Belived и Активный
        * Проверить, что в БД товар создался корректно

        Открыть полную карточку созданного товара и проверить:
        * Поля в карточке товара заполнены в соответствии с введенным при создани (в.т.ч фото)
        * Проверить корректность сформированной URL карточки товара
        """
        # добавляем фото
        for img_path in img_path_list:
            add_img_btn = self.get_element_navigate(self.driver, self.click_my_goods.ADD_PHOTO)
            add_img_btn.click()
            self.check_add_photo(img_path)
        # выбираем категорию
        xpath_category = self.click_my_goods.PATH_REQUIRE_FIELDS + self.click_my_goods.FIELD_CATEGORY
        self.select_category(self.driver, require_category, xpath_category)
        # заполняем имя и минимальную партию
        xpath_name = self.click_my_goods.PATH_REQUIRE_FIELDS + self.input_my_goods.ADD_GOOD_NAME
        xpath_min_stock = self.click_my_goods.PATH_REQUIRE_FIELDS + self.input_my_goods.ADD_GOOD_MIN_STOCK
        name = self.get_element_navigate(self.driver, xpath_name)
        min_stock = self.get_element_navigate(self.driver, xpath_min_stock)
        name.send_keys(require_fields['name'])
        min_stock.send_keys(require_fields['min_stock'])

        self.check_name_fields(self.driver)
        # выбираем страну изготовитель
        xpath_country = self.click_my_goods.PATH_FIELDS + self.click_my_goods.FIELD_CATEGORY
        self.select_category(self.driver, select_country, xpath_country)
        # выбираем цвет
        xpath_color = self.click_my_goods.PATH_FIELDS + self.click_my_goods.SELECT_COLOR
        self.select_multi_cast(self.driver, select_color, xpath_color, self.click_my_goods.PLUS_BTN)
        # выбираем материал
        xpath_material = self.click_my_goods.PATH_FIELDS + self.click_my_goods.SELECT_MATERIAL
        self.select_multi_cast(self.driver, select_material, xpath_material, self.click_my_goods.PLUS_BTN)
        self.set_input_fields(self.driver)
        # парсим страницу добавления товара, чтобы получить идентификаторы фотографий товара
        list_img_id = self.get_category_id_from_page_source(self.driver, self.path_my_goods.PATH_IMG_ID_START,
                                                            self.path_my_goods.PATH_IMG_ID_END)

        # жмем опубликовать
        btn_publish = self.get_element_navigate(self.driver, self.click_my_goods.ADD_GOOD_BTN_PUBLISH)
        self.click_button(btn_publish)
        # проверяем, что перешли в Активные
        self.get_element_navigate(self.driver, self.check_my_goods.MENU_ACTIVE % "Активные")
        # проверяем короткую карточку товара в Активных
        data_good = self.get_data_add_good(require_category, require_fields, list_img_id, text_input['price']['data'],
                                           text_input['remains']['data'])
        self.check_shot_card_good(self.driver, self.check_my_goods.SHOT_CARD_GOOD_DATA % 1, data_good)
        # проверяем фото в короткой карточке товара
        xpath_img_list_short = self.get_xpath_img_list(self.check_my_goods.SHOT_CARD_GOOD_PHOTO, [list_img_id[0]],
                                                       self.path_my_goods.PATH_IMG_ID_END)
        self.check_image_in_card(self.driver, xpath_img_list_short)
        # переходим на страницу товара
        name_good = self.get_element_navigate(self.driver, self.click_my_goods.NAME_CARD_GOOD % 1)
        self.click_button(name_good)
        # проверяем данные на странице товара
        xpath_img_list = self.get_xpath_img_list(self.check_good.GALLERY_PREVIEW_PHOTO, list_img_id,
                                                 self.path_good.PATH_IMG_ID_END)
        self.check_image_in_card(self.driver, xpath_img_list)
        self.check_card_good_require_fields(self.driver, data_good)
        self.check_card_good_text_fields(self.driver)
        self.check_selected_field(self.driver, select_color, self.check_good.COLOR)
        self.check_selected_field(self.driver, select_material, self.check_good.MATERIAL)

    @skip('update')
    @priority("High")
    def test_create_good_require(self, require_category=HelpGoodData.REQUIRE_CATEGORY,
                                 require_fields=HelpGoodData.REQUIRE_FIELDS_REQUIRE,
                                 img_path=HelpGoodData.IMG_PATH_LIST[0]):
        """
        Title: Я могу Добавить и Сохранить как черновик новый товар, заполнив только обязательные поля
        Description:
        Проверить:
        * При создании товара не возникло ошибок и предупреждений
        * После нажатия кнопки "Сохранить как черновик" выполнен переход на страницу "Мои товары": "Неактивные".
        * Созданный товар отображается на странице "Мои товары":"Неактивные"
        * Товар имеет статус Belived и Неактивный
        * В БД товар созался корректно

        Открыть полную карточку созданного товара и проверить:
        * Поля в карточке товара заполнены в соответствии с введенным при создани (в.т.ч фото)
        """
        # добавляем фото
        add_img_btn = self.get_element_navigate(self.driver, self.click_my_goods.ADD_PHOTO)
        add_img_btn.click()
        self.check_add_photo(img_path)
        # выбираем категорию
        xpath_category = self.click_my_goods.PATH_REQUIRE_FIELDS + self.click_my_goods.FIELD_CATEGORY
        self.select_category(self.driver, require_category, xpath_category)

        # заполняем имя и минимальную партию
        xpath_name = self.click_my_goods.PATH_REQUIRE_FIELDS + self.input_my_goods.ADD_GOOD_NAME
        xpath_min_stock = self.click_my_goods.PATH_REQUIRE_FIELDS + self.input_my_goods.ADD_GOOD_MIN_STOCK
        name = self.get_element_navigate(self.driver, xpath_name)
        min_stock = self.get_element_navigate(self.driver, xpath_min_stock)
        name.send_keys(require_fields['name'])
        min_stock.send_keys(require_fields['min_stock'])

        # парсим страницу добавления товара, чтобы получить идентификаторы фотографий товара
        list_img_id = self.get_category_id_from_page_source(self.driver, self.path_my_goods.PATH_IMG_ID_START,
                                                            self.path_my_goods.PATH_IMG_ID_END)
        # жмем опубликовать
        btn_publish = self.get_element_navigate(self.driver, self.click_my_goods.ADD_GOOD_BTN_PUBLISH)
        self.click_button(btn_publish)

        # проверяем, что перешли в Активные
        self.get_element_navigate(self.driver, self.check_my_goods.MENU_ACTIVE % "Активные")

        # проверяем короткую карточку товара в Активных
        data_good = self.get_data_add_good(require_category, require_fields, list_img_id)
        self.check_shot_card_good(self.driver, self.check_my_goods.SHOT_CARD_GOOD_DATA % 1, data_good)

        # проверяем фото в короткой карточке товара
        xpath_img_list_short = self.get_xpath_img_list(self.check_my_goods.SHOT_CARD_GOOD_PHOTO, [list_img_id[0]],
                                                       self.path_my_goods.PATH_IMG_ID_END)

        self.check_image_in_card(self.driver, xpath_img_list_short)
        # переходим на страницу товара

        name_good = self.get_element_navigate(self.driver, self.click_my_goods.NAME_CARD_GOOD % 1)
        self.click_button(name_good)
        # проверяем данные на странице товара

        xpath_img_list = self.get_xpath_img_list(self.check_good.GALLERY_PREVIEW_PHOTO, list_img_id,
                                                 self.path_good.PATH_IMG_ID_END)
        self.check_image_in_card(self.driver, xpath_img_list)
        self.check_card_good_require_fields(self.driver, data_good)

    @skip('manual')
    @priority("Medium")
    def test_create_good_maximum(self, require_category=HelpGoodData.REQUIRE_CATEGORY,
                                 require_fields=HelpGoodData.REQUIRE_FIELDS_MAXIMUM,
                                 img_path_list=HelpGoodData.IMG_PATH_LIST_MAX, select_country=HelpGoodData.COUNTRY,
                                 text_input=HelpGoodData.LIST_TEXT_INPUT_MAX):
        """
        Title: Создание товара максимальный вариант
        """
        # добавляем фото
        for img_path in img_path_list:
            add_img_btn = self.get_element_navigate(self.driver, self.click_my_goods.ADD_PHOTO)
            add_img_btn.click()
            self.check_add_photo(img_path)

        # выбираем категорию
        xpath_category = self.click_my_goods.PATH_REQUIRE_FIELDS + self.click_my_goods.FIELD_CATEGORY
        self.select_category(self.driver, require_category, xpath_category)
        # заполняем имя и минимальную партию
        xpath_name = self.click_my_goods.PATH_REQUIRE_FIELDS + self.input_my_goods.ADD_GOOD_NAME
        xpath_min_stock = self.click_my_goods.PATH_REQUIRE_FIELDS + self.input_my_goods.ADD_GOOD_MIN_STOCK
        name = self.get_element_navigate(self.driver, xpath_name)
        min_stock = self.get_element_navigate(self.driver, xpath_min_stock)
        name.send_keys(require_fields['name'])
        min_stock.send_keys(require_fields['min_stock'])
        self.check_name_fields(self.driver)
        # выбираем страну изготовитель
        xpath_country = self.click_my_goods.PATH_FIELDS + self.click_my_goods.FIELD_CATEGORY
        self.select_category(self.driver, select_country, xpath_country)
        # выбираем все цвета и материалы
        xpath_color = self.click_my_goods.PATH_FIELDS + self.click_my_goods.SELECT_COLOR
        list_options_color = self.get_options_in_select(self.driver, xpath_color % (0, ''))[1:]
        self.select_all_options(self.driver, xpath_color, list_options_color, self.click_my_goods.PLUS_BTN)

        xpath_material = self.click_my_goods.PATH_FIELDS + self.click_my_goods.SELECT_MATERIAL
        list_options_material = self.get_options_in_select(self.driver, xpath_material % (0, ''))[1:]
        self.select_all_options(self.driver, xpath_material, list_options_material, self.click_my_goods.PLUS_BTN)
        self.set_input_fields(self.driver, text_input)
        # парсим страницу добавления товара, чтобы получить идентификаторы фотографий товара
        list_img_id = self.get_category_id_from_page_source(self.driver, self.path_my_goods.PATH_IMG_ID_START,
                                                            self.path_my_goods.PATH_IMG_ID_END)
        # проверяем, что нельзя добавить 6-е фото
        msg = 'Можно добавить 6 фото'
        self.check_no_such_element(self.driver, test_data=dict(xpath=self.click_my_goods.ADD_PHOTO, err_msg=msg))
        # жмем опубликовать
        btn_publish = self.get_element_navigate(self.driver, self.click_my_goods.ADD_GOOD_BTN_PUBLISH)
        self.click_button(btn_publish)
        # проверяем, что перешли в Активные
        self.get_element_navigate(self.driver, self.check_my_goods.MENU_ACTIVE % "Активные")
        # проверяем короткую карточку товара в Активных
        data_good = self.get_data_add_good(require_category, require_fields, list_img_id, text_input['price']['data'],
                                           text_input['remains']['data'])
        self.check_shot_card_good(self.driver, self.check_my_goods.SHOT_CARD_GOOD_DATA % 1, data_good)
        # проверяем фото в короткой карточке товара
        xpath_img_list_short = self.get_xpath_img_list(self.check_my_goods.SHOT_CARD_GOOD_PHOTO, [list_img_id[0]],
                                                       self.path_my_goods.PATH_IMG_ID_END)
        self.check_image_in_card(self.driver, xpath_img_list_short)
        # переходим на страницу товара
        name_good = self.get_element_navigate(self.driver, self.click_my_goods.NAME_CARD_GOOD % 1)
        self.click_button(name_good)
        # проверяем данные на странице товара
        xpath_img_list = self.get_xpath_img_list(self.check_good.GALLERY_PREVIEW_PHOTO, list_img_id,
                                                 self.path_good.PATH_IMG_ID_END)
        self.check_image_in_card(self.driver, xpath_img_list)
        self.check_card_good_require_fields(self.driver, data_good)
        self.check_card_good_text_fields(self.driver, text_input)
        self.check_selected_field(self.driver, list_options_color, self.check_good.COLOR)
        self.check_selected_field(self.driver, list_options_material, self.check_good.MATERIAL)

    @skip('manual')
    @priority("Medium")
    def test_create_good_minimum(self, require_category=HelpGoodData.REQUIRE_CATEGORY,
                                 require_fields=HelpGoodData.REQUIRE_FIELDS_MINIMUM,
                                 img_path=HelpGoodData.IMG_PATH_LIST[0], select_country=HelpGoodData.COUNTRY,
                                 select_color=HelpGoodData.SELECT_COLOR_ONE,
                                 select_material=HelpGoodData.SELECT_MATERIAL_ONE,
                                 text_input=HelpGoodData.LIST_TEXT_INPUT_MIN):
        """
        Title: Создание товара минимальный вариант
        """
        # добавляем фото
        add_img_btn = self.get_element_navigate(self.driver, self.click_my_goods.ADD_PHOTO)
        add_img_btn.click()
        self.check_add_photo(img_path)
        # выбираем категорию
        xpath_category = self.click_my_goods.PATH_REQUIRE_FIELDS + self.click_my_goods.FIELD_CATEGORY
        self.select_category(self.driver, require_category, xpath_category)
        # заполняем имя и минимальную партию
        xpath_name = self.click_my_goods.PATH_REQUIRE_FIELDS + self.input_my_goods.ADD_GOOD_NAME
        xpath_min_stock = self.click_my_goods.PATH_REQUIRE_FIELDS + self.input_my_goods.ADD_GOOD_MIN_STOCK
        name = self.get_element_navigate(self.driver, xpath_name)
        min_stock = self.get_element_navigate(self.driver, xpath_min_stock)
        name.send_keys(require_fields['name'])
        min_stock.send_keys(require_fields['min_stock'])
        self.check_name_fields(self.driver)
        # выбираем страну изготовитель
        xpath_country = self.click_my_goods.PATH_FIELDS + self.click_my_goods.FIELD_CATEGORY
        self.select_category(self.driver, select_country, xpath_country)
        # выбираем цвет
        xpath_color = self.click_my_goods.PATH_FIELDS + self.click_my_goods.SELECT_COLOR
        self.select_multi_cast(self.driver, select_color, xpath_color, self.click_my_goods.PLUS_BTN)
        # выбираем материал
        xpath_material = self.click_my_goods.PATH_FIELDS + self.click_my_goods.SELECT_MATERIAL
        self.select_multi_cast(self.driver, select_material, xpath_material, self.click_my_goods.PLUS_BTN)
        self.set_input_fields(self.driver, text_input)
        # парсим страницу добавления товара, чтобы получить идентификаторы фотографий товара
        list_img_id = self.get_category_id_from_page_source(self.driver, self.path_my_goods.PATH_IMG_ID_START,
                                                            self.path_my_goods.PATH_IMG_ID_END)

        # жмем опубликовать
        btn_publish = self.get_element_navigate(self.driver, self.click_my_goods.ADD_GOOD_BTN_PUBLISH)
        self.click_button(btn_publish)
        # проверяем, что перешли в Активные
        self.get_element_navigate(self.driver, self.check_my_goods.MENU_ACTIVE % "Активные")
        # проверяем короткую карточку товара в Активных
        data_good = self.get_data_add_good(require_category, require_fields, list_img_id, text_input['price']['data'],
                                           text_input['remains']['data'])
        self.check_shot_card_good(self.driver, self.check_my_goods.SHOT_CARD_GOOD_DATA % 1, data_good)
        # проверяем фото в короткой карточке товара
        xpath_img_list_short = self.get_xpath_img_list(self.check_my_goods.SHOT_CARD_GOOD_PHOTO, [list_img_id[0]],
                                                       self.path_my_goods.PATH_IMG_ID_END)
        self.check_image_in_card(self.driver, xpath_img_list_short)
        # переходим на страницу товара
        name_good = self.get_element_navigate(self.driver, self.click_my_goods.NAME_CARD_GOOD % 1)
        self.click_button(name_good)
        # проверяем данные на странице товара
        xpath_img_list = self.get_xpath_img_list(self.check_good.GALLERY_PREVIEW_PHOTO, list_img_id,
                                                 self.path_good.PATH_IMG_ID_END)
        self.check_image_in_card(self.driver, xpath_img_list)
        self.check_card_good_require_fields(self.driver, data_good)
        self.check_card_good_text_fields(self.driver, text_input)
        self.check_selected_field(self.driver, select_color, self.check_good.COLOR)
        self.check_selected_field(self.driver, select_material, self.check_good.MATERIAL)

    @skip('manual')
    @priority("Low")
    def test_create_good_cancel(self):
        """
        Title: Я могу заполнить форму создания товара, но не сохранять изменения. Товар не создастся
        Description:
        * После нажатия "Отмена" я возвращусь на страницу откуда инициировал открытие формы создания товара
        * Новый товар не создастся с БД
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()



class EditGood():
    """
    Story: Редкатировать свой товар
    """

    @skip('need_auto')
    @priority("High")
    def test_edit_good_change_all_field(self):
        """
        Title: Я могу Отредактировать свой товар, изменив все поля.
        Description:
        Проверить:
        * После нажатия кнопки "Отправить" выполнен переход на страницу "Мои товары": "Активные"
        * Проверить, что в БД данные по товару изменены корректно
        * Товар сбросит статус на Belived и Активный

        Открыть полную карточку созданного товара и проверить:
        * Поля в карточке товара заполнены в соответствии с измененными данными (в.т.ч фото)
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_edit_good_cancel(self):
        """
        Title: Я могу отредактировать товар, но не сохранять изменения. Данные товара не изменятся.
        Description:
        * После нажатия "Отмена" я возвращусь на страницу откуда инициировал открытие формы редактирования товара
        * Данные товара в БД не изменятся
        """
        pass



class EditGoodByModerator():
    """
    Story: Модератор может Редактировать любой товар
    """

    @skip('need_auto')
    @priority("High")
    def test_edit_good_by_moderator_change_all_field(self):
        """
        Title: Модераторо может отредактировать все поля товара любого пользователя
        Description:
        Проверить:
        * После нажатия кнопки "Отправить" выполнен переход на карточку редактируемого товара
        * Проверить, что в БД данные по товару изменены корректно
        * Проверить, что товар останется в том же статусе модерации в котором и был до редактирования.

        Открыть полную карточку созданного товара и проверить:
        * Поля в карточке товара заполнены в соответствии с измененными данными (в.т.ч фото)
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_edit_good_by_moderator_cancel(self):
        """
        Title: Модератор может  отредактировать товар, но не сохранять изменения. Данные товара не изменятся.
        Description:
        * После нажатия кнопки "Отправить" выполнен переход на карточку редактируемого товара
        * Данные товара в БД не изменятся
        """
        pass




class GoodPhoto():
    """
    Story: Тесты на работу с фотографими товаров
    """

    @skip('manual')
    @priority("Medium")
    def test_add_or_delete_photo_on_add_good_page(self):
        """
        Title: Добавление \ Удаление фото
        Description:
        * При клике на плейсхолдер для фото на карточке добавления товара - открывается диалог добавления фото
        * При нажатии на «Х» фотография удаляется
        """
        pass

    @skip('manual')
    @priority("High")
    def test_change_photo_positiond_on_add_good_page(self):
        """
        Title: Изменение очередности фото
        Description:
        * есть возможность изменить очередность фотографий drag'n'drop
        * после изменения очередности фото, новая первая фото - становится обложкой товара в карточках товара.
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_miniature_of_photo(self):
        """
        Title: Для загружаемой в карточку товара фото, на сервере создается три миниатюры
        Description:
        * 650x650
        * 226x226
        * 75x75
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_size_miniature_of_photo(self):
        """
        Title: Проверить размер фото на сайте (для сущ-го и вновь созданного) не  более 500кб
        Description:
        * Для 2-5 товаров с сайта скачать их zoom-фото и проверить что вес каждого не превышает 500кб
        * Создать товар с тяжелым фото (более 2мб) и скачать его zoom-фото и проверить что его размер не превышает 500кб
        """
        pass



class OtherTests():
    """
    Story: Прочие тесты
    """

    @skip('manual')
    @priority("Low")
    def test_add_or_edit_good_form_catalog_field(self):
        """
        Title: Отображение категорий и подкатегорий каталога в форме добавления товара
        Description:
        Тут нужно написать один тест, который получает значения выпадающих списков  для каждого раздела и каждой категории
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_add_or_edit_good_form_color_field(self):
        """
        Title: Добавление нескольких вариантов цветов к материалу
        Description:
        * при нажатии кнопки "Добавить цвет" появляется еще один выпадающий список с возможностью выбрать еще один цвет
        (при этом уже ранее выбранный цвет отсутствует в списке).
        * при нажатии кнопки "X" (в случае, когда есть несколько полей с цветом) данная строка удаляется.
        * при нажатии кнопки "X" (в случае, когда поле с цветом всего одна) выбранное значение сбрасывается на значение по дефолту
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_add_or_edit_good_form_material_field(self):
        """
        Title: Добавление нескольких вариантов цветов к материалу
        Description:
        * при нажатии кнопки "Добавить материал" появляется еще один выпадающий список с возможностью выбрать еще один материал
        (при этом уже ранее выбранный материал отсутствует в списке).
        * при нажатии кнопки "X" (в случае, когда есть несколько строк с материалами) данная строка удаляется.
        * при нажатии кнопки "X" (в случае, когда строка с материалами всего одна) выбранное значение сбрасывается назначение по дефолту
        """
        pass




class CreateGoodForm():
    """
    Story: Форма Добавления товара
    """

    @skip('manual')
    @priority("Medium")
    def test_create_good_form_view(self):
        """
        Title: Вид формы добавления товара
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_create_good_form_validation_positive(self):
        """
        Title: Проверка ограничения на поля формы: Позитивные значения
        Description:
        Наборы значений: Зеленые из таблицы сущностей, проверить:
        * Появилось сообщение об успешном сохранении изменений
        * Проверить корректность сохранения значений в базе данных
        * Проверить корректность отображения сделанных изменений на странице товара
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_create_good_form_validation_negative(self):
        """
        Title: Проверка ограничения на поля формы: Негативные значения
        Description:
        Наборы значений: Красные из таблицы сущностей, проверить:
        * невозможность сохранить изменения
        * выдачу соответствующего предупреждающего сообщения
        * в базе значения измененных полей не поменялись на новые.
        """
        pass






'''
@ddt
class TestGoodCreateNegative(HelpGoodCheckMethods, HelpGoodData, HelpAuthCheckMethods, HelpProfileSettingsCheckMethods,
                             HelpNavigateData, HelpGoodCreateCheckMethods):
    """
    Story: Создание товара - негативные значения
    """
    @classmethod
    def setUp(cls):
        # Берем тестового продавца на магазине которого будут проводиться проверки
        test_seller_id = AccountingMethods.get_default_user_id(role='seller')
        user = databases.db1.accounting.get_user_by_account_id(test_seller_id)[0]
        AccountingMethods.save_user_password(user_id=user["id"], hash_passwd=user["code_value"], salt=user["salt"])

        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, user["salt"])
        databases.db1.accounting.update_user_password(user["id"], hash_res_new)

        # Подготовка работы с selenium
        driver = webdriver.Chrome(CHROMEDRIVER_PATH)
        driver.implicitly_wait(time_to_wait=HelpNavigateData.timeout)
        driver.maximize_window()
        cls.driver = driver
        cls.go_main(cls.driver, phone=user["phone"], passwd=default_new_passwd, flag_auth=True)
        cls.get_page(cls.driver, cls.path_my_goods.URL_ADD_GOOD)
        service_log.preparing_env(cls)

    @skip('update')
    @priority("medium")
    @data(*HelpGoodData.LIST_TEXT_INPUT_NEGATIVE)
    def test_create_good_negative_text_input(self, test_data):
        """
        Title: Тест проверяет негативные значения для всех текстовых полей кроме названия товара
        """
        # жмем опубликовать
        btn_publish = self.get_element_navigate(self.driver, self.click_my_goods.ADD_GOOD_BTN_PUBLISH)
        self.click_button(btn_publish)
        # начинаем проверять
        values_list = self.LIST_TEXT_INPUT_NEGATIVE[test_data]
        for value in values_list['data']:
            obj_input = self.get_element_navigate(self.driver, values_list['input_xpath'])
            self.clear_input_row(self.driver, obj_input)
            obj_input.send_keys(value['value'])
            btn_publish = self.get_element_navigate(self.driver, self.click_my_goods.ADD_GOOD_BTN_PUBLISH)
            self.click_button(btn_publish)
            check_err = self.get_element_navigate(self.driver, values_list['err_xpath'] % value['err'])

    @skip('update')
    @priority("medium")
    @data(*HelpGoodData.LIST_TEXT_INPUT_NEGATIVE_EMPTY)
    def test_create_good_negative_require_fields_empty(self, test_data):
        """
        Title: Тест проверяет пустые значения в обязательных для заполнения полях
        """
        # жмем опубликовать
        btn_publish = self.get_element_navigate(self.driver, self.click_my_goods.ADD_GOOD_BTN_PUBLISH)
        self.click_button(btn_publish)
        # начинаем проверять
        values_list = self.LIST_TEXT_INPUT_NEGATIVE_EMPTY[test_data]
        for value in values_list['data']:
            check_err = self.get_element_navigate(self.driver, values_list['err_xpath'] % value['err'])

    @skip('update')
    @priority("medium")
    def test_create_good_negative_category_four(self, test_data=HelpGoodData.CATEGORY_FOUR):
        """
        Title: Тест проверяет недозаполненые категории
        """
        # жмем опубликовать
        btn_publish = self.get_element_navigate(self.driver, self.click_my_goods.ADD_GOOD_BTN_PUBLISH)
        self.click_button(btn_publish)
        err_data = self.LIST_TEXT_INPUT_NEGATIVE_EMPTY['categorySelect-1']
        xpath_category = self.click_my_goods.PATH_REQUIRE_FIELDS + self.click_my_goods.FIELD_CATEGORY
        msg = "После выбора финальной категории осталась ошибка Выберите категорию."
        # начинаем проверять
        for index, category in enumerate(test_data):
            self.select_category(self.driver, [test_data[index]], xpath_category)
            if index != len(test_data)-1:
                check_err = self.get_element_navigate(self.driver, err_data['err_xpath'] % err_data['data'][0]['err'])
            else:
                self.check_no_such_element(self.driver, test_data=dict(xpath=err_data['err_xpath'], err_msg=msg))



    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()
'''