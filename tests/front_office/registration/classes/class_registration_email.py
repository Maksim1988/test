# coding=utf-8
import time
from support.utils.db import databases
from tests.MainClass import MainClass
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods as Front

__author__ = 'm.senchuk'


class RegEmailData(MainClass):
    URL_VALIDATE_PATH = "/activation/validate-email?token="
    URL_VALIDATE_EMAIL = "/activation/validate-email?token=%s"


class RegEmailMethods(RegEmailData):
    @staticmethod
    def get_new_email(db_link):
        """
        Получить новый email, которого нет в БД
        :return: email
        """
        f = True
        email = 'oratest+%s@oorraa.com' % str(time.time())
        while f is True:
            u = db_link.accounting.get_user_by_criteria_only("email='%s'" % email)
            if len(u) == 0:
                f = False
            else:
                email = 'oratest+%s@oorraa.com' % str(time.time())
        return email

    @staticmethod
    def get_reg_email_success(driver, email):
        """
        Получить форму успешной регистрации по емайл
        :param driver:
        :param email:
        :return:
        """
        Navigate.element_is_present(driver, Navigate.check_reg.E_TITLE_REG_SUCCESS)
        Navigate.element_is_present(driver, Navigate.check_reg.E_ICON_REG_SUCCESS)
        Navigate.element_is_present(driver, Navigate.check_reg.E_TEXT_REG_SUCCESS % email)
        return Navigate.element_is_present(driver, Navigate.click_reg.E_BTN_START_WORK)

    @staticmethod
    def get_validated_email_success(driver):
        """
        Получить форму успешной активации емайла
        :param driver:
        :return:
        """
        Navigate.element_is_present(driver, Navigate.check_reg.E_TITLE_VALIDATED)
        Navigate.element_is_present(driver, Navigate.check_reg.E_ICON_ACTIVATE_SUCCESS)
        Navigate.element_is_present(driver, Navigate.check_reg.E_TEXT_VALIDATED_SUCCESS)
        return Navigate.element_is_present(driver, Navigate.click_reg.E_BTN_START_WORK_AFTER_SUCCESS)

    @staticmethod
    def reading_unread_messages_after_reg(driver, new_messages):
        """
        Прочитать(протыкать) все непрочитанные сообщения(диалоги с пользователями)
        :param driver:
        :return:
        """
        dialogs = Navigate.elements_is_present(driver, Navigate.click_chat.ALL_UNREAD_MESSAGES)
        for dialog in dialogs:
            body_msg = Navigate.element_is_present(driver, Navigate.check_chat.LAST_MSG)
            Navigate.element_is_present(driver, Navigate.check_main.COUNT_NEW_MSG % (new_messages-1), wait=20)
            Navigate.element_click(driver, dialog, change_page_url=True)
            body_msg_new = Navigate.get_element_navigate(driver, Navigate.check_chat.LAST_MSG)
            assert body_msg != body_msg_new, "Тело нового диалога не появилось, переход на новый диалог не произошел"
        msg = Navigate.get_element_navigate(driver, Navigate.check_main.ABSTRACT_MSG)
        msg = msg.text.encode('utf-8')
        return msg


class RegEmailCheckMethods(RegEmailMethods):
    def check_sent_email(self, link_db, user):
        """
        Проверить, что отправлено письмо на емайл после регистрации
        :param link_db:
        :param user:
        :return:
        """
