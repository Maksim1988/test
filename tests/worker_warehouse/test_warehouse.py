 # -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Файл с классами для работы с Warehouse worker.
#--------------------------------------------------------------------
import random
from unittest import skip, expectedFailure
import funcy
import funky
from ddt import data, ddt
from support import service_log
from support.utils.common_utils import run_on_prod, NoneToInt, unique_number
from support.utils.db import databases
from support.utils.thrift4req import services
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.worker_warehouse.class_warehouse import WarehouseCheckMethods

__author__ = 's.trubachev'


@ddt
class TestGetWaresFromWarehouse(WarehouseCheckMethods):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        service_log.preparing_env(cls)

    @data(*range(3))
    def test_getWare(self, num=0):
        """ Проверка метода getWare.
        Берём из БД Cassandra произвольный товар.
        Берём из воркера Warehouse товар с идентификатором товара от товара взятого из БД.
        Сравниваем эти два товара между собой.
        """
        service_log.run(self)
        wares = databases.db1.warehouse.get_wares_with_limit(100)
        ware_cassandra = self.get_random_ware(wares)

        service_log.put("Get ware, ware_id=%s from Cassandra." % str(ware_cassandra["ware_id"]))
        ware_warehouse = services.warehouse.root.tframed.getWare(ware_cassandra["ware_id"])
        service_log.put("Data ware from worker Warehouse: %s" % str(ware_warehouse))

        #self.check_ware(ware_worker=ware_warehouse, ware_cassandra=ware_cassandra)

    @data(1, random.randint(2, 99), 100)
    def test_getWaresBatch(self, count_wares):
        """ Проверка метода getWaresBatch.
        Берём из БД Cassandra список из нескольких товаров.
        Берём из воркера Warehouse товары с идентификаторами товаров из БД.
        Сравниваем количество товаров общее количество товаров из БД и от воркера.
        Сравниваем товары с одинаковыми идентификаторами из БД и воркера.
        """
        service_log.run(self)

        # делаем выборку товаров из Cassandra
        wares_cassandra = databases.db1.warehouse.get_wares_with_limit(count_wares)
        self.deserialize_and_update_all_contents(wares_cassandra)

        # делаем выборку товаров из воркера
        service_log.put("Get ware, ware_id=%s from Cassandra." % str(funky.pluck(wares_cassandra, "ware_id")))
        wares_warehouse = services.warehouse.root.tframed.getWaresBatch(funky.pluck(wares_cassandra, "ware_id"))
        service_log.put("Data ware from worker Warehouse: %s" % str(wares_warehouse))

        self.check_wares(wares_worker=wares_warehouse, wares_cassandra=wares_cassandra)

    @skip("TODO")
    def test_getWaresFilter_only_user_id(self):
        """ Проверка метода getWaresFilter.
        Выставляем все значения, кроме user_id равными по умолчанию None.
        Warning: на данный момент user_id эквивалентен shop_id
        """
        service_log.run(self)

        #  берём произвольный товар из бд и по его shop_id находим остальные товары продавца
        wares = databases.db1.warehouse.get_wares_with_limit(100)
        ware_cassandra = self.get_random_ware(wares)
        wares_cassandra = databases.db1.warehouse.get_wares_by_shop_id(shop_id=ware_cassandra['shop_id'])
        self.deserialize_and_update_all_contents(wares_cassandra)

        # по user_id - находим все товары, т.к. None - должен выключать фильтр
        wares_filter_dto = self.get_WaresFilterDto(user_id=ware_cassandra['shop_id'],
                                                   categories=None, moderation_states=None, stock_states=None,
                                                   limit=None, offset=None)
        # делаем выборку товаров из воркера
        wares_warehouse = services.warehouse.root.tframed.getWaresFilter(wares_filter_dto)
        service_log.put("Response wares from worker: %s" % str(wares_warehouse))
        self.check_wares(wares_cassandra=wares_cassandra, wares_worker=wares_warehouse)

    @skip("TODO")
    def test_countWaresFilter_only_user_id(self):
        """ Проверка метода countWaresFilter.
        Выставляем все значения, кроме user_id равными по умолчанию None.
        Warning: на данный момент user_id эквивалентен shop_id
        """
        service_log.run(self)

        #  берём произвольный товар из бд и по его shop_id находим остальные товары продавца
        wares = databases.db1.warehouse.get_wares_with_limit(100)
        ware_cassandra = self.get_random_ware(wares)
        wares_cassandra = databases.db1.warehouse.get_wares_by_shop_id(shop_id=ware_cassandra['shop_id'])

        #  по user_id - находим все товары, т.к. None - должен выключать фильтр
        wares_filter_dto = self.get_WaresFilterDto(user_id=ware_cassandra['shop_id'],
                                                   categories=None, moderation_states=None, stock_states=None,
                                                   limit=None, offset=None)
        # делаем выборку количества товаров воркера
        count_wares_warehouse = services.warehouse.root.tframed.countWaresFilter(wares_filter_dto)
        service_log.put("Response wares from worker: %s" % str(count_wares_warehouse))
        self.assertEqual(len(wares_cassandra), count_wares_warehouse, "The quantity of the wares does not match.")

    @skip("in_develop")
    def test_getWaresFilter_categories_and_states(self):
        """

        :return:
        """
        # TODO: лажает
        #  берём произвольный товар из бд и по его shop_id находим остальные товары продавца
        wares = databases.db1.warehouse.get_wares_with_limit(100)
        ware_cassandra = self.get_random_ware(wares)
        wares_cassandra = databases.db1.warehouse.get_wares_by_shop_id(shop_id=ware_cassandra['shop_id'])
        self.deserialize_and_update_all_contents(wares_cassandra)

        categories, moderation, stock = self.select_categories_moderation_stock(wares_cassandra, ware_cassandra)
        filtered_wares_cassandra = self.chose_ware_ids_with_requirement(wares_cassandra, categories, moderation, stock)

        # по user_id - находим все товары, т.к. None - должен выключать фильтр
        wares_filter_dto = self.get_WaresFilterDto(user_id=ware_cassandra['shop_id'],
                                                   categories=categories,
                                                   moderation_states=moderation,
                                                   stock_states=stock,
                                                   limit=None, offset=None)

        # делаем выборку товаров из воркера
        wares_warehouse = services.warehouse.root.tframed.getWaresFilter(wares_filter_dto)
        service_log.put("Response wares from worker: %s" % str(wares_warehouse))

        self.check_wares(wares_cassandra=filtered_wares_cassandra, wares_worker=wares_warehouse)

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        service_log.end()


