# -*- coding: utf-8 -*-
"""
Feature: Страницы ошибок (404, 503)
"""

from support.utils.common_utils import priority
from unittest import skip


class Error404Page():
    """
    Story: Страница 404 Error
    """

    @skip('need_auto')
    @priority("High")
    def test_error_404_page_not_found(self):
        """
        Title: Проверить выдачу данной страницы, если введен url страницы которой нет на сайте
        Description:
        * Проверить выдачу данной страницы, если введен url страницы которой нет на сайте
        * Проверить выдачу данной страницы, при запросе товара которого нет на сайте
        * Проверить выдачу данной страницы, при запросе магазина продавца которого нет на сайте
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_error_404_view(self):
        """
        Title: Внешний вид страницы 404
        Description:
        * Есть шапка
        * Есть подвал
        * Есть картинка 404 и текст сообщения
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_error_404_link(self):
        """
        Title: Кнопка "На главную" ведет на главную страницу портала
        """
        pass



class Error503Page():
    """
    Story: Страница 503 Error
    """

    @skip('manual')
    @priority("Low")
    def test_error_503_service_unavailable(self):
        """
        Title: Проверить выдачу данной страницы, когда бекэнд недоступен
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_error_404_view(self):
        """
        Title: Внешний вид страницы 503
        Description:
        * Нет шапки
        * Нет подвала
        * Есть картинка 503 и текст сообщения
        """
        pass

