# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
#         	Tests accounting worker favorites.
#--------------------------------------------------------------------
import random
import funcy
import funky
from ddt import ddt, data
from support import service_log
from support.utils.db import databases
from support.utils.thrift4req import services
from tests.worker_accounting.class_accounting import AccountingMethods
from tests.worker_accounting.class_favorites import FavoritesCheckMethods

__author__ = 's.trubachev'


class AuxiliaryFavorites(FavoritesCheckMethods):

    @staticmethod
    def clear_fav_wares(user_id, fav_type, wares):
        """ Очистить избранные товары пользователя, если таковые имеются.
        :param user_id: идентификатор пользователя
        :param fav_type: тип избранного
        :param wares: список идентификаторов товаров
        """
        if wares is not None:
            ware_ids = set(funky.pluck(wares, "fav_ware_id"))
            param = FavoritesCheckMethods.get_FavoritesRemoveRequest(user_id, fav_type, fav_ware_ids=ware_ids)
            services.favorites.root.tframed.removeFavorites(param)

    @staticmethod
    def clear_fav_users(user_id, fav_type, users):
        """ Очистить избранные товары пользователя, если таковые имеются.
        :param user_id: идентификатор пользователя
        :param fav_type: тип избранного
        :param users: список идентификаторов товаров
        """
        if users is not None:
            ware_ids = set(funky.pluck(users, "fav_usr_id"))
            param = FavoritesCheckMethods.get_FavoritesRemoveRequest(user_id, fav_type, fav_usr_ids=ware_ids)
            services.favorites.root.tframed.removeFavorites(param)


class TestCheckUserHasFavorite(AuxiliaryFavorites):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        cls.fav_type_ware = cls.get_FavoriteType("WARE")
        cls.fav_type_user = cls.get_FavoriteType("USER")
        cls.user_id = int(AccountingMethods.get_default_user_id('seller_alien'))

        # добавляем пользователей и товары в избранное для проверки удаления
        users = databases.db3.accounting.get_users(limit=5)
        user_ids = [index["id"] for index in users]
        dto_list = cls.generate_dto_list_equal_fav_user(cls.user_id, user_ids)
        param = cls.get_FavoritesAddRequest(dto_list)
        services.favorites.root.tframed.addFavorites(param)

        wares = databases.db2.warehouse.get_wares_with_limit(limit=5)
        ware_ids = [index["ware_id"] for index in wares]
        dto_list = cls.generate_dto_list_equal_fav_ware(cls.user_id, ware_ids)
        param = cls.get_FavoritesAddRequest(dto_list)
        services.favorites.root.tframed.addFavorites(param)

        service_log.preparing_env(cls)

    def test_checkUserHasFavorite_user_is_present(self):
        """ Проверяем, содержится ли пользователь в избранном у указанного пользователя.
        """
        service_log.run(self)
        before_fav_users = databases.db1.favorites.get_fav_users_by_user_id(self.user_id)
        fav_user = random.choice(before_fav_users)
        param = self.get_FavoriteContentDto(self.user_id, self.fav_type_user, fav_user_id=fav_user["fav_usr_id"])
        result = services.favorites.root.tframed.checkUserHasFavorite(param)
        after_fav_users = databases.db1.favorites.get_fav_users_by_user_id(self.user_id)
        self.assertEqual(result, True, "Not found favorite user!")
        self.check_fav_user_from_db(before_fav_users, after_fav_users)

    def test_checkUserHasFavorite_ware_is_present(self):
        """ Проверяем, содержится ли товар в избранном у указанного пользователя.
        """
        service_log.run(self)
        before_fav_wares = databases.db1.favorites.get_fav_wares_by_user_id(self.user_id)
        fav_ware = random.choice(before_fav_wares)
        param = self.get_FavoriteContentDto(self.user_id, self.fav_type_ware, fav_ware_id=fav_ware["fav_ware_id"])
        result = services.favorites.root.tframed.checkUserHasFavorite(param)
        after_fav_wares = databases.db1.favorites.get_fav_wares_by_user_id(self.user_id)
        self.assertEqual(result, True, "Not found favorite ware!")
        self.check_fav_ware_from_db(before_fav_wares, after_fav_wares)

    def test_checkUserHasFavorite_ware_is_not_present(self):
        """ Проверяем, что товар не содержится в избранном у указанного пользователя.
        """
        service_log.run(self)
        # Находим товар которого нет в избранном у пользователя
        fav_wares = databases.db1.favorites.get_fav_wares(limit=200)
        before_fav_wares = databases.db1.favorites.get_fav_wares_by_user_id(self.user_id)
        before_fav_wares_id = [index["fav_ware_id"] for index in before_fav_wares]
        not_present_wares = [index for index in fav_wares if index["fav_ware_id"] not in before_fav_wares_id]
        fav_ware = random.choice(not_present_wares)

        param = self.get_FavoriteContentDto(self.user_id, self.fav_type_ware, fav_ware_id=fav_ware["fav_ware_id"])
        result = services.favorites.root.tframed.checkUserHasFavorite(param)
        after_fav_wares = databases.db1.favorites.get_fav_wares_by_user_id(self.user_id)
        self.assertEqual(result, False, "Found favorite ware!")
        self.check_fav_ware_from_db(before_fav_wares, after_fav_wares)

    def test_checkUserHasFavorite_user_is_not_present(self):
        """ Проверяем, что товар не содержится в избранном у указанного пользователя.
        """
        service_log.run(self)
        # Находим товар которого нет в избранном у пользователя
        fav_users = databases.db1.favorites.get_fav_users(limit=200)
        before_fav_users = databases.db1.favorites.get_fav_users_by_user_id(self.user_id)
        before_fav_users_id = [index["fav_usr_id"] for index in before_fav_users]
        not_present_users = [index for index in fav_users if index["fav_usr_id"] not in before_fav_users_id]
        fav_user = random.choice(not_present_users)

        param = self.get_FavoriteContentDto(self.user_id, self.fav_type_user, fav_user_id=fav_user["fav_usr_id"])
        result = services.favorites.root.tframed.checkUserHasFavorite(param)
        after_fav_users = databases.db1.favorites.get_fav_users_by_user_id(self.user_id)
        self.assertEqual(result, False, "Found favorite ware!")
        self.check_fav_user_from_db(before_fav_users, after_fav_users)

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        service_log.end()


