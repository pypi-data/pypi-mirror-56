# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app/src/res/layout/activity_setup.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SetupDialog(object):
    def setupUi(self, SetupDialog):
        SetupDialog.setObjectName("SetupDialog")
        SetupDialog.resize(730, 464)
        SetupDialog.setStyleSheet("background-color: rgb(41, 41, 49);")
        self.layoutWidget = QtWidgets.QWidget(SetupDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(128, 10, 591, 66))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_curr_source = QtWidgets.QLabel(self.layoutWidget)
        self.label_curr_source.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_curr_source.setObjectName("label_curr_source")
        self.horizontalLayout_3.addWidget(self.label_curr_source)
        self.curr_source_dir = QtWidgets.QLineEdit(self.layoutWidget)
        self.curr_source_dir.setStyleSheet("QLineEdit {\n"
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
        self.curr_source_dir.setObjectName("curr_source_dir")
        self.horizontalLayout_3.addWidget(self.curr_source_dir)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lable_curr_build = QtWidgets.QLabel(self.layoutWidget)
        self.lable_curr_build.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.lable_curr_build.setObjectName("lable_curr_build")
        self.horizontalLayout.addWidget(self.lable_curr_build)
        self.curr_build_dir = QtWidgets.QLineEdit(self.layoutWidget)
        self.curr_build_dir.setStyleSheet("QLineEdit {\n"
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
        self.curr_build_dir.setObjectName("curr_build_dir")
        self.horizontalLayout.addWidget(self.curr_build_dir)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.label_logo = QtWidgets.QLabel(SetupDialog)
        self.label_logo.setGeometry(QtCore.QRect(30, 10, 61, 61))
        self.label_logo.setStyleSheet("QLineEdit {\n"
"    url(:/icons/icons/ic_app.png)\n"
"}")
        self.label_logo.setText("")
        self.label_logo.setPixmap(QtGui.QPixmap(":/ic_res/icons/ic_app.png"))
        self.label_logo.setScaledContents(True)
        self.label_logo.setObjectName("label_logo")
        self.layoutWidget1 = QtWidgets.QWidget(SetupDialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(130, 402, 471, 39))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(34)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.push_not_yet = QtWidgets.QPushButton(self.layoutWidget1)
        self.push_not_yet.setStyleSheet("QPushButton {\n"
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
        self.push_not_yet.setObjectName("push_not_yet")
        self.horizontalLayout_2.addWidget(self.push_not_yet)
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
        self.horizontalLayout_2.addWidget(self.push_setup)
        self.tabWidget = QtWidgets.QTabWidget(SetupDialog)
        self.tabWidget.setGeometry(QtCore.QRect(1, 89, 731, 301))
        self.tabWidget.setStyleSheet("QTabWidget::pane { /* The tab widget frame */\n"
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
        self.tabWidget.setObjectName("tabWidget")
        self.tab_core_opt = QtWidgets.QWidget()
        self.tab_core_opt.setObjectName("tab_core_opt")
        self.groupBox = QtWidgets.QGroupBox(self.tab_core_opt)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 731, 271))
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
        self.frame_5 = QtWidgets.QFrame(self.groupBox)
        self.frame_5.setGeometry(QtCore.QRect(10, 20, 341, 211))
        self.frame_5.setStyleSheet("background-color: rgb(113, 113, 113);")
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(7)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_auto_features = QtWidgets.QLabel(self.frame_5)
        self.label_auto_features.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_auto_features.setObjectName("label_auto_features")
        self.horizontalLayout_10.addWidget(self.label_auto_features)
        self.combo_box_auto_feature = QtWidgets.QComboBox(self.frame_5)
        self.combo_box_auto_feature.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 255, 255);\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_auto_feature.setObjectName("combo_box_auto_feature")
        self.combo_box_auto_feature.addItem("")
        self.combo_box_auto_feature.addItem("")
        self.combo_box_auto_feature.addItem("")
        self.horizontalLayout_10.addWidget(self.combo_box_auto_feature)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(41)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_backend = QtWidgets.QLabel(self.frame_5)
        self.label_backend.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_backend.setObjectName("label_backend")
        self.horizontalLayout_7.addWidget(self.label_backend)
        self.combo_box_backend = QtWidgets.QComboBox(self.frame_5)
        self.combo_box_backend.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 255, 255);\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_backend.setObjectName("combo_box_backend")
        self.combo_box_backend.addItem("")
        self.combo_box_backend.addItem("")
        self.combo_box_backend.addItem("")
        self.combo_box_backend.addItem("")
        self.combo_box_backend.addItem("")
        self.combo_box_backend.addItem("")
        self.horizontalLayout_7.addWidget(self.combo_box_backend)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(36)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_10 = QtWidgets.QLabel(self.frame_5)
        self.label_10.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_8.addWidget(self.label_10)
        self.combo_box_buildtype = QtWidgets.QComboBox(self.frame_5)
        self.combo_box_buildtype.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 255, 255);\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_buildtype.setObjectName("combo_box_buildtype")
        self.combo_box_buildtype.addItem("")
        self.combo_box_buildtype.addItem("")
        self.combo_box_buildtype.addItem("")
        self.combo_box_buildtype.addItem("")
        self.combo_box_buildtype.addItem("")
        self.combo_box_buildtype.addItem("")
        self.horizontalLayout_8.addWidget(self.combo_box_buildtype)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setSpacing(3)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_8 = QtWidgets.QLabel(self.frame_5)
        self.label_8.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_12.addWidget(self.label_8)
        self.combo_box_default_library = QtWidgets.QComboBox(self.frame_5)
        self.combo_box_default_library.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 255, 255);\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_default_library.setObjectName("combo_box_default_library")
        self.combo_box_default_library.addItem("")
        self.combo_box_default_library.addItem("")
        self.combo_box_default_library.addItem("")
        self.horizontalLayout_12.addWidget(self.combo_box_default_library)
        self.verticalLayout.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setSpacing(16)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_28 = QtWidgets.QLabel(self.frame_5)
        self.label_28.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_11.addWidget(self.label_28)
        self.combo_box_wrap_mode = QtWidgets.QComboBox(self.frame_5)
        self.combo_box_wrap_mode.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 255, 255);\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_wrap_mode.setObjectName("combo_box_wrap_mode")
        self.combo_box_wrap_mode.addItem("")
        self.combo_box_wrap_mode.addItem("")
        self.combo_box_wrap_mode.addItem("")
        self.combo_box_wrap_mode.addItem("")
        self.horizontalLayout_11.addWidget(self.combo_box_wrap_mode)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setSpacing(57)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_29 = QtWidgets.QLabel(self.frame_5)
        self.label_29.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_29.setObjectName("label_29")
        self.horizontalLayout_17.addWidget(self.label_29)
        self.combo_box_unity = QtWidgets.QComboBox(self.frame_5)
        self.combo_box_unity.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 255, 255);\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_unity.setObjectName("combo_box_unity")
        self.combo_box_unity.addItem("")
        self.combo_box_unity.addItem("")
        self.combo_box_unity.addItem("")
        self.horizontalLayout_17.addWidget(self.combo_box_unity)
        self.verticalLayout.addLayout(self.horizontalLayout_17)
        self.frame_4 = QtWidgets.QFrame(self.groupBox)
        self.frame_4.setGeometry(QtCore.QRect(372, 20, 341, 211))
        self.frame_4.setStyleSheet("background-color: rgb(113, 113, 113);")
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setSpacing(54)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_layout_3 = QtWidgets.QLabel(self.frame_4)
        self.label_layout_3.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_layout_3.setObjectName("label_layout_3")
        self.horizontalLayout_13.addWidget(self.label_layout_3)
        self.combo_box_layout = QtWidgets.QComboBox(self.frame_4)
        self.combo_box_layout.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 255, 255);\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_layout.setObjectName("combo_box_layout")
        self.combo_box_layout.addItem("")
        self.combo_box_layout.addItem("")
        self.horizontalLayout_13.addWidget(self.combo_box_layout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setSpacing(8)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_11 = QtWidgets.QLabel(self.frame_4)
        self.label_11.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_14.addWidget(self.label_11)
        self.combo_box_warning = QtWidgets.QComboBox(self.frame_4)
        self.combo_box_warning.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 255, 255);\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_warning.setObjectName("combo_box_warning")
        self.combo_box_warning.addItem("")
        self.combo_box_warning.addItem("")
        self.combo_box_warning.addItem("")
        self.combo_box_warning.addItem("")
        self.horizontalLayout_14.addWidget(self.combo_box_warning)
        self.verticalLayout_3.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(16)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label = QtWidgets.QLabel(self.frame_4)
        self.label.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label.setObjectName("label")
        self.horizontalLayout_9.addWidget(self.label)
        self.combo_box_optimization = QtWidgets.QComboBox(self.frame_4)
        self.combo_box_optimization.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 255, 255);\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_optimization.setObjectName("combo_box_optimization")
        self.combo_box_optimization.addItem("")
        self.combo_box_optimization.addItem("")
        self.combo_box_optimization.addItem("")
        self.combo_box_optimization.addItem("")
        self.combo_box_optimization.addItem("")
        self.combo_box_optimization.addItem("")
        self.horizontalLayout_9.addWidget(self.combo_box_optimization)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setSpacing(47)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_13 = QtWidgets.QLabel(self.frame_4)
        self.label_13.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_16.addWidget(self.label_13)
        self.combo_box_werror = QtWidgets.QComboBox(self.frame_4)
        self.combo_box_werror.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 255, 255);\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_werror.setObjectName("combo_box_werror")
        self.combo_box_werror.addItem("")
        self.combo_box_werror.addItem("")
        self.horizontalLayout_16.addWidget(self.combo_box_werror)
        self.verticalLayout_3.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setSpacing(54)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_12 = QtWidgets.QLabel(self.frame_4)
        self.label_12.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_15.addWidget(self.label_12)
        self.combo_box_debug = QtWidgets.QComboBox(self.frame_4)
        self.combo_box_debug.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 255, 255);\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_debug.setObjectName("combo_box_debug")
        self.combo_box_debug.addItem("")
        self.combo_box_debug.addItem("")
        self.horizontalLayout_15.addWidget(self.combo_box_debug)
        self.verticalLayout_3.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setSpacing(63)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_20 = QtWidgets.QLabel(self.frame_4)
        self.label_20.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_18.addWidget(self.label_20)
        self.combo_box_strip = QtWidgets.QComboBox(self.frame_4)
        self.combo_box_strip.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 255, 255);\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_strip.setObjectName("combo_box_strip")
        self.combo_box_strip.addItem("")
        self.combo_box_strip.addItem("")
        self.horizontalLayout_18.addWidget(self.combo_box_strip)
        self.verticalLayout_3.addLayout(self.horizontalLayout_18)
        self.tabWidget.addTab(self.tab_core_opt, "")
        self.tab_base_opt = QtWidgets.QWidget()
        self.tab_base_opt.setObjectName("tab_base_opt")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_base_opt)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 0, 731, 271))
        self.groupBox_2.setAutoFillBackground(False)
        self.groupBox_2.setStyleSheet("QGroupBox {\n"
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
        self.groupBox_2.setObjectName("groupBox_2")
        self.frame_10 = QtWidgets.QFrame(self.groupBox_2)
        self.frame_10.setGeometry(QtCore.QRect(372, 20, 341, 211))
        self.frame_10.setStyleSheet("background-color: rgb(113, 113, 113);")
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.label_lto = QtWidgets.QLabel(self.frame_10)
        self.label_lto.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_lto.setObjectName("label_lto")
        self.horizontalLayout_26.addWidget(self.label_lto)
        self.combo_box_b_lto = QtWidgets.QComboBox(self.frame_10)
        self.combo_box_b_lto.setStyleSheet("QComboBox {\n"
"    background-color: white;\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_b_lto.setObjectName("combo_box_b_lto")
        self.combo_box_b_lto.addItem("")
        self.combo_box_b_lto.addItem("")
        self.horizontalLayout_26.addWidget(self.combo_box_b_lto)
        self.verticalLayout_7.addLayout(self.horizontalLayout_26)
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.label_ndebug = QtWidgets.QLabel(self.frame_10)
        self.label_ndebug.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_ndebug.setObjectName("label_ndebug")
        self.horizontalLayout_27.addWidget(self.label_ndebug)
        self.combo_box_b_ndebug = QtWidgets.QComboBox(self.frame_10)
        self.combo_box_b_ndebug.setStyleSheet("QComboBox {\n"
"    background-color: white;\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_b_ndebug.setObjectName("combo_box_b_ndebug")
        self.combo_box_b_ndebug.addItem("")
        self.combo_box_b_ndebug.addItem("")
        self.combo_box_b_ndebug.addItem("")
        self.horizontalLayout_27.addWidget(self.combo_box_b_ndebug)
        self.verticalLayout_7.addLayout(self.horizontalLayout_27)
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.label_pch = QtWidgets.QLabel(self.frame_10)
        self.label_pch.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_pch.setObjectName("label_pch")
        self.horizontalLayout_28.addWidget(self.label_pch)
        self.combo_box_b_pch = QtWidgets.QComboBox(self.frame_10)
        self.combo_box_b_pch.setStyleSheet("QComboBox {\n"
"    background-color: white;\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_b_pch.setObjectName("combo_box_b_pch")
        self.combo_box_b_pch.addItem("")
        self.combo_box_b_pch.addItem("")
        self.horizontalLayout_28.addWidget(self.combo_box_b_pch)
        self.verticalLayout_7.addLayout(self.horizontalLayout_28)
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.label_pgo = QtWidgets.QLabel(self.frame_10)
        self.label_pgo.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_pgo.setObjectName("label_pgo")
        self.horizontalLayout_29.addWidget(self.label_pgo)
        self.combo_box_b_pgo = QtWidgets.QComboBox(self.frame_10)
        self.combo_box_b_pgo.setStyleSheet("QComboBox {\n"
"    background-color: white;\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_b_pgo.setObjectName("combo_box_b_pgo")
        self.combo_box_b_pgo.addItem("")
        self.combo_box_b_pgo.addItem("")
        self.combo_box_b_pgo.addItem("")
        self.horizontalLayout_29.addWidget(self.combo_box_b_pgo)
        self.verticalLayout_7.addLayout(self.horizontalLayout_29)
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.label_sanitize = QtWidgets.QLabel(self.frame_10)
        self.label_sanitize.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_sanitize.setObjectName("label_sanitize")
        self.horizontalLayout_30.addWidget(self.label_sanitize)
        self.combo_box_b_sanitize = QtWidgets.QComboBox(self.frame_10)
        self.combo_box_b_sanitize.setStyleSheet("QComboBox {\n"
"    background-color: white;\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_b_sanitize.setObjectName("combo_box_b_sanitize")
        self.combo_box_b_sanitize.addItem("")
        self.combo_box_b_sanitize.addItem("")
        self.combo_box_b_sanitize.addItem("")
        self.combo_box_b_sanitize.addItem("")
        self.combo_box_b_sanitize.addItem("")
        self.combo_box_b_sanitize.addItem("")
        self.horizontalLayout_30.addWidget(self.combo_box_b_sanitize)
        self.verticalLayout_7.addLayout(self.horizontalLayout_30)
        self.horizontalLayout_32 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.label_pie = QtWidgets.QLabel(self.frame_10)
        self.label_pie.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_pie.setObjectName("label_pie")
        self.horizontalLayout_32.addWidget(self.label_pie)
        self.combo_box_b_pie = QtWidgets.QComboBox(self.frame_10)
        self.combo_box_b_pie.setStyleSheet("QComboBox {\n"
"    background-color: white;\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_b_pie.setObjectName("combo_box_b_pie")
        self.combo_box_b_pie.addItem("")
        self.combo_box_b_pie.addItem("")
        self.horizontalLayout_32.addWidget(self.combo_box_b_pie)
        self.verticalLayout_7.addLayout(self.horizontalLayout_32)
        self.frame_9 = QtWidgets.QFrame(self.groupBox_2)
        self.frame_9.setGeometry(QtCore.QRect(10, 20, 341, 211))
        self.frame_9.setStyleSheet("background-color: rgb(113, 113, 113);")
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_asneeded = QtWidgets.QLabel(self.frame_9)
        self.label_asneeded.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_asneeded.setObjectName("label_asneeded")
        self.horizontalLayout_21.addWidget(self.label_asneeded)
        self.combo_box_b_asneeded = QtWidgets.QComboBox(self.frame_9)
        self.combo_box_b_asneeded.setStyleSheet("QComboBox {\n"
"    background-color: white;\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_b_asneeded.setObjectName("combo_box_b_asneeded")
        self.combo_box_b_asneeded.addItem("")
        self.combo_box_b_asneeded.addItem("")
        self.horizontalLayout_21.addWidget(self.combo_box_b_asneeded)
        self.verticalLayout_2.addLayout(self.horizontalLayout_21)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.label_staticpic = QtWidgets.QLabel(self.frame_9)
        self.label_staticpic.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_staticpic.setObjectName("label_staticpic")
        self.horizontalLayout_22.addWidget(self.label_staticpic)
        self.combo_box_b_staticpic = QtWidgets.QComboBox(self.frame_9)
        self.combo_box_b_staticpic.setStyleSheet("QComboBox {\n"
"    background-color: white;\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_b_staticpic.setObjectName("combo_box_b_staticpic")
        self.combo_box_b_staticpic.addItem("")
        self.combo_box_b_staticpic.addItem("")
        self.horizontalLayout_22.addWidget(self.combo_box_b_staticpic)
        self.verticalLayout_2.addLayout(self.horizontalLayout_22)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.label_colorout = QtWidgets.QLabel(self.frame_9)
        self.label_colorout.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_colorout.setObjectName("label_colorout")
        self.horizontalLayout_23.addWidget(self.label_colorout)
        self.combo_box_b_colorout = QtWidgets.QComboBox(self.frame_9)
        self.combo_box_b_colorout.setStyleSheet("QComboBox {\n"
"    background-color: white;\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_b_colorout.setObjectName("combo_box_b_colorout")
        self.combo_box_b_colorout.addItem("")
        self.combo_box_b_colorout.addItem("")
        self.combo_box_b_colorout.addItem("")
        self.horizontalLayout_23.addWidget(self.combo_box_b_colorout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_23)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.label_coverage = QtWidgets.QLabel(self.frame_9)
        self.label_coverage.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_coverage.setObjectName("label_coverage")
        self.horizontalLayout_24.addWidget(self.label_coverage)
        self.combo_box_b_coverage = QtWidgets.QComboBox(self.frame_9)
        self.combo_box_b_coverage.setStyleSheet("QComboBox {\n"
"    background-color: white;\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_b_coverage.setObjectName("combo_box_b_coverage")
        self.combo_box_b_coverage.addItem("")
        self.combo_box_b_coverage.addItem("")
        self.horizontalLayout_24.addWidget(self.combo_box_b_coverage)
        self.verticalLayout_2.addLayout(self.horizontalLayout_24)
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.label_lundef = QtWidgets.QLabel(self.frame_9)
        self.label_lundef.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_lundef.setObjectName("label_lundef")
        self.horizontalLayout_25.addWidget(self.label_lundef)
        self.combo_box_b_lundef = QtWidgets.QComboBox(self.frame_9)
        self.combo_box_b_lundef.setStyleSheet("QComboBox {\n"
"    background-color: white;\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_b_lundef.setObjectName("combo_box_b_lundef")
        self.combo_box_b_lundef.addItem("")
        self.combo_box_b_lundef.addItem("")
        self.horizontalLayout_25.addWidget(self.combo_box_b_lundef)
        self.verticalLayout_2.addLayout(self.horizontalLayout_25)
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.label_bitcode = QtWidgets.QLabel(self.frame_9)
        self.label_bitcode.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_bitcode.setObjectName("label_bitcode")
        self.horizontalLayout_31.addWidget(self.label_bitcode)
        self.combo_box_b_bitcode = QtWidgets.QComboBox(self.frame_9)
        self.combo_box_b_bitcode.setStyleSheet("QComboBox {\n"
"    background-color: white;\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_b_bitcode.setObjectName("combo_box_b_bitcode")
        self.combo_box_b_bitcode.addItem("")
        self.combo_box_b_bitcode.addItem("")
        self.horizontalLayout_31.addWidget(self.combo_box_b_bitcode)
        self.verticalLayout_2.addLayout(self.horizontalLayout_31)
        self.tabWidget.addTab(self.tab_base_opt, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_4.setGeometry(QtCore.QRect(0, 0, 731, 271))
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
        self.frame_13 = QtWidgets.QFrame(self.groupBox_4)
        self.frame_13.setGeometry(QtCore.QRect(10, 20, 341, 81))
        self.frame_13.setStyleSheet("background-color: rgb(113, 113, 113);")
        self.frame_13.setObjectName("frame_13")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_13)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_43 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_43.setObjectName("horizontalLayout_43")
        self.label_stdsplit = QtWidgets.QLabel(self.frame_13)
        self.label_stdsplit.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_stdsplit.setObjectName("label_stdsplit")
        self.horizontalLayout_43.addWidget(self.label_stdsplit)
        self.combo_box_stdsplit = QtWidgets.QComboBox(self.frame_13)
        self.combo_box_stdsplit.setStyleSheet("QComboBox {\n"
"    background-color: white;\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_stdsplit.setObjectName("combo_box_stdsplit")
        self.combo_box_stdsplit.addItem("")
        self.combo_box_stdsplit.addItem("")
        self.horizontalLayout_43.addWidget(self.combo_box_stdsplit)
        self.verticalLayout_6.addLayout(self.horizontalLayout_43)
        self.horizontalLayout_44 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_44.setObjectName("horizontalLayout_44")
        self.label_errorlogs = QtWidgets.QLabel(self.frame_13)
        self.label_errorlogs.setStyleSheet("background-color: rgb(113, 113, 113);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"Gill Sans\"")
        self.label_errorlogs.setObjectName("label_errorlogs")
        self.horizontalLayout_44.addWidget(self.label_errorlogs)
        self.combo_box_errorlogs = QtWidgets.QComboBox(self.frame_13)
        self.combo_box_errorlogs.setStyleSheet("QComboBox {\n"
"    background-color: white;\n"
"    selection-color: rgb(34, 255, 12);\n"
"    color: rgb(28, 170, 2);\n"
"    border-width: 5px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid gray;\n"
"    padding: 1px 10px 1px 50px;\n"
"    min-width: 10em;\n"
"    font: 13pt \"Gill Sans\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"/* shift the arrow when popup is open */\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    url(:/ic_res/icons/down_arrow.png)\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.combo_box_errorlogs.setObjectName("combo_box_errorlogs")
        self.combo_box_errorlogs.addItem("")
        self.combo_box_errorlogs.addItem("")
        self.horizontalLayout_44.addWidget(self.combo_box_errorlogs)
        self.verticalLayout_6.addLayout(self.horizontalLayout_44)
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(SetupDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SetupDialog)

    def retranslateUi(self, SetupDialog):
        _translate = QtCore.QCoreApplication.translate
        SetupDialog.setWindowTitle(_translate("SetupDialog", "Setup dialog"))
        self.label_curr_source.setText(_translate("SetupDialog", "Source directory:"))
        self.lable_curr_build.setText(_translate("SetupDialog", "Builddir directory:"))
        self.push_not_yet.setText(_translate("SetupDialog", "Not yet"))
        self.push_setup.setText(_translate("SetupDialog", "Setup project"))
        self.groupBox.setTitle(_translate("SetupDialog", "Meson core options:"))
        self.label_auto_features.setText(_translate("SetupDialog", "auto_features:"))
        self.combo_box_auto_feature.setItemText(0, _translate("SetupDialog", "auto"))
        self.combo_box_auto_feature.setItemText(1, _translate("SetupDialog", "enabled"))
        self.combo_box_auto_feature.setItemText(2, _translate("SetupDialog", "disabled"))
        self.label_backend.setText(_translate("SetupDialog", "backend:"))
        self.combo_box_backend.setItemText(0, _translate("SetupDialog", "Ninja build"))
        self.combo_box_backend.setItemText(1, _translate("SetupDialog", "Xcode"))
        self.combo_box_backend.setItemText(2, _translate("SetupDialog", "Visual Studio 2010"))
        self.combo_box_backend.setItemText(3, _translate("SetupDialog", "Visual Studio 2015"))
        self.combo_box_backend.setItemText(4, _translate("SetupDialog", "Visual Studio 2017"))
        self.combo_box_backend.setItemText(5, _translate("SetupDialog", "Visual Studio 2019"))
        self.label_10.setText(_translate("SetupDialog", "buildtype:"))
        self.combo_box_buildtype.setItemText(0, _translate("SetupDialog", "debug"))
        self.combo_box_buildtype.setItemText(1, _translate("SetupDialog", "debugoptimized"))
        self.combo_box_buildtype.setItemText(2, _translate("SetupDialog", "release"))
        self.combo_box_buildtype.setItemText(3, _translate("SetupDialog", "plain"))
        self.combo_box_buildtype.setItemText(4, _translate("SetupDialog", "minsize"))
        self.combo_box_buildtype.setItemText(5, _translate("SetupDialog", "custom"))
        self.label_8.setText(_translate("SetupDialog", "default_library:"))
        self.combo_box_default_library.setItemText(0, _translate("SetupDialog", "shared"))
        self.combo_box_default_library.setItemText(1, _translate("SetupDialog", "static"))
        self.combo_box_default_library.setItemText(2, _translate("SetupDialog", "both"))
        self.label_28.setText(_translate("SetupDialog", "wrap_mode:"))
        self.combo_box_wrap_mode.setItemText(0, _translate("SetupDialog", "default"))
        self.combo_box_wrap_mode.setItemText(1, _translate("SetupDialog", "nofallback"))
        self.combo_box_wrap_mode.setItemText(2, _translate("SetupDialog", "nodownload"))
        self.combo_box_wrap_mode.setItemText(3, _translate("SetupDialog", "forcefallback"))
        self.label_29.setText(_translate("SetupDialog", "unity:"))
        self.combo_box_unity.setItemText(0, _translate("SetupDialog", "off"))
        self.combo_box_unity.setItemText(1, _translate("SetupDialog", "on"))
        self.combo_box_unity.setItemText(2, _translate("SetupDialog", "subprojects"))
        self.label_layout_3.setText(_translate("SetupDialog", "layout:"))
        self.combo_box_layout.setItemText(0, _translate("SetupDialog", "mirror"))
        self.combo_box_layout.setItemText(1, _translate("SetupDialog", "flat"))
        self.label_11.setText(_translate("SetupDialog", "warning_level:"))
        self.combo_box_warning.setItemText(0, _translate("SetupDialog", "0"))
        self.combo_box_warning.setItemText(1, _translate("SetupDialog", "1"))
        self.combo_box_warning.setItemText(2, _translate("SetupDialog", "2"))
        self.combo_box_warning.setItemText(3, _translate("SetupDialog", "3"))
        self.label.setText(_translate("SetupDialog", "optimization:"))
        self.combo_box_optimization.setItemText(0, _translate("SetupDialog", "0"))
        self.combo_box_optimization.setItemText(1, _translate("SetupDialog", "g"))
        self.combo_box_optimization.setItemText(2, _translate("SetupDialog", "1"))
        self.combo_box_optimization.setItemText(3, _translate("SetupDialog", "2"))
        self.combo_box_optimization.setItemText(4, _translate("SetupDialog", "3"))
        self.combo_box_optimization.setItemText(5, _translate("SetupDialog", "s"))
        self.label_13.setText(_translate("SetupDialog", "werror:"))
        self.combo_box_werror.setItemText(0, _translate("SetupDialog", "false"))
        self.combo_box_werror.setItemText(1, _translate("SetupDialog", "true"))
        self.label_12.setText(_translate("SetupDialog", "debug:"))
        self.combo_box_debug.setItemText(0, _translate("SetupDialog", "true"))
        self.combo_box_debug.setItemText(1, _translate("SetupDialog", "false"))
        self.label_20.setText(_translate("SetupDialog", "strip:"))
        self.combo_box_strip.setItemText(0, _translate("SetupDialog", "false"))
        self.combo_box_strip.setItemText(1, _translate("SetupDialog", "true"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_core_opt), _translate("SetupDialog", "Core options"))
        self.groupBox_2.setTitle(_translate("SetupDialog", "Meson base options:"))
        self.label_lto.setText(_translate("SetupDialog", "b_lto:"))
        self.combo_box_b_lto.setItemText(0, _translate("SetupDialog", "false"))
        self.combo_box_b_lto.setItemText(1, _translate("SetupDialog", "true"))
        self.label_ndebug.setText(_translate("SetupDialog", "b_ndebug:"))
        self.combo_box_b_ndebug.setItemText(0, _translate("SetupDialog", "false"))
        self.combo_box_b_ndebug.setItemText(1, _translate("SetupDialog", "true"))
        self.combo_box_b_ndebug.setItemText(2, _translate("SetupDialog", "if-release"))
        self.label_pch.setText(_translate("SetupDialog", "b_pch:"))
        self.combo_box_b_pch.setItemText(0, _translate("SetupDialog", "true"))
        self.combo_box_b_pch.setItemText(1, _translate("SetupDialog", "false"))
        self.label_pgo.setText(_translate("SetupDialog", "b_pgo:"))
        self.combo_box_b_pgo.setItemText(0, _translate("SetupDialog", "off"))
        self.combo_box_b_pgo.setItemText(1, _translate("SetupDialog", "generate"))
        self.combo_box_b_pgo.setItemText(2, _translate("SetupDialog", "use"))
        self.label_sanitize.setText(_translate("SetupDialog", "b_sanitize:"))
        self.combo_box_b_sanitize.setItemText(0, _translate("SetupDialog", "none"))
        self.combo_box_b_sanitize.setItemText(1, _translate("SetupDialog", "address"))
        self.combo_box_b_sanitize.setItemText(2, _translate("SetupDialog", "thread"))
        self.combo_box_b_sanitize.setItemText(3, _translate("SetupDialog", "undefined"))
        self.combo_box_b_sanitize.setItemText(4, _translate("SetupDialog", "memory"))
        self.combo_box_b_sanitize.setItemText(5, _translate("SetupDialog", "address,undefined"))
        self.label_pie.setText(_translate("SetupDialog", "b_pie:"))
        self.combo_box_b_pie.setItemText(0, _translate("SetupDialog", "false"))
        self.combo_box_b_pie.setItemText(1, _translate("SetupDialog", "true"))
        self.label_asneeded.setText(_translate("SetupDialog", "b_asneeded:"))
        self.combo_box_b_asneeded.setItemText(0, _translate("SetupDialog", "true"))
        self.combo_box_b_asneeded.setItemText(1, _translate("SetupDialog", "false"))
        self.label_staticpic.setText(_translate("SetupDialog", "b_staticpic:"))
        self.combo_box_b_staticpic.setItemText(0, _translate("SetupDialog", "true"))
        self.combo_box_b_staticpic.setItemText(1, _translate("SetupDialog", "false"))
        self.label_colorout.setText(_translate("SetupDialog", "b_colorout:"))
        self.combo_box_b_colorout.setItemText(0, _translate("SetupDialog", "always"))
        self.combo_box_b_colorout.setItemText(1, _translate("SetupDialog", "auto"))
        self.combo_box_b_colorout.setItemText(2, _translate("SetupDialog", "never"))
        self.label_coverage.setText(_translate("SetupDialog", "b_coverage:"))
        self.combo_box_b_coverage.setItemText(0, _translate("SetupDialog", "false"))
        self.combo_box_b_coverage.setItemText(1, _translate("SetupDialog", "true"))
        self.label_lundef.setText(_translate("SetupDialog", "b_lundef:"))
        self.combo_box_b_lundef.setItemText(0, _translate("SetupDialog", "true"))
        self.combo_box_b_lundef.setItemText(1, _translate("SetupDialog", "false"))
        self.label_bitcode.setText(_translate("SetupDialog", "b_bitcode:"))
        self.combo_box_b_bitcode.setItemText(0, _translate("SetupDialog", "false"))
        self.combo_box_b_bitcode.setItemText(1, _translate("SetupDialog", "true"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_base_opt), _translate("SetupDialog", "Base options"))
        self.groupBox_4.setTitle(_translate("SetupDialog", "Meson test options:"))
        self.label_stdsplit.setText(_translate("SetupDialog", "stdsplit:"))
        self.combo_box_stdsplit.setItemText(0, _translate("SetupDialog", "true"))
        self.combo_box_stdsplit.setItemText(1, _translate("SetupDialog", "false"))
        self.label_errorlogs.setText(_translate("SetupDialog", "errorlogs:"))
        self.combo_box_errorlogs.setItemText(0, _translate("SetupDialog", "true"))
        self.combo_box_errorlogs.setItemText(1, _translate("SetupDialog", "false"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("SetupDialog", "Test options"))
from . import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SetupDialog = QtWidgets.QDialog()
    ui = Ui_SetupDialog()
    ui.setupUi(SetupDialog)
    SetupDialog.show()
    sys.exit(app.exec_())
