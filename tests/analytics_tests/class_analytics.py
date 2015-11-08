# -*- coding: utf-8 -*-
from support import service_log
from support.utils.common_utils import json_to_dict, url_decode
from tests.MainClass import MainClass
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateData

__author__ = 's.trubachev'


class HelpAnalyticsData(MainClass):

    # данные для доступа к Segment
    READ_KEY = "ODlUkX414m443mQNpnj4TZsWHJ2LiilW"
    WRITE_KEY = "eEQ1ZAxCdV4NQGdZY9qA5VwtSBw22SHl"
    PROJECT_ID = "UoKMSxu4j0"

    # страницы на которые может зайти не авторизованный пользователь
    PATH_PAGES_NO_AUTH = [HelpNavigateData.path_auth.PATH_AUTH,
                          HelpNavigateData.path_help.UH_HOW_BE_SELLER,
                          HelpNavigateData.path_help.UH_HOW_BUY,
                          HelpNavigateData.path_category.URL_ALL_BESTSELLERS,
                          HelpNavigateData.path_category.URL_ALL_WARE_NEW,
                          HelpNavigateData.path_category.URL_ALL_LAST_DEALS,
                          HelpNavigateData.path_category.URL_GOODS_FROM_BEST_SELLERS,
                          HelpNavigateData.path_category.URL_POPULAR_GOODS,
                          # TODO: поведение при уже авторизованном пользователе - переход на главную, как будут себя вести счетчики аналитики:
                          HelpNavigateData.path_back_auth.URL_LOGIN]

    # Старинцы на которые может зайти покупатель
    PATH_PAGES_BYER = [HelpNavigateData.path_favorites.URL_FAVORITES_GOODS,
                       HelpNavigateData.path_favorites.URL_FAVORITES_USERS,
                       HelpNavigateData.path_settings.PATH_PROFILE_SETTINGS,
                       HelpNavigateData.path_contacts.URL_CONTACTS]

    # Старинцы требующие подстановки каких-то уточняющих данных, например номера конкретной категории или магазина
    # HelpNavigateData.path_shop.URL_SHOP,

    # Старинцы на которые может зайти только продавец
    PATH_PAGES_SELLER = [HelpNavigateData.path_my_goods]

    USER_AGENT = {
        "bot": True,
        "user": False
    }


class HelpAnalyticsMethods(HelpAnalyticsData):

    @staticmethod
    def get_js_scripts(segment_url='http://example.com/segment'):
        """ Получить JavaScript для внедренния его в страницу и перехвата метрик.
        :param: url-адрес для отсылки перехваченного сообщения.
        :return: type(str)
        """

        service_log.put("Response url for script: %s" % segment_url)
        p = """(function(url){

                var iframe = document.createElement('iframe');
                var form = document.createElement('form');
                var input = document.createElement('input');

                function init() {
                    var iid = 'segment_iframe';

                    document.body.appendChild(iframe);
                    iframe.style.display = 'none';
                    iframe.contentWindow.name = iid;

                    form.target = iid;
                    form.action = url;
                    form.method = 'POST';

                    input.type = 'hidden';
                    input.name = 'segmentData';

                    form.appendChild(input);
                    document.body.appendChild(form);
                }

                function sendData(method, arguments) {
                    input.value = JSON.stringify({
                        method: method,
                        params: arguments
                    });

                    form.submit();
                }

                ['identify', 'track', 'page', 'alias'].forEach(function(method){
                    var oldMeth = analytics[method];

                    analytics[method] = function() {
                        sendData(method, arguments);
                        oldMeth.apply(this, arguments);
                    };
                });

                init();

            })('%s' /* урл для отправки данных */)""" % segment_url
        service_log.put("Get JavaScript for load in page")
        return p

    @staticmethod
    def get_js_scripts2(segment_url='http://example.com/segment'):
        """ Получить JavaScript для внедренния его в страницу и перехвата метрик.
        P.S: Обновленный скрипт
        :param: url-адрес для отсылки перехваченного сообщения.
        :return: type(str)
        """

        service_log.put("Response url for script: %s" % segment_url)
        p = """(function(url){

                function sendData(method, args) {
                    var data = {
                        segmentMethod: method,
                        // Делаем из args нормальный массив
                        params: Array.prototype.slice.call(args, 0)
                    };
                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", url);
                    xhr.send(JSON.stringify(data));
                }

                ["identify", "track", "page", "alias"].forEach(function(method){
                    var oldMeth = analytics[method];

                    analytics[method] = function() {
                        sendData(method, arguments);
                        oldMeth.apply(this, arguments);
                    };
                });

            })('%s' /* урл для отправки данных */);""" % segment_url
        service_log.put("Get JavaScript for load in page")
        return p

    @staticmethod
    def inclusion_js_script(driver):
        """ Интегрировать скрипт в страницу.
        :return: True
        """
        service_log.put("Inclusion javascript in the html-page.")
        from support.utils.variables import EVariable
        script_js = HelpAnalyticsMethods.get_js_scripts2(":".join([EVariable.serv.url, EVariable.serv.port]))
        driver.execute_script(script_js)
        return True

    @staticmethod
    def parsing_segment_data(data):
        """ Парсим результат работы методов Segment.
        :param data: строка с данными
        :return: type(dict)
        """
        service_log.put("Parsing segment data.")
        segment_data = url_decode(data).replace("segmentData=", "")
        return json_to_dict(segment_data)