@ddt
class TestEditCreateWareFromWarehouse(WarehouseCheckMethods):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        #  берём произвольный товар из бд, и смотрим его shop_id и категорию (что бы взять существующие данные)
        cls.wares = databases.db1.warehouse.get_wares_with_limit(100)
        cls.ware1 = cls.get_random_ware(cls.wares)
        service_log.preparing_env(cls)

    @run_on_prod(False)
    @data(*range(0, 10))
    def test_createWare(self, n=1):
        """ Создание товара.
        Создаём дубликат существующего товара.
        Сравниваем значения от сервиса со значениями из БД.
        """
        service_log.run(self)

        # создаём товар
        ware_req = self.duplicate_ware_req(shop_id=self.ware1['shop_id'],
                                           category=self.ware1['managed_category_id'],
                                           content=self.ware1["content"],
                                           stock_state=self.ware1['stock_state_id'])


        wares_warehouse = services.warehouse.root.tframed.createWare(ware_req)
        service_log.put("Created ware: %s" % wares_warehouse)

        # Возьмём значение из БД только что созданного товара по его идентификатору
        ware_cassandra = databases.db1.warehouse.get_wares_by_ware_id(wares_warehouse.wareId)
        service_log.put("Ware from BD: %s" % ware_cassandra)

        # проверяем, что вернулось только один товар
        self.assertEqual(len(ware_cassandra), 1, "Found more than one item.")
        ware_cassandra = ware_cassandra[0]

        self.update_data_content(ware_cassandra, self.deserialize_content(ware_cassandra['content']))

        #  проверяем полученно значение от сервиса со значениями из БД
        self.check_ware(ware_worker=wares_warehouse, ware_dbase=ware_cassandra)

    @run_on_prod(False)
    @data(*range(0, 5))
    def test_updateWare(self, n=0):
        """ Обновление данных товара.
        Берём два товара. Подменяем в товаре №1 значения от товара №2
        Обновляем данные через сервис.
        Проверяем данные вернувшиеся значения от сервиса со значениями, которые записались в БД.
        Проверяем, что значения от товара № 2 добавились в товар № 1
        Восстанавливаем данные товара № 1 на первоночальные.
        """
        service_log.run(self)

        # сохраняем данные по товару № 1
        self.save_ware_data(self.ware1)
        service_log.put("Save the data in a single product.")

        # берём произвольно товар № 2
        self.ware2 = random.choice(self.wares)
        #self.update_data_content(self.ware2, self.ware2['content']) # ?????????????
        service_log.put("Ware2: %s" % self.ware2)

        # Создаём запрос для обновления товара №1 значениями от товара № 2. Отправляем его на сервис.
        ware_req = self.req_update_ware(self.ware1["ware_id"], self.ware2['managed_category_id'], self.ware2["content"])

        # название товара должно совпадать, восстанавливаем его до товара № 2
        ware_req.newWareContent.textFields[u'title'].value = self.ware2['content'][u'title'][u'value']

        wares_warehouse = services.warehouse.root.tframed.updateWare(ware_req)
        service_log.put("Updated ware: %s" % str(wares_warehouse))

        # Возьмём значение из БД только что обновлённого товара №1 по его идентификатору
        ware_postgresql = databases.db1.warehouse.get_wares_by_ware_id(wares_warehouse.wareId)
        service_log.put("Ware from BD: %s" % ware_postgresql)

        # проверяем, что вернулось только один товар
        self.assertEqual(len(ware_postgresql), 1, "Found more than one item.")
        ware_postgresql = ware_postgresql[0]

        #self.update_data_content(ware_cassandra, self.deserialize_content(ware_cassandra['content'])) # ?????

        # проверяем, что идентификаторы товара остались прежними
        self.assertEqual(wares_warehouse.wareId, self.ware1["ware_id"], "Do not match the identifiers of the ware.")

        #  проверяем полученное значение от сервиса со значениями из БД
        self.check_ware(wares_warehouse, ware_postgresql)

        #  проверяем первоночальные значения товара №2 с обновленными значениями товара № 1 - должны быть идентичны
        self.check_updated_ware(ware_service=self.ware2, ware_dbase=ware_postgresql)

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        cls.recover_ware_data(databases.db1)
        service_log.end()


