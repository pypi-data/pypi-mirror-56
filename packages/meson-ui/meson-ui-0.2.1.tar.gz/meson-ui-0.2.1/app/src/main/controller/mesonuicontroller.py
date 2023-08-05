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
from ..model.mesonuimodel import MesonUiModule


class MesonUiController:
    def __init__(self, model: MesonUiModule = None):
        super().__init__()
        self._model: MesonUiModule = model
    # end of method

    def meson_project_changed(self, project) -> None:
        self._model.get_project().set_sourcedir(value=project.get_sourcedir())
        self._model.get_project().set_builddir(value=project.get_builddir())
    # end of method
