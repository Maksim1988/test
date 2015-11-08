# -*- coding: utf-8 -*-
from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from tests.MainClass import MainClass

__author__ = 'm.senchuk'


class ProfileSettingsPage(MainClass):

    class Path():
        URL_SHOP_INFO = "/user/settings/store"
        URL_DELIVERY_INFO = "/user/settings/delivery"
        URL_PAYMENT_INFO = "/user/settings/payment"
        URL_COMPANY_DETAILS = "/user/settings/details"
        URL_CHANGE_PASSWORD = "/user/settings/password"
        PATH_PROFILE_SETTINGS = "/user/settings/profile"
        PATH_COMMON_INFO = "//form[contains(@class,'form_settings')]"
        PATH_SHOP_INFO = "//form[@class='form form_store-info']/fieldset[@class='form__fieldset']"
        PATH_ABOUT_COMPANY = "//fieldset[@class='form__fieldset form__fieldset_company']/div[@class='form__group']"
        PATH_BANKING_INFO = "//div[@class='form__group']/div[@class='form__group form__group_banking']"
        PATH_PASSWD_CHANGE = "//fieldset[@class='form__fieldset' and contains(.,'Смена пароля')]"

    class Check():
        ADDRESS_YOUR_PAGE = "//div[@class='alert alert_info']/span[contains(.,'Адрес Вашей страницы')]"

        TITLE_PROFILE_SETTINGS = "//h1[@class='title__name' and contains(.,'Настройки')]"
        TITLE_COMMON_INFO = "//h2[@class='inner-layout__title' and contains(.,'Профиль пользователя')]"
        TITLE_ABOUT_COMPANY = "//div[@class='form__legend' and contains(.,'О компании')]"
        TITLE_BANKING_INFO = "//div[@class='form__legend' and contains(.,'Банковские реквизиты')]"
        TITLE_PASSWD_CHANGE = "//div[@class='form__legend' and contains(.,'Смена пароля')]"

        TEXT_LIST = "//span[contains(.,'%s')]"

        AVATAR_PATH = "//div[@class='form__preview']/img[@class='form__photo' and @src='%s%s_s100x100']"
        FORM_PHONE_DISABLED = "//input[@class='form__input' and @type='tel' and @disabled and @value='%s']"
        FORM_ID_USER = "//div[@class='form__static']/span[@class='form__text' and contains(.,'%s')]"
        FORM_ROLE_USER = "//span[@class='form__text form__text_bold' and contains(.,'%s')]"
        PREFIX_SHOP_ADDRESS = "//span[@class='form__input__before' and contains(.,'')]"

        STATUS_CHECKBOX_ADDRESS = "//input[@type='checkbox' and %s]"
        LIST_CHECKBOX = {True: "@checked",
                         False: "not(@checked)"}

        TEXT_HELP_PASSWD1 = "Пароль должен содержать не менее шести символов, содержащих минимум 1 цифру и минимум 1 " \
                            "заглавную букву. Язык ввода — английский"
        TEXT_HELP_PASSWD = TEXT_HELP_PASSWD1

        FORM_HELP_PASSWD_CHANGE = "//span[contains(.,'%s')]" % TEXT_HELP_PASSWD
        ERROR_PATH_PASSWD_OLD = "//div[@class='form__row form__row_error'][1]/label"
        ERROR_PATH_PASSWD_NEW = "//div[@class='form__row form__row_error'][2]/label"
        ERROR_PATH_PASSWD_NEW_REPEAT = "//div[@class='form__row form__row_error'][3]/label"

        DIV_NOTIFICATION_SUCCESS = "//div[@class='notification notification_success']"
        DIV_NOTIFICATION_ERROR = "//div[@class='notification notification_error']"
        FORM_SUCCESS_CHANGE = "//span[@class='notification__title' and contains(.,'%s')]"
        FORM_ERROR_CHANGE = "//span[@class='notification__title' and contains(.,'%s')]"

        FORM_ERROR_MESSAGE = "//span[@class='form__error' and contains(.,'%s')]"
        FORM_ERROR_MESSAGE_ABSTRACT = "//span[@class='form__error']"

        LIST_SAVE_TEXT = {"COMMON": "Профиль успешно изменен",
                          "PASSWD": "Пароль успешно изменен",
                          "PASSWD_ERR": "Ошибка изменения пароля"}


        HELP_ADD_AVATAR_TEXT = "//div[@class='form__hint form__hint_avatar']/" \
                               "span[contains(.,'Фото')]"

        #TODO: Изменения для новых настроек профиля
        TITLE_CHANGE_PASSWORD = "//h2[contains(.,'Смена пароля')]"

        LABEL_NAME = "//label/span[contains(.,'Имя:')]"
        LABEL_GENDER = "//div[@class='form__row'][2]/span[contains(.,'Пол:')]"
        LABEL_PHONE = "//label/span[contains(.,'Телефон:')]"
        LABEL_EMAIL = "//label/span[contains(.,'Эл. почта:')]"
        LABEL_USER_ID = "//div[@class='form__row']/span[contains(.,'ID пользователя:')]"
        TEXT_USER_ID = "//div[@class='form__row']/div[@class='form__static']"

        LABEL_PASSWORD = "//label/span[contains(.,'Текущий пароль:')]"
        LABEL_N_PASSWORD = "//label/span[contains(.,'Новый пароль:')]"
        LABEL_R_PASSWORD = "//label/span[contains(.,'Повторите пароль:')]"

        CHANGE_PASSWORD_SUCCESS = "//div[@class='notification__wrapper' and contains(.,'Пароль успешно изменен')]"

        TITLE_STORE_INFO = "//h2[contains(.,'О компании')]"
        LABEL_STORE_URL = "//div[@class='inner-layout__content']/div[contains(.,'Адрес вашего магазина" \
                          "oorraa.com/store/%s')]"
        LABEL_STORE_NAME = "//label/span[contains(.,'Наименование компании:')]"
        LABEL_STORE_ADDRESS = "//label/span[contains(.,'Адрес магазина:')]"
        LABEL_DESCRIPTION = "//label/span[contains(.,'Описание:')]"
        CHANGE_STORE_INFO_SUCCESS = "//div[@class='notification__wrapper' and contains(.,'Информация о магазине сохранена')]"

        TITLE_COMPANY_DETAILS = "//h2[contains(.,'Реквизиты компании')]"
        LABEL_ABOUT_COMPANY = "//div[@class='form__legend' and contains(.,'О компании')]"
        LABEL_LEGAL_NAME = "//label/span[contains(.,'Полное наименование юр.') and contains(.,'лица:')]"
        LABEL_INN = "//label/span[contains(.,'ИНН:10-12 символов')]"
        LABEL_KPP = "//label/span[contains(.,'КПП:9 символов')]"
        LABEL_OGRN = "//label/span[contains(.,'ОГРН:13 символов')]"
        LABEL_LEGAL_ADDRESS = "//label/span[contains(.,'Юридический адрес:')]"
        LABEL_REAL_ADDRESS = "//label/span[contains(.,'Фактический адрес:')]"
        LABEL_BANK_DETAILS = "//div[@class='form__legend' and contains(.,'Банковские реквизиты')]"
        LABEL_BIK = "//label/span[contains(.,'БИК:9 символов')]"
        LABEL_BANK_NAME = "//label/span[contains(.,'Наименование и местоположение банка:')]"
        LABEL_BANK_ACCOUNT = "//label/span[contains(.,'Номер счета:20 символов')]"
        LABEL_CORRESPONDENT = "//label/span[contains(.,'Корреспондентский счет:20 символов')]"

        TITLE_PAYMENT = "//h2[contains(.,'Оплата')]"
        LABEL_PAYMENT_INFO = "//div[contains(@class,'inner-layout__notice') and contains(.,'Данная информация будет " \
                             "отображаться на всех ваших карточках товаров.')]"
        LABEL_CASH = "//div[@class='form__row form__row_switcher']//span[contains(.,'Наличными')]"
        LABEL_CASH_ON_DELIVERY = "//div[@class='form__row form__row_switcher']//span[contains(.,'Наложенным платежом')]"
        LABEL_PAY_BANK_ACCOUNT = "//div[@class='form__row form__row_switcher']//span[contains(.,'По счету через банк')]"
        LABEL_CARD = "//div[@class='form__row form__row_switcher']//span[contains(.,'Переводом на карту банка:')]"
        LABEL_E_MONEY = "//div[@class='form__row form__row_switcher']//span[contains(.,'Картой или электронными " \
                        "деньгами:')]"
        CHANGE_PAYMENTS_SUCCESS = "//div[@class='notification__wrapper' and contains(.,'Информация о способах оплаты " \
                                  "сохранена')]"

        CHANGE_DELIVERY_SUCCESS = "//div[@class='notification__wrapper' and contains(.,'Информация о способах " \
                                  "доставки сохранена')]"
        TITLE_DELIVERY = "//h2[contains(.,'Доставка')]"
        LABEL_DELIVERY_INFO = "//div[contains(@class,'inner-layout__notice') and contains(.,'Данная информация будет " \
                              "отображаться на всех ваших карточках товаров.')]"
        LABEL_TK = "//div[@class='form__row form__row_switcher']//span[contains(.,'Транспортными компаниями:')]"
        LABEL_COURIER = "//div[@class='form__row form__row_switcher']//span[contains(.,'Курьером по городу:')]"
        LABEL_OWN_DEL_SERVICE = "//div[@class='form__row form__row_switcher']//span[contains(.,'Собственная служба " \
                                "доставки')]"
        LABEL_MAIL = "//div[@class='form__row form__row_switcher']//span[contains(.,'Почта России')]"
        LABEL_PICKUP = "//div[@class='form__row form__row_switcher']//span[contains(.,'Самовывоз:')]"

    class Click():
        URL_YOUR_PAGE = "//div[@class='alert alert_info']/a[contains(@href,'/store/%s')]/span[contains(.,'oorraa.com/store/')]/.." \
                        "/span[contains(.,'%s')]/.."
        LIST_WANT_ROLE_SELLER = {True: "//button[@type='button' and @disabled and contains(.,'Заявка отправлена')]",
                                 False: "//button[@type='button' and not(@disabled) and "
                                        "contains(.,'Заявка на роль продавца')]"}
        DELETE_AVATAR_BUTTON = "//span[@class='form__hint form__hint_delete']"
        AVATAR_EMPTY_PATH = "//div[@class='form__preview form__preview_empty file-upload']/label/input[@type='file']"
        FORM_CHECKBOX_ADDRESS = "//span[@class='form__check form__check_button-light']"
        CLICK_GENDER = "//input[@name='userGender' and %s]"
        GENDER_CHECKED = "@checked]/..//span[contains(.,'%s')"
        GENDER_UNCHECKED = "not(@checked)]/..//span[contains(.,'%s')"
        SAVE_BUTTON = "//span[contains(.,'Сохранить')]"
        #TODO: Изменения для новых настроек профиля
        CHECKED_GENDER = "//span[@class='radio-set__area']/input[@name='userGender' and @checked]/../" \
                         "label[@class='radio-set__button' and contains(.,'%s')]"
        UNCHECKED_GENDER = "//span[@class='radio-set__area']/input[@name='userGender' and not(@checked)]/../" \
                           "label[@class='radio-set__button']"
        BTN_SAVE = "//button[contains(.,'Сохранить')]"

        CHECKBOX_SOVPADAET = "//span/input[@id='sovpadaet' %s]/../label[contains(.,'Совпадает с юридическим')]"

        CHECKBOX_CASH = "//div[@class='form__row form__row_switcher']//span[contains(.,'Наличными')]/..//input[@id=" \
                        "'payment1' and @type='checkbox' %s]/../label"
        CHECKBOX_CASH_ON_DELIVERY = "//div[@class='form__row form__row_switcher']//span[contains(.,'Наложенным " \
                                    "платежом')]/..//input[@id='payment2' and @type='checkbox' %s]/../label"
        CHECKBOX_BANK_ACCOUNT = "//div[@class='form__row form__row_switcher']//span[contains(.,'По счету через банк')]" \
                                "/..//input[@id='payment3' and @type='checkbox' %s]/../label"
        CHECKBOX_CARD = "//div[@class='form__row form__row_switcher']//span[contains(.,'Переводом на карту банка:')]" \
                        "/..//input[@id='payment4' and @type='checkbox' %s]/../label"
        CHECKBOX_E_MONEY = "//div[@class='form__row form__row_switcher']//span[contains(.,'Картой или электронными " \
                           "деньгами:')]/..//input[@id='payment5' and @type='checkbox' %s]/../label"

        CHECKBOX_TRANSPORT_COMPANY = "//div[@class='form__row form__row_switcher']//span[contains(.,'Транспортными " \
                                     "компаниями:')]/..//input[@id='delivery1' and @type='checkbox' %s]/../label"
        CHECKBOX_COURIER = "//div[@class='form__row form__row_switcher']//span[contains(.,'Курьером по городу:')]" \
                           "/..//input[@id='delivery2' and @type='checkbox' %s]/../label"
        CHECKBOX_OWN_DEL_SERVICE = "//div[@class='form__row form__row_switcher']//span[contains(.,'Собственная служба " \
                                   "доставки')]/..//input[@id='delivery3' and @type='checkbox' %s]/../label"
        CHECKBOX_RUSSIAN_MAIL = "//div[@class='form__row form__row_switcher']//span[contains(.,'Почта России')]/..//" \
                                "input[@id='delivery4' and @type='checkbox' %s]/../label"
        CHECKBOX_PICKUP = "//div[@class='form__row form__row_switcher']//span[contains(.,'Самовывоз:')]/..//" \
                          "input[@id='delivery5' and @type='checkbox' %s]/../label"



    class Input():
        LIST_VALUE_OR_NOT_VALUE = {True: "@value='%s'", False: "not(@value='%s')"}
        FORM_DISPLAY_NAME = "//label/span[contains(.,'Имя')]/../input[@class='form__input' and @maxlength=200 and %s]"
        FORM_EMAIL = "//label/span[contains(.,'Эл. почта:')]/../input[@class='form__input' and %s]"
        EMAIL_ABSTRACT = "//label/span[contains(.,'Эл. почта:')]/../input[@class='form__input']"

        FORM_SHOP_NAME = "//label/span[contains(.,'Наименование компании:')]/../input[@class='form__input' and " \
                         "@maxlength=200 and %s]"
        FORM_SHOP_DESCRIPTION = "//label/span[contains(.,'Описание')]/..//textarea[@class='form__textarea_company' " \
                                "and @maxlength=200 and contains(.,'%s')]"
        FORM_SHOP_ADDRESS = "//label/span[contains(.,'Адрес магазина')]/..//input[@class='form__input' " \
                            " and @maxlength=200 and %s]"

        FORM_FULL_LEGAL_NAME = "//label/span[contains(.,'Полное наименование юр.')]/../input[@class='form__input' and %s]"
        FORM_INN = "//label/span[contains(.,'ИНН')]/../input[@class='form__input' and @maxlength='12' and %s]"
        FORM_KPP = "//label/span[contains(.,'КПП')]/../input[@class='form__input' and @maxlength='9' and %s]"
        FORM_OGRN = "//label/span[contains(.,'ОГРН')]/../input[@class='form__input' and @maxlength='13' and %s]"
        FORM_LEGAL_ADDRESS = "//label/span[contains(.,'Юридический адрес')]/../input[@class='form__input' and %s]"
        FORM_ACTUAL_ADDRESS = "//label/span[contains(.,'Фактический адрес')]/../input[@class='form__input' and %s]"

        FORM_BANK_BIC = "//label/span[contains(.,'БИК')]/../input[@class='form__input' and @maxlength='9' and %s]"
        FORM_BANK_NAME_AND_ADDRESS = "//label/span[contains(.,'Наименование и местоположение банка')]/../" \
                                     "input[@class='form__input' and %s]"
        FORM_BANK_ACCOUNT = "//label/span[contains(.,'Номер счета')]/../input[@class='form__input' and " \
                            "@maxlength='20' and %s]"
        FORM_BANK_CORR_ACCOUNT = "//label/span[contains(.,'Корреспондентский счет')]/../input[@class='form__input' " \
                                 "and @maxlength='20' and %s]"

        FORM_PASSWD_OLD = "//label/span[contains(.,'Текущий пароль')]/../input[@class='form__input' and @maxlength=200]"
        FORM_PASSWD_NEW = "//label/span[contains(.,'Новый пароль')]/../input[@class='form__input' and @maxlength=200]"
        FORM_PASSWD_NEW_REPEAT = "//label/span[contains(.,'Повторите пароль')]/../input[@class='form__input'" \
                                 " and @maxlength=200]"
        #TODO: Изменения для новых настроек профиля
        INPUT_NAME = "//label/span[contains(.,'Имя:')]/../input[@maxlength='200' and @value%s and not(@disabled)]"
        INPUT_PHONE = "//label/span[contains(.,'Телефон:')]/../input[@type='tel' and @value%s and @disabled]"
        INPUT_EMAIL = "//label/span[contains(.,'Эл. почта:')]/../input[@maxlength='50' and @disabled %s]"

        INPUT_PASSWORD = "//label/span[contains(.,'Текущий пароль:')]/..//input[@type='password' and @maxlength='100']"
        INPUT_N_PASSWORD = "//label/span[contains(.,'Новый пароль:')]/..//input[@type='password' and @maxlength='100']"
        INPUT_R_PASSWORD = "//label/span[contains(.,'Повторите пароль:')]/..//input[@type='password' and @maxlength='100']"

        INPUT_STORE_NAME = "//label/span[contains(.,'Наименование компании:')]/../input[@maxlength='200' %s]"
        INPUT_STORE_ADDRESS = "//label/span[contains(.,'Адрес магазина:')]/../input[@maxlength='200' %s]"
        INPUT_DESCRIPTION = "//label/span[contains(.,'Описание:')]/..//textarea[@maxlength='200' %s]"

        INPUT_LEGAL_NAME = "//label/span[contains(.,'Полное наименование юр.')]/../input[@class='form__input' %s]"
        INPUT_INN = "//label/span[contains(.,'ИНН:10-12 символов')]/../input[@maxlength=12 %s]"
        INPUT_KPP = "//label/span[contains(.,'КПП:9 символов')]/../input[@maxlength=9 %s]"
        INPUT_OGRN = "//label/span[contains(.,'ОГРН:13 символов')]/../input[@maxlength=13 %s]"
        INPUT_LEGAL_ADDRESS = "//label/span[contains(.,'Юридический адрес:')]/../input[@class='form__input' %s]"
        INPUT_REAL_ADDRESS = "//label/span[contains(.,'Фактический адрес:')]/../input[@class='form__input' %s]"
        INPUT_BIK = "//label/span[contains(.,'БИК:9 символов')]/../input[@maxlength=9 %s]"
        INPUT_NAME_BANK = "//label/span[contains(.,'Наименование и местоположение банка:')]/../" \
                          "input[@class='form__input' %s]"
        INPUT_ACCOUNT = "//label/span[contains(.,'Номер счета:20 символов')]/../input[@maxlength=20 %s]"
        INPUT_CORRESPONDENT = "//label/span[contains(.,'Корреспондентский счет:20 символов')]/../" \
                              "input[@maxlength=20 %s]"

        INPUT_PAY_CARD = "//div[@class='form__row form__row_switcher']//span[contains(.,'Переводом на карту банка:')]" \
                         "/..//textarea[@maxlength='500' and @placeholder='Альфа-Банк, Сбербанк и т.д.' %s]"
        INPUT_E_MONEY = "//div[@class='form__row form__row_switcher']//span[contains(.,'Картой или электронными " \
                        "деньгами:')]/..//textarea[@maxlength='500' and @placeholder='Укажите данные карты или " \
                        "эл. кошелька' %s]"

        INPUT_TK = "//div[@class='form__row form__row_switcher']//span[contains(.,'Транспортными компаниями:')]/..//" \
                   "textarea[@maxlength='500' and @placeholder='DPD Classic, ПЭК Авто, СДЕК Экспресс лайт и т.д.' %s]"
        INPUT_COURIER = "//div[@class='form__row form__row_switcher']//span[contains(.,'Курьером по городу:')]/..//" \
                        "textarea[@maxlength='500' and @placeholder='Москва, Пенза и т.д.' %s]"
        INPUT_PICKUP = "//div[@class='form__row form__row_switcher']//span[contains(.,'Самовывоз:')]" \
                       "/..//textarea[@maxlength='500' and @placeholder='Город и адрес где забрать товар' %s]"


