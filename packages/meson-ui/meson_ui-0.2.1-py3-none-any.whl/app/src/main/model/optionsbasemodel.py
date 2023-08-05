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
from ..mesonuilib.utils.optionconsts import (base_opts)


class IntroBaseOptionsModel:
    def __init__(self, meson_info: MesonInfo = None):
        self._meson: MesonInfo = meson_info

    def get_b_asneeded(self, value: str):
        return self._meson_info.get_option(base_opts['b_asneeded'], value)

    def get_b_bitcode(self, value: str):
        return self._meson_info.get_option(base_opts['b_bitcode'], value)

    def get_b_colorout(self, value: str):
        return self._meson_info.get_option(base_opts['b_colorout'], value)

    def get_b_coverage(self, value: str):
        return self._meson_info.get_option(base_opts['b_coverage'], value)

    def get_b_lto(self, value: str):
        return self._meson_info.get_option(base_opts['b_lto'], value)

    def get_b_lundef(self, value: str):
        return self._meson_info.get_option(base_opts['b_lundef'], value)

    def get_b_ndebug(self, value: str):
        return self._meson_info.get_option(base_opts['b_ndebug'], value)

    def get_b_pch(self, value: str):
        return self._meson_info.get_option(base_opts['b_pch'], value)

    def get_b_pgo(self, value: str):
        return self._meson_info.get_option(base_opts['b_pgo'], value)

    def get_b_pie(self, value: str):
        return self._meson_info.get_option(base_opts['b_pie'], value)

    def get_b_sanitize(self, value: str):
        return self._meson_info.get_option(base_opts['b_sanitize'], value)

    def get_b_staticpi(self, value: str):
        return self._meson_info.get_option(base_opts['b_staticpi'], value)
