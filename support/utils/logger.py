# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Логирование.
#--------------------------------------------------------------------
__author__ = 'Strubachev'

import logging
import logging.config


class InitializationLogger():
    LOGGER_NAME = 'ftest'

    def __init__(self, path=None):
        # Очищаем лог перед началом тестирования
        f = open(InitializationLogger.LOGGER_NAME + '.log', 'w')
        f.write("---== Start testing. ==---\n\r")
        f.close()

    @staticmethod
    def get_logger():
        #  Конфигурация логгирования
        logging.config.fileConfig("logger.cfg")
        return logging.getLogger(InitializationLogger.LOGGER_NAME)


class LoggerInfo():
    def __init__(self, log):
        self.main_log = log

    def put(self, text):
        """ Логирование общей информации.
        :param text: текст которые слудует положить в лог файл
        """
        self.main_log.info(text)

    def user(self, user):
        msg = "Get user, id=%s: %s" % (user["id"], user)
        self.main_log.info(msg)

    def error(self, text):
        """ Логирование ошибки.
        :param text: текст которые слудует положить в лог файл
        """
        self.main_log.info("Error: " + str(text))

    def warning(self, text):
        """ Логирование предупреждения.
        :param text: текст которые слудует положить в лог файл
        """
        self.main_log.info("Warning: " + text)

    def c_request(self, data):
        """ Логирование созданных запросов.
        :param data: Созданный для отправки сервису запрос
        """
        self.main_log.info("Create request json-rpc for service: %s" % data)

    def s_response(self, data):
        """ Логирование ответов.
        :param data: Созданный для отправки сервису запрос
        """
        self.main_log.info("Response json-rpc from service: %s" % data)

    def preparing_env(self, data):
        """ Логирование запуска теста.
        :param data: глобальные переменные
        """
        self.main_log.info("\n\n == Preparing the test environment ==")
        self.main_log.info("Link Test: %s " % str(data).replace("'", ''))

    def run(self, data):
        """ Логирование запуска теста.
        :param data: глобальные переменные
        """
        self.main_log.info("\n\n == Run Test ==")
        self.main_log.info("Name Test: %s " % data._testMethodName)

    def end(self):
        """ Логирование завершения теста.
        """
        self.main_log.info("\n *** The test TearDown ***")
