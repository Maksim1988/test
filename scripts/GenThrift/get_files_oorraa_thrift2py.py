# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------
#         Скачать файлы Thrift для конвертации из в python-файлы.
# ----------------------------------------------------------------------------------------
import platform
import paramiko

__author__ = 's.trubachev'


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


def connect_by_user_password(host, user, passwd, port):
    """ Коннектимся к удалённой консоли.
    :return: возвращаем ссылку на терминал
    """
    try:
        client = paramiko.SSHClient()
        type_host_key = paramiko.AutoAddPolicy()
        client.set_missing_host_key_policy(type_host_key)  # add ssh-key in list keys — file .ssh/known_hosts
        client.connect(hostname=host, username=user, password=passwd, port=int(port))
        print encode_print(u"Открываем SSH соеденение.")
        return client
    except Exception, tx:
        msg_error = encode_print(u"Ошибка: SSH соеденение не открыто!")
        print msg_error
        print tx
        raise AssertionError(msg_error)


def connect_by_key_file():
    return 0


def close_connect(client=None, channel=None):
    """ Закрываем соединение.
    """
    try:
        if channel:
            channel.close()
        if client:
            client.close()
    except Exception, tx:
        print encode_print(u"Ошибка: SSH соединение не удалось успешно закрыть.")
        print str(tx)
    print encode_print(u"SSH соединение успешно закрыто")


def command_execution(host, user, passwd, port, cls, keyfile=None, flag_output=True):
    """ Выполнить оперцию на удалённой консоли.
    :param cls: команда, которую необходимо запустить
    :param flag_output: если флаг False, то результат не возвращаем
    :return: Результат выполненной операции, либо ничего
    """
    if passwd is not None:
        client = connect_by_user_password(host, user, passwd, port)
    elif keyfile is not None:
        client = connect_by_key_file()
    else:
        msg_error = u"Не найден пароль или ключ-файл для соеденения!"
        print encode_print(msg_error)
        raise AssertionError(msg_error)
    try:
        print encode_print(u"Выполнение: %s." % cls)
        if flag_output is True:
            stdin, stdout, stderr = client.exec_command("""%s""" % cls)
            data = dict(stdout=stdout.read(), stderr=stderr.read())
            if data["stderr"] != '':
                print encode_print(u"Процесс выполнения прерван: %s" % str(data))
                raise AssertionError(u"Ошибка: %s" % str(stderr))
            print encode_print(u"Процесс выполнения успешен: %s" % str(data))
            return data
        else:
            client.exec_command("""%s""" % cls)
            print encode_print(u"Процесс выполнения успешен.")
            return None
    except Exception, tx:
        print str(tx)
        raise AssertionError(str(tx))
    finally:
        print encode_print(u"Соединение закрыто")
        close_connect(client)

def con():
    import requests
    import json
    import ssl
    r = requests.get('https://git.home.oorraa.net/internal-api/oorraa-thrift')
    return r

def ssl_connection():
    pass

if __name__ == '__main__':
    print encode_print(u"Соединение..")
    ssh_link = "git@git.home.oorraa.net:internal-api/oorraa-thrift.git"
    https_link = "https://git.home.oorraa.net/internal-api/oorraa-thrift"
    ssh_link = "ssh://git@git.home.oorraa.net:2795/qa-team/api-tests.git"
    ssh_link = "ssh://git@git.home.oorraa.net/qa-team/api-tests.git"

    #print con()
    command_execution(host=ssh_link,
                      user="s.trubachev",
                      passwd="1835&yu!j*00",
                      port=2795,
                      cls="ls")
