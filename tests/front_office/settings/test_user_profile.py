# -*- coding: utf-8 -*-
"""
Feature: Профиль пользователя
"""
from unittest import skip
from ddt import ddt
import time
from support import service_log
from support.utils import common_utils
from support.utils.common_utils import generate_sha256, priority
from support.utils.db import databases
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.data_navigation import ProfileSettingsPage as PSP
from tests.front_office.settings.classes.class_profile_settings import HelpProfileSettingsCheckMethods
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleCheckMethods


@ddt
class FillOrEditUserProfile(HelpAuthCheckMethods, HelpProfileSettingsCheckMethods, PSP):
    """
    Story: Заполнить \ Редактировать профиль пользователя
    """
    @classmethod
    def setUp(cls):
        # Настройка окружения и вспомогательные параметры
        default_user_id = AccountingMethods.get_default_user_id(role='seller')
        cls.user = databases.db1.accounting.get_user_by_account_id(default_user_id)[0]
        databases.db1.accounting.update_account_details_by_criteria(default_user_id, "locale='ru'")
        AccountingMethods.save_user_password(user_id=cls.user["id"], hash_passwd=cls.user["code_value"],
                                             salt=cls.user["salt"])

        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleCheckMethods.get_driver()
        service_log.preparing_env(cls)

    @priority('must')
    def test_fill_user_profile(self):
        """
        Title: Я могу отредактировать Имя и Пол в своем профиле. На всех моих карточках будет новое Имя. Новый пользователь.
        """
        self.go_to_main_page(self.driver)
        user = self.registration(link_db=databases.db1)
        self.get_page(self.driver, self.path_settings.PATH_PROFILE_SETTINGS)
        profile = self.get_user_profile_form(self.driver, user)
        gender = self.get_gender_user(self.driver, user["gender"])
        self.clear_input_row(self.driver, profile["name_input"])
        new_name = common_utils.random_string()
        profile["name_input"].send_keys(new_name)
        gender_ui = self.set_gender(gender, user["gender"])
        self.click_button(profile["save_btn"])
        self.get_element_navigate(self.driver, self.check_main.WU_NAME % new_name)
        criteria = "gender='%s' and display_name='%s' and id=%s" % (gender_ui, new_name, user["id"])
        user_updated = databases.db1.accounting.get_user_by_criteria_only(criteria)[0]
        self.driver.refresh()
        time.sleep(2)
        HelpProfileSettingsCheckMethods.progress(self.driver)
        self.get_user_profile_form(self.driver, user_updated)
        self.get_gender_user(self.driver, user_updated["gender"])
        self.check_header_widget_seller_all(self.driver, user_updated)

    @priority('must')
    def test_edit_user_profile(self):
        """
        Title: Я могу отредактировать Имя и Пол в своем профиле. На всех моих карточках будет новое Имя. Существующий пользователь.
        """
        # Устанавливаем новый пароль для пользователя
        default_new_passwd = AccountingMethods.get_default_password()
        hash_res_new = generate_sha256(default_new_passwd, self.user["salt"])
        databases.db1.accounting.update_user_password(self.user["id"], hash_res_new)
        self.go_to_main_page(self.driver)
        self.go_main(self.driver, phone=self.user["phone"], passwd=default_new_passwd, flag_auth=True, flag_api=False)

        self.get_page(self.driver, self.path_settings.PATH_PROFILE_SETTINGS)
        profile = self.get_user_profile_form(self.driver, self.user)
        gender = self.get_gender_user(self.driver, self.user["gender"])
        self.clear_input_row(self.driver, profile["name_input"])
        new_name = common_utils.random_string()
        profile["name_input"].send_keys(new_name)
        gender_ui = self.set_gender(gender, self.user["gender"])
        self.click_button(profile["save_btn"])
        self.get_element_navigate(self.driver, self.check_main.WU_NAME % new_name)
        criteria = "gender='%s' and display_name='%s' and id=%s" % (gender_ui, new_name, self.user["id"])
        user_updated = databases.db1.accounting.get_user_by_criteria_only(criteria)[0]
        self.driver.refresh()
        time.sleep(2)
        HelpProfileSettingsCheckMethods.progress(self.driver)
        self.get_user_profile_form(self.driver, user_updated)
        self.get_gender_user(self.driver, user_updated["gender"])
        self.check_header_widget_seller_all(self.driver, user_updated)

    @skip('manual')
    @priority("Low")
    def test_not_save_changes_user_profile(self):
        """
        Title: Я могу ввести новое Имя и Пол, но не сохранять изменения. Данные останутся старыми
        """
        pass

    @classmethod
    def tearDown(cls):
        AccountingMethods.recover_user_password(databases.db1)
        cls.driver.quit()
        service_log.end()


class AddOrEditUserProfilePhoto():
    """
    Story: Добавить \ Удалить аватар пользователя
    """

    @skip('need_auto')
    @priority("Must")
    def test_add_user_photo_from_PC(self):
        """
        Title: Я могу изменить \ загрузить аватар в свой профиль (Через файвловый менеджер на ПК).
        Description: На всех моих карточках будет новый аватар
        """
        pass

    @skip('need_auto')
    @priority("High")
    def test_delete_user_photo(self):
        """
        Title: Я могу удалить аватар из своего профиля. На всех моих карточках будет заглушка, вместо аватара
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_add_user_photo_from_tablet(self):
        """
        Title: Я могу изменить \ загрузить аватар в свой профиль (Через файвловый менеджер на планшете).
        Description: На всех моих карточках будет новый аватар
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_add_user_photo_from_tablet_camera(self):
        """
        Title: Я могу изменить \ загрузить аватар в свой профиль (Через камеру на планшете).
        Description: На всех моих карточках будет новый аватар
        """
        pass


class UserProfileForm():
    """
    Story: Форма Профиля пользователя + Аватар
    """

    @skip('manual')
    @priority("Medium")
    def test_user_profile_form_view(self):
        """
        Title: Вид формы профиля пользователя
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_user_profile_form_validation_positive(self):
        """
        Title: Проверка ограничения на поля формы: Позитивные значения
        Description:
        Наборы значений: Зеленые из таблицы сущностей, проверить:
        * Появилось сообщение об успешном сохранении изменений
        * Проверить корректность сохранения значений в базе данных
        * Проверить корректность отображения сделанных изменений на странице настроек
        * Проверить отображение изменений Имени и Фото в шапке сайта
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_user_profile_form_validation_negative(self):
        """
        Title: Проверка ограничения на поля формы: Негативные значения
        Description:
        Наборы значений: Красные из таблицы сущностей, проверить:
        * невозможность сохранить изменения
        * выдачу соответствующего предупреждающего сообщения
        * в базе значения измененных полей не поменялись на новые.
        """
        pass


class ManageNotifications():
    """
    Story: Управление нотификациями
    """

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft_2(self):
        """
        Title:
        """
        pass


class ManageRecommendations():
    """
    Story: Управление рекомендациями
    """

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft_2(self):
        """
        Title:
        """
        pass


class ManageMailing():
    """
    Story: Управление рассылками
    """

    @skip('draft')
    @priority("Low")
    def test_draft_1(self):
        """
        Title:
        """
        pass

    @skip('draft')
    @priority("Low")
    def test_draft_2(self):
        """
        Title:
        """
        pass
