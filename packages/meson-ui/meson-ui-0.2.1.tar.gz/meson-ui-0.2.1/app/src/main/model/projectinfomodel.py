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


class IntroProjectInfoModel:
    '''
        This is a data class for Meson project info
    '''

    def __init__(self, meson_info: MesonInfo = None):
        self._meson_info: MesonInfo = meson_info

    def get_name(self) -> str:
        return self._meson_info.get_projectinfo(value='descriptive_name')

    def get_version(self) -> str:
        return self._meson_info.get_projectinfo(value='version')

    def get_subprojects(self) -> str:
        return self._meson_info.get_projectinfo(value='subprojects')

    def get_subproject_dir(self) -> str:
        return self._meson_info.get_projectinfo(value='subproject_dir')
