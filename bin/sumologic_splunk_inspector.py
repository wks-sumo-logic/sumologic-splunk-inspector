#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sumologic doctor, analyzing a system files and usage for ingestion/integration with sumologic

Usage:
    $ python sumologic_splunk_inspector [ options ]

Style:
    Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html

    @name           sumologic_splunk_inspector
    @version        1.0.00
    @author-name    Wayne Schmidt
    @author-email   wschmidt@sumologic.com
    @license-name   GNU GPL
    @license-url    http://www.gnu.org/licenses/gpl.html
"""

__version__ = 1.00
__author__ = "Wayne Schmidt (wschmidt@sumologic.com)"

import argparse
import configparser
import datetime
import json
import os
import shutil
import re
import sys
import subprocess
import tarfile
import requests

sys.dont_write_bytecode = 1

PARSER = argparse.ArgumentParser(description="""

This script acts like the local doctor for existing systems to help
clients assess how their systems are performing, by collecting both
commands and files from target systems and pushing them to SumoLogic.

""")

PARSER.add_argument('-w', metavar='<weburl>', dest='weburl', help='weburl')

PARSER.add_argument('-s', metavar='<source>', default='localhost', dest='source', help='set source')
PARSER.add_argument('-t', metavar='<type>', default='splunk', dest='type', help='set type')


PARSER.add_argument('-u', metavar='<user>', dest='username', help='set username')
PARSER.add_argument('-p', metavar='<pass>', dest='password', help='set password')

PARSER.add_argument('-f', metavar='<list>', dest='list', action='append', help='set file list')
PARSER.add_argument('-r', metavar='<cmds>', dest='cmds', action='append', help='set commands')

PARSER.add_argument('-o', metavar='<output>', dest='outputdir', help='set outputdir')
PARSER.add_argument('-c', metavar='<cfgfile>', dest='cfgfile', help='use job file')

ARGS = PARSER.parse_args()

if ARGS.cfgfile:
    CFGFILE = os.path.abspath(ARGS.cfgfile)
    CONFIG = configparser.ConfigParser()
    CONFIG.read(CFGFILE)
    USERNAME = json.loads(CONFIG.get("Default", "USERNAME"))
    os.environ['USERNAME'] = USERNAME
    PASSWORD = json.loads(CONFIG.get("Default", "PASSWORD"))
    os.environ['PASSWORD'] = PASSWORD
    SUMOHTTP = json.loads(CONFIG.get("Default", "SUMOHTTP"))
    os.environ['SUMOHTTP'] = SUMOHTTP
    SUMOLIST = json.loads(CONFIG.get("Default", "SUMOLIST"))
    SUMOCMDS = json.loads(CONFIG.get("Default", "SUMOCMDS"))
else:
    if ARGS.username:
        os.environ["USERNAME"] = ARGS.username
    if ARGS.password:
        os.environ["PASSWORD"] = ARGS.password
    if ARGS.weburl:
        os.environ["SUMOHTTP"] = ARGS.weburl
    if ARGS.list:
        SUMOLIST = ARGS.list
    if ARGS.cmds:
        SUMOCMDS = ARGS.cmds

SRCTYPE = 'splunk'
SRCNAME = ARGS.source
SRCTAG = SRCTYPE + '_' + SRCNAME

CURRENT = datetime.datetime.now()
DSTAMP = CURRENT.strftime("%Y%m%d")
TSTAMP = CURRENT.strftime("%H%M%S")
LSTAMP = DSTAMP + '.' + TSTAMP

try:
    PASSWORD = os.environ['PASSWORD']
    USERNAME = os.environ['USERNAME']
    SUMOHTTP = os.environ['SUMOHTTP']
except KeyError as myerror:
    print('Environment Variable Not Set :: {} '.format(myerror.args[0]))

def main():
    """
    This will prepare the output and input directories, then connect,
    then extract the data, then persist this into a cache, then upload.
    """

    homedir = os.path.abspath((os.path.join(os.environ['HOME'], 'Downloads')))
    cmddir = '%s/%s/%s/cmd' % (homedir, SRCTAG, DSTAMP)
    cfgdir = '%s/%s/%s/cfg' % (homedir, SRCTAG, DSTAMP)
    logdir = '%s/%s/%s/log' % (homedir, SRCTAG, DSTAMP)
    tardir = '%s/%s/%s/tar' % (homedir, SRCTAG, DSTAMP)
    os.makedirs(tardir, exist_ok=True)
    dirlist = [cmddir, cfgdir, logdir]
    for mydir in dirlist:
        os.makedirs(mydir, exist_ok=True)

    process_files(cfgdir)
    executes_cmds(cmddir)
    build_archive(tardir, dirlist)

def process_files(cfgdir):
    """
    This walks through a list of the files required.
    files can be regular expressions or specific.
    This converts all files within the cache into a single string file
    the originals are kept for future analysis
    """

    targetlist = SUMOLIST
    for targetfile in targetlist:
        srcfile = os.path.abspath(targetfile)
        shutil.copy(srcfile, cfgdir)
        dstfile = os.path.abspath(os.path.join(cfgdir, os.path.basename(srcfile)))
        with open(dstfile, encoding='utf8') as targetfile:
            targetstring = targetfile.read().strip()
            targetstring = targetstring.replace('\n', '')
            print(dstfile)
            upload_remote(targetstring)

def executes_cmds(cmddir):
    """
    This walks through a list of the commands required.
    This converts all command output within the cache into a single string file
    the originals are kept for future analysis
    """

    targetcmds = SUMOCMDS
    for targetcmd in targetcmds:
        cmdoutput = subprocess.Popen(targetcmd, shell=True, \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = cmdoutput.communicate()
        characters = "/`*{}[]()>#+-.!$"
        for character in characters:
            targetcmd = targetcmd.replace(character, '_')
        targetcmd = targetcmd.replace(' ', '')
        targetcmd = re.sub('_{2,}', '_', targetcmd)
        if stderr:
            errfile = os.path.join(cmddir, targetcmd + '.' + DSTAMP + '.' + 'err.txt')
            errfileobj = open(errfile, 'w+')
            errfileobj.write(str(stderr))
        if stdout:
            outfile = os.path.join(cmddir, targetcmd + '.' + DSTAMP + '.' + 'out.txt')
            outfileobj = open(outfile, 'w+')
            outfileobj.write(str(stdout))

def upload_remote(targetstring):
    """
    Upload all of the files in the cache into the remote site
    """
    requestobj = requests.post(SUMOHTTP, data=targetstring.encode('utf-8'), \
        headers={'Content-type': 'text/plain; charset=utf-8'})
    print(requestobj.status_code)

def build_archive(tardir, dirlist):
    """
    Then, build a compresses archive for future use.
    The archive will include the commands as well as the logs of the run.
    """

    tar_name = os.path.join(tardir, SRCTAG + '.' + DSTAMP + '.' + 'tar.gz')
    with tarfile.open(tar_name, "w:gz") as tar_handle:
        for mydir in dirlist:
            for root, _dirs, files in os.walk(mydir):
                for file in files:
                    tar_handle.add(os.path.join(root, file))

if __name__ == '__main__':
    main()
