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
from subprocess import check_call

check_call(['python3', 'setup.py', 'sdist', 'bdist_wheel'])
check_call(['python3', '-m', 'twine', 'upload', 'dist/*'])
