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
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem as Item
from ..model.mesonuimodel import MesonUiModule
from ..controller.mesonuicontroller import MesonUiController
from ..ui.activity_data import Ui_IntroDialog


class IntroActivity(QMainWindow, Ui_IntroDialog):
    def __init__(self, context=None, model: MesonUiModule = None, controller: MesonUiController = None):
        super(IntroActivity, self).__init__()
        self.setupUi(self)

        self.setFixedSize(730, 464)

        self._model = model
        self._controller = controller
        self.on_create()
        self.push_ok.clicked.connect(lambda: self.onclick_ok())

    def on_create(self):
        self.table_projectinfo_setup()
        self.table_targets_setup()
        self.table_unittest_setup()
        self.table_benchmark_setup()
    # end of method

    def table_projectinfo_setup(self):
        self.table_projectinfo.setItem(0, 0, Item(self._model.get_projectinfo().get_name()))
        self.table_projectinfo.setItem(1, 0, Item(self._model.get_projectinfo().get_version()))
        self.table_projectinfo.setItem(2, 0, Item(str(self._model.get_projectinfo().get_subprojects())))
        self.table_projectinfo.setItem(3, 0, Item(self._model.get_projectinfo().get_subproject_dir()))
    # end of method

    def table_targets_setup(self):
        self.table_targets.setItem(0, 0, Item(self._model.get_targets().get_name()))
        self.table_targets.setItem(1, 0, Item(self._model.get_targets().get_type()))
        self.table_targets.setItem(2, 0, Item(self._model.get_targets().get_id()))
        self.table_targets.setItem(3, 0, Item(self._model.get_targets().get_defined_in()))
        self.table_targets.setItem(4, 0, Item(str(self._model.get_targets().get_filename())))
        self.table_targets.setItem(5, 0, Item(str(self._model.get_targets().get_build_by_default())))
        self.table_targets.setItem(6, 0, Item(str(self._model.get_targets_sources().get_language())))
        self.table_targets.setItem(7, 0, Item(str(self._model.get_targets_sources().get_compiler())))
        self.table_targets.setItem(8, 0, Item(str(self._model.get_targets_sources().get_parameters())))
        self.table_targets.setItem(9, 0, Item(str(self._model.get_targets_sources().get_sources())))
        self.table_targets.setItem(10, 0, Item(str(self._model.get_targets_sources().get_generated_sources())))
        self.table_targets.setItem(11, 0, Item(str(self._model.get_targets().get_subproject())))
        self.table_targets.setItem(12, 0, Item(str(self._model.get_targets().get_installed())))
        self.table_targets.setItem(13, 0, Item(str(self._model.get_targets().get_install_filename())))
    # end of method

    def table_unittest_setup(self):
        self.table_unittest.setItem(0, 0, Item(str(self._model.get_tests().get_command(0))))
        self.table_unittest.setItem(1, 0, Item(str(self._model.get_tests().get_environment(0))))
        self.table_unittest.setItem(2, 0, Item(str(self._model.get_tests().get_name(0))))
        self.table_unittest.setItem(3, 0, Item(str(self._model.get_tests().get_workdir(0))))
        self.table_unittest.setItem(4, 0, Item(str(self._model.get_tests().get_timeout(0))))
        self.table_unittest.setItem(5, 0, Item(str(self._model.get_tests().get_suite(0))))
        self.table_unittest.setItem(5, 0, Item(str(self._model.get_tests().get_is_parallel(0))))
        self.table_unittest.setItem(5, 0, Item(str(self._model.get_tests().get_priority(0))))
    # end of method

    def table_benchmark_setup(self):
        self.table_benchmark.setItem(0, 0, Item(str(self._model.get_benchmark().get_command(0))))
        self.table_benchmark.setItem(1, 0, Item(str(self._model.get_benchmark().get_environment(0))))
        self.table_benchmark.setItem(2, 0, Item(str(self._model.get_benchmark().get_name(0))))
        self.table_benchmark.setItem(3, 0, Item(str(self._model.get_benchmark().get_workdir(0))))
        self.table_benchmark.setItem(4, 0, Item(str(self._model.get_benchmark().get_timeout(0))))
        self.table_benchmark.setItem(5, 0, Item(str(self._model.get_benchmark().get_suite(0))))
        self.table_benchmark.setItem(5, 0, Item(str(self._model.get_benchmark().get_is_parallel(0))))
        self.table_benchmark.setItem(5, 0, Item(str(self._model.get_benchmark().get_priority(0))))
    # end of method

    def onclick_ok(self):
        self.close()
