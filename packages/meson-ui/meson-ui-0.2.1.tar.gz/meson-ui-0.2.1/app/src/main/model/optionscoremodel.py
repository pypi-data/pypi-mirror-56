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
from ..mesonuilib.utils.optionconsts import (core_opts)


class IntroCoreOptionsModel:
    def __init__(self, meson_info: MesonInfo = None):
        self._meson_info: MesonInfo = meson_info

    def get_auto_feature(self, value: str):
        return self._meson_info.get_option(core_opts['auto_features'], value)

    def get_backend(self, value: str):
        return self._meson_info.get_option(core_opts['backend'], value)

    def get_buildtype(self, value: str):
        return self._meson_info.get_option(core_opts['buildtype'], value)

    def get_debug(self, value: str):
        return self._meson_info.get_option(core_opts['debug'], value)

    def get_default_library(self, value: str):
        return self._meson_info.get_option(core_opts['default_library'], value)

    def get_install_umask(self, value: str):
        return self._meson_info.get_option(core_opts['install_umask'], value)

    def get_layout(self, value: str):
        return self._meson_info.get_option(core_opts['layout'], value)

    def get_optimization(self, value: str):
        return self._meson_info.get_option(core_opts['optimization'], value)

    def get_strip(self, value: str):
        return self._meson_info.get_option(core_opts['strip'], value)

    def get_unity(self, value: str):
        return self._meson_info.get_option(core_opts['unity'], value)

    def get_warning_level(self, value: str):
        return self._meson_info.get_option(core_opts['warning_level'], value)

    def get_werror(self, value: str):
        return self._meson_info.get_option(core_opts['werror'], value)

    def get_wrap_mode(self, value: str):
        return self._meson_info.get_option(core_opts['wrap_mode'], value)

    def get_cmake_prefix_path(self, value: str):
        return self._meson_info.get_option(core_opts['cmake_prefix_path'], value)

    def get_pkg_config_path(self, value: str):
        return self._meson_info.get_option(core_opts['pkg_config_path'], value)

    def get_build_cmake_prefix_path(self, value: str):
        return self._meson_info.get_option(core_opts['build.cmake_prefix_path'], value)

    def get_build_pkg_config_path(self, value: str):
        return self._meson_info.get_option(core_opts['build.pkg_config_path'], value)

    def get_backend_max_links(self, value: str):
        return self._meson_info.get_option(core_opts['backend_max_links'], value)
