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


class IntroMesonInfoModel:
    '''
        This is a data class for Meson build system info
    '''

    def __init__(self, meson_info: MesonInfo = None):
        self._meson_info: MesonInfo = meson_info

    def get_full_version(self):
        return self._meson_info.get_mesoninfo(value='full')

    def get_major_version(self):
        return self._meson_info.get_mesoninfo(value='major')

    def get_minor_version(self):
        return self._meson_info.get_mesoninfo(value='minor')

    def get_patch_version(self):
        return self._meson_info.get_mesoninfo(value='patch')
