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
""" Check student's submission; requires the main file and the
    template file from the original repository. """
# pexpect documentation
#  https://pexpect.readthedocs.io/en/stable/index.html

# ex.
# .action/solution_check_p1.py  part-1 asgt

import io
import logging
import math
import sys
import os
import re
import pexpect
from assessment import csv_solution_check_make
from logger import setup_logger

import lab_config as cfg

def regex_it(s):
    combine_white_space_regex = re.compile(r"\s+")
    s = combine_white_space_regex.sub(" ", s).strip()
    s = s.replace(' ', '\\s+').replace('\n', '\\s+')
    return f'\\s*{s}\\s*'


def run_p1(binary):
    """Run part-1"""
    logger = setup_logger()
    status = []
    error_values = ()
    values = (
        ('-5', '-5 ml = -1.0144 tsp  = -0.338135 tbsp  = -0.169067 oz  = -0.0211334 cups'),
        ('-0.123', '-0.123 ml = -0.0249544 tsp  = -0.00831812 tbsp  = -0.00415906 oz  = -0.000519882 cups'),
        ('-1312.56', '-1312.56 ml = -266.293 tsp  = -88.7645 tbsp  = -44.3822 oz  = -5.54778 cups'),
        ('0', '0 ml = 0 tsp  = 0 tbsp  = 0 oz  = 0 cups'),
        ('5', '5 ml = 1.0144 tsp  = 0.338135 tbsp  = 0.169067 oz  = 0.0211334 cups'),
        ('3.356', '3.356 ml = 0.680868 tsp  = 0.226956 tbsp  = 0.113478 oz  = 0.0141848 cups'),
        ('1312.56', '1312.56 ml = 266.293 tsp  = 88.7645 tbsp  = 44.3822 oz  = 5.54778 cups'),
    )
        

    for index, val in enumerate(error_values):
        test_number = index + 1
        logger.info('Test %d - %s', test_number, val)
        rv = _run_p1_error(binary, val)
        if not rv:
            logger.error("Did not receive expected response for test %d.", test_number)
        status.append(rv)
    
    for index, val in enumerate(values):
        test_number = len(error_values) + index + 1
        logger.info('Test %d - %s', test_number, val)
        rv = _run_p1(binary, val)
        if not rv:
            logger.error("Did not receive expected response for test %d.", test_number)
        status.append(rv)
    return status

def _run_p1_error(binary, values):
    raise NotImplementedError

def _run_p1(binary, values):
    """The actual test with the expected input and output"""
    logger = setup_logger()
    status = False
    proc = pexpect.spawn(binary, timeout=1)
    # proc.logfile = sys.stdout.buffer
    # values = list(map(str, values))
    with io.BytesIO() as log_stream:
        proc.logfile = log_stream
        try:
            proc.expect(
                r'(?i)\s*Enter\s+ml.?\s*(\.?)\s*'
            )
        except (pexpect.exceptions.TIMEOUT, pexpect.exceptions.EOF) as exception:
            logger.error('Could not find expected output.')
            logger.error('Expected "Enter ml: "')
            logger.error('Your output: "%s"', log_stream.getvalue().decode('utf-8'))
            logger.debug("%s", str(exception))
            logger.debug(str(proc))
            return status
        proc.sendline(values[0])
        
        try:
            expected_output = values[1]
            expected_output_regex = regex_it(expected_output)
            proc.expect(
                fr'(?i){expected_output_regex}'
            )
        except (pexpect.exceptions.TIMEOUT, pexpect.exceptions.EOF) as exception:
            logger.error('Could not find expected output.')
            logger.error(f'Expected "{expected_output}"')
            logger.error('Your output: "%s"', log_stream.getvalue().decode('utf-8'))
            logger.debug("%s", str(exception))
            logger.debug(str(proc))
            return status
        
        proc.expect(pexpect.EOF)
        proc.close()
        if proc.exitstatus == 0:
            status = True
        else:
            logger.error("Expected: zero exit code.")
            logger.error(f'Exit code was {proc.exitstatus}.')
            logger.error("Program returned non-zero, but zero is required")
            logger.error('Your output: "%s"', log_stream.getvalue().decode('utf-8'))
    
    return status

def run_p2(binary):
    """Run part-2"""
    logger = setup_logger()
    status = []
    error_values = ()
    values = (
        ('first_guess_win_prompts', '42', '42'),
        ('first_guess_win_prompts', '100', '100'),
        ('second_guess_win_prompts', '42', '10', '42'),
        ('second_guess_win_prompts', '42', '50', '42'),
        ('second_guess_lose_prompts', '42', '10', '15'),
        ('second_guess_lose_prompts', '42', '50', '45'),
    )

    for index, val in enumerate(error_values):
        test_number = index + 1
        logger.info('Test %d - %s', test_number, val)
        rv = _run_p2_error(binary, val)
        if not rv:
            logger.error("Did not receive expected response for test %d.", test_number)
        status.append(rv)
    
    for index, val in enumerate(values):
        test_number = len(error_values) + index + 1
        logger.info('Test %d - %s', test_number, val)
        rv = _run_p2(binary, val)
        if not rv:
            logger.error("Did not receive expected response for test %d.", test_number)
        status.append(rv)
    return status
    

