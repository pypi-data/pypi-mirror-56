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
from PyQt5.QtCore import QObject


class InterfaceNinjaCommand(QObject):
    def __init__(self, context):
        self._context = context

    def _run(self, cmd: list = []):
        self._context.process().waitForReadyRead()
        self._context.process().start('ninja', cmd)

    def __del__(self):
        self._context.process().terminate()
        if not self._context.process().waitForFinished(1000):
            self._context.process().kill()
