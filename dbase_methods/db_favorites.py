# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Класс работы с Cassandra для воркера Favorites.
#
# P.S: — Хорошо излагает, собака, — шепнул Остап на ухо Ипполиту Матвеевичу, — учитесь. (с)
#--------------------------------------------------------------------
from support.utils.db_cassandra import ClassSaveLinkCassandra, execute_cql

__author__ = 's.trubachev'


class ClassFavoritesData(ClassSaveLinkCassandra):
    pass


class ClassGetFavoritesCql(ClassFavoritesData):

    @execute_cql
    def get_limit_favorites(self, limit=100):
        """ Взять все товары.
        WARNING: товаров может быть очень много.
        :param limit: количество элементов
        :return: список с данными по товарам
        """
        return """select * from favorites limit %s;""" % limit

    @execute_cql
    def get_fav_wares_by_user_id(self, user_id, limit=100):
        """ Получить список избранных товаров по идентификатору пользователя.
        :param user_id: идентификатор пользователя
        :return: список с данными по товарам
        """
        return """select * from user_with_fav_wares where user_id = %s limit %s;""" % (user_id, limit)

    @execute_cql
    def get_fav_wares(self, limit=100):
        """ Получить список избранных товаров по идентификатору пользователя.
        :param limit: количество элементов
        :return: список с данными по товарам
        """
        return """select * from user_with_fav_wares limit %s;""" % limit

    @execute_cql
    def get_fav_users_by_user_id(self, user_id, limit=100):
        """ Получить список избранных товаров по идентификатору пользователя.
        :param user_id: идентификатор пользователя
        :param limit: количество элементов
        :return: список с данными по пользователям
        """
        return """select * from user_with_fav_users where user_id = %s limit %s;""" % (user_id, limit)

    @execute_cql
    def get_fav_users(self, limit=100):
        """ Получить список избранных пользователей по идентификатору пользователя.
        :param limit: количество элементов
        :return: список с данными по пользователям
        """
        return """select * from user_with_fav_users limit %s;""" % limit


class ClassFavoritesCql(ClassGetFavoritesCql):
    """ --== Класс буфер. ==--
    Содержит методы группирующие вызовы методов родительских классов.
    """
    pass

