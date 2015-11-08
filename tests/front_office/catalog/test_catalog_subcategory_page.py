# -*- coding: utf-8 -*-
"""
Feature: Страница Подкатегории Каталога (3-й уровень каталога)
"""
from unittest import skip
from support.utils.common_utils import priority



class TestChangePageView():
    """
    Story: Изменить вид страницы
    """

    @skip('draft')
    @priority("draft")
    def test_draft_name1(self):
        """
        Title:
        """
        pass



class TestSortGoods():
    """
    Story: Отсортировать товары (по дате, по цене, вернуть в исходное)
    """

    @skip('manual')
    @priority("Medium")
    def test_sort_goods_by_date(self):
        """
        Title: Я могу сортировать товары по дате↓↑
        Description:
        * Проверить корректность работы сортировки по дате публикации (в оба направления)
        * Проверить что url страницы при сортировки меняется
        * Проверить что иконки изменяются, отображая выбранный способ сортировки "стрелвка вверх" и "стрелка вниз"
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_sort_goods_by_price(self):
        """
        Title: Я могу сортировать по цене↓↑
        Description:
        * Проверить корректность работы сортировки по цене
            * сортировка по возрастанию цены: сначала дешевые, потом дорогие, потом без цены
            * сортировка по убыванию цены: сначала дорогие, потом дешевые, потом без цены
        * Проверить что иконки изменяются, отображая выбранный способ сортировки "стрелвка вверх" и "стрелка вниз"
        * Проверить что url страницы при сортировки меняется
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_sort_goods_by_default(self):
        """
        Title: Я могу вернуть сортировку в исходную, по кнопке По умолчанию
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_only_one_method_sorting(self):
        """
        Title: Я не могу сортировать одновременно по дате и цене. Выбор одного способа сортировки отменяет другой
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_sorting_goods_with_paginator(self):
        """
        Title: Проверить корректность работы сортировки товаров с пагинатором
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_sorting_goods_with_filtering(self):
        """
        Title: Проверить корректность работы сортировки товаров с фильтрацией
        """
        pass



class TestFilteringGoods():
    """
    Story: Фильтровать товары (пол, материал, цвет, цена за штуку)
    """

    @skip('draft')
    @priority("draft")
    def test_draft_name1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("draft")
    def test_draft_name2(self):
        """
        Title:
        """
        pass



class TestMenuCategirySection():
    """
    Story: Меню категории
    """

    @skip('draft')
    @priority("draft")
    def test_draft_name1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("draft")
    def test_draft_name2(self):
        """
        Title:
        """
        pass



class TestGoodsListingSection():
    """
    Story: Листинг товаров
    """

    @skip('draft')
    @priority("draft")
    def test_draft_name1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("draft")
    def test_draft_name2(self):
        """
        Title:
        """
        pass