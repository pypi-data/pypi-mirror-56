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
import json
from os.path import join as join_paths
from os import path

class MesonInfo:
    '''
        This works on getting the data from Meson 'intro-*.json' files.
        and feeds it to the data wrappers classes.
    '''

    def __init__(self, context = None):
        self._context = context
    # end of method

    def _meson_info_dir(self) -> str:
        return join_paths(f'{self._context.get_builddir()}', 'meson-info', 'meson-info.json')

    def _load_data(self, key: str) -> any:
        info_path = join_paths(self._meson_info_dir())
        if not path.exists(info_path):
            return 'null'
        with open(info_path, 'r') as f:
            data = json.load(f)
        return data["introspection"]["information"][key]["file"]

    def _load_infodir(self) -> list:
        info_path = join_paths(self._meson_info_dir())
        if not path.exists(info_path):
            return 'null'
        with open(info_path, 'r') as f:
            info = json.load(f)
        return info["directories"]["info"]

    def get_mesoninfo(self, value: str) -> any:
        info_path = join_paths(self._meson_info_dir())
        if not path.exists(info_path):
            return 'null'
        with open(info_path, 'r') as f:
            info = json.load(f)
        return info['meson_version'][value]

    def get_projectinfo(self, value: str) -> any:
        info_path = join_paths(self._load_infodir(), self._load_data('projectinfo'))
        if not path.exists(info_path):
            return 'null'
        with open(info_path, 'r') as f:
            info = json.load(f)
        return info[value]

    def get_targets(self, index: int, value: str) -> any:
        info_path = join_paths(self._load_infodir(), self._load_data('targets'))
        if not path.exists(info_path):
            return 'null'
        with open(info_path, 'r') as f:
            info = json.load(f)
        return info[index][value]

    def get_benchmarks(self, index: int, value: str) -> any:
        info_path = join_paths(self._load_infodir(), self._load_data('benchmarks'))
        if not path.exists(info_path):
            return 'null'
        with open(info_path, 'r') as f:
            info = json.load(f)
        return info[index][value]

    def get_tests(self, index: int, value: str) -> any:
        info_path = join_paths(self._load_infodir(), self._load_data('tests'))
        if not path.exists(info_path):
            return 'null'
        with open(info_path, 'r') as f:
            info = json.load(f)
        return info[index][value]

    def get_targets_sources(self, index: int, value: str) -> any:
        info_path = join_paths(self._load_infodir(), self._load_data('targets'))
        if not path.exists(info_path):
            return 'null'
        with open(info_path, 'r') as f:
            info = json.load(f)
        return info[index]['target_sources'][index][value]

    def get_option(self, index: int, value: str):
        info_path = join_paths(self._load_infodir(), self._load_data('buildoptions'))
        if not path.exists(info_path):
            return 'null'
        with open(info_path, 'r') as f:
            info = json.load(f)
        return info[index][value]

    def get_dir(self, value: str) -> any:
        with open(self._meson_info_dir(), 'r') as f:
            dirs = json.load(f)
        return dirs["directories"][value]