class MainPage(MainClass):

    class Path():
        TO_FIND_GOODS = '<a class="lot__link" href="/goods/'

        HTML_NEW_GOODS = '<a class="title__link" href="/catalog/new"'
        HTML_POPULAR_GOODS = '<a class="title__link" href="/catalog/225"'
        HTML_LAST_DEALS = '<a class="title__link" href="/catalog/deals"'
        HTML_GOODS_FROM_BEST_SELLERS = '<a class="title__link" href="/catalog/226"'

        # изменения build 14.05.2015
        #FIRST_GROUP_GOODS = "//div[@class='catalog catalog_index'][1]"
        FIRST_GROUP_GOODS = "//div[@class='catalog__list catalog__list_index'][1]"



        BLOCK_LAST_DEALS = "//div[@class='catalog']/div[@class='catalog__title']/a[contains(.,'Последние сделки')]/../../" \
                           "div[@class='catalog__list catalog__list_index']"

        BLOCK_GOOD_BEST_SELLERS = "//div[@class='catalog']/div[@class='catalog__title']/a[contains(.,'" \
                                  "Товары от лучших продавцов')]/../../div[@class='catalog__list catalog__list_index']"

        # блок одежды, название n-ого товара в нём
        BLOCK_CLOTHING = "//div[2]/div[@class='catalog catalog_index  catalog_side-banner'][1]" \
                         "/div[@class='catalog__list catalog__list_index']/div[@class='lot lot_with-store'][%s]" \
                         "/a[@class='lot__item']/div[@class='lot__name']"

        BLOCK_NEW_GOOD = "//div[@class='catalog']/div[@class='catalog__title']/a[contains(.,'Новинки')]/../../" \
                         "div[@class='catalog__list catalog__list_index']"

        BLOCK_POPULAR_GOOD = "//div[@class='catalog']/div[@class='catalog__title']/a[contains(.,'Популярные товары')]/../" \
                             "../div[@class='catalog__list catalog__list_index']"

        URL_LOGO_GRAY = "/images/logo-gray.ru.94637f944366534201b0.png"
        XPATH_LOGO = "/html/body/img[@src='%s']"

        PATH_ALL_FINAL_CATEGORY = "/../..//ul[@class='cat__catlist']/li[@class]/a[contains(.,'')]"
        PATH_FINAL_CATEGORY = "/../..//ul[@class='cat__catlist']/li/a[contains(.,'%s')]"

        PATH_USER_LOT = "//div[%s]/a[@class='lot__user']"
        WIDGET_USER = "//div[contains(@class,'header__user')]"

    class Check():
        PROGRESS_BAR = "//div[@id='nprogress']"
        ON_BOARDING_MSG_REG = "//div[@class='hint__message' and contains(.,'РегистрацияЧтобы использовать все " \
                              "возможности сайта, пройдите простую регистрацию')]"
        ON_BOARDING_MSG_LANG = "//div[@class='hint__message' and contains(.,'Выбор языкаВыберите удобный вам язык')]"
        #FC ~ FOOTER COPYRIGHT
        FC_COPYRIGHT_TEXT = "2014 - 2015 © OORRAA.com Все права защищены"
        FC_COPYRIGHT = "//div[@class = 'footer__copy']/span"
        CHECK_MENU_USER = "//div[@class='header__info']"


        USER_NAME_LOT = "//div[@class='user__name' and contains(.,'%s')]"
        USER_PHOTO = "//img[@class='user__photo' and contains(@src,'%s_s100x100')]"

        WU_AVATAR = "//img[@class='header__avatar' and contains(@src,'%s')]"
        WU_NAME = "//span[@class='header__name' and contains(.,'%s')]"
        WU_MY_SHOP = "//a[contains(@href,'/store/%s')]/span[contains(.,'Мой магазин')]/.."

        MAIN_MENU_SECTION_ABSTRACT = "//div[@class='header__nav-items']/div[contains(@class,'header__nav-item')]"
        MAIN_MENU_CATEGORY_ABSTRACT = "//div[@class='header__nav-menu-side']/div[contains(@class,'header__nav-menu-label')]"
        MAIN_MENU_SUB_CATEGORY = "//div[@class='header__nav-menu-main']"

        MAIN_MENU_SUB_CATEGORY_ABSTRACT = "//div[@class='header__nav-menu-main']//a[@class='header__nav-menu-subcat']"
        MAIN_MENU_SECTION_MENU = "//div[contains(@class,'header__nav-item header__nav-item_menu') and contains(.,'%s')]"
        MAIN_MENU_CATEGORY_MENU = "//div[@class='header__nav-menu-label header__nav-menu-label_active' and contains(.,'%s')]"
        SECTION_MENU = "//div[@class='header__nav-menu']"
        MAIN_MENU_HOME_ACTIVE = "//a[@class='header__nav-home active' and @href='/']/i"
        MAIN_MENU_SECTION_ACTIVE = "//div[@class='header__nav-item header__nav-item_active' and contains(.,'%s')]"
        MAIN_MENU = "//nav[@class='header__nav']"

        ABSTRACT_MSG = "//a[contains(@href,'/user/chats')]"
        COUNT_NEW_MSG = ABSTRACT_MSG + "//b[@class='header__count note-counter note-counter_unread' and text()=%s]"
        ALL_NUMERATE_MSG = ABSTRACT_MSG + "//b[@class='header__count note-counter note-counter_unread']"
        COUNTER_MSG_USER = "//div/a[@class='contact-list__item'][%s]/span[@class='note-counter note-counter_unread']"

        AREA_FOR_SEND_MSG = "//textarea[@class='publisher__textarea']"

        TEXT_WARES_ON_MAIN = '//li[@class="banner-stat__item banner-stat__item_goods"]//div[@class="banner-stat__info"]'
        TEXT_USERS_ON_MAIN = '//li[@class="banner-stat__item banner-stat__item_buyer"]//div[@class="banner-stat__info"]'

    class Click():

        HEADER_CONTACTS = "//a[contains(@href,'/user/contacts') and contains(.,'Контакты')]"

        LANGUAGE_BTN = "//div[@class='lang-selector__link' and contains(.,'%s')]"
        ON_BOARDING_REGISTRATION = "//div[@class='hint hint_reg']/div[@class='hint__button']"
        ON_BOARDING_LANGUAGE = "//div[@class='hint hint_lang']/div[@class='hint__button']"
        BTN_SEARCH = "//button[@class='search__submit']"
        LINK_SELLER_AVATAR = "/../a[contains(@href,'/store/%s')]"

        BUTTON_LOGIN = "//a[contains(@href,'/login') and contains(.,'Вход')]"
        BUTTON_REG_AN_LOGIN = "//a[contains(.,'Регистрация и вход')]"   # было вместо a -> button
        BUTTON_REG_AND_LOGIN = "//a[contains(.,'Регистрация и вход')]"
        BTN_LOGIN = "//a[@class='header__auth-button button button_primary button_icon']"

        REGISTRATION_PAGE2 = "//a[contains(@href,'/registration')]/b[contains(.,'Регистрация')]"
        HEADER_WIDGET_CHATS = "//a[contains(@href,'/user/chats') and contains(.,'Сообщения')]"
        HEADER_FAVORITES = "//a[contains(@href,'/user/favorites')]//span[contains(.,'Избранное')]"
        HEADER_MY_SHOP = "//span[contains(.,'Мой магазин')]"
        HEADER_MY_GOODS = "//a[contains(@href,'/user/goods/active/1')]//span[contains(.,'Мои товары')]"
        HEADER_LANG_SELECTOR = "//div[@class='lang-selector']/ul[@class='lang-selector__list']" \
                               "/li[@class='lang-selector__list-item lang-selector__list-item_active']" \
                               "/div[@class='lang-selector__link']"
        USER_MENU = "//div[contains(@class,'header__user')]/div[@class='header__info']"
        MENU = "//div[contains(@class,'header__user')]"
        MENU_MY_SHOP = "//a[contains(@href,'/store/%s')]/span[contains(.,'Мой магазин')]"
        MENU_PROFILE_NAME = MENU + "//span[@class='header__name' and contains(.,'%s')]"
        MENU_PROFILE_AVATAR = MENU + "//img[@class='header__avatar' and contains(@src,'%s')]"
        MENU_PROFILE_MY_STORE = MENU + "//a[contains(@href,'/store/manage')]/span[contains(.,'Мой магазин')]"
        MENU_PROFILE_FAVORITES = MENU + "//a[contains(@href,'/user/favorites')]//span[contains(.,'Избранное')]"
        MENU_PROFILE_CONTACTS = MENU + "//a[contains(@href,'/user/contacts') and contains(.,'Контакты')]"
        MENU_PROFILE_SETTINGS = MENU + "//a[contains(@href,'/user/settings/profile')]/span[contains(.,'Настройки')]"
        MENU_PROFILE_EXIT = MENU + "//span[@class='header__action header__action_exit' and contains(.,'Выход')]"


        MAIN_BANNER = "//a[@class='promo__slide slick-slide slick-active']"

        #MBV ~ MAIN BANNER VISITOR
        MBV_VIDEO = "//div[@class='promo__nav']//span[contains(.,'Видеоролик о компании')]"
        MBV_START_SALE = "//div[@class='promo__nav']//span[contains(.,'Начни')]"
        MBV_HOW_JOB = "//div[@class='promo__nav']//span[contains(.,'Как работать')]"

        MBV_NEW_GARMENT = "//div[@class='promo__nav']//span[contains(.,'Новинки верхней одежды')]"
        MBV_FOR_CHILD = "//div[@class='promo__nav']//span[contains(.,'Заказать товары для детей')]"
        MBV_NEW_FOOTWEAR = "//div[@class='promo__nav']//span[contains(.,'Новое поступление демисезонной обуви')]"

        #MBB ~ MAIN BANNER BUYER
        MBB_COLLECTION = "//div[@class='promo__nav']//span[contains(.,'Коллекции')]"

        #MBS ~ MAIN BANNER SELLER
        MBS_ADD_GOOD = "//div[@class='promo__nav']//span[contains(.,'Размещайте')]"
        MBS_CREATE_SITE = "//div[@class='promo__nav']//span[contains(.,'Создай свой')]"

        # CM ~ CATEGORY MAIN
        CM_GARMENT = "//h3[@class='cat__name']/span[contains(.,'Одежда')]"
        CM_SHOES = "//h3[@class='cat__name']/span[contains(.,'Обувь')]"
        CM_UNDERWEAR = "//h3[@class='cat__name']/span[contains(.,'Белье')]"
        CM_ACCESSORY = "//h3[@class='cat__name']/span[contains(.,'Аксессуары')]"
        CM_TEXTILE = "//h3[@class='cat__name']/span[contains(.,'Домашний текстиль')]"
        CM_CHILD = "//h3[@class='cat__name']/span[contains(.,'Детские товары')]"

        # TB ~ TITLE BLOCK
        TB_LAST_DEALS = "//a[contains(@href,'/catalog/deals') and contains(.,'Последние сделки')]"
        TB_GOODS_BEST_SELLERS = "//a[contains(.,'Товары от лучших продавцов')]"
        TB_NEW_GOODS = "//a[contains(@href,'/catalog/new') and contains(.,'Новинки')]"
        TB_POPULAR_GOODS = "//a[contains(.,'Популярные товары')]"

        # BR ~ BANNER RIGHT
        BR_SUBSCRIBE = "//a[@class='banner banner_wide_v']/img[@class='banner__img' and @alt='Подпишись']"
        BR_START_SELL = "//a[@class='banner banner_wide_v']/img[@class='banner__img' and @alt='Начни торговать']"
        BR_IN_CENTER = "//a[@class='banner banner_wide_v']/img[@class='banner__img' and @alt='Будь на виду']"
        BR_FAVORITES = "//a[@class='banner banner_wide_v']/img[@class='banner__img' and @alt='Избранное']"
        BR_TAKE_SELLER = "//a[@class='banner banner_wide_v']/img[@class='banner__img' and @alt='Стань продавцом']"
        BR_SOME_STORE = "//a[@class='banner banner_wide_v']/img[@class='banner__img' and @alt='Женские платья, " \
                        "сумки, туфли']"
        BR_TRADE_ALL = "//a[@class='banner banner_wide_v']/img[@class='banner__img' and " \
                       "@alt='Торгуй везде с мобильным приложением УУРРАА']"
        BR_SELL_ALL = "//a[@class='banner banner_wide_v']/img[@class='banner__img' and @alt='Торгуй везде!']"

        # BW - BANNER WIDTH
        BW_MAN_ACCESS = "//a[@class='banner banner_wide_h' and contains(@href,'116')]/img"
        BW_CATALOG_DRESS = "//a[@class='banner banner_wide_h' and contains(@href,'/catalog/29')]/img"
        BW_AUTUMN = "//a[@class='banner banner_wide_h' and contains(@href,'/catalog/20')]/img"
        BW_TEXTILE = "//a[@class='banner banner_wide_h' and contains(@href,'/catalog/147')]/img"

        # FB ~ FOOTER BUTTON
        FB_TEXTILE = "//li[@class='footer__item']/a[contains(.,'Домашний текстиль')]"
        FB_CATALOG = "//a/span[contains(., 'Каталог')]"
        FB_GARMENT = "//a[@class='footer__cat' and contains(.,'Одежда')]"
        FB_SHOES_AND_ACCESSORY = "//a[@class='footer__cat' and contains(.,'Обувь и аксессуары']"
        FB_CHILD = "//a[@class='footer__cat' and contains(.,'Товары для детей')]"
        FB_HOUSE = "//a[@class='footer__cat' and contains(., 'Товары для дома')]"
        FB_GARDEN = "//a[@class='footer__cat' and contains(., 'Товары для сада')]"
        FB_TRADE_EQUIPMENT = "//a[@class='footer__cat' and contains(., 'Торговое оборудование')]"
        FB_ABOUT_COMPANY = "//a[@class='footer__cat' and contains(.,'О компании')]"
        FB_CONTACTS = "//a[@class='footer__cat' and contains(.,'Контакты')]"
        FB_JOB = "//a[@class='footer__cat' and contains(.,'Вакансии')]"
        FB_FAQ = "//a[@class='footer__cat' and contains(.,'Вопросы и ответы')]"
        FB_RULES = "//a[@class='footer__cat' and contains(.,'Правила УУРРАА')]"
        FB_CONFIDENTIAL = "//a[@class='footer__cat' and contains(.,'Политика конфиденциальности')]"
        FB_DELIVERY = "//a[@class='footer__cat' and contains(.,'Калькулятор доставки')]"
        FB_PAYMENTS = "//a[@class='footer__cat' and contains(., 'УУРРАА Касса')]"

        #FC ~ FOOTER COPYRIGHT
        FC_LOGO = "//a[@class = 'footer__logo']"

        PATH_GOOD = "//div[@class='lot lot_with-store'][%s]/a[@class='lot__item']/div[@class='lot__name']"
        PATH_GOOD_INFO = "/div[%s]/a[@class='lot__link']"
        PATH_NAME_BS = "/div[%s]//div[@class='user__name']"
        SEARCH_BTN = "//button[contains(@title,'Поиск')]"

        MAIN_MENU_SECTION = "//div[@class='header__nav-item' and contains(.,'%s')]"
        MAIN_MENU_CATEGORY = "//div[contains(@class,'header__nav-menu-label') and contains(.,'%s')]"
        MAIN_MENU_CATEGORY_ICON = "//div[contains(@class,'header__nav-menu-label') and contains(.,'%s')]/i"
        MAIN_MENU_SUB_CATEGORY_BY_NAME = "//div[@class='header__nav-menu-main']//a[contains(.,'%s')]"

        MAIN_MENU_HOME = "//a[@class='header__nav-home' and @href='/']/i"
        ALL_CATEGORIES = "//div[@class='header__nav-menu']//a[contains(.,'Все категории')]"
        ALL_SUB_CATEGORIES = "//div[@class='header__nav-menu']//a[contains(.,'Все подкатегории')]"

    class Input():
        SEARCH = "//input[@class='search__input' and @type='search' and @maxlength=100 and @placeholder='Я ищу...']"


