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

class MesonUiError(Exception):
    """Meson-ui exception!"""

class MesonBuildError(Exception):
    """Meson build system exception!"""
    pass

class NinjaBuildError(Exception):
    """Ninja build system exception!"""
    pass

class MesonBuildCommandError(MesonBuildError):
    """Meson build command exception!"""
    pass

class NinjaBuildCommandError(NinjaBuildError):
    """Ninja build command exception!"""
    pass
