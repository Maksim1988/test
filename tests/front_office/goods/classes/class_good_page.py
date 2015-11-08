# -*- coding: utf-8 -*-
from support import service_log
from tests.MainClass import MainClass
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods as Navigate

__author__ = 'm.senchuk'


class GoodData(MainClass):
    pass


class GoodMethods(GoodData):
    @staticmethod
    def get_form_call_seller(driver):
        """
        Get popup 'Call with seller' as logged user.
        :param driver:
        :return:
        """
        call_seller = dict(
            title=Navigate.element_is_present(driver, Navigate.check_good.P_TITLE),
            label_who=Navigate.element_is_present(driver, Navigate.check_good.P_WHO),
            who=Navigate.element_is_present(driver, Navigate.check_good.P_WHO_VALUE),
            label_subject=Navigate.element_is_present(driver, Navigate.check_good.P_SUBJECT),
            good=Navigate.element_is_present(driver, Navigate.click_good.POPUP_CARD_GOOD),
            label_message=Navigate.element_is_present(driver, Navigate.check_good.P_MESSAGE),
            input_message=Navigate.element_is_present(driver, Navigate.input_good.POPUP_INPUT_MSG),
            btn_send=Navigate.element_is_present(driver, Navigate.click_good.BTN_SEND),
            btn_cancel=Navigate.element_is_present(driver, Navigate.click_good.BTN_CANCEL_CALL),
            btn_close=Navigate.element_is_present(driver, Navigate.click_good.BTN_TO_CARD_GOOD),
        )
        return call_seller

    @staticmethod
    def get_form_call_success(driver):
        """
        Get popup after send message to seller as logged user.
        :param driver:
        :return:
        """
        call_success = dict(
            success=Navigate.element_is_present(driver, Navigate.check_good.P_SUCCESS_SENT),
            title=Navigate.element_is_present(driver, Navigate.check_good.P_TITLE_SENT),
            body=Navigate.element_is_present(driver, Navigate.check_good.P_BODY_SENT),
            btn_to_catalog=Navigate.element_is_present(driver, Navigate.click_good.BTN_POPUP_TO_CATALOG),
            btn_close=Navigate.element_is_present(driver, Navigate.click_good.BTN_TO_CARD_GOOD)
        )
        return call_success

    @staticmethod
    def get_visitor_form_call_seller(driver):
        """
        Get popup 'Call with seller' as visitor.
        :param driver:
        :return:
        """
        call_seller = dict(
            title=Navigate.element_is_present(driver, Navigate.check_good.P_TITLE),
            label_your_name=Navigate.element_is_present(driver, Navigate.check_good.P_YOUR_NAME),
            input_your_name=Navigate.element_is_present(driver, Navigate.input_good.POPUP_INPUT_NAME),
            label_who=Navigate.element_is_present(driver, Navigate.check_good.P_WHO),
            who=Navigate.element_is_present(driver, Navigate.check_good.P_WHO_VALUE),
            label_subject=Navigate.element_is_present(driver, Navigate.check_good.P_SUBJECT),
            good=Navigate.element_is_present(driver, Navigate.click_good.POPUP_CARD_GOOD),
            label_message=Navigate.element_is_present(driver, Navigate.check_good.P_MESSAGE),
            input_message=Navigate.element_is_present(driver, Navigate.input_good.POPUP_INPUT_MSG),
            label_email=Navigate.element_is_present(driver, Navigate.check_good.P_EMAIL_FEEDBACK),
            input_email=Navigate.element_is_present(driver, Navigate.input_good.POPUP_INPUT_EMAIL),
            btn_send=Navigate.element_is_present(driver, Navigate.click_good.BTN_SEND),
            btn_cancel=Navigate.element_is_present(driver, Navigate.click_good.BTN_CANCEL_CALL),
            btn_close=Navigate.element_is_present(driver, Navigate.click_good.BTN_TO_CARD_GOOD),
        )
        return call_seller

    @staticmethod
    def get_visitor_form_call_success(driver):
        """
        Get popup after send message to seller as visitor.
        :param driver:
        :return:
        """
        call_success = dict(
            success=Navigate.element_is_present(driver, Navigate.check_good.P_SUCCESS_SENT),
            title=Navigate.element_is_present(driver, Navigate.check_good.P_VISITOR_TITLE_SENT),
            body=Navigate.element_is_present(driver, Navigate.check_good.P_VISITOR_BODY_SENT),
            input_password=Navigate.element_is_present(driver, Navigate.input_good.POPUP_INPUT_PASS),
            label_help=Navigate.element_is_present(driver, Navigate.check_good.P_HELP_PASS),
            btn_reg=Navigate.element_is_present(driver, Navigate.click_good.BTN_POPUP_REG),
            btn_reject=Navigate.element_is_present(driver, Navigate.click_good.BTN_POPUP_REJECT),
            label_attention=Navigate.element_is_present(driver, Navigate.check_good.P_ATTENTION),
            link_agreement=Navigate.element_is_present(driver, Navigate.click_good.POPUP_LINK_AGREEMENT),
            btn_close=Navigate.element_is_present(driver, Navigate.click_good.BTN_TO_CARD_GOOD)
        )
        return call_success

    @staticmethod
    def get_gallery(driver, pictures, main_picture=None):
        """
        Получить объекты галерии
        :param driver:
        :param pictures:
        :param main_picture:
        :return:
        """
        count = 0
        pict = dict()
        if main_picture is None:
            main_picture = pictures[0]
        value_main = Navigate.element_is_present(driver, Navigate.click_good.IMG_GALLERY_VIEW % main_picture)
        for picture in pictures:
            count += 1
            name_dict = 'prev_%s' % count
            value_dict = Navigate.element_is_present(driver, Navigate.click_good.IMG_GALLERY_PREVIEW % (count, picture))
            pict.update({name_dict: value_dict})
        value_act = Navigate.element_is_present(driver, Navigate.click_good.IMG_GALLERY_PREVIEW_ACTIVE % main_picture)
        value_zoom = Navigate.element_is_present(driver, Navigate.click_good.IMG_ZOOM)
        pict.update({'main': value_main})
        pict.update({'prev_active': value_act})
        pict.update({'btn_zoom': value_zoom})
        return pict

    @staticmethod
    def get_gallery_zoom(driver, pictures, zoom_picture=None):
        """
        Получить объекты zoom галереи
        :param driver:
        :param pictures:
        :param zoom_picture:
        :return:
        """
        count = 0
        pict = dict()
        if zoom_picture is None:
            zoom_picture = pictures[0]
        value_main = Navigate.element_is_present(driver, Navigate.click_good.IMG_ZOOMED % zoom_picture)
        for picture in pictures:
            count += 1
            name_dict = 'prev_%s' % count
            value_dict = Navigate.element_is_present(driver, Navigate.click_good.IMG_ZOOM_PREVIEW % (count, picture))
            pict.update({name_dict: value_dict})
        value_act = Navigate.element_is_present(driver, Navigate.click_good.IMG_ZOOM_PREVIEW_ACTIVE % zoom_picture)
        value_close = Navigate.element_is_present(driver, Navigate.click_good.ZOOM_CLOSE)
        pict.update({'zoomed': value_main})
        pict.update({'prev_active': value_act})
        pict.update({'close': value_close})
        return pict

    @staticmethod
    def get_tree_categories(db_link, category, tree=list()):
        """
        Получить дерево-список категорий, которому принадлежит товар
        :param db_link:
        :param category: финальная категория товара
        :param tree:
        :return:
        """
        cat = db_link.accounting.get_categories_psql("id=%s" % category)[0]
        tree.append(cat["id"])
        if cat["parent_id"] != 1:
            tree = GoodMethods.get_tree_categories(db_link, cat["parent_id"], tree)
        return tree

    @staticmethod
    def get_tree_breadcrumbs(driver, tree_cat, db_link):
        """
        Получить объекты хлебных крошек на странице товара (родительская категория->категория->финальная категория)
        :param driver:
        :param tree_cat: дерево-список категорий, кокторым принадлежит товар
        :param db_link:
        :return:
        """
        count = 0
        breads = dict()
        for cat in tree_cat:
            count += 1
            cat_local = db_link.accounting.get_category_name(cat)[0]
            name = cat_local["value"]
            value_dict = Navigate.element_is_present(driver, Navigate.click_good.BREADCRUMB % (count, cat, name))
            breads.update({count: value_dict})
        return breads


class GoodCheckMethods(GoodMethods):
    pass

