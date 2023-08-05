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
from .ninjainstall import NinjaInstall
from .ninjabuild import NinjaBuild
from .ninjaclear import NinjaClean
from .ninjatest import NinjaTests
from .ninjadist import NinjaDist


class Ninja:
    def __init__(self, context = None):
        self._context = context
        self._install: NinjaInstall = NinjaInstall(context=self._context)
        self._build: NinjaBuild = NinjaBuild(context=self._context)
        self._clean: NinjaBuild = NinjaClean(context=self._context)
        self._tests: NinjaTests = NinjaTests(context=self._context)
        self._dist: NinjaDist = NinjaDist(context=self._context)
    # end of method

    def build(self) -> NinjaBuild:
        return self._build.run()
    # end of method

    def clean(self) -> NinjaClean:
        return self._clean.run()
    # end of method

    def test(self) -> NinjaTests:
        return self._tests.run()
    # end of method

    def install(self) -> NinjaInstall:
        return self._install.run()
    # end of method

    def dist(self) -> NinjaDist:
        return self._dist.run()
    # end of method
