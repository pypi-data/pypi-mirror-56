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
from ..mesonuilib.utils.optionconsts import (path_opts)


class IntroPathOptionsModel:
    def __init__(self, meson_info: MesonInfo = None):
        self._meson_info: MesonInfo = meson_info

    def get_bindir(self, value: str):
        return self._meson_info.get_option(path_opts['bindir'], value)

    def get_datadir(self, value: str):
        return self._meson_info.get_option(path_opts['datadir'], value)

    def get_includedir(self, value: str):
        return self._meson_info.get_option(path_opts['includedir'], value)

    def get_infodir(self, value: str):
        return self._meson_info.get_option(path_opts['infodir'], value)

    def get_libdir(self, value: str):
        return self._meson_info.get_option(path_opts['libdir'], value)

    def get_libexecdir(self, value: str):
        return self._meson_info.get_option(path_opts['libexecdir'], value)

    def get_localedir(self, value: str):
        return self._meson_info.get_option(path_opts['localedir'], value)

    def get_localstatedir(self, value: str):
        return self._meson_info.get_option(path_opts['localstatedir'], value)

    def get_manddir(self, value: str):
        return self._meson_info.get_option(path_opts['mandir'], value)

    def get_prefix(self, value: str):
        return self._meson_info.get_option(path_opts['prefix'], value)

    def get_sbindir(self, value: str):
        return self._meson_info.get_option(path_opts['sbindir'], value)

    def get_sharedstatedir(self, value: str):
        return self._meson_info.get_option(path_opts['sharedstatedir'], value)

    def get_sysconfdir(self, value: str):
        return self._meson_info.get_option(path_opts['sysconfdir'], value)

    def get_execdir(self, value: str):
        return self._meson_info.get_option(path_opts['execdir'], value)
