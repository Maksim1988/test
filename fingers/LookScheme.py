# -*- coding: utf-8 -*-
import ConfigParser
import sys
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication
from this_looksheme import Ui_MainWindow


__author__ = 's.trubachev'

#  C:\Python27\Lib\site-packages\PySide\scripts\uic.py "C:\Data\ToDeveloper\bitbucket\LookScheme\rs_looksheme.ui" -o "C:\Data\ToDeveloper\bitbucket\LookScheme\looksheme.py"


class MainWinUI(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWinUI, self).__init__()
        self.setupUi(self)
        self.cord.signal.connect(self.push_table)

    @staticmethod
    def config_env_data():
        """ Получить конфигурационные данные.
        :return: ссылка на объект конфигурационного файла
        """
        config_raw = ConfigParser.ConfigParser()
        config_raw.read('../env.cfg')
        return config_raw

    def get_env_schemes(self):
        """ Получить все схемы.
        :return: список схем.
        """
        config_raw = self.config_env_data()
        return config_raw.sections()

    def get_data_scheme(self, name_scheme):
        """ Получить данные одной схемы.
         :param name_scheme: название схемы
        :return: словарь данных.
        """
        config_raw = self.config_env_data()
        return dict(config_raw.items(name_scheme))

    @staticmethod
    def set_group(data):
        """ Установить группировку сырых данных.
        :param data: сырые данные
        :return: сгруппированные данные
        """
        dict_equals = {"db": "Database", "ssh": "SSH", "metric": "DashBoard", "front": "FrontOffice",
                       "back_base": "BackOffice", "nutcracker": "Connector", "static": "Data",
                       "warehouse": "Worker", "accounting": "Worker", "categories": "Worker",
                       "messaging": "Worker", "session": "Worker", "favorites": "Worker", "serv": "Server",
                       "crud": "Worker"}
        func_equals = lambda param, equal_elem: [v for n, v in equal_elem.iteritems() if param.find(n) == 0]
        build_dict = lambda x, y, z: {"type": x[0] if len(x) != 0 else "Not found", "name": y, "value": z}
        mas = [build_dict(func_equals(name, dict_equals), name, value) for name, value in data.items()]
        return mas

    @QtCore.Slot(str)
    def push_table(self, scheme):
        """ Заполняем таблицу.
        :param scheme: название схемы
        """
        source_data = self.get_data_scheme(scheme)
        grouped_data = self.set_group(source_data)
        sorted_data = sorted(grouped_data, key=lambda x: x["name"][:15])  # 15 - кол-во символов по к-ым идет сортировка
        self.tableWidget.setRowCount(len(sorted_data))
        for num, index in enumerate(sorted_data):
            self.add_item(index, num)

    def add_item(self, data, num=0):
        """ Добавить строку в таблицу.
        :param data: словарь с данными
        :param num: номер строки
        """
        self.tableWidget.setItem(num, 0, QtGui.QTableWidgetItem("{0}".format(data["type"])))
        self.tableWidget.setItem(num, 1, QtGui.QTableWidgetItem("{0}".format(data["name"])))
        self.tableWidget.setItem(num, 2, QtGui.QTableWidgetItem("{0}".format(data["value"])))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWinUI()
    window.show()
    app.exec_()


