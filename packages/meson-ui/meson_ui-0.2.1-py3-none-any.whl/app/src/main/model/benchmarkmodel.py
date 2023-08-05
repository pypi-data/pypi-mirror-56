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


class IntroBenchmarkModel:
    '''
        This is a data class for Meson benchmark info
    '''

    def __init__(self, meson_info: MesonInfo = None):
        self._meson_info: MesonInfo = meson_info

    def get_command(self, index: int = 0) -> str:
        return self._meson_info.get_benchmarks(index, value='cmd')

    def get_environment(self, index: int = 0) -> str:
        return self._meson_info.get_benchmarks(index, value='env')

    def get_name(self, index: int = 0) -> str:
        return self._meson_info.get_benchmarks(index, value='name')

    def get_workdir(self, index: int = 0) -> str:
        return self._meson_info.get_benchmarks(index, value='workdir')

    def get_timeout(self, index: int = 0) -> str:
        return self._meson_info.get_benchmarks(index, value='timeout')

    def get_suite(self, index: int = 0) -> str:
        return self._meson_info.get_benchmarks(index, value='suite')

    def get_is_parallel(self, index: int = 0) -> str:
        return self._meson_info.get_benchmarks(index, value='is_parallel')

    def get_priority(self, index: int = 0) -> str:
        return self._meson_info.get_benchmarks(index, value='priority')
