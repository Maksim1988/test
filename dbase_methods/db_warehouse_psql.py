# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# После перезда воркера Warehouse с Cassandra на PostgreSQL
# методы взаимодействия с БД перехали из "db_warehouse" в "db_warehouse_psql".
# ------------------------------------------------------------------------------

from support.utils.common_utils import run_on_prod
from support.utils.db_postgresql import execute_sql, ClassSaveLinkPostgreSQL

__author__ = 's.trubachev'


class ClassWarehouseData(ClassSaveLinkPostgreSQL):

    PRIMARY_KEYS = ["shop_id", "ware_id"]

    def delete_primary_keys_from_dict(self, data):
        """ Удаляем ключи из данных, индексы которых не должны быть нарушены.
        :param data: словарь с данными
        :return: словарь с данными без первичных ключей
        """
        for index in self.PRIMARY_KEYS:
            try:
                data.pop(index)
            except KeyError:
                pass
        return data


class ClassGetWarehouseSql(ClassWarehouseData):

    @execute_sql
    def get_wares(self):
        """ Взять все товары.
        WARNING: товаров может быть очень много.
        :return: список с данными по товарам
        """
        return """select * from warehouse.wares;"""

    @execute_sql
    def get_wares_with_limit(self, limit=10):
        """ Взять несколько товаров.
        :param limit: количество товаров в зпросе
        :return: список с данными по товарам
        """
        return """select * from warehouse.wares limit %s;""" % limit

    @execute_sql
    def get_wares_by_shop_id(self, shop_id):
        """ Взять несколько товаров по идентификатору магазина.
        :param shop_id: идентификатор магазина
        :return: список с данными по товарам
        """
        return """select * from warehouse.wares where shop_id=%s;""" % shop_id

    @execute_sql
    def get_wares_by_ware_id(self, ware_id):
        """ Взять товар по идентификатору товара.
        :param ware_id: идентификатор товара
        :return: список с данными по товару
        """
        return """select * from warehouse.wares where ware_id = '%s';""" % ware_id

    @execute_sql
    def get_moderation_by_ware_id(self, index_id):
        """ Взять состояние модерации товара по порядковому идентификатору.
        :param index_id: порядковый идентификатор товара
        :return: список с данными по товару
        """
        return """select * from warehouse.o_moderation where ware_id = '%s';""" % index_id

    @execute_sql
    def get_wares_by_ware_ids(self, ware_ids):
        """ Взять товары по идентификаторам товаров.
        :param ware_id: строка идентификаторов товаров через запятую
        :return: список с данными по товарам
        """
        return """select * from warehouse.wares where ware_id in (%s) ALLOW FILTERING;""" % ware_ids

    @execute_sql
    def get_moderation_state_by_ware_id(self, ware_id):
        """
        Получить данные о модерации товара
        :param ware_id:
        :return:
        """
        return """SELECT * FROM warehouse.o_moderation WHERE ware_id = %s""" % ware_id

    @execute_sql
    def get_ware_with_photo(self, count):
        """
        Получить товар с заданным количеством фотографий
        :param count: количество фото
        :return: товары
        """
        return """SELECT * FROM warehouse.wares WHERE json_array_length(content->'pictures'->'value') = %s""" % count

    @execute_sql
    def get_id_stock_state_by_name(self, name):
        """
        Получить идентификатор состояния товара на сатйе(опубликован,скрыт и.т.д) по названию состояния
        :param name: название stock_state
        :return: id
        """
        return """SELECT id FROM d_stock_state WHERE name='%s'""" % name

    @execute_sql
    def get_wares_by_criteria(self, criteria):
        """
        Получить товары по заданным критериям
        :param criteria:
        :return: товары
        """
        return """SELECT * FROM warehouse.wares WHERE %s""" % criteria

    @execute_sql
    def get_wares_by_id_and_moderation_state(self, ids, m_status):
        """
        Получить товары по идентификатору и статусу модерации
        :param ids: id товаров
        :param m_status: татус модерации
        :return:
        """
        return """SELECT ww.*, wom.moderation_state_id FROM warehouse.wares AS ww
        LEFT JOIN warehouse.o_moderation AS wom
        ON ww.id = wom.ware_id
        WHERE ww.ware_id in (%s) and wom.moderation_state_id in (%s)""" % (ids, m_status)

    @execute_sql
    def get_wares_by_criteria_and_moderation_state(self, m_status, criteria):
        """
        Получить товары по идентификатору и статусу модерации
        :param ids: id товаров
        :param m_status: татус модерации
        :return:
        """
        p = "SELECT ww.*, wom.moderation_state_id FROM warehouse.wares AS ww " \
            "LEFT JOIN warehouse.o_moderation AS wom ON ww.id = wom.ware_id " \
            "WHERE wom.moderation_state_id in (%s) and %s" % (m_status, criteria)
        return p

    @execute_sql
    def get_count_wares(self):
        '''
        Получить общее кол-во товаров из базы
        :return: количество товаров, int
        '''
        return """select count(*) from warehouse.wares"""


