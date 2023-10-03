#!/usr/bin/env python3
#
# Copyright 2021-2023 Michael Shafae
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
""" Utilities used to manipulate C++ source code files from student
    assignments. """

import datetime
import glob
import json
import subprocess
import difflib
import os
import os.path
import platform
import sys
from logger import setup_logger

import lab_config as cfg


def backup_file(target_file_path):
    """Given a path to a file, back it up by copying it to a new filename."""
    logger = setup_logger()
    mtime_str = datetime.datetime.fromtimestamp(
        os.path.getmtime(target_file_path)
    ).strftime('%Y%m%d-%H%M%S')
    backup_path = f'{target_file_path}_{mtime_str}'
    logger.debug(f'Backing up {target_file_path} to {backup_path}.')
    try:
        os.rename(target_file_path, backup_path)
    except OSError as exception:
        logger.error(
            f'Cannot backup {target_file_path} to {backup_path}\n{exception.strerror}'
        )
        sys.exit(1)


def mk_makefiles(repo_root, config=cfg, makefile_name='Makefile'):
    """Given a configuration dict and a repository root
    (relative or fully qualified path), generate all makefiles"""
    logger = setup_logger()
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if cfg.lab['hidden_makefiles']:
        makefile_name = f'.{makefile_name}'
    # Make makefiles for each part
    for part in range(config.lab['num_parts']):
        part_num = part + 1
        part_path = os.path.join(repo_root, f'part-{part_num}')
        makefile_path = os.path.join(part_path, makefile_name)
        part_cfg = config.lab['parts'][part]
        part_makefile = f"""
# Automatically generated by {__file__} on {now}

TARGET = {part_cfg['target']}
# C++ Source Code Files
CXXFILES = {part_cfg['src']} {part_cfg['other_src']}
# C++ Headers Files
HEADERS = {part_cfg['header']} {part_cfg['other_header']}

DO_UNITTESTS = "{str(part_cfg['do_unit_tests'])}"

CXX = {part_cfg['CXX']}
CXXFLAGS += {part_cfg['CXXFLAGS']}
LDFLAGS += {part_cfg['LDFLAGS']}

UNAME_S = $(shell uname -s)
ifeq ($(UNAME_S),Linux)
	CXXFLAGS += {part_cfg['linux_CXXFLAGS']}
	LDFLAGS += {part_cfg['linux_LDFLAGS']}
	SED = {part_cfg['linux_sed']}
	GTESTINCLUDE = {part_cfg['linux_GTESTINCLUDE']}
	GTESTLIBS = {part_cfg['linux_GTESTLIBS']}
	# Note in Ubuntu 22 clang++ has it's own std. library
	# clang++ -nostdinc++ -nostdlib++ -isystem /usr/lib/llvm-14/include/c++/v1 -L /usr/lib/llvm-14/lib -Wl,-rpath,/usr/lib/llvm-14/lib -lc++ -std=c++17 
endif
ifeq ($(UNAME_S),Darwin)
	ifeq (,$(wildcard "/opt/local/bin/port"))
		# Use MacPorts clang++'s standard library
		CXXFLAGS += {part_cfg['darwin_CXXFLAGS']}
		LDFLAGS += {part_cfg['darwin_LDFLAGS']}
		SED = {part_cfg['darwin_sed']}
		GTESTINCLUDE = {part_cfg['darwin_GTESTINCLUDE']}
		GTESTLIBS = {part_cfg['darwin_GTESTLIBS']}
	else
		# Use Apple's standard library (not recommended)
		CXXFLAGS += -D OSX
	endif
endif
UNAME_M = $(shell uname -m)
ifeq ($(UNAME_M),x86_64)
	CXXFLAGS += -D AMD64
endif
ifneq ($(filter %86,$(UNAME_M)),)
	CXXFLAGS += -D IA32
endif
ifneq ($(filter arm%,$(UNAME_M)),)
	CXXFLAGS += -D ARM
endif

GTEST_OUTPUT_FORMAT ?= "{part_cfg['GTEST_OUTPUT_FORMAT']}"
GTEST_OUTPUT_FILE ?= "{part_cfg['GTEST_OUTPUT_FILE']}"

DOXYGEN = {part_cfg['DOXYGEN']}
DOCDIR = {part_cfg['DOCDIR']}

MAKEHEADERS := $(shell command -v makeheaders 2>/dev/null)

OBJECTS = $(CXXFILES:.cc=.o)

DEP = $(CXXFILES:.cc=.d)

MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
PART_PATH := $(dir $(MKFILE_PATH))
LAB_PART := $(notdir $(patsubst %/,%,$(dir $(MKFILE_PATH))))

.SILENT: doc lint format header test

default all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) $(LDFLAGS) -o $(TARGET) $(OBJECTS) $(LLDLIBS)

-include $(DEP)

%.d: %.cc
	set -e; $(CXX) -MM $(CXXFLAGS) $< \
	| sed 's/\($*\)\.o[ :]*/\1.o $@ : /g' > $@; \
	[ -s $@ ] || rm -f $@

%.o: %.cc
	$(CXX) $(CXXFLAGS) -c $<

clean:
	-rm -f $(OBJECTS) core $(TARGET).core

spotless: clean cleanunittest
	-rm -f $(TARGET) $(DEP) a.out
	-rm -rf $(DOCDIR)
	-rm -rf $(TARGET).dSYM
	-rm -f compile_commands.json

doc: $(CXXFILES) $(HEADERS)
	(cat Doxyfile; echo "PROJECT_NAME = $(TARGET)") | $(DOXYGEN) -

compilecmd:
	@echo "$(CXX) $(CXXFLAGS)"

format:
	@python3 ../.action/checks.py format $(LAB_PART)

lint:
	@python3 ../.action/checks.py lint $(LAB_PART)

header:
	@python3 ../.action/checks.py header $(LAB_PART)

test:
	@python3 ../.action/solution_check.py $(LAB_PART) $(TARGET)

ifneq ($(DO_UNITTESTS), "True")
unittest:
	@echo "No unit tests for $(LAB_PART)"
else
unittest: cleanunittest utest

utest: {part_cfg['gtest_dependencies']}
	{part_cfg['gtest_compile_cmd']}
	{part_cfg['gtest_run']}

endif

cleanunittest:
		-@rm -rf unittest.dSYM
		-@rm unittest test_detail.json

        """
        if not os.path.exists(part_path):
            logger.warning(
                f'Directory "{part_path}" does not exist. Creating...'
            )
            os.mkdir(part_path)
        if os.path.exists(makefile_path):
            logger.info(f'File {makefile_path} exists. Backing it up.')
            backup_file(makefile_path)
        with open(makefile_path, 'w', encoding='UTF-8') as file_handle:
            file_handle.write(part_makefile)

    # Make repo_root level Makefile
    top_level_makefile = f"""
# Automatically generated by {__file__} on {now}

TOPTARGETS = all clean spotless format lint header test unittest

SUBDIRS = $(wildcard part-?/.)

default all: all

$(TOPTARGETS): $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) -f {makefile_name} -C $@ $(MAKECMDGOALS)

.PHONY: $(TOPTARGETS) $(SUBDIRS)

"""
    target = os.path.join(repo_root, makefile_name)
    if os.path.exists(target):
        logger.info(f'File {target} exists. Backing it up.')
        backup_file(target)
    with open(target, 'w', encoding='UTF-8') as file_handle:
        file_handle.write(top_level_makefile)


