# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# Класс работы с Elasticsearch для воркера Warehouse.
#
#
# --------------------------------------------------------------------
from support.utils.common_utils import convert_dict_to_json
from support.utils.db_elasticsearch import execute_query, ClassSaveLinkElasticsearch

__author__ = 's.trubachev'


class ClassElasticsearchData(ClassSaveLinkElasticsearch):
    pass


class ClassGetElasticsearchQuery(ClassElasticsearchData):
    @execute_query
    @convert_dict_to_json
    def get_popular_wares(self, size=5):
        """ Взять популярные товары.
        :return: список с данными по товарам
        """
        query_popular_wares = {"from": 0,
                               "size": size,
                               "post_filter": {
                                   "bool": {
                                       "must": [
                                           {"bool": {
                                               "should": [
                                                   {"term": {"moderationState": "accepted"}},
                                                   {"term": {"moderationState": "believed"}}]}},
                                           {"bool": {"should": {"term": {"stockState": "published"}}}},
                                           {"bool": {"must": {
                                               "bool": {"should": {"term": {"special_category_marker": "totalpopular"}}}
                                           }}}
                                       ]
                                   }
                               },
                               "explain": True,
                               "sort": [{"creationTimestamp": {"order": "desc"}}]}
        return query_popular_wares

    @execute_query
    @convert_dict_to_json
    def get_last_deals_wares(self, size=5):
        """ Взять товары последних сделох.
        :return: список с данными по товарам
        """
        query_last_deals_wares = {"from": 0,
                                  "size": size,
                                  "post_filter": {
                                      "bool": {
                                          "must": [
                                              {"bool": {
                                                  "should": {"term": {"moderationState": "accepted"}}}},
                                              {"bool": {"should": {"term": {"stockState": "published"}}}},
                                              {"range": {"lastDealTimestamp": {
                                                  "from": 1,
                                                  "to": None,
                                                  "include_lower": True,
                                                  "include_upper": True
                                              }}}
                                          ]
                                      }
                                  },
                                  "explain": True,
                                  "sort": [{"lastDealTimestamp": {"order": "desc"}}]}
        return query_last_deals_wares

    @execute_query
    @convert_dict_to_json
    def get_best_sellers_wares(self, size=5):
        """ Взять товары лучших продовцов.
        size - число
        :return: список с данными по товарам
        """
        query_best_sellers_wares = {"from": 0,
                                    "size": size,
                                    "post_filter": {
                                        "bool": {
                                            "must": [
                                                {"bool": {
                                                    "should": [
                                                        {"term": {"moderationState": "accepted"}},
                                                        {"term": {"moderationState": "believed"}}
                                                    ]
                                                }},
                                                {"bool": {"should": {"term": {"stockState": "published"}}}},
                                                {"bool": {"must": {
                                                    "bool": {
                                                        "should": {"term": {"special_category_marker": "bestsellers"}}
                                                    }
                                                }}}
                                            ]
                                        }
                                    },
                                    "explain": True,
                                    "sort": [{"creationTimestamp": {"order": "desc"}}]}
        return query_best_sellers_wares

    @execute_query
    @convert_dict_to_json
    def get_new_wares(self, size=5):
        """ Взять товары 'Новинки'.
        :return: список с данными по товарам
        """
        query_new_wares = {"from": 0,
                           "size": size,
                           "post_filter": {
                               "bool": {
                                   "must": [
                                       {"bool": {"should": {"term": {"moderationState": "accepted"}}}},
                                       {"bool": {"should": {"term": {"stockState": "published"}}}}
                                   ]
                               }
                           },
                           "explain": True,
                           "sort": [{"creationTimestamp": {"order": "desc"}}]}
        return query_new_wares

    @execute_query
    @convert_dict_to_json
    def get_wares_final_category(self, size=5, macro_value=None, final_filter=None):
        """ Взять товары 'Новинки'.
        :return: список с данными по товарам
        """
        query_new_wares = {"from": 0,
                           "size": size,
                           "post_filter": {
                               "bool": {
                                   "must": [
                                       {
                                           "bool": {
                                               "should": [
                                                   {"term": {"moderationState": "accepted"}},
                                                   {"term": {"moderationState": "believed"}}
                                               ]
                                           }
                                       },
                                       {
                                           "bool": {"should": {"term": {"stockState": "published"}}}
                                       },
                                       {
                                           "bool": {
                                               "must": [
                                                   {"bool": {"should": {"term": {"macro_type": macro_value}}}},
                                                   {"bool": {"should": {"term": {final_filter['name']:
                                                                                     final_filter['value']
                                                   }}}}
                                               ]
                                           }
                                       }
                                   ]
                               }
                           },
                           "explain": True, "sort": [{"creationTimestamp": {"order": "desc"}}]}
        return query_new_wares


    @execute_query
    @convert_dict_to_json
    def get_spec_category_wares(self, size=5, marker=None):
        """ Взять товары спец категории.
        size - число
        :return: список с данными по товарам
        """
        query_spec_category_wares = {"from": 0,
                                     "size": size,
                                     "post_filter": {
                                         "bool": {
                                             "must": [
                                                 {"bool": {
                                                     "should": [
                                                         {"term": {"moderationState": "accepted"}},
                                                         {"term": {"moderationState": "believed"}}
                                                     ]
                                                 }},
                                                 {"bool": {"should": {"term": {"stockState": "published"}}}},
                                                 {"bool": {"must": {
                                                     "bool": {
                                                         "should": {"term": {"special_category_marker": marker}}
                                                     }
                                                 }}}
                                             ]
                                         }
                                     },
                                     "explain": True,
                                     "sort": [{"creationTimestamp": {"order": "desc"}}]}
        return query_spec_category_wares


    @execute_query
    @convert_dict_to_json
    def get_bestsellers_category_wares(self, size=5, macro_type=None):
        """ Взять товары бестселлеры категории.
        size - число
        macro_type - родительская категория
        :return: список с данными по товарам
        """
        query_bestsellers_cat_wares = {
            "from": 0,
            'size': size,
            'post_filter': {
                "bool": {
                    "must": [
                        {"bool": {"should": {"term": {"moderationState": "accepted"}}}},
                        {"bool": {"should": {"term": {"stockState": "published"}}}},
                        {
                            "range": {"startedDeals": {
                            "from": 1, "to": None, "include_lower": True, "include_upper": True}}
                        },
                        {"bool": {"must": {"bool": {"should": {"term": {"macro_type": macro_type}}}}}}
                    ]
                }
            },
            "explain": True,
            "sort": [
                {"successfulDeals": {"order": "desc"}},
                {"startedDeals": {"order": "desc"}}
            ]
        }

        return query_bestsellers_cat_wares

    @execute_query
    @convert_dict_to_json
    def get_wares(self, size=1):
        """ Взять товары бестселлеры категории.
        size - число
        macro_type - родительская категория
        :return: список с данными по товарам
        """
        query_wares = {
            "from": 0,
            'size': size,
            "explain": True
        }

        return query_wares


class ClassElasticsearchQuery(ClassGetElasticsearchQuery):
    """ --== Класс буфер. ==--
    Содержит методы группирующие вызовы методов родительских классов.
    """
    pass