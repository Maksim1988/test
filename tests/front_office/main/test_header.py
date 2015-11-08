# -*- coding: utf-8 -*-
"""
Feature: Шапка
"""
from unittest import skip
from support.utils.common_utils import priority


class Logout():
    """
    Story: Выход из аккаунта
    """

    @skip('need_auto')
    @priority("Must")
    def test_logout_from_public_page(self):
        """
        Title: Если я залогинен и нахожусь на общедоступной странице, то я могу выполнить логаут из системы, кликнув на "Выход" в выпадающем меня профиля
        Descriptoin:
        * Вид шапки изменился на шпаку для Гостя
        * Если logout с общедоступной страницы, то отображается данная страница в виде Гость.
        """
        pass

    @skip('need_auto')
    @priority("Must")
    def test_logout_from_private_page(self):
        """
        Title: Если я залогинен и нахожусь на личной странице, то я могу выполнить логаут из системы, кликнув на "Выход" в выпадающем меня профиля
        Descriptoin:
        * Вид шапки изменился на шпаку для Гостя
        * Если logout с личной страницы, то отображается страница Авторизации
        """
        pass


class HeaderForGuest():
    """
    Story: Шапка Сайта для Гостя
    """

    @skip('need_auto')
    @priority("Must")
    def test_header_for_guest_view(self):
        """
        Title: Если я Гость, то я вижу в шапке: Лого УУРРАА, строку поиска, кнопку "Вход"
        """
        pass

    @skip('need_auto')
    @priority("Must")
    def test_header_for_guest_click_to_login(self):
        """
        Title: Click: Если я Гость, то я могу перейти на страницу Регистрации, нажав на "Войти"
        """
        pass



class HeaderForUser():
    """
    Story: Шапка Сайта для Пользователя платформы
    """

    @skip('need_auto')
    @priority("Must")
    def test_header_for_user_view(self):
        """
        Title: Проверить состав шапки сайта для зарегистрированного пользователя платформы
        Description:
        Шапка сайта состоит из:
        * Лого УУРРАА,
        * строка поиска,
        * "Сообщения",
        * "Контакты",
        * Профиль пользователя, содержащий: "Мой магазин", "Мои товары", "Избранное", "Настройки" и "Выход"
        """
        pass

    @skip('need_auto')
    @priority("Must")
    def test_header_for_user_click_to_messages(self):
        """
        Title: Click: Если я Продавец, то я могу перейти к своим сообщениям с пользователями, кликнув на "Сообщения"
        """
        pass

    @skip('need_auto')
    @priority("Must")
    def test_header_for_user_click_to_contacts(self):
        """
        Title: Click: Если я Продавец, то я могу перейти к своим контактам, кликнув на "Контакты"
        """
        pass

    @skip('need_auto')
    @priority("Must")
    def test_header_for_user_click_to_my_shop(self):
        """
        Title: Click: Если я Продавец, то я могу перейти на страницу Мой магазин, кликнув на "Мой магазин.Активные" в выпадающем меня профиля
        """
        pass

    @skip('need_auto')
    @priority("Must")
    def test_header_for_user_click_to_favorites(self):
        """
        Title: Click: Если я Продавец, то я могу перейти на страницу Избранные товары, кликнув на "Избранное" в выпадающем меня профиля
        """
        pass

    @skip('need_auto')
    @priority("Must")
    def test_header_for_user_click_to_settings(self):
        """
        Title: Click: Если я Продавец, то я могу перейти на страницу настроек своего профиля, кликнув на "Настройки" в выпадающем меня профиля
        """
        pass