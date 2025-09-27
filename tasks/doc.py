
####################################################################################################
#
# -
# Copyright (C) 2025 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

from pathlib import Path
# import os
import shutil

from invoke import task

# from .release import update_git_sha as _update_git_sha

####################################################################################################

SOURCE_PATH = Path(__file__).resolve().parents[1]

SPHINX_PATH = SOURCE_PATH.joinpath('doc', 'sphinx')
BUILD_PATH = SPHINX_PATH.joinpath('build')
RST_SOURCE_PATH = SPHINX_PATH.joinpath('source')
RST_API_PATH = RST_SOURCE_PATH.joinpath('api')
RST_EXAMPLES_PATH = RST_SOURCE_PATH.joinpath('examples')

####################################################################################################

@task
def clean_build(ctx):
    # ctx.run('rm -rf {}'.format(BUILD_PATH))
    if BUILD_PATH.exists():
        shutil.rmtree(BUILD_PATH)

####################################################################################################

@task
def clean_api(ctx):
    # ctx.run('rm -rf {}'.format(RST_API_PATH))
    if RST_API_PATH.exists():
        shutil.rmtree(RST_API_PATH)

# @task(_update_git_sha, clean_api)
@task(clean_api)
def make_api(ctx):
    print()
    print('Generate RST API files')
    ctx.run('pyterate-rst-api {0.Package}'.format(ctx))
    run_sphinx(ctx)
    print('')
    print('<<< Check API contains undocumented >>>')

####################################################################################################

@task
def run_sphinx(ctx):
    print()
    print('Run Sphinx')
    working_path = SPHINX_PATH
    # subprocess.run(('make-html'), cwd=working_path)
    # --clean
    with ctx.cd(str(working_path)):
        ctx.run('make-html')

####################################################################################################

@task
def make_readme(ctx):
    # File "/usr/bin/rst2html", line 17, in <module>
    # from docutils.core import publish_cmdline, default_description
    # ModuleNotFoundError: No module named 'docutils'
    from setup_data import long_description
    with open('README.rst', 'w') as fh:
        fh.write(long_description)
    # import subprocess
    # subprocess.call(('rst2html', 'README.rst', 'README.html'))
    ctx.run('rst2html5.py README.rst README.html')

####################################################################################################

# @task
# def update_authors(ctx):
#     # Keep authors in the order of appearance and use awk to filter out dupes
#     ctx.run("git log --format='- %aN <%aE>' --reverse | awk '!x[$0]++' > AUTHORS")

####################################################################################################

# @task
# def publish(ctx):
#     from .SECRET_CONFIG import SSH_CONFIG
#     import PySpice
#     release = PySpice.__version__
#     rc = input(f"Release is {release}: [Y/N]")
#     if rc.lower() != 'y':
#         return
#     print('rsync...')
#     version = '.'.join(release.split('.')[:2])
#     command_template = (
#         'rsync'
#         ' -av -c --delete'
#         ' --exclude="*~" --delete-excluded'
#         ' -e "ssh -p {ssh_port}" {src_path}/ {ssh_user}@{ssh_host}:{ssh_path}/releases/v{version}/'
#     )
#     command = command_template.format(
#         src_path=BUILD_PATH.joinpath('html'),
#         version=version,
#         **SSH_CONFIG)
#     print(command)
#     ctx.run(command)

####################################################################################################

@task
def xdg_open(ctx):
    ctx.run('xdg-open doc/sphinx/build/html/index.html')
