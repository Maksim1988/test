# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Класс работы с PostgreSQL для воркера Accounting.
#--------------------------------------------------------------------
from support.utils.common_utils import run_on_prod
from support.utils.db_postgresql import ClassSaveLinkPostgreSQL, execute_sql


__author__ = 's.trubachev'


class ClassGetAccountingSql(ClassSaveLinkPostgreSQL):

    @execute_sql
    def get_user_account_info_by_id(self, user_id):
        """ Получить информацию аккаунта пользователя по его идентификатору.
        :param user_id: идентификатор пользователя
        :return: данные таблицы account_info
        """
        return """SELECT * FROM accounts WHERE account_details_id = %i;""" % user_id

    @execute_sql
    def get_users_by_status(self, status='ENABLED', limit=100):
        """ Получить данные пользователей.
        :param limit: количество возвращаемых записей
        :return: список данных пользователей
        """
        #return """SELECT * FROM group_members limit %i;""" % limit

        query = """SELECT * FROM group_members JOIN account_info ON account_info.account_id = group_members.id
                   AND account_info.account_status = '%s' limit %i;""" % (status, limit)
        return query

    @execute_sql
    def get_user_by_id(self, user_id):
        """ Получить данные пользователя по его идентификатору.
        :param user_id: идентификатор пользователя
        :return: данные пользователя
        """
        return """SELECT * FROM group_members WHERE id=%i;""" % user_id

    @execute_sql
    def get_user_by_login(self, login):
        """ Получить данные пользователя по его логина.
        :param login: логин пользователя
        :return: данные пользователя
        """
        return """SELECT * FROM group_members WHERE login='%s';""" % login

    @execute_sql
    def get_users_by_part_phone(self, part_phone):
        """ Получить пользователей по части их номера.
        :param part_phone: часть номера телефона
        :return: данные пользователей у которых присутствуют заданные цифры в телефоне
        """
        return """SELECT * FROM group_members as gm WHERE gm.phone LIKE ('%""" + part_phone + """%');"""

    @execute_sql
    def get_validate_user(self, group_id, status, length_phone=11):
        """ Выбор валидного пользователя из БД.
        :param group_id: идентификатор группы
        :param status: статус
        :param length_phone: длина номера телефона
        :return: данные таблицы account_details
        """
        p = """SELECT phone, auths.code_value, id, display_name, auths.salt FROM account_details
                LEFT OUTER JOIN auths ON account_details.id = auths.account_details_id
                WHERE auths.salt IS NOT NULL AND phone LIKE """ + "'7999%'" + """ AND LENGTH(phone)=%i
                AND id IN
                (SELECT account_details_id FROM accounts WHERE account_status = '%s' and account_details_id IN (
                SELECT account_details_id FROM account_details_permissions GROUP BY account_details_id
                HAVING SUM(permission_id) = %s));""" % (length_phone, status, group_id)
        return p

    @execute_sql
    def get_not_enabled_user(self, status, length_phone=11):
        """ Выбор валидного пользователя из БД.
        :param status: статус
        :param length_phone: длина номера телефона
        :return: данные таблицы account_details
        """
        p = """SELECT phone, auths.code_value, id, display_name, auths.salt FROM account_details
                LEFT OUTER JOIN auths ON account_details.id = auths.account_details_id
                WHERE auths.salt IS NOT NULL AND phone LIKE """ + "'7%'" + """ AND LENGTH(phone)=%i
                AND id IN
                (SELECT account_details_id FROM accounts WHERE account_status = '%s');""" % (length_phone, status)
        return p

    @execute_sql
    def get_validate_seller(self, group_id, status, length_phone=11, template_phone=7666):
        """ Выбор валидного пользователя из БД.
        :param group_id: идентификатор группы
        :param status: статус
        :param length_phone: длина номера телефона
        :param template_phone: шаблон для выборки телефона
        :return: данные таблицы account_details
        """
        p = """SELECT phone, auths.code_value, id, display_name, auths.salt FROM account_details
                LEFT OUTER JOIN auths ON account_details.id = auths.account_details_id
                WHERE auths.salt IS NOT NULL AND phone LIKE '""" + str(template_phone) + '%' + """' AND LENGTH(phone)=%i
                AND id IN
                (SELECT account_details_id FROM account_details_permissions WHERE permission_id in (%s) AND account_details_id IN
                (SELECT account_details_id FROM accounts
                        WHERE account_status = '%s'));""" % (length_phone, group_id, status)
        return p

    @execute_sql
    def get_users_with_status(self, status='ENABLED', template_phone=7666):
        """ Вернуть пользователей с определённым статусом, корректным телефоном и солью в пароле.
        :param template_phone: шаблон для выборки телефона
        :return: данные таблицы account_details
        """

        p = """SELECT phone, auths.code_value, auths.salt, display_name, avatar_id, id FROM account_details
                  LEFT OUTER JOIN auths ON account_details.id = auths.account_details_id
                  WHERE phone LIKE '""" + str(template_phone) + """%' AND LENGTH(phone)=11
                    AND auths.salt IS NOT NULL AND id IN (SELECT account_details_id FROM accounts""" + """
                    WHERE account_status = '%s');""" % status
        return p

    @execute_sql
    def get_user_by_account_id(self, user_id):
        """ Получить данные таблицы account_details и auths.
        :param user_id: идентификатор пользователя с товарами
        :return: данные таблицы account_details
        """
        p = """SELECT * FROM account_details
                LEFT OUTER JOIN auths ON account_details.id = auths.account_details_id
                WHERE id = '%s';""" % user_id
        return p

    @execute_sql
    def get_user_by_criteria(self, account_status, criteria):
        """ Получить данные таблицы account_details по любому критерию
        :param seller_id: идентификатор продавца с товарами
        :return: данные таблицы account_details
        """
        p = """SELECT * FROM account_details LEFT OUTER JOIN auths ON account_details.id = auths.account_details_id
               LEFT OUTER JOIN accounts ON accounts.account_details_id = auths.account_details_id
               WHERE accounts.account_status = '%s' AND %s;""" % (account_status, criteria)
        return p

    @execute_sql
    def get_user_by_criteria_only(self, criteria):
        """ Получить данные таблицы account_details по любому критерию
        :param seller_id: идентификатор продавца с товарами
        :return: данные таблицы account_details
        """
        p = """SELECT * FROM account_details LEFT OUTER JOIN auths ON account_details.id = auths.account_details_id
               LEFT OUTER JOIN accounts ON accounts.account_details_id = auths.account_details_id
               WHERE %s;""" % criteria
        return p

    @execute_sql
    def get_user_by_role(self, need_role, not_role):
        """ Получить идентификатор пользователя нужной роли
        :param need_role: нужная роль
        :param not_role: у пользователя не должно быть этой роли
        :return: данные таблицы account_details_permissions
        """
        p = """SELECT account_details_id FROM  account_details_permissions WHERE permission_id in (%s) AND account_details_id
               not in (SELECT account_details_id FROM  account_details_permissions WHERE permission_id in (%s));""" % (need_role,
                                                                                                              not_role)
        return p

    @execute_sql
    def get_data_accounts_by_user_id_and_status(self, account_details_id, status='ENABLED'):
        """ Получть пароль, телефон, соль.
        :param account_details_id: идентификатор
        :param status: статус пользователя
        """
        # TODO: исправить название метода
        p = """SELECT * FROM account_details LEFT OUTER JOIN auths ON account_details.id = auths.account_details_id
               LEFT OUTER JOIN accounts ON accounts.account_details_id = auths.account_details_id
                         AND accounts.account_status = '%s' WHERE account_details.id = %s""" % (status,
                                                                                                account_details_id)
        return p

    @execute_sql
    def get_data_user_by_phone(self, phone):
        """ Получить данные аккаунта пользователя по его номеру телефона.
        :param user_id: идентификатор пользователя
        """
        # TODO: исправить название метода
        p = """SELECT * FROM account_details LEFT OUTER JOIN auths ON account_details.id = auths.account_details_id
               LEFT OUTER JOIN accounts ON accounts.account_details_id = auths.account_details_id
                          WHERE account_details.phone = '%s'""" % phone
        return p

    @execute_sql
    def get_data_user_by_id(self, user_id):
        """ Получить данные аккаунта пользователя по его иденификатору.
        :param user_id: идентификатор пользователя
        """
        # TODO: исправить название метода
        p = """SELECT * FROM account_details LEFT OUTER JOIN auths ON account_details.id = auths.account_details_id
               LEFT OUTER JOIN accounts ON accounts.account_details_id = auths.account_details_id
                          WHERE account_details.id = '%s'""" % user_id
        return p

    @execute_sql
    def get_for_restore(self, status='ENABLED'):
        # TODO: описание
        p = """SELECT phone, auths.code_value, auths.salt, display_name, avatar_id, id FROM account_details
            LEFT OUTER JOIN auths ON account_details.id = auths.account_details_id
            WHERE phone like """ + "'76669%'" + """ and LENGTH(phone)=11 and auths.salt is not null and id in
            (SELECT account_details_id FROM accounts WHERE account_status = '%s');""" % status
        return p

    @execute_sql
    def get_all_user_info_by_id(self, user_id):
        # Получить всю инфу о пользователе
        p = """SELECT * FROM account_details
            LEFT OUTER JOIN auths ON account_details.id = auths.account_details_id
            WHERE id = '%s';""" % user_id
        return p

    @execute_sql
    def get_user_role_by_id(self, user_id):
        # Получить список ролей пользователя
        p = """SELECT * FROM permissions WHERE id IN
               (SELECT permission_id FROM account_details_permissions WHERE account_details_id = '%s');""" % user_id
        return p

    @execute_sql
    def get_users_with_display_name_by_id(self, user_id, limit=10):
        # Получить список пользователей с непустыми display_name и не равными пользователю под которым залогинены
        p = """SELECT * FROM account_details WHERE display_name IS NOT NULL AND id != '%s' ORDER BY RANDOM()
               LIMIT %i;""" % (user_id, limit)
        return p

    @execute_sql
    def get_users_with_inn_kpp_ogrn_by_id(self, user_id, limit=10):
        # Получить список пользователей с непустыми ИНН, КПП, ОГРН и не равными пользователю под которым залогинены
        p = """SELECT * FROM account_details WHERE inn IS NOT NULL AND kpp IS NOT NULL AND ogrn IS NOT NULL AND
               id != '%s' ORDER BY RANDOM() LIMIT %i;""" % (user_id, limit)
        return p

    @execute_sql
    def get_users_with_bank_info_by_id(self, user_id, limit=10):
        # Получить список пользователей с непустыми Банковскими реквизитами и не равными пользователю под
        # которым залогинены
        p = """SELECT * FROM account_details WHERE bank_bic IS NOT NULL AND bank_name_and_address IS NOT NULL AND
               bank_account IS NOT NULL AND bank_correspondent_account IS NOT NULL AND
               id != '%s' ORDER BY RANDOM() LIMIT %i;""" % (user_id, limit)
        return p

    @execute_sql
    def get_users_by_id_and_permissions(self, user_id, is_permissions, not_is_permissions):
        """
        Получить пользователя по идентификатору и правам
        :param id:
        :param is_permissions:
        :param not_is_permissions:
        :return:
        """
        return """SELECT ad.id FROM account_details AS ad
        LEFT OUTER JOIN account_details_permissions AS adp ON ad.id = adp.account_details_id
        LEFT OUTER JOIN accounts AS a ON a.account_details_id = adp.account_details_id
        WHERE ad.id in (%s) and adp.permission_id in (%s) and adp.permission_id not in (%s)  GROUP BY ad.id""" % \
               (user_id, is_permissions, not_is_permissions)

    @execute_sql
    def get_roles_by_id(self, account_details_id):
        """ Получить роли пользователя.
        :param account_details_id: идентификатор пользователя
        :return: список ролей пользователя
        """
        p = "SELECT permission_id FROM account_details_permissions WHERE account_details_id = %s" % account_details_id
        return p

    @execute_sql
    def get_provided_filter_by_id(self, category_id):
        """ Получить маркер спец-категории
        :param category_id: идентификатор категории
        :return: название маркера
        """
        p = "SELECT * FROM categories.provided_filters WHERE category_id = %s" % category_id
        return p

    @execute_sql
    def get_provided_filter_by_criteria(self, criteria):
        """ Получить маркер спец-категории
        :param criteria: кусок sql запроса
        :return: название маркера
        """
        p = "SELECT * FROM categories.provided_filters WHERE %s" % criteria
        return p

    @execute_sql
    def get_shop_details_by_shop_id(self, shop_id):
        """ Получить нформация о магазине
        :param shop_id: идентификатор магазина
        :return:
        """
        p = "SELECT * FROM shop_details WHERE shop_id = %s" % shop_id
        return p

    @execute_sql
    def get_shop_details_by_criteria(self, criteria):
        """ Получить нформация о магазине
        :param criteria: любая выборка
        :return:
        """
        p = "SELECT * FROM shop_details WHERE %s" % criteria
        return p

    @execute_sql
    def get_all_user_ids(self):
        """ Получить идентификаторы всех пользователей.
        :return:
        """
        p = "SELECT id FROM account_details;"
        return p

    @execute_sql
    def get_user_ids_by_permissions(self, permissions_id):
        """ Получить пользователей заданного типа.
         :param permissions_id: идентификатор роли пользователей
        :return: список словарь с идентификаторами пользователей
        """
        return "SELECT account_details_id FROM account_details_permissions WHERE permission_id = %i;" % permissions_id

    @execute_sql
    def get_users(self, limit=100):
        """ Получить данные пользователей.
        :param limit: количество возвращаемых записей
        :return: список данных пользователей
        """
        return """SELECT * FROM account_details limit %i;""" % limit

    @execute_sql
    def get_users_by_phone(self, phone):
        """ Получить данные пользователей по номеру телефона.
        :param phone: номер телефона
        :return: список пользователей
        """
        p = """SELECT * FROM account_details WHERE phone = '%s'""" % phone
        return p

    @execute_sql
    def get_salt(self, user_id):
        """ Получить соль пользователя.
        :param user_id: идентификатор пользователя
        :return: соль пользователя
        """
        return """SELECT salt FROM auths WHERE account_details_id=%i;""" % user_id

    @execute_sql
    def get_auths(self, user_id):
        """ Получить данные пользователя из таблицы auths по идентификатору пользователя.
        :param user_id: идентификатор пользователя
        :return: соль пользователя
        """
        return """SELECT * FROM auths WHERE account_details_id=%i;""" % user_id

    @execute_sql
    def get_permissions(self, limit=10):
        """ Подучить список разрешений с данными из табл. permissions
        :param limit: лимит списка
        :return: список данных с разрешениями
        """
        return "SELECT * FROM permissions limit %s;" % limit

    @execute_sql
    def get_permissions_with_sort_by_id(self, direction="ASC", offset=0, limit=100):
        """ Подучить список разрешений, сортировка по id.
        :param offset: с какого элемента
        :param limit: лимит списка
        :return: список данных с разрешениями
        """
        return "SELECT * FROM permissions ORDER BY id %s offset %s limit %s;" % (direction, offset, limit)

    @execute_sql
    def get_permissions_by_id(self, permission_id):
        """ Подучить разрешение по идентиф. из табл. permissions
        :param permission_id:идентификатор разрешения
        :return: список данных с разрешениями
        """
        return "SELECT * FROM permissions WHERE id=%i;" % permission_id

    @execute_sql
    def get_permissions_inner_by_id(self, permission_id):
        """ Получает соответствие внутренних пермиссий к обобщающим - группам.
        :param permission_id: идентификатор разрешения
        :return: список соответствий
        """
        return "SELECT * FROM permissions_inner_permissions WHERE permission_id = %s;" % permission_id

    @execute_sql
    def get_accounts_by_criteria(self, criteria):
        """
        Получаем данные из таблицы accounts по любому критерию отсортированные по возрастанию account_details_id
        :param criteria: строка выборки
        :return:
        """
        return "SELECT * FROM accounts WHERE %s order by account_details_id asc" % criteria

    @execute_sql
    def get_account_details_by_criteria(self, criteria):
        """
        Получаем данные из таблицы account_details по любому критерию отсортированные по возрастанию id
        :param criteria: строка выборки
        :return:
        """
        return "SELECT * FROM accounts WHERE account_details_id in " \
               "(SELECT id FROM account_details WHERE %s order by id asc)" % criteria

    @execute_sql
    def get_account_details_permissions_by_criteria(self, criteria):
        """
        Получаем данные из таблицы account_details_permissions по любому критерию отсортированные по возрастанию
        account_details_id
        :param criteria: строка выборки
        :return:
        """
        return "SELECT * FROM account_details_permissions WHERE %s order by account_details_id asc" % criteria

    @execute_sql
    def get_email_statuses_by_email(self, email):
        """
        Получаем данные из таблицы email_statuses по email поьлзователя
        :return:
        """
        return "SELECT * FROM notifications.email_statuses WHERE recipient in ('%s') ORDER BY id DESC;" % email

    @execute_sql
    def get_emails_by_hash(self, value):
        """
        Получаем данные из таблицы emails по hash пользователя
        :return:
        """
        return "SELECT * FROM notifications.emails WHERE body LIKE '%" + value + "%';"

    @execute_sql
    def get_auths_criteria(self, criteria):
        """ Получить данные пользователя из таблицы auths по критерию.
        :param user_id: идентификатор пользователя
        :return: соль пользователя
        """
        return """SELECT * FROM auths WHERE %s;""" % criteria

    @execute_sql
    def get_payment_details_by_user_id(self, user_id):
        """ Получить варианты оплаты из таблицы payment_details по идентификатору продавца.
        :param user_id: идентификатор пользователя
        :return: соль пользователя
        """
        return """SELECT * FROM payment_details WHERE account_details_id=%s;""" % user_id

    @execute_sql
    def get_delivery_details_by_user_id(self, user_id):
        """ Получить способы доставки из таблицы delivery_details по идентификатору продавца.
        :param user_id: идентификатор пользователя
        :return: соль пользователя
        """
        return """SELECT * FROM delivery_details WHERE account_details_id=%s;""" % user_id

    @execute_sql
    def get_all_goods_psql(self, criteria):
        """ Получить товары
        :return: список товаров
        """
        return """SELECT * FROM warehouse.wares WHERE %s;""" % criteria

    @execute_sql
    def get_stock_state_id_by_name(self, status):
        """
        получить идентификаторы статусов товара
        :return:
        """
        return """SELECT id FROM warehouse.d_stock_state WHERE name in (%s);""" % status

    @execute_sql
    def get_parent_categories_visible(self):
        """
        Получить все родительское категории, отображаемые на сайте
        :return:
        """
        return """select * from categories.catalog_categories where id in (select parent_id from
        categories.catalog_categories group by parent_id) and enabled=true and visible=true;"""

    @execute_sql
    def get_management_categories_by_criteria(self, criteria):
        """
        Получить данные из таблицы management_categories по criteria
        :param criteria:
        :return:
        """
        return """SELECT * FROM categories.management_categories WHERE %s;""" % criteria

    @execute_sql
    def get_categories_psql(self, criteria):
        """ Получить категории
        :return: список категорий
        """
        return """SELECT * FROM categories.catalog_categories WHERE %s and enabled=true and visible=true
        order by parent_id asc;""" % criteria

    @execute_sql
    def get_category_name(self, cat_id, locale='ru'):
        """
        получить наименование категории (на сайте)
        :return:
        """
        return """SELECT * FROM localization.localized_values WHERE name = 'cat_cat.""" + str(cat_id) + """.name' and
        locale='""" + locale + """';"""

    @execute_sql
    def get_fav_user_by_user_id(self, user_id):
        """
        Получить избранных пользователей по идентификатору пользователя
        :return: список с данными по товарам
        """
        return """select * from o_account_favorites where account_id = %s;""" % user_id

    @execute_sql
    def get_fav_user_in_cl_user(self, user_id, fav_usr_id):
        """
        Проверить есть ли избранный пользователь у пользователя в контакт листе
        :return: список с данными по товарам
        """
        return """select * from o_account_favorites where account_id=%s and favorites_account_id=%s;""" % (user_id, fav_usr_id)

    @execute_sql
    def get_count_users(self):
        '''
        Получить общее кол-во пользователей из базы
        :return: количество товаров, int
        '''
        return """select count(1) from public.account_details"""

    @execute_sql
    def get_sms(self, phone):
        """ Взять все смс по заданному номеру
        :return: данные о смс
        """
        return """SELECT * FROM communication.o_sms_history WHERE destination='%s' order by create_date desc;;""" % phone


