#!/usr/bin/env python
#
# Copyright (c) 2016 Intel Corporation.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of works must retain the original copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the original copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of Intel Corporation nor the names of its contributors
#   may be used to endorse or promote products derived from this work without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY INTEL CORPORATION "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL INTEL CORPORATION BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors:
#         Li, Hao <haox.li@intel.com>

import os
import sys
import logging
import glob
import commands
import subprocess
import time
import csv
from optparse import OptionParser

SCRIPT_PATH = os.path.realpath(__file__)
ROOT_PATH = os.path.dirname(SCRIPT_PATH)
LOG = None
LOG_LEVEL = logging.DEBUG
WORK_STAT_SHEET = []

class ColorFormatter(logging.Formatter):

    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)

    def format(self, record):
        red, green, yellow, blue = range(4)
        colors = {'INFO': green, 'DEBUG': blue,
                  'WARNING': yellow, 'ERROR': red}
        msg = record.msg
        if msg[0] == "+":
            msg = "\33[01m" + msg[1:] + "\033[0m"
        elif msg[0] == "=":
            msg = "\33[07m" + msg + "\033[0m"
        levelname = record.levelname
        if levelname in colors:
            msg_color = "\033[0;%dm" % (
                31 + colors[levelname]) + msg + "\033[0m"
            record.msg = msg_color

        return logging.Formatter.format(self, record)

def doCMD(cmd):
    # Do not need handle timeout in this short script, let tool do it
    print ">>>> \"%s\"" % cmd
    output = []
    cmd_return_code = 1
    cmd_proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    while True:
        output_line = cmd_proc.stdout.readline().strip("\r\n")
        cmd_return_code = cmd_proc.poll()
        if output_line == '' and cmd_return_code is not None:
            break
        sys.stdout.write("%s\n" % output_line)
        sys.stdout.flush()
        output.append(output_line)

    return (cmd_return_code, output)

def check_repo(repo):
    if(os.path.exists(repo)):
        #update
        os.chdir(repo)
        cmd = "git pull"
        (return_code, output) = doCMD(cmd)
        if return_code == 0:
            print ">>>> %s success to update." % repo
        else:
            print ">>>> %s fail to update." % repo
    else:
        LOG.error(">>>> %s does not exist, exit ..." % repo)
        sys.exit(1) 


def statistics(repo):
    os.chdir(repo)
    cmd = "git log --pretty=format:'%H' "
    if PARAMETERS.since:
        cmd = cmd + "--since '%s' " % PARAMETERS.since
    if PARAMETERS.until:
        cmd = cmd + "--until '%s' " % PARAMETERS.until
    if PARAMETERS.author:
        cmd = cmd + "--author '%s' " % PARAMETERS.author

    (return_code, output) = doCMD(cmd)
    for line in output:
        commitlog = os.popen("git log %s --stat -1 " % line)
        logarr = list(commitlog)
        #eg. Merge pull request
        if "Merge:" in str(logarr[1]):
            continue                
        #eg. Author: Li Hao <haox.li@intel.com>\n
        commit_author = logarr[1].strip("\n").split("Author:")[1].strip()
        #eg. Date:   Thu Jan 21 15:49:13 2016 +0800\n
        timearr = logarr[2].strip("\n").split("Date:")[1].strip().split()
        #eg. Jan-21-2016
        commit_date = str(timearr[1]) + "-" + str(timearr[2]) + "-" + str(timearr[4])
        #eg. Impacted tests(approved): new 0, update 1, delete 0
        test_new = ""
        test_update = ""
        test_delete = ""
        for ut in logarr[3:-1]:
            utstr = ut.lower()
            if utstr.find("new") > -1 and utstr.find("update") > -1 and utstr.find("delete") > -1:
                impactedtest = utstr.strip("\n").split(":")[1].strip().split(",")
                for impacted in impactedtest:
                    ut_value = "0"
                    item = impacted.strip().split()
                    if len(item) > 1:
                        ut_value = item[1]
                    if impacted.find("new") > -1:
                        test_new = ut_value
                    elif impacted.find("update") > -1:
                        test_update = ut_value
                    elif impacted.find("delete") > -1:
                        test_delete = ut_value
        #eg.  1 file changed, 1 insertion(+), 1 deletion(-)\n
        changesarr = logarr[-1].strip("\n").split(",")
        commit_file_changed = "0"
        commit_code_insertion = "0"
        commit_code_deletion = "0"
        for change in changesarr:
            change_value = change.strip().split()[0]
            if change.find("files changed") > -1:
                commit_file_changed = change_value
            elif change.find("insertion") > -1:
                commit_code_insertion = change_value
            elif change.find("deletion") > -1:
                commit_code_deletion = change_value
        commitarr = [line, commit_author, commit_date, test_new, test_update, test_delete, commit_file_changed, commit_code_insertion, commit_code_deletion]
        WORK_STAT_SHEET.append(commitarr)
        print commitarr

def make_csv(commit_data, csv_path):
    LOG.info("General: %s" % csv_path)
    writer = csv.writer(file(csv_path, 'wb'))
    writer.writerow(['Commit Id',
                     'Author',
                     'Date',
                     'New Case',
                     'Update Case',
                     'Delete Case',
                     'File Changed',
                     'Code Insertion',
                     'Code Deletion'])
    for commit in commit_data:
        writer.writerow([commit[0],
                         commit[1],
                         commit[2],
                         commit[3],
                         commit[4],
                         commit[5],
                         commit[6],
                         commit[7],
                         commit[8]])


def main():
    global LOG, ROOT_DIR
    LOG = logging.getLogger("log")
    LOG.setLevel(LOG_LEVEL)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(LOG_LEVEL)
    stream_formatter = ColorFormatter("[%(asctime)s] %(message)s")
    stream_handler.setFormatter(stream_formatter)
    LOG.addHandler(stream_handler)

    ROOT_DIR = os.getcwd()

    try:
        usage = "Usage: ./git_stat.py -r <repo path> [-s <since>] [-u <until>] [-a <author>] [-o <output>]"
        opts_parser = OptionParser(usage=usage)
        opts_parser.add_option(
            "-r",
            "--repo",
            dest="repo",
            help="Git repo which need stat")
        opts_parser.add_option(
            "-s",
            "--since",
            dest="since",
            help="Show commits after the date")
        opts_parser.add_option(
            "-u",
            "--until",
            dest="until",
            help="Show commits before the date")
        opts_parser.add_option(
            "-a",
            "--author",
            dest="author",
            help="Show commits by author")
        opts_parser.add_option(
            "-o",
            "--output",
            dest="output",
            help="Specify an output file")

        if len(sys.argv) == 1:
            sys.argv.append("-h")

        global PARAMETERS
        (PARAMETERS, args) = opts_parser.parse_args(sys.argv[1:])

        #check_repo(PARAMETERS.repo)
        statistics(PARAMETERS.repo)
        csv_file = ""
        if not PARAMETERS.output:
            csv_file = os.path.join(ROOT_PATH, "work_stat_%s.csv" % time.strftime('%Y-%m-%d',time.localtime(time.time())))
        else:
            csv_file = PARAMETERS.output
        make_csv(WORK_STAT_SHEET, csv_file)

    except Exception as e:
        LOG.error(">>>> Got wrong options: %s, exit ..." % e)
        sys.exit(1)


if __name__ == '__main__':
    main()
