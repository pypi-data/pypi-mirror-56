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
from PyQt5.QtCore import QObject, QProcess
from app.src.main.model.mesonuimodel import MesonUiModule
from app.src.main.mesonuilib.meson.meson import Meson
from os.path import exists as does_exists
from os.path import join as join_paths
from time import sleep


test_case: map = {
    'case-01': 'test-cases/meson/01-setup-prog',
    'case-02': 'test-cases/meson/02-build-prog',
    'case-03': 'test-cases/meson/03-clean-prog',
    'case-04': 'test-cases/meson/04-test-prog',
    'case-05': 'test-cases/meson/05-install-prog',
    'case-06': 'test-cases/meson/06-dist-prog',
    'case-07': 'test-cases/meson/07-setup-error',
    'case-08': 'test-cases/meson/08-build-error',
    'case-09': 'test-cases/meson/09-clean-error',
    'case-10': 'test-cases/meson/10-test-error',
    'case-11': 'test-cases/meson/11-install-error',
    'case-12': 'test-cases/meson/12-dist-error',
    'case-13': 'test-cases/meson/13-intro-data',
    'case-14': 'test-cases/meson/14-intro-null',
}


#
# This class is faking the apps projetc data
#
class FakeProg(QObject):
    def __init__(self):
        super().__init__()
        self._process = QProcess(self)
        self.dir_src = ''
        self.dir_build = ''

    def process(self):
        return self._process

    def set_sourcedir(self, value: str) -> str:
        self.dir_src = value

    def set_builddir(self, value: str) -> str:
        self.dir_build = value

    def get_sourcedir(self) -> str:
        return self.dir_src

    def get_builddir(self) -> str:
        return self.dir_build


def test_basic_setup():
    prog = FakeProg()
    prog.set_sourcedir(test_case['case-01'])
    prog.set_builddir(join_paths(test_case['case-01'], 'builddir'))

    meson = Meson(prog)
    meson.setup()
    sleep(3)

    assert does_exists(prog.get_sourcedir())
    assert does_exists(prog.get_builddir())


def test_basic_build():
    prog = FakeProg()
    prog.set_sourcedir(test_case['case-02'])
    prog.set_builddir(join_paths(test_case['case-02'], 'builddir'))

    meson = Meson(prog)
    meson.setup()
    meson.build()

    assert does_exists(prog.get_sourcedir())
    assert does_exists(prog.get_builddir())


def test_basic_clean():
    prog = FakeProg()
    prog.set_sourcedir(test_case['case-03'])
    prog.set_builddir(join_paths(test_case['case-03'], 'builddir'))

    meson = Meson(prog)
    meson.setup()
    meson.build()

    meson.clean()

    assert does_exists(prog.get_sourcedir())
    assert does_exists(prog.get_builddir())


def test_basic_test():
    prog = FakeProg()
    prog.set_sourcedir(test_case['case-04'])
    prog.set_builddir(join_paths(test_case['case-04'], 'builddir'))

    meson = Meson(prog)
    meson.setup()
    meson.build()
    meson.tests()

    assert does_exists(prog.get_sourcedir())
    assert does_exists(prog.get_builddir())


def test_basic_install():
    prog = FakeProg()
    prog.set_sourcedir(test_case['case-05'])
    prog.set_builddir(join_paths(test_case['case-05'], 'builddir'))

    meson = Meson(prog)
    meson.setup()
    meson.build()
    meson.install()

    assert does_exists(prog.get_sourcedir())
    assert does_exists(prog.get_builddir())


def test_basic_dist():
    prog = FakeProg()
    prog.set_sourcedir(test_case['case-06'])
    prog.set_builddir(join_paths(test_case['case-06'], 'builddir'))

    meson = Meson(prog)
    meson.setup()
    meson.build()
    meson.dist()

    assert does_exists(prog.get_sourcedir())
    assert does_exists(prog.get_builddir())


def test_error_setup():
    prog = FakeProg()
    prog.set_sourcedir(test_case['case-07'])
    prog.set_builddir(join_paths(test_case['case-07'], 'builddir'))

    meson = Meson(prog)
    meson.setup()

    assert does_exists(prog.get_sourcedir())
    assert not does_exists(prog.get_builddir())


def test_error_build():
    prog = FakeProg()
    prog.set_sourcedir(test_case['case-08'])
    prog.set_builddir(join_paths(test_case['case-08'], 'builddir'))

    meson = Meson(prog)
    meson.build()

    assert does_exists(prog.get_sourcedir())
    assert not does_exists(prog.get_builddir())


def test_error_clean():
    prog = FakeProg()
    prog.set_sourcedir(test_case['case-09'])
    prog.set_builddir(join_paths(test_case['case-09'], 'builddir'))

    meson = Meson(prog)
    meson.setup()
    meson.clean()

    assert does_exists(prog.get_sourcedir())
    assert does_exists(prog.get_builddir())


def test_error_test():
    prog = FakeProg()
    prog.set_sourcedir(test_case['case-10'])
    prog.set_builddir(join_paths(test_case['case-10'], 'builddir'))

    meson = Meson(prog)
    meson.tests()

    assert does_exists(prog.get_sourcedir())
    assert not does_exists(prog.get_builddir())

