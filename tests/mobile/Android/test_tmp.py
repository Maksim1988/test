# -*- coding: utf-8 -*-
import time
from support import service_log
from support.utils.exec_cmd import CmdWork, cmd_work
from support.utils.webserver import start_WebServer
from tests.get_coverage import j_files

__author__ = 's.trubachev'

# Android environment
import unittest
import os
from appium import webdriver

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

NAME_APK = "OORRAA_2_2_0_RC_HTTPS.apk"
PATH_APK = '../../../tmp/' + NAME_APK
# sdk C:\Users\s.trubachev\AppData\Local\Android\sdk
REMOTE_URL = "http://localhost:4723/wd/hub"
emulator = "emulator.exe -avd Nexus_S_API_23"
# tskill 3432
# tasklist /FI "WINDOWTITLE eq 5554:Nexus_S_API_23"
# emulator-x86.exe
# tasklist /FI "IMAGENAME eq emulator-x86.exe"


class AndroidMethods(unittest.TestCase):

    @staticmethod
    def turn_off_android_emulator(driver):
        """ Выключить устройство.
        :param driver: ссылка на драйвер
        :return: True
        """
        service_log.put("Initiated the process to TURN OFF the Android emulator...\n")
        driver.long_press_keycode(26)
        return True

    @staticmethod
    def go_home(driver):
        """ Нажать на клавишу - ДОМОЙ.
        :param driver: ссылка на драйвер
        """
        driver.press_keycode(3)
        return True

    @staticmethod
    def close_android_emulator(driver):
        """ Завершить работу эмулятора.
        1) Выключаем устройство.
        2) Завершем работу драйвера для связи с эмулятором.
        3) Убиваем процесс эмулятора.
        :param driver: ссылка на драйвер
        """
        AndroidMethods.turn_off_android_emulator(driver)
        driver.quit()
        cmd_work.kill_android_emulator()
        return True

    @staticmethod
    def start_android_emulator(self):
        pass


class SimpleAndroidTests(AndroidMethods):

    def setUp(self):
        p = j_files
        desired_caps = dict()
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0'
        desired_caps['deviceName'] = 'emulator-5554'
        desired_caps['app'] = PATH(PATH_APK)

        #cmd_work.start_android_emulator(70)
        # adb start-server
        #cmd_work.start_appium()
        cmd_work.adb_start_server()
        cmd_work.start_cmd_appium()
        self.driver = webdriver.Remote(REMOTE_URL, desired_caps)
        time.sleep(5)
        #self.driver.createSession()

    def find_text_view_and_click(self, text, num_text_view, time_sleep=0):
        """ Найти на странице TextView с определенным названием и нажать его.
        :return: True
        """
        el = self.driver.find_elements_by_class_name('android.widget.TextView')[num_text_view]
        service_log.put("Element: %s" % str(el))
        self.assertEqual(el.text, text, "This element not have text - %s." % text)
        el.click()
        time.sleep(time_sleep)
        return True

    def test_apk(self):
        self.find_text_view_and_click("Next", 3)  # page 1: Welcom to OORRAA
        self.find_text_view_and_click("Next", 3)  # page 2: 'Get in contact'
        self.find_text_view_and_click("Next", 3)  # page 3: 'Convenient search'
        self.find_text_view_and_click("Next", 3)  # page 4: 'Create shop'
        self.find_text_view_and_click("Done", 2)  # page 5: 'Done'
        self.find_text_view_and_click("OORRAA server", 1)  # page Choice 'OORRAA server' for test

        time.sleep(10)
        #el = self.driver.find_element_by_accessibility_id('Arcs')
        #self.assertIsNotNone(el)
        #self.driver.back()
        #el = self.driver.find_element_by_accessibility_id("App")
        #self.assertIsNotNone(el)
        #els = self.driver.find_elements_by_android_uiautomator("new UiSelector().clickable(true)")
        #self.assertGreaterEqual(12, len(els))
        #self.driver.find_element_by_android_uiautomator('text("API Demos")')

    def tearDown(self):
        # end the session
        self.close_android_emulator(self.driver)
        cmd_work.adb_stop_server()
        #cmd_work.kill_cmd_appium()


