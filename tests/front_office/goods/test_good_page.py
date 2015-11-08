# -*- coding: utf-8 -*-
"""
Feature: Страница Товара
"""
import time
from support import service_log

from support.utils.common_utils import priority, generate_sha256
from unittest import skip
from support.utils.db import databases
from tests import MainClass
from tests.front_office.authorization.classes.class_authorization import AuthCheckMethods as Auth
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.registration.classes.class_registration_email import RegEmailCheckMethods as Registration
from tests.worker_warehouse.class_warehouse import WarehouseCheckMethods
from tests.front_office.settings.classes.class_profile_settings import HelpProfileSettingsCheckMethods as Profile
from tests.front_office.goods.classes.class_good_page import GoodCheckMethods as Good
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods
from tests.front_office.not_sorted.classes.class_user_card import HelpUserCardCheckMethods


class ContactTheSeller(Profile, Auth, Good, Registration):
    """
    Story: Связаться с продавцом
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        cls.buyer_id = AccountingMethods.get_default_user_id(role='buyer')
        cls.seller_id = AccountingMethods.get_default_user_id(role='seller')
        databases.db1.accounting.update_account_details_by_criteria(cls.buyer_id, "locale='ru'")
        databases.db1.accounting.update_account_details_by_criteria(cls.seller_id, "locale='ru'")
        cls.buyer = databases.db1.accounting.get_user_by_account_id(cls.buyer_id)[0]
        cls.seller = databases.db1.accounting.get_user_by_account_id(cls.seller_id)[0]
        cls.shop = databases.db1.accounting.get_shop_details_by_shop_id(cls.seller["shop_id"])[0]
        criteria = "shop_id=%s and stock_state_id=2 order by random() limit 5;" % cls.seller_id
        cls.good = databases.db1.warehouse.get_wares_by_criteria(criteria)[0]
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

    @priority("Must")
    def test_contact_the_seller(self):
        """
        Title: Я, как Покупатель, могу отправить продавцу сообщение по Активному товару,
        нажав на "Связаться с продавцом"
        Description:
        Проверяется только действие, состав UI форм проверяется ниже отдельно
        Проверить:
        * После нажатия кнопки открывается окно "Связаться с продавцом"
        * После ввода и отправки сообщения отображается окно "Сообщение отправлено"
        * В чате с продавцом есть отправленное от меня сообщение и карточка товара. Проверить соответствие текста
        и товара.
        """
        AccountingMethods.save_user_password(user_id=self.buyer["id"], hash_passwd=self.buyer["code_value"],
                                             salt=self.buyer["salt"])
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.buyer["salt"])
        databases.db1.accounting.update_user_password(self.buyer["id"], hash_res_new)
        # Получить страницу авторизации
        self.get_page(self.driver, self.path_auth.PATH_AUTH)
        obj_phone, obj_password, obj_submit_button = self.get_data_authorization(self.driver)
        # Вводим данные на авторизацию
        self.send_phone(phone_object=obj_phone, phone_number=self.buyer["phone"])
        self.send_password(password_object=obj_password, password_number=default_new_passwd)
        # Нажатие на кнопку авторизации
        self.element_click(self.driver, obj_submit_button, change_page_url=True)
        self.is_logged(self.driver)
        self.get_page(self.driver, self.path_good.URL_GOOD % self.good['ware_id'])
        self.element_click(self.driver, self.click_good.BTN_CALL_SELLER, change_page_url=False)
        popup = self.get_form_call_seller(self.driver)
        card_good = popup["good"].text
        msg_text = u"Calling_to_seller_%s" % str(time.time())
        self.input_str(popup["input_message"], msg_text)
        self.element_click(self.driver, popup["btn_send"], change_page_url=False)
        success_popup = self.get_form_call_success(self.driver)
        self.element_click(self.driver, success_popup["btn_close"], change_page_url=False)
        self.get_page(self.driver, self.path_chat.URL_CHAT_WITH_USER % self.seller_id)
        messages = self.elements_is_present(self.driver, self.check_chat.LAST_MSG_WITH_SEPARATOR)
        self.assertIn(self.buyer['display_name'], messages[0].text, "The message was not sent from me")
        self.assertIn(card_good, messages[0].text, "Card good in popup not equal card good in chat")
        self.assertIn(self.buyer['display_name'], messages[1].text, "The message was not sent from me")
        self.assertIn(msg_text, messages[1].text, "Text message in popup not equal text message in chat")

    @skip('need_auto')
    @priority("Medium")
    def test_contact_the_seller_cancel(self):
        """
        Title: Я, как Покупатель, могу закрыть форму связи, выбрав Отменить, на форе ввода текста сообщения
        """
        pass

    @priority("Must")
    def test_contact_the_seller_as_guest(self):
        """
        Title: Я, как Гость, могу отправить продавцу сообщение по Активному товару, нажав на
        "Связаться с продавцом" и указав e-mail для ответа
        Description:
        Проверяется только действие, состав UI форм проверяется ниже отдельно
        Use Case:
        * Если я гость и нажимаю "Связаться с продавцом" по активному товару:
            - открывается окно "Связаться с продавцом"
            - среди прочих, присутствуют поля "Имя" и "e-mail"
        * Заполнить и отправить форму
            - отображается окно "Сообщение отправлено" с возможностью придумать пароль
            - В БД создался новый пользователь в статусе Wait_For_Registration (данные пользователя = вводимым данным)
        * Придумать пароль и нажать "Зарегистрироваться"
            - происходит автологин в систему под созданной учетной записью
            - отображается сообщение "Вы зарегистрированы на платформе"
            - В БД у созданного пользователя изменился статус на Enabled  и сохранился пароль
            - В чате с продавцом есть отправленное от меня сообщение и карточка товара.
            Проверить соответствие текста и товара.
        """
        buyer_name = u"TestUserName%s" % str(time.time())[:-3]
        msg_text = u"Calling_to_seller_%s" % str(time.time())
        buyer_email = self.get_new_email(databases.db1)
        new_password = AccountingMethods.get_default_password(5)
        self.get_page(self.driver, self.path_good.URL_GOOD % self.good['ware_id'])
        self.element_click(self.driver, self.click_good.BTN_CALL_SELLER, change_page_url=False)
        popup = self.get_visitor_form_call_seller(self.driver)
        card_good = popup["good"].text
        self.input_str(popup["input_your_name"], buyer_name)
        self.input_str(popup["input_message"], msg_text)
        self.input_str(popup["input_email"], buyer_email)
        self.element_click(self.driver, popup["btn_send"], change_page_url=False)
        time.sleep(self.time_sleep)
        # Check new user in DB
        accounting_status_1 = 'WAIT_FOR_REGISTRATION'
        criteria = "email='%s' and display_name='%s'" % (buyer_email, buyer_name)
        new_buyer = databases.db1.accounting.get_user_by_criteria(accounting_status_1, criteria)
        self.assertEqual(1, len(new_buyer), "The user is not created in the DB")
        success_popup = self.get_visitor_form_call_success(self.driver)
        self.input_str(success_popup["input_password"], new_password)
        self.element_click(self.driver, success_popup["btn_reg"], change_page_url=False)
        time.sleep(self.time_sleep)
        accounting_status_2 = 'ENABLED'
        buyer = databases.db1.accounting.get_user_by_criteria(accounting_status_2, criteria)
        self.assertGreaterEqual(len(buyer), 1, "The user is not updated account status in the DB")
        self.element_is_present(self.driver, self.check_good.NOTIFY_REG_SUCCESS)
        self.get_page(self.driver, self.path_chat.URL_CHAT_WITH_USER % self.seller_id)
        messages = self.elements_is_present(self.driver, self.check_chat.LAST_MSG_WITH_SEPARATOR)
        self.assertIn(buyer_name, messages[0].text, "The message was not sent from me")
        self.assertIn(card_good, messages[0].text, "Card good in popup not equal card good in chat")
        self.assertIn(buyer_name, messages[1].text, "The message was not sent from me")
        self.assertIn(msg_text, messages[1].text, "Text message in popup not equal text message in chat")

    @skip('manual')
    @priority("High")
    def test_contact_the_seller_as_guest_already_in_db(self):
        """
        Title: Я, как Гость, не могу отправить продавцу сообщение, если ввел уже существующий в системе e-mail
        Description:
        * Отображается сообщение "
        """
        pass

    @skip('need_auto')
    @priority("Medium")
    def test_contact_the_seller_disable_if_i_good_owner(self):
        """
        Title: Я, как Продавец на картчоке по своему Активному товару, не могу "Связаться с продавцом" т.к. кнопка
        залочена
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_contact_the_seller_disable_if_good_inactice(self):
        """
        Title: Я, как Покупатель, не могу написать продавцу сообщение по Не активному товару, т.к. кнопка залочена
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_contact_the_seller_disable_if_good_wait_moderation(self):
        """
        Title: Я, как Покупатель, не могу написать продавцу сообщение по Ожидающему повторной модерации товару,
        т.к. кнопка залочена
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class ComplainAboutGood():
    """
    Story: Пожаловаться на товар
    """

    @skip('need_auto')
    @priority("High")
    def test_complain_about_good(self):
        """
        Title: Я как Покупатель, могу отправить жалобу на товар Модератору, нажав на "Пожаловаться на товар"
        Description:
        * Проверить, что при нажатии на кнопку, пользователю выдается сообщений, что жалоба отправлена модератору.
        * Проверить, что после отсылки сообщения кнопка становится неактивной
        * Проверить, что после обновления страницы кнопка становится активной
        * Проверить, что отправленное сообщение пришло Модератору
        Wiki:
        * id модератора задается в property файле фронта
        * Жалоба приходит в виде: Текста "Пользователь пожаловался на товар" + карточка товара
        """
        pass

    @skip('need_auto')
    @priority("High")
    def test_complain_about_good_as_guest(self):
        """
        Title: Я как Гость, при нажатии на "Пожаловаться на товар" увижу страницу Авторизации
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_complain_about_good_disable_if_i_good_owner(self):
        """
        Title: Я как Продавец не могу пожаловаться на свой товар, т.к не вижу данной кнопки
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_complain_about_good_disable_if_good_inactice(self):
        """
        Title: Я как Покупатель могу пожаловаться на неактивный товар, нажав на "Пожаловаться на товар"
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_complain_about_good_disable_if_good_wait_moderation(self):
        """
        Title: Я как Покупатель могу пожаловаться на отклоненный модератором товар (Banned),
        нажав на "Пожаловаться на товар"
        """
        pass


class OpenZoomPhoto(Profile, Good):
    """
    Story: Открыть фото товара на zoom
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        criteria = "json_array_length(content->'pictures'->'value')>2 and stock_state_id=2 order by random() limit 5;"
        cls.goods = databases.db1.warehouse.get_wares_by_criteria(criteria)
        count = len(cls.goods)
        assert count > 1, "No found goods with criteria"
        cls.good = cls.goods[0]
        cls.pictures = cls.good['content'][u'pictures'][u'value']
        cls.count_pict = len(cls.pictures)
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        cls.get_page(cls.driver, cls.path_good.URL_GOOD % cls.good["ware_id"])
        service_log.preparing_env(cls)

    @priority("Must")
    def test_open_zoom_photo(self):
        """
        Title: Я могу открыть на zoom фото товара. Я могу закрыть фото твоара с zoom
        """
        main_pict = self.pictures[0]
        gallery = self.get_gallery(self.driver, self.pictures, main_pict)
        self.element_click(self.driver, gallery["btn_zoom"], change_page_url=False)
        zoom_gallery = self.get_gallery_zoom(self.driver, self.pictures, main_pict)
        self.element_click(self.driver, zoom_gallery["close"], change_page_url=False)
        self.element_is_none(self.driver, self.click_good.POPUP_ZOOM_GALLERY)

    @skip('manual')
    @priority("Medium")
    def test_listing_zoom_photo(self):
        """
        Title: Если фото, товаров несколько то я могу их пролистать в режиме zoom
        """
        pass

    @priority("Must")
    def test_select_photo_in_gallery(self):
        """
        Title: Я могу выбрать нужное фото товара, кликнув на него в виджете Галлерея
        """
        main_pict = self.pictures[0]
        last_pict = self.pictures[self.count_pict-1]
        gallery = self.get_gallery(self.driver, self.pictures, main_pict)
        self.element_click(self.driver, gallery["prev_%s" % self.count_pict], change_page_url=False)
        self.get_gallery(self.driver, self.pictures, last_pict)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class BreadcrumbsElement(Profile, Good):
    """
    Story: Хлебные крошки
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        criteria = "stock_state_id=2 order by random() limit 5;"
        cls.goods = databases.db1.warehouse.get_wares_by_criteria(criteria)
        count = len(cls.goods)
        assert count > 1, "No found goods with criteria"
        cls.good = cls.goods[0]
        cls.mng_cat = cls.good['managed_category_id']
        cat = databases.db1.accounting.get_management_categories_by_criteria("id=%s" % cls.mng_cat)[0]
        tree = cls.get_tree_categories(databases.db1, cat["catalog_id"])
        # делаем реверс списка категория, чтобы первой была родительская категория, а последней финальная категория
        tree.reverse()
        cls.tree = list(tree)
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        cls.get_page(cls.driver, cls.path_good.URL_GOOD % cls.good["ware_id"])
        service_log.preparing_env(cls)

    @priority("Must")
    def test_breadcrumb_view(self):
        """
        Title: Хлебные крошки отображают путь до товара в каталоге
        """
        self.get_tree_breadcrumbs(self.driver, self.tree, databases.db1)

    @skip('need_auto')
    @priority("Medium")
    def test_breadcrumbs_change(self):
        """
        Title: При изменении расположения товара в каталоге - соответствующим образом меняются хлебные крошки.
        """
        pass

    @priority("Must")
    def test_breadcrumbs_click(self):
        """
        Title: Click: По хлебным крошкам можно перейти в соответствующи товару родительские категории
        Description:
        * Click: Я могу перейти в каталог, в Подкатегорию к которой принадлежит данный товар используя хлебные крошки
        * Click: Я могу перейти в каталог в Категорию к которой принадлежит данный товар, используя хлебные крошки.
        * Click: Я могу перейти в каталог в Раздел к которой принадлежит данный товар, используя хлебные крошки.
        """
        count = 0
        for cat in self.tree:
            count += 1
            obj_breads = self.get_tree_breadcrumbs(self.driver, self.tree, databases.db1)
            self.element_click(self.driver, obj_breads[count], change_page_url=True)
            url = self.driver.current_url.encode('utf-8')
            self.assertIn(str(cat), url, "Не произошел переход на страницу каталога")
            self.driver.back()

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()


class OtherStoreGoodsSection():
    """
    Story: Блок "Другие товары магазина"
    """

    @skip('manual')
    @priority("Low")
    def test_other_store_goods_section_view1(self):
        """
        Title: Внешний вид блока (чужой товар)
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_other_store_goods_section_view2(self):
        """
        Title: Внешний вид блока (свой товар)
        """
        pass

    @skip('need_auto')
    @priority("Medium")
    def test_other_store_goods_section_click(self):
        """
        Title: Click: Я могу перейти в другой товар продавца, кликнув на него в блоке Другие товары продавца.
        Description:
        При этом товар на который я перешел не будет отображаться в блоке Другие товары.
        """
        pass

    @skip('need_auto')
    @priority("Medium")
    def test_other_store_goods_section_content(self):
        """
        Title: Содержимое блока
        Description:
        Проверить:
        * отображаются 4е  экспресс карточки товаров
        * все товары принадлежат данному магазину
        * все товары только в статусе Активный (Неактивные товары не отображаются в блоке)
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_other_store_goods_section_empty_foreign(self):
        """
        Title: Если у продавца больше нет ни одного активного товара (кроме просматриваемого),
        то блок не отображается на странице.
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_other_store_goods_section_empty_myself(self):
        """
        Title: Если это мой товар и у меня нет ни одного активного товара (кроме просматриваемого),
        то блок отображает действие Добавить товар
        Description:
        * Отображается соответствующий текст (типа у вас нет других товаров)
        * Отображается кнопка "Добавить товар"
        * Кнопка ведет на форму добавления товара
        """
        pass