class TestFavoritesWorkerRemove(AuxiliaryFavorites):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        cls.fav_type_ware = cls.get_FavoriteType("WARE")
        cls.fav_type_user = cls.get_FavoriteType("USER")
        cls.user_id = int(AccountingMethods.get_default_user_id('seller_alien'))

        # добавляем пользователей и товары в избранное для проверки удаления
        users = databases.db3.accounting.get_users(limit=5)
        user_ids = [index["id"] for index in users]
        dto_list = cls.generate_dto_list_equal_fav_user(cls.user_id, user_ids)
        param = cls.get_FavoritesAddRequest(dto_list)
        services.favorites.root.tframed.addFavorites(param)

        wares = databases.db2.warehouse.get_wares_with_limit(limit=5)
        ware_ids = [index["ware_id"] for index in wares]
        dto_list = cls.generate_dto_list_equal_fav_ware(cls.user_id, ware_ids)
        param = cls.get_FavoritesAddRequest(dto_list)
        services.favorites.root.tframed.addFavorites(param)

        service_log.preparing_env(cls)

    def test_remove_fav_wares(self):
        """ Проверка удаления товаров в Избранное через метод removeFavorites.
        """
        service_log.run(self)

        before_fav_wares = databases.db1.favorites.get_fav_wares_by_user_id(self.user_id)
        self.assertIsNotNone(before_fav_wares)
        ware_ids = set(funky.pluck(before_fav_wares, "fav_ware_id"))
        param = self.get_FavoritesRemoveRequest(self.user_id, fav_type=self.fav_type_ware, fav_ware_ids=ware_ids)
        result = services.favorites.root.tframed.removeFavorites(param)
        after_fav_wares = databases.db1.favorites.get_fav_wares_by_user_id(self.user_id)
        self.assertIsNone(result)
        self.assertIsNone(after_fav_wares)

    def test_remove_fav_users(self):
        """ Проверка удаления товаров в Избранное через метод removeFavorites.
        """
        service_log.run(self)

        before_fav_users = databases.db1.favorites.get_fav_users_by_user_id(self.user_id)
        self.assertIsNotNone(before_fav_users)
        user_ids = set(funky.pluck(before_fav_users, "fav_usr_id"))
        param = self.get_FavoritesRemoveRequest(self.user_id, fav_type=self.fav_type_user, fav_usr_ids=user_ids)
        result = services.favorites.root.tframed.removeFavorites(param)
        after_fav_users = databases.db1.favorites.get_fav_users_by_user_id(self.user_id)
        self.assertIsNone(result)
        self.assertIsNone(after_fav_users)

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        service_log.end()


