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
from PyQt5.QtWidgets import QTableWidgetItem as Item


class MesonUiTargetList:
    def __init__(self, context = None):
        self._context = context
    # end of method

    def update_table(self):
        self._context.targets_view.setItem(0, 0, Item(self._context._model.get_targets().get_name()))
        self._context.targets_view.setItem(1, 0, Item(self._context._model.get_targets().get_type()))
        self._context.targets_view.setItem(2, 0, Item(self._context._model.get_targets().get_id()))
        self._context.targets_view.setItem(3, 0, Item(self._context._model.get_targets().get_defined_in()))
        self._context.targets_view.setItem(4, 0, Item(str(self._context._model.get_targets().get_filename())))
        self._context.targets_view.setItem(5, 0, Item(str(self._context._model.get_targets().get_build_by_default())))
        self._context.targets_view.setItem(6, 0, Item(str(self._context._model.get_targets_sources().get_language())))
        self._context.targets_view.setItem(7, 0, Item(str(self._context._model.get_targets_sources().get_compiler())))
        self._context.targets_view.setItem(8, 0, Item(str(self._context._model.get_targets_sources().get_parameters())))
        self._context.targets_view.setItem(9, 0, Item(str(self._context._model.get_targets_sources().get_sources())))
        self._context.targets_view.setItem(10, 0, Item(str(self._context._model.get_targets_sources().get_generated_sources())))
        self._context.targets_view.setItem(11, 0, Item(str(self._context._model.get_targets().get_subproject())))
        self._context.targets_view.setItem(12, 0, Item(str(self._context._model.get_targets().get_installed())))
        self._context.targets_view.setItem(13, 0, Item(str(self._context._model.get_targets().get_install_filename())))
