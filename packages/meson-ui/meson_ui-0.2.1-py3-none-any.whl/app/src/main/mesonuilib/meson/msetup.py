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


class MesonSetup(InterfaceMesonCommand):
    def __init__(self, context=None):
        self._context = context
        super().__init__(context=self._context)

    def run(self, args: list = []):
        try:
            meson_args = ['setup', self._context.get_sourcedir(), self._context.get_builddir()]
            meson_args.extend(args)
        except MesonBuildCommandError as e:
            print(f'exception: {e}')
        return self._run(cmd=meson_args)
