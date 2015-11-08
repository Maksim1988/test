# -*- coding: utf-8 -*-
"""
Feature: Определение и изменение языковой версии сайта
"""

from support.utils.common_utils import priority
from unittest import skip


class ChangeLanguageVersion():
    """
    Story: Изменение языковой версии сайта
    """

    @skip('manual')
    @priority("Medium")
    def test_change_language_version(self):
        """
        Title: Проверить изменение версии сайта через выпадающий список (4-е языка)
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_save_lang_version_in_session_context_1(self):
        """
        Title: Изменение языковой версии и ее сохранение в контексте ссесии для пользователя: Не залогинен и Не менял язык
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_save_lang_version_in_session_context_2(self):
        """
        Title: Изменение языковой версии и ее обновление в контексте ссесии для пользователя: Не залогинен и Менял язык
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_save_lang_version_in_locale(self):
        """
        Title: Изменение языковой версии и обновление locale в профиле для пользователя: Залогинен
        """
        pass







class DefinitionUserLanguageVersion():
    """
    Story: Определение языковой версии сайта
    """

    @skip('manual')
    @priority("Low")
    def test_definition_language_by_browser(self):
        """
        Title: Определение языковой версии по языку браузера: Не залогинен и Не менял язык
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_definition_language_by_session_context(self):
        """
        Title: Определение языковой версии по контексту ссесии: Не залогинен и Менял язык
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_definition_language_by_locale_in_db(self):
        """
        Title: Определение языковой версии по locale в профиле: Залогинен
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_definition_language_in_resistration(self):
        """
        Title: Проверить  что при регистрации пользователя locale проставляется = текущему языку
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_definition_language_in_utorization(self):
        """
        Title: Проверить, что при авторизации пользователя , он переключается на языковую версию = той,
        которая у него в locale, вне зависимости от того, какой у него язык был выбран до авторизации
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_definition_language_in_private_browser(self):
        """
        Title: Проверить, что в приватной вкладке браузера определение языковой версии идет по языку браузера
        Description:
        * Проверить, что в приватной вкадке браузера сохраняется язык браузера
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_definition_language_alternative(self):
        """
        Title: Альтернатива 1: Случаи когда изменение основного языка браузера не влияют на отображаемый язык
        Description:
        * Проверить, что для случая (Не залогинен и Менял язык) изменение основного языка браузера
        не влияет на отображаемый язык (т.к определение идет по контексту ссесии)
        * Проверить, что для случая (Залогинен) изменение основного языка браузера
        не влияет на отображаемый язык (т.к определение идет по locale в профиле)
        """
        pass
