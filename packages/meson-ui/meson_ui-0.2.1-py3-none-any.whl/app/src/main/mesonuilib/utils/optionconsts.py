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


'''
   The const values are stored in this map so we can reuse the name value
   as the key to get a value from whatever option we need at the time.
'''
core_opts: map = {
    'auto_features': 0,
    'backend': 1,
    'buildtype': 2,
    'debug': 3,
    'default_library': 4,
    'install_umask': 5,
    'layout': 6,
    'optimization': 7,
    'strip': 8,
    'unity': 9,
    'warning_level': 10,
    'werror': 11,
    'wrap_mode': 12,
    'cmake_prefix_path': 13,
    'pkg_config_path': 14,
    'build.cmake_prefix_path': 15,
    'build.pkg_config_path': 16,
    'backend_max_links': 17,
}

base_opts: map = {
    'b_asneeded': 18,
    'b_bitcode': 19,
    'b_colorout': 20,
    'b_coverage': 21,
    'b_lto': 22,
    'b_lundef': 23,
    'b_ndebug': 24,
    'b_pch': 25,
    'b_pgo': 26,
    'b_pie': 27,
    'b_sanitize': 28,
    'b_staticpic': 29,
}

path_opts: map = {
    'bindir': 36,
    'datadir': 37,
    'execdir': 38,
    'includedir': 39,
    'infodir': 40,
    'libdir': 41,
    'libexecdir': 42,
    'localedir': 43,
    'localstatedir': 44,
    'mandir': 45,
    'prefix': 46,
    'sbindir': 47,
    'sharedstatedir': 48,
    'sysconfdir': 49
}

c_cmpl: map = {
    'c_args': 30,
    'c_link_args': 31,
    'c_std': 32,
    'build.c_args': 33,
    'build.c_link_args': 34,
    'build.c_std': 35,
}

cpp_cmpl: map = {
    'cpp_args': 30,
    'cpp_link_args': 31,
    'cpp_std': 32,
    'build.cpp_args': 33,
    'build.cpp_link_args': 34,
    'build.cpp_std': 35,
}
