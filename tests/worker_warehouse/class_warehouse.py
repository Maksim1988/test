# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Файл с классами для работы с тестами для Warehouse worker.
#--------------------------------------------------------------------
import random
import funcy
import funky
from thrift.TSerialization import deserialize, serialize
import time
from gen_py.Common.ttypes import CurrencyAmount
from gen_py.CommonConstants.ttypes import CurrencyType
from gen_py.WareFields.ttypes import WareContentDto, FileIdFieldDto, ScaleFieldDto, MultiTextFieldDto, TextFieldDto, \
    CurrencyFieldDto, MultiEnumFieldDto, EnumFieldDto, IntegerRangeFieldDto, IntegerFieldDto
from gen_py.WarehouseWorker.ttypes import WaresFilterDto, CreateWareRequestDto, UpdateWareRequestDto, \
    ImportWareRequestDto
from gen_py.WarehouseWorkerConstants.ttypes import StockState, ModerationState
from gen_py.WaresIndexWorker.ttypes import WaresSearchResponseDto, SearchRequestDto
from support import service_log
from support.utils.common_utils import instance_to_dict, intersection_lists, run_on_prod, dict_to_json
from support.utils.variables import EVariable
from tests.MainClass import MainClass

__author__ = 's.trubachev'


class WarehouseData(MainClass):

    # данные по товарам, которые необходимо будет восстановить
    SAVED_WARE = None
    SAVED_WARES = None

    TYPES_WARE_CONTENT_DTO = ["ENUM", "TEXT", "SCALE", "INTEGER", "FILE_ID", "MULTI_ENUM", "MULTI_TEXT",
                              "CURRENCY", "RANGE"]

    # Товары с прода для тестирования (продавец Максим Чекмарев):
    prod_ware1 = {"id": "362fea0b27590b0e692753b6dd25767b",
                  "name": "Часы Белые Керамические",
                  "name_seller": "Максим Чекмарев",
                  "store_id": 588}

    # Товары с тестовой среды для тестирования:
    test1_ware1 = {"id": "82abaeedff0571cda9a160116635afee",
                   "name": "For autotests active (НЕ ТРОГАТЬ)",
                   "name_seller": "тестинг",
                   "store_id": 3111}

    test2_ware1 = {"id": "14c34573a77f023b75c3d9c85e5ee265",
                   "name": "Autotest_1422355422",
                   "name_seller": "Тестовый Продавец 76",
                   "store_id": 42}

    prod_env__wares_for_test = [prod_ware1]
    test1_env_wares_for_test = [test1_ware1]
    test2_env_wares_for_test = [test2_ware1]

    static_wares_for_test = {
        "http://www.oorraa.com": prod_env__wares_for_test,
        "http://front1.test.oorraa.net": test1_env_wares_for_test,
        "http://front2.test.oorraa.net": test2_env_wares_for_test}


