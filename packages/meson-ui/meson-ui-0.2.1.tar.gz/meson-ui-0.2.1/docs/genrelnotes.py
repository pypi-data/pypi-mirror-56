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
import sys, os, subprocess
from os.path import join as join_paths
from glob import glob

relnote_template = '''---
title: Release {}
short-description: Release notes for {}
...

# New features

'''


def add_to_sitemap(from_version, to_version):
    sitemapfile = join_paths('..', 'sitemap.txt')
    sf = open(sitemapfile)
    lines = sf.readlines()
    sf.close()
    with open(sitemapfile, 'w') as sf:
        for line in lines:
            if 'Release-notes' in line and from_version in line:
                new_line = line.replace(from_version, to_version)
                sf.write(new_line)
            sf.write(line)

def generate(from_version, to_version):
    ofilename = f'Release-notes-for-{to_version}.md'
    with open(ofilename, 'w') as ofile:
        ofile.write(relnote_template.format(to_version, to_version))
        for snippetfile in glob(join_paths('snippets', '*.md')):
            snippet = open(snippetfile).read()
            ofile.write(snippet)
            if not snippet.endswith('\n'):
                ofile.write('\n')
            ofile.write('\n')
            subprocess.check_call(['git', 'rm', snippetfile])
    subprocess.check_call(['git', 'add', ofilename])
    add_to_sitemap(from_version, to_version)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(sys.argv[0], 'from_version to_version')
        sys.exit(1)
    from_version = sys.argv[1]
    to_version = sys.argv[2]
    os.chdir('markdown')
    generate(from_version, to_version)