def mk_doxyfile(target_dir, doxyfile='Doxyfile'):
    """Create a basic Doxyfile given a path."""
    logger = setup_logger()
    doxyfile_src = f"""
DOXYFILE_ENCODING      = UTF-8
OUTPUT_DIRECTORY       = {cfg.global_makefile['DOCDIR']}
GENERATE_LATEX         = NO
USE_MDFILE_AS_MAINPAGE = README.md
"""
    target = os.path.join(target_dir, doxyfile)
    if os.path.exists(target):
        logger.info(f'File {target} exists. Backing it up.')
        backup_file(target)
    with open(target, 'w', encoding='UTF-8') as file_handle:
        file_handle.write(doxyfile_src)


def create_clang_compile_commands_db(
    files=None, remove_existing_db=False, compile_cmd=None
):
    """Create a Clang compile commands DB named
    compile_commands.json in the current working directory."""
    out = 'compile_commands.json'
    linux_includes = ' -I/usr/include/c++/9/'
    darwin_includes = ' -D OSX -nostdinc++ -I/opt/local/include/libcxx/v1'
    my_platform = platform.system()
    logger = setup_logger()
    if not compile_cmd:
        compile_cmd = 'clang++ -g -O3 -Wall -pipe -std=c++14'
    if my_platform == 'Linux':
        compile_cmd = compile_cmd + linux_includes
    elif my_platform == 'Darwin':
        compile_cmd = compile_cmd + darwin_includes
    if not files:
        files = glob.glob('*.cc')
    compile_commands_db = [
        {
            'directory': '/tmp',
            'command': '{} {}'.format(compile_cmd, f),
            'file': f,
        }
        for f in files
    ]
    if os.path.exists(out) and remove_existing_db:
        logger.debug('Removing %s', out)
        os.unlink(out)
    elif os.path.exists(out) and not remove_existing_db:
        logger.warning(
            'The file %s already exists and will not be removed.', out
        )
        logger.warning('Compile commands DB not created. Using existing.')
    if not os.path.exists(out):
        with open(out, 'w', encoding='UTF-8') as file_handle:
            logger.debug('Writing %s', out)
            json.dump(compile_commands_db, file_handle)


