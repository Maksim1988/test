# coding=utf-8
import random

from support import service_log
from support.utils.db import databases
from support.utils.thrift4req import services
from support.utils.variables import EVariable
from tests.MainClass import MainClass
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateData, HelpNavigateMethods, HelpNavigateCheckMethods
from tests.front_office.data_navigation import GoodPage
from tests.worker_warehouse.class_warehouse import WarehouseMethods
from support.utils import common_utils


__author__ = 'm.senchuk'


class HelpGoodData(MainClass):

    PRICE_GOOD = {
        'price': 555,
        'without_price': None,
    }

    REQUIRE_CATEGORY = ['Одежда',
                        'Верх',
                        'Для женщин',
                        'Платья']

    CAT_1 = ["Одежда",
             "Верх",
             "Для женщин",
             "Платья"]

    CAT_2 = ["Обувь и аксессуары",
             "Аксессуары",
             "Для женщин",
             "Банданы"]

    CAT_3 = ["Товары для дома",
             "Текстиль",
             "Одеяла"]

    CAT_4 = ["Товары для сада",
             "Растения",
             "Газоны"]

    CAT_SUITE = {
        "Одежда": CAT_1,
        "Обувь и аксессуары": CAT_2,
        "Товары для дома": CAT_3,
        "Товары для сада": CAT_4
    }

    CATEGORY_FOUR = ['Детская одежда', 'Для подростков', 'Для девочек', 'Платья']

    REQUIRE_FIELDS_ETALON = {'name': u'Комплект платьев ' + str(random.randrange(1000, 9999, 1)),
                             'min_stock': str(random.randrange(10, 70, 1))
    }
    REQUIRE_FIELDS_REQUIRE = {'name': u'Красное платье ' + str(random.randrange(1000, 9999, 1)),
                              'min_stock': str(random.randrange(10, 70, 1))
    }
    REQUIRE_FIELDS_MAXIMUM = {'name': u'Комплект платьев maximum ' + common_utils.random_string(length=100),
                              'min_stock': '999'
    }
    REQUIRE_FIELDS_MINIMUM = {'name': common_utils.random_string(length=1),
                              'min_stock': '1'
    }
    REQUIRE_FIELDS_POSITIVE = {'name': '0',
                               'min_stock': '100'
    }

    IMG_PATH_LIST = ['C:\Data\img\\' + u'имя+файла.jpg',
                     "C:\Data\img\File name.jpg",
                     "C:\Data\img\\" + u"ИмяФайла2252x3648.jpg"]

    IMG_AVATAR = ['C:\Data\img\8108263.jpg']

    IMG_PATH_LIST_MAX = ['C:\Data\img\\' + u'имя+файла.jpg',
                         "C:\Data\img\File name.jpg",
                         "C:\Data\img\\" + u"ИмяФайла2252x3648.jpg",
                         "C:\Data\img\\" + u"y3_4-rr.rr.jpeg",
                         "C:\Data\img\Kim_Kardashian_Midori_Green_HaloCostume_Party_Vettri.Net-35.jpg"
    ]
    COUNTRY = ['Китай']
    SELECT_COLOR = ['Черный',
                    'Зеленый',
                    'Белый',
                    'Красный']

    SELECT_MATERIAL = ['Велюр',
                       'Кожа',
                       'Шелк',
                       'Акрил']

    SELECT_COLOR_ONE = ['Черный']

    SELECT_MATERIAL_ONE = ['Велюр']

    LIST_NAME_FIELDS = ['Остаток, шт.:',
                        'Цена за штуку, руб.:',
                        'Артикул:',
                        'Бренд:',
                        'Страна-изготовитель:',
                        'Число товаров в упаковке, шт.:',
                        'Материал:',
                        'Цвет:',
                        'Размеры:',
                        'Описание:']

    LIST_TEXT_INPUT = {
        'price': {
            'xpath': HelpNavigateData.input_my_goods.PRICE,
            'data': str(random.randrange(1, 999, 1))
        },
        'remains': {
            'xpath': HelpNavigateData.input_my_goods.REMAINS,
            'data': str(random.randrange(1, 1000, 1))
        },
        'article': {
            'xpath': HelpNavigateData.input_my_goods.ARTICLE,
            'data': common_utils.random_string('all', 15)
        },
        'brand_name': {
            'xpath': HelpNavigateData.input_my_goods.BRAND_NAME,
            'data': common_utils.random_string('all', 15)
        },
        'stock_size': {
            'xpath': HelpNavigateData.input_my_goods.STOCK_SIZE,
            'data': str(random.randrange(1, 99, 1))
        },
        'size_plain': {
            'xpath': HelpNavigateData.input_my_goods.SIZES_PLAIN,
            'data': common_utils.random_string('all', 20)
        },
        'description': {
            'xpath': HelpNavigateData.input_my_goods.DESCRIPTION,
            'data': common_utils.random_string('all', 300)
        },
    }

    LIST_TEXT_INPUT_MAX = {
        'price': {
            'xpath': HelpNavigateData.input_my_goods.PRICE, 'data': str(9999999)},
        'remains': {
            'xpath': HelpNavigateData.input_my_goods.REMAINS, 'data': str(1000)},
        'article': {
            'xpath': HelpNavigateData.input_my_goods.ARTICLE, 'data': common_utils.random_string('all', 128)},
        'brand_name': {
            'xpath': HelpNavigateData.input_my_goods.BRAND_NAME, 'data': common_utils.random_string('all', 128)},
        'stock_size': {
            'xpath': HelpNavigateData.input_my_goods.STOCK_SIZE, 'data': str(9999999)},
        'size_plain': {
            'xpath': HelpNavigateData.input_my_goods.SIZES_PLAIN, 'data': common_utils.random_string('all', 128)},
        'description': {
            'xpath': HelpNavigateData.input_my_goods.DESCRIPTION, 'data': common_utils.random_string('all', 500)},
    }

    LIST_TEXT_INPUT_MIN = {
        'price': {
            'xpath': HelpNavigateData.input_my_goods.PRICE, 'data': str(random.randrange(1, 9, 1))},
        'remains': {
            'xpath': HelpNavigateData.input_my_goods.REMAINS, 'data': str(random.randrange(1, 9, 1))},
        'article': {
            'xpath': HelpNavigateData.input_my_goods.ARTICLE, 'data': common_utils.random_string('all', 1)},
        'brand_name': {
            'xpath': HelpNavigateData.input_my_goods.BRAND_NAME, 'data': common_utils.random_string('all', 1)},
        'stock_size': {
            'xpath': HelpNavigateData.input_my_goods.STOCK_SIZE, 'data': str(random.randrange(1, 9, 1))},
        'size_plain': {
            'xpath': HelpNavigateData.input_my_goods.SIZES_PLAIN, 'data': common_utils.random_string('all', 1)},
        'description': {
            'xpath': HelpNavigateData.input_my_goods.DESCRIPTION, 'data': common_utils.random_string('all', 1)},
    }

    LIST_TEXT_INPUT_POSITIVE = {
        'price': {
            'xpath': HelpNavigateData.input_my_goods.PRICE, 'data': '01000'},
        'remains': {
            'xpath': HelpNavigateData.input_my_goods.REMAINS, 'data': '0100'},
        'article': {
            'xpath': HelpNavigateData.input_my_goods.ARTICLE, 'data': ' '},
        'brand_name': {
            'xpath': HelpNavigateData.input_my_goods.BRAND_NAME, 'data': ' '},
        'stock_size': {
            'xpath': HelpNavigateData.input_my_goods.STOCK_SIZE, 'data': '050'},
        'size_plain': {
            'xpath': HelpNavigateData.input_my_goods.SIZES_PLAIN, 'data': ' '},
        'description': {
            'xpath': HelpNavigateData.input_my_goods.DESCRIPTION, 'data': ' '},
    }

    LIST_TEXT_INPUT_NEGATIVE = {
        'min_stock': {
            'input_xpath': HelpNavigateData.input_my_goods.ADD_GOOD_MIN_STOCK,
            'err_xpath': HelpNavigateData.check_my_goods.ERR_MIN_STOCK,
            'data': [
                {'value': u'ренwd', 'err': 'Введите целое число'},
                {'value': u'50 шт.', 'err': 'Введите целое число'},
                {'value': '1,66', 'err': 'Введите целое число'},
                {'value': '1000', 'err': 'Число не должно быть больше 999'},
                {'value': '', 'err': 'Обязательное поле'},
                {'value': '0', 'err': 'Число не должно быть меньше 1'},
                {'value': u' \ / : * ? " < > |', 'err': 'Введите целое число'},
                {'value': u'! № @ ; # ? $ % ^ & ( ) + _ - "', 'err': 'Введите целое число'},
                {'value': '-1', 'err': 'Число не должно быть меньше 1'}
            ]
        },
        'remains': {
            'input_xpath': HelpNavigateData.input_my_goods.REMAINS,
            'err_xpath': HelpNavigateData.check_my_goods.ERR_REMAINS,
            'data': [
                {'value': 'h', 'err': 'Введите целое число'},
                {'value': u'50 шт.', 'err': 'Введите целое число'},
                {'value': '1,66', 'err': 'Введите целое число'},
                {'value': '10000000', 'err': 'Число не должно быть больше 9999999'},
                # {'value': '0', 'err': ''},
                {'value': u' \ / : * ? " < > |', 'err': 'Введите целое число'},
                {'value': u'! № @ ; # ? $ % ^ & ( ) + _ - "', 'err': 'Введите целое число'},
                {'value': '-1', 'err': 'Число не должно быть меньше '}
            ]
        },
        'price': {
            'input_xpath': HelpNavigateData.input_my_goods.PRICE,
            'err_xpath': HelpNavigateData.check_my_goods.ERR_PRICE,
            'data': [
                {'value': 'hfgh', 'err': 'Введите целое число'},
                {'value': u'1000 руб.', 'err': 'Введите целое число'},
                {'value': '1,66', 'err': 'Введите целое число'},
                {'value': '10000000', 'err': 'Число не должно быть больше 9999999'},
                {'value': '0', 'err': 'Введите число больше 0'},
                {'value': u' \ / : * ? " < > |', 'err': 'Введите целое число'},
                {'value': u'! № @ ; # ? $ % ^ & ( ) + _ - "', 'err': 'Введите целое число'},
                {'value': '-1', 'err': 'Введите число больше 0'}
            ]
        },
        'stock_size': {
            'input_xpath': HelpNavigateData.input_my_goods.STOCK_SIZE,
            'err_xpath': HelpNavigateData.check_my_goods.ERR_STOCK_SIZE,
            'data': [
                {'value': 'tgre', 'err': 'Введите целое число'},
                {'value': u'50 шт.', 'err': 'Введите целое число'},
                {'value': '1,66', 'err': 'Введите целое число'},
                {'value': '10000000', 'err': 'Число не должно быть больше 9999999'},
                {'value': u' \ / : * ? " < > |', 'err': 'Введите целое число'},
                {'value': u'! № @ ; # ? $ % ^ & ( ) + _ - "', 'err': 'Введите целое число'},
                {'value': '-1', 'err': 'Число не должно быть меньше '}
            ]
        },
    }

    LIST_TEXT_INPUT_NEGATIVE_EMPTY = {
        'name': {
            'input_xpath': HelpNavigateData.input_my_goods.ADD_GOOD_NAME,
            'err_xpath': HelpNavigateData.check_my_goods.ERR_NAME,
            'data': [
                {'value': None, 'err': 'Обязательное поле'}
            ]
        },
        'categorySelect-1': {
            'input_xpath': None,
            'err_xpath': HelpNavigateData.check_my_goods.ERR_CATEGORY_1,
            'data': [
                {'value': None, 'err': 'Выберите категорию товара'}
            ]
        },
        'file': {
            'input_xpath': None,
            'err_xpath': HelpNavigateData.check_my_goods.ERR_FILE,
            'data': [
                {'value': None, 'err': 'Загрузите хотя бы одну фотографию товара'}
            ]
        },
    }