class HelpAnalyticsCheckMethods(HelpAnalyticsMethods):

    def check_first_visit(self, segment_data, page="index"):
        """ Проверка первого визита на страницу для не зарегистрированного пользователя.
        :param segment_data: данные счетчиков
        :param page: страница с которой пришли счетчики
        """
        self.assertEqual(segment_data["segmentMethod"], "track")
        self.assertEqual(segment_data["params"]["0"], "First Visit")
        self.assertEqual(segment_data["params"]["1"]["page"], page)
        self.assertEqual(segment_data["params"]["1"]["visitFrom"], "web")

    def check_search_result(self, segment_data, query, role=u'anonymous'):
        """ Проверка первого визита на страницу для не зарегистрированного пользователя.
        :param segment_data: данные счетчиков
        :param query: запрос
        :param role: роль в системе
        """
        self.assertEqual(segment_data["segmentMethod"], "track")
        self.assertEqual(segment_data["params"][0], "Search Results View")
        self.assertEqual(segment_data["params"][1]["query"], query)
        self.assertEqual(segment_data["params"][1]["role"], role)
        self.assertEqual(segment_data["params"][1]["type"], "goods")
        self.assertEqual(segment_data["params"][1]["visitFrom"], "web")
        # TODO: self.assertEqual(segment_data[u'params'][1][u'label'], 1) Для чего это?
        # TODO: self.assertEqual(segment_data[u'params'][1][u'result'], 1) Как это?

    def check_search_query(self, segment_data, query, role=u'anonymous'):
        """ Проверка поискового запроса.
        :param query: поисковый запрос
        :param segment_data: данные счетчиков
        """
        self.assertEqual(segment_data["segmentMethod"], "track")
        self.assertEqual(segment_data["params"][0], "Search")
        self.assertEqual(segment_data["params"][1]["query"], query)
        self.assertEqual(segment_data["params"][1]["visitFrom"], 'web')
        self.assertEqual(segment_data["params"][1]["role"], role)
        # TODO: self.assertEqual(segment_data[u'params'][1][u'label'], u'/') Для чего это?

    def check_first_visit_for_auth(self, segment_data, role, page="index"):
        """ Проверка первого визита на страницу для зарегистрированного пользователя.
        :param role: роль пользователя в системе
        :param segment_data: данные счетчиков
        :param page: страница с которой пришли счетчики
        """
        self.assertEqual(segment_data["method"], "track")
        self.assertEqual(segment_data["params"]["0"], "First Visit")
        self.assertEqual(segment_data["params"]["1"]["page"], page)
        self.assertEqual(segment_data["params"]["1"]["role"], role)
        self.assertEqual(segment_data["params"]["1"]["visitFrom"], "web")

    def check_login(self, segment_data, role):
        """ Проверка авторизации пользователя.
        :param role: роль пользователя в системе
        :param segment_data: данные счетчиков
        """
        self.assertEqual(segment_data["method"], "track")
        self.assertEqual(segment_data["params"]["0"], "LogIn")
        self.assertEqual(segment_data["params"]["1"]["role"], role)

    def check_analytics_as_bot(self, source):
        """
        Проверка, что скрипты аналитики не подключены на странице
        :return:
        """
        service_log.put("Check not load analytics scripts as bot user-agent.")
        self.assertNotIn('segment', source, "Source page include Segment script")
        self.assertNotIn('metrika', source, "Source page include Yandex.Metrika script")

    def check_analytics_as_user(self, source):
        """
        Проверка, что скрипты аналитики подключены на странице
        :return:
        """
        service_log.put("Check load analytics scripts as normal user-agent.")
        self.assertIn('segment', source, "Source page not include Segment script")
        self.assertIn('metrika', source, "Source page not include Yandex.Metrika script")