class AuthorizationPage(MainClass):

    class Path():
        PATH_AUTH = "/login"

    class Check():
        # изменения, build 14.05.2015 TODO: удалить
        TITLE_AUTH_PAGE = "//div[@class='registration']//span[contains(.,'Вход')]"

        HEADER = "//header[@class='header']"                                    # проверка header.
        LOGO = "//a[@class='header__logo header__cell' and @href='/']"               # проверка логотипа.

        # проверка формы авторизации, объеденена с формой регистрации (build 14.05.2015)
        #FORM_AUTH = "//fieldset[@class='form__fieldset']"
        FORM_AUTH = "//div[@class='registration']"

        # проверка формы Моб.телефон, авторизация объеденена с формой регистрации (build 14.05.2015)
        #FORM_PHONE = "//span[@class='form__text' and contains(.,'Мобильный телефон:')]"
        FORM_PHONE = "//span[contains(.,'Телефон или почта:')]"

        FORM_PASS = "//span[contains(.,'Пароль')]"                                      # проверка формы Пароль

        # проверка кнопки Забыли пароль, авторизация объеденена с формой регистрации (build 14.05.2015)
        #BTN_RESTORE = "//a[@href='/restore']"
        BTN_RESTORE = "//span[contains(.,'Забыли пароль?')]"

        # блок справа "Впервые на УУРРАА? Регистрация", убран - авторизация объеденена с регистрацией (build 14.05.2015)
        # BLC_RIGHT = "//div[@class='sidebar__reg sidebar__reg_auth']"
        # TITLE_RIGHT = "//h2/span[contains(.,'Первый раз на УУРРАА?')]"     # проверка загловка 'Впервые на УУРРАА?'
        # TITLE_BLC = "//div[@class='sidebar__reg-cover sidebar__reg-cover_auth']"   # загловк 'Впервые на УУРРАА?'

        # # проверка кнопки Регистрация, авторизация объеденена с формой регистрации (build 14.05.2015)
        #BTN_REGISTRATION = "//a[@href='/registration']/span[contains(.,'Регистрация')]"
        BTN_REGISTRATION = "//a[contains(@href,'/registration')]"

        FOOTER = "//footer[@class='footer']"                                       # проверка подвала
        INPUT_PHONE = "//input[@name='phoneOrEmail']"
        INPUT_PASS = "//input[@name='password']"
        BTN_LOGIN = "//button[@type='submit']"                                     # проверка кнопки Войти

        # Изменения от 25.05.2015 Новые xpath
        TAB_LOGIN_ACTIVE = "//div[contains(@class,'registration__tab-item_active') and contains(.,'Вход')]"
        LABEL_EMAIL = "//label/span[contains(.,'Телефон или почта:')]"
        LABEL_PASSWORD = "//label/span[contains(.,'Пароль:')]"

        ERR_CHECK_EMAIL_AND_PASS = "//label/input[@name='phoneOrEmail']/..//span[@class='form__error' and " \
                                   "contains(.,'Проверьте правильность ввода email и пароля')]"
        ERR_CHECK_DISABLED = "//h2[@class='disabled-user__title' and contains(.,'Ваш аккаунт заблокирован')]"
        ERR_INPUT_PASS = "//label/input[@name='password']/..//span[@class='form__error' and " \
                         "contains(.,'Введите пароль')]"
        ERR_INPUT_EMAIL = "//label/input[@name='phoneOrEmail']/..//span[@class='form__error' and " \
                          "contains(.,'Введите email')]"
        ERR_EMPTY_EMAIL_OR_PHONE = "//label/input[@name='phoneOrEmail']/..//span[@class='form__error' and " \
                                   "contains(.,'Введите телефон или email')]"
        ERR_CHECK_EMAIL = "//label/input[@name='phoneOrEmail']/..//span[@class='form__error' and " \
                          "contains(.,'Проверьте правильность ввода email и пароля')]"

    class Click():
        TAB_REG = "//a[@href='/registration' and contains(.,'Регистрация')]"
        BTN_PHONE = "//label[@class='radio-set__button' and contains(.,'Мобильный телефон')]"  # кнопка перехода, авторизации по телефону
        BTN_EMAIL = ".//*[@id='app']/div/div[2]/div/section/div/div[2]/span[2]/label/span/span"   # кнопка перехода, авторизации по e-mail
        SWITCH_EMAIL = "//label[@for='rs_loginWith_email' and contains(.,'Эл. почта')]"
        SWITCH_PHONE = "//label[@for='rs_loginWith_phone' and contains(.,'Мобильный телефон')]"
        BTN_LOGIN = "//button[contains(.,'Войти')]"

        BTN_RESTORE = "//a[@href='/restore/email' and contains(.,'Забыли пароль?')]"
        BACK_TO_MAIN = "//a[@class='header__back-link' and contains(.,'На главную')]"

    class Input():
        INPUT_EMAIL = "//input[@name='phoneOrEmail']"
        INPUT_PASSWORD = "//input[@name='password']"


class RestorePage(MainClass):

    class Path():
        URL_RESTORE_PHONE = "/restore/phone"
        URL_RESTORE_EMAIL = "/restore/email"

    class Check():

        #  build 14.05.2015
        #TITLE_RESTORE_PAGE = "//h1[@class='title__name' and contains(.,'Забыли пароль?')]"
        TITLE_RESTORE_PAGE = "//h2[contains(.,'Восстановление пароля')]"
        TITLE_INPUT_PASS_PAGE = "//h2[contains(.,'Установить новый пароль')]"

        HEADER = "//header[@class='header']"                                    # проверка header.
        LOGO = "//a[@class='header__logo header__cell' and @href='/']"               # проверка логотипа.

        # проверка формы "забыли пароль", build 14.05.2015
        #FORM_RESTORE = "//fieldset[@class='form__fieldset']"
        FORM_RESTORE = "//section[contains(@class,'recovery')]"

        FORM_PHONE = "//span[@class='form__text' and contains(.,'Мобильный телефон:')]"  # проверка формы Моб.телефон
        LABEL_EMAIL = "//span[@class='form__text' and contains(.,'Эл. почта:')]"  # проверка формы Моб.телефон
        LABEL_EMAIL_INCORRECT = "//span[@class='form__text' and contains(.,'settings')]"

        #BLC_RIGHT = "//div[@class='sidebar__reg sidebar__reg_auth']"  # блок справа "Впервые на УУРРАА? Регистрация"
        #TITLE_RIGHT = "//h2/span[contains(.,'Первый раз на УУРРАА?')]"     # проверка загловка 'Впервые на УУРРАА?'
        #TITLE_BLC = "//div[@class='sidebar__reg-cover sidebar__reg-cover_auth']"   # загловк 'Впервые на УУРРАА?'

        BTN_REGISTRATION = "//a[contains(@href,'/registration')]/span[contains(.,'Регистрация')]"   # проверка кнопки Регистрация
        FOOTER = "//footer[@class='footer']"                                    # проверка подвала
        INPUT_PHONE = "//input[@name='phone' and @placeholder='(800) 000-00-00']"
        BTN_RESTORE = "//button/span[contains(.,'Выслать пароль')]"                             # проверка кнопки Войти

        # изменения билд 14.05.2015
        #RESTORE_PAGE = "//a[@href='/restore']"
        RESTORE_PAGE = "//a[contains(@href,'/restore/email')]"

        # изменения билд 14.05.2015 todo: проверить смысл ссылки
        #RESTORE_PAGE_FORM_AUTH = "//form[@class='form form_auth']"
        RESTORE_PAGE_FORM_AUTH = "//section[contains(@class,'recovery')]"

        TEXT_SENT_TO_EMAIL = "//p[@class='registration__text' and contains(.,'На ваш электронный ящик было выслано " \
                             "письмо с ссылкой на сброс пароля.')]"
        INPUT_EMAIL_HOLD = "//input[@class='form__input' and @value='%s' and @disabled]"
        LABEL_PASSWORD = "//label/span[@class='form__label' and contains(.,'Новый пароль:')]"
        LABEL_R_PASSWORD = "//label/span[@class='form__label' and contains(.,'Повторите пароль:')]"
        TEXT_NEW_PASS_SET = "//p[@class='registration__text' and contains(.,'Новый пароль установлен')]"
        ERR_PHONE_OR_PASS = "//div[contains(@class,'notification notification_error') and " \
                            "contains(.,'Проверьте правильность ввода номера телефона и пароля')]"
        ERR_EMAIL_OR_PASS = "//div[contains(@class,'notification notification_error') and " \
                            "contains(.,'Проверьте правильность ввода емайл и пароля')]"
        ERR_NEED_PHONE = "//span[@class='form__error' and contains(.,'Введите телефон')]"

        ERR_VALIDATE_URL = "//div[@class='registration__text-wrap']/p[@class='registration__text' and " \
                           "contains(.,'Истек срок действия активационной ссылки, повторите активацию еще раз')]"
        E_EMAIL_EMPTY = "//label[contains(.,'Эл. почта:')]/span[@class='form__error' and contains(.,'Введите e-mail')]"

    class Click():
        BTN_RESTORE = "//button[contains(.,'Выслать пароль')]"
        BTN_TO_MAIN = "//section//a[@href='/' and contains(.,'На главную')]"
        BTN_SET_PASS = "//button[contains(.,'Установить новый пароль')]"
        BTN_START_WORK = "//button[contains(.,'Начать работу')]"

    class Input():
        INPUT_EMAIL = "//input[@name='email']"
        INPUT_PASSWORD = "//label[contains(.,'Новый пароль:')]/input[@name='password']"
        INPUT_R_PASSWORD = "//label[contains(.,'Повторите пароль:')]/input[@name='password']"


