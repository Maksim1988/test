# -*- coding: utf-8 -*-
"""
Feature: Работа с ссессиями и автологин
"""
from unittest import skip
from support.utils.common_utils import priority



class TestUserSessions():
    """
    Story: Сохранине сессии пользователя
    """

    @skip('manual')
    @priority("Must")
    def test_user_must_be_authorized_when_i_refresh_page(self):
        """
        Title: Проверить, что при обновлении страницы пользователь остается залогиненным
        """
        pass

    @skip('manual')
    @priority("Must")
    def test_user_must_be_auto_authorized_when_i_close_and_open_again_page(self):
        """
        Title: Проверить, что при закрытии вкладки браузера и открытии ее снова пользователь остается залогиненным
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_disabled_user_not_autologin(self):
        """
        Title: Проверить, что для заблокированного (DISABLED) пользователя не происходит автологин
        """
        pass



class TestUserSessionsDetaled():
    """
    Story: Детальная проверка ссесий
    """

    @skip('manual')
    @priority("Medium")
    def test_save_session_id_in_cookie(self):
        """
        Title: Проверить, что при заходе на сайт в cookie записывается session ID
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_save_contextType(self):
        """
        Title: Проверить, что при авторизации на сайте session Id не изменяется и создается новая запись контекста c contextType = auth
        """
        pass

    @skip('manual')
    @priority("Medium")
    def test_save_contextType(self):
        """
        Title: Проверить, что при заходе на сайт из разных браузеров и авторизации создаются свои session ID и контексты
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_end_live_time_of_session(self):
        """
        Title: Проверить что после окончания времени жизни контекста ссесии, автологин не происходит и пользователю нужно самому выполнить логин
        """
        pass



class SynchronLoginOrLogoutFromBrowserTabs():
    """
    Story: Синхронизация login\logout между всеми вкладками браузера пользователя
    """
    @skip('manual')
    @priority("High")
    def test_auto_login_or_logout_in_tabs_browser(self):
        """
        Title: Авто login\logout в пределах вкладок одного браузера
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_not_auto_login_or_logout_in_private_tab(self):
        """
        Title: Отсутствие авто login\logout в приватной вкладке
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_not_auto_login_or_logout_in_other_browser(self):
        """
        Title: Отсутствие авто login\logout в другом браузере
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_auto_login_or_logout_when_registration_finished(self):
        """
        Title: Авто login на открытых вкладках браузера при завершении регистрации на одной из них
        """
        pass
