# -*- coding: utf-8 -*-
"""
Feature: Страница Магазина
"""

from unittest import skip
from support.utils.common_utils import priority



class TestSortGoods():
    """
    Story: Отсортировать товары (по дате, по цене, вернуть в исходное) на странице магазина
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
    Story: Фильтровать товары (пол, материал, цвет, цена за штуку) на странице магазина
    """

    @skip('draft')
    @priority("Low")
    def test_draft_name1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft_name2(self):
        """
        Title:
        """
        pass



class TestSeeSellerPhone():
    """
    Story: Посмотреть телефон продавца
    """

    @skip('need_auto')
    @priority("Medium")
    def test_see_seller_name_for_guest(self):
        """
        Title: Кнопка "Показать телефон" ведёт на регистрацию, если пользователь не авторизован
        """
        pass

    @skip('need_auto')
    @priority("Medium")
    def test_see_seller_name_for_autorized_user(self):
        """
        Title: Кнопка "Показать телефон" показывает телефон магазина, если пользователь авторизован
        """
        pass

    @skip('need_auto')
    @priority("Medium")
    def test_see_seller_name_disabled_if_phone_empty(self):
        """
        Title: Кнопки "Показать телефон" нет, если владелец магазина не указал телефона в настройках магазина
        """
        pass



class TestAddOrDeleteUserFromContactList():
    """
    Story: Добавить \ Удалить пользователя из контакт листа
    """

    @skip('need_auto')
    @priority("High")
    def test_add_user_to_contact_list(self):
        """
        Title: Добавление пользователя в список контактов
        Description:
        Если пользователя нет контакт листе:
         * то кнопка называется "В контакты"
         * При нажатии на нее, пользователь добавляется в контакт листа
         * кнопка меняет название на "В контактах"
        """
        pass

    @skip('need_auto')
    @priority("High")
    def test_delete_user_from_contact_list(self):
        """
        Title: Удаление пользователя из списка контактов.
        Description:
        Если пользователь уже есть в контакт листе:
         * то кнопка называется "В контактах"
         * При нажатии на нее, пользователь удаляется из контакт листа
         * кнопка меняет название на "В контакты"
        """
        pass

    @skip('need_auto')
    @priority("Medium")
    def test_add_user_to_contact_list_disabled(self):
        """
        Title: Если пользователь находится в своем магазине возможность добавить (удалить) в контакты залочена
        """
        pass

    @skip('need_auto')
    @priority("Medium")
    def test_add_user_to_contact_list_for_guest(self):
        """
        Title: Если пользователь неавторизованный, то кнопка ведёт на страницу регистрации
        """
        pass



class TestSubscribeToShopNews():
    """
    Story: Подписаться на новинки магазина
    """

    @skip('need_auto')
    @priority("High")
    def test_subscribe_to_shop_news(self):
        """
        Title: Подписаться на новинки магазина
        Description:
        Если пользователь еще не подписан на новинки магазина:
         * то кнопка называется "Подписаться на новинки магазина"
         * При нажатии на нее ... (видимо где то в базе проставляется соотв-й флаг)
         * кнопка меняет название на "Отписаться от новинок магазина"
        """
        pass

    @skip('need_auto')
    @priority("High")
    def test_unsubscribe_from_shop_news(self):
        """
        Title: Отписаться от подписки на новинки магазина
        Description:
        Если пользователь уже подписан на новинки магазина:
         * то кнопка называется "Отписаться от новинок магазина"
         * При нажатии на нее ... (видимо где то в базе убирается соотв-й флаг)
         * кнопка меняет название на "Подписаться на новинки магазина"
        """
        pass

    @skip('need_auto')
    @priority("Medium")
    def test_subscribe_disabled(self):
        """
        Title: Если пользователь находится в своем магазине возможность подписаться на новинки залочена
        """
        pass

    @skip('need_auto')
    @priority("Medium")
    def test_subscribe_for_guest(self):
        """
        Title: Если пользователь неавторизованный, то кнопка ведёт на страницу регистрации
        """
        pass



class TestContactSeller():
    """
    Story: Связаться с продавцом
    """

    @skip('need_auto')
    @priority("High")
    def test_contact_seller(self):
        """
        Title: При нажатии на "Связаться с продавцом" открывается страница чата с данным продавцом
        """
        pass


    @skip('need_auto')
    @priority("Medium")
    def test_contact_seller_disabled(self):
        """
        Title: Если пользователь находится в своем магазине возможность связаться залочена
        """
        pass

    @skip('need_auto')
    @priority("Medium")
    def test_contact_seller_for_guest(self):
        """
        Title: Если пользователь неавторизованный, то кнопка ведёт на страницу регистрации
        """
        pass



class TestGoodsListingSection():
    """
    Story: Листинг товаров на странице магазина
    """

    @skip('need_auto')
    @priority("High")
    def test_listing_goods_view(self):
        """
        Title: Отображаются только активные товары (Активные.В модерации и Активные.Утвержден)
        """
        pass

    @skip('manual')
    @priority("High")
    def test_listing_goods_pagination(self):
        """
        Title: На страницу помещается 40 экспресс-карточек товаров. Остальное скрывается пагинацей
        Description:
        * Если товаров 40 - пагинатор не отображается
        * Если товаров 41 - отображается вторая страница пагинатора
        """
        pass

    @skip('need_auto')
    @priority("High")
    def test_click_to_good(self):
        """
        Title: Click: При клике на экспресс-карточку товара происходит переход на карточку данного товара
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_foreign_listing_goods_empty(self):
        """
        Title: Заглушка "Нет товаров", если в чужом магазине нет товаров
        Description:
        Если у продавца нет ни одного товара в статусе Активный, отображается соответств-й текст-аглушка
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_my_listing_goods_empty(self):
        """
        Title: Заглушка "Добавить товар", если в своём магазине нет товаров
        Description:
        Если пользователь в своем магазине где нет ни одного товара в статусе Активный, отображается соответств-й текст-заглушка
        """
        pass



class TestAboutStoreSection():
    """
    Story: Блок Информация о магазине и владельце магазина
    """

    @skip('manual')
    @priority("Medium")
    def test_draft_test_1(self):
        """
        Title: Отображается Карточка Магазина
        Description:
        Провоерить, что информация в карточку выводится из настроек магазина продавца + дописать тесты
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_draft_test_2(self):
        """
        Title: Отображается Карточка Пользователя
        Description:
        * Проверить, что информация в карточку выводится из настроек продавца
        * Проверить, что Карточка Пользователя отображается только в виде Чужой магазин и не отображается в виде Свой магазин
        * дописать тесты
        """
        pass



class TestStoreOwnerTape():
    """
    Story: Плашка Владельца магазина
    """

    @skip('manual')
    @priority("Medium")
    def test_owner_tape(self):
        """
        Title: Плашка "Так видят ваш магазин другие пользователи" отображается только для роли ПРОДАВЕЦ.СВОЙ_МАГАЗИН.
        Description:
        * если пользователь просматривает чуждой магазин - плашки нет
        * если пользователь просматривает свой магазин - плашка есть + соотв. текст на ней
        * при Logout плашка "Это ваш магазин" исчезает (...)
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_owner_tape_edit_store_button(self):
        """
        Title: Click: Я могу перейти на страницу редактирования своего магазина, кникнув на "Редактировать"
        """
        pass



class TestOtherTests():
    """
    Story: Прочие тесты
    """

    @skip('manual')
    @priority("Low")
    def test_redirect_to_store(self):
        """
        Title: Переход по /user/{id_продавца} редиректит на /store/{id_продавца}
        """
        pass