@ddt
class TestModerationWareFromWarehouse(WarehouseCheckMethods):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        #  берём произвольный товар из бд, и смотрим его shop_id и категорию (что бы взять существующие данные)
        wares = databases.db1.warehouse.get_wares_with_limit(100)
        cls.ware = cls.get_random_ware(wares)
        cls.moderator_id = int(AccountingMethods.get_default_user_id('moderator'))
        service_log.preparing_env(cls)

    @run_on_prod(False)
    @skip("TODO")
    def test_makeModeration_new_ware_accepted(self):
        """ Проверяем метод для модерации товара.
        Создаём товар. Проверяем его статус - BELIEVED.
        Отсылаем запрос на перевод его в другой статус.
        Проверяем, что статус изменился на ACCEPTED.
        """
        service_log.run(self)
        # создаём товар
        ware_req = self.duplicate_ware_req(self.ware['shop_id'], self.ware['managed_category_id'],
                                           self.ware["content"], self.ware['stock_state_id'])

        ware_warehouse = services.warehouse.root.tframed.createWare(ware_req)
        service_log.put("Created ware: %s" % ware_warehouse)
        # Возьмём значение из БД только что созданного товара №1 по его идентификатору
        ware_believed_dbase = databases.db1.warehouse.get_wares_by_ware_id(ware_warehouse.wareId)
        service_log.put("Ware created from BD: %s" % ware_believed_dbase)
        # Проверяем, что статус товара - BELIEVED.
        self.assertEqual(ware_believed_dbase[0]['moderation_state_id'], 1, "Ware moderation status not BELIEVED.")
        # Меняем статус
        ware_warehouse = services.warehouse.root.tframed.makeModeration(ware_warehouse.wareId, True, self.moderator_id)
        # Возьмём значение из БД только что созданного товара №1 по его идентификатору
        ware_accepted_warehouse = databases.db1.warehouse.get_wares_by_ware_id(ware_warehouse.wareId)
        service_log.put("Ware created from BD: %s" % ware_accepted_warehouse)
        # Проверяем, что статус изменился на ACCEPTED.
        self.assertEqual(ware_accepted_warehouse[0]['moderation_state'], 2, "Ware moderation status not ACCEPTED by BD")
        self.assertEqual(ware_warehouse.moderationState, 2, "Ware moderation status not ACCEPTED by service")

    @run_on_prod(False)
    def test_makePublication_published(self):
        """ Опубликовать товар.
        Создаём товар. Проверяем, что по умолчанию статус опубликованности HIDDEN.
        Изменяем его статус. Проверяем, что по умолчанию статус опубликованности PUBLISHED.
        """
        service_log.run(self)
        # создаём товар
        ware_req = self.duplicate_ware_req(self.ware['shop_id'], self.ware['managed_category_id'],
                                           self.ware["content"], self.ware["stock_state_id"])

        ware_warehouse = services.warehouse.root.tframed.createWare(ware_req)
        service_log.put("Created ware: %s" % ware_warehouse)

        # выставляем состояние StockState Опубликованный товар. Доступен всем. Индексируется. PUBLISHED = 2
        msg_published = "Stock state not equal PUBLISHED. Data from service."
        msg_published_db = "Stock state not equal PUBLISHED. Data from DB."
        stock_state = self.get_StockState('PUBLISHED')
        wh_ware_published = services.warehouse.root.tframed.makePublication(ware_warehouse.wareId, stock_state)
        self.assertEqual(wh_ware_published.stockState, stock_state, msg_published)
        ware_after_changed = databases.db1.warehouse.get_wares_by_ware_id(ware_warehouse.wareId)[0]
        self.assertEqual(ware_after_changed["stock_state_id"], stock_state, msg_published_db)

    @run_on_prod(False)
    def test_makePublication_hidden(self):
        """ Опубликовать товар.
        Создаём товар. Проверяем, что по умолчанию статус опубликованности HIDDEN.
        Изменяем его статус. Проверяем, что по умолчанию статус опубликованности PUBLISHED.
        Снова изменяем его статус. Проверяем, что по умолчанию статус опубликованности HIDDEN.
        """
        service_log.run(self)
        msg_published = "Stock state not equal %s. Data from service."
        msg_published_db = "Stock state not equal %s. Data from DB."

        # создаём товар
        name_stock_state = 'HIDDEN'
        ware_req = self.duplicate_ware_req(self.ware['shop_id'],
                                           self.ware['managed_category_id'],
                                           self.ware["content"],
                                           self.ware["stock_state_id"])

        ware_warehouse = services.warehouse.root.tframed.createWare(ware_req)
        service_log.put("Created ware: %s" % ware_warehouse)

        # Проверяем, что StockState у созданного товара HIDDEN = 3 (по умолчанию)
        self.assertEqual(ware_warehouse.stockState, 3, msg_published % name_stock_state)
        ware_after_created = databases.db1.warehouse.get_wares_by_ware_id(ware_warehouse.wareId)[0]
        self.assertEqual(ware_after_created["stock_state_id"], 3, msg_published_db % name_stock_state)

        # выставляем состояние StockState Опубликованный товар. Доступен всем. Индексируется. PUBLISHED = 2
        name_stock_state = 'PUBLISHED'
        stock_state = self.get_StockState(name_stock_state)
        wh_ware_published = services.warehouse.root.tframed.makePublication(ware_warehouse.wareId, stock_state)
        self.assertEqual(wh_ware_published.stockState, stock_state, msg_published % name_stock_state)
        ware_after_changed = databases.db1.warehouse.get_wares_by_ware_id(ware_warehouse.wareId)[0]
        self.assertEqual(ware_after_changed["stock_state_id"], stock_state, msg_published_db % name_stock_state)

        # выставляем состояние StockState Опубликованный товар. Доступен всем. Индексируется. HIDDEN = 3
        name_stock_state = 'HIDDEN'
        stock_state = self.get_StockState(name_stock_state)
        wh_ware_published = services.warehouse.root.tframed.makePublication(ware_warehouse.wareId, stock_state)
        self.assertEqual(wh_ware_published.stockState, stock_state, msg_published % name_stock_state)
        ware_after_changed = databases.db1.warehouse.get_wares_by_ware_id(ware_warehouse.wareId)[0]
        self.assertEqual(ware_after_changed["stock_state_id"], stock_state, msg_published_db % name_stock_state)

    @run_on_prod(False)
    def test_makePublication_nothing(self):
        """ Опубликовать товар.
        Создаём товар. Проверяем, что по умолчанию статус опубликованности HIDDEN.
        Изменяем его статус. Проверяем, что по умолчанию статус опубликованности PUBLISHED.
        Снова изменяем его статус. Проверяем, что по умолчанию статус опубликованности HIDDEN.
        """
        service_log.run(self)
        msg_published = "Stock state not equal %s. Data from service."
        msg_published_db = "Stock state not equal %s. Data from DB."

        # создаём товар
        name_stock_state = 'HIDDEN'
        ware_req = self.duplicate_ware_req(self.ware['shop_id'], self.ware['managed_category_id'],
                                           self.ware["content"], self.ware["stock_state_id"])

        ware_warehouse = services.warehouse.root.tframed.createWare(ware_req)
        service_log.put("Created ware: %s" % ware_warehouse)
        self.assertEqual(ware_warehouse.stockState, 3, msg_published % name_stock_state)
        ware_after_created = databases.db1.warehouse.get_wares_by_ware_id(ware_warehouse.wareId)[0]
        self.assertEqual(ware_after_created["stock_state_id"], 3, msg_published_db % name_stock_state)

        # выставляем состояние StockState Опубликованный товар. Доступен всем. Индексируется. HIDDEN = 3
        stock_state = self.get_StockState(name_stock_state)
        wh_ware_published = services.warehouse.root.tframed.makePublication(ware_warehouse.wareId, stock_state)
        self.assertEqual(wh_ware_published.stockState, stock_state, msg_published % name_stock_state)
        ware_after_changed = databases.db1.warehouse.get_wares_by_ware_id(ware_warehouse.wareId)[0]
        self.assertEqual(ware_after_changed["stock_state_id"], stock_state, msg_published_db % name_stock_state)

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        service_log.end()