class RegistrationPage(MainClass):
    class Path():
        URL_REG = "/registration"
        URL_REG_SWITCH = "/registration"
        URL_VALIDATED_EMAIL = "/activation/success"

    class Check():
        TITLE_REGISTRATION_PAGE = "//h1[@class='title__name' and contains(.,'Создайте свой аккаунт на УУРРАА')]"
        TAB_REG_ACTIVE = "//div[contains(@class,'registration__tab-item_active') and contains(.,'Регистрация')]"
        LABEL_NAME = "//label/span[contains(.,'Ваше имя:')]"
        LABEL_EMAIL = "//label/span[contains(.,'Эл. почта:')]"
        LABEL_PASSWORD = "//label/span[contains(.,'Пароль:')]"
        RULES = "//p[@class='registration__text']/span[contains(.,'Нажимая кнопку \"Зарегистрироваться\", " \
                "вы подтверждаете свое согласие с условиями предоставления услуг (')]/a[contains(@href,'/rules') " \
                "and contains(.,'Пользовательское соглашение')]"

        E_TITLE_REG_SUCCESS = "//h2[@class='registration__title' and contains(.,'Спасибо за регистрацию')]"
        E_ICON_REG_SUCCESS = "//i[@class='i i_registration-lg']"
        E_ICON_ACTIVATE_SUCCESS = "//i[@class='registration__success-icon']"
        E_TEXT_REG_SUCCESS = "//div[@class='registration__text-wrap' and contains(.,'На ваш электронный ящик %s" \
                             "выслано письмо с подтверждением вашего аккаунта.Перейдите в почту для подтверждения " \
                             "адреса')]"

        E_TITLE_VALIDATED = "//h2[@class='registration__title' and contains(.,'Активация аккаунта')]"
        E_TEXT_VALIDATED_SUCCESS = "//div[@class='registration__text-wrap' " \
                                   "and contains(.,'Спасибо, что прошли по активационной ссылке. Теперь вы можете " \
                                   "начать работу в системе')]"
        E_ALREADY_REG_EMAIL = "//label[contains(.,'Эл. почта:')]/span[@class='form__error' and contains(.,'" \
                              "Пользователь с указанными данными уже зарегистрирован')]"

        E_NAME_EMPTY = "//label[contains(.,'Ваше имя:')]/span[@class='form__error' and contains(.,'Введите имя')]"
        E_EMAIL_EMPTY = "//label[contains(.,'Эл. почта:')]/span[@class='form__error' and contains(.,'Введите e-mail')]"
        E_PASSWORD_EMPTY = "//label[contains(.,'Пароль:')]/span[@class='form__error' and contains(.,'Введите пароль')]"

    class Click():
        TAB_LOGIN = "//a[contains(@href,'/login') and contains(.,'Вход')]"
        SWITCH_EMAIL = "//label[@for='rs_regType_email' and contains(.,'Эл. почта')]"
        SWITCH_PHONE = "//label[@for='rs_regType_phone' and contains(.,'Мобильный телефон')]"
        BTN_REG = "//button[contains(.,'Зарегистрироваться')]"
        BACK_TO_MAIN = "//a[@class='header__back-link' and contains(.,'На главную')]"

        BTN_OK = "//button[contains(.,'OK')]"
        BTN_CREATE_ACCOUNT = "//button[contains(.,'Создать аккаунт')]"

        E_BTN_START_WORK = "//button[contains(.,'Начать работу')]"
        E_BTN_START_WORK_AFTER_SUCCESS = "//a[contains(.,'Начать работу')]"
        LINK_RULES = "//a[@class='registration__link' and contains(@href,'rules') and " \
                     "contains(.,'Пользовательское соглашение')]"

    class Input():
        E_INPUT_NAME = "//input[@name='username' and @maxlength='200']"
        E_INPUT_EMAIL = "//div[@class='form__row'][2]/label/input[@class='form__input']"
        E_INPUT_PASSWORD = "//div[@class='form__row'][3]/label/input[@class='form__input']"

        P_INPUT_PASSWORD = "//input[@name='pass' and @maxlength='5']"


class CatalogCategoryPage(MainClass):

    class Path():
        TO_FIND_GOODS = '<a class="lot__link" href="/goods/'
        CAT_PATH_FINAL_CATEG = "//h1[@class='title__name']/span[contains(.,'%s')]"
        PATH_TREE_CATEGORY = "//ul[@class='sidebar__list']/li[@class]/a"
        PATH_GOOD_IN_WIN_CATALOG = "/../..//div[@class='lot'][%s]//div[@class='lot__name']"

        URL_PATH_ROOT_CATEGORY = "/catalog/%s"
        URL_ALL_IN_CATEGORY = "/catalog/%s/all"
        URL_ALL_CATALOG = "/catalog/all"

        URL_BESTSELLERS = "/catalog/%s/bestsellers"
        URL_ALL_BESTSELLERS = "/catalog/bestsellers"


        URL_WARE_NEW = "/catalog/%s/new"
        URL_ALL_WARE_NEW = "/catalog/new"

        URL_LAST_DEALS = "/catalog/%s/deals"
        URL_ALL_LAST_DEALS = "/catalog/deals"

        URL_GOODS_FROM_BEST_SELLERS = "/catalog/226"
        URL_POPULAR_GOODS = "/catalog/225"

        START_FIND_CATEGORY = '<a class="title__link" href="/catalog/'
        END_FIND_CATEGORY = '" data-reactid="'
        HTML_CATEGORY = '<a class="title__link" href="/catalog/%s"'
        HTML_END_SECTION = '</section>'

        PATH_IMG = "//img[contains(@src,'%s')]"

    class Check():

        ON_BOARDING_MSG_CAT = "//div[@class='hint__message hint__message_right' and contains(.,'Цена и партия " \
                              "товараВ описании указана минимальная для заказа партия. Цена указана за один товар. " \
                              "Кликните на фото, чтобы узнать детали')]"
        # TCS ~ TITLE CATEGORY SPECIAL
        TCS_LAST_DEALS = "//h1[@class='title__name']/span[contains(.,'Последние сделки')]"
        TCS_GOODS_BEST_SELLERS = "//h1[@class='title__name']/span[contains(.,'Товары от лучших продавцов')]"
        TCS_NEW_GOODS = "//h1[@class='title__name']/span[contains(.,'Новинки')]"
        TCS_POPULAR_GOODS = "//h1[@class='title__name']/span[contains(.,'Популярные товары')]"

        # FC ~ FINAL CATEGORY
        FC_DRESS = "//h1[@class='title__name']/span[contains(.,'Платья')]"
        FC_JACKET = "//h1[@class='title__name']/span[contains(.,'Куртки')]"
        FC_COATS = "//h1[@class='title__name']/span[contains(.,'Пальто и плащи')]"
        FC_BAGS = "//h1[@class='title__name' and contains(.,'Сумки')]"

        TITLE_ALL_CATALOG = "//div[@class='catalog']/h1[contains(.,'Каталог товаров')]"
        ACTIVE_TREE_CATEGORY = "//ul[@class='sidebar__list']/li[@class='sidebar__item sidebar__item_active']" \
                               "/a[contains(.,'%s')]"
        ROOT_CATEGORY_ABSTRACT = "//div[@class='header__nav-item header__nav-item_active']"
        CATEGORY_ABSTRACT = "//div[@class='sidebar__title']/span[text()]"
        CATEGORY_ALL = "//div[@class='layout']//a[contains(@href,'/catalog') and contains(.,'%s')]"
        FINAL_CATEGORY_ABSTRACT = "//div[@class='catalog']//h1[@class='page-title__header']"
        ROOT_CATEGORY = "//div[@class='header__nav-item header__nav-item_active' and contains(.,'%s')]"
        CATEGORY = "//div[@class='sidebar__title']/span[contains(.,'%s')]"
        FINAL_CATEGORY_2 = "//div[@class='catalog']//h1[@class='page-title__header' and contains(.,'%s')]"
        FINAL_CATEGORY = "//div[@class='title title_catalog']/h1[@class='title__name']/span[contains(.,'%s')]/../../.." \
                         "//div[@class='catalog__list']"
        WARE_ID_ALL_CATALOG = "//a[contains(@href,'/goods/%s')]"
        PATH_WARE_IN_PAGE = "//img[contains(@alt,'%s')]"

        PARENT_CATEGORY_ABSTRACT_BY_NAME = "//div[@class='header__nav-item header__nav-item_active' and contains(.,'%s')]"
        CATEGORY_ABSTRACT_BY_NAME = "//div[contains(@class,'title') and contains(.,'%s')]"
        PARENT_CAT_IN_SUB_CAT_LISTING = "//div[@class='sidebar__title']/a[contains(.,'%s')]"

    class Click():
        ON_BOARDING_CATALOG = "//div[@class='hint hint_catalog']/div[@class='hint__button']"
        # LRC ~ LINK ROOT CATEGORY
        #LRC_GARMENT = "//div[@class='sidebar__title']/span[contains(.,'Одежда')]"
        LRC_GARMENT = "//div[@class = 'header__nav-item header__nav-item_active' and contains(., 'Одежда')]"
        LRC_SHOES = "//div[@class='sidebar__title']/span[contains(.,'Обувь')]"
        LRC_SHOES_AND_ACCESSORY = "//div[@class='header__nav-item header__nav-item_active' and contains(.,'Обувь и аксессуары')]"
        LRC_UNDERWEAR = "//div[@class='sidebar__title']/span[contains(.,'Белье')]"

        LRC_ACCESSORY = "//div[@class='sidebar__title']/span[contains(.,'Аксессуары')]"
        LRC_TEXTILE = "//div[@class='sidebar__title']/span[contains(.,'Домашний текстиль')]"
        #LRC_CHILD = "//div[@class='sidebar__title']/span[contains(.,'Детские товары')]"
        LRC_CHILD = "//div[@class = 'header__nav-item header__nav-item_active' and contains(., 'Товары для детей')]"
        LRC_HOUSE = "//div[@class = 'header__nav-item header__nav-item_active' and contains(., 'Товары для дома')]"
        LRC_GARDEN = "//div[@class = 'header__nav-item header__nav-item_active' and contains(., 'Товары для сада')]"
        LRC_TRADE_EQUIPMENT = "//div[@class = 'header__nav-item header__nav-item_active' and contains(., 'Торговое оборудование')]"

        LINK_TREE_CATEGORY = "//ul[@class='sidebar__list']/li[@class]/a[contains(.,'%s')]"
        FC_CLOTHING = "//div[@class='title title_catalog']/h1[@class='title__name']/span[contains(.,'Платья')]"

        WINDOW_CATALOG = "//div[@class='title title_catalog']/h1[@class='title__name']/a[contains(.,'%s')]/.."

        GOOD_LNK = "//div[@class='catalog__list']/div[@class='lot'][%s]//div[@class='lot__name']"
        GOOD_NEW_LNK = "//div[@class='catalog__list']/div[contains(@class,'lot')][%s]//h3[@class='lot-inline__title']/a"
        GOOD_BY_ID = "//h3/a[contains(@class,'lot') and contains(@href,'%s')]"
        GOOD_IMG = "//a[contains(@class,'lot') and contains(@href,'%s')]"
        PATH_GOOD = "//div[@class='lot-inline'][%s]/div[@class='lot-inline__item-info']/h3[@class='lot-inline__title']/a"

    class Input():
        pass


class HelpPage(MainClass):

    class Path():
        # UH ~ URL HELP
        UH_HOW_BUY = "/help-1"
        UH_HOW_BE_SELLER = "/help-2"

    class Check():
        TITLE_ABOUT_COMPANY = "//div[@class = 'inner-layout__list-link inner-layout__list-link_active' and contains(., 'О "\
                    "компании')]"
        TITLE_HOW_REG = "//div[@class = 'inner-layout__list-link inner-layout__list-link_active' and contains(., 'Как "\
                    "зарегистрироваться')]"
        TITLE_FAQ = "//a[@class='inner-layout__list-link inner-layout__list-link_active' and contains(.,'Ваш бизнес " \
                    "на УУРРАА')]"
        TITLE_RULES = "//a[@class='inner-layout__list-link inner-layout__list-link_active' and contains(.,'Правила УУРРАА')]"
        TITLE_CONFIDENTIAL = "//a[@class = 'inner-layout__list-link inner-layout__list-link_active']/span[contains(., "\
                    "'Политика конфиденциальности')]]"
        T_RULES = "//div[@class='help-cover help-cover_rules' and contains(.,'Правила УУРРАА')]"
        TITLE_SUBSCRIBE = "//article[@class='help help_text']/h1[contains(.,'Как подписаться на новинки?')]"
        REG_HELP_CENTER = "//h1[@class='title__name' and contains(.,'УУРРАА центр помощи')]"
        TITLE_FILL_PROFILE = "//article[@class='help help_text']/h1[contains(.,'Зачем заполнять профиль?')]"
        TITLE_AVAIL_SERVICE = "//article[@class='help help_text']/h1[contains(.,'Где доступен сервис')]"
        TITLE_TAKE_SELLER = "//article[@class='help help_text']/h1[contains(.,'Что такое страница продавца?')]"
        #TITLE_CONFIDENTIAL = "//article[@class='help help_text']/h1[contains(.,'Политика конфиденциальности')]"
        
        
        TITLE_HOW_SELL = "//a[@class='inner-layout__list-link inner-layout__list-link_active' and contains(.,'Перечень" \
                         " запрещенных товаров')]"
        TITLE_HOW_BUY = "//a[@class='inner-layout__list-link inner-layout__list-link_active' and contains(.,'Как " \
                        "сделать заказ')]"
        TITLE_FAVORITES = "//a[@class='sidebar__item sidebar__link sidebar__item_active' and contains(.," \
                          "'Что такое \"Избранное\"?')]"
        TITLE_VIDEO = "//article[@class='help help_text']/h1[contains(.,'Видеоролик о компании')]"
        TITLE_SELLER_PAGE = "//article[@class='help help_text']/h1[contains(.,'Что такое страница продавца?')]"

    class Click():
        # BTN ~ BUTTON
        BTN_GO_CATALOG = "//div[@class='help__num-submit']/a[contains(@href,'/catalog') and contains(.,'Перейти в каталог')]"
        BTN_HOW_BUY_REG = "//div[@class='help__num-submit']/a[contains(@href,'/registration') and contains(.," \
                          "'Зарегистрироваться')]"
        BTN_HOW_BE_SELLER_REG = "//div[@class='help__submit']/a[contains(@href,'/registration') and contains(.," \
                                "'Зарегистрироваться')]"

    class Input():
        pass


