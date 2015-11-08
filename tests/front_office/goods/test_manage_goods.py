# -*- coding: utf-8 -*-
"""
Feature: Страница Управление товарами (Мой магазин)
"""

from unittest import skip
from support.utils.common_utils import generate_sha256, priority



class MoveToActiveOrInactiveViaOperations():
    """
    Story: Переместить товар в Активные \ Неактивные, через Действия
    """

    @skip('need_auto')
    @priority("Must")
    def test_move_to_inactive_via_operations(self):
        """
        Title: Я могу переместить активный товар в неактивные, через Действия
        Description:
        * Товар отображается в списке Неактивных товаров, и не отображается в списке Активных
        * В БД у товара изменился признак активности на "Не активный"
        * На карточке товара есть плашка "Этот товар неактивен"
        """
        pass

    @skip('need_auto')
    @priority("Must")
    def test_move_to_active_via_operations(self):
        """
        Title: Я могу переместить неактивный товар в активные, через Действия
        Description:
        * Товар отображается в списке Активных товаров, и не отображается в списке Неактивных
        * В БД у товара изменился признак активности на "Активный"
        * На карточке товара нет плашки "Этот товар неактивен"
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_disable_move_to_active_if_good_rejected_by_moderator(self):
        """
        Title: Я  не могу переместить отклоненный модератором товар в активные. Действие недоступно.
        """
        pass



class OpenToEditViaOperations():
    """
    Story: Открыть товар на редактирование, через Действия
    """

    @skip('need_auto')
    @priority("High")
    def test_open_to_edit_via_operations(self):
        """
        Title: Я могу открыть выбранный товар на редактирование, через Действия
        """
        pass



class CreateOnTheBasisOf():
    """
    Story: Создать новый товар на основе выбранного
    """

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft_2(self):
        """
        Title:
        """
        pass



class SelectOrCancelSelection():
    """
    Story: Выделить несколько товаров \ Снять выделение
    """

    @skip('manual')
    @priority("Low")
    def test_select_one_good(self):
        """
        Title: Я могу выделить один товар и увижу плашку с доступными пакетными действиями и счетчиком кол-ва выделенных товаров
        Description:
        * На плашке отображается кол-во выделенных товаров = 1
        * На плашке отображается кнопка "Отмена"
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_cancel_selection_via_button(self):
        """
        Title: Если я сниму выделение с товара через кнопку "Отмена", плашка с доступными действиями исчезнет
        Description:
        * плашка исчезает и товар не отмечен выбранным
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_cancel_selection_via_checkbox(self):
        """
        Title: Если я сниму выделение с товара через снятие чек-бокса, плашка с доступными действиями исчезнет
        Description:
        * плашка исчезает и товар не отмечен выбранным
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_select_all_good_on_page(self):
        """
        Title: Я могу выделить все товары на странице, используя чек-бокс на плашке с доступными действиями
        Description:
        * На плашке отображается кол-во выделенных товаров
        * У всех товаров на странице отображается проставленным чек-бокс выделения
        """
        pass



class CustomazeShowcaseOfStore():
    """
    Story: Настроить витрину своего магазина (Изменить порядо следования товаров)
    """

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft_2(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft_3(self):
        """
        Title:
        """
        pass



class BatchMoveToActiveOrInactiveViaSelection():
    """
    Story: Пакетное перемещение товаров в Активные \ Неактивные, через Выделение
    """

    @skip('need_auto')
    @priority("Must")
    def test_batch_move_to_inactive_via_selection(self):
        """
        Title: Я могу выделить несколько активных товаров и переместить их в неактивные
        Description:
        * Товары отображаются в списке Неактивных товаров, и не отображается в списке Активных
        * В БД у товаров изменился признак активности на "Не активный"
        """
        pass

    @skip('need_auto')
    @priority("Must")
    def test_batch_move_to_active_via_selection(self):
        """
        Title: Я могу выделить несколько неактивных товаров и переместить их в активные, через Действия
        Description:
        * Товары отображаются в списке Активных товаров, и не отображается в списке Неактивных
        * В БД у товаров изменился признак активности на "Активный"
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_disable_move_to_active_if_good_rejected_by_moderator(self):
        """
        Title: Я  не могу переместить отклоненный модератором товар в активные. Кнопка залочена.
        """
        pass



class BatchChangePriceViaSelection():
    """
    Story: Пакетное изменение цены у товаров
    """

    @skip('draft')
    @priority("Low")
    def test_draft1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft2(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft3(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft4(self):
        """
        Title:
        """
        pass



class AboutMyStoreSection():
    """
    Story: Блок Информация о магазине
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



class GoodsListing():
    """
    Story: Пакетное изменение цены у товаров
    """

    @skip('manual')
    @priority("Low")
    def test_goods_listing_view(self):
        """
        Title: Внешний вид листинга товаров (Активные и Неактивные)
        """
        pass

    @skip('manual')
    @priority("High")
    def test_goods_listing_content(self):
        """
        Title: Содержимое листинга активных и неактивных товаров
        Description:
        * Вкладка "Активные" содержит: только товары данного продавца в статусе Активные
        * Вкладка "Неактивные" содержит: только товары данного продавца в статусе Неактивные, Отклоненные модератором и Ожидающие модерации
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_goods_listing_counter_rejected_by_moderator_goods(self):
        """
        Title: Счетчик отображает кол-во отклоненных на модерации товаров
        """
        pass

    @skip('manual')
    @priority("High")
    def test_goods_listing_add_good_page_link(self):
        """
        Title: Кнопка "Добавить товар" ведет на страницу добавления товара
        """
        pass

    @skip('manual')
    @priority("High")
    def test_goods_listing_bath_load_page_link(self):
        """
        Title: Кнопка "Пакетная загрузка" ведет на страницу пакетной загрузке товаров
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_goods_listing_rejected_by_moderator_good(self):
        """
        Title: Отклоненный модератором товар имеет причину отклонения и визуально выделен
        """
        pass

    @skip('raft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title: Пагинатор
        """
        pass



class ChangePriceForm():
    """
    Story: Форма пакетного изменения цены у товаров
    """

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft_2(self):
        """
        Title:
        """
        pass
