class SimilarGoodsSection():
    """
    Story: Блок "Похожие товары"
    """

    @skip('manual')
    @priority("Low")
    def test_similar_goods_section_view(self):
        """
        Title: Внешний вид блока
        """
        pass

    @skip('need_auto')
    @priority("Medium")
    def test_similar_goods_section_click(self):
        """
        Title: Click: Я могу перейти в другой товар продавца, кликнув на него в блоке Похожие товары.
        Description:
        При этом товар на который я перешел не будет отображаться в блоке Похожие товары.
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_similar_goods_section_content(self):
        """
        Title: Содержимое блока
        Description:
        Проверить:
        * отображаются 4е  экспресс карточки товаров
        * уточнить по какому принципу идет отбор товаров в данный блок
        * все товары только в статусе Активный (Неактивные товары не отображаются в блоке)
        """
        pass



class DetailAboutGoodSection():
    """
    Story: Блок "Детально о товаре"
    """

    @skip('manual')
    @priority("Low")
    def test_detail_about_good_view(self):
        """
        Title: Внешний вид блока
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_detail_about_good_id_and_creation_date(self):
        """
        Title: На карточке товара отображается ID товара и дата создания
        """
        pass



class AboutStoreSection():
    """
    Story: Блок "Детально о товаре"
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


class ContactTheSellerForm():
    """
    Story: Окно "Связаться с продавцом" (для пользователя)
    """

    @skip('manual')
    @priority("Low")
    def test_contact_the_seller_form_view(self):
        """
        Title: Вид формы Связаться с продавцом (для пользователя)
        Description:
        На форме отображается:
        * Название = Связаться с продавцом
        * Аватар + Имя продавца чей товар
        * Карточка товара, по которому задается вопрос
        * Поле для отправки сообщения
        * Карточка товара ведет на страницу данного товара
        """
        pass

    @skip('need_auto')
    @priority("Medium")
    def test_contact_the_seller_form_empty_message(self):
        """
        Title: Нет возможности отправить пустое сообщение. Кнопка отправки залочена.
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_contact_the_seller_form_max_message(self):
        """
        Title: Поле "Сообщение" максимально принимает 500 символов
        Description: Это не точно, нужно уточнить требования
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_contact_the_seller_form_negative_message(self):
        """
        Title: Нет возможности отправить сообщение с текстом в 501 символ.
        Description: Отображается сообщение "Уточнить текст"
        Кроме того нужно уточнить действительные ограничения на поле
        """
        pass


class ContactTheSellerFormForGuest():
    """
    Story: Окно "Связаться с продавцом" (для гостя)
    """

    @skip('need_auto')
    @priority("Medium")
    def test_contact_the_seller_form_for_guest_empty_name(self):
        """
        Title: Нет возможности отправить сообщение не указав Имя
        Description:
        * Отображается сообщение "Введите имя"
        """
        pass

    @skip('need_auto')
    @priority("Medium")
    def test_contact_the_seller_form_for_guest_empty_email(self):
        """
        Title: Нет возможности отправить сообщение не указав e-mail
        Description:
        * Отображается сообщение "Введите e-mail"
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_contact_the_seller_form_for_guest_positive_name_and_email(self):
        """
        Title: Проверка ограничения на поля формы: Позитивные значения
        Description:
        Наборы значений: Зеленые из таблицы сущностей, проверить:
        * Сообщение отправлено и отображается в чате с продавцом
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_contact_the_seller_form_for_guest_negative_name_and_email(self):
        """
        Title: Проверка ограничения на поля формы: Негативные значения
        Description:
        Наборы значений: Красные из таблицы сущностей, проверить:
        * невозможность отправить сообщение
        * выдачу соответствующего предупреждающего сообщения
        """
        pass




















