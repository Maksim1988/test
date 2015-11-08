# -*- coding: utf-8 -*-
"""
Feature: Реквизиты компании
"""
from support import service_log
from support.utils import common_utils
from support.utils.common_utils import priority
from support.utils.db import databases
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.settings.classes.class_profile_settings import HelpProfileSettingsCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods
from unittest import skip



class FillOrEditStoreRequisites(HelpProfileSettingsCheckMethods, HelpAuthCheckMethods):
    """
    Story: Заполнить \ Редактировать реквизиты компании
    """
    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

    @priority("Medium")
    def test_fill_store_requisites(self):
        """
        Title: Я могу заполнить реквизиты компании и сохранить изменения. Новый пользователь.
        Description:
        Блок "О компании" и "Банковские реквизиты"
        Проверить:
        * в БД сохранились данные
        * изменения отображаются на странице задания  реквизитов
        """
        self.go_to_main_page(self.driver)
        self.user = self.registration(link_db=databases.db1)

        self.get_page(self.driver, self.path_settings.URL_COMPANY_DETAILS)
        details = self.get_details_form(self.driver, self.user)

        self.clear_input_row(self.driver, details["legal_name_input"])
        self.clear_input_row(self.driver, details["inn_input"])
        self.clear_input_row(self.driver, details["kpp_input"])
        self.clear_input_row(self.driver, details["ogrn_input"])
        self.clear_input_row(self.driver, details["legal_address_input"])
        self.clear_input_row(self.driver, details["real_address_input"])
        self.clear_input_row(self.driver, details["bik_input"])
        self.clear_input_row(self.driver, details["name_bank_input"])
        self.clear_input_row(self.driver, details["account_input"])
        self.clear_input_row(self.driver, details["correspondent_input"])

        details_new = {
            'legal_name': common_utils.random_string(params="russian"),
            'inn': common_utils.random_string(params='digits', length=12),
            'kpp': common_utils.random_string(params='digits', length=9),
            'ogrn': common_utils.random_string(params='digits', length=13),
            'legal_address': common_utils.random_string(params="russian", length=30),
            'real_address': common_utils.random_string(params="russian", length=35),
            'bik': common_utils.random_string(params='digits', length=9),
            'name_bank': common_utils.random_string(params="russian", length=30),
            'account': common_utils.random_string(params='digits', length=20),
            'correspondent': common_utils.random_string(params='digits', length=20),
        }

        details["legal_name_input"].send_keys(details_new["legal_name"])
        details["inn_input"].send_keys(details_new["inn"])
        details["kpp_input"].send_keys(details_new["kpp"])
        details["ogrn_input"].send_keys(details_new["ogrn"])
        details["legal_address_input"].send_keys(details_new["legal_address"])
        details["real_address_input"].send_keys(details_new["real_address"])
        details["bik_input"].send_keys(details_new["bik"])
        details["name_bank_input"].send_keys(details_new["name_bank"])
        details["account_input"].send_keys(details_new["account"])
        details["correspondent_input"].send_keys(details_new["correspondent"])

        self.click_button(details["save_btn"])
        err_msg = "Не появилось сообщение об успешном сохранении."
        self.element_is_present(self.driver, self.check_settings.CHANGE_STORE_INFO_SUCCESS)
        self.driver.refresh()
        HelpProfileSettingsCheckMethods.progress(self.driver)
        criteria_1 = "legal_name='%s' and inn='%s' and kpp='%s' and ogrn='%s' and "
        criteria_2 = "legal_address='%s' and actual_address='%s' and bank_bic='%s' and "
        criteria_3 = "bank_name_and_address='%s' and bank_account='%s' and bank_correspondent_account='%s'"
        legal_name = details_new["legal_name"].encode('utf-8')
        legal_address = details_new["legal_address"].encode('utf-8')
        real_address = details_new["real_address"].encode('utf-8')
        name_bank = details_new["name_bank"].encode('utf-8')
        crt_1 = criteria_1 % (legal_name, details_new["inn"], details_new["kpp"], details_new["ogrn"])
        crt_2 = criteria_2 % (legal_address, real_address, details_new["bik"])
        crt_3 = criteria_3 % (name_bank, details_new["account"], details_new["correspondent"])
        criteria = crt_1 + crt_2 + crt_3
        user_updated = databases.db1.accounting.get_user_by_criteria_only(criteria)[0]
        self.assertIsNotNone(user_updated, "Не найдено записей в таблице account_details по запросу %s" % criteria)
        self.get_details_form(self.driver, user_updated)

    @skip('manual')
    @priority("Medium")
    def test_edit_store_requisites(self):
        """
        Title: Я могу отредактировать реквизиты компании и сохранить изменения. Существующий пользователь.
        Description:
        Блок "О компании" и "Банковские реквизиты"
        Проверить:
        * в БД сохранились данные
        * изменения отображаются на странице задания  реквизитов
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()



class StoreRequisitesForm():
    """
    Story: Форма Реквизиты компании
    """

    @skip('manual')
    @priority("Low")
    def test_store_requisites_form_view(self):
        """
        Title: Вид формы реквизиты компании
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_store_requisites_form_validation_positive(self):
        """
        Title: Проверка ограничения на поля формы: Позитивные значения
        Description:
        Наборы значений: Зеленые из таблицы сущностей, проверить:
        * Появилось сообщение об успешном сохранении изменений
        * Проверить корректность сохранения значений в базе данных
        * Проверить корректность отображения сделанных изменений на странице реквизитов магазина (после F5)
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_store_requisites_form_validation_negative(self):
        """
        Title: Проверка ограничения на поля формы: Негативные значения
        Description:
        Наборы значений: Красные из таблицы сущностей, проверить:
        * невозможность сохранить изменения
        * выдачу соответствующего предупреждающего сообщения
        * в базе значения измененных полей не поменялись на новые.
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_store_requisites_same_as_legal_address(self):
        """
        Title: Чек-бокс "Совпадает с юридическим"
        * Проверить, что при проставлении чек-бокса "Совпадает с юридическим",
        поле "Физический адрес" становится недоступным для редактирования и содержит то же значение, что и в поле "Юридический адрес".
        * Проверить, что при снятии проставленного чек-бокса "Совпадает с юридическим",
        поле "Физический адрес" становится доступным для редактирования.
        """
        pass