class AboutPage(MainClass):

    class Check():
        TITLE_ABOUT = "//h1[@class='title__name' and contains(.,'О компании')]"

    class Click():
        pass

    class Input():
        pass


class ContactsPage(MainClass):

    class Path():
        URL_CONTACTS = "/contacts"

    class Check():
        TITLE_CONTACTS = "//h1[@class='title__name' and contains(.,'Контакты')]"
        FEEDBACK_INFO = "//section[@class='feedback']/div[@class='feedback__left-column']/" \
                        "div[@class='feedback__text-wrap'][1]"
        FEEDBACK_LEGAL = "//section[@class='feedback']/div[@class='feedback__left-column']/" \
                         "div[@class='feedback__text-wrap'][2]"
        FEEDBACK_ADDRESS = "//section[@class='feedback']/div[@class='feedback__left-column']/" \
                           "div[@class='feedback__text-wrap'][3]"
        FEEDBACK_TITLES = "//section[@class='feedback']/div[@class='feedback__right-column']"

        MSG_SUCCESS = "//div[@class='feedback__success' and contains(.,'Отправлено') and contains(.,'Спасибо за ваше " \
                      "обращение. Мы в ближайшее время с вами свяжемся.')]"
        MSG_ERROR_NAME = "//div[@class='form__row form__row_error']//input[@name='username']/../span[contains(.,'Введите имя')]"
        MSG_ERROR_EMAIL = "//div[@class='form__row form__row_error']//input[@name='email']/../span[contains(.,'Введите email')]"
        MSG_ERROR_MESSAGE = "//div[@class='form__row form__row_error']//textarea[@name='text']/../../span[contains(.,'Введите сообщение')]"

    class Click():
        HOW_BUY = "//a[contains(@href,'/buyer') and contains(.,'Как покупать на Уурраа?')]"
        HOW_SELL = "//a[contains(@href,'/forbiddengoods') and contains(.,'Как стать продавцом и разместить товары?')]"
        FAQ = "//a[contains(@href,'/business') and contains(.,'Часто задаваемые вопросы')]"
        LOCALE = "//a[contains(@href,'http://oorraa.net/#locate') and contains(.,'Показать на карте')]"

        SENDING = "//button[@type='submit']"

    class Input():
        NAME = "//input[@name='username' and @placeholder='Имя, фамилия' and @maxlength='200']"
        PHONE = "//input[@name='phone' and @placeholder='(800) 000-00-00']"
        EMAIL = "//input[@name='email' and @placeholder='mail@example.com' and @maxlength='200']"
        MESSAGE = "//textarea[@name='text' and @maxlength='1000']"


class OorraaNetPage(MainClass):

    class Check():
        TITLE_JOB = "//a[@class='global-nav__item-link global-nav__item-link_current' and contains(@href,'#vacancies')]"
        TITLE_CONTACTS = "//a[@class='global-nav__item-link global-nav__item-link_current' and contains(@href,'#locate')]"

    class Click():
        pass

    class Input():
        pass

class DeliveryPage(MainClass):

    class Check():
        FIRST_VISIT_MSG = "//div[@id = 'pointer']/h2[contains(., 'Доставка по лучшей цене')]"

    class Click():
        pass

    class Input():
        pass 

class PaymentsPage(MainClass):

    class Check():
        TITLE_MAIN = "//div[@class = 'header-line__wrap' and contains(., 'Сервис приема платежей онлайн')]"

    class Click():
        pass

    class Input():
        pass

class GoodPage(MainClass):

    class Path():
        URL_GOOD = "/goods/%s"
        PATH_IMG_ID_START = '<img class="gallery__preview" src="%s' % MainClass.ENV_STATIC_PATH
        PATH_IMG_ID_END = '_s150x150'
        PATH_SHOP_ID_START = 'href="/store/'
        PATH_SHOP_ID_END = '" data-reactid'
        PATH_OTHER_GOOD = '<a class="lot__item" href="/goods/'

    class Check():
        POPUP_REGISTRATION = "//h2[@class='popup__title' and contains(.,'Регистрация')]"
        POPUP_MSG_FROM_GOOD = "//div[@class='popup__content']//form[@class='form form_popup-lot']//" \
                              "span[contains(@class,'form__textarea')]/textarea[contains(.,'%s')]"
        ON_BOARDING_MSG_KNOW_PRICE = "//div[@class='hint__message hint__message_left' and contains(.,'Условия " \
                                     "сделкиЗарегистрируйтесь, чтобы узнать стоимость необходимого вам количества " \
                                     "товаров')]"
        ON_BOARDING_MSG_IN_SHOP = "//div[@class='hint__message hint__message_left' and contains(.,'Информация о " \
                                  "продавцеУзнайте подробную информацию о продавце и товарах, которые он предлагает')]"

        TITLE_GOOD = "//section[@class='card']//h1[@class='title__name' and text()]"
        TITLE_WARE = "//h1[@class='title__name']"
        NAME_GOOD = "//h1[@class='title__name' and contains(.,'%s')]"
        NOTIFY_MY_GOOD = "//div[@class='notice notice_fixed']//span[contains(.,'Это Ваш товар')]"
        SHOP_LOGO = "//img[@class='card__store-logo' and contains(@src,'%s_s100x100')]"
        SHOP_NO_LOGO = "/img[contains(@src,'no-store-logo')]"
        SHOP_TITLE = "//a[contains(@href,'/store/')]/span[@class='card__store-title' and contains(.,'%s')]"
        USER_PHOTO = "//img[@class='user__photo' and contains(@src,'%s_s100x100')]"
        USER_NO_PHOTO = "//img[contains(@src,'no_ava')]"
        USER_NAME = "//span[@class='user__name' and contains(.,'%s')]"
        USER_STATUS = "//span[@class='user__type' and contains(.,'%s')]"
        USER_YOUR_SELLER = "//span[@class='user__type' and contains(.,'Вы продавец')]"
        COMPLAIN_SUCCESS = "//div[@class='notification notification_success']//span[contains(.,'Ваша жалоба " \
                           "отправлена модератору')]/.."
        BTN_COMPLAIN_HOLD = "//button[@disabled and contains(.,'Пожаловаться на товар')]"
        BTN_KNOW_PRICE_HOLD = "//button[@type='button' and @disabled]/span[contains(.,'Узнать цену')]/.."
        QUERY_SENT_SELLER = "//div[@class='notification notification_success']//span[contains(.,'Ваш запрос был " \
                            "отправлен продавцу.')]/.."
        MIN_STOCK = "//div[@class='card__min-order']/b[@class='card__value']/span[1]"
        ERR_NEED_STOCK_ABSTRACT = "//div[@class='card__note card__note_error' and contains(.,'')]"
        ERR_NEED_STOCK_MIN_MSG = "//div[@class='card__note card__note_error' and contains(.,'Число меньше " \
                                 "минимальной партии')]"
        ERR_NEED_STOCK_MAX_MSG = "//div[@class='card__note card__note_error' and contains(.,'В одном заказе может " \
                                 "быть не более 1') and contains(.,'000 штук')]"
        DELIVERY_ADDRESS_FULL = "//div[@class='info__row info__row_delivery' and contains(.,'Доставка:Самовывоз, %s')]"
        DELIVERY_ADDRESS_EMPTY = "//div[@class='info__row info__row_delivery']/div[text()='Самовывоз']"

        GALLERY_MAIN_PHOTO = "//div[@class='gallery__view']//img[@class='gallery__photo' and contains(@src,'%s_s452x452')]"
        GALLERY_PREVIEW_PHOTO = "//div[@class='gallery__list']/div[%s]//img[@class='gallery__preview' and " \
                                "contains(@src,'%s%s')]"

        MIN_STOCK_VALUE = "//div[@class='card__order']//div[@class='card__min-order' " \
                          "and contains(.,'мин. заказ%s шт.')] "

        PRICE_VALUE = "//div[@class='card__order']//div[@class='card__price' and contains(.,'Цена за штуку:%s')]"
        PRICE = "//div[@class='card__order']//div[@class='card__price']/b[@class='card__value']"

        BREAD_SPLIT = "//section[@class='card']/ul[@class='breadcrumbs' and contains(.,'%s%s')]"
        NEED_QUANTITY = "//span[@class='card__output']/input[@class='card__digit' and contains(@value,'%s')]"

        COUNT_GOODS = "//span[contains(.,'%s шт.')]"
        PRICE_PER_PIECE = "//b[contains(.,'%s руб.')]"

        SIZE_PLAIN = "//article[@class='info']//span[contains(.,'Размеры')]/../../div[contains(.,'%s')]"
        ARTICLE = "//article[@class='info']//span[contains(.,'Артикул')]/../../div[contains(.,'%s')]"
        BRAND_NAME = "//article[@class='info']//span[contains(.,'Бренд')]/../../div[contains(.,'%s')]"
        STOCK_SIZE = "//article[@class='info']//span[contains(.,'Число товаров в упаковке')]/../../div[contains(.,'%s')]"
        DESCRIPTION = "//article[@class='info']//span[contains(.,'Описание')]/../../div[contains(.,'%s')]"
        COLOR = "//div[@class='info__row info__row_color']/div[@class='info__value' and contains(.,'%s')]"
        MATERIAL = "//div[@class='info__row info__row_clothing-material']/div[@class='info__value' and contains(.,'%s')]"

        MSG_SENT_SUCCESS = "//h2[@class='popup__title'and contains(.,'Сообщение отправлено')]"

        USER_NAME_SELLER = "//span[@class='user__name']"

        POPUP_MESSAGE_TO_SELLER = "//div[@class='popup__content']"

        BLOCK_PAYMENT_INFO = "//div[@class='info__row info__row_payment']"
        LABEL_PAYMENT_INFO = BLOCK_PAYMENT_INFO + "//div[contains(.,'Методы оплаты:')]"
        CASH = BLOCK_PAYMENT_INFO + "//dt[contains(.,'Наличными')]"
        CASH_ON_DELIVERY = BLOCK_PAYMENT_INFO + "//dt[contains(.,'Наложенным платежом')]"
        BANK_ACCOUNT = BLOCK_PAYMENT_INFO + "//dt[contains(.,'По счету через банк')]"
        CARD = BLOCK_PAYMENT_INFO + "//dt[contains(.,'Переводом на карту банка')]"
        CARD_TEXT = BLOCK_PAYMENT_INFO + "//dd[contains(.,'%s')]"
        E_MONEY = BLOCK_PAYMENT_INFO + "//dt[contains(.,'Картой или электронными деньгами')]"
        E_MONEY_TEXT = BLOCK_PAYMENT_INFO + "//dd[contains(.,'%s')]"

        BLOCK_DELIVERY_INFO = "//div[@class='info__row info__row_delivery']"
        LABEL_DELIVERY_INFO = BLOCK_DELIVERY_INFO + "//div[contains(.,'Доставка:')]"
        TRANSPORT_COMPANY = BLOCK_DELIVERY_INFO + "//dt[contains(.,'Транспортными компаниями')]"
        TRANSPORT_COMPANY_TEXT = BLOCK_DELIVERY_INFO + "//dd[contains(.,'%s')]"
        COURIER = BLOCK_DELIVERY_INFO + "//dt[contains(.,'Курьером по городу')]"
        COURIER_TEXT = BLOCK_DELIVERY_INFO + "//dd[contains(.,'%s')]"
        OWN_DELIVERY_SERVICE = BLOCK_DELIVERY_INFO + "//dt[contains(.,'Собственная служба доставки')]"
        RUSSIAN_MAIL = BLOCK_DELIVERY_INFO + "//dt[contains(.,'Почта России')]"
        PICKUP = BLOCK_DELIVERY_INFO + "//dt[contains(.,'Самовывоз')]"
        PICKUP_TEXT = BLOCK_DELIVERY_INFO + "//dd[contains(.,'%s')]"


        # попап после нажатия кнопки связаться с продавцом как посетитель
        POPUP_SEND = "//div[@class='popup__content']"
        P_TITLE = POPUP_SEND + "//h2[@class='popup__title' and contains(.,'Связаться с продавцом')]"
        P_YOUR_NAME = POPUP_SEND + "//label[@class='form__label' and contains(.,'Ваше имя:')]"
        P_WHO = POPUP_SEND + "//label[@class='form__label' and contains(.,'Кому:')]"
        P_WHO_VALUE = "//div[@class='popup__content']//div[contains(@class,'user_popup')]"
        P_SUBJECT = POPUP_SEND + "//label[@class='form__label' and contains(.,'Тема:')]"
        P_MESSAGE = POPUP_SEND + "//label[@class='form__label' and contains(.,'Соообщение')]"
        P_EMAIL_FEEDBACK = POPUP_SEND + "//label[@class='form__label' and contains(.,'Ответ отправитьна почту:')]"

        #
        P_SUCCESS_SENT = "//div[contains(@class,'popup__content')]//p[contains(.,'Сообщение отправлено')]"
        P_TITLE_SENT = "//div[contains(@class,'popup__content')]//h2[contains(.,'Совет: пишите нескольким продавцам')]"
        P_BODY_SENT = "//div[contains(@class,'popup__content')]//p[contains(.,'Чтобы быстро договориться о сделке " \
                      "на выгодных условиях,пишите большему количеству продавцов')]"
        P_LABEL_SIMILAR_GOOD = "//div[contains(@class,'popup__content')]//h3/span[contains(.,'Похожие товары')]"
        P_ATTENTION = "//span[contains(.,'Нажимая кнопку \"Зарегистрироваться\", вы подтверждаете свое согласие " \
                      "с условиями предоставления услуг (Пользовательское соглашение)')]"
        P_HELP_PASS = "//div[contains(@class,'popup__content')]//p[@class='form__hint-text' and " \
                      "contains(.,'Не менее6 символов')]"
        P_VISITOR_BODY_SENT = "//div[contains(@class,'popup__content')]//p[@class='popup__text' and " \
                              "contains(.,'Вам остается всего один шаг дозавершения регистрации.')]"
        P_VISITOR_TITLE_SENT = "//div[contains(@class,'popup__content')]//h2[@class='popup__title' and " \
                               "contains(.,'Придумайте пароль')]"
        NOTIFY_REG_SUCCESS = "//span[@class='notification__title' and " \
                             "contains(.,'Поздравляем, Вы зарегистрированы на платформе УУРРАА!')]"

    class Click():
        GOOD_BY_ID_POPUP = "//div[@class='popup__content']//a[contains(@href,'%s')]"
        ON_BOARDING_KNOW_PRICE = "//div[@class='hint hint_price']/div[@class='hint__button']"
        ON_BOARDING_IN_SHOP = "//div[@class='hint hint_about']/div[@class='hint__button']"

        BTN_IN_SHOP_ABSTRACT = "//a[contains(.,'Перейти в магазин')]"
        NOTIFY_MY_GOOD_EDIT = "//div[@class='notice notice_fixed']//span[contains(.,'Редактировать')]"
        BTN_IN_SHOP = "//a[contains(@href,'/store/%s')]/span[contains(.,'Перейти в магазин')]"
        BTN_SHOW_MORE = "//a[contains(@href,'/store/%s')]/span[contains(.,'Показать больше')]/.."
        LINK_SELLER_AVATAR = "//a[@class and contains(@href,'/store/%s')]/img"
        ANY_GOOD = "//div[@class='card__other']/div[@class='lot'][%s]//div[@class='lot__name']"
        OTHER_GOOD_BY_ID = "//div[@class='card__other']//a[contains(@href, '%s')]/div[@class='lot__name']"

        BREADCRUMBS = "//li[@class='breadcrumbs__item'][%s]//span[text()]/.."
        BREADCRUMB = "//li[@class='breadcrumbs__item'][%s]//a[contains(@href,'/catalog/%s') and contains(.,'%s')]"
        BREADCRUMB_LIST = "//ul[@class='breadcrumbs']/li[@class='breadcrumbs__item']"

        ASK_BTN = "//button[@class='button card__ask' and not(@disabled)]/span[contains(.,'" \
                  "Задать вопрос о товаре')]/.."
        ASK_BTN_HOLD = "//button[@class='button card__ask' and @disabled]/span[contains(.,'" \
                       "Задать вопрос о товаре')]/.."

        BTN_COMPLAIN = "//button[contains(.,'Пожаловаться на товар')]"
        KNOW_PRICE_BTN = "//button[@type='button']/span[contains(.,'Узнать цену')]/.."
        DEL_FAVORITE = "//span[contains(.,'Удалить из избранного')]"
        ADD_FAVORITE = "//span[contains(.,'Добавить в избранное')]"
        ADD_FAVORITE_HOLD = "//button[@class='button card__favorite' and @disabled]/span[contains(.,'Добавить в " \
                            "избранное')]"
        BTN_CALL_SELLER = "//button[contains(.,'Связаться с продавцом') and not(@disabled)]"
        BTN_CALL_SELLER_HOLD = "//button[contains(.,'Связаться с продавцом') and (@disabled)]"
        BTN_CALL_SELLER2 = "//button[contains(.,'Связаться с продавцом')]"

        POPUP_CARD_GOOD = "//div[@class='popup__content']//a[@class='lot__item active']"
        BTN_SEND = "//button[contains(.,'Отправить')]"
        BTN_TO_CARD_GOOD = "//div[@class='popup__close']"
        BTN_TO_CHAT = "//button[contains(.,'Перейти в чат')]"
        BTN_CANCEL_CALL = "//button[contains(.,'Отмена')]"

        BTN_ANSWER_TO_SELLER = "//button[@class='button button_warning']"
        BTN_GO_TO_CHAT = "//button[@class='button button_warning']"
        BTN_GO_TO_GOOD_PAGE = "//button[@class='button button_light']"
        BTN_POPUP_TO_CATALOG = "//div[contains(@class,'popup__content')]//a[contains(.,'Вернуться в каталог')]"
        BTN_POPUP_REJECT = "//div[contains(@class,'popup__content')]//button[contains(.,'Отказаться')]"
        BTN_POPUP_REG = "//div[contains(@class,'popup__content')]//button[contains(.,'Зарегистрироваться')]"
        POPUP_LINK_AGREEMENT = "//div[contains(@class,'popup__content')]//a[@href='/rules' and " \
                               "contains(.,'Пользовательское соглашение')]"
        # галерея на странице товара
        IMG_GALLERY_PREVIEW = "//div[@class='gallery__list']/div[%s]//" \
                              "img[@class='gallery__preview' and contains(@src, '%s')]"
        IMG_GALLERY_PREVIEW_ACTIVE = "//div[@class='gallery__list']/div[@class='gallery__slide " \
                                     "gallery__slide_active']//img[@class='gallery__preview' and contains(@src, '%s')]"
        IMG_GALLERY_VIEW = "//div[@class='gallery__view']//img[@class='gallery__photo' and contains(@src,'%s')]"
        IMG_ZOOM = "//div[@class='gallery']/div[@class='gallery__view']//span[@class='zoom']"
        # zoom галерея на странице товара
        POPUP_ZOOM_GALLERY = "//div[@class='popup__content']"
        IMG_ZOOMED = POPUP_ZOOM_GALLERY + "//img[@class='popup__img' and contains(@src,'%s')]"
        IMG_ZOOM_PREVIEW = POPUP_ZOOM_GALLERY + "//div[@class='popup__thumbs']/div[%s]//" \
                                                "img[@class='popup__thumb-img' and contains(@src, '%s')]"
        IMG_ZOOM_PREVIEW_ACTIVE = POPUP_ZOOM_GALLERY + "//div[@class='popup__thumb popup__thumb_active']//" \
                                                       "img[@class='popup__thumb-img' and contains(@src, '%s')]"
        ZOOM_CLOSE = POPUP_ZOOM_GALLERY + "//div[@class='popup__close']"


    class Input():
        POPUP_INPUT_NAME = "//div[@class='popup__content']//input[contains(@name,'userName') and @maxlength=200]"
        POPUP_INPUT_MSG = "//span[@class='form__textarea form__textarea_custom-placeholder']/textarea[@maxlength=1000]"
        POPUP_INPUT_EMAIL = "//div[@class='popup__content']//input[contains(@name,'userEmail') and @maxlength=200]"
        POPUP_INPUT_PASS = "//div[contains(@class,'popup__content')]//input[contains(@name,'userPassword')]"
        NEED_STOCK = "//span[@class='card__output']/input"


