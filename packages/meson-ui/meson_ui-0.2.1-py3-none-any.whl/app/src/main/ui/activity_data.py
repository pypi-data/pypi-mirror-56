# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app/src/res/layout/activity_data.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IntroDialog(object):
    def setupUi(self, IntroDialog):
        IntroDialog.setObjectName("IntroDialog")
        IntroDialog.resize(731, 459)
        IntroDialog.setStyleSheet("background-color: rgb(41, 41, 49);")
        self.tab_unittests = QtWidgets.QTabWidget(IntroDialog)
        self.tab_unittests.setGeometry(QtCore.QRect(-1, 0, 741, 401))
        self.tab_unittests.setStyleSheet("QTabWidget::pane { /* The tab widget frame */\n"
"    border-top: 2px solid #C2C7CB;\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    left: 5px; /* move to the right by 5px */\n"
"}\n"
"\n"
"/* Style the tab using the tab sub-control. Note that\n"
"    it reads QTabBar _not_ QTabWidget */\n"
"QTabBar::tab {\n"
"    background: rgb(123, 123, 123);\n"
"    border: 2px solid #C4C4C3;\n"
"    border-bottom-color: #C2C7CB; /* same as the pane color */\n"
"    border-top-left-radius: 8px;\n"
"    border-top-right-radius: 8px;\n"
"    min-width: 10ex;\n"
"    padding: 2 15px;\n"
"}\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"    background: rgb(148, 147, 147);\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    border-color: #9B9B9B;\n"
"    border-bottom-color: #C2C7CB; /* same as pane color */\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    margin-top: 2px; /* make non-selected tabs look smaller */\n"
"}\n"
"\n"
"/* make use of negative margins for overlapping tabs */\n"
"QTabBar::tab:selected {\n"
"    /* expand/overlap to the left and right by 4px */\n"
"    margin-left: -4px;\n"
"    margin-right: -4px;\n"
"}\n"
"\n"
"QTabBar::tab:first:selected {\n"
"    margin-left: 0; /* the first selected tab has nothing to overlap with on the left */\n"
"}\n"
"\n"
"QTabBar::tab:last:selected {\n"
"    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
"}\n"
"\n"
"QTabBar::tab:only-one {\n"
"    margin: 0; /* if there is only one tab, we don\'t want overlapping margins */\n"
"}\n"
"")
        self.tab_unittests.setObjectName("tab_unittests")
        self.tab_projectinfo = QtWidgets.QWidget()
        self.tab_projectinfo.setObjectName("tab_projectinfo")
        self.groupBox = QtWidgets.QGroupBox(self.tab_projectinfo)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 731, 371))
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setStyleSheet("QGroupBox {\n"
"    background-color: rgb(113, 113, 113);\n"
"    color: rgb(255, 255, 255);\n"
"    border: 2px solid gray;\n"
"    border-radius: 10px;\n"
"    margin-top: 1ex; /* leave space at the top for the title */\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center; /* position at the top center */\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 0 50px;\n"
"    background-color: rgb(141, 141, 141);\n"
"}")
        self.groupBox.setObjectName("groupBox")
        self.frame_4 = QtWidgets.QFrame(self.groupBox)
        self.frame_4.setGeometry(QtCore.QRect(372, 20, 341, 211))
        self.frame_4.setStyleSheet("background-color: rgb(113, 113, 113);")
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.table_projectinfo = QtWidgets.QTableWidget(self.groupBox)
        self.table_projectinfo.setGeometry(QtCore.QRect(20, 30, 691, 321))
        self.table_projectinfo.setAutoFillBackground(True)
        self.table_projectinfo.setStyleSheet("QTableWidget {\n"
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
        self.table_projectinfo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.table_projectinfo.setLineWidth(1)
        self.table_projectinfo.setObjectName("table_projectinfo")
        self.table_projectinfo.setColumnCount(1)
        self.table_projectinfo.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.table_projectinfo.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_projectinfo.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_projectinfo.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_projectinfo.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_projectinfo.setHorizontalHeaderItem(0, item)
        self.table_projectinfo.horizontalHeader().setVisible(False)
        self.table_projectinfo.horizontalHeader().setCascadingSectionResizes(False)
        self.table_projectinfo.horizontalHeader().setSortIndicatorShown(False)
        self.table_projectinfo.horizontalHeader().setStretchLastSection(True)
        self.table_projectinfo.verticalHeader().setCascadingSectionResizes(False)
        self.table_projectinfo.verticalHeader().setSortIndicatorShown(False)
        self.table_projectinfo.verticalHeader().setStretchLastSection(False)
        self.tab_unittests.addTab(self.tab_projectinfo, "")
        self.tab_target = QtWidgets.QWidget()
        self.tab_target.setObjectName("tab_target")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_target)
        self.groupBox_5.setGeometry(QtCore.QRect(0, 0, 731, 371))
        self.groupBox_5.setAutoFillBackground(False)
        self.groupBox_5.setStyleSheet("QGroupBox {\n"
"    background-color: rgb(113, 113, 113);\n"
"    color: rgb(255, 255, 255);\n"
"    border: 2px solid gray;\n"
"    border-radius: 10px;\n"
"    margin-top: 1ex; /* leave space at the top for the title */\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center; /* position at the top center */\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 0 50px;\n"
"    background-color: rgb(141, 141, 141);\n"
"}")
        self.groupBox_5.setObjectName("groupBox_5")
        self.frame_8 = QtWidgets.QFrame(self.groupBox_5)
        self.frame_8.setGeometry(QtCore.QRect(372, 20, 341, 211))
        self.frame_8.setStyleSheet("background-color: rgb(113, 113, 113);")
        self.frame_8.setObjectName("frame_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.table_targets = QtWidgets.QTableWidget(self.groupBox_5)
        self.table_targets.setGeometry(QtCore.QRect(20, 30, 691, 321))
        self.table_targets.setAutoFillBackground(True)
        self.table_targets.setStyleSheet("QTableWidget {\n"
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
        self.table_targets.setObjectName("table_targets")
        self.table_targets.setColumnCount(1)
        self.table_targets.setRowCount(14)
        item = QtWidgets.QTableWidgetItem()
        self.table_targets.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_targets.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_targets.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_targets.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_targets.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_targets.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_targets.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_targets.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_targets.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_targets.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_targets.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_targets.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_targets.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_targets.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_targets.setHorizontalHeaderItem(0, item)
        self.table_targets.horizontalHeader().setVisible(False)
        self.table_targets.horizontalHeader().setStretchLastSection(True)
        self.table_targets.verticalHeader().setCascadingSectionResizes(False)
        self.table_targets.verticalHeader().setStretchLastSection(False)
        self.tab_unittests.addTab(self.tab_target, "")
        self.tab_unittest = QtWidgets.QWidget()
        self.tab_unittest.setObjectName("tab_unittest")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_unittest)
        self.groupBox_4.setGeometry(QtCore.QRect(0, 0, 731, 371))
        self.groupBox_4.setAutoFillBackground(False)
        self.groupBox_4.setStyleSheet("QGroupBox {\n"
"    background-color: rgb(113, 113, 113);\n"
"    color: rgb(255, 255, 255);\n"
"    border: 2px solid gray;\n"
"    border-radius: 10px;\n"
"    margin-top: 1ex; /* leave space at the top for the title */\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center; /* position at the top center */\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 0 50px;\n"
"    background-color: rgb(141, 141, 141);\n"
"}")
        self.groupBox_4.setObjectName("groupBox_4")
        self.frame_7 = QtWidgets.QFrame(self.groupBox_4)
        self.frame_7.setGeometry(QtCore.QRect(372, 20, 341, 211))
        self.frame_7.setStyleSheet("background-color: rgb(113, 113, 113);")
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.table_unittest = QtWidgets.QTableWidget(self.groupBox_4)
        self.table_unittest.setGeometry(QtCore.QRect(20, 30, 691, 321))
        self.table_unittest.setAutoFillBackground(True)
        self.table_unittest.setStyleSheet("QTableWidget {\n"
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
        self.table_unittest.setObjectName("table_unittest")
        self.table_unittest.setColumnCount(1)
        self.table_unittest.setRowCount(8)
        item = QtWidgets.QTableWidgetItem()
        self.table_unittest.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_unittest.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_unittest.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_unittest.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_unittest.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_unittest.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_unittest.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_unittest.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_unittest.setHorizontalHeaderItem(0, item)
        self.table_unittest.horizontalHeader().setVisible(False)
        self.table_unittest.horizontalHeader().setStretchLastSection(True)
        self.tab_unittests.addTab(self.tab_unittest, "")
        self.tab_benchmark = QtWidgets.QWidget()
        self.tab_benchmark.setObjectName("tab_benchmark")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_benchmark)
        self.groupBox_3.setGeometry(QtCore.QRect(0, 0, 731, 371))
        self.groupBox_3.setAutoFillBackground(False)
        self.groupBox_3.setStyleSheet("QGroupBox {\n"
"    background-color: rgb(113, 113, 113);\n"
"    color: rgb(255, 255, 255);\n"
"    border: 2px solid gray;\n"
"    border-radius: 10px;\n"
"    margin-top: 1ex; /* leave space at the top for the title */\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center; /* position at the top center */\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 0 50px;\n"
"    background-color: rgb(141, 141, 141);\n"
"}")
        self.groupBox_3.setObjectName("groupBox_3")
        self.frame_6 = QtWidgets.QFrame(self.groupBox_3)
        self.frame_6.setGeometry(QtCore.QRect(372, 20, 341, 211))
        self.frame_6.setStyleSheet("background-color: rgb(113, 113, 113);")
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.table_benchmark = QtWidgets.QTableWidget(self.groupBox_3)
        self.table_benchmark.setGeometry(QtCore.QRect(20, 30, 691, 321))
        self.table_benchmark.setAutoFillBackground(True)
        self.table_benchmark.setStyleSheet("QTableWidget {\n"
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
        self.table_benchmark.setObjectName("table_benchmark")
        self.table_benchmark.setColumnCount(1)
        self.table_benchmark.setRowCount(8)
        item = QtWidgets.QTableWidgetItem()
        self.table_benchmark.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_benchmark.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_benchmark.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_benchmark.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_benchmark.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_benchmark.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_benchmark.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_benchmark.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_benchmark.setHorizontalHeaderItem(0, item)
        self.table_benchmark.horizontalHeader().setVisible(False)
        self.table_benchmark.horizontalHeader().setStretchLastSection(True)
        self.tab_unittests.addTab(self.tab_benchmark, "")
        self.push_ok = QtWidgets.QPushButton(IntroDialog)
        self.push_ok.setGeometry(QtCore.QRect(250, 410, 223, 31))
        self.push_ok.setStyleSheet("QPushButton {\n"
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
        self.push_ok.setObjectName("push_ok")

        self.retranslateUi(IntroDialog)
        self.tab_unittests.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(IntroDialog)

    def retranslateUi(self, IntroDialog):
        _translate = QtCore.QCoreApplication.translate
        IntroDialog.setWindowTitle(_translate("IntroDialog", "Meson Introspection dialog"))
        self.groupBox.setTitle(_translate("IntroDialog", "Meson Project Introspection:"))
        item = self.table_projectinfo.verticalHeaderItem(0)
        item.setText(_translate("IntroDialog", "Project name"))
        item = self.table_projectinfo.verticalHeaderItem(1)
        item.setText(_translate("IntroDialog", "Version"))
        item = self.table_projectinfo.verticalHeaderItem(2)
        item.setText(_translate("IntroDialog", "Subprojects"))
        item = self.table_projectinfo.verticalHeaderItem(3)
        item.setText(_translate("IntroDialog", "Subproject dir"))
        item = self.table_projectinfo.horizontalHeaderItem(0)
        item.setText(_translate("IntroDialog", "Value"))
        self.tab_unittests.setTabText(self.tab_unittests.indexOf(self.tab_projectinfo), _translate("IntroDialog", "Meson Project Info"))
        self.groupBox_5.setTitle(_translate("IntroDialog", "Meson Targets Introspection:"))
        item = self.table_targets.verticalHeaderItem(0)
        item.setText(_translate("IntroDialog", "name"))
        item = self.table_targets.verticalHeaderItem(1)
        item.setText(_translate("IntroDialog", "type"))
        item = self.table_targets.verticalHeaderItem(2)
        item.setText(_translate("IntroDialog", "id"))
        item = self.table_targets.verticalHeaderItem(3)
        item.setText(_translate("IntroDialog", "defined_in"))
        item = self.table_targets.verticalHeaderItem(4)
        item.setText(_translate("IntroDialog", "filename"))
        item = self.table_targets.verticalHeaderItem(5)
        item.setText(_translate("IntroDialog", "build_by_default"))
        item = self.table_targets.verticalHeaderItem(6)
        item.setText(_translate("IntroDialog", "language"))
        item = self.table_targets.verticalHeaderItem(7)
        item.setText(_translate("IntroDialog", "compiler"))
        item = self.table_targets.verticalHeaderItem(8)
        item.setText(_translate("IntroDialog", "parameters"))
        item = self.table_targets.verticalHeaderItem(9)
        item.setText(_translate("IntroDialog", "sources"))
        item = self.table_targets.verticalHeaderItem(10)
        item.setText(_translate("IntroDialog", "generated_sources"))
        item = self.table_targets.verticalHeaderItem(11)
        item.setText(_translate("IntroDialog", "subproject"))
        item = self.table_targets.verticalHeaderItem(12)
        item.setText(_translate("IntroDialog", "installed"))
        item = self.table_targets.verticalHeaderItem(13)
        item.setText(_translate("IntroDialog", "install_filename"))
        item = self.table_targets.horizontalHeaderItem(0)
        item.setText(_translate("IntroDialog", "Value"))
        self.tab_unittests.setTabText(self.tab_unittests.indexOf(self.tab_target), _translate("IntroDialog", "Meson Targets"))
        self.groupBox_4.setTitle(_translate("IntroDialog", "Meson Unit Test Introspection:"))
        item = self.table_unittest.verticalHeaderItem(0)
        item.setText(_translate("IntroDialog", "command"))
        item = self.table_unittest.verticalHeaderItem(1)
        item.setText(_translate("IntroDialog", "environment"))
        item = self.table_unittest.verticalHeaderItem(2)
        item.setText(_translate("IntroDialog", "name"))
        item = self.table_unittest.verticalHeaderItem(3)
        item.setText(_translate("IntroDialog", "workdir"))
        item = self.table_unittest.verticalHeaderItem(4)
        item.setText(_translate("IntroDialog", "timeout"))
        item = self.table_unittest.verticalHeaderItem(5)
        item.setText(_translate("IntroDialog", "suite"))
        item = self.table_unittest.verticalHeaderItem(6)
        item.setText(_translate("IntroDialog", "is_parallel"))
        item = self.table_unittest.verticalHeaderItem(7)
        item.setText(_translate("IntroDialog", "priority"))
        item = self.table_unittest.horizontalHeaderItem(0)
        item.setText(_translate("IntroDialog", "Value"))
        self.tab_unittests.setTabText(self.tab_unittests.indexOf(self.tab_unittest), _translate("IntroDialog", "Meson Unit Test"))
        self.groupBox_3.setTitle(_translate("IntroDialog", "Meson Benchmark Introspection:"))
        item = self.table_benchmark.verticalHeaderItem(0)
        item.setText(_translate("IntroDialog", "command"))
        item = self.table_benchmark.verticalHeaderItem(1)
        item.setText(_translate("IntroDialog", "environment"))
        item = self.table_benchmark.verticalHeaderItem(2)
        item.setText(_translate("IntroDialog", "name"))
        item = self.table_benchmark.verticalHeaderItem(3)
        item.setText(_translate("IntroDialog", "workdir"))
        item = self.table_benchmark.verticalHeaderItem(4)
        item.setText(_translate("IntroDialog", "timeout"))
        item = self.table_benchmark.verticalHeaderItem(5)
        item.setText(_translate("IntroDialog", "suite"))
        item = self.table_benchmark.verticalHeaderItem(6)
        item.setText(_translate("IntroDialog", "is_parallel"))
        item = self.table_benchmark.verticalHeaderItem(7)
        item.setText(_translate("IntroDialog", "priority"))
        item = self.table_benchmark.horizontalHeaderItem(0)
        item.setText(_translate("IntroDialog", "Value"))
        self.tab_unittests.setTabText(self.tab_unittests.indexOf(self.tab_benchmark), _translate("IntroDialog", "Meson Benchmark"))
        self.push_ok.setText(_translate("IntroDialog", "Ok"))
from . import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    IntroDialog = QtWidgets.QDialog()
    ui = Ui_IntroDialog()
    ui.setupUi(IntroDialog)
    IntroDialog.show()
    sys.exit(app.exec_())
