# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Класс работы с Cassandra для воркера Warehouse.
#
# P.S: — Хорошо излагает, собака, — шепнул Остап на ухо Ипполиту Матвеевичу, — учитесь. (с)
#--------------------------------------------------------------------
from support.utils.common_utils import run_on_prod
from support.utils.db_cassandra import ClassSaveLinkCassandra, execute_cql

__author__ = 'm.senchuk'


class ClassCassandraSmsData(ClassSaveLinkCassandra):
    pass


class ClassGetCassandraSmsCql(ClassCassandraSmsData):

    @execute_cql
    def get_sms(self, phone):
        """ Взять все смс по заданному номеру
        :return: список с данными по товарам
        """
        return """SELECT * FROM sms WHERE destination='%s' order by creation_timestamp desc;;""" % phone


class ClassUpdateCassandraSmsCql(ClassCassandraSmsData):
    pass


class ClassCassandraSmsCql(ClassGetCassandraSmsCql, ClassUpdateCassandraSmsCql):
    """ --== Класс буфер. ==--
    Содержит методы группирующие вызовы методов родительских классов.
    """
    pass

