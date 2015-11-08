# coding=utf-8
import random
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from support.utils.db import databases
from tests.front_office.registration.classes.class_registration_email import RegEmailCheckMethods as Reg
from tests.MainClass import MainClass
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as HNCM
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from support.utils import common_utils

__author__ = 'm.senchuk'


class HelpContactsData(MainClass):
    TEXT_INFO_FEEDBACK = "Звонитепобуднямс9до18длямосквы:+7495668-11-98длярегионов:+7800500-16-43Ответимнавопросы," \
                         "поможемразместитьтоварыизаказать.КакпокупатьнаУурраа?Какстатьпродавцомиразместитьтовары?" \
                         "ЧастозадаваемыевопросыПравообладателямПишитенаlegal@oorraa.com,еслипродавецнаУурраанарушает" \
                         "авторскиеправаилиправаинтеллектуальнойсобственности.Мыразберемсяиустранимнарушения.ОфисыООО" \
                         "«УУРРАА»Москва123022,Москва,Рочдельскаяул.,д.15стр.25©ЯндексУсловияиспользованияОткрыть" \
                         "вЯндекс.Картах400мРостов-на-Дону344068," \
                         "Ростов-на-Дону,пр-тМихаилаНагибина,д.43+7800500-16-43Краснодар350001,Краснодар,ул." \
                         "Ставропольская,д.100,2йэтаж+7800500-16-43"

    TEXT_FEEDBACK_TITLES = "Пишитенаtesty@oorraa.comилизаполнитеформу:Вашеимя:Мобильныйтелефон:+7Электроннаяпочта:" \
                           "Сообщение:Отправить"

    CT_HOW_BUY = dict(start_click=HNCM.click_contacts.HOW_BUY, finish_page=HNCM.check_help.TITLE_HOW_BUY)
    CT_HOW_SELL = dict(start_click=HNCM.click_contacts.HOW_SELL, finish_page=HNCM.check_help.TITLE_HOW_SELL)
    CT_FAQ = dict(start_click=HNCM.click_contacts.FAQ, finish_page=HNCM.check_help.TITLE_FAQ)
    CT_LOCALE = dict(start_click=HNCM.click_contacts.LOCALE, finish_page=HNCM.check_oorraa_net.TITLE_CONTACTS)
    CONTACT_NAVIGATE = {
        "how_buy": CT_HOW_BUY,
        "how_sell": CT_HOW_SELL,
        "faq": CT_FAQ,
        #"locale": CT_LOCALE
    }

    ERR_FIELD = {
        'name': HNCM.check_contacts.MSG_ERROR_NAME,
        'email': HNCM.check_contacts.MSG_ERROR_EMAIL,
        'message': HNCM.check_contacts.MSG_ERROR_MESSAGE,
    }


class HelpContactsMethods(HelpContactsData, HNCM):
    @staticmethod
    def generate_data_for_feedback():
        """
        Генерируем тестовые данные для отзыва
        :return:
        """
        FEEDBACK_VISITOR = {
            'name': 'Test_%s' % common_utils.random_string(params='letters', length=5),
            'email': Reg.get_new_email(databases.db1).lower(),
            'phone': str(random.randrange(70000000000, 70999999999, 1)),
            'message': common_utils.random_string(params='letters', length=200),
        }
        return FEEDBACK_VISITOR

    @staticmethod
    def get_left_feedback_text(driver, xpath):
        """
        Получить текст из левой колонки страницы Контакты
        :param driver:
        :return:
        """
        return HNCM.get_element_navigate(driver, xpath, mode=None).text.encode('utf-8').replace('\n', '').replace(' ', '')

    @staticmethod
    def get_all_fields(driver):
        """
        Получить все input объекты формы обратной связи
        :return:
        """
        obj = dict()
        obj['name'] = HNCM.get_element_navigate(driver, HNCM.input_contacts.NAME)
        obj['phone'] = HNCM.get_element_navigate(driver, HNCM.input_contacts.PHONE)
        obj['email'] = HNCM.get_element_navigate(driver, HNCM.input_contacts.EMAIL)
        obj['message'] = HNCM.get_element_navigate(driver, HNCM.input_contacts.MESSAGE)
        return obj

    @staticmethod
    def set_fields(obj, text):
        """
        Ввести данные в input поля
        :param obj:
        :param text:
        :return:
        """
        obj['name'].send_keys(text['name'])
        obj['phone'].send_keys(text['phone'])
        obj['email'].send_keys(text['email'])
        obj['message'].send_keys(text['message'])

    @staticmethod
    def set_email(driver, email):
        """
        Вводим емайл и сохраняем
        :param email:
        :return:
        """
        input_email = HNCM.get_element_navigate(driver, HNCM.input_settings.EMAIL_ABSTRACT)
        input_email.click()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).key_down(Keys.DELETE).\
            key_up(Keys.DELETE).perform()
        input_email.send_keys(email)
        submit_btn = HNCM.get_element_navigate(driver, HNCM.path_settings.PATH_COMMON_INFO +
                                               HNCM.click_settings.SAVE_BUTTON)
        HelpAuthCheckMethods.click_button(submit_btn, sleep=3)


class HelpContactsCheckMethods(HelpContactsMethods):
    def check_view_contacts(self, driver):
        """
        Проверка элементов на странице Контакты
        :param driver:
        :return:
        """
        self.get_element_navigate(driver, self.check_contacts.TITLE_CONTACTS)
        txt_info = self.get_left_feedback_text(driver, self.check_contacts.FEEDBACK_INFO)
        self.assertEqual(txt_info, self.TEXT_INFO_FEEDBACK, "Текст с страницы:\n'%s'\nне совпадает с текстом:\n'%s'" %
                        (txt_info, self.TEXT_INFO_FEEDBACK))
        txt_titles = self.get_left_feedback_text(driver, self.check_contacts.FEEDBACK_TITLES)
        self.assertEqual(txt_titles, self.TEXT_FEEDBACK_TITLES, "Текст с страницы:\n'%s'\nне совпадает с текстом:\n'%s'" %
                        (txt_titles, self.TEXT_FEEDBACK_TITLES))

    def check_success_sent(self, driver, sleep=5):
        """
        Проверка финального текста - Сообщение успешно отправлено
        :param driver:
        :return:
        """
        self.get_element_navigate(driver, self.check_contacts.MSG_SUCCESS, mode=None, sleep=0.5)
        time.sleep(sleep)
        self.get_all_fields(driver)

    def check_success_sent_user(self, driver, sleep=5):
        """
        Проверка финального текста для пользователя - Сообщение успешно отправлено
        :param driver:
        :return:
        """
        self.get_element_navigate(driver, self.check_contacts.MSG_SUCCESS, mode=None, sleep=0.5)
        time.sleep(sleep)
        self.get_element_navigate(driver, self.input_contacts.MESSAGE)

    def check_email(self, link_db, user_id, email):
        """
        Проверка, что емайл записан в БД
        :param link_db:
        :param email:
        :return:
        """
        e = lambda e: None if e == '' else e
        user = link_db.accounting.get_user_by_account_id(user_id)[0]
        self.assertEqual(user['email'], e(email), "Email не был изменен. В базе='%s', а должен быть='%s'" %
                         (user['email'], email))

    def check_err_msg(self, driver, field):
        """
        Проверка, что подсвечивается незаполненное обязательное поле
        :param driver:
        :param field:
        :return:
        """
        self.get_element_navigate(driver, self.ERR_FIELD[field])