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
from setuptools import setup
from app.src.main.coredata import AppCoreData as PyPiInfo
import sys

pypi_info = PyPiInfo()

pypi_info.required_version()

data_files = []
if sys.platform != 'win32':
    # Only useful on UNIX-like systems
    data_files = [('share/man/man1', ['man/mesonui.1'])]

setup(
    name=pypi_info.get_name(),
    author=pypi_info.get_author(),
    version=pypi_info.get_version(),
    license=pypi_info.get_license(),
    author_email=pypi_info.get_gmail(),
    description=pypi_info.get_description(),
    packages=pypi_info.get_packages(),
    data_files=data_files,
    entry_points={
        'gui_scripts': ['meson-ui=app.__main__:mesonui_main'],
    },
    zip_safe=True,
    include_package_data=True,
    install_requires=['PyQt5', 'meson', 'ninja']
)
