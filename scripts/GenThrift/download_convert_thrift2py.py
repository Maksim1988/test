# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------
#         Скачать файл thrift для генерации.
# ----------------------------------------------------------------------------------------
import os
import platform
import sys
from tempfile import NamedTemporaryFile
from urllib2 import urlopen
import shutil
import time

__author__ = 's.trubachev'


VERSION_THRIFT = "0.9.2"
NAME_FILE = "thrift-%s" % VERSION_THRIFT
LINUX_URL = "http://apache-mirror.rbc.ru/pub/apache/thrift/%s/%s.tar.gz" % (VERSION_THRIFT, NAME_FILE)
WINDOWS_URL = "http://apache-mirror.rbc.ru/pub/apache/thrift/%s/%s.exe" % (VERSION_THRIFT, NAME_FILE)

# GIT Checkout
# then... cd thrift
GIT_CLONE_THRIFT = "git clone https://git-wip-us.apache.org/repos/asf/thrift.git thrift"


DEST_FILE_NAME = 'THRIFTEXEC'
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = HERE[:HERE.find('scripts')]  # корень относительно папки "scripts"
LOCAL_TEMP = ROOT_PATH + 'tmp'


PLATFORM_OS = ".exe" if platform.uname()[0] == "Windows" else ".tar.gz"
THRIFTEXEC_URL_BASE = "http://apache-mirror.rbc.ru/pub/apache/thrift/%s/%s%s" % (VERSION_THRIFT, NAME_FILE, PLATFORM_OS)


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


class RequestProgressWrapper():
    """ Simple helper for displaying file download progress;
    if works with file-like objects"""
    def __init__(self, obj):
        self.obj = obj
        self.total_size = float(obj.headers['content-length'].strip())
        self.url = obj.url
        self.bytes_so_far = 0

    def read(self, length):
        self.bytes_so_far += length
        percent = self.bytes_so_far / self.total_size
        percent = round(percent * 100, 2)
        sys.stdout.write(
            encode_print("%s: загружено %d из %d байт (%0.f%%)\r") %
            (self.url, self.bytes_so_far, self.total_size, percent))
        sys.stdout.flush()
        return self.obj.read(length)

    def __del__(self):
        sys.stdout.write('\n')


def download_ziped_resource(url, name):
    """ Скачать и разархивировать исполняемый thrift-файл.
    Скачиваем архив thrift-файла, распаковываем его и копируем в папку LOCAL_TEMP фреймворка.
    :param url: ссылка для скачивания thrift-файла
    :param name: наименование файла thrift-файла, которое мы установим
    :return: путь до thrift-файла
    """
    opj = os.path.join
    path_storage = opj(LOCAL_TEMP, name) if platform.uname()[0] != "Windows" else opj(LOCAL_TEMP, name + '.exe')

    if os.path.exists(path_storage):
        print encode_print(u"Warning: Исполняемый файл файл для thrift-генерации уже загружен!")
        return path_storage

    req = urlopen(url)
    data_destination = NamedTemporaryFile(delete=False)

    with data_destination as f:
        shutil.copyfileobj(RequestProgressWrapper(req), f.file)
        f.close()  # Закрываем файл, иначе файл будет занят другим процессом

        def unzip_file(tfile, local_temp):
            """ Разархивировать zip-файл.
            :param tfile: файл
            :param local_temp: локальный путь
            :return: путь до временного хранилища
            """
            import tarfile
            tarredgzippedFile = tarfile.TarFile.open(tfile.name, 'r:gz')
            tarredgzippedFile.extractall(local_temp)
            name = tarredgzippedFile.members[0].name
            tarredgzippedFile.close()
            return os.path.join(local_temp, name)

        def normal_file(tfile, local_temp):
            """ Файл, оставляем в таком виде, в каком есть.
            :param tfile: файл
            :param local_temp: локальный путь
            :return: путь до временного хранилища
            """
            return os.path.join(LOCAL_TEMP, f.name)

        path_source = unzip_file(f, LOCAL_TEMP) if platform.uname()[0] != "Windows" else normal_file(f, LOCAL_TEMP)

        # переименновываем файл(директорию)
        os.rename(path_source, path_storage)

        try:
            os.remove(f.name)
        except WindowsError, tx:
            print encode_print(u"ОШИБКА! Удалить временный файл не удалось.")
            print tx
            print encode_print(u"Продолжение работы программы.")

    # Если это линукс, выставляем права на файл
    if platform.uname()[0] != "Windows":
        os.chmod(path_storage, 0o755)
    return path_storage


if __name__ == '__main__':

    print encode_print(u"Начинаем загрузку исполняемого файл для thrift-генерации.")
    print encode_print(u"Имя: %s" % DEST_FILE_NAME)
    time.sleep(3)
    downloaded_file = download_ziped_resource(THRIFTEXEC_URL_BASE, DEST_FILE_NAME)
    print encode_print(u"Путь до исполняемого файла: %s" % downloaded_file)
    print encode_print(u"Загрузка завершена.")
    time.sleep(5)

