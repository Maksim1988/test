# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------
#         Выводит количество товаров по категориям из БД.
# ----------------------------------------------------------------------------------------
import platform
import time
import psycopg2
import psycopg2.extras

__author__ = 's.trubachev'


ENV_HOST = "dev-db.oorraa.pro"
ENV_PORT = 5432
ENV_NAME = "accounting_test1"
ENV_LOGIN = "cat_user_test1"
ENV_PASWORD = "shahtuo0Cu8k"


def encode_print(msg):
    """ Вывод строки под кодировку консоли.
    :param msg: строка для вывода
    """
    if platform.uname()[0] != "Windows":
        if type(msg) == unicode:
            return msg
        else:
            return msg.encode("utf8")
    else:
        return msg.encode("cp866")


def close(connection, cursor):
    """ Закрываем соединение.
    :param cursor: ссылка на курсор
    """
    cursor.close()
    connection.close()
    print encode_print(u"Содинение с базой закрыто.")


def connect(host, port, name, user, passwd, cursor_view="dict"):
    """ Коннектимся с базой.
    :param cursor_view: вид в котором возвращается ответ (по умолчанию - dict, словарь)
    :return: возвращаем ссылку на соединение и курсор
    """
    cursor = None
    conn = None
    try:
        factory = psycopg2.extras.DictCursor if cursor_view == "dict" else psycopg2.extras.NamedTupleCursor
        conn = psycopg2.connect(host=host, port=port, dbname=name, user=user, password=passwd, cursor_factory=factory)
        cursor = conn.cursor()
    except Exception, tx:
        print encode_print(u"Ошибка соединения с базой PostgreSQL.")
        print str(tx)
    print encode_print(u"Соединение с базой PostgreSQL произведено.")
    print encode_print(u"  Хост: %s:%s" % (ENV_HOST, ENV_PORT))
    print encode_print(u"  Схема: %s" % ENV_NAME)
    print encode_print(u"  Пользователь: %s" % ENV_LOGIN)
    return conn, cursor


def execute(connection, cursor, request, cursor_view="dict"):
    """ Выполнить запрос.
    :param cursor: ссылка на соединение
    :param request: запрос на выполнение
    :return: результат операции
    """
    what_cursor_view = lambda view, element: dict(element) if view == "dict" else element
    try:
        cursor.execute(request)
        result1 = cursor.fetchall()
        print encode_print(u"  Тип: Fetchall rows")
        return [what_cursor_view(cursor_view, elem) for elem in result1]
    except Exception, tx:
        print encode_print(u"Ошибка при работе скрипта!")
        print str(tx)
        raise AssertionError(str(tx))
    finally:
        close(connection, cursor)

if __name__ == '__main__':

    print encode_print(u"--== Подсчет товаров по категориям. ==--")
    time.sleep(3)

    connect, cursor_now = connect(host=ENV_HOST, port=ENV_PORT, name=ENV_NAME, user=ENV_LOGIN, passwd=ENV_PASWORD)
    req = """SELECT id FROM categories.catalog_categories;"""
    result = execute(connect, cursor=cursor_now, request=req)
    result = [category["id"] for category in result]
    print encode_print(u"Количество категорий в БД: %s" % len(result))

    print encode_print(u"Подсчёт завершен.")
    time.sleep(5)