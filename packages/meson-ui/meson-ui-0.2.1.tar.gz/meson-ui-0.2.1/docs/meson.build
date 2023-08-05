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
project('Meson-ui documentation', version: '0.1.0')

hotdoc = import('hotdoc')

documentation = hotdoc.generate_doc(meson.project_name(),
    project_version: meson.project_version(),
    sitemap: 'sitemap.txt',
    build_by_default: true,
    index: 'markdown/index.md',
    install: false,
    extra_assets: ['images/', join_paths('..', 'app', 'src', 'main', 'res', 'assets')],
    include_paths: ['markdown'],
    default_license: 'CC-BY-SAv4.0',
    html_extra_theme: join_paths('theme', 'extra'),
    syntax_highlighting_activate: true
)