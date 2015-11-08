# -*- coding: utf-8 -*-
"""
Feature: Жизненный цикл товара
"""

from unittest import skip
from support.utils.common_utils import generate_sha256, priority



class GoodLifeCycle():
    """
    Story: Жизненный цикл товара
    Description:
    Проверяется прохождение товаром Жизненного цикла (http://portal.home.oorraa.net/pages/viewpage.action?pageId=656259)
    и отображение его на сайте в зависимости от состояния
    """

    @skip('manual')
    @priority("Must")
    def test_good_life_cycle_1(self):
        """
        Title: 1. Основной: Утвержден на модерации
        """
        pass

    @skip('manual')
    @priority("Must")
    def test_good_life_cycle_2(self):
        """
        Title: 2. Основной: Отклонен на модерации
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_good_life_cycle_3(self):
        """
        Title: 3. Альтернатива: Создан как Не Активный
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_good_life_cycle_4(self):
        """
        Title: 4. Альтернатива: Отклонен на повторной модерации
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_good_life_cycle_5(self):
        """
        Title: 5. Альтернатива: Попавший в модерацию товар переносят в Не Активный
        Description:
        * Создание товара > активный > модерация утвердить > активный прошел > неактивный прошел
        """
        pass

