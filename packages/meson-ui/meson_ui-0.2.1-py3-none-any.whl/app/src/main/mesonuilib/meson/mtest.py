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
from ..interface.interfacemesoncmd import InterfaceMesonCommand
from ..utils.exceptions import MesonBuildCommandError


class MesonTest(InterfaceMesonCommand):
    def __init__(self, context=None):
        self._context = context
        super().__init__(context=self._context)

    def run(self):
        try:
            meson_args = ['test', '-C', self._context.get_builddir()]
        except MesonBuildCommandError as e:
            print(f'exception: {e}')
        return self._run(cmd=meson_args)
