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


class IntroTargetSourcesModel:
    '''
        This is a data class for Meson target sources info
    '''

    def __init__(self, meson_info: MesonInfo = None):
        self._meson_info: MesonInfo = meson_info

    def get_language(self, index: int = 0) -> str:
        return self._meson_info.get_targets_sources(index, value='language')

    def get_compiler(self, index: int = 0) -> str:
        return self._meson_info.get_targets_sources(index, value='compiler')

    def get_parameters(self, index: int = 0) -> str:
        return self._meson_info.get_targets_sources(index, value='parameters')

    def get_sources(self, index: int = 0) -> str:
        return self._meson_info.get_targets_sources(index, value='sources')

    def get_generated_sources(self, index: int = 0) -> str:
        return self._meson_info.get_targets_sources(index, value='generated_sources')