class ChatPage(MainClass):

    class Path():
        PATH_CHAT_USER_CARD = "//a[@class='list__item'][%s]"
        PATH_DEAL_USER_CARD = "//a[@class='partner__link']"
        URL_CHAT = "/user/chats"

        URL_CHAT_WITH_USER = "/user/chats/%s"

        TO_FIND_USER_ID_START = 'href="/user/chats/'
        TO_FIND_USER_ID_END = '" data-reactid='
        PATH_CHAT_USER = "//div[@class='contact-list contact-list_scrollable']/div/a[%s]"

    class Check():
        TITLE_CHAT = "//h1[@class='title__name' and contains(.,'Сделки и сообщения')]"
        TITLE_USER_IN_CHAT = "//div[@class='partner']//a[@class='partner__link' and contains(@href,'/store/%s')]"
        CHAT_SECTION_CHAT = "//a[@class='deals-bar__block deals-bar__block_active' and contains(@href,'/user/chat/with/%s')]//" \
                            "div[contains(.,'Чат с пользователем')]/../.."
        DEAL_WITH_SELLER_INFO = "//a[@class='list__item'][%s]/div[@class='list__text']/div[@class='list__info' " \
                                "and contains(.,'%sОбновление в сделке по товару: %s')]"
        CH_USER_PHOTO = "//img[@class='contact-list__ava' and contains(@src,'%s_s100x100')]"
        CH_USER_NAME = "//p[@class='contact-list__name' and contains(.,'%s')]"
        CH_USER_STATUS = "//p[@class='list__status' and contains(.,'Пользователь') and contains(.,'%s')]"

        DL_USER_PHOTO = "//img[@class='partner__avatar' and contains(@src,'%s_s100x100')]"
        DL_USER_NAME = "//span[@class='partner__name' and contains(.,'%s')]"
        DL_USER_STATUS = "//span[@class='partner__status' and contains(.,'Пользователь') and contains(.,'%s')]"

        COMPLAIN_1_MSG = "//div[@class='chat__text' and contains(.,'Жалоба модератору на товар:')]"
        COMPLAIN_TIME = "//div[@class='chat__item-wrap'][last()]//span[@class='chat__time']"
        COMPLAIN_GOOD_LINK = "//a[@class='lot__item' and contains(@href,'/goods/%s')]"
        COMPLAIN_GOOD_NAME = "//div[@class='lot__name' and contains(.,'%s')]"
        LAST_MSG = "//section[@class='messenger__content']/div[@class='chat']//div[@class='chat__item-wrap'][last()]"
        LAST_MSG_WITH_SEPARATOR = LAST_MSG + "/div"

        ACTIVE_USER_BY_ID = "//div/a[contains(@class,'contact-list__item contact-list__item_active') and " \
                            "contains(@href,'/user/chats/%s')]"

        GET_NAME_OPPONENTS = "//div[@class='contact-list contact-list_scrollable']/div//p[@class='contact-list__name']"

        #UPDATE: RT-876
        DIALOGS = "//div[@class='chat']//div[@class='chat__item-wrap']"
        DIALOG_BY_POSITION = "//div[@class='chat__item-wrap'][%s]"
        DIALOG = "//div[@class='chat__item-wrap' and contains(@data-reactid, '%s')]"
        MESSAGE = DIALOG + "//div[contains(@class,'chat__item chat__item_')]"

        # информация об отправителе, времени отправки сообщения и отметки о прочтении
        SENDER_AVATAR = "//a/img[@class='chat__ava' and contains(@src, '%s')]"
        SENDER_NAME = "//p[@class='chat__name' and contains(.,'%s')]"
        SEND_TIME = "//span[contains(@class, 'chat__time') and contains(.,'%s')]"
        READ_MSG = "//span[@class='chat__time chat__time_read chat__time_sent']"
        UNREAD_MSG = "//span[@class='chat__time chat__time_sent']"

        # текстовое сообщение
        TEXT_MSG = MESSAGE + """//div[@class='chat__text' and contains(.,"%s")]"""

        # сообщение карточка товара
        MSG_WARE = MESSAGE + "//a[@class='lot__item' and contains(@href,'/goods/%s')]"
        WARE_PICTURE = MSG_WARE + "//img[@class='lot__photo' and contains(@src, '%s')]"
        WARE_NAME = MSG_WARE + "//div[@class='lot__name' and contains(., '%s')]"
        WARE_PRICE = MSG_WARE + "//div[contains(@class,'lot__price') and contains(., 'За штуку')]"
        WARE_QUANTITY = MSG_WARE + "//div[contains(@class,'lot__quantity') and contains(., 'Мин. заказ')]"

        # сообщение карточка пользователя
        MSG_USER = MESSAGE + "//li[@class='contact-list__item']/a[contains(@href, '/%s')]"
        USER_AVATAR = MSG_USER + "//img[@class='contact-list__ava' and contains(@src, '%s')]"
        USER_NAME = MSG_USER + "//p[@class='contact-list__name' and contains(.,'%s')]"
        USER_STATUS = MSG_USER + "//span[@class='contact-list__text' and contains(.,'%s')]"

        # сообщение картинка
        MSG_PICTURE = MESSAGE + "//div[@class='chat__img-cover' and contains(@style, '%s')]"

    class Click():
        ALL_DIALOGS = "//div[@class='contact-list contact-list_scrollable']//a"
        ALL_UNREAD_MESSAGES = "//div[@class='contact-list contact-list_scrollable']//a//span[@class='note-counter " \
                              "note-counter_unread']"
        DL_LINK_USER_AVATAR = "//../a[contains(@href,'/%s')]"
        USER_CHAT_AND_DEAL = "//a[@class='list__item' and contains(@href,'/user/chat/with/%s')]"

        BTN_SEND = "//button[contains(.,'Отправить')]"

        BTN_ANSWER = "//button[@class='button button_warning']"

    class Input():
        CHAT_INPUT = "//form[@class='chat__add']//input[@class='form__input' and @type='text' and " \
                     "@placeholder='Ваше сообщение...' and @maxlength='500']"
        CHAT_INPUT_ABSTRACT = "//form[@class='chat__add']//input[@class='form__input' and @type='text']"

        #UPDATE: RT-876
        SEND_CHAT = "//textarea[@class='publisher__textarea' and @placeholder='Ваше сообщение...' and @maxlength=1000]"


class FavoritePage(MainClass):

    class Path():
        URL_FAVORITES_GOODS = "/user/favorites"
        URL_FAVORITES_USERS = "/user/contacts"

        PATH_FAVORITE = "//div[@class='list__item'][%s]"
        PATH_FG_USERS = "//div[@class='list__user']"
        PATH_FU_USERS = "//a[@class='list__user']"
        PATH_IMG = "//img[contains(@src,'%s')]"

    class Check():
        TITLE_FAVORITE = "//h1[@class='title__name' and contains(.,'Избранное')]"
        FG_USER_PHOTO = "//img[@class='list__avatar' and contains(@src,'%s_s100x100')]"
        FG_USER_NAME = "//h2[@class='list__name' and contains(.,'%s')]"

        MENU_ACTIVE = "//a[@class='menu__link active' and contains(.,'%s')]"
        MENU_INACTIVE = "//a[@class='menu__link' and contains(.,'%s')]"

        WARE_NAME_FAVORITE = "//a[contains(.,'%s')]"
        MIN_STOCK_BY_GOOD_ID = "//a[@class='list__cover' and contains(@href,'%s')]/..//div[@class='list__option'][1]"
        PRICE_BY_GOOD_ID = "//a[@class='list__cover' and contains(@href,'%s')]/..//div[@class='list__option'][2]"

    class Click():
        GOOD_BY_ID = "//a[@class='list__cover' and contains(@href,'%s')]"
        GOOD_NAME_BY_GOOD_ID = "//a[@class='list__cover' and contains(@href,'%s')]/..//a[@class='list__link']"

        FG_LINK_SELLER_AVATAR = "//a[@class='list__misc' and contains(@href,'/store/%s')]"


        USERS_PAGE = "//a[contains(@href,'/user/favorites/users') and contains(.,'Пользователи')]"
        GOODS_PAGE = "//a[contains(@href,'/user/favorites/') and contains(.,'Товары')]"

        FAV_GOOD_NAME = "//div[@class='list__item'][%s]//h2[@class='list__name']/a[@class='list__link']"
        FG_USER_NAME_ABSTRACT = "//div[@class='list__item'][%s]/a[@class='list__misc']/h2[@class='list__name' and text()]"
        FU_SELLER_NAME_ABSTRACT = "//div[@class='list__item']/a[contains(@href,'/store')]/..//h2[@class='list__name']" \
                                  "/a[text()][%s]"
        BREADCRUMBS = "//div[@class='list__item'][1]//p[@class='list__category']/a[text()][%s]"

        GOOD_NAME = "//div[@class='list__item'][%s]/div[@class='list__text']/div[@class='list__info']/" \
                    "h2[@class='list__name']/a[contains(.,'%s')]"
        GOOD_NAME_BY_ID = """//div[@class='goods-table__row']//a[contains(@href,'/goods/%s') and text()]"""
        GOOD_NAME_BY_ID_AND_TITLE = """//div[@class='goods-table__row' and contains(.,"%s")]/a[contains(@href,'%s')]/.."""
        DEL_FAVORITE = GOOD_NAME_BY_ID_AND_TITLE + "//div[@class='goods-table__delete-button']"
        DEL_FAVORITE_BY_GOOD_ID = "//a[@class='list__cover' and contains(@href,'%s')]/..//span[contains(.,'Удалить')]"

    class Input():
        pass