class HelpGoodMethods(HelpGoodData):

    @staticmethod
    def select_category(driver, category_list, xpath_category):
        """
        Метод выбирает категории из селектеров
        :param driver:
        :param category_list: - список категорий, от родительской до финальной
        :param xpath_category: - xpath селектера
        :return:
        """
        for category in category_list:
            select_cat = HelpNavigateMethods.get_element_navigate(driver, xpath_category % category)
            select_cat.click()

    @staticmethod
    def select_multi_cast(driver, category_list, xpath_category, xpath_multi):
        """
        Метод выбирает категории из селектеров
        :param driver:
        :param category_list: - список категорий, от родительской до финальной
        :param xpath_category: - xpath селектера
        :return:
        """
        for index, category in enumerate(category_list):
            select_cat = HelpNavigateMethods.get_element_navigate(driver, xpath_category % (index, category))
            select_cat.click()
            plus_btn = HelpNavigateMethods.get_element_navigate(driver,
                                                                xpath_category % (index, category) + xpath_multi)
            plus_btn.click()

    @staticmethod
    def get_data_add_good(list_category, require_fields, list_img_id, price=None, remains=None):
        """
        Вспомогательный метод, который структурирует данные о товаре, отображаемсые на короткой карточке
        :param list_category: - список категорий, от родительской до финальной
        :param require_fields: - обязательные поля, имя и минимальная партия
        :param price: - цена за шт.
        :return:
        """

        data = {'name': require_fields['name'].encode('utf-8'),
                'cat_1': list_category[0],
                'cat_2': list_category[1],
                'cat_3': list_category[2],
                'cat_4': list_category[3],
                'min_stock': require_fields['min_stock'],
                'remains': remains,
                'price': "---" if price is None else price}

        for num, img in enumerate(list_img_id):
            data.update({'img_%s' % (num + 1): img})
        return data

    @staticmethod
    def get_xpath_img_list(xpath_img, img_id_list, img_size):
        """
        Вспомогательный метод, собирает xpath для фотографий
        :param xpath_img:
        :param img_id_list:
        :return:
        """
        xpath_img_list = []
        for num, img_id in enumerate(img_id_list):
            xpath_img_list.append(xpath_img % ((num + 1), img_id, img_size))
        return xpath_img_list

    @staticmethod
    def set_input_fields(driver, list_data=None):
        """
        Метод заполняет текстовые поля при создании товара
        :param driver:
        :param list_data:
        :return:
        """
        if list_data is None:
            list_data = HelpGoodData.LIST_TEXT_INPUT
        for data in list_data:
            obj_input = HelpNavigateMethods.get_element_navigate(driver, list_data[data]['xpath'])
            obj_input.send_keys(list_data[data]['data'])

    @staticmethod
    def get_options_in_select(driver, select_xpath):
        """
        Метод собирает все опции для селкетора и возвращает список опций
        :param driver:
        :param select_xpath:
        :return:
        """
        list_options = []
        obj_list_options = driver.find_elements_by_xpath(select_xpath)
        for obj_options in obj_list_options:
            list_options.append(obj_options.text.encode('utf-8'))
        return list_options

    @staticmethod
    def select_all_options(driver, select_xpath, list_options, plus_xpath):
        """
        Метод выбирает все варианты в селекторе
        :param driver:
        :param select_xpath:
        :param plus_xpath:
        :return:
        """
        for key, option in enumerate(list_options):
            obj_option = HelpNavigateMethods.get_element_navigate(driver, select_xpath % (key, option))
            obj_option.click()
            if key != len(list_options) - 1:
                obj_plus = HelpNavigateMethods.get_element_navigate(driver, select_xpath % (key, option) + plus_xpath)
                obj_plus.click()

    @staticmethod
    def set_price_for_good_by_id(good_id, value=None):
        """
        Метод задает значение поля цена для товара в зависимости от выбранной стратегии
        :param good_id:
        :param price_strategy:
        :return:
        """
        # TODO: не работает
        ware_cassandra = databases.db0.warehouse.get_wares_by_ware_id(good_id)[0]
        WarehouseMethods.update_data_content(ware_cassandra,
                                             WarehouseMethods.deserialize_content(ware_cassandra['content']))
        ware_obj = WarehouseMethods.req_update_ware(good_id, ware_cassandra['managed_category'],
                                                    ware_cassandra['content'])
        ware_obj.newWareContent.currencyFields['price'].amount.significand = value
        services.warehouse.root.tframed.updateWare(ware_obj)
        return value

    @staticmethod
    def set_photo(ware_cassandra, good_id):
        """
        Метод добавляет фото к товару
        :param ware_cassandra:
        :param good_id:
        :return:
        """
        if len(ware_cassandra['content']['pictures']['value']) < 5:
            ware_cassandra['content']['pictures']['value'].append(ware_cassandra['content']['pictures']['value'][0])
            ware_obj = WarehouseMethods.req_update_ware(good_id, ware_cassandra['managed_category_id'],
                                                        ware_cassandra['content'])
            services.warehouse.root.tframed.updateWare(ware_obj)

    @staticmethod
    def get_breadcrumbs(driver, xpath_breads=HelpNavigateCheckMethods.click_good.BREADCRUMBS):
        """
        Получить названия хлебных крошек
        :param driver:
        :return:
        """
        service_log.put("Get breadcrumbs.")
        bread_dict_value = {
            "root_cat": HelpNavigateCheckMethods.get_element_navigate(driver, xpath_breads % 1).text.encode('utf-8'),
            "cat": HelpNavigateCheckMethods.get_element_navigate(driver, xpath_breads % 2).text.encode('utf-8'),
            "final_cat": HelpNavigateCheckMethods.get_element_navigate(driver, xpath_breads % 3).text.encode('utf-8')
        }
        service_log.put("Get breadcrumbs - successful")
        return bread_dict_value

    @staticmethod
    def get_breadcrumb_list(driver, xpath_breads=HelpNavigateCheckMethods.click_good.BREADCRUMB_LIST):
        """ Получить названия хлебных крошек
        :param driver:
        :return:
        """
        bread_list_value = []
        service_log.put("Get breadcrumb list.")
        obj_bread_list = driver.find_elements_by_xpath(xpath_breads)
        for obj_bread in obj_bread_list:
            bread_list_value.append(obj_bread.text.encode('utf-8'))
            service_log.put("Breadcrumb='%s'" % obj_bread.text.encode('utf-8'))
        service_log.put("Get breadcrumbs - successful")
        return bread_list_value

    @staticmethod
    def set_categories(driver, new_category_not=None):
        """
        Задать новые категории для товара
        :param driver:
        :param new_categories_dict:
        :return:
        """
        root_cat_xpath = HelpNavigateCheckMethods.click_my_goods.ROOT_CATEGORY % ''
        obj_categories = driver.find_elements_by_xpath(root_cat_xpath)
        service_log.put("Get all root categories obj.")
        list_root_cat = []
        for obj_cat in obj_categories:
            list_root_cat.append(obj_cat.text.encode('utf-8'))
        service_log.put("Create list root categories='%s'" % list_root_cat)
        list_root_cat.remove(new_category_not)
        try:
            list_root_cat.remove("Выберите категорию")
            list_root_cat.remove("Товары для детей")
            list_root_cat.remove("Торговое оборудование")
        except Exception:
            pass
        service_log.put(
            "Remove old root category='%s' from list root category='%s'" % (new_category_not, list_root_cat))
        new_root = random.choice(list_root_cat)
        new_root_xpath = HelpNavigateCheckMethods.click_my_goods.ROOT_CATEGORY % new_root
        obj_root_cat = HelpNavigateCheckMethods.get_element_navigate(driver, new_root_xpath)
        service_log.put("Get new root category='%s'" % new_root)
        HelpAuthCheckMethods.click_button(obj_root_cat)
        xpath_category = HelpNavigateCheckMethods.click_my_goods.PATH_REQUIRE_FIELDS + \
                         HelpNavigateCheckMethods.click_my_goods.FIELD_CATEGORY
        HelpGoodMethods.select_category(driver, HelpGoodData.CAT_SUITE[new_root], xpath_category)
        return HelpGoodData.CAT_SUITE[new_root]


