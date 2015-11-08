# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------
#         Генерация файлов thrift для python 2.7
# Перед началом выполнения положить в одну папку скрипт thrift и скрипт генерации.
# см. по запуску скриптов статью: http://www.py-my.ru/post/4bfb3c691d41c846bc000061
# ----------------------------------------------------------------------------------------
import time
import subprocess
#from scripts.GenThrift.download_convert_thrift2py import THRIFTEXEC_PATH


name_thrift_prog = "thrift.exe"

params_thrift = " -r --gen py "

lists_trift_files = ["backend/categories/CategoryTreeCrudWorker.thrift",
                     "backend/categories/CategoryTreeWorker.thrift",
                     "backend/categories/CategoryTreeWorkerConstants.thrift",
                     "backend/accounting/backoffice/AccountingBackOfficeWorker.thrift",
                     "backend/accounting/favorites/FavoritesWorker.thrift",
                     "backend/accounting/favorites/FavoritesConstants.thrift",
                     "backend/accounting/search/AccountingSearchWorker.thrift",
                     "backend/accounting/search/AccountingSearchWorkerConstants.thrift",
                     "backend/accounting/security/AccountingWorker.thrift",
                     "backend/accounting/security/AccountingWorkerConstants.thrift",
                     "backend/session/SessionWorker.thrift",
                     "backend/session/SessionWorkerConstants.thrift",
                     "backend/im/InstantMessagingWorker.thrift",
                     "backend/im/InstantMessagingWorkerConstants.thrift",
                     "backend/warehouse/WarehouseWorker.thrift",
                     "backend/warehouse/WarehouseWorkerConstants.thrift",
                     "backend/warehouse/WaresIndexWorker.thrift",
                     "backend/warehouse/WaresIndexWorkerConstants.thrift",
                     "backend/wares/fields/WareFieldDefinitions.thrift",
                     "backend/wares/fields/WareFields.thrift",
                     "backend/wares/fields/WareSearchConditions.thrift",
                     "backend/wares/fields/WareSearchConditionsConstants.thrift",
                     "common/Common.thrift",
                     "common/CommonConstants.thrift",
                     "exceptions/Exceptions.thrift"]

if __name__ == '__main__':
    print u"Начинаем генерировать файлы.".encode("cp866")
    print u"Имя исполняемого файла: ".encode("cp866") + name_thrift_prog
    print u"Параметры исполняемого файла: ".encode("cp866") + params_thrift + "\n"
    time.sleep(3)
    for num, index in enumerate(lists_trift_files):
        print u"%s) Выполнение: %s" % (str(num), index)
        cmd = name_thrift_prog + params_thrift + index
        print cmd
        PIPE = subprocess.PIPE
        subprocess.Popen(cmd, shell=True)
    
    print u"Завершение генерирования файлов.".encode("cp866")
    time.sleep(5)