# coding=utf-8
from tests.MainClass import MainClass
from tests.class_selenium import SeleniumMethods


__author__ = 'm.senchuk'


class HelpOnBoardingData(MainClass):
    LOCAL_STORAGE_KEY = 'onboarding'

    LOCAL_REGISTRATION = '{"register":"1"}'
    LOCAL_LANGUAGE = '{"langauge-select":"1"}'
    LOCAL_CATALOG = '{"catalog-good-info":"1"}'
    LOCAL_KNOW_PRICE = '{"good-price":"1"}'
    LOCAL_IN_SHOP = '{"store-info":"1"}'
    LOCAL_SHOP_ADDRESS = '{"store-address":"1"}'


class HelpOnBoardingMethods(HelpOnBoardingData):

    @staticmethod
    def get_local_storage_keys(driver):
        """ Метод получает все ключи хранящиеся в local storage
        :param driver: ссылка на драйвер
        :return:
        """
        return SeleniumMethods.get_local_storage_keys(driver)

    @staticmethod
    def get_local_storage_items(driver, key):
        """ Метод получает значение по ключу хранящееся в local storage
        :param driver:
        :return:
        """
        return SeleniumMethods.get_local_storage_items(driver, key).encode('utf-8')


class HelpOnBoardingCheckMethods(HelpOnBoardingMethods):
    def check_key_in_local_storage(self, driver, key):
        """
        Метод проверяет, что в local storage есть ключ key
        :param driver:
        :param key:
        :return:
        """
        self.assertIn(key, self.get_local_storage_keys(driver), "Нет ключа onboarding в local storage.")

    def check_items_in_local_storage(self, driver, key, check_value):
        """
        Метод проверяет, что в local storage начение item совпадает с ожидаемым check_value
        :param driver:
        :param key:
        :param check_value:
        :return:
        """
        local_item = self.get_local_storage_items(driver, key).encode('utf-8')
        self.assertEqual(local_item, check_value, "Значение ключа onboarding не совпадает с нужным.")