class HelpGoodCheckMethods(HelpGoodMethods, HelpNavigateCheckMethods):

    def check_shot_card_good(self, driver, xpath_shot_card_good, data):
        """
        Метод проверяет короткую карточку товара
        :param driver:
        :param xpath_shot_card_good:
        :param data:
        """
        cd_1 = "%s%s | %s | %s | %s" % (data['name'], data['cat_1'], data['cat_2'], data['cat_3'], data['cat_4'])
        cd_2 = '' if data['remains'] is None else "Остаток:%s шт." % data['remains']
        cd_3 = "Мин. заказ:%s шт." % data['min_stock']
        cd_4 = "Цена за штуку:%s руб." % data['price']
        checking_data = cd_1 + cd_2 + cd_3 + cd_4
        shot_card_data = self.get_name(self.get_element_navigate(driver, xpath_shot_card_good))
        cut_shot_card_data = shot_card_data.replace('\n', '')
        msg = "Данные полученные из короткой карточки товара: '%s' не совпадают с введенными: %s"
        self.assertEqual(cut_shot_card_data, checking_data, msg % (cut_shot_card_data, checking_data))

    def check_image_in_card(self, driver, xpath_img_list):
        """
        Метод проверяет фотографии в карточке товара
        :param driver:
        :param img: - список идентификаторов фотографий
        :return:
        """
        for xpath_img in xpath_img_list:
            self.get_element_navigate(driver, xpath_img)

    def check_card_good_require_fields(self, driver, data_good):
        """ Метод проверяет обязательные поля на странице товара.
        Проверяем: минимальное количество товаров, цену, хлебные крошки, имя товара
        :param driver: ссылка на драйвер
        :param data_good: данные товара
        """
        self.get_element_navigate(driver, self.check_good.MIN_STOCK_VALUE % data_good['min_stock'])
        price = self.get_element_navigate(driver, self.check_good.PRICE).text.encode('utf-8').replace(' ', '')
        self.assertIn(data_good['price'], price)
        self.get_element_navigate(driver, self.check_good.BREAD_SPLIT % (data_good['cat_1'], data_good['cat_2']))
        self.get_element_navigate(driver, self.check_good.NAME_GOOD % data_good['name'])

    def check_card_good_text_fields(self, driver, list_text=None):
        """
        Метод проверяет поля на странице товара
        :param driver:
        :param data_good:
        :return:
        """
        if list_text is None:
            list_text = self.LIST_TEXT_INPUT
        self.get_element_navigate(driver, self.check_good.SIZE_PLAIN % list_text['size_plain']['data'])
        self.get_element_navigate(driver, self.check_good.STOCK_SIZE % list_text['stock_size']['data'])
        self.get_element_navigate(driver, self.check_good.BRAND_NAME % list_text['brand_name']['data'])
        self.get_element_navigate(driver, self.check_good.ARTICLE % list_text['article']['data'])
        self.get_element_navigate(driver, self.check_good.DESCRIPTION % list_text['description']['data'])

    def check_card_good_text_fields_positive(self, driver, list_text=None):
        """
        Метод проверяет поля на странице товара для позитивного сценария
        :param driver:
        :param data_good:
        :return:
        """
        err_msg = 'Element present in page'
        no_such_elem = [{'xpath': self.check_good.BRAND_NAME % list_text['brand_name']['data'], 'err_msg': err_msg},
                        {'xpath': self.check_good.ARTICLE % list_text['article']['data'], 'err_msg': err_msg},
                        {'xpath': self.check_good.DESCRIPTION % list_text['description']['data'], 'err_msg': err_msg},
                        {'xpath': self.check_good.SIZE_PLAIN % list_text['size_plain']['data'], 'err_msg': err_msg}]
        if list_text is None:
            list_text = self.LIST_TEXT_INPUT
        self.get_element_navigate(driver, self.check_good.STOCK_SIZE % list_text['stock_size']['data'][1:])
        for elem in no_such_elem:
            self.check_no_such_element(driver, elem)

    def check_name_fields(self, driver):
        """
        Проверка названия полей при создании товара
        :param driver:
        :return:
        """
        for name_field in self.LIST_NAME_FIELDS:
            self.get_element_navigate(driver, self.check_my_goods.ADD_GOOD_NAME_FIELDS % name_field)

    def check_selected_field(self, driver, select_list, xpath_select):
        """
        Проверка значений полей селектов на странице товара
        :param driver:
        :param select_list:
        :return:
        """
        for select in select_list:
            self.get_element_navigate(driver, xpath_select % select)

    def check_breads(self, new_bread, cat_list):
        """
        Проверка изменения хлебных крошек
        :param driver:
        :param old_bread:
        :param new_bread:
        :param cat_list:
        :return:
        """
        try:
            cat_list.remove("Для женщин")
            cat_list.remove("Для мужчин")
        except Exception:
            pass
        self.assertEqual(cat_list[0], new_bread["root_cat"])
        self.assertEqual(cat_list[1], new_bread["cat"])
        self.assertEqual(cat_list[2], new_bread["final_cat"])

    def check_bread_navigate(self, driver, bread_list):
        """

        :param driver:
        :param bread_list:
        :return:
        """
        count_bread = len(bread_list)
        self.check_navigate_in_good_page(driver, self.BREADCRUMBS_SUITE["root_category"],
                                         self.BREADCRUMBS_SUITE["root_category"]["brc_num"])
        self.get_element_navigate(driver, self.check_catalog.ROOT_CATEGORY % bread_list[0])
        driver.back()
        if count_bread == 2:
            self.BREADCRUMB_ABSTRACT["finish_xpath_good"] = self.BREADCRUMB_ABSTRACT["finish_xpath_good"] % bread_list[1]
            self.check_navigate_in_good_page(driver, self.BREADCRUMB_ABSTRACT, 2)
            self.get_element_navigate(driver, self.check_catalog.CATEGORY_ALL % bread_list[1])
        else:
            self.check_navigate_in_good_page(driver, self.BREADCRUMBS_SUITE["category"],
                                         self.BREADCRUMBS_SUITE["category"]["brc_num"])
            self.get_element_navigate(driver, self.check_catalog.CATEGORY % bread_list[1])
            driver.back()
            self.check_navigate_in_good_page(driver, self.BREADCRUMBS_SUITE["final_category"],
                                         self.BREADCRUMBS_SUITE["final_category"]["brc_num"])
            self.get_element_navigate(driver, self.check_catalog.FINAL_CATEGORY_2 % bread_list[2])
            driver.back()

    def check_url_ware(self, ware_id, url):
        """ Сравниваем url страницы товара с той, которая должна быть.
        :param ware_id: идентификатор товара
        :param url: url-страницы сравнения
        """
        link_ware = EVariable.front_base.url.strip() + GoodPage.Path.URL_GOOD % ware_id
        self.assertEqual(link_ware, url)