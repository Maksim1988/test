# -*- coding: utf-8 -*-
"""
Feature: Доступ к страницам по урлу
Description: Проверка, что страницы доступны по урлу
"""
import time
from unittest import skip

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from support import service_log
from support.utils.common_utils import priority, generate_sha256
from support.utils.db import databases
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods

__author__ = 'm.senchuk'


class OpenGoods(Navigate):
    """
    Story: Открыть страницы товаров
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_fast_driver()
        service_log.preparing_env(cls)

    @priority("low")
    def test_open_good_page(self):
        """
        Title: Открыть все товары.
        """
        do_time = time.time()
        count = 0   # счетчик обработкти товаров
        goods_not_opened = list()
        criteria = "'PUBLISHED'"   # товары только активные и неактивные
        statuses_id = databases.db7.accounting.get_stock_state_id_by_name(criteria)
        stat = ','.join([str(i['id']) for i in statuses_id])
        goods = databases.db7.accounting.get_all_goods_psql("stock_state_id in (%s)" % stat)  # получить все товары из БД
        goods_count = len(goods)    # количество товаров из БД
        service_log.put("Количество товаров %s" % goods_count)
        print("Count goods %s" % goods_count)
        service_log.put("Начало обработки товаров...")
        print("Start reading goods...")
        # В цикле происходит обход всех страниц товаров
        for good in goods:
            count += 1
            good_url = self.ENV_BASE_URL + self.path_good.URL_GOOD % good['ware_id']
            self.get_page(self.driver, self.path_good.URL_GOOD % good['ware_id'])
            try:
                good_name_db = good['content']['title']['value'].replace('\n', ' ')
                good_list = good_name_db.split(' ')
                # убираем из названия товара двойные ит.д. пробелы
                good_name = ' '.join([i for i in good_list if i != ''])
            except Exception:
                good_name = None
                service_log.warning("У товара %s нет названия" % good_url)
                print("WARNING: Good %s is not Title" % good_url)
            xpath_good = self.check_good.TITLE_WARE
            try:
                obj = self.find_element_by_xpath_fast(self.driver, xpath_good)
                service_log.put("Success! Element by xpath=%s is found." % xpath_good)
                self.assertIn(obj.text, good_name)
            except Exception:
                goods_not_opened.append(good_url)
                service_log.warning("Страница товара %s не открылась" % good_url)
                print("WARNING: Good page %s not opened" % good_url)
            if count % 100 == 0 or count == goods_count:
                service_log.put("Обработано %s товаров" % count)
                print("Reading %s goods" % count)
        work_time = self.work_time(do_time)
        service_log.put("Время работы [%s]" % work_time)
        service_log.put("Обработка товаров завершена.")
        print("Finish reading goods.")
        service_log.put("Товары не открылись:\n%s" % goods_not_opened)
        print("Warning goods:\n%s" % goods_not_opened)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class OpenCategories(Navigate):
    """
    Story: Открыть страницы категорий
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_fast_driver()
        service_log.preparing_env(cls)

    @priority("low")
    def test_open_category_page(self):
        """
        Title: Открыть все видимые категории.
        :return:
        """
        do_time = time.time()
        # xpath для раздела идля категории различается
        l = lambda x: self.check_catalog.PARENT_CATEGORY_ABSTRACT_BY_NAME if x['parent_id'] == 1 else \
            self.check_catalog.CATEGORY_ABSTRACT_BY_NAME
        count = 0   # счетчик обработкти категорий
        category_not_opened = list()
        parent_categories = databases.db3.accounting.get_parent_categories_visible()
        pc_str = ','.join([str(i['id']) for i in parent_categories if i['id'] != 0])
        criteria = "parent_id in (%s)" % pc_str  # видимые категории на сайте
        categories = databases.db3.accounting.get_categories_psql(criteria)   # получить категории из БД
        categories_count = len(categories)    # количество категорий из БД
        service_log.put("Количество категорий %s" % categories_count)
        print("Count categories %s" % categories_count)
        service_log.put("Начало обработки категорий...")
        print("Start reading categories...")
        # В цикле происходит обход всех страниц категорий
        for category in categories:
            count += 1
            category_url = self.ENV_BASE_URL + self.path_category.URL_PATH_ROOT_CATEGORY % category['id']
            self.get_page(self.driver, self.path_category.URL_PATH_ROOT_CATEGORY % category['id'])
            category_name = databases.db8.accounting.get_category_name(category['id'])[0]
            xpath_category = l(category) % category_name['value']
            try:
                self.find_element_by_xpath_fast(self.driver, xpath_category)
                service_log.put("Success! Element by xpath=%s is found." % xpath_category)
            except Exception:
                category_not_opened.append(category_url)
                service_log.warning("Страница категории %s не открылась" % category_url)
                print("WARNING: Category page %s not opened" % category_url)
            if count % 100 == 0 or count == categories_count:
                service_log.put("Обработано %s категорий" % count)
                print("Reading %s categories" % count)
        work_time = self.work_time(do_time)
        service_log.put("Время работы [%s]" % work_time)
        service_log.put("Обработка категорий завершена.")
        print("Finish reading categories.")
        service_log.put("Категории не открылись:\n%s" % category_not_opened)
        print("Warning categories:\n%s" % category_not_opened)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class OpenMain(Navigate):
    """
    Story: Открыть главную страницу
    """
    driver = None

    @staticmethod
    def reimann(RIEMANN_HOST, RIEMANN_PORT, metric1, metric1_value, metric3, metric3_value):
        """
        Отправка данных метрик в reimann (агрегатор graphite метрик)
        :param RIEMANN_HOST: хост RIEMANN
        :param RIEMANN_PORT: порт RIEMANN
        :param metric1, metric2, metric3: имена метрик
        :param metric1_value, metric2_value, metric3_value: значение метрик
        """
        import bernhard
        c = bernhard.Client(host=RIEMANN_HOST, port=RIEMANN_PORT)
        c.send({'service': metric1, 'metric': metric1_value},
               #{'service': metric2, 'metric': metric2_value},
               {'service': metric3, 'metric': metric3_value})
        q = c.query('true')

    @staticmethod
    def netcat(CARBON_SERVER, CARBON_PORT, content):
        """
        Отправка данных netcat'м в graphite
        :param CARBON_SERVER: хост для CARBON GRAPHITE
        :param CARBON_PORT: порт для CARBON GRAPHITE
        :param content: контент
        """
        from socket import socket
        sock = socket()
        sock.connect((CARBON_SERVER, CARBON_PORT))
        sock.sendall(content)
        sock.shutdown(1)
        while 1:
            data = sock.recv(1024)
            if data == "":
                break
            print "Received:", repr(data)
        print "Connection closed."
        sock.close()

    @staticmethod
    def home_element_present_time(self, do_get_time, wait=3):
        """
        Проверка, что появился на главной старнице элемент дом-активный
        :return: (время поиска элемента, флаг фейла)
        """
        flag_fail = True
        time_z3 = 0
        do_time = time.time()
        while time.time() - do_time < wait:
            try:
                self.find_element_by_xpath_fast(self.driver, '.icon-home', by=By.CSS_SELECTOR)
                work_time = self.work_time(do_time)
                flag_fail = False
                break
            except NoSuchElementException:
                pass
        if flag_fail is True:
            time_z3 = wait
            service_log.put("Элемент не найден.")
            self.driver.get_screenshot_as_file('tmp/main_page_not_present_%s.png' % str(time.ctime()).replace(' ', '_'))
        else:
            service_log.put("Элемент найден. время поиска: [%s]" % work_time)
            common_time = self.work_time(do_get_time)
            time_z3 = work_time.replace("00:00:", '').replace(',', '.')
            service_log.put("Common time: [%s]. Time to metric [%s]" % (common_time, time_z3))
        return time_z3, flag_fail

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_firefox_driver(manual_user_agent=True)
        service_log.preparing_env(cls)

    @skip('deprecated')
    @priority("low")
    def test_open_main(self):
        """
        Title: Открыть главную страницу
        """
        fail = 0
        count = 0
        env_base_url = self.ENV_BASE_URL
        metric_path = self.ENV_METRIC + ".main"
        metric1 = metric_path + ".DOM_on_load"
        metric2 = metric_path + ".received_page"
        metric3 = metric_path + ".element_present"
        send_ip = self.ENV_METRIC_IP
        send_port = int(self.ENV_METRIC_PORT)
        open_time = time.time()
        while time.time() - open_time < 1190:
            count += 1
            service_log.put("[PASS %s]" % count)
            service_log.put("Get page: %s" % env_base_url)
            do_get_work = time.time()
            self.driver.get(env_base_url)
            work_get_time = self.work_time(do_get_work)
            service_log.put("Onload event time: [%s]" % work_get_time)
            work_progress_time = self.progress(self.driver, wait=50)
            work_load_time = self.work_time(do_get_work)
            time_z1 = work_get_time.replace("00:00:", '').replace(',', '.')
            time_z2 = work_progress_time.replace("00:00:", '').replace(',', '.')
            service_log.put("Page received: %s" % env_base_url)
            service_log.put("Page received time: %s" % work_load_time)
            time_z3, flag = self.home_element_present_time(self, do_get_work, wait=50)
            fail += flag
            do_send = time.time()
            service_log.put("Send metric to Riemann")
            self.reimann(send_ip, send_port, metric1, float(time_z1), metric2, float(time_z2), metric3, float(time_z3))
            service_log.put("Success! Sent metric to Riemann. Send time: [%s]" % self.work_time(do_send))
            self.driver.delete_all_cookies()
        self.assertEqual(0, fail, "Element not found. Count=%s" % fail)
        # альтернативные варианты отправки данных в graphite
        #kkk = shell.ssh2.authorization.set_metric(time_z, cur_time)
        #self.netcat(send_ip, send_port, '%s %s %d\n' % (metric1, time_z1, cur_time))
        #self.reimann(send_ip, send_port, metric2, float(time_z2))

    @staticmethod
    def cond(driver):
        """
        Метод проверяет окончание загрузки DOM
        :param driver:
        :return:
        """
        return driver.execute_script("return document.readyState == 'complete';")

    @staticmethod
    def see_content(driver, see_time, wait=5):
        """
        Метод проверяет наличие активной кнопки домой
        :param driver:
        :return:
        """
        flag_fast_pass = True
        do_time = time.time()
        while time.time() - do_time < wait:
            try:
                Navigate.find_element_by_xpath_fast(driver, Navigate.check_main.MAIN_MENU_HOME_ACTIVE)
                work_time = Navigate.work_time(do_time)
                fail = 0
                break
            except NoSuchElementException:
                flag_fast_pass = False
                work_time = wait
                fail = 1
        if flag_fast_pass is True:
            return see_time, fail
        else:
            return work_time, fail

    @priority("medium")
    def test_open_main_ssr(self):
        """
        Title: Открыть главную страницу - server side rendering
        """
        fail = 0
        count = 0
        wait = WebDriverWait(self.driver, 50, 0.001)
        env_base_url = self.ENV_BASE_URL
        metric_path = self.ENV_METRIC + ".main"
        metric1 = metric_path + ".get_page"
        metric2 = metric_path + ".see_content"
        metric3 = metric_path + ".dom_loaded"
        send_ip = self.ENV_METRIC_IP
        send_port = int(self.ENV_METRIC_PORT)
        open_time = time.time()
        while time.time() - open_time < 1190:
            count += 1
            service_log.put("[PASS %s]" % count)
            service_log.put("Get page: %s" % env_base_url)
            do_get_work = time.time()
            self.driver.get(env_base_url)
            work_get_time = self.work_time(do_get_work)
            do_see_time = time.time()
            while time.time() - do_see_time < 50:
                try:
                    d = self.driver.page_source
                    self.assertIn(u'header__nav-home active', d)
                    break
                except Exception:
                    pass
            wait.until(self.cond)
            work_dom_loaded_time = self.work_time(do_see_time)
            service_log.put("DOM content loaded. Time [%s]" % work_dom_loaded_time)
            time_z1 = work_get_time.replace("00:00:", '').replace(',', '.')
            #time_z2 = work_see_time.replace("00:00:", '').replace(',', '.')
            time_z3 = work_dom_loaded_time.replace("00:00:", '').replace(',', '.')
            do_send = time.time()
            service_log.put("Send metric to Riemann")
            self.reimann(send_ip, send_port, metric1, float(time_z1), metric3, float(time_z3))
            service_log.put("Success! Sent metric to Riemann. Send time: [%s]" % self.work_time(do_send))
            self.driver.delete_all_cookies()
        self.assertEqual(0, fail, "Element not found. Count=%s" % fail)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class OpenAllPages(Navigate, HelpAuthCheckMethods):
    """
    Story: Открыть все страницы сайта
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_firefox_driver(manual_user_agent=True)
        service_log.preparing_env(cls)

    def get_urls_from_html(self, list_urls):
        """
        Получить список урлов со страницы
        :param list_urls:
        :return:
        """
        urls = list()
        base_url = self.driver.current_url.encode('utf-8')
        if self.ENV_BASE_URL in base_url:
            base_url = self.ENV_BASE_URL
        service_log.put("Reading urls in the %s page ..." % base_url)
        for url in list_urls:
            end_url = url.find('"')
            new_url = url[:end_url]
            service_log.put("Reading url %s ..." % new_url)
            if new_url == '/':
                service_log.put("Url going to main page")
            elif len(new_url) == 0:
                service_log.put("Incorrect url length")
            elif new_url[:2] == '//' and \
                    ('oorraa.net' in new_url or 'oorraa.com' in new_url or self.ENV_BASE_URL in new_url):
                new_url = 'https:' + new_url
                urls.append(new_url)
            elif new_url[0] == '/' and len(new_url) > 1:
                new_url = base_url + new_url
                urls.append(new_url)
            elif new_url[:4] == 'http' and \
                    ('oorraa.net' in new_url or 'oorraa.com' in new_url or self.ENV_BASE_URL in new_url):
                urls.append(new_url)
        return urls

    def sort_type_urls(self, list_urls, count_goods=1, count_catalog=1, count_store=1, count_chats=1):
        """
        Сортировка и удаление повторяющегося типа урлов
        :param list_urls:
        :return:
        """
        c_goods = 0
        c_catalog = 0
        c_store = 0
        c_chats = 0
        new_list_urls = list()
        for url in list_urls:
            if 'goods' in url:
                if c_goods < count_goods:
                    new_list_urls.append(url)
                c_goods += 1
            elif 'catalog' in url:
                if c_catalog < count_catalog:
                    new_list_urls.append(url)
                c_catalog += 1
            elif 'store' in url:
                if c_store < count_store:
                    new_list_urls.append(url)
                c_store += 1
            elif 'chats' in url:
                if c_chats < count_chats:
                    new_list_urls.append(url)
                c_chats += 1
            else:
                new_list_urls.append(url)
        return new_list_urls

    def check_status_code(self):
        """
        Проверка статус-кода возвращенного страницей
        :return:
        """
        source = self.driver.page_source.encode('utf-8')
        url = self.driver.current_url.encode('utf-8')
        if source.find('server__404') != -1:
            code_response = '404'
        elif source.find('<img alt="503"') != -1:
            code_response = '503'
        elif source.find('Internal Server Error') != -1:
            code_response = '500 Internal Server Error'
        elif source.find("Error: Couldn't find location for") != -1:
            code_response = "500 " + source[source.find('<body>')+6:source.find('</body>')]
        elif source.find('Connection refused') != -1:
            code_response = '500' + source[source.find('<body>')+6:source.find('</body>')]
        else:
            code_response = '200'
        return {code_response: url}

    @priority('medium')
    def test_open_all_pages(self):
        """
        Title: Получить все урлы на странице, перейти по всем урлам получить все урлы на странице, перейти по урлам
        """
        status_urls = list()
        all_urls = list()
        main_urls_sort = list()
        self.go_main(self.driver, phone='79999999999', passwd='123')
        status_urls.append(self.check_status_code())
        page = self.driver.page_source.encode('utf-8')
        body = page.split('<body')
        list_page_objs = body[1].split('href="')
        if len(list_page_objs) > 1:
            list_page_objs = list_page_objs[1:]
            main_urls = self.get_urls_from_html(list_page_objs)
            main_urls_sort = self.sort_type_urls(main_urls, 5, 5, 5, 5)
        else:
            service_log.put("On main page not found urls")
        for main_url in main_urls_sort:
            self.driver.get(main_url)
            service_log.put("Get url: %s" % main_url)
            status_urls.append(self.check_status_code())
            page = self.driver.page_source.encode('utf-8')
            body = page.split('<body')
            list_page_objs = body[1].split('href="')
            if len(list_page_objs) > 1:
                list_page_objs = list_page_objs[1:]
                urls = self.get_urls_from_html(list_page_objs)
                urls_sort = self.sort_type_urls(urls, 5, 5, 5, 5)
                tmp_list = list()
                for item in set(urls_sort).difference(all_urls):
                    tmp_list.append(item)
                all_urls.extend(tmp_list)
            else:
                service_log.put("On %s page not found urls" % main_url)
        new_check_urls = list()
        for items in set(all_urls).difference(main_urls_sort):
            new_check_urls.append(items)
        for url_check in new_check_urls:
            self.driver.get(url_check)
            service_log.put("Get url: %s" % url_check)
            status_urls.append(self.check_status_code())
        service_log.put(status_urls)
        bad_status_code_urls = list()
        for status in status_urls:
            st_code = status.get('200')
            if st_code is None:
                bad_status_code_urls.append(status)
        count_urls = str((len(main_urls_sort)+len(new_check_urls)))
        service_log.put("Reading %s url" % count_urls)
        self.assertEqual(bad_status_code_urls, list(), "Not opened urls:\n%s" % bad_status_code_urls)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()