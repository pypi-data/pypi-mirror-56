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
import sys


class AppCoreData:
    @staticmethod
    def get_version() -> str:
        return '0.2.1'
    # end of method

    @staticmethod
    def get_name() -> str:
        return 'meson-ui'
    # end of method

    @staticmethod
    def get_license() -> str:
        return 'Apache 2.0'
    # end of method

    @staticmethod
    def get_author() -> str:
        return 'Michael Brockus'
    # end of method

    @staticmethod
    def get_gmail() -> str:
        return 'michaelbrockus@gmail.com'
    # end of method

    @staticmethod
    def get_description() -> str:
        return 'Command line GUI for the Meson build system.'
    # end of method

    @staticmethod
    def get_packages() -> list:
        return ['app',
                'app.src',
                'app.src.main',
                'app.src.main.controller',
                'app.src.main.model',
                'app.src.main.repo',
                'app.src.main.view',
                'app.src.main.ui',
                'app.src.main.mesonuilib',
                'app.src.main.mesonuilib.interface',
                'app.src.main.mesonuilib.component',
                'app.src.main.mesonuilib.ninja',
                'app.src.main.mesonuilib.meson',
                'app.src.main.mesonuilib.utils']
    # end of method

    @staticmethod
    def required_version() -> None:
        if sys.version_info < (3, 6, 0):
            raise SystemExit(f'ERROR: Tried to install Meson-ui with an unsupported Python version: {sys.version}'
                             '\n\nMeson requires Python 3.6.0 or greater')