class TestDealWareFromWarehouse(WarehouseCheckMethods):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        #  берём произвольный товар из бд, и смотрим его shop_id и категорию (что бы взять существующие данные)
        wares = databases.db1.warehouse.get_wares_with_limit(100)
        cls.ware = cls.get_random_ware(wares)
        service_log.preparing_env(cls)

    @run_on_prod(False)
    @skip("Deprecate")
    def test_registerNewDeal(self):
        """ Проверка счетчика новых сделок по указанному товару.
        Берём произвольный товар. Запоминаем текущее состояние количества сделок.
        Регистрируем новыую сделку. Сверяем, что счетчик изменился.
        P.S: Сортировка идеёт сначало по SuccessfulDeal, затем по registerNewDeal
            - на основании этого высчитывается популярный товар.
        """
        # TODO: метод могут выпилить
        ware_deal = services.warehouse.root.tframed.registerNewDeal(self.ware["ware_id"])
        ware_new_deal = databases.db1.warehouse.get_wares_by_ware_id(self.ware["ware_id"])[0]
        msg = "Value started_deals_count is not more after changed."
        self.assertEqual(ware_new_deal['started_deals_count'], NoneToInt(self.ware['started_deals_count'])+1, msg)
        self.assertEqual(ware_new_deal['started_deals_count'], ware_deal.startedDealsCount, msg)

    @run_on_prod(False)
    @skip("Deprecate")
    def test_registerSuccessfulDeal(self):
        """ Проверка счетчика завершенных[ сделок по указанному товару.
        Берём произвольный товар. Запоминаем текущее состояние количества сделок.
        Регистрируем завершенную сделку. Сверяем, что счетчик изменился.
        P.S: Сортировка идеёт сначало по SuccessfulDeal, затем по registerNewDeal
            - на основании этого высчитывается популярный товар.
        """
        # TODO: метод могут выпилить
        ware_deal = services.warehouse.root.tframed.registerSuccessfulDeal(self.ware["ware_id"])
        ware_suc_deal = databases.db1.warehouse.get_wares_by_ware_id(self.ware["ware_id"])[0]
        msg = "Value successful_deals_count is not more after changed."
        self.assertEqual(ware_suc_deal['successful_deals_count'], NoneToInt(self.ware['successful_deals_count'])+1, msg)
        self.assertEqual(ware_suc_deal['successful_deals_count'], ware_deal.successfulDealsCount, msg)

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        service_log.end()


