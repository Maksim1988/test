# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Файл с классами для работы с Favorites worker.
#--------------------------------------------------------------------
import funcy
from gen_py.FavoritesConstants.ttypes import FavoriteType
from gen_py.FavoritesWorker.ttypes import UsersFavoritesRequest, PagingRequest, FavoriteContentDto, FavoritesAddRequest, \
    FavoritesRemoveRequest
from support import service_log
from support.utils.common_utils import crop_date_time_to_sec, crop_and_convert_unix_to_time
from tests.MainClass import MainClass

__author__ = 's.trubachev'


class FavoritesData(MainClass):
    """
    Статические данные свойственные только FavoritesWorker: переменные, константы, названия классов и т.д.
    """

    favorite_types = ["USER", "WARE"]


class FavoritesMethods(FavoritesData):

    @staticmethod
    def get_number_FavoriteType(number, all_item):
        """ Получить номер типа "Избраного".
        :param number: номер статуса
        :param all_item: флаг, взять все значения
        :return: номер типа
        """
        if all_item is True:
            service_log.put("Get FavoriteType number: %s" % FavoriteType._NAMES_TO_VALUES.keys())
            return FavoriteType._NAMES_TO_VALUES.keys()
        else:
            stock_state_number = FavoriteType._NAMES_TO_VALUES[number]
            service_log.put("Get FavoriteType number: %s" % stock_state_number)
            return stock_state_number

    @staticmethod
    def get_name_FavoriteType(name, all_item):
        """ Получить имя типа "Избраного".
        :param name: имя статуса
        :param all_item: флаг, взять все значения
        :return: название типа
        """
        if all_item is True:
            service_log.put("Get FavoriteType names: %s" % FavoriteType._VALUES_TO_NAMES.keys())
            return FavoriteType._VALUES_TO_NAMES.keys()
        else:
            stock_type_name = FavoriteType._VALUES_TO_NAMES[name]
            service_log.put("Get FavoriteType name: %s" % stock_type_name)
            return stock_type_name

    @staticmethod
    def get_FavoriteType(data, all_item=False):
        """ Получить статус опубликованности товара.
        :param data: строка или число
        :return: число или строка
        """
        if type(data) == str:
            return FavoritesMethods.get_number_FavoriteType(data, all_item)
        elif type(data) == int:
            return FavoritesMethods.get_name_FavoriteType(data, all_item)

    @staticmethod
    def get_PagingRequest(offset=None, count=None):
        """ Получить объект PagingRequest.
        :param offset: Выбираем начиная с N-ого элемента
        :param count: Количество элементов которое мы хотим получить в ответе
        :return: type(PagingRequest)
        """
        p = PagingRequest(offset=offset, count=count)
        service_log.put("Get PagingRequest: %s" % str(p))
        return p

    @staticmethod
    def get_UsersFavoritesRequest(user_id=None, paging_req=None, fav_type=None, fav_user_ids=None, fav_ware_ids=None):
        """ Получить объект UsersFavoritesRequest.
        :param user_id: идентификатор пользователя
        :param paging_req: объект пагинации, type(PagingRequest)
        :param fav_type: тип "избранного"
        :param fav_user_ids: список идентификаторов пользователей
        :param fav_ware_ids: список идентификаторов товаров
        :return: type(UsersFavoritesRequest)
        """
        params = {"userId": user_id,
                  "pagingRequest": paging_req,
                  "type": fav_type,
                  "favUserIdSet": fav_user_ids,
                  "favWareIdSet": fav_ware_ids}
        params_without_none = dict((index, val) for index, val in params.iteritems() if params[index] is not None)
        p = UsersFavoritesRequest(**params_without_none)
        service_log.put("Get UsersFavoritesRequest: %s" % str(p))
        return p

    @staticmethod
    def get_FavoriteContentDto(user_id=None, fav_type=None, fav_user_id=None, fav_ware_id=None):
        """ Получить объект FavoriteContentDto.
        :param user_id: идентификатор пользователя, которому добавляется избранное
        :param fav_type: тип "Избранного"
        :param fav_user_id: идентификатор избранного пользователя
        :param fav_ware_id: идентификатор избранного товара
        :return: объект FavoriteContentDto
        """
        p = FavoriteContentDto(userId=user_id, type=fav_type, favUserId=fav_user_id, favWareId=fav_ware_id)
        service_log.put("Get FavoriteContentDto: %s" % str(p))
        return p

    @staticmethod
    def get_FavoritesAddRequest(content_dto_list):
        """ Получить объект FavoritesAddRequest.
        :param content_dto_list: список объектов FavoriteContentDto
        :return: объект FavoritesAddRequest
        """
        p = FavoritesAddRequest(content_dto_list)
        service_log.put("Get FavoritesAddRequest.")
        return p

    @staticmethod
    def generate_dto_list_equal_fav_ware(user_id, ware_ids):
        """ Сгенерировать список объектов для добавления товаров в избранное.
        :param user_id: идентификатор пользователя
        :param ware_ids: список идентификаторов товара
        :return: список get_FavoriteContentDto
        """
        fav_type = FavoritesMethods.get_FavoriteType("WARE")
        return [FavoritesMethods.get_FavoriteContentDto(user_id, fav_type, fav_ware_id=index) for index in ware_ids]

    @staticmethod
    def generate_dto_list_equal_fav_user(user_id, user_ids):
        """ Сгенерировать список объектов для добавления пользователей в избранное.
        :param user_id: идентификатор пользователя
        :param user_ids: список идентификаторов товара
        :return: список get_FavoriteContentDto
        """
        fav_type = FavoritesMethods.get_FavoriteType("USER")
        return [FavoritesMethods.get_FavoriteContentDto(user_id, fav_type, fav_user_id=index) for index in user_ids]

    @staticmethod
    def get_FavoritesRemoveRequest(user_id=None, fav_type=None, fav_usr_ids=None, fav_ware_ids=None):
        """ Получить объект FavoritesRemoveRequest.
        :param user_id: идентификатор пользователя у которого удалеется "избранное"
        :param fav_type: тип избранного
        :param fav_usr_ids: список идентификаторов пользователей
        :param fav_ware_ids: список идентификаторов товаров
        :return: объект FavoritesRemoveRequest
        """
        p = FavoritesRemoveRequest(userId=user_id, type=fav_type, favUsrIds=fav_usr_ids, favWareIds=fav_ware_ids)
        service_log.put("Get FavoritesRemoveRequest: %s" % str(p))
        return p