@ddt
class TestFavoritesWorkerAdd(AuxiliaryFavorites):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        cls.user_id = int(AccountingMethods.get_default_user_id('seller_alien'))
        cls.fav_type_ware = cls.get_FavoriteType("WARE")
        cls.fav_type_user = cls.get_FavoriteType("USER")
        fav_wares = databases.db1.favorites.get_fav_wares_by_user_id(cls.user_id)
        fav_users = databases.db1.favorites.get_fav_users_by_user_id(cls.user_id)

        # очищаем все избранное у пользователя
        cls.clear_fav_wares(cls.user_id, cls.fav_type_ware, fav_wares)
        cls.clear_fav_users(cls.user_id, cls.fav_type_user, fav_users)
        service_log.preparing_env(cls)

    @data(1, 2, 5, 20)
    def test_add_fav_wares(self, limit_wares=5):
        """ Проверка добавления товаров в Избранное через метод addFavorites.
        """
        service_log.run(self)

        before_fav_wares = databases.db1.favorites.get_fav_wares_by_user_id(self.user_id)

        wares = databases.db2.warehouse.get_wares_with_limit(limit=limit_wares)
        ware_ids = [index["ware_id"] for index in wares]
        dto_list = self.generate_dto_list_equal_fav_ware(self.user_id, ware_ids)
        param = self.get_FavoritesAddRequest(dto_list)
        result = services.favorites.root.tframed.addFavorites(param)

        after_fav_wares = databases.db1.favorites.get_fav_wares_by_user_id(self.user_id)

        self.assertIsNone(before_fav_wares)
        self.assertEqual(len(result.dtoList), limit_wares, "Does not match the number of elements.")
        for index in result.dtoList:
            fav_data = funcy.where(after_fav_wares, fav_ware_id=index.content.favWareId)
            self.check_fav_ware(user_id=self.user_id, data=index, fav_data=fav_data, fav_type=self.fav_type_ware)
            # TODO: в одном случае 0, в другом None - баг: https://jira.oorraa.net/browse/RT-786
            self.assertEqual(index.content.favUserId, 0, "Is not None value favorite users.")

    @data(1, 2, 5, 20)
    def test_add_fav_users(self, limit_users=5):
        """ Проверка добавления товаров в Избранное через метод addFavorites.
        """
        service_log.run(self)

        before_fav_users = databases.db1.favorites.get_fav_wares_by_user_id(self.user_id)

        users = databases.db3.accounting.get_users(limit=limit_users)
        user_ids = [index["id"] for index in users]
        dto_list = self.generate_dto_list_equal_fav_user(self.user_id, user_ids)
        param = self.get_FavoritesAddRequest(dto_list)
        result = services.favorites.root.tframed.addFavorites(param)

        after_fav_users = databases.db1.favorites.get_fav_users_by_user_id(self.user_id)

        self.assertIsNone(before_fav_users)
        self.assertEqual(len(result.dtoList), limit_users, "Does not match the number of elements.")
        for index in result.dtoList:
            fav_data = funcy.where(after_fav_users, fav_usr_id=index.content.favUserId)
            self.check_fav_user(user_id=self.user_id, data=index, fav_data=fav_data, fav_type=self.fav_type_user)

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        service_log.end()


