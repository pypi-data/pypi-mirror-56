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
from ..repo.mesoninfo import MesonInfo


class IntroTargetModel:
    '''
        This is a data class for Meson target info
    '''

    def __init__(self, meson_info: MesonInfo = None):
        self._meson_info: MesonInfo = meson_info

    def item_iter(self):
        return self._meson_info.iter_targets()

    def get_name(self, index: int = 0) -> str:
        return self._meson_info.get_targets(index, value='name')

    def get_id(self, index: int = 0) -> str:
        return self._meson_info.get_targets(index, value='id')

    def get_type(self, index: int = 0) -> str:
        return self._meson_info.get_targets(index, value='type')

    def get_defined_in(self, index: int = 0) -> str:
        return self._meson_info.get_targets(index, value='defined_in')

    def get_filename(self, index: int = 0) -> str:
        return self._meson_info.get_targets(index, value='filename')

    def get_build_by_default(self, index: int = 0) -> str:
        return self._meson_info.get_targets(index, value='build_by_default')

    def get_target_sources(self, index: int = 0) -> str:
        return self._meson_info.get_targets(index, value='target_sources')

    def get_subproject(self, index: int = 0) -> str:
        return self._meson_info.get_targets(index, value='subproject')

    def get_installed(self, index: int = 0) -> str:
        return self._meson_info.get_targets(index, value='installed')

    def get_install_filename(self, index: int = 0) -> str:
        return self._meson_info.get_targets(index, value='install_filename')