def remove_cpp_comments(file):
    """Remove CPP comments from a file using the CPP preprocessor"""
    # Inspired by
    # https://stackoverflow.com/questions/13061785/remove-multi-line-comments
    # and
    # https://stackoverflow.com/questions/35700193/how-to-find-a-search-term-in-source-code/35708616#35708616
    logger = setup_logger()
    no_comments = None
    cmd = 'clang++ -E -P -'
    try:
        with open(file, encoding='UTF-8') as file_handle:
            # replace 'a', '__' and '#' to avoid preprocessor handling
            filtered_contents = (
                file_handle.read()
                .replace('a', 'aA')
                .replace('__', 'aB')
                .replace('#', 'aC')
            )
        proc = subprocess.run(
            [cmd],
            capture_output=True,
            shell=True,
            timeout=10,
            check=False,
            text=True,
            input=filtered_contents,
        )
        if proc.returncode == 0:
            no_comments = (
                proc.stdout.replace('aC', '#')
                .replace('aB', '__')
                .replace('aA', 'a')
            )
        else:
            logger.error('Errors encountered removing comments.')
            logger.error('stderr {}'.format(str(proc.stderr).rstrip("\n\r")))
    except FileNotFoundError as exception:
        logger.error('Cannot remove comments. No such file. %s', file)
        logger.error(exception)
    return no_comments


def makefile_has_compilecmd(target_makefile):
    """Given a Makefile, see if it has the compilecmd target which prints
    the compilation command to stdout."""
    has_compilecmd = False
    logger = setup_logger()
    try:
        with open(target_makefile, encoding='UTF-8') as file_handle:
            has_compilecmd = file_handle.read().find('compilecmd:') != -1
    except FileNotFoundError as exception:
        logger.error('Cannot open Makefile "%s" for reading.', target_makefile)
        logger.error(exception)
    return has_compilecmd


def makefile_get_compilecmd(target_dir, compiler='clang++'):
    """Given a Makefile with the compilecmd target, return the string
    which represents the compile command. For use with making the
    compile database for linting."""
    logger = setup_logger()
    compilecmd = None
    makefiles = glob.glob(
        os.path.join(target_dir, '*Makefile'), recursive=False
    )
    # Break on the first matched Makefile with compilecmd
    matches = None
    for makefile in makefiles:
        if makefile_has_compilecmd(makefile):
            cmd = 'make -C {} compilecmd'.format(target_dir)
            proc = subprocess.run(
                [cmd],
                capture_output=True,
                shell=True,
                timeout=10,
                check=False,
                text=True,
            )
            matches = [
                line
                for line in str(proc.stdout).split('\n')
                if line.startswith(compiler)
            ]
            break
    if matches:
        compilecmd = matches[0]
    else:
        logger.debug('Could not identify compile command; using default.')
    return compilecmd


