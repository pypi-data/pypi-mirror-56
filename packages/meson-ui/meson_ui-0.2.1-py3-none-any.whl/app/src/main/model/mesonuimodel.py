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
from .targetsourcesmodel import IntroTargetSourcesModel
from .projectinfomodel import IntroProjectInfoModel
from .benchmarkmodel import IntroBenchmarkModel
from .mesoninfomodel import IntroMesonInfoModel
from .optionscoremodel import IntroCoreOptionsModel
from .optionsbasemodel import IntroBaseOptionsModel
from .optionspathmodel import IntroPathOptionsModel
from .targetmodel import IntroTargetModel
from .testmodel import IntroTestModel
from .projectmodel import ProjectModel
from ..repo.mesoninfo import MesonInfo


class MesonUiModule:
    def __init__(self, context=None):
        self._meson_info_json = MesonInfo(context=context)
        self._targets_sources_model = IntroTargetSourcesModel(meson_info=self._meson_info_json)
        self._projectinfo_model = IntroProjectInfoModel(meson_info=self._meson_info_json)
        self._benchmark_model = IntroBenchmarkModel(meson_info=self._meson_info_json)
        self._mesoninfo_model = IntroMesonInfoModel(meson_info=self._meson_info_json)
        self._coreopts_model = IntroCoreOptionsModel(meson_info=self._meson_info_json)
        self._baseopts_model = IntroBaseOptionsModel(meson_info=self._meson_info_json)
        self._pathopts_model = IntroPathOptionsModel(meson_info=self._meson_info_json)
        self._targets_model = IntroTargetModel(meson_info=self._meson_info_json)
        self._tests_model = IntroTestModel(meson_info=self._meson_info_json)
        self._project_model = ProjectModel(context=context)
    # end of method

    def get_benchmark(self) -> IntroBenchmarkModel:
        return self._benchmark_model
    # end of method

    def get_targets_sources(self) -> IntroTargetSourcesModel:
        return self._targets_sources_model
    # end of method

    def get_targets(self) -> IntroTargetModel:
        return self._targets_model
    # end of method

    def get_mesoninfo(self) -> IntroMesonInfoModel:
        return self._mesoninfo_model
    # end of method

    def get_core_option(self) -> IntroCoreOptionsModel:
        return self._coreopts_model
    # end of method

    def get_base_option(self) -> IntroBaseOptionsModel:
        return self._baseopts_model
    # end of method

    def get_path_option(self) -> IntroPathOptionsModel:
        return self._pathopts_model
    # end of method

    def get_tests(self) -> IntroTestModel:
        return self._tests_model
    # end of method

    def get_projectinfo(self) -> IntroProjectInfoModel:
        return self._projectinfo_model
    # end of method

    def get_project(self) -> ProjectModel:
        return self._project_model
    # end of method
