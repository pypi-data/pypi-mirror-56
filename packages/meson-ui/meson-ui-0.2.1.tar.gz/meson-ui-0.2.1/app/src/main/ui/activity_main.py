# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app/src/res/layout/activity_main.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("border: 0px solid #263238;\n"
"background-color: rgb(41, 41, 49);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setGeometry(QtCore.QRect(30, 15, 81, 81))
        self.label_logo.setStyleSheet("QLineEdit {\n"
"    url(:/icons/icons/ic_app.png)\n"
"}")
        self.label_logo.setText("")
        self.label_logo.setPixmap(QtGui.QPixmap(":/ic_res/icons/ic_app.png"))
        self.label_logo.setScaledContents(True)
        self.label_logo.setObjectName("label_logo")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(130, 18, 591, 66))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_source = QtWidgets.QLabel(self.layoutWidget)
        self.label_source.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_source.setObjectName("label_source")
        self.horizontalLayout_3.addWidget(self.label_source)
        self.source_dir = QtWidgets.QLineEdit(self.layoutWidget)
        self.source_dir.setStyleSheet("QLineEdit {\n"
"    border-width: 5px;\n"
"    border-radius: 15px;\n"
"    font: 13pt \"Gill Sans\";\n"
"    border: 2px solid gray;\n"
"    border-radius: 10px;\n"
"    padding: 2 10px;\n"
"    background: rgb(255, 255, 255);\n"
"    color: rgb(0, 0, 0);\n"
"    selection-background-color: rgb(233, 233, 233);\n"
"}")
        self.source_dir.setObjectName("source_dir")
        self.horizontalLayout_3.addWidget(self.source_dir)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lable_build = QtWidgets.QLabel(self.layoutWidget)
        self.lable_build.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.lable_build.setObjectName("lable_build")
        self.horizontalLayout_4.addWidget(self.lable_build)
        self.build_dir = QtWidgets.QLineEdit(self.layoutWidget)
        self.build_dir.setStyleSheet("QLineEdit {\n"
"    border-width: 5px;\n"
"    border-radius: 15px;\n"
"    font: 13pt \"Gill Sans\";\n"
"    border: 2px solid gray;\n"
"    border-radius: 10px;\n"
"    padding: 2 10px;\n"
"    background: rgb(255, 255, 255);\n"
"    color: rgb(0, 0, 0);\n"
"    selection-background-color: rgb(233, 233, 233);\n"
"}")
        self.build_dir.setObjectName("build_dir")
        self.horizontalLayout_4.addWidget(self.build_dir)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.push_open = QtWidgets.QPushButton(self.centralwidget)
        self.push_open.setGeometry(QtCore.QRect(726, 16, 36, 30))
        self.push_open.setStyleSheet("QPushButton {\n"
"    background-color: rgb(105, 105, 105);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: rgb(127, 127, 127);\n"
"    color: rgb(255, 255, 255);\n"
"    font: 13pt \"Gill Sans\";\n"
"    min-width: 2em;\n"
"    padding: 1px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(127, 127, 127);\n"
"    border-style: inset;\n"
"    color: rgb(36, 255, 6);\n"
"}")
        self.push_open.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ic_res/icons/open_dir.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_open.setIcon(icon)
        self.push_open.setObjectName("push_open")
        self.mesonui_output_console = QtWidgets.QTextEdit(self.centralwidget)
        self.mesonui_output_console.setGeometry(QtCore.QRect(40, 430, 721, 81))
        self.mesonui_output_console.setStyleSheet("QTextEdit {\n"
"    background-attachment: scroll;\n"
"    background-color: rgb(63, 63, 63);\n"
"    border-color: rgb(245, 251, 251);\n"
"    border-style: outset;\n"
"    border-width: 1px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    padding: 6px;\n"
"    color: rgb(63, 255, 6);\n"
"    font: 13pt \"Monaco\";\n"
"}")
        self.mesonui_output_console.setReadOnly(True)
        self.mesonui_output_console.setObjectName("mesonui_output_console")
        self.push_clean = QtWidgets.QPushButton(self.centralwidget)
        self.push_clean.setGeometry(QtCore.QRect(595, 523, 166, 31))
        self.push_clean.setStyleSheet("QPushButton {\n"
"    background-color: rgb(105, 105, 105);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: rgb(127, 127, 127);\n"
"    color: rgb(255, 255, 255);\n"
"    font: 13pt \"Gill Sans\";\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(127, 127, 127);\n"
"    border-style: inset;\n"
"    color: rgb(36, 255, 6);\n"
"}")
        self.push_clean.setObjectName("push_clean")
        self.push_docs = QtWidgets.QPushButton(self.centralwidget)
        self.push_docs.setGeometry(QtCore.QRect(35, 523, 166, 31))
        self.push_docs.setStyleSheet("QPushButton {\n"
"    background-color: rgb(105, 105, 105);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: rgb(127, 127, 127);\n"
"    color: rgb(255, 255, 255);\n"
"    font: 13pt \"Gill Sans\";\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(127, 127, 127);\n"
"    border-style: inset;\n"
"    color: rgb(36, 255, 6);\n"
"}")
        self.push_docs.setObjectName("push_docs")
        self.push_clear = QtWidgets.QPushButton(self.centralwidget)
        self.push_clear.setGeometry(QtCore.QRect(726, 54, 36, 30))
        self.push_clear.setStyleSheet("QPushButton {\n"
"    background-color: rgb(105, 105, 105);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: rgb(127, 127, 127);\n"
"    color: rgb(255, 255, 255);\n"
"    font: 13pt \"Gill Sans\";\n"
"    min-width: 2em;\n"
"    padding: 1px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(127, 127, 127);\n"
"    border-style: inset;\n"
"    color: rgb(36, 255, 6);\n"
"}")
        self.push_clear.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/ic_res/icons/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_clear.setIcon(icon1)
        self.push_clear.setObjectName("push_clear")
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(40, 110, 721, 86))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.push_setup = QtWidgets.QPushButton(self.layoutWidget1)
        self.push_setup.setStyleSheet("QPushButton {\n"
"    background-color: rgb(105, 105, 105);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: rgb(127, 127, 127);\n"
"    color: rgb(255, 255, 255);\n"
"    font: 13pt \"Gill Sans\";\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(127, 127, 127);\n"
"    border-style: inset;\n"
"    color: rgb(36, 255, 6);\n"
"}")
        self.push_setup.setObjectName("push_setup")
        self.horizontalLayout.addWidget(self.push_setup)
        self.push_build = QtWidgets.QPushButton(self.layoutWidget1)
        self.push_build.setStyleSheet("QPushButton {\n"
"    background-color: rgb(105, 105, 105);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: rgb(127, 127, 127);\n"
"    color: rgb(255, 255, 255);\n"
"    font: 13pt \"Gill Sans\";\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(127, 127, 127);\n"
"    border-style: inset;\n"
"    color: rgb(36, 255, 6);\n"
"}")
        self.push_build.setObjectName("push_build")
        self.horizontalLayout.addWidget(self.push_build)
        self.push_install = QtWidgets.QPushButton(self.layoutWidget1)
        self.push_install.setStyleSheet("QPushButton {\n"
"    background-color: rgb(105, 105, 105);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: rgb(127, 127, 127);\n"
"    color: rgb(255, 255, 255);\n"
"    font: 13pt \"Gill Sans\";\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(127, 127, 127);\n"
"    border-style: inset;\n"
"    color: rgb(36, 255, 6);\n"
"}")
        self.push_install.setObjectName("push_install")
        self.horizontalLayout.addWidget(self.push_install)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.push_intro = QtWidgets.QPushButton(self.layoutWidget1)
        self.push_intro.setStyleSheet("QPushButton {\n"
"    background-color: rgb(105, 105, 105);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: rgb(127, 127, 127);\n"
"    color: rgb(255, 255, 255);\n"
"    font: 13pt \"Gill Sans\";\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(127, 127, 127);\n"
"    border-style: inset;\n"
"    color: rgb(36, 255, 6);\n"
"}")
        self.push_intro.setObjectName("push_intro")
        self.horizontalLayout_2.addWidget(self.push_intro)
        self.push_test = QtWidgets.QPushButton(self.layoutWidget1)
        self.push_test.setStyleSheet("QPushButton {\n"
"    background-color: rgb(105, 105, 105);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: rgb(127, 127, 127);\n"
"    color: rgb(255, 255, 255);\n"
"    font: 13pt \"Gill Sans\";\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(127, 127, 127);\n"
"    border-style: inset;\n"
"    color: rgb(36, 255, 6);\n"
"}")
        self.push_test.setObjectName("push_test")
        self.horizontalLayout_2.addWidget(self.push_test)
        self.push_dist = QtWidgets.QPushButton(self.layoutWidget1)
        self.push_dist.setStyleSheet("QPushButton {\n"
"    background-color: rgb(105, 105, 105);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: rgb(127, 127, 127);\n"
"    color: rgb(255, 255, 255);\n"
"    font: 13pt \"Gill Sans\";\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(127, 127, 127);\n"
"    border-style: inset;\n"
"    color: rgb(36, 255, 6);\n"
"}")
        self.push_dist.setObjectName("push_dist")
        self.horizontalLayout_2.addWidget(self.push_dist)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.targets_view = QtWidgets.QTableWidget(self.centralwidget)
        self.targets_view.setGeometry(QtCore.QRect(40, 208, 721, 211))
        self.targets_view.setAutoFillBackground(True)
        self.targets_view.setStyleSheet("QTableWidget {\n"
"    border: 1px solid #cccccc;\n"
"    border-radius: 5px;\n"
"    background-color: rgb(83, 87, 86);\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    border-bottom: 1px solid;\n"
"    background-color: rgb(96, 96, 96);\n"
"    color: rgb(56, 139, 12);\n"
"}\n"
"\n"
"QTableWidget::item:hover {\n"
"    border: 1px solid rgb(57, 187, 3);\n"
"    border-radius: 5px;\n"
"    background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"    background: #263238;                /* Background where slider is not */\n"
"    height: 10px;\n"
"    margin: 0;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    background: #263238;                /* Background where slider is not */\n"
"    width: 10px;\n"
"    margin: 0;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(152, 152, 152);                    /* Slider color */\n"
"    min-width: 16px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: rgb(152, 152, 152);                    /* Slider color */\n"
"    min-height: 16px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal,\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;                                                /* Removes the dotted background */\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {    /* Hides the slider arrows */\n"
"      border: none;\n"
"      background: none;\n"
"}\n"
"\n"
"\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"    color: #546E7A;\n"
"    border: 1px solid transparent;\n"
"    padding: 4px 22px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color: #AFBDC4;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background: transparent;\n"
"    border: 1px solid transparent;\n"
"    color: #546E7A;\n"
"}\n"
"\n"
"QSpinBox {\n"
"    background: transparent;\n"
"    border: 1px solid transparent;\n"
"    color: #546E7A;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: gray;\n"
"    color: white;\n"
"    padding-left: 10px;\n"
"    border: 1px solid #6c6c6c;\n"
"}\n"
"\n"
"/* style the sort indicator */\n"
"QHeaderView::down-arrow {\n"
"    image: url(:/ic_res/icons/down_arrow.png);\n"
"}\n"
"\n"
"QHeaderView::up-arrow {\n"
"    image: url(:/ic_res/icons/down_arrow.png);\n"
"}")
        self.targets_view.setObjectName("targets_view")
        self.targets_view.setColumnCount(1)
        self.targets_view.setRowCount(14)
        item = QtWidgets.QTableWidgetItem()
        self.targets_view.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.targets_view.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.targets_view.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.targets_view.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.targets_view.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.targets_view.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.targets_view.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.targets_view.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.targets_view.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.targets_view.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.targets_view.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.targets_view.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.targets_view.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.targets_view.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.targets_view.setHorizontalHeaderItem(0, item)
        self.targets_view.horizontalHeader().setVisible(False)
        self.targets_view.horizontalHeader().setCascadingSectionResizes(False)
        self.targets_view.horizontalHeader().setSortIndicatorShown(False)
        self.targets_view.horizontalHeader().setStretchLastSection(True)
        self.targets_view.verticalHeader().setCascadingSectionResizes(True)
        self.targets_view.verticalHeader().setSortIndicatorShown(False)
        self.targets_view.verticalHeader().setStretchLastSection(False)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.actionMeson_docs = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/ic_res/icons/ic_docs.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMeson_docs.setIcon(icon2)
        self.actionMeson_docs.setObjectName("actionMeson_docs")
        self.actionMeson_QnA = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/ic_res/icons/qna_ic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMeson_QnA.setIcon(icon3)
        self.actionMeson_QnA.setObjectName("actionMeson_QnA")
        self.actionMeson_ui_issue = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/ic_res/icons/github_ic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMeson_ui_issue.setIcon(icon4)
        self.actionMeson_ui_issue.setObjectName("actionMeson_ui_issue")
        self.actionMeson_issue = QtWidgets.QAction(MainWindow)
        self.actionMeson_issue.setIcon(icon4)
        self.actionMeson_issue.setObjectName("actionMeson_issue")
        self.menuHelp.addAction(self.actionMeson_docs)
        self.menuHelp.addAction(self.actionMeson_QnA)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionMeson_ui_issue)
        self.menuHelp.addAction(self.actionMeson_issue)
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Meson-ui"))
        self.label_source.setText(_translate("MainWindow", "Source directory:"))
        self.lable_build.setText(_translate("MainWindow", "Builddir directory:"))
        self.push_clean.setText(_translate("MainWindow", "Clean project"))
        self.push_docs.setText(_translate("MainWindow", "Meson docs"))
        self.push_setup.setText(_translate("MainWindow", "Setup project"))
        self.push_build.setText(_translate("MainWindow", "Build project"))
        self.push_install.setText(_translate("MainWindow", "Install project"))
        self.push_intro.setText(_translate("MainWindow", "Introspect"))
        self.push_test.setText(_translate("MainWindow", "Test project"))
        self.push_dist.setText(_translate("MainWindow", "Dist project"))
        item = self.targets_view.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "name"))
        item = self.targets_view.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "type"))
        item = self.targets_view.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "id"))
        item = self.targets_view.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "defined_in"))
        item = self.targets_view.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "filename"))
        item = self.targets_view.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "build_by_default"))
        item = self.targets_view.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "language"))
        item = self.targets_view.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "compiler"))
        item = self.targets_view.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "parameters"))
        item = self.targets_view.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "sources"))
        item = self.targets_view.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "generated_sources"))
        item = self.targets_view.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "subproject"))
        item = self.targets_view.verticalHeaderItem(12)
        item.setText(_translate("MainWindow", "installed"))
        item = self.targets_view.verticalHeaderItem(13)
        item.setText(_translate("MainWindow", "install_filename"))
        item = self.targets_view.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Value"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionMeson_docs.setText(_translate("MainWindow", "Meson docs"))
        self.actionMeson_QnA.setText(_translate("MainWindow", "Meson QnA"))
        self.actionMeson_ui_issue.setText(_translate("MainWindow", "Meson-ui issue"))
        self.actionMeson_issue.setText(_translate("MainWindow", "Meson issue"))
from . import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
