# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
#         Генерация отчета по товарам в каталоге категорий.
# ----------------------------------------------------------------------
import codecs
import platform
from support import service_log
from support.utils.common_utils import priority
from support.utils.thrift4req import services
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.worker_warehouse.class_warehouse import WarehouseCheckMethods, WarehouseMethods

__author__ = 's.trubachev'


class TestWares(WarehouseCheckMethods):

    FILE_BUF = None

    @staticmethod
    def encode_print(msg):
        """ Вывод строки под кодировку консоли.
        :param msg: строка для вывода
        """
        import traceback
        try:
            if platform.uname()[0] != "Windows":
                msg = msg.encode("cp1251")
                return msg
            else:
                return msg.encode("cp1251")
        except Exception, tx:
            import funcy
            logs = funcy.join(traceback.format_stack(limit=10))
            service_log.put("Trace:   " + str(logs))
            service_log.put("End Trace!!!!")
            raise AssertionError(tx)


    @staticmethod
    def get_bread_crumbs(all_category, category, crumbs=None):
        """ Получить хлебные крошки категории.
        :param all_category: словарь всех категорий param category: категория поиска param crumbs: хлебные крошки return: список "хлебных крошек"
        """
        for index in all_category.values():
            if category == index.categoryId and index.categoryId != 0:
                if index.parentCategories is not None:
                    if isinstance(crumbs, list):
                        crumbs.append(index.localizedName)
                    else:
                        crumbs = list()
                        crumbs.append(index.localizedName)
                    for parent in index.parentCategories:
                        # TODO: есть риск множественного наследования родительских категорий
                        el = TestWares.get_bread_crumbs(all_category, parent, crumbs)
                        return el
                else:
                    return crumbs
            elif category == 0:
                if isinstance(crumbs, list):
                    crumbs.append(index.name)
                else:
                    crumbs = list()
                    crumbs.append(index.name)
                return crumbs

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        service_log.put("Created file for unloading wares by category.")
        path_t = "tmp/unloading_wares_by_category.csv"
        TestWares.FILE_BUF = codecs.open(path_t, "w", "cp1251")
        TestWares.FILE_BUF.close()
        TestWares.FILE_BUF = open(path_t, 'ab+')
        TestWares.FILE_BUF.write(cls.encode_print("Category path;Count wares;Genders\n"))

    @priority("low")
    def test_gets(self):
        """ Выгрузка товаров для категорий.
        :return: файл с количеством товаров по категориям
        """

        result = services.crud.root.tframed.getAllCatalogCategories("ru") # TODO: send_getVisibleLiteCatalogTree или др.
        for index in result.values():
            t = self.get_bread_crumbs(result, index.categoryId)
            t.reverse()
            path = " > ".join(t)

            def created_req(limit_n=1, offset_n=0):
                """ Формируем запрос для условий выборки товара.
                :param limit_n: лимит
                :param offset_n: смещение
                :return: запрос
                """
                pag = AccountingMethods.get_PaginationDto(limit=limit_n, offset=offset_n)
                search_req = WarehouseMethods.get_SearchRequestDto(search_category=index.categoryId, pagination=pag,
                                                                   stock_states=[1, 2, 3, 4, 5],
                                                                   moderation_states=[1, 2, 3, 4])
                p = services.warehouse_index.root.tframed.search(search_req)
                return p

            key_count = 200  # что бы избежать переполнение памяти, выводим результат порциями
            res = created_req()
            all_gender = list()

            for num in range((res.totalCount / key_count) + 1):
                wares = created_req(limit_n=key_count, offset_n=(num*key_count))
                for ware in wares.wares:
                    if ware.content.enumFields is not None:
                        if "gender_adult" in ware.content.enumFields.keys():
                            all_gender.append(ware.content.enumFields['gender_adult'].value)
                        elif "gender_children_bgu" in ware.content.enumFields.keys():
                            all_gender.append(ware.content.enumFields['gender_children_bgu'].value)
                        elif "gender_adult_unisex" in ware.content.enumFields.keys():
                            all_gender.append(ware.content.enumFields['gender_adult_unisex'].value)
                        elif "gender_children" in ware.content.enumFields.keys():
                            all_gender.append(ware.content.enumFields['gender_children'].value)
                        else:
                            all_gender.append("None")
                    else:
                        all_gender.append("None")

            #genders = ":%s, ".join(set(all_gender))

            genders = ["%s:%s" % (num, len([index for index in all_gender if num == index])) for num in set(all_gender)]
            genders_str = ", ".join(genders)


            ccc = u"%s;%s;%s\n" % (unicode(path, "utf-8"), str(res.totalCount), genders_str)
            rrr = self.encode_print(ccc)
            self.FILE_BUF.write(rrr)

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        TestWares.FILE_BUF.close()
        TestWares.FILE_BUF = None
        service_log.put("Closed file.")