class TestImportWareFromWarehouse(WarehouseCheckMethods, AccountingMethods):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        #  берём произвольный товар из бд, и смотрим его shop_id и категорию (что бы взять существующие данные)
        cls.wares = databases.db1.warehouse.get_wares_with_limit(100)
        cls.ware1 = cls.get_random_ware(cls.wares)
        service_log.preparing_env(cls)

    @run_on_prod(False)
    @expectedFailure
    def test_new_importWare(self):
        """ Импорт премодерированного товара
        Товар проходит базовую валидацию, переводится в указанное состояние
        и помечается как отмодерированный.
        """
        # TODO: Ошибка "https://jira.oorraa.net/browse/RT-290"
        service_log.run(self)

        # импортируем новый товар
        ware_req = self.duplicate_import_ware_req(shop_id=self.ware1['shop_id'],
                                                  category=self.ware1['managed_category'],
                                                  content=self.ware1["content"],
                                                  moderator_id=int(self.get_default_user_id("moderator")),
                                                  stock_state=self.get_StockState("PUBLISHED"),
                                                  ware_import_id=str(unique_number()))
        wares_warehouse = services.warehouse.root.tframed.importWare(ware_req)
        service_log.put("Import ware: %s" % wares_warehouse)

        # Возьмём значение из БД только что импортированного товара по его идентификатору
        ware_cassandra = databases.db1.warehouse.get_wares_by_ware_id(wares_warehouse.wareId)
        service_log.put("Ware from BD: %s" % ware_cassandra)

        # проверяем, что вернулось только один товар
        self.assertEqual(len(ware_cassandra), 1, "Found more than one item.")
        ware_cassandra = ware_cassandra[0]

        self.update_data_content(ware_cassandra, self.deserialize_content(ware_cassandra['content']))

        #  проверяем полученно значение от сервиса со значениями из БД
        self.check_ware(ware_worker=wares_warehouse, ware_dbase=ware_cassandra)

    @run_on_prod(False)
    def test_old_importWare(self):
        # TODO: тест на уже существующий товар
        pass

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        service_log.end()


