# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------
#                   Нагрузочное тестирование, пробный тест.
# info: http://docs.locust.io/en/latest/index.html
# Запуск: locust -f ./load_tests/quick_start_locust.py --host=http://front1.test.oorraa.net
# ----------------------------------------------------------------------------------------------
__author__ = 's.trubachev'

from locust import HttpLocust, TaskSet


def login(l):
    l.client.post("/login", {"username": "ellen_key", "password": "education"})


def index(l):
    l.client.get("/")


def profile(l):
    l.client.get("/catalog/670")


class UserBehavior(TaskSet):
    tasks = {index: 2, profile: 1}

    def on_start(self):
        login(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
