# coding=utf-8
import time
from support import service_log
from tests.MainClass import MainClass


__author__ = 'm.senchuk'


class HelpGoodCreateData(MainClass):
    pass


class HelpGoodCreateMethods(HelpGoodCreateData):
    @staticmethod
    def add_photo2(image_path):
        """
        Метод добавляет фото по указанному пути
        :param image_path: - абсолютный путь до фото
        :return:
        """
        #from PyAutoItPy import AutoItX, WinHandle
        #Automat=AutoItX()
        #title = "[CLASS:#32770]"
        #control = '[CLASS:Edit; INSTANCE:1]'
        #opened = Automat.WinWait(title, 5)
        #handle = WinHandle(Automat.WinGetHandle(title))
        #active = Automat.WinActivate(handle)
        #focus = Automat.ControlFocus(handle, control)
        #time.sleep(1)
        #p = Automat.ControlSetText(handle, control, image_path)
        ##ENTER - подтверждение (можно вместо этого нажать на кнопку)
        #Automat.Send("{ENTER}")
        #time.sleep(5)
        #return p
        # TODO: deprecate!
        pass


    @staticmethod
    def add_photo(image_path):
        """
        Метод добавляет фото по указанному пути
        :param image_path: - абсолютный путь до фото
        :return:
        """
        import autoit

        title = "[CLASS:#32770]"
        control = '[CLASS:Edit; INSTANCE:1]'
        control_open_btn = '[CLASS:Button; INSTANCE:1]'
        opened = autoit.win_wait(title, 5)
        if opened != 1:
            msg = "Not opened window!"
            service_log.error(msg)
            assert msg
        handle = autoit.win_get_handle(title)
        if isinstance(handle, int) is not True:
            msg = "Not found Handle!"
            service_log.error(msg)
            assert msg
        autoit.win_activate_by_handle(handle)
        ret = autoit.control_focus(title, control)
        if ret != 1:
            msg = "Not found control_focus!"
            service_log.error(msg)
            assert msg
        time.sleep(1)
        autoit.control_set_text(title, control, image_path)
        autoit.control_focus(title, control_open_btn)
        autoit.control_click(title, control_open_btn)
        #autoit.mouse_click()
        #ENTER - подтверждение (можно вместо этого нажать на кнопку)
        #autoit.send("{ENTER}")
        time.sleep(5)
        return True


class HelpGoodCreateCheckMethods(HelpGoodCreateMethods):
    def check_add_photo(self, img_path):
        """
        Метод проверяет, что путь до изображения успешно вставлен в диалоговое окно
        :param img_path:
        :return:
        """
        paste_img_path = self.add_photo(img_path)
        self.assertTrue(paste_img_path, "Путь до фото не был вставлен в диалоговое окно")