class WarehouseMethods(WarehouseData):

    @staticmethod
    def get_static_wares():
        """ Получить статичные данные по товарам.
        :return: список данных по товарам
        """
        service_log.put("Get static data for wares.")
        return WarehouseMethods.static_wares_for_test[EVariable.front_base.url.strip()]

    @staticmethod
    def save_ware_data(data):
        """ Сохранить данные товара.
        :param data: данные товара
        :return: True
        """
        WarehouseMethods.SAVED_WARE = data
        service_log.put("Save the data in a single ware.")
        return True

    @staticmethod
    def save_wares_data(data):
        """ Сохранить список данных товаров.
        :param data: данные товаров
        :return: True
        """
        if isinstance(data, list):
            WarehouseMethods.SAVED_WARE = data
            service_log.put("Save the data in a single ware.")
            return True
        else:
            service_log.error("Data is not list.")
            assert AssertionError("Data is not list.")

    @staticmethod
    def recover_ware_data(link_db):
        """ Восстановить данные по товару.
        Сериализуем контент товара, если это необходимо.
        :return: True - в случае успешного обновления, False - в случае если обновление не удалось
        """
        if WarehouseMethods.SAVED_WARE is not None and isinstance(WarehouseMethods.SAVED_WARE, list) is not True:
            service_log.put("Try recover data for ware ID's: %s" % WarehouseMethods.SAVED_WARE["ware_id"])

            # обновляем данные
            ware_data = WarehouseMethods.SAVED_WARE

            # обновляем идентификатор stock_state_id
            link_db.warehouse.update_stack_state_by_ware_id(shop_id=ware_data["shop_id"],
                                                            ware_id=ware_data["ware_id"],
                                                            stack_state=ware_data["stock_state_id"])

            # обновляем идентификатор managed_category_id
            link_db.warehouse.update_category_by_ware_id(shop_id=ware_data["shop_id"],
                                                         ware_id=ware_data["ware_id"],
                                                         category=ware_data["managed_category_id"])

            # обновляем данные контента
            link_db.warehouse.update_content_by_ware_id(shop_id=ware_data["shop_id"],
                                                        ware_id=ware_data["ware_id"],
                                                        content=dict_to_json(ware_data["content"]))

            service_log.put("Recovered data ware.")
            return True
        else:
            service_log.put("Warning! : The variable with the data ware is empty. Recovery data ware - cancelled.")
            return False

    @staticmethod
    def recover_wares_data(link_db):
        """ Восстановить данные по товару.
        Сериализуем контент товара, если это необходимо.
        :return: True - в случае успешного обновления, False - в случае если обновление не удалось
        """
        if isinstance(WarehouseMethods.SAVED_WARE, list) is True:
            service_log.put("The save several value.")
            for index in WarehouseMethods.SAVED_WARE:
                if isinstance(index["content"], dict):
                    # сериализуем контент, если это необходимо
                    content = WarehouseMethods.serialize_content(index["content"])
                    WarehouseMethods.update_data_content(index, content)
                # обновляем данные
                link_db.warehouse.update_ware_by_ware_id(index, index["ware_id"])
                service_log.put("Recovered data ware.")
            return True
        else:
            service_log.put("Warning! : The variable with the data ware is empty. Recovery data ware - cancelled.")
            return False

    @staticmethod
    def save_wares_data(data):
        """ Сохранить данные товаров
        :param data: данные товаров
        :return:
        """
        pass

    @staticmethod
    def recover_wares_data():
        """ Восстановить данные по товарам.
        :return: None
        """
        pass

    @staticmethod
    def deserialize_content(content, flag=False):
        """ Десериализация контента товара из БД Cassandra.
        Десерилизация и приведение объектов к словарю.
        :param content: контент, который необходимо десериализовать
        :return: словарь с данными
        """

        if flag:
            content_dict = instance_to_dict(deserialize(WareContentDto(), content))
        else:
            content_dict = content
        service_log.put("Deserialized content: %s" % str(content_dict))
        return content_dict

    @staticmethod
    def serialize_content(content):
        """ Серилизация контента товара для БД Cassandra.
        :param content: контент, который необходимо сериализовать
        :return: строка
        """
        p = WarehouseMethods.build_dict_for_WareContentDto(content)
        content = WarehouseMethods.get_WareContentDto(**p)
        content_obj = serialize(content)
        service_log.put("Serialized content: %s" % str(content_obj))
        return content_obj

    @staticmethod
    def deserialize_and_update_all_contents(list_with_data):
        """ Десериализация полей 'content' для списка товаров из БД Cassandra.
        Вытаскиваем поле контент, десериализуем его и присваем ему новое значение словаря с данными.
        :param list_with_data: список с данными из БД
        """

        for index in list_with_data:
            index.update({"content": WarehouseMethods.deserialize_content(index['content'])})
        service_log.put("Deserialized and update contents. All data: %s" % str(list_with_data))

    @staticmethod
    def update_data_content(data, content):
        """ Обновить словарь с данными из БД поле 'content' на десериализованные данные.
        :param data: словарь с данными
        :return:
        """

        data.update({"content": content})
        service_log.put("Update content: %s" % str(data))

    @staticmethod
    def get_number_StockState(number, all_item):
        """ Получить номер статуса опубликованности товара.
        :param number: номер статуса
        :param all_item: флаг, взять все значения
        :return: название состояние
        """
        if all_item is True:
            service_log.put("Get StockState number: %s" % StockState._NAMES_TO_VALUES.keys())
            return StockState._NAMES_TO_VALUES.keys()
        else:
            stock_state_number = StockState._NAMES_TO_VALUES[number]
            service_log.put("Get StockState number: %s" % stock_state_number)
            return stock_state_number

    @staticmethod
    def get_name_StockState(name, all_item):
        """ Получить имя статуса опубликованности товара.
        :param name: имя статуса
        :param all_item: флаг, взять все значения
        :return: номер состояния
        """
        if all_item is True:
            service_log.put("Get StockState names: %s" % StockState._VALUES_TO_NAMES.keys())
            return StockState._VALUES_TO_NAMES.keys()
        else:
            stock_type_name = StockState._VALUES_TO_NAMES[name]
            service_log.put("Get StockState name: %s" % stock_type_name)
            return stock_type_name

    @staticmethod
    def get_StockState(data, all_item=False):
        """ Получить статус опубликованности товара.
        :param data: строка или число
        :return: число или строка
        """
        if type(data) == str:
            return WarehouseMethods.get_number_StockState(data, all_item)
        elif type(data) == int:
            return WarehouseMethods.get_name_StockState(data, all_item)

    @staticmethod
    def get_number_CurrencyType(number, all_item):
        """ Получить номер типа валюты товара.
        :param number: номер типа
        :param all_item: флаг, взять все значения
        :return: название состояние
        """
        if all_item is True:
            service_log.put("Get CurrencyType number: %s" % CurrencyType._NAMES_TO_VALUES.keys())
            return CurrencyType._NAMES_TO_VALUES.keys()
        else:
            currency_type_number = CurrencyType._NAMES_TO_VALUES[number]
            service_log.put("Get CurrencyType number: %s" % currency_type_number)
            return currency_type_number

    @staticmethod
    def get_name_CurrencyType(name, all_item):
        """ Получить имя типа валюты товара.
        :param name: имя типа
        :param all_item: флаг, взять все значения
        :return: номер состояния
        """
        if all_item is True:
            service_log.put("Get CurrencyType names: %s" % CurrencyType._VALUES_TO_NAMES.keys())
            return CurrencyType._VALUES_TO_NAMES.keys()
        else:
            currency_type_name = CurrencyType._VALUES_TO_NAMES[name]
            service_log.put("Get CurrencyType name: %s" % currency_type_name)
            return currency_type_name

    @staticmethod
    def get_CurrencyType(data, all_item=False):
        """ Получить тип валюты товара.
        :param data: строка или число
        :return: число или строка
        """
        if type(data) == unicode:
            return WarehouseMethods.get_number_CurrencyType(data, all_item)
        elif type(data) == int:
            return WarehouseMethods.get_name_CurrencyType(data, all_item)

    @staticmethod
    def get_number_ModerationState(number, all_item):
        """ Получить номер статуса состояния модерации товара.
        :param number: номер статуса
        :param all_item: флаг, взять все значения
        :return: название состояние
        """
        if all_item is True:
            service_log.put("Get ModerationState number: %s" % ModerationState._NAMES_TO_VALUES.keys())
            return ModerationState._NAMES_TO_VALUES.keys()
        else:
            moderation_state_number = ModerationState._NAMES_TO_VALUES[number]
            service_log.put("Get ModerationState number: %s" % moderation_state_number)
            return moderation_state_number

    @staticmethod
    def get_name_ModerationState(name, all_item):
        """ Получить имя статуса состояния модерации товара.
        :param name: имя статуса
        :param all_item: флаг, взять все значения
        :return: номер состояния
        """
        if all_item is True:
            service_log.put("Get ModerationState names: %s" % ModerationState._VALUES_TO_NAMES.keys())
            return ModerationState._VALUES_TO_NAMES.keys()
        else:
            moderation_state_name = ModerationState._VALUES_TO_NAMES[name]
            service_log.put("Get ModerationState name: %s" % moderation_state_name)
            return moderation_state_name

    @staticmethod
    def get_ModerationState(data, all_item=False):
        """ Получить статус состояния модерации товара.
        :param data: строка или число
        :return: число или строка
        """
        if type(data) == str:
            return WarehouseMethods.get_number_ModerationState(data, all_item)
        elif type(data) == int:
            return WarehouseMethods.get_name_ModerationState(data, all_item)

    @staticmethod
    def get_IntegerFieldDto(name, value):
        """ Поле товара с целым значением.
        :param name: наименование, тип str
        :param value: значение, тип int
        :return: IntegerFieldDto
        """
        p = IntegerFieldDto(name=name, value=value)
        service_log.put("Get obj IntegerFieldDto: %s" % str(p))
        return p

    @staticmethod
    def get_IntegerRangeFieldDto(dto_name, dto_from, dto_to):
        """ Поле товара со значением в виде целочисленного интервала.
        Нужно гарантировать, что from <= to
        :param dto_name: наименование, тип str
        :param dto_from: начало интервала, тип int
        :param dto_to: конец интервала, тип int
        :return: IntegerRangeFieldDto
        """
        p = IntegerRangeFieldDto(name=dto_name, tfrom=dto_from, to=dto_to)
        service_log.put("Get obj IntegerRangeFieldDto: %s" % str(p))
        return p

    @staticmethod
    def get_EnumFieldDto(name, value):
        """ Поле товара с несколькими значениями из енума.
        :param name: наименование, тип string
        :param values: значение, тип string
        :return: EnumFieldDto
        """
        p = EnumFieldDto(name=name, value=value)
        service_log.put("Get obj EnumFieldDto: %s" % str(p))
        return p

    @staticmethod
    def get_MultiEnumFieldDto(name, value):
        """ Поле товара с несколькими значениями из енума.
        :param name: наименование, тип string
        :param values: значение, тип list<string>
        :return: MultiEnumFieldDto
        """
        p = MultiEnumFieldDto(name=name, values=value)
        service_log.put("Get obj MultiEnumFieldDto: %s" % str(p))
        return p

    @staticmethod
    def get_CurrencyAmount(currency, significand, exponent):
        """ Денежная сумма. В десятичном экспоненциальном формате.
        :param currency: валюта, тип <CommonConstants.CurrencyType>
        :param significand: Мантисса денежной суммы, тип <float>
        :param exponent: Экспонента денежной суммы, тип <int>
        :return: <CurrencyAmount>
        """
        p = CurrencyAmount(currency=currency, significand=significand, exponent=exponent)
        service_log.put("Get obj CurrencyAmount: %s" % str(p))
        return p

    @staticmethod
    def get_CurrencyFieldDto(name, value):
        """ Поле товара со значением валютного типа.
        Дает возможность автоматически конвертировать валюты.
        :param name: наименование
        :param amount: количество, тип <Common.CurrencyAmount> или dict
        :return: CurrencyFieldDto
        """
        p = None
        if isinstance(value, dict):
            p = CurrencyFieldDto(name=name, amount=WarehouseMethods.get_CurrencyAmount(**value))
        else:
            p = CurrencyFieldDto(name=name, amount=value)
        service_log.put("Get obj CurrencyFieldDto: %s" % str(p))
        return p

    @staticmethod
    def get_TextFieldDto(name, value, flag_for_text=True):
        """ Поле товара с текстовым значением.
        :param name: наименование, тип str
        :param value: значение, тип str
        :return: TextFieldDto
        """
        if flag_for_text is True:
            p = TextFieldDto(name, "Autotest_%s" % int(time.time()))
        else:
            p = TextFieldDto(name, str(value))
        service_log.put("Get obj TextFieldDto: %s" % str(p))
        return p

    @staticmethod
    def get_MultiTextFieldDto(name, values):
        """ Поле товара с несколькими текстовыми значениями.
        :param name: название
        :param values: значение
        :return: MultiTextFieldDto
        """
        p = MultiTextFieldDto(name=name, values=values)
        service_log.put("Get obj MultiTextFieldDto: %s" % str(p))
        return p

    @staticmethod
    def get_ScaleFieldDto(name, scale, value):
        """ Поле товара, содержащее значение из какой-то шкалы.
        Доступные шкалы определяются в описании категории.
        Поле товара содержит имя шкалы и значение по этой шкале.
        :param name: наименование, тип str
        :param scale: шкала, тип str
        :param value: значение, тип str
        :return: ScaleFieldDto
        """
        p = ScaleFieldDto(name=name, scale=scale, value=value)
        service_log.put("Get obj ScaleFieldDto: %s" % str(p))
        return p

    @staticmethod
    def get_FileIdFieldDto(name, value):
        """ Поле товара с одним или несколькими файловыми значениями.
        :param name: наименование
        :param values: значения, тип list<str> (см. StaticStorageWorker)
        :return: FileIdFieldDto
        """
        p = FileIdFieldDto(name=name, values=value)
        service_log.put("Get obj FileIdFieldDto: %s" % str(p))
        return p

    @staticmethod
    def get_WaresFilterDto(user_id, stock_states, moderation_states, categories, limit=None, offset=None):
        """ Получить объект WaresFilterDto.
        :param user_id: идентификатор пользователя
        :param stock_states: состояние опубликованность товара
        :param moderation_states: состояние модерации товара
        :param categories: категории
        :param limit: количество
        :param offset: с какого номера будет отсчёт
        :return: объект WaresFilterDto
        """
        p = WaresFilterDto(userId=user_id, allowedStockStates=stock_states, allowedModerationStates=moderation_states,
                           allowedCategories=categories, limit=limit, offset=offset)
        service_log.put("Get obj WaresFilterDto: %s" % str(p))
        return p

    @staticmethod
    def get_WareContentDto(int_fields=None, range_fields=None, enum_fields=None, multi_enum_fields=None,
                           currency_fields=None, text_fields=None, multi_text_fields=None, scale_fields=None,
                           file_fields=None):
        """Контентные поля товара.
        P.S: Должны соответствовать полям, определенным в описании категории товара.

        :param int_fields: Поле товара с целым значением, <IntegerFieldDto>
        :param range_fields: Поле товара со значением в виде целочисленного интервала, <IntegerRangeFieldDto>
        :param enum_fields: Поле товара с несколькими значениями из енума, <EnumFieldDto>
        :param multi_enum_fields: Поле товара с несколькими значениями из енума, <MultiEnumFieldDto>
        :param currency_fields: Поле товара со значением валютного типа, <CurrencyFieldDto>
        :param text_fields: Поле товара с текстовым значением, <TextFieldDto>
        :param multi_text_fields: Поле товара с несколькими текстовыми значениями, <MultiTextFieldDto>
        :param scale_fields: Поле товара, содержащее значение из какой-то шкалы, <ScaleFieldDto>
        :param file_fields: Поле товара с одним или несколькими файловыми значениями, <FileIdFieldDto>
        :return: <WareContentDto>
        """
        p = WareContentDto(integerFields=int_fields,
                           integerRangeFields=range_fields,
                           enumFields=enum_fields,
                           multiEnumFields=multi_enum_fields,
                           currencyFields=currency_fields,
                           textFields=text_fields,
                           multiTextFields=multi_text_fields,
                           scaleFields=scale_fields,
                           fileFields=file_fields)
        service_log.put("Get obj WaresFilterDto: %s" % str(p))
        return p

    @staticmethod
    def get_CreateWareRequestDto(shop_id, category, content, stock_state, ware_import_id):
        """ Получить объект для создания нового товара.
        Запрос на создание товара.
        Нужно указать id магазина, список терминальных категорий и, собственно, контентные поля.
        :param category: категория
        :param content: объект <WareContentDto>
        :param stock_state: идентификатор состояния
        :param ware_import_id: идентификатор импорта (TODO: Deprecate)
        :return: <CreateWareRequestDto>
        """
        p = CreateWareRequestDto(shopId=shop_id, category=category, content=content,
                                 stockState=stock_state, wareImportId=ware_import_id)
        service_log.put("Get obj CreateWareRequestDto: %s" % str(p))
        return p

    @staticmethod
    def get_ImportWareRequestDto(shop_id, category_id, content, ware_import_id, moderator_id, stock_state):
        """ Запрос на импорт премодерированного одного товара.
        Товар проходит базовую валидацию, переводится в указанное состояние и помечается как отмодерированный.
        Warning: ware_import_id - идентификатор импорта, задаётся контент группой по определённыому алгоритма,
            это просто уникальный номер товара, который используется для инвентаризации
            контентщиками (нужен просто уникальный номер). Если номер уже был указа, то товар считается уже добавленным
            ранее и обновляется только его содержание.
        :param shop_id: идентификатор магазина
        :param category_id: идентификатор категории
        :param content: контент, type(WareContentDto)
        :param ware_import_id: идентификатор импорта
        :param moderator_id: идентификатор магазина
        :param stock_state: статус опубликованности товара, type(StockState)
        :return: type(ImportWareRequestDto)
        """
        p = ImportWareRequestDto(shopId=shop_id, category=category_id, content=content, wareImportId=ware_import_id,
                                 moderatorId=moderator_id, wantedStockState=stock_state)
        service_log.put("Get obj ImportWareRequestDto: %s" % str(p))
        return p

    @staticmethod
    def get_SearchRequestDto(pagination=None, ordering=None, search_category=None, management_categories=None,
                             shop_ids=None, search_conditions=None, moderation_states=None, stock_states=None,
                             text_search=None, min_deal_timestamp=None, min_creation_timestamp=None,
                             min_started_deals=None, min_successful_deals=None):
        """
         Получить объект SearchRequestDto.
        :param pagination: Настройки пагинации. Размер страницы, отступ и направление.
        :param ordering: Порядок сортировки. Default - NATURAL, т.е. *без сортировки*.
        :param search_category: Категория каталога. Идентификатор catalogCategory. См. CategoryTreeWorker.
        :param management_categories: Допустимые категории управляющего дерева.
        :param shop_ids: Допустимые магазины.
        :param search_conditions: Дополнительные поисковые условия. См. WareSearchConditionsDto
        :param moderation_states: Допустимые значения ModerationState.
        :param stock_states: Допустимые значения StockState.
        :param text_search: Строка для полнотекстового поиска.
        :param min_deal_timestamp: время сделок
        :param min_creation_timestamp: время создания сделок
        :param min_started_deals: время начала сделок
        :param min_successful_deals: колич.завершенных сделок
        :return: type(SearchRequestDto)
        """
        p = SearchRequestDto(pagination=pagination,
                             ordering=ordering,
                             searchCategory=search_category,
                             allowedManagementCategories=management_categories,
                             allowedShopIds=shop_ids,
                             searchConditions=search_conditions,
                             allowedModerationStates=moderation_states,
                             allowedStockStates=stock_states,
                             textStringSearch=text_search,
                             minimalDealTimestamp=min_deal_timestamp,
                             minimalCreationTimestamp=min_creation_timestamp,
                             minimalStartedDeals=min_started_deals,
                             minimalSuccessfulDeals=min_successful_deals)
        service_log.put("Get obj SearchRequestDto: %s" % str(p))
        return p

    @staticmethod
    def build_dict_for_WareContentDto_old(content):
        """ Делаем сборку всех значения для WareContentDto
        :param content: словарь с контентом
        :return: словарь с объектами.
        """
        # TODO: deprecate
        # Если значение s не None, вызываем метод f с параметроми, иначе оставляем None
        if_none = lambda f, s: dict([(str(i), f(**s[i])) for i in s.keys()]) if s is not None else None

        # TODO: смотри товары с integerRangeFields и currencyFields, нужны ддоп методы

        # составляем словарь с параметрами для WareContentDto
        ware_cont = dict(int_fields=if_none(WarehouseMethods.get_IntegerFieldDto, content["integerFields"]),
                         range_fields=if_none(WarehouseMethods.get_IntegerRangeFieldDto, content["integerRangeFields"]),
                         enum_fields=if_none(WarehouseMethods.get_EnumFieldDto, content["enumFields"]),
                         multi_enum_fields=if_none(WarehouseMethods.get_MultiEnumFieldDto, content["multiEnumFields"]),
                         currency_fields=if_none(WarehouseMethods.get_CurrencyFieldDto, content["currencyFields"]),
                         text_fields=if_none(WarehouseMethods.get_TextFieldDto, content["textFields"]),
                         multi_text_fields=if_none(WarehouseMethods.get_MultiTextFieldDto, content["multiTextFields"]),
                         scale_fields=if_none(WarehouseMethods.get_ScaleFieldDto, content["scaleFields"]),
                         file_fields=if_none(WarehouseMethods.get_FileIdFieldDto, content["fileFields"]))
        return ware_cont

    @staticmethod
    def get_list_content(content, name_type):
        """ Получить список словарей с заданным ключем.
        Ключ - это тип значения для WareContentDto.
        :param content: словарь с контентом
        :param name_type: имя ключа для выборки
        :return: список словарей
        """
        list_content = list()
        for index in content.keys():
            if content[index]["type"] == name_type:
                list_content.append({"name": index, "value": content[index]["value"]})
        return list_content

    @staticmethod
    def get_convert_content_to_inst(funct, list_content):
        """ Конвертировать элемент списка в словарь экземпляров класса.
        :param funct: функция для конвертирования
        :param list_content: список словарей
        :return: словарь с экземпляром класса
        """
        map_content = dict()
        if len(list_content) != 0:
            for index in list_content:
                map_content.update({index["name"]: funct(**index)})
            return map_content
        else:
            return None


    @staticmethod
    def get_convert_content_to_dict(list_content):
        """ Конвертировать элемент списка в словарь.
        :param list_content: список словарей
        :return: словарь с экземпляром класса
        """
        map_content = dict()
        if len(list_content) != 0:
            for index in list_content:
                map_content.update({index["name"]: index})
        return map_content

    @staticmethod
    def get_convert_currency(content):
        """ Преобразуем строковый тип цены в числовой в соответствии с методом get_CurrencyType.
        :param content: контент товара
        :return: обнвленный контент товара
        """
        get_currency_type = WarehouseMethods.get_CurrencyType
        if len(content) != 0:
            for index in content:
                dict_position = content[index]
                if dict_position['type'] == 'CURRENCY':
                    dict_position['value'].update({'currency': get_currency_type(dict_position['value']['currency'])})
            return content
        else:
            return None

    @staticmethod
    def build_dict_for_WareContentDto(content):
        """ Сборка всех значения для WareContentDto в словарь экземпляров.
        Преобразуем в соответствии с тем, в каком виде должны передаваться параметры.
        :param content: словарь с контентом (то как он храниться в БД postgresql)
        :return: словарь с объектами.
        """
        wh = WarehouseMethods
        cont = wh.get_convert_currency(content)

        enum_content = wh.get_convert_content_to_inst(wh.get_EnumFieldDto, wh.get_list_content(cont, "ENUM"))
        text_content = wh.get_convert_content_to_inst(wh.get_TextFieldDto, wh.get_list_content(cont, "TEXT"))
        int_content = wh.get_convert_content_to_inst(wh.get_IntegerFieldDto, wh.get_list_content(cont, "INTEGER"))
        file_content = wh.get_convert_content_to_inst(wh.get_FileIdFieldDto, wh.get_list_content(cont, "FILE_ID"))
        multi_enum_content = wh.get_convert_content_to_inst(wh.get_MultiEnumFieldDto, wh.get_list_content(cont, "MULTI_ENUM"))
        multi_text_content = wh.get_convert_content_to_inst(wh.get_MultiTextFieldDto, wh.get_list_content(cont, "MULTI_TEXT"))
        currency_content = wh.get_convert_content_to_inst(wh.get_CurrencyFieldDto, wh.get_list_content(cont, "CURRENCY"))
        scale_content = wh.get_convert_content_to_inst(wh.get_ScaleFieldDto, wh.get_list_content(cont, "SCALE"))
        int_range_content = wh.get_convert_content_to_inst(wh.get_IntegerRangeFieldDto, wh.get_list_content(cont,"RANGE"))

        # составляем словарь с параметрами для WareContentDto
        ware_cont = dict(int_fields=int_content,
                         range_fields=int_range_content,
                         enum_fields=enum_content,
                         multi_enum_fields=multi_enum_content,
                         currency_fields=currency_content,
                         text_fields=text_content,
                         multi_text_fields=multi_text_content,
                         scale_fields=scale_content,
                         file_fields=file_content)
        return ware_cont

    @staticmethod
    def elem_WareContentDto_to_dict(instance, number_name=1):
        """

        :param instance:
        :param number_name:
        :return:
        """
        data = dict()
        if instance is not None:
            for index in instance.keys():
                if number_name == 1:
                    data.update({index: {"name": instance[index].name, "value": instance[index].value}})
                elif number_name == 2:
                    data.update({index: {"name": instance[index].name, "value": instance[index].values}})
                else:
                    msg = "Not found value number_name."
                    service_log.error(msg)
                    assert AssertionError(msg)
        return data

    @staticmethod
    def convert_WareContentDto_to_dict(content):
        """ Конвертировать словарь экземпляров класса для WareContentDto в словарь.
        :return: словарь с данными
        """
        wh = WarehouseMethods
        fields_currency = wh.elem_WareContentDto_to_dict(content.currencyFields)
        fields_enum = wh.elem_WareContentDto_to_dict(content.enumFields)
        fields_file = wh.elem_WareContentDto_to_dict(content.fileFields, 2)
        fields_integer = wh.elem_WareContentDto_to_dict(content.integerFields)
        fields_integer_range = wh.elem_WareContentDto_to_dict(content.integerRangeFields)
        fields_multi_enum = wh.elem_WareContentDto_to_dict(content.multiEnumFields, 2)
        fields_multi_text = wh.elem_WareContentDto_to_dict(content.multiTextFields)
        fields_scale = wh.elem_WareContentDto_to_dict(content.scaleFields)
        fields_text = wh.elem_WareContentDto_to_dict(content.textFields)

        p = dict(ENUM=fields_enum,
                 CURRENCY=fields_currency,
                 FILE_ID=fields_file,
                 INTEGER=fields_integer,
                 RANGE=fields_integer_range,
                 MULTI_ENUM=fields_multi_enum,
                 MULTI_TEXT=fields_multi_text,
                 SCALE=fields_scale,
                 TEXT=fields_text)
        service_log.put("Convert instance WareContentDto to dict: %s" % str(p))
        return p

    @staticmethod
    def convert_content_list_to_dict(content):
        """

        :param content: контент
        :return:
        """
        convert_cont = dict()
        for name in WarehouseMethods.TYPES_WARE_CONTENT_DTO:
            list_content = WarehouseMethods.get_list_content(content, name)
            dict_cont = WarehouseMethods.get_convert_content_to_dict(list_content)
            convert_cont.update({name: dict_cont})
        return convert_cont

    @staticmethod
    def duplicate_ware_req(shop_id, category, content, stock_state, ware_import_id=None):
        """ Создать запрос на создание тестового товара на основе дубликата.
        :param shop_id: идентификатор магазина
        :param category: категория
        :param content: контент
        :param stock_state: идентификатор состояния
        :param ware_import_id: идентификатор импорта товара (TODO: deprecate)
        :return: запрос, тип <CreateWareRequestDto>
        """

        ware_cont = WarehouseMethods.build_dict_for_WareContentDto(content)
        content = WarehouseMethods.get_WareContentDto(**ware_cont)

        # составляем запрос CreateWareRequestDto
        p = WarehouseMethods.get_CreateWareRequestDto(shop_id, category, content, stock_state, ware_import_id)
        service_log.put("Get obj CreateWareRequestDto: %s" % str(p))
        return p

    @staticmethod
    def duplicate_import_ware_req(shop_id, category, content, moderator_id, stock_state, ware_import_id):
        """ Создать запрос на создание тестового товара на основе дубликата для импорта.
        :param shop_id: идентификатор магазина
        :param category: категория
        :param content: контент
        :return: запрос, тип <CreateWareRequestDto>
        """

        ware_cont = WarehouseMethods.build_dict_for_WareContentDto(content)
        content = WarehouseMethods.get_WareContentDto(**ware_cont)

        # составляем запрос ImportWareRequestDto
        # TODO: WTF ???
        p = WarehouseMethods.get_CreateWareRequestDto(shop_id, category, content, stock_state, ware_import_id)
        p = WarehouseMethods.get_ImportWareRequestDto(shop_id=shop_id, category_id=category, content=content,
                                                      ware_import_id=ware_import_id, moderator_id=moderator_id,
                                                      stock_state=stock_state)
        service_log.put("Get obj ImportWareRequestDto: %s" % str(p))
        return p

    @staticmethod
    def get_UpdateWareRequestDto(ware_id, category, ware_content, expected_revision=0):
        """ Запрос на обновление товара.
        Если какие-либо из остальных полей указаны, их старые значения будут заменены на указанные.
        :param ware_id: идентификатор товара, тип <str>
        :param category: категория товара, тип <int>
        :param ware_content: контент поля товара, тип <WareFields.WareContentDto>
        :param expected_revision:  RESERVED; NOT IMPLEMENTED YET (см. thrift), тип <int>
        :return: UpdateWareRequestDto
        """
        # составляем запрос CreateWareRequestDto
        p = UpdateWareRequestDto(wareId=ware_id, expectedRevision=expected_revision,
                                 newCategory=category, newWareContent=ware_content)
        service_log.put("Get obj UpdateWareRequestDto: %s" % str(p))
        return p

    @staticmethod
    def req_update_ware(ware_id, category, content):
        """ Создать запрос на обновление тестового товара на основе дубликата.
        :param ware_id: идентификатор товара
        :param category: категория
        :param content: контент
        :return: запрос, тип <CreateWareRequestDto>
        """
        # TODO: смотри товары с integerRangeFields и currencyFields, нужны ддоп методы
        ware_cont = WarehouseMethods.build_dict_for_WareContentDto(content)
        content = WarehouseMethods.get_WareContentDto(**ware_cont)

        # составляем запрос CreateWareRequestDto
        p = WarehouseMethods.get_UpdateWareRequestDto(ware_id=ware_id, category=category, ware_content=content,
                                                      expected_revision=0)
        service_log.put("Get obj UpdateWareRequestDto: %s" % str(p))
        return p

    @staticmethod
    def get_random_filtered_values(source, key):
        """ Делаем выборку значений из словаря по ключу.
        Из выборки составляем список уникальных элементов.
        Список может варьироваться от 1 до всех элементов.
        :param source: исходный словарь с данными
        :param key: ключ по которому происходит выборка
        :return: список значений
        """
        elements = list(set(funky.pluck(source, key)))
        p = list(set(map(lambda x: random.choice(elements), range(random.randint(1, len(elements))))))
        service_log.put("Get random values %s form filtered key (%s)" % (str(p), key))
        return p

    @staticmethod
    def select_categories_moderation_stock(wares, ware, flag=True):
        """ Выбираем товары с определёнными статусами.
        :param wares: список товаров
        :param ware: привязка к одному товары
        :param flag: флаг
        :return: set(категории, типы модерации, типы стока)
        """

        # находим категории товаров, состояния модерации, статусов и формируем произвольные наборы этих значений
        wares_categories = WarehouseMethods.get_random_filtered_values(wares, "managed_category")
        wares_moderation_states = WarehouseMethods.get_random_filtered_values(wares, "moderation_state")
        wares_stock_states = WarehouseMethods.get_random_filtered_values(wares, "stock_state")

        if flag is True:
            # для того, что бы нам точно вернулся хотя бы один товар,
            # добавляем его параметры в параметры свойств фильтрации
            wares_categories.append(ware["managed_category"])
            wares_moderation_states.append(ware["moderation_state"])
            wares_stock_states.append(ware["stock_state"])
        # TODO: а если флаг False?
        return wares_categories, wares_moderation_states, wares_stock_states

    @staticmethod
    def chose_ware_ids_with_requirement(wares, categories, moderation, stock):
        """ Делаем пересечение условия для существующих товаров.
        :param wares: список товаров
        :param categories: список категорий
        :param moderation: модерирование
        :param stock: сток
        :return: список товаров с пересечениями
        """
        # делаем пересечение условий
        w_c = [funky.pluck(funcy.where(wares, managed_category=x), 'ware_id') for x in categories]
        w_m = [funky.pluck(funcy.where(wares, moderation_state=x), 'ware_id') for x in moderation]
        w_s = [funky.pluck(funcy.where(wares, stock_state=x), 'ware_id') for x in stock]
        return intersection_lists(w_c + w_m + w_s)

    @staticmethod
    def del_thrift_from_dict(data):
        """ Удаляем ключи-артевакты оставшиеся от thrift,  если таковые есть.
        :param data: словарь с данными
        :return: словарь без артефактов
        """
        return data.pop('textFields') if 'textFields' in data.keys() else data

    @staticmethod
    def get_random_ware(wares, flag_deserialize=False):
        """ Взять произвольный товар из БД.
        Делаем выборку товара из списка и десериализуем контент этого товара.
        :return: товар с данными
        """
        service_log.put("Get random ware and deserialize content.")
        ware = random.choice(wares)
        if flag_deserialize:
            data = WarehouseCheckMethods.deserialize_content(ware['content'])
            WarehouseCheckMethods.update_data_content(ware, data)
        service_log.put("Ware from BD: %s" % ware)
        return ware


