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

meson_version: map = {
    '50':      '0.50.0',
    '50-beta': '0.50.999',
    '51':      '0.51.0',
    '51-beta': '0.51.999',
    '52':      '0.52.0',
    '52-beta': '0.52.999',
}

MESON_BUILD_FILE = 'meson.build'
MESON_BUILD_DIR = 'builddir'

class Cout:
    def __lshift__(self, other):
        print(other, end='')
        return self

    def __rrshift__(self, other):
        print(other, end='')
        return self


class Endl:
    def __lshift__(self, other):
        return other + '\n'

    def __rrshift__(self, other):
        return '\n'

cout = Cout()
endl = Endl()


class MesonString(str):
    """Meson string type"""

    def type_id(self):
        return 'string'


class MesonCombo(str):
    """Meson combo type"""

    def type_id(self):
        return 'combo'


class MesonArray(str):
    """Meson array type"""

    def type_id(self):
        return 'array'


class MesonInteger(str):
    """Meson integer type"""

    def type_id(self):
        return 'integer'


class MesonBool(str):
    """Meson boolean type"""

    def type_id(self):
        return 'bool'

    def false(self):
        return 'false'

    def true(self):
        return 'true'