class FavoritesCheckMethods(FavoritesMethods):

    def check_fav_ware(self, user_id, data, fav_data, fav_type):
        """ Проверка избранного товара.
        :param user_id: идентификатор пользователя
        :param data: данные от сервиса
        :param fav_data: данные из БД
        :param fav_type: тип "Избранного"
        """
        self.assertEqual(len(fav_data), 1, "Find several ware with equal ware's ID.")
        self.assertEqual(fav_data[0]["user_id"], user_id, "Is not equal to the source user ID.")
        self.assertEqual(fav_data[0]["user_id"], data.content.userId, "Not equal user id's.")
        self.assertEqual(str(fav_data[0]["fav_ware_id"]), str(data.content.favWareId), "Not equal ware id's.")
        self.assertEqual(crop_date_time_to_sec(fav_data[0]["creation_timestamp"]),
                         crop_and_convert_unix_to_time(data.creationTimestamp), "Different creationTimestamp.")
        self.assertEqual(data.content.type, fav_type, "Is not equal to the source favorite type.")

    def check_fav_user(self, user_id, data, fav_data, fav_type):
        """ Проверка избранного пользователя.
        :param user_id: идентификатор пользователя
        :param data: данные от сервиса
        :param fav_data: данные из БД
        :param fav_type: тип "Избранного"
        """
        self.assertEqual(len(fav_data), 1, "Find several ware with equal ware's ID.")
        self.assertEqual(fav_data[0]["user_id"], user_id, "Is not equal to the source user ID.")
        self.assertEqual(fav_data[0]["user_id"], data.content.userId, "Not equal user id's.")
        self.assertEqual(fav_data[0]["fav_usr_id"], data.content.favUserId, "Not equal ware id's.")
        self.assertEqual(crop_date_time_to_sec(fav_data[0]["creation_timestamp"]),
                         crop_and_convert_unix_to_time(data.creationTimestamp), "Different creationTimestamp.")
        self.assertEqual(data.content.type, fav_type, "Is not equal to the source favorite type.")
        self.assertIsNone(data.content.favWareId, "Is not None value favorite users.")

    def check_fav_user_from_db(self, before_fav_users, after_fav_users):
        """ Сравнить на идентичность избранных пользователей до и после какого-то действия.
        :param before_fav_users: список словарей до какого-то действия
        :param after_fav_users: список словарей после какого-то действия
        """
        self.assertEqual(len(before_fav_users), len(after_fav_users), "Changed the number of favorite user.")
        for user in before_fav_users:
            fav_data = funcy.where(after_fav_users, fav_usr_id=user["fav_usr_id"])
            fav_elem = fav_data[0]
            self.assertEqual(len(fav_data), 1)
            self.assertEqual(fav_elem["fav_usr_id"], user["fav_usr_id"])
            self.assertEqual(fav_elem["user_id"], user["user_id"])
            self.assertEqual(fav_elem["creation_timestamp"], user["creation_timestamp"])

    def check_fav_ware_from_db(self, before_fav_wares, after_fav_wares):
        """ Сравнить на идентичность избранных товаров до и после какого-то действия.
        :param before_fav_wares: список словарей до какого-то действия
        :param after_fav_wares: список словарей после какого-то действия
        """
        self.assertEqual(len(before_fav_wares), len(after_fav_wares), "Changed the number of favorite user.")
        for user in before_fav_wares:
            fav_data = funcy.where(after_fav_wares, fav_ware_id=user["fav_ware_id"])
            fav_elem = fav_data[0]
            self.assertEqual(len(fav_data), 1)
            self.assertEqual(fav_elem["fav_ware_id"], user["fav_ware_id"])
            self.assertEqual(fav_elem["user_id"], user["user_id"])
            self.assertEqual(fav_elem["creation_timestamp"], user["creation_timestamp"])
