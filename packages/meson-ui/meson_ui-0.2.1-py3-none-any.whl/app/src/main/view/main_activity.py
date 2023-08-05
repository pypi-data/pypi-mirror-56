#!/user/bin/env python3
###################################################################################
#                                                                                 #
# AUTHOR: Michael Brockus.                                                        #
#                                                                                 #
# CONTACT: <mailto:michaelbrockus@gmail.com>                                      #
#                                                                                 #
# LICENSE: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0                 #
#                                                                                 #
###################################################################################
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDir
from ..mesonuilib.component.console import MesonUiConsole
from ..mesonuilib.component.targetview import MesonUiTargetList
from ..mesonuilib.meson.meson import Meson
from ..model.mesonuimodel import MesonUiModule
from ..controller.mesonuicontroller import MesonUiController
from .setup_activity import SetupActivity
from .data_activity import IntroActivity
from ..mesonuilib.interface.interfaceappcompact import InterfaceAppCompact
from ..ui.activity_main import Ui_MainWindow

from os.path import join as join_paths
import os


class MainActivity(InterfaceAppCompact, Ui_MainWindow):
    def __init__(self):
        super(MainActivity, self).__init__()
        self.setupUi(self)
        self.setFixedSize(800, 600)

        self._model = MesonUiModule(context=self)
        self._controller = MesonUiController(self._model)

        # This is used to perform Meson build actions
        self.meson = Meson(self)
        self.console = MesonUiConsole(self)
        self.tableview = MesonUiTargetList(self)

        self.source_dir.setText(self.auto_fill_sourcedir())
        self.build_dir.setText(self.auto_fill_builddir())
        self._model.get_project().set_sourcedir(self.get_sourcedir())
        self._model.get_project().set_builddir(self.get_builddir())

        # Meson-ui help.
        self.actionMeson_docs.triggered.connect(lambda: self.onclick_docs())
        self.actionMeson_QnA.triggered.connect(lambda: self.onclick_faqs())
        self.actionMeson_ui_issue.triggered.connect(lambda: self.onclick_mesonui_issue())
        self.actionMeson_issue.triggered.connect(lambda: self.onclick_meson_issue())

        # Mesnu-ui main view buttons.
        self.push_install.clicked.connect(lambda: self.onclick_install())
        self.push_setup.clicked.connect(lambda: self.onclick_setup())
        self.push_build.clicked.connect(lambda: self.onclick_build())
        self.push_clear.clicked.connect(lambda: self.onclick_clear())
        self.push_clean.clicked.connect(lambda: self.onclick_clean())
        self.push_intro.clicked.connect(lambda: self.onclick_data())
        self.push_test.clicked.connect(lambda: self.onclick_tests())
        self.push_dist.clicked.connect(lambda: self.onclick_dist())
        self.push_open.clicked.connect(lambda: self.onclick_open())
        self.push_docs.clicked.connect(lambda: self.onclick_docs())
    # end of method

    @pyqtSlot()
    def onclick_setup(self) -> None:
        self._model.get_project().set_sourcedir(self.get_sourcedir())
        self._model.get_project().set_builddir(self.get_builddir())
        self.intent_setup = SetupActivity(self, model=self._model, controller=self._controller)
        self.intent_setup.show()
    # end of method

    @pyqtSlot()
    def onclick_data(self) -> None:
        self.intent_data = IntroActivity(self, model=self._model, controller=self._controller)
        self.intent_data.show()

    @pyqtSlot()
    def onclick_build(self) -> None:
        self.meson.build()
        self.tableview.update_table()
    # end of method

    @pyqtSlot()
    def onclick_dist(self) -> None:
        self.meson.dist()
    # end of method

    @pyqtSlot()
    def onclick_clean(self) -> None:
        self.meson.clean()
        self.tableview.update_table()
    # end of method

    @pyqtSlot()
    def onclick_tests(self) -> None:
        self.meson.tests()
    # end of method

    @pyqtSlot()
    def onclick_install(self) -> None:
        self.meson.install()
    # end of method

    @pyqtSlot()
    def onclick_clear(self) -> None:
        self.source_dir.setText(self.empty())
        self.build_dir.setText(self.empty())
    # end of method

    @pyqtSlot()
    def onclick_open(self) -> None:
        project_path = str(QFileDialog.getExistingDirectory(self, 'Open project directory', QDir.homePath()))
        if project_path != self.empty():
            self._model.get_project().set_sourcedir(project_path)
            self._model.get_project().set_builddir(join_paths(project_path, 'builddir'))

        self.source_dir.setText(self._model.get_project().get_sourcedir())
        self.build_dir.setText(self._model.get_project().get_builddir())
        self.tableview.update_table()
    # end of method

    @pyqtSlot()
    def onclick_docs(self):
        self.on_open_url(url_link='https://mesonbuild.com')
    # end of method

    @pyqtSlot()
    def onclick_faqs(self):
        self.on_open_url(url_link='https://mesonbuild.com/FAQ.html')
    # end of method

    @pyqtSlot()
    def onclick_mesonui_issue(self):
        self.on_open_url(url_link='https://github.com/michaelbadcrumble/meson-ui/issues')
    # end of method

    @pyqtSlot()
    def onclick_meson_issue(self):
        self.on_open_url(url_link='https://github.com/mesonbuild/meson/issues')
    # end of method

    def get_sourcedir(self) -> str:
        return self.source_dir.text()

    def get_builddir(self) -> str:
        return self.build_dir.text()

    def auto_fill_sourcedir(self) -> str:
        '''
           Auto fill the value for source directory
        '''
        return f'{os.getcwd()}'

    def auto_fill_builddir(self) -> str:
        '''
           Auto fill the value for builddir directory
        '''
        return join_paths(f'{os.getcwd()}', 'builddir')

    def process(self):
        return self.meson.process()
