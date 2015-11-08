# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Переопределяем методы unittest.
#       P.S: Имей совесть и делай что хочешь.
#--------------------------------------------------------------------
import unittest
import funcy
import traceback
from support import service_log, configs

__author__ = 's.trubachev'

# TODO: print u"Тестирование, русские буквы в консоли ".encode("cp866")


def assert_log(func):
    """ Обертка для методов типа assert из unittest.
    Логируем необходимые действия.
    :type func: функция, которую оборачиваем
    :return: ссылка на функцию
    """
    def modify(*args, **kwargs):
        try:
            service_log.put("Params for %s: %s, %s" % (func.func_name, str(args[1:]), str(kwargs)))
            link_func = unittest.TestCase.__dict__[func.func_name]
            return link_func(*args, **kwargs)
        except Exception, tx:
            limit_print_exc = 10
            msg_line = "#" + ("-"*100)
            service_log.error(tx)
            service_log.put("\n%s\n%s\n%s" % (msg_line, traceback.format_exc(limit_print_exc), msg_line))
            trace_stack_log = funcy.join(traceback.format_stack(limit=limit_print_exc))
            service_log.put("Traceback stack:\n%s\n%s" % (str(trace_stack_log), msg_line))
            raise AssertionError(tx)
    return modify


class MainClass(unittest.TestCase):

    ENV_BASE_URL = None
    ENV_BASE_BACK_URL = None
    ENV_PROD_BASE_URL = "http://oorraa.com"
    ENV_STATIC_PATH = None
    ENV_METRIC = None
    ENV_MAIL_HOST = 'mx.oorraa.com'
    ENV_MAIL_LOGIN = 'oratest@oorraa.com'
    ENV_MAIL_PASS = 'WJuR897uMM'

    try:
        ENV_BASE_URL = configs.config["env_info"]["front_base_url"]
        ENV_BASE_BACK_URL = configs.config["env_info"]["back_base_url"]
        ENV_STATIC_PATH = configs.config["env_info"]["static_url"]
        ENV_METRIC = configs.config["env_info"]["metric_path"]
        ENV_METRIC_IP = configs.config["env_info"]["metric_ip"]
        ENV_METRIC_PORT = configs.config["env_info"]["metric_port"]
        ENV_BROWSER = configs.config["browser"]
        ENV_MAIL_HOST = configs.config["env_info"]["mail_host"]
        ENV_MAIL_LOGIN = configs.config["env_info"]["mail_login"]
        ENV_MAIL_PASS = configs.config["env_info"]["mail_pass"]
    except Exception, tx:
        service_log.put("Warning! Not found param config: %s" % str(tx))

    STATIC_USERS = [{"id": 113,
                     "display_name": "тестовый покупатель 2",
                     "phone": "79999999999",
                     "password": "123",
                     "email": "tes1t@test.ru",
                     "role": "buyer"},

                    {"id": 112,
                     "display_name": "Тест 666",
                     "phone": "79163898804",
                     "password": "12336",
                     "email": "vasya@oorraa.com",
                     "role": "seller"}
    ]


    @staticmethod
    def get_static_user(user_id):
        """ Получить данные статичного пользователя для прода по идентификатору.
        :param user_id: идентификатор пользователя
        :return: список словарей
        """
        from funcy import where
        return where(MainClass.STATIC_USERS, user_id=user_id)

    @staticmethod
    def get_static_user_by_role(role):
        """ Получить данные статичного пользователя для прода по его роли.
        :param role: роль пользователя
        :return: список словарей
        """
        from funcy import where
        return where(MainClass.STATIC_USERS, role=role)



    @assert_log
    def assertEqual(*args, **kwargs):
        pass

    @assert_log
    def assertDictEqual(*args, **kwargs):
        pass

    @assert_log
    def assertGreaterEqual(*args, **kwargs):
        pass

    @assert_log
    def assertGreater(*args, **kwargs):
        pass

    @assert_log
    def assertLessEqual(*args, **kwargs):
        pass

    @assert_log
    def assertLess(*args, **kwargs):
        pass

    @assert_log
    def assertIsNone(*args, **kwargs):
        pass

    @assert_log
    def assertIsNotNone(*args, **kwargs):
        pass

    @assert_log
    def assertListEqual(*args, **kwargs):
        pass

    @assert_log
    def assertFalse(*args, **kwargs):
        pass

    @assert_log
    def assertTrue(*args, **kwargs):
        pass

    @assert_log
    def assertNotEqual(*args, **kwargs):
        pass