@ddt
class TestFavoritesWorkerFind(AuxiliaryFavorites):

    @classmethod
    def setUp(cls):
        """ Пре-установка окружения для теста.
        """
        cls.user_id = int(AccountingMethods.get_default_user_id('seller_alien'))
        cls.fav_type_ware = cls.get_FavoriteType("WARE")
        cls.fav_type_user = cls.get_FavoriteType("USER")
        fav_wares = databases.db1.favorites.get_fav_wares_by_user_id(cls.user_id)
        fav_users = databases.db1.favorites.get_fav_users_by_user_id(cls.user_id)

        # очищаем все избранное у пользователя
        cls.clear_fav_wares(cls.user_id, cls.fav_type_ware, fav_wares)
        cls.clear_fav_users(cls.user_id, cls.fav_type_user, fav_users)

        service_log.preparing_env(cls)

    @data(1, 2, 5, 20)
    def test_find_fav_wares_for_user(self, limit_wares=5):
        """ Проверка выборки избранных товаров пользователя.
        :param limit_wares: количество добавляемых товаров для проверки
        """
        service_log.run(self)

        wares = databases.db2.warehouse.get_wares_with_limit(limit=limit_wares)
        ware_ids = [index["ware_id"] for index in wares]
        dto_list = self.generate_dto_list_equal_fav_ware(self.user_id, ware_ids)
        add_fav_param = self.get_FavoritesAddRequest(dto_list)
        services.favorites.root.tframed.addFavorites(add_fav_param)

        param = self.get_UsersFavoritesRequest(user_id=self.user_id, fav_type=self.fav_type_ware)
        result = services.favorites.root.tframed.findUsersFavoritesByParams(param)
        f_wares = databases.db1.favorites.get_fav_wares_by_user_id(self.user_id)

        self.assertEqual(len(f_wares), len(result.dtoList), "Different length of lists.")
        self.assertEqual(len(f_wares), result.totalCount, "Wrong value totalCount.")

        for ware in result.dtoList:
            fav_data = funcy.where(f_wares, fav_ware_id=ware.content.favWareId)
            self.check_fav_ware(user_id=self.user_id, data=ware, fav_data=fav_data, fav_type=self.fav_type_ware)
            self.assertIsNone(ware.content.favUserId, "Is not None value favorite users.")

    @data(1, 2, 5, 20)
    def test_find_fav_users_for_user(self, limit_users=5):
        """ Проверка выборки избранных пользователей у пользователя.
        :param limit_users: количество добавляемых пользователей для проверки
        """
        service_log.run(self)

        users = databases.db3.accounting.get_users(limit=limit_users)
        user_ids = [index["id"] for index in users]
        dto_list = self.generate_dto_list_equal_fav_user(self.user_id, user_ids)
        add_fav_param = self.get_FavoritesAddRequest(dto_list)
        services.favorites.root.tframed.addFavorites(add_fav_param)

        param = self.get_UsersFavoritesRequest(user_id=self.user_id, fav_type=self.fav_type_user)
        result = services.favorites.root.tframed.findUsersFavoritesByParams(param)
        f_wares = databases.db1.favorites.get_fav_users_by_user_id(self.user_id)

        self.assertEqual(len(f_wares), len(result.dtoList), "Different length of lists.")
        self.assertEqual(len(f_wares), result.totalCount, "Wrong value totalCount.")

        for user in result.dtoList:
            fav_data = funcy.where(f_wares, fav_usr_id=user.content.favUserId)
            self.check_fav_user(user_id=self.user_id, data=user, fav_data=fav_data, fav_type=self.fav_type_user)

    @classmethod
    def tearDown(cls):
        """ Пост-работа после завершения теста.
        """
        service_log.end()