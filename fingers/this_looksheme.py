# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Data\ToDeveloper\bitbucket\LookScheme\rs_looksheme.ui'
#
# Created: Fri Jun 19 16:07:57 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui


class Cord(QtCore.QObject):

    signal = QtCore.Signal(tuple)  # создаем сигнал


class Ui_MainWindow(object):

    def get_settings_frame_descriptions(self):
        self.frame_7 = QtGui.QFrame(self.centralwidget)
        self.frame_7.setGeometry(QtCore.QRect(340, 50, 531, 581))
        self.frame_7.setStyleSheet("#frame_7\n"
                                   "{\n"
                                   "background-color: #253139;\n"
                                   "border-style: normal;\n"
                                   "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                   "border-color: #FFFFFF;\n"
                                   "color: #505d6b;\n"
                                   "font: normal 14px;\n"
                                   "min-width: 10em;\n"
                                   "padding: 8px;\n"
                                   "}\n")
        self.frame_7.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")

    def create_menu(self, MainWindow):
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 893, 21))
        self.menubar.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.menubar.setAcceptDrops(True)
        self.menubar.setToolTip("")
        self.menubar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.menubar.setStyleSheet(self.get_style_menu())
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setAutoFillBackground(False)
        self.menuFile.setInputMethodHints(QtCore.Qt.ImhNone)
        self.menuFile.setTearOffEnabled(False)
        self.menuFile.setSeparatorsCollapsible(False)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setAcceptDrops(False)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

    def setupUi(self, MainWindow):

        self.cord = Cord()  # создаем сигнал

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(893, 672)
        MainWindow.setSizeIncrement(QtCore.QSize(0, 71))
        MainWindow.setStyleSheet("background: #5F6D77;")
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.get_settings_frame_descriptions()

        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 50, 311, 581))
        self.scrollArea.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.scrollArea.setStyleSheet("width: 10px")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 299, 579))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.verticalLayoutWidget = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 281, 602))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)

        self.create_table()
        for index in MainWindow.get_env_schemes():
            self.verticalLayout.addWidget(self.create_elems(index))

        self.scrollAreaWidgetContents.setLayout(self.verticalLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 311, 31))
        self.textBrowser.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textBrowser.setObjectName("textBrowser")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 16, 31, 20))
        self.label_2.setStyleSheet("background-color: rgb(255, 255, 255);\ncolor: rgb(0, 0, 0);")
        self.label_2.setObjectName("label_2")
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(780, 20, 91, 17))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")

        MainWindow.setCentralWidget(self.centralwidget)
        self.create_menu(MainWindow)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        utf_cl = QtGui.QApplication.UnicodeUTF8
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, utf_cl))
        self.checkBox.setText(QtGui.QApplication.translate("MainWindow", "Source config", None, utf_cl))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, utf_cl))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "exit", None, utf_cl))

    def get_style_sheet_frame(self, name):
        fr = "QFrame#%s\n" \
                "{\n" \
                "background-color: #253139;\n"\
                "border-style: normal;\n"\
                "border-width: 2px;\n"\
                "border-radius: 10px;\n"\
                "border-color: #FFFFFF;\n"\
                "color: #505d6b;\n"\
                "font: normal 14px;\n"\
                "min-width: 10em;\n"\
                "padding: 8px;\n"\
                "}\n"\
                "QPushButton#%s_pushButton:hover:!pressed { background-color: #C22E2E } \n"\
                "QPushButton#%s_pushButton:hover { background-color:#EDEF85 }\n"\
                "QPushButton{\n"\
                "background-color: #C54444;\n"\
                "border-width: 2px;\n"\
                "color: black;\n"\
                "border-width: 2px;\n"\
                "border-top-left-radius: 10px;\n"\
                "border-top-right-radius: 10px;\n"\
                "border-bottom-right-radius: 0;\n"\
                "border-bottom-left-radius: 0;\n"\
                "border-color: #FFFFFF;\n"\
                "font: normal 14px;\n"\
                "min-width: 10em;\n"\
                "padding: 5px;\n"\
                "}\n" % (name, name, name)
        return fr

    def get_style_sheet_label(self):
        lbl = "QLabel{\n"\
                "background-color: #253139;\n"\
                "border-style: normal;\n"\
                "color: #FFFFFF;\n"\
                "font: normal 12px;\n"\
                "padding: 5px;\n"\
                "}\n"
        return lbl

    def get_style_menu(self):
        return "QMenuBar {\n"\
                "font: 11pt \"MS Shell Dlg 2\";\n"\
                "background-color: #253139;\n"\
                "color: #FFFFFF    \n"\
                "}\n"\
                "QMenuBar::item {\n"\
                "spacing: 3px; /* spacing between menu bar items */\n"\
                "padding: 1px 4px;\n"\
                "background: transparent;\n"\
                "}\n"\
                "QMenuBar::item:selected { /* when selected using mouse or keyboard */\n"\
                "background: #a8a8a8;\n"\
                "}\n"\
                "QMenuBar::item:pressed {background: #888888;}"

    def create_table(self):
        self.tableWidget = QtGui.QTableWidget(self.frame_7)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 510, 561))
        self.tableWidget.setMinimumSize(QtCore.QSize(510, 521))
        self.tableWidget.setMaximumSize(QtCore.QSize(500, 16777215))
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setStyleSheet("#tableWidget\n"
                "{\n"
                "background-color: #253139;\n"
                "border-style: normal;\n"
                "border-width: 2px;\n"
                "border-color: #FFFFFF;\n"
                "color: #505d6b;\n"
                "font: normal 14px;\n"
                "}\n"
                "")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(5)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)

        utf_cl = QtGui.QApplication.UnicodeUTF8
        translate = QtGui.QApplication.translate
        self.tableWidget.horizontalHeaderItem(0).setText(translate("MainWindow", "Type", None, utf_cl))
        self.tableWidget.setColumnWidth(0, 80)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 180)
        self.tableWidget.horizontalHeaderItem(1).setText(translate("MainWindow", "Name", None, utf_cl))
        self.tableWidget.horizontalHeaderItem(2).setText(translate("MainWindow", "Value", None, utf_cl))

    def clicked_btn(self, scheme):
        """ Отправляем сигнал о текущей схеме для просмотра
        :param scheme: название схемы
        """
        self.cord.signal.emit(scheme)

    def create_elems(self, scheme,):
        coord_button = [0, 0, 281, 31]
        coord_label = [10, 31, 261, 29]
        style_name = scheme + "_frame"
        obj_un = QtGui.QApplication.UnicodeUTF8
        frame_scheme = QtGui.QFrame()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frame_scheme.sizePolicy().hasHeightForWidth())
        frame_scheme.setSizePolicy(sizePolicy)
        frame_scheme.setMinimumSize(QtCore.QSize(190, 61))
        frame_scheme.setStyleSheet(self.get_style_sheet_frame(style_name))
        frame_scheme.setFrameShape(QtGui.QFrame.StyledPanel)
        frame_scheme.setFrameShadow(QtGui.QFrame.Raised)
        frame_scheme.setObjectName(style_name)

        pushButton_scheme = QtGui.QPushButton(frame_scheme)
        pushButton_scheme.setGeometry(QtCore.QRect(*coord_button))
        pushButton_scheme.setObjectName(style_name + "_pushButton")

        # соединяем сигнал от нажатия кнопки со значением схемы
        set_scheme = lambda: self.clicked_btn(scheme)
        QtCore.QObject.connect(pushButton_scheme, QtCore.SIGNAL("clicked()"), set_scheme)

        label_scheme = QtGui.QLabel(frame_scheme)
        label_scheme.setGeometry(QtCore.QRect(*coord_label))
        label_scheme.setStyleSheet(self.get_style_sheet_label())
        label_scheme.setObjectName(style_name + "_label")

        # если название схемы не умещается, ставим многоточие
        if len(scheme) > 30:
            pushButton_scheme.setText(QtGui.QApplication.translate("MainWindow", scheme[:30] + "...", None, obj_un))
        else:
            pushButton_scheme.setText(QtGui.QApplication.translate("MainWindow", scheme, None, obj_un))

        label_scheme.setText(QtGui.QApplication.translate("MainWindow", "Update: 22.06.2015", None, obj_un))
        return frame_scheme

