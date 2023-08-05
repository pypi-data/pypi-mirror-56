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
from ..interface.interfaceninjacmd import InterfaceNinjaCommand
from ..utils.exceptions import NinjaBuildCommandError


class NinjaBuild(InterfaceNinjaCommand):
    def __init__(self, context):
        self._context = context
        super(self.__class__, self).__init__(context=self._context)

    def run(self):
        try:
            self._run(cmd=['-C', self._context.get_builddir()])
        except NinjaBuildCommandError as e:
            print(f'exception: {e}')
    # end of method
