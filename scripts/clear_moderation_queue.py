# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------
#         Очистить очередь модерации.
# ----------------------------------------------------------------------------------------
import platform
import subprocess
import time
import sys


__author__ = 's.trubachev'


def encode_print(msg):
    """ Вывод строки под кодировку консоли.
    :param msg: строка для вывода
    """
    try:
        if platform.uname()[0] != "Windows":
            if type(msg) == unicode:
                return msg.encode("utf8") # return msg - должно быть так, но не работает при вызове из Jenkins
            else:
                return msg.encode("utf8")
        else:
            return msg.encode("cp866")
    except Exception:
        return u"Warning! Cannot convert conclusion. The error is caught, the continuation of the work."


def check_install_package(package):
    """ Порверить, что в системе установлены необходимые пакеты.
    Выполняем команды.
    Получаем вывод этой команды.
    :param package: имя пакета
    :return: информация по пакету
    """
    cmd = 'pip show %s'
    try:
        present = subprocess.Popen(cmd % package, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception, kx:
        print encode_print(u"Ошибка! При проверке пакетов возник сбой. \n"
                           u"Проверьте правильность команды: %s" % cmd % package)
        print kx
        return False

    # Получаем вывод команды
    lines = [line for line in present.stdout.readlines()]
    result_output = dict()
    for l in lines[1:]:
        num = l.find(":")
        result_output.update({l[:num]: l[num+1:].strip().strip("\n")})
    return result_output


def force_package():
    """ Перебор списка пакетов.
    :return: флаг результата работы
    """
    packages = ["thrift"]
    flag = True
    for name in packages:
        result_install = check_install_package(name)
        if result_install is False:
            print encode_print(u"Внимание! Отключение проверки зависимостей.")
            return True
        elif len(result_install) == 0:
            print encode_print(u"Ошибка! Не найден пакет %s" % name)
            flag = False
        elif len(result_install) != 0:
            if "Version" not in result_install:
                print encode_print(u"Внимание! Не найдена версия пакета %s" % name)
            elif len(result_install["Version"]) == 0:
                print encode_print(u"Внимание! Не найдена версия пакета %s" % name)
                # TODO: может быть следует проверять ещё и версию пакета?!
    return flag


def generator_req(thrift_methods, stock, moderation):
    """ Генерация запроса для выборки товаров на модерацию.
    :param stock: статус состояня
    :param moderation: статус модерации
    :return: запрос
    """
    pagination = thrift_methods.Common.ttypes.PaginationDto(limit=count_wares, offset=0)
    main_search = thrift_methods.SearchRequestDto(pagination=pagination, allowedModerationStates=[moderation],
                                                  allowedStockStates=[stock])
    return main_search


def get_wares(t_client, req, msg):
    """ Получить список товаров.
    :param req: запрос
    :param msg: сообщение для вывода
    :return: товары
    """
    print encode_print(msg)
    st1_wares = t_client.search(req)
    print encode_print(u"  Получено товаров: %s" % st1_wares.totalCount)
    print encode_print(u"  Очистка очереди товаров.")
    return st1_wares


def clear_queue(w_client, list_wares, moderator_id=28):
    """ Очистить очередь.
    :param enumeration_wares: товары
    """
    def return_runner(elem=None):
        if elem == None:
            return u"*"
        elif elem == u"*":
            return u"|"
        elif elem == u"|":
            return u"/"
        elif elem == u"/":
            return u"-"
        elif elem == u"-":
            return u"*"

    t = None
    for ware in list_wares:
        w_client.makeModeration(ware.wareId, True, moderator_id)
        t = return_runner(t)
        try:
            sys.stdout.write(encode_print(u"  Выполняется: ") + u"%s\r " % t)
        except Exception:
            print encode_print(u"  Выполняется...")
        time.sleep(0.05)
    print encode_print(u"  Завершено!        ")


if __name__ == '__main__':
    print encode_print(u"Проверка установленных пакетов для корректной работы скрипта..")
    time.sleep(3)
    if force_package():
        print encode_print(u"Проверка установленных пакетов закончена.\n")
        try:
            # импортируем необходимые библиотеки
            import os
            HERE = os.path.dirname(os.path.abspath(__file__))
            ROOT_WORK = HERE.replace("scripts", "")[:-1]
            sys.path.append(ROOT_WORK)
            import gen_py.WaresIndexWorker.WaresIndexWorker as index_thrift_methods
            import gen_py.WarehouseWorker.WarehouseWorker as warehouse_thrift_methods
            from thrift import Thrift
            from thrift.transport import TSocket
            from thrift.transport import TTransport
            from thrift.protocol import TBinaryProtocol

            try:
                index_thost = "test-app1.oorraa.pro"
                index_tport = 10060

                warehouse_thost = "test-app1.oorraa.pro"
                warehouse_tport = 10002

                count_wares = 5000
                msg1 = u"  Шаг 1. Выборка товаров с условиями: BELIEVED=1, PUBLISHED=2"
                msg2 = u"  Шаг 2. Выборка товаров с условиями: WAITING=3, HIDDEN=3"

                print encode_print(u"Устанавливается соединение: %s:%s" % (index_thost, index_tport))

                index_socket = TSocket.TSocket(index_thost, index_tport)
                index_thrift_transport = TTransport.TFramedTransport(index_socket)
                index_protocol = TBinaryProtocol.TBinaryProtocol(index_thrift_transport)
                index_client = index_thrift_methods.Client(index_protocol)
                index_thrift_transport.open()

                warehouse_socket = TSocket.TSocket(warehouse_thost, warehouse_tport)
                warehouse_thrift_transport = TTransport.TFramedTransport(warehouse_socket)
                warehouse_protocol = TBinaryProtocol.TBinaryProtocol(warehouse_thrift_transport)
                warehouse_client = warehouse_thrift_methods.Client(warehouse_protocol)
                warehouse_thrift_transport.open()


                # Шаг 1. ModerationStates["BELIEVED"] = 1, StockStates["PUBLISHED"] = 2
                search_req = generator_req(thrift_methods=index_thrift_methods, stock=2, moderation=1)
                wares = get_wares(index_client, search_req, msg1)
                clear_queue(warehouse_client, wares.wares)

                # Шаг 2. ModerationStates["WAITING"] = 3, StockStates["HIDDEN"] = 3
                search_req = generator_req(thrift_methods=index_thrift_methods, stock=3, moderation=3)
                wares = get_wares(index_client, search_req, msg2)
                clear_queue(warehouse_client, wares.wares)

                index_thrift_transport.close()
                warehouse_thrift_transport.close()
                print encode_print(u"Работа скрипта завершена.")

            except Exception, zx:
                print encode_print(u"Ошибка! Попытка очистить очередь модерации закончилась неудачей.")
                print "Error: " + str(zx)
        except Exception, tx:
            print encode_print(u"Ошибка! Импорт модулей фреймворка для корректной работы скрипта закончилася неудачей.")
            print "Error: " + str(tx)
    else:
        print encode_print(u"Ошибка: Работа скрипта не завершена. Необходимо устновить зависимости.")
    time.sleep(5)
