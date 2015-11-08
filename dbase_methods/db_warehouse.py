# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Класс работы с Cassandra для воркера Warehouse.
#
# P.S: — Хорошо излагает, собака, — шепнул Остап на ухо Ипполиту Матвеевичу, — учитесь. (с)
#--------------------------------------------------------------------
from support.utils.common_utils import run_on_prod
from support.utils.db_cassandra import ClassSaveLinkCassandra, execute_cql

__author__ = 's.trubachev'


class ClassCassandraData(ClassSaveLinkCassandra):

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


class ClassGetCassandraCql(ClassCassandraData):

    @execute_cql
    def get_wares(self):
        """ Взять все товары.
        WARNING: товаров может быть очень много.
        :return: список с данными по товарам
        """
        return """select * from wares;"""

    @execute_cql
    def get_wares_with_limit(self, limit=100):
        """ Взять несколько товаров.
        :param limit: количество товаров в зпросе
        :return: список с данными по товарам
        """
        return """select * from wares limit %s;""" % limit

    @execute_cql
    def get_wares_by_shop_id(self, shop_id):
        """ Взять несколько товаров по идентификатору магазина.
        :param shop_id: идентификатор магазина
        :return: список с данными по товарам
        """
        return """select * from wares where shop_id=%s;""" % shop_id

    @execute_cql
    def get_wares_by_ware_id(self, ware_id):
        """ Взять товар по идентификатору товара.
        :param ware_id: идентификатор товара
        :return: список с данными по товару
        """
        return """select * from wares where ware_id = '%s';""" % ware_id

    @execute_cql
    def get_wares_by_ware_ids(self, ware_ids):
        """ Взять товары по идентификаторам товаров.
        :param ware_id: строка идентификаторов товаров через запятую
        :return: список с данными по товарам
        """
        return """select * from wares where ware_id in (%s) ALLOW FILTERING;""" % ware_ids


class ClassGetCassandraAccountingCql(ClassCassandraData):

    @execute_cql
    def get_fav_user_by_user_id(self, user_id):
        """
        Получить избранных пользователей по идентификатору пользователя
        :return: список с данными по товарам
        """
        return """select * from user_with_fav_users where user_id = %s;""" % user_id

    @execute_cql
    def get_fav_user_in_cl_user(self, user_id, fav_usr_id):
        """
        Проверить есть ли избранный пользователь у пользователя в контакт листе
        :return: список с данными по товарам
        """
        return """select * from user_with_fav_users where user_id=%s and fav_usr_id=%s;""" % (user_id, fav_usr_id)


class ClassUpdateCassandraCql(ClassCassandraData):

    @execute_cql
    @run_on_prod(False)
    def update_ware_by_ware_id(self, criteria, ware_id):
        """ Обновить существующий товар по заданному критерию.
        Запоминаем первичный ключ shop_id, т.к. мы его потом удалим.
        Удаляем первичные ключи, т.к. их по ним строится индекс и они не изменяются.
        Формируем CQL-запрос с условием из первичных и с данными без онных.
        :param criteria: строка критерии обновления, type=dict
        :param ware_id: идентификатор товара, type=str
        :return: cql-запрос, список с данными, type=tuple
        """

        #  подготовка данных
        shop_id = criteria["shop_id"]
        criteria = self.delete_primary_keys_from_dict(criteria)
        format_cql = ", ".join([str(index) + " = ?" for index in criteria.keys()])

        # формируем запрос без значений
        query = """UPDATE wares SET %s WHERE ware_id=? AND shop_id=?;""" % format_cql

        # формируем значения для биндинга в запрос
        params_for_query = criteria.values() + [ware_id, shop_id]
        return query, params_for_query


class ClassCassandraCql(ClassGetCassandraCql, ClassUpdateCassandraCql, ClassGetCassandraAccountingCql):
    """ --== Класс буфер. ==--
    Содержит методы группирующие вызовы методов родительских классов.
    """
    pass