def _run_p2_error(binary, values):
    raise NotImplementedError

def _run_p2(binary, values):
    """The actual test with the expected input and output"""
    logger = setup_logger()
    status = False
    proc = pexpect.spawn(binary, timeout=1)
    # proc.logfile = sys.stdout.buffer
    # values = list(map(str, values))
    first_guess_win_prompts = (
        "Player 1, enter the secret number:",
        "Player 2, enter your first guess:",
        "Correct, you win!",
    )
    second_guess_win_prompts = (
        "Player 1, enter the secret number:",
        "Player 2, enter your first guess:",
        # Too high or Too low
        "Player 2, enter your second guess:",
        "Correct, you win!",
    )
    second_guess_lose_prompts = (
        "Player 1, enter the secret number:",
        "Player 2, enter your first guess:",
        # Too high or Too low
        "Player 2, enter your second guess:",
        "Incorrect, the secret number was {}, you lose.",
    )
    
    prompts = locals()[values[0]]
    guess_msg = None
    if len(prompts) > 3 and int(values[1]) > int(values[2]):
        guess_msg = 'Too low'
    elif len(prompts) > 3 and int(values[1]) <= int(values[2]):
        guess_msg = 'Too high'
    
    with io.BytesIO() as log_stream:
        proc.logfile = log_stream
        for i, p in enumerate(prompts):
            if len(prompts) > 3 and i == 2:
                p_regex = regex_it(f'{guess_msg}\n{p}')
            elif values[0] == 'second_guess_lose_prompts' and i == 3:
                p = p.format(values[1])
                p_regex = regex_it(p)
            else:
                p_regex = regex_it(p)       
            try:
                proc.expect(
                    fr'(?i){p_regex}'
                )
            except (pexpect.exceptions.TIMEOUT, pexpect.exceptions.EOF) as exception:
                logger.error('Could not find expected output.')
                logger.error(f'Expected "{p}"')
                logger.error('Your output: "%s"', log_stream.getvalue().decode('utf-8'))
                logger.debug("%s", str(exception))
                logger.debug(str(proc))
                return status
                
            if i+1 < len(values):
                proc.sendline(values[i+1])
        # try:
        #     expected_output_regex = regex_it(expected_output)
        #     proc.expect(
        #         fr'(?i){expected_output_regex}'
        #     )
        # except (pexpect.exceptions.TIMEOUT, pexpect.exceptions.EOF) as exception:
        #     logger.error('Could not find expected output.')
        #     logger.error(f'Expected "{expected_output}"')
        #     logger.error('Your output: "%s"', log_stream.getvalue().decode('utf-8'))
        #     logger.debug("%s", str(exception))
        #     logger.debug(str(proc))
        #     return status
        
        proc.expect(pexpect.EOF)
        proc.close()
        if proc.exitstatus == 0:
            status = True
        else:
            logger.error("Expected: zero exit code.")
            logger.error(f'Exit code was {proc.exitstatus}.')
            logger.error("Program returned non-zero, but zero is required")
            logger.error('Your output: "%s"', log_stream.getvalue().decode('utf-8'))
    
    return status

if __name__ == '__main__':
    cwd = os.getcwd()
    repo_name = os.path.basename(cwd)
    td = sys.argv[1]

    if sys.argv[1] == 'part-1':
        part_config = cfg.lab['parts'][0]
        _program_name = part_config['target']
        _files = part_config['src'].split() + part_config['header'].split()
        _do_format_check = part_config['do_format_check']
        _do_lint_check = part_config['do_lint_check']
        _do_unit_tests = part_config['do_unit_tests']
        _tidy_options = part_config['tidy_opts']
        _skip_compile_cmd = part_config['skip_compile_cmd']
        # There needs to be some magic here to figure out which due date to use.
        _lab_due_date = cfg.lab['mon_duedate'].isoformat()
        _run_func = locals()[part_config['test_main']]
    elif sys.argv[1] == 'part-2':
        part_config = cfg.lab['parts'][1]
        _program_name = part_config['target']
        _files = part_config['src'].split() + part_config['header'].split()
        _do_format_check = part_config['do_format_check']
        _do_lint_check = part_config['do_lint_check']
        _do_unit_tests = part_config['do_unit_tests']
        _tidy_options = part_config['tidy_opts']
        _skip_compile_cmd = part_config['skip_compile_cmd']
        # There needs to be some magic here to figure out which due date to use.
        _lab_due_date = cfg.lab['mon_duedate'].isoformat()
        _run_func = locals()[part_config['test_main']]
    else:
        print(f'Error: {sys.argv[0]} no match.')
        sys.exit(1)
    # Execute the solution check
    csv_solution_check_make(
        csv_key=repo_name, target_directory=td, program_name=_program_name, run=_run_func, files=_files, do_format_check=_do_format_check, do_lint_check=_do_lint_check, do_unit_tests=_do_unit_tests, tidy_options=_tidy_options, skip_compile_cmd=_skip_compile_cmd, lab_due_date=_lab_due_date
    )