def test_error_install():
    prog = FakeProg()
    prog.set_sourcedir(test_case['case-11'])
    prog.set_builddir(join_paths(test_case['case-11'], 'builddir'))

    meson = Meson(prog)
    meson.install()

    assert does_exists(prog.get_sourcedir())
    assert not does_exists(prog.get_builddir())


def test_error_dist():
    prog = FakeProg()
    prog.set_sourcedir(test_case['case-12'])
    prog.set_builddir(join_paths(test_case['case-12'], 'builddir'))

    meson = Meson(prog)
    meson.dist()

    assert does_exists(prog.get_sourcedir())
    assert not does_exists(prog.get_builddir())


def test_intro_data():
    prog = FakeProg()
    prog.set_sourcedir(test_case['case-13'])
    prog.set_builddir(join_paths(test_case['case-13'], 'builddir'))

    meson = Meson(prog)
    meson.setup()
    meson.build()

    meson_data: MesonUiModule = MesonUiModule(prog)
    intex: int = 0

    sleep(3)

    #Testing project info
    assert meson_data.get_projectinfo().get_name() == 'c-exe'
    assert meson_data.get_projectinfo().get_version() == 'undefined'
    assert meson_data.get_projectinfo().get_subproject_dir() == 'subprojects'
    assert meson_data.get_projectinfo().get_subprojects() == []

    # Testing targets info
    assert meson_data.get_targets().get_build_by_default() is True
    assert meson_data.get_targets().get_type() == 'executable'
    assert meson_data.get_targets().get_subproject() is None
    assert meson_data.get_targets().get_name() == 'exe'

    # Testing targets sources info
    assert meson_data.get_targets_sources().get_language() == 'c'

    # Testing test info
    assert meson_data.get_tests().get_environment(index=intex) == {}
    assert meson_data.get_tests().get_is_parallel(index=intex) is True
    assert meson_data.get_tests().get_name(index=intex) == 'Run test exe'
    assert meson_data.get_tests().get_priority(index=intex) == 0
    assert meson_data.get_tests().get_suite(index=intex) == ['c-exe']
    assert meson_data.get_tests().get_timeout(index=intex) == 30
    assert meson_data.get_tests().get_workdir(index=intex) is None

    # Testing benchmark info
    assert meson_data.get_benchmark().get_environment(index=intex) == {}
    assert meson_data.get_benchmark().get_is_parallel(index=intex) is True
    assert meson_data.get_benchmark().get_name(index=intex) == 'Run benchmark exe'
    assert meson_data.get_benchmark().get_priority(index=intex) == 0
    assert meson_data.get_benchmark().get_suite(index=intex) == ['c-exe']
    assert meson_data.get_benchmark().get_timeout(index=intex) == 30
    assert meson_data.get_benchmark().get_workdir(index=intex) is None


def test_intro_null():
    prog = FakeProg()
    prog.set_sourcedir(test_case['case-14'])

    meson_data: MesonUiModule = MesonUiModule(prog)
    intex: int = 0

    #Testing project info
    assert meson_data.get_projectinfo().get_name() == 'null'
    assert meson_data.get_projectinfo().get_version() == 'null'
    assert meson_data.get_projectinfo().get_subproject_dir() == 'null'
    assert meson_data.get_projectinfo().get_subprojects() == 'null'

    # Testing targets info
    assert meson_data.get_targets().get_build_by_default() == 'null'
    assert meson_data.get_targets().get_type() == 'null'
    assert meson_data.get_targets().get_subproject() == 'null'
    assert meson_data.get_targets().get_name() == 'null'

    # Testing targets sources info
    assert meson_data.get_targets_sources().get_compiler() == 'null'
    assert meson_data.get_targets_sources().get_language() == 'null'

    # Testing targets info
    assert meson_data.get_targets().get_build_by_default() == 'null'
    assert meson_data.get_targets().get_type() == 'null'
    assert meson_data.get_targets().get_subproject() == 'null'
    assert meson_data.get_targets().get_name() == 'null'

    # Testing targets sources info
    assert meson_data.get_targets_sources().get_compiler() == 'null'
    assert meson_data.get_targets_sources().get_language() == 'null'
    assert meson_data.get_targets_sources().get_sources() == 'null'

    # Testing test info
    assert meson_data.get_tests().get_environment(index=intex) == 'null'
    assert meson_data.get_tests().get_is_parallel(index=intex) == 'null'
    assert meson_data.get_tests().get_name(index=intex) == 'null'
    assert meson_data.get_tests().get_priority(index=intex) == 'null'
    assert meson_data.get_tests().get_suite(index=intex) == 'null'
    assert meson_data.get_tests().get_timeout(index=intex) == 'null'
    assert meson_data.get_tests().get_workdir(index=intex) == 'null'

    # Testing benchmark info
    assert meson_data.get_benchmark().get_environment(index=intex) == 'null'
    assert meson_data.get_benchmark().get_is_parallel(index=intex) == 'null'
    assert meson_data.get_benchmark().get_name(index=intex) == 'null'
    assert meson_data.get_benchmark().get_priority(index=intex) == 'null'
    assert meson_data.get_benchmark().get_suite(index=intex) == 'null'
    assert meson_data.get_benchmark().get_timeout(index=intex) == 'null'
    assert meson_data.get_benchmark().get_workdir(index=intex) == 'null'