@ddt
class TestUpdateAndCreateWaresFromWarehouse(WarehouseCheckMethods):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        cls.count_wares = 3  # количество товаров

        #  берём произвольный товар из бд, и смотрим его shop_id и категорию (что бы взять существующие данные)
        cls.wares = databases.db1.warehouse.get_wares_with_limit(100)
        cls.list_wares = list()
        for index in range(cls.count_wares):
            cls.list_wares.append(cls.get_random_ware(cls.wares))
        service_log.preparing_env(cls)

    @run_on_prod(False)
    def test_createWares(self):
        """ Создание нескольких товаров.
        Создаём дубликаты из существующих товаров.
        Сравниваем значения от сервиса со значениями из БД.
        """
        service_log.run(self)

        # создаём данные для товары
        wares_req = list()
        for ware in self.list_wares:
            duplicate_ware = self.duplicate_ware_req(shop_id=ware['shop_id'],
                                                     category=ware['managed_category_id'],
                                                     content=ware["content"],
                                                     stock_state=ware['stock_state_id'],
                                                     ware_import_id=None)  # TODO: ware_import_id - deprecate 22.06.15
            wares_req.append(duplicate_ware)

        # создаём несколько товаров
        wares_warehouse = services.warehouse.root.tframed.createWares(wares_req)
        service_log.put("Created wares: %s" % wares_warehouse)

        for ware in wares_warehouse:
            # Возьмём значение из БД только что созданного товара по его идентификатору
            ware_cassandra = databases.db1.warehouse.get_wares_by_ware_id(ware.wareId)
            service_log.put("Ware from BD: %s" % ware_cassandra)

            # проверяем, что вернулось только один товар
            self.assertEqual(len(ware_cassandra), 1, "Found more than one item.")
            ware_cassandra = ware_cassandra[0]
            # десериализуем и обновляем контент
            self.update_data_content(ware_cassandra, self.deserialize_content(ware_cassandra['content']))
            #  проверяем полученно значение от сервиса со значениями из БД
            self.check_ware(ware_worker=ware, ware_dbase=ware_cassandra)

    @run_on_prod(False)
    def test_updateWares(self):
        """ Импорт премодерированного товара
        Товар проходит базовую валидацию, переводится в указанное состояние
        и помечается как отмодерированный.
        """
        service_log.run(self)

        # сохраняем первоночальные данные по товарам
        self.save_wares_data(self.list_wares)
        service_log.put("Save the data in a several product.")

        # берём произвольно товары № 2

        self.list_wares2 = list()
        for index in range(self.count_wares):
            self.list_wares2.append(self.get_random_ware(self.wares))
        service_log.put("Get list2 with Ware: %s" % self.list_wares2)

        # Создаём запрос для обновления товара №1 значениями от товара № 2. Отправляем его на сервис.
        wares_req = list()
        for num, index in enumerate(self.list_wares2):
            ware1 = self.list_wares[num]
            wares_req.append(self.req_update_ware(ware1["ware_id"], index['managed_category_id'], index["content"]))
        wares_warehouse = services.warehouse.root.tframed.updateWares(wares_req)
        service_log.put("Updated wares: %s" % str(wares_warehouse))

        for ware in wares_warehouse:
            # Возьмём значение из БД только что обновлённого товара №1 по его идентификатору
            ware_cassandra = databases.db1.warehouse.get_wares_by_ware_id(ware.wareId)
            service_log.put("Ware from BD: %s" % ware_cassandra)

            # проверяем, что вернулось только один товар
            self.assertEqual(len(ware_cassandra), 1, "Found more than one item.")
            ware_cassandra = ware_cassandra[0]
            # десериализуем и обновляем контент
            self.update_data_content(ware_cassandra, self.deserialize_content(ware_cassandra['content']))

            # проверяем, что идентификаторы товара остались прежними
            ware_in_list_wares = funcy.where(self.list_wares, ware_id=ware.wareId)[0]
            self.assertEqual(ware.wareId, ware_in_list_wares["ware_id"], "Do not match the identifiers of the ware.")

            #  проверяем полученное значение от сервиса со значениями из БД
            self.check_ware(ware_worker=ware, ware_dbase=ware_cassandra)

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        cls.recover_wares_data()
        service_log.end()