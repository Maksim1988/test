# -*- coding: utf-8 -*-
"""
Feature: Live-chat
"""
from unittest import skip
from support.utils.common_utils import priority


class ConnectToSupportViaLiveChat():
    """
    Story: Связатьс со службой поддержки через liveChat
    """

    @skip('manual')
    @priority("Low")
    def test_connect_to_support_via_live_chat(self):
        """
        Title: Я могу написать сообщение оператору, который онлайн. Текс сообщения прийдет оператору
        Description:
        Что бы проверить функционал чата, возможно понадобится доступ и пароль к админке live-chat.
        Т.к. live-chat показывается на сайте только в том случае, если есть активный оператор.
        Админка: https://my.livechatinc.com/chats
        Логин: support@oorraa.net
        Пароль Oorraa2811_
        """
        pass




class LiveChatWindow():
    """
    Story: Окно LiveChat
    """

    @skip('manual')
    @priority("Low")
    def test_live_chat_minimaze_or_maximize(self):
        """
        Title: Окно LiveChat можно свернуть \ развернуть
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_live_chat_close(self):
        """
        Title: Окно LiveChat можно закрыть
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_live_chat_view(self):
        """
        Title: Внешний вид окна Live Chat
        Description:
        В развернутом виде: аватар и имя ореатора, окно чата, приветственное сообщение оператора, форма для ввода текста.
        """
        pass

    @skip('manual')
    @priority("Low")
    def test_live_on_all_pages(self):
        """
        Title: Отображение окна livechat на всех страницах сайта
        """
        pass