class UserContactsPage(MainClass):
    class Path():
        URL_FAVORITES_USERS = "/user/contacts"
        TO_FIND_USER_ID_START = 'href="/user/chats/'
        TO_FIND_USER_ID_END = '" data-reactid='
        path_favorites_USER = "//div[@class='contact-list contact-list_scrollable']/div/div[%s]"

    class Check():
        FU_USER_PHOTO = "//img[contains(@src,'%s_s150x150')]"
        FU_USER_PHOTO_IN_SEARCH = "//img[contains(@src,'%s_s100x100')]"
        FU_USER_NAME = "//p[@class='contact-list__name' and contains(.,'%s')]"
        FU_USER_STATUS = "//span[@class='contact-list__text' and contains(.,'%s')]"
        FU_ACTIVE_USER_ABSTRACT = "//div[@class='contact-list__item contact-list__item_active']" \
                                  "/p[@class='contact-list__name']"

        USER_INFO = "//div[@class='user user_contact']"
        UI_USER_NAME = "//p[@class='user__name' and contains(.,'%s')]"
        UI_USER_STATUS = "//p[@class='user__status' and contains(.,'%s')]"
        COUNT_USERS = "//div[contains(@class,'contact-list__item')]"

        USER_STORE = "//div[@class='user user_contact user_store']"
        US_LABEL_NAME = "//p[@class='user__status' and contains(.,'Магазин пользователя')]"
        US_NAME = "//p[@class='user__name' and contains(.,'%s')]"
        US_DESCRIPTION = "//div[@class='user__store-address']/p[@class='user__txt' and contains(.,'%s')]"
        US_LABEL_ADDRESS = "//div/p[@class='user__txt' and contains(.,'Адрес магазина')]"
        US_ADDRESS = "//p[@class='user__store' and contains(.,'%s')]"
        US_LOGO = "//img[@class='user__store-logo' and contains(@src,'%s_s100x100')]"
        US_LOGO_STUB = "//img[@class='user__store-logo' and contains(@src,'no-store-logo')]"
        US_WITHOUT_NAME = "//p[@class='user__name' and contains(.,'Магазин пользователя')]"

        USER_CARD_BY_ID = "//div[contains(@class,'contact-list__item') and contains(@data-reactid,'%s')]"
        ACTIVE_USER_CARD_BY_ID = "//div[contains(@class,'contact-list__item contact-list__item_active') and " \
                                 "contains(@data-reactid,'%s')]"
        USER_IN_SEARCH = "//li[@class='contact-list__item']"
        ITS_YOU = "//span[@class='contact-list__text']/span[contains(.,'Это вы')]"
        MSG_SUCCESS_ADD_USER = "//div[@class='notification__wrapper' and contains(.,'Пользователь %s добавлен " \
                               "в список ваших контактов')]"
        MSG_ALERT = "//div[@class='notification__wrapper' and contains(.,'Введите номер телефона полностью')]"
        MSG_DELETE_USR = "//div[@class='notification__wrapper' and contains(.,'Пользователь %s удален из списка " \
                         "ваших контактов')]"

        NOT_FOUND_USER = "//p[@class='messenger__empty messenger__empty_left' and contains(.,'К сожалению, " \
                         "пользователь с таким номером телефона не найден')]"
        NOT_FOUND_BY_NAME = "//p[@class='messenger__empty' and contains(.,'Не найдено ни одного контакта')]"
        SECTION_SEARCH = "//section[@class='messenger__content messenger__content_store']"
        ALREADY_IN_CONTACT_LIST = "//div[@class='contact-list__status' and contains(.,'Уже в контактах')]"

    class Click():
        SEND_MSG = "//a[contains(@href,'/user/chats/%s') and contains(.,'Сообщение')]"
        IN_SHOP = "//a[contains(@href,'/store/%s') and contains(.,'В магазин')]"
        IN_CONTACT_USER = "//button[contains(.,'В контакты') or contains(.,'Добавить в контакты')]"
        OUT_CONTACT_USER = "//button[contains(.,'В контактах') or contains(.,'Удалить из контактов')]"
        LAST_USER = "//div[contains(@class,'contact-list__item')][last()]"
        BTN_DELETE = "//button[contains(.,'Удалить')]"
        BTN_NEW_CONTACT = "//button[contains(.,'Новый контакт')]"
        BTN_ADD_CONTACT = "//button[contains(.,'Добавить в контакты')]"
        BTN_CLOSE_ADD_CONTACT = "//span[@class='chat-search__reject']"

    class Input():
        PHONE = "//span[contains(.,'+7')]/..//input[@type='tel' and @placeholder='(800) 000-00-00']"
        NAME = "//input[contains(@placeholder,'Поиск среди контак') and @maxlength=100]"

class MyGoodsPage(MainClass):

    class Path():
        URL_MY_GOODS = '/user/goods/active/1'
        URL_ADD_GOOD = "/user/goods/create"
        URL_EDIT_GOOD = "/user/goods/%s/edit"
        TO_FIND_GOODS = '<a class="list__cover" href="/goods/'
        URL_GOODS = '/goods/%s'
        PAGINATOR_LIST = "//div[@class='pagenav__nav']/ul[@class='pagenav__list']//a[text()]"
        PAGINATOR_ACTIVE = "//li[@class='pagenav__item pagenav__item_active']/a[@class='pagenav__link' and " \
                           "contains(.,'%s')]"
        PATH_IMG_ID_START = 'src="%s' % MainClass.ENV_STATIC_PATH
        PATH_IMG_ID_END = '_s452x452'

    class Check():
        TITLE_MY_GOODS = "//h1[@class='title__name' and contains(.,'Мои товары')]"
        TITLE_ADD_GOOD = "//h1[@class='title__name' and contains(.,'Добавить товар')]"
        TITLE_EDIT_GOOD = "//h1[@class='title__name' and contains(.,'Редактирование товара')]"
        MENU_ACTIVE = "//a[@class='menu__link active' and contains(.,'%s')]"
        MENU_INACTIVE = "//a[@class='menu__link' and contains(.,'%s')]"
        SHOT_INFO_GOOD = "//div[@class='list__item list__item_active'][%s]/div[@class='list__text']"
        PAG_PREV_PASSIVE = "//span[@class='pagenav__prev pagenav__prev_passive' and contains(.,'‹')]"
        PAG_NEXT_PASSIVE = "//span[@class='pagenav__next pagenav__next_passive' and contains(.,'›')]"
        WARE_NAME = "//a[contains(.,'%s')]"

        SHOT_CARD_GOOD_DATA = "//div[@class='list__item list__item_active'][%s]/div[@class='list__text']"
        SHOT_CARD_GOOD_PHOTO = "//div[@class='list__item list__item_active'][%s]//img[@class='list__photo' and " \
                               "contains(@src,'%s%s')]"

        ADD_GOOD_NAME_FIELDS = "//fieldset[@class='form__fieldset']//span[@class='form__label' and contains(.,'%s')]"

        ERR_MIN_STOCK = "//label/input[@name='min_stock']/../span[@class='form__error' and contains(.,'%s')]"
        ERR_REMAINS = "//label/input[@name='remains']/../span[@class='form__error' and contains(.,'%s')]"
        ERR_PRICE = "//label/input[@name='price']/../span[@class='form__error' and contains(.,'%s')]"
        ERR_STOCK_SIZE = "//label/input[@name='stock_size']/../span[@class='form__error' and contains(.,'%s')]"
        ERR_NAME = "//label/input[@name='title']/../span[@class='form__error' and contains(.,'%s')]"
        ERR_CATEGORY_1 = "//select[@id='categorySelect-1']/../../span[@class='form__error' and contains(.,'%s')]"
        ERR_FILE = "//label/input[@type='file']/../../../../span[@class='form__error' and contains(.,'%s')]"

        CHECKBOX_WARE = "//div[@class='list__item list__item_active'][%s]/div[@class='form__check form__check_goods']" \
                        "/label[@class='form__check__controller']/div[@class='form__check__view']"

    class Click():
        ROOT_CATEGORY = "//fieldset[@class='form__fieldset form__fieldset_required']//span[@class='form__select'][1]" \
                        "/select/option[contains(.,'%s')]"
        CATEGORY = "//fieldset[@class='form__fieldset form__fieldset_required']//span[@class='form__select'][%s]" \
                   "/select/option[contains(.,'')][2]"
        COUNT_SELECT = "//fieldset[@class='form__fieldset form__fieldset_required']/div[@class='form__row']/" \
                       "span[@class='form__select']"
        ACTIVE_PAGE = "//a[contains(@href,'/user/goods/active/1') and contains(.,'Активные')]"
        INACTIVE_PAGE = "//a[contains(@href,'/user/goods/inactive/1') and contains(.,'Неактивные')]"
        BUTTON_ADD_GOOD = "//a[contains(@href,'/user/goods/create')]/span[contains(.,'Добавить товар')]/.."
        BUTTON_EDIT = "//a[contains(.,'Изменить')]"
        NAME_CARD_GOOD = "//div[@class='list__item list__item_active'][%s]//h2[@class='list__name']/a[text()]"
        PAG_NEXT = "//div[@class='pagenav__nav']/a[@class='pagenav__next']"
        PAG = "//div[@class='pagenav__nav']//a[contains(.,'%s')]"
        PAG_PREV = "//div[@class='pagenav__nav']/a[@class='pagenav__prev']"
        GOOD_BY_ID_TO_STATUS ="//div[@class='notice__side']/button[@class='button button_light' and contains(.,'%s')]"

        CHECKBOX = "//div[@class='list__item list__item_active']/a[contains(@href,'%s')]/.." \
                   "//div[@class='form__check__view']"

        PATH_REQUIRE_FIELDS = "//fieldset[@class='form__fieldset form__fieldset_required']"
        PATH_FIELDS = "//fieldset[@class='form__fieldset']"
        FIELD_CATEGORY = "//select/option[contains(.,'%s')]"
        ADD_PHOTO = "//div[@class='form__preview form__preview_empty file-upload']/label"
        ADD_AVATAR = "//div[@class='file-upload file-upload_avatar file-upload']/label"
        ADD_GOOD_BTN_PUBLISH = "//button[contains(.,'Опубликовать')]"

        SELECT_COLOR = "//select[contains(@id,'color-%s')]/option[contains(.,'%s')]"
        SELECT_MATERIAL = "//select[contains(@id,'material-%s')]/option[contains(.,'%s')]"
        PLUS_BTN = "/../../../..//i[@class]"

        DELETE_PHOTO = "//div[@class='form__preview'][%s]/span[@class='form__delete']"

        BTN_INACTIVE = "//button[@class='button button_light group__item']"

    class Input():
        ADD_GOOD_NAME = "//input[@name='title' and @maxlength='200' and @placeholder='200 символов']"
        ADD_GOOD_MIN_STOCK = "//input[@name='min_stock']"
        REMAINS = "//input[@name='remains']"
        PRICE = "//input[@name='price']"
        ARTICLE = "//input[@name='article' and @maxlength='128' and @placeholder='128 символов']"
        BRAND_NAME = "//input[@name='brand_name' and @maxlength='128' and @placeholder='128 символов']"
        STOCK_SIZE = "//input[@name='stock_size']"
        SIZES_PLAIN = "//input[@name='sizes_plain' and @maxlength='128' and @placeholder='128 символов']"
        DESCRIPTION = "//textarea[@name='description' and @maxlength='1500' and contains(@placeholder,'500 символов')]"


class ShopPage(MainClass):

    class Path():
        URL_SHOP = "/store/%s"
        TO_FIND_GOODS = '<a class="lot__item" href="/goods/'
        PATH_IMG = "//img[contains(@src,'%s')]"

    class Check():
        ON_BOARDING_MSG_ADDRESS = "//div[@class='hint__message' and contains(.,'Адрес магазинаХотите забрать товар " \
                                  "сами? Обратите внимание на адрес, указанный продавцом.')]"
        NOTIFY_MY_SHOP = "//span[@class='notice__title' and contains(.,'Это ваш магазин')]"
        NAME_SELLER = "//div[@class='store__wrapper']/section[@class='store']//div[@class='store__user-name' and text()]"
        INFO_URL = "//div[@class='store']//p[contains(.,'/store/%s')]"
        INFO_ADDRESS = "//dl[@class='store__info-list' and contains(.,'%s')]"
        INFO_ADDRESS_ABSTRACT = "//dl[@class='store__info-list' and contains(.,'')]/div[1]"
        TITLE_SHOP ="//div[@class='catalog__title catalog__title_store' and contains(.,'Товары')]"

        USER_PHOTO = "//div[@class='store__user-avatar']/img[contains(@src,'%s_s100x100')]"
        USER_NAME = "//div[@class='store__user-name' and contains(.,'%s')]"
        USER_NAME_ABSTRACT = "//div[@class='store__user-name' and text()]"
        USER_STATUS = "//div[@class='store__user-status' and contains(.,'Пользователь') and contains(.,'%s')]"

        NAME_STORE = "//h3[@class='store__title' and contains(.,'%s')]"
        ADDRESS_STORE = "//dl[@class='store__info-list' and contains(.,'%s')]"
        DESCRIPTION_STORE = "//dl[@class='store__info-list' and contains(.,'%s')]"

    class Click():
        ON_BOARDING_ADDRESS = "//div[@class='hint hint_store']/div[@class='hint__button']"
        GOOD_BY_ID = "//a[@class='lot__item' and contains(@href,'%s')]"
        GOOD_NAME_BY_ID = "//a[@class='lot__item' and contains(@href,'%s')]/div[@class='lot__name']"
        CHAT_BUTTON = "//div[@class='store__actions']//a[contains(@href,'/user/chat/with/%s')]/span[contains(.,'Сообщение')]/.."
        GOOD = "//div[contains(@class,'lot')][%s]//div[@class='lot__name']"
        ADD_GOOD = "//div[@class='notice__side']/../span[contains(.,'Это ваш магазин')]/..//a[contains(@href,'/user/goods/create')]"
        SETTINGS = "//div[@class='notice__side']/../span[contains(.,'Это ваш магазин')]/..//a[contains(@href,'/user/settings')]"
        PAG_NEXT = "//a[@class='pagenav__next']"
        PAG_ACTIVE = "//li[@class='pagenav__item pagenav__item_active']/a[contains(@class,'pagenav__link')]"
        PAG_BY_NUMBER = "//a[@class='pagenav__link' and contains(.,'%s')]"
        ADD_WARE_FROM_MY_SHOP = "//a[@class='button button_compact'][2]"

    class Input():
        pass


