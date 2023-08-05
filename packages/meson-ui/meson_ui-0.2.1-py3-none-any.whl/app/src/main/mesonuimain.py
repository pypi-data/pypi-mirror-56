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
from .mesonuiinit import MesonUi
from .coredata import AppCoreData
import argparse
import sys


def mesonui_main():
    coredata: AppCoreData = AppCoreData()

    parser: argparse = argparse.ArgumentParser(description='Meson-ui Process args.')

    parser.add_argument('-v', '--version', action='version', version=coredata.get_version(), help='print version number')
    parser.parse_args()

    app: MesonUi = MesonUi(sys_argv=sys.argv)
    sys.exit(app.exec_())
# end of function mesonui_main

if __name__ == "__main__":
    mesonui_main()
