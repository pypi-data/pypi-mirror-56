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
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl


class InterfaceAppCompact(QMainWindow, QApplication):
    def __init__(self):
        super(QMainWindow, self).__init__()
        super(QApplication, self).__init__()

    def on_error(self, err):
        print(f'Exception: {err}')

    def on_open_url(self, url_link: str = ''):
        url = QUrl(url_link)
        QDesktopServices.openUrl(url=url)

    def empty(self):
        return ''

    def null(self):
        return 'null'