class ClassUpdateWarehouseSql(ClassWarehouseData):

    #@run_on_prod(False)
    #def update_ware_by_ware_id(self, criteria, ware_id):
    #    """ Обновить существующий товар по заданному критерию.
    #    Запоминаем первичный ключ shop_id, т.к. мы его потом удалим.
    #    Удаляем первичные ключи, т.к. их по ним строится индекс и они не изменяются.
    #    Формируем CQL-запрос с условием из первичных и с данными без онных.
    #    :param criteria: строка критерии обновления, type=dict
    #    :param ware_id: идентификатор товара, type=str
    #    :return: cql-запрос, список с данными, type=tuple
    #    """
    #
    #    #  подготовка данных
    #    shop_id = criteria["shop_id"]
    #    ware_id = criteria["ware_id"]
    #    criteria = self.delete_primary_keys_from_dict(criteria)
    #    format_cql = ", ".join([str(index) + " = ?" for index in criteria.keys()])
    #
    #    # формируем запрос без значений
    #    query = """UPDATE warehouse.wares SET content='%s' WHERE ware_id='%s' AND shop_id=%s;""" % (ware_id, shop_id)
    #
    #    # формируем значения для биндинга в запрос
    #    params_for_query = criteria.values() + [ware_id, shop_id]
    #    return query, params_for_query

    @execute_sql
    @run_on_prod(False)
    def update_content_by_ware_id(self, shop_id, ware_id, content):
        """ Обновить контент товара.
        :param content: контент товара, type=str
        :param ware_id: идентификатор товара, type=str
        :param shop_id: идентификатор магазина, type=str
        :return: sql-запрос
        """

        # формируем запрос без значений
        query = """UPDATE warehouse.wares SET content='%s' WHERE ware_id='%s' AND shop_id=%s;""" % (content, ware_id,
                                                                                                    shop_id)
        return query

    @execute_sql
    @run_on_prod(False)
    def update_stack_state_by_ware_id(self, shop_id, ware_id, stack_state):
        """ Обновить stack_state товара.
        :param stack_state: идентификатор stack_state
        :param ware_id: идентификатор товара, type=str
        :param shop_id: идентификатор магазина, type=str
        :return: sql-запрос
        """

        # формируем запрос без значений
        query = """UPDATE warehouse.wares SET stock_state_id=%s WHERE ware_id='%s' AND shop_id=%s;""" % (stack_state,
                                                                                                         ware_id,
                                                                                                         shop_id)
        return query

    @execute_sql
    @run_on_prod(False)
    def update_category_by_ware_id(self, shop_id, ware_id, category):
        """ Обновить stack_state товара.
        :param category: идентификатор категории
        :param ware_id: идентификатор товара, type=str
        :param shop_id: идентификатор магазина, type=str
        :return: sql-запрос
        """

        # формируем запрос без значений
        query = """UPDATE warehouse.wares SET managed_category_id=%s """ \
        """WHERE ware_id='%s' AND shop_id=%s;""" % (category, ware_id, shop_id)
        return query



class ClassWarehouseSql(ClassGetWarehouseSql, ClassUpdateWarehouseSql):
    """ --== Класс буфер. ==--
    Содержит методы группирующие вызовы методов родительских классов.
    """
    pass