def strip_and_compare_files(base_file, submission_file):
    """ Compare two source files with a contextual diff, return \
    result as a list of lines. """
    logger = setup_logger()
    base_file_contents_no_comments = remove_cpp_comments(base_file)
    contents_no_comments = remove_cpp_comments(submission_file)
    diff = ""
    if contents_no_comments and base_file_contents_no_comments:
        base_file_contents_no_comments = base_file_contents_no_comments.split(
            '\n'
        )
        contents_no_comments = contents_no_comments.split('\n')
        diff = difflib.context_diff(
            base_file_contents_no_comments,
            contents_no_comments,
            'Base',
            'Submission',
            n=3,
        )
    else:
        logger.error('Cannot perform contextual diff.')
    return list(diff)


def format_check(file):
    """ Use clang-format to check file's format against the \
    Google C++ style.
    Throws ChildProcessError if clang-format is not executable."""
    # logger = setup_logger()
    # clang-format
    cmd = 'clang-format'
    cmd_options = '-style=Google --Werror'
    cmd = cmd + ' ' + cmd_options + ' ' + file
    # logger.debug('clang format: %s', cmd)
    proc = subprocess.run(
        [cmd],
        capture_output=True,
        shell=True,
        timeout=10,
        check=False,
        text=True,
    )
    if proc.returncode != 0:
        raise ChildProcessError('clang-format is not executable')
    correct_format = str(proc.stdout).split('\n')
    with open(file, encoding='UTF-8') as file_handle:
        original_format = file_handle.read().split('\n')
    diff = difflib.context_diff(
        original_format,
        correct_format,
        'Student Submission (Yours)',
        'Correct Format',
        n=3,
    )
    # print('\n'.join(list(diff)))
    return list(diff)


def lint_check(file, tidy_options=None, skip_compile_cmd=False):
    """ Use clang-tidy to lint the file. Options for clang-tidy \
    defined in the function. """
    logger = setup_logger()
    # clang-tidy
    if not skip_compile_cmd:
        logger.debug(
            'Checking for makefile in %s',
            os.path.dirname(os.path.realpath(file)),
        )
        compilecmd = makefile_get_compilecmd(
            os.path.dirname(os.path.realpath(file))
        )
        logger.debug('Makefile reported compile commmand as %s', compilecmd)
    if not skip_compile_cmd and compilecmd:
        logger.debug('Using compile command %s', compilecmd)
        create_clang_compile_commands_db(
            remove_existing_db=True, compile_cmd=compilecmd
        )
        logger.debug('Created clang compile command db.')
    elif not skip_compile_cmd and not compilecmd:
        logger.debug('Creating compile commands.')
        create_clang_compile_commands_db(files=[file], remove_existing_db=True)
    cmd = 'clang-tidy'
    if not tidy_options:
        logger.debug('Using default tidy options.')
        cmd_options = r'-checks="-*,google-*, modernize-*, \
        readability-*,cppcoreguidelines-*,\
        -google-build-using-namespace,\
        -google-readability-todo,\
        -modernize-use-trailing-return-type,\
        -cppcoreguidelines-avoid-magic-numbers,\
        -readability-magic-numbers,\
        -cppcoreguidelines-pro-type-union-access,\
        -cppcoreguidelines-pro-bounds-constant-array-index"'
        # cmd_options = '-checks="*"'
    else:
        cmd_options = tidy_options
    cmd = cmd + ' ' + cmd_options + ' ' + file
    if skip_compile_cmd:
        cmd = cmd + ' -- -std=c++17'
    logger.debug('Tidy command %s', cmd)
    proc = subprocess.run(
        [cmd],
        capture_output=True,
        shell=True,
        timeout=60,
        check=False,
        text=True,
    )
    linter_warnings = str(proc.stdout).split('\n')
    linter_warnings = [line for line in linter_warnings if line != '']
    return linter_warnings


def glob_cc_src_files(target_dir='.'):
    """Recurse through the target_dir and find all the .cc files."""
    return glob.glob(os.path.join(target_dir, '**/*.cc'), recursive=True)


def glob_h_src_files(target_dir='.'):
    """Recurse through the target_dir and find all the .h files."""
    return glob.glob(os.path.join(target_dir, '**/*.h'), recursive=True)


def glob_all_src_files(target_dir='.'):
    """Recurse through the target_dir and find all the .cc and .h files."""
    files = glob_cc_src_files(target_dir) + glob_h_src_files(target_dir)
    return files


if __name__ == '__main__':
    mk_makefiles('/tmp/foo', cfg)