class WarehouseCheckMethods(WarehouseMethods):

    def check_dict_or_none(self, p1, p2):
        if isinstance(p1, dict) and isinstance(p2, dict):
            self.assertDictEqual(p1, p2)
        else:
            self.assertIsNone(p1, p2)

    def check_ware_content(self, content_dbase, worker_content):
        """ Проверка контента товара.
        Контент товаря является серриализованным.
        Контент должен быть приведён с типу dict.
        Избавляемся от артефактов трифтового протокола.
        :param content_dbase: контент для сравнения из БД
        :param worker_content: конвертированный контент для сравнения из воркера
        """
        msg_error = "Not equal dicts with type=%s"
        for name in worker_content.keys():
            self.assertDictEqual(worker_content[name], content_dbase[name], msg_error % name)

    def check_ware(self, ware_worker, ware_dbase):
        """ Сравниваем товар от Cassandra и от Warehouse.
        :param ware_worker: товар от воркера Warehouse
        :param ware_dbase:  товар от Cassandra
        """
        service_log.put("Check base information by ware.")

        self.assertEqual(ware_dbase["managed_category_id"], ware_worker.managedCategory)
        self.assertEqual(ware_dbase["revision"], ware_worker.revision)
        self.assertEqual(ware_dbase["shop_id"], ware_worker.shopId)
        self.assertEqual(ware_dbase["stock_state_id"], ware_worker.stockState)
        self.assertEqual(str(ware_dbase["ware_id"]), ware_worker.wareId)
        self.assertEqual(str(ware_dbase["ware_import_id"]), str(ware_worker.wareImportId), "Check import id's.")

        self.check_ware_content(self.convert_content_list_to_dict(ware_dbase["content"]),
                                self.convert_WareContentDto_to_dict(ware_worker.content))

        # TODO: convert
        #self.assertEqual(ware_cassandra["creation_date"], ware_worker.creationTimestamp)
        #self.assertEqual(ware_cassandra["last_modified_date"], ware_worker.lastModifiedTimestamp)
        #self.assertEqual(ware_cassandra["last_published_date"], ware_worker.lastPublishedTimestamp)

        # TODO: в другой таблице
        # self.assertEqual(ware_cassandra["last_moderation_timestamp"], ware_worker.lastModerationTimestamp)
        # self.assertEqual(ware_cassandra["last_moderator_id"], ware_worker.lastModeratorId)
        # self.assertEqual(ware_cassandra["moderation_state"], ware_worker.moderationState)
        # self.assertEqual(str(ware_cassandra["ware_id_salt"]), ware_worker.wareIdSalt)

    def check_wares(self, wares_cassandra, wares_worker):
        """ Сравниваем списки товаров от Cassandra и от Warehouse.
        Сраниваем общее количество товаров.
        Сравниваем каждый товар по отдельности.
        :param wares_cassandra: список с данными от Warehouse
        :param wares_worker:  список с данными от Cassandra
        """
        service_log.put("Check lists from BD and Warehouse.")
        self.assertEqual(len(wares_worker), len(wares_cassandra), "The quantity of the wares does not match.")
        for ware_worker in wares_worker:
            service_log.put("Get ware in list: %s" % str(ware_worker))
            ware_cassandra = funcy.where(wares_cassandra, ware_id=ware_worker.wareId)
            self.assertEqual(len(ware_cassandra), 1, "Found several ware with one id.")
            self.assertNotEqual(len(ware_cassandra), 0, "Not found ware in data from worker Warehouse.")
            self.check_ware(ware_worker, ware_cassandra[0])

    def check_updated_ware(self, ware_service, ware_dbase):
        """ Проверка обновленных данных.
        :param ware_service: исходный товар с которого делалась копия данных
        :param ware_dbase: данные из БД после обновления
        """
        self.assertEqual(ware_dbase["managed_category_id"], ware_service["managed_category_id"], "No equals category.")
        service_log.put("Convert data ware, instance to dict.")
        self.check_ware_content(self.convert_content_list_to_dict(ware_dbase["content"]),
                                self.convert_content_list_to_dict(ware_service["content"]))