class SearchPage(MainClass):

    class Path():
        PATH_IMG = "//img[contains(@src,'%s')]"
        PATH_FIND_USER = 'a class="list__user" href="/store/'
        PATH_SEARCH_USER = "//div[@class='list__item']/a[contains(@href,'/store/%s')]/.."
        PATH_CATALOG_GOOD = "//div[@class='catalog']/div[@class='catalog__list']"
        PATH_CATALOG_SELLER = "//div[@class='catalog']/div[@class='catalog__list']/section[@class='list list_users']" \
                              "/div/div"

    class Check():
        GOODS_IN_PAGE = "//div[@class='catalog']/div[@class='catalog__list']"
        TITLE_SEARCH = "//div[@class='sidebar__title' and contains(.,'Поиск')]"
        USER_PHOTO = "//img[@class='list__avatar' and contains(@src,'%s_s100x100')]"
        USER_NAME = "//a[@class='list__link' and contains(.,'%s')]"
        USER_STATUS = "//p[@class='list__status' and contains(.,'Пользователь') and contains(.,'%s')]"

        ABSTRACT_COUNT_PATH = "/../span[3]"
        CATALOG_ALL_EMPTY = "//section[@class='empty empty_search-result']//h1[@class='empty__title' and " \
                            "contains(.,'По запросу “%s”пользователей и товаров не найдено')]"
        CATALOG_EMPTY_DESC = "//p[@class='empty__description' and contains(.,'Пожалуйста, проверьте правильность " \
                             "написания или воспользуйтесь каталогом')]"

        CATALOG_GOOD_EMPTY = "//section[@class='empty empty_search-result']//h1[@class='empty__title' and " \
                             "contains(.,'По запросу “%s”товаров не найдено')]"
        CATALOG_GOOD_EMPTY_DESC = "//section[@class='empty empty_search-result']//p[@class='empty__description' and " \
                                  "contains(.,'Зато мы нашли одного пользователя по этому запросу')]"

        CATALOG_USER_EMPTY = "//section[@class='empty empty_search-result']//h1[@class='empty__title' and " \
                             "contains(.,'По запросу “%s” пользователей не найдено')]"
        CATALOG_USER_EMPTY_DESC = "//section[@class='empty empty_search-result']//p[@class='empty__description' and " \
                                  "contains(.,'Зато мы нашли один товар по этому запросу')]"

        SECTION_GOODS = "//div[@class='catalog']//div[@class='category']/div[@class='lot']"
        SECTION_USERS = "//div[@class='catalog']//section[@class='list list_users']//div[@class='list__item']"


    class Click():
        GOOD_BY_ID = "//a[@class='lot__item' and contains(@href,'%s')]"
        GOOD_BY_NUMBER = "//div[@class='catalog__list']/div[@class='lot'][%s]/a[@class='lot__link']"
        SELLER_BY_NUMBER = "//section[@class='list list_users']/div[@class='list__feed']/div[@class='list__item'][%s]"
        USER_MENU = "//ul[@class='sidebar__list']//span[contains(.,'Пользователи')]"
        LINK_SELLER_AVATAR = "//a[@class='list__user' and contains(@href,'/store/%s')]"
        SELLER_NAME_WITH_ID = LINK_SELLER_AVATAR + "/..//a[@class='list__link' and contains(.,'%s')]"
        LNK_GOOD_WITH_HREF = "//div[@class='catalog__list']//a[@class='lot__item' and contains(@href,'%s') " \
                             "and contains(.,'%s')]"
        MENU_ACTIVE = "//li[@class='sidebar__item sidebar__item_active']//span[contains(.,'%s')]"
        MENU_INACTIVE = "//li[@class='sidebar__item']//span[contains(.,'%s')]"

        BTN_CATALOG = "//a[contains(@href,'/catalog') and contains(.,'Перейти в каталог')]"

        #TODO: test_search_new
        GOODS_MENU = {
            "goods": "//a[@class='sidebar__link active' and contains(@href,'/search/goods')]",
            "users": "//a[@class='sidebar__link' and contains(@href,'/search/goods')]"
        }
        USERS_MENU = {
            "goods": "//a[@class='sidebar__link' and contains(@href,'/search/users')]",
            "users": "//a[@class='sidebar__link active' and contains(@href,'/search/users')]"
        }
        PAG_PAGE = "//li[@class='pagenav__item' and contains(.,'%s')]"

        GOOD_CARD_BY_ID = "//a[@class='lot__item' and @href='/goods/%s']"
        GOOD_PICTURE = GOOD_CARD_BY_ID + "/img[@class='lot__photo' and contains(@src, '%s_s452x452')]"
        GOOD_TITLE = GOOD_CARD_BY_ID + "/div[@class='lot__name' and contains(.,'%s')]"
        GOOD_PRICE = GOOD_CARD_BY_ID + "/div[contains(@class,'lot__price') and contains(.,'За штуку%s руб.')]"
        GOOD_MIN_STOCK = GOOD_CARD_BY_ID + "/div[@class='lot__quantity' and contains(.,'Мин. заказ%s шт.')]"

        BTN_TO_USERS = "//section[@class='empty empty_search-result']//a[contains(@href,'/search/users?q=%s') " \
                       "and contains(.,'Смотреть пользователей')]"
        BTN_TO_GOODS = "//section[@class='empty empty_search-result']//a[contains(@href,'/search/goods?q=%s') " \
                       "and contains(.,'Смотреть товары')]"

    class Input():
        pass


class BuyerPage(MainClass):

    class Path():
        URL_BUYER = "/user/%s"

    class Check():
        USER_PHOTO = "//img[@class='buyer__photo' and contains(@src,'%s_s100x100')]"
        USER_NAME = "//div[@class='buyer__name' and contains(.,'%s')]"
        USER_STATUS = "//div[@class='buyer__status' and contains(.,'Пользователь') and contains(.,'%s')]"

    class Click():
        pass

    class Input():
        pass


class BackAuthPage(MainClass):

    class Path():
        URL_LOGIN = "/login"

    class Check():
        TITLE = "//h2[contains(.,'Please sign in')]"
        MSG_FAILED = "Невозможно отобразить страницу"
        NAV_BAR_TOP = "//div[@class='navbar navbar-inverse navbar-fixed-top' and contains(.,'OORRAA B2B Marketplace " \
                      "Back OfficeВыход')]"
        FAIL_LOGIN = "//div[@class='login-alert alert alert-danger']/span[contains(.,'У вас нет прав на вход в " \
                     "административную панель')]"

    class Click():
        BTN_SUBMIT = "//button[@type='submit' and contains(.,'Submit')]"
        MENU_ITEM = "//ul[@class='nav nav-sidebar']/li/a[contains(.,'%s')]"

    class Input():
        FORM_LOGIN = "//input[@name='login' and @placeholder='+7']"
        FORM_PASS = "//input[@name='password' and @placeholder='Password']"


class BackWaresPage(MainClass):

    class Path():
        URL_WARES = "/#/wares"
        TO_FIND_GOOD = '<iframe src="//%s/goods/'

    class Check():
        COUNT_WARES = "//div[@class='goods']//p[contains(.,'Неподтвержденных товаров: %s')]"
        WARE_TITLE = "//h1[contains(.,'%s')]"

    class Click():
        BTN_START_MODERATION = "//a[contains(@href,'#/wares/moderation') and contains(.,'Приступить к модерации')]"
        BTN_START_MODERATION_STATUS = "//a[contains(@href,'#/wares/moderation') and contains(.,'Приступить к модерации') and %s]"
        BTN_DO_ACCEPT = "//button[contains(.,'Утвердить')]"
        BTN_DO_DECLINE = "//button[contains(.,'Отклонить')]"
        BTN_DECLINE = "//div[@class='modal-footer']/button[contains(.,'Отклонить')]"
        LIST_REASON_DECLINE = "//select[@class='form-control ng-pristine ng-valid']/option"
        REASON_DECLINE = "//select[@class='form-control ng-pristine ng-valid']/option[contains(@label,'%s')]"

    class Input():
        pass


class BackLoadWaresPage(MainClass):

    class Path():
        URL_LOAD_WARES = "/#/import"

    class Check():
        TITLE = "//h2[@class='ng-scope' and contains(.,'Загрузка товаров')]"

    class Click():
        pass

    class Input():
        pass


class BackUsersPage(MainClass):

    class Path():
        URL_USERS = "/#/users"

    class Check():
        CREATED_USER_ID = "//div[contains(.,'ID пользователя')]//input[@readonly and @value=%s]"
        NAME = "//tbody/tr[@class='ng-scope']//a[contains(@href,'#/users/id%s') and contains(.,'%s')]"
        ID = "//tbody/tr[@class='ng-scope']//div[contains(.,'ID: %s')]"
        PHONE = "//tbody/tr[@class='ng-scope']//div[contains(.,'+%s')]"
        ROLE = "//tbody//div[@ng-repeat='authority in user.authorities']/span[contains(.,'%s')]"
        LINES = "//table[@class='table table-striped table-bordered ng-scope']/tbody/tr[@class='ng-scope']"
        LINE = "//table[@class='table table-striped table-bordered ng-scope']/tbody/tr[@class='ng-scope'][%s]"
        COUNT_USERS = "//div[@class='alert alert-info ng-scope']/b[@class='ng-binding']"
        PHONES = "//tbody/tr[@class='ng-scope']//div[@class='user-info__item ng-binding'][2]"
        IDS = "//tbody/tr[@class='ng-scope']//div[@class='user-info__item ng-binding'][1]"

        NAME_FIELDS = "//form[@name='userForm']//label[contains(.,'%s')]"
        MSG_SUCCESS = "//div[@class='growl']/div[contains(.,'Изменения сохранены')]"

        MODAL_BODY = "//div[@class='modal-dialog']/div[@class='modal-content']/div[@class='modal-body' and " \
                     "contains(.,'Вы уверены, что хотите заблокировать пользователя и деактивировать все его товары. " \
                     "Деактивацию товаров невозможно отменить!')]"

        MODAL_DISABLED_BTN = "//div[@class='modal-dialog']/div[@class='modal-content']/div[@class='modal-footer']/" \
                             "button[@class='btn btn-danger' and contains(.,'Заблокировать')]"

        MODAL_CANCEL_BTN = "//div[@class='modal-dialog']/div[@class='modal-content']/div[@class='modal-footer']/" \
                           "button[contains(.,'Отмена')]"

        DISABLED_SUCCESS = "//div[@class='growl']//div[@class='ng-binding ng-scope' and contains(.,'Пользователь " \
                           "успешно заблокирован.')]"

    class Click():
        BTN_BACK_FIND_RES = "//button[contains(.,'Вернуться к результатам поиска')]"
        BTN_SAVE = "//button[contains(.,'Сохранить')]"
        BTN_CREATE_USER = "//a[contains(@href,'#/users/new/') and contains(.,'Создать учетную запись')]"
        ROLE_LIST = "//label[contains(.,'Роль пользователя')]/..//select[@name='role']"
        SELECT_ROLE = "//label[contains(.,'Роль пользователя')]/..//select[@name='role']/option[contains(.,'%s')]"
        SELECT_PARAM = "//select[@name='param']/option[contains(.,'%s')]"
        DATE_FROM = "//label[contains(.,'Дата создания с')]/../div/input[@name='iDateFrom']"
        DATE_TO = "//label[contains(.,'по')]/../div/input[@name='iDateTo']"
        BTN_FIND = "//button[contains(.,'Найти')]"
        BTN_DAY_ACTIVE = "/..//div[@ng-switch='datepickerMode']//button[@class='btn btn-default btn-sm active']"
        BTN_DAY_FIRST_IN_CALENDAR = "/..//div[@ng-switch='datepickerMode']//tr[@class][1]" \
                                    "/td[@id][1]/button[@class='btn btn-default btn-sm']"
        PAG_NEXT = "//a[contains(.,'След.')]"
        BTN_EDIT = "//a[contains(@href,'#/users/id%s') and contains(.,'Редактировать')]"

        CHANGE_STATUS = "//div[contains(@class,'btn btn-xs action ng-binding btn-') and contains(.,'%s')]"

    class Input():
        FIELD_FIND = "//input[@type='text' and @placeholder='Найти...']"
        FIELD_NAME = "//input[@id='displayName' and @required and @maxlength=200]"
        FIELD_EMAIL = "//input[@id='email']"
        FILED_CITY = "//input[@id='city']"
        FIELD_PHONE = "//input[@id='phone' and @maxlength=11]"
        FIELD_PASS = "//input[@id='password' and @required]"
        FIELD_PASS_EDIT = "//input[@id='password' and not(@required)]"
        RADIO_MAN = "//label[@class='radio-inline' and contains(.,'Мужской')]"
        RADIO_WOMAN = "//label[@class='radio-inline' and contains(.,'Женский')]"
        GENDER = {"MAN": RADIO_MAN, "WOMAN": RADIO_WOMAN}
        FIELD_ROLE = "//select[@id='role']/option[contains(.,'%s')]"


class BackInvitesPage(MainClass):

    class Path():
        URL_INVITES = "/#/invites/"
        URL_INVITES_SINGLE = "/#/invites/single"
        URL_INVITES_MULTI = "/#/invites/multi"

    class Check():
        BTN_TITLE = "//a[@class='btn btn-primary' and contains(.,'Создать уникальный промо-код') or " \
                    "contains(.,'Создать многоразовый промо-код')]"
        TITLE_SINGLE = "//h3[contains(.,'Создание одноразового промо-кода')]"
        TITLE_MULTI = "//h3[contains(.,'Создание многоразового промо-кода')]"

    class Click():
        pass

    class Input():
        pass


class BackCmsWaresPage(MainClass):

    class Path():
        URL_CMS_WARES = "/#/cms-wares"

    class Check():
        pass

    class Click():
        BTN_ADD_WARE = "//a[contains(@href,'#/cms-wares/new') and contains(.,'Добавить товар')]"

    class Input():
        pass