class ClassUpdateAccountingSql(ClassSaveLinkPostgreSQL):
    @execute_sql
    @run_on_prod(False)
    def delete_payment_details_by_user_id(self, user_id):
        """ Удалить все варианты оплаты для пользователя
        :param user_id: идентификатор пользователя
        :return: None
        """
        return """DELETE FROM payment_details WHERE account_details_id=%s;""" % user_id

    @execute_sql
    @run_on_prod(False)
    def delete_delivery_details_by_user_id(self, user_id):
        """ Удалить все варианты оставки для пользователя
        :param user_id: идентификатор пользователя
        :return: None
        """
        return """DELETE FROM delivery_details WHERE account_details_id=%s;""" % user_id

    @execute_sql
    @run_on_prod(False)
    def update_account_details_by_criteria(self, user_id, criteria):
        """ Изменить статус пользователя.
        :param user_id: идентификатор пользователя
        :param user_status: статус пользователя
        :return: None
        """
        return """UPDATE account_details SET %s WHERE id=%s;""" % (criteria, user_id)

    @execute_sql
    @run_on_prod(False)
    def update_shop_details_by_criteria(self, shop_id, criteria):
        """ Изменить статус пользователя.
        :param user_id: идентификатор пользователя
        :param user_status: статус пользователя
        :return: None
        """
        return """UPDATE shop_details SET %s WHERE shop_id=%s;""" % (criteria, shop_id)

    @execute_sql
    @run_on_prod(False)
    def update_user_status(self, user_id, user_status):
        """ Изменить статус пользователя.
        :param user_id: идентификатор пользователя
        :param user_status: статус пользователя
        :return: None
        """
        return """UPDATE account_info SET account_status='%s' WHERE account_id=%s;""" % (user_status, user_id)

    @execute_sql
    @run_on_prod(False)
    def update_user_password_old(self, user_id, passwd_hash):
        """ Изменить пароль пользователя.
        :param user_id: идентификатор пользователя
        :param passwd_hash: хеш пароля пользователя (default: SHA-256)
        :return: None
        """
        # TODO: устаревший метод
        return """UPDATE group_members SET password='%s' WHERE id=%s;""" % (passwd_hash, user_id)

    @execute_sql
    @run_on_prod(False)
    def update_user_password(self, account_id, new_pass):
        """ Изменить пароль пользователя.
        :param new_pass: новый пароль
        :param account_id: идентификатор пользователя
        :return: None
        """
        p = "UPDATE auths SET code_value='%s' WHERE account_details_id='%s';" % (new_pass, account_id)
        return p

    @execute_sql
    @run_on_prod(False)
    def update_user_wants_to_be_seller(self, account_id, new_flag):
        """ Изменить флаг wants_to_be_seller.
        :param new_pass: новый пароль
        :param account_id: идентификатор пользователя
        :return: None
        """
        p = "UPDATE account_details SET wants_to_be_seller='%s' WHERE id='%s';" % (new_flag, account_id)
        return p

    @execute_sql
    @run_on_prod(False)
    def update_user_salt(self, account_id, new_salt):
        """ Изменить соль пользователя.
        :param account_id: идентификатор пользователя
        :param new_salt: новая соль
        :return: None
        """
        p = "UPDATE auths SET salt='%s' WHERE account_details_id='%s';" % (new_salt, account_id)
        return p

    @execute_sql
    @run_on_prod(False)
    def update_passwd_hash_by_phone(self, passwd_hash, phone):
        """ Обновить пароль по номеру телефона.
        :param passwd_hash: хеш пароля
        :param hash: номер телефона
        :return:
        """
        p = """UPDATE auths SET code_value='%s' WHERE account_details_id IN
            (SELECT id FROM account_details WHERE phone='%s');""" % (passwd_hash, phone)
        return p



class ClassForRegistration(ClassSaveLinkPostgreSQL):

    @execute_sql
    @run_on_prod(False)
    def insert_promo_code(self, new_id, status, promo,
                          creation_timestamp=1411475813143,
                          valid_from_timestamp=1411416000000,
                          valid_to_timestamp=2411416000000,
                          optim_lock=0,
                          registration_count=0,
                          registration_limit=1,
                          creation_id=1,
                          comments="test registration seller"):
        """ Создать промокод.
        :param new_id: новый идентификатор промокода
        :param status: статус промокода
        :param promo: значение промокода
        :param creation_timestamp: время создания промокода
        :param valid_from_timestamp: время с которого промокод действует
        :param valid_to_timestamp: время до какого периуда промокод действителен
        :param optim_lock: флаг блокировки промокода
        :param registration_count: сколько раз с этим промокодом зарегистрировалось пользователей
        :param registration_limit: сколько раз успешно можно зарегистрировать с промокодом
        :param creation_id: идентификтор создателя промокода
        :param comments: комментарий к промокоду
        """

        p = """INSERT INTO promo_code VALUES (%s, '%s',%s, %s, %s, '%s', %s, %s,'%s', %s, %s);"""
        return p % (new_id, comments, creation_timestamp, registration_count, registration_limit, status,
                    valid_from_timestamp, valid_to_timestamp, promo, optim_lock, creation_id)

    @execute_sql
    def select_next_val(self):
        """ Получить следующее значение промокода
        """
        return "SELECT nextval('promo_code_id_seq');"


class ClassAccountingSql(ClassGetAccountingSql, ClassUpdateAccountingSql, ClassForRegistration,):
    """ --== Класс буфер. ==--
    Содержит методы группирующие вызовы методов родительских классов.
    """
    pass






