#!/usr/bin/env python
#
# Copyright (c) 2015 Intel Corporation.
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
#         Yun, Liu<yunx.liu@intel.com>

import unittest
import os
import comm
import shutil
import urllib2
import re
from bs4 import BeautifulSoup
import zipfile
import json


class TestCrosswalkApptoolsFunctions(unittest.TestCase):

    def test_create_package_basic(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.clear("org.xwalk.test")
        os.mkdir("org.xwalk.test")
        os.chdir('org.xwalk.test')
        cmd = comm.HOST_PREFIX + comm.PackTools + \
            "crosswalk-pkg --platforms=windows --crosswalk=" + comm.XwalkPath + comm.windowsCrosswalk + " " + comm.ConstPath + "/../testapp/create_package_basic/"
        (return_code, output) = comm.getstatusoutput(cmd)
        apks = os.listdir(os.getcwd())
        apkLength = 0
        for i in range(len(apks)):
            if apks[i].endswith(".msi"):
                apkLength = apkLength + 1
        comm.clear("org.xwalk.test")
        self.assertEquals(return_code, 0)
        self.assertIn("candle", output[0])
        self.assertIn("light", output[0])
        self.assertNotIn("target android", output[0])
        self.assertEquals(apkLength, 1)

    def test_create_package_missing_icon_startUrl(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.clear("org.xwalk.test")
        os.mkdir("org.xwalk.test")
        os.chdir('org.xwalk.test')
        cmd = comm.HOST_PREFIX + comm.PackTools + \
            "crosswalk-pkg --platforms=windows --crosswalk=" + comm.XwalkPath + comm.windowsCrosswalk + " " + comm.ConstPath + "/../testapp/create_package_missing_icon_startUrl/"
        return_code = os.system(cmd)
        apks = os.listdir(os.getcwd())
        apkLength = 0
        for i in range(len(apks)):
            if apks[i].endswith(".msi"):
                apkLength = apkLength + 1
        comm.clear("org.xwalk.test")
        self.assertEquals(return_code, 0)
        self.assertEquals(apkLength, 1)

    def test_create_package_canary(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.clear("org.xwalk.test")
        os.mkdir("org.xwalk.test")
        os.chdir('org.xwalk.test')
        cmd = comm.HOST_PREFIX + comm.PackTools + \
            "crosswalk-pkg --platforms=windows --crosswalk=canary " + comm.ConstPath + "/../testapp/create_package_basic/"
        (return_code, output) = comm.getstatusoutput(cmd)
        version = comm.check_crosswalk_version(self, "canary")
        crosswalk = 'crosswalk-{}.zip'.format(version)
        apks = os.listdir(os.getcwd())
        apkLength = 0
        for i in range(len(apks)):
            if apks[i].endswith(".msi"):
                apkLength = apkLength + 1
        comm.clear("org.xwalk.test")
        if not comm.cachedir:
            namelist = os.listdir(os.getcwd())
        else:
            newcachedir = os.environ.get('CROSSWALK_APP_TOOLS_CACHE_DIR')
            os.chdir(newcachedir)
            namelist = os.listdir(os.getcwd())
        self.assertEquals(return_code, 0)
        self.assertIn("canary", output[0])
        self.assertIn(version, output[0])
        self.assertIn(crosswalk, namelist)
        self.assertEquals(apkLength, 1)

    def test_create_package_download_crosswalk(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.clear("org.xwalk.test")
        if os.path.exists("crosswalk-17.45.421.0.zip"):
            os.remove("crosswalk-17.45.421.0.zip")
        os.mkdir("org.xwalk.test")
        os.chdir('org.xwalk.test')
        cmd = comm.HOST_PREFIX + comm.PackTools + \
            "crosswalk-pkg --platforms=windows --crosswalk=17.45.421.0 " + comm.ConstPath + "/../testapp/create_package_basic/"
        (return_code, output) = comm.getstatusoutput(cmd)
        apks = os.listdir(os.getcwd())
        apkLength = 0
        for i in range(len(apks)):
            if apks[i].endswith(".msi"):
                apkLength = apkLength + 1
        comm.clear("org.xwalk.test")
        namelist = os.listdir(os.getcwd())
        self.assertEquals(return_code, 0)
        self.assertIn("crosswalk-17.45.421.0.zip", namelist)
        self.assertIn("17.45.421.0", output[0])
        self.assertEquals(apkLength, 1)

    def test_create_package_crosswalkdir(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.clear("org.xwalk.test")
        os.mkdir("org.xwalk.test")
        crosswalkzip = zipfile.ZipFile(comm.XwalkPath + comm.windowsCrosswalk,'r')
        for file in crosswalkzip.namelist():
            crosswalkzip.extract(file, r'.')
        crosswalkzip.close()
        os.chdir('org.xwalk.test')
        cmd = comm.HOST_PREFIX + comm.PackTools + \
            "crosswalk-pkg --platforms=windows --crosswalk=" + comm.XwalkPath + comm.windowsCrosswalk[:comm.windowsCrosswalk.index(".zip")] + "/ " + comm.ConstPath + "/../testapp/create_package_basic/"
        return_code = os.system(cmd)
        apks = os.listdir(os.getcwd())
        apkLength = 0
        for i in range(len(apks)):
            if apks[i].endswith(".msi"):
                apkLength = apkLength + 1
        comm.clear("org.xwalk.test")
        shutil.rmtree(comm.windowsCrosswalk[:comm.windowsCrosswalk.index(".zip")])
        self.assertEquals(return_code, 0)
        self.assertEquals(apkLength, 1)

    def test_create_package_without_channel(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.clear("org.xwalk.test")
        os.mkdir("org.xwalk.test")
        os.chdir('org.xwalk.test')
        cmd = comm.HOST_PREFIX + comm.PackTools + \
            "crosswalk-pkg --platforms=windows " + comm.ConstPath + "/../testapp/create_package_basic/"
        (return_code, output) = comm.getstatusoutput(cmd)
        version = comm.check_crosswalk_version(self, "stable")
        crosswalk = 'crosswalk-{}.zip'.format(version)
        apks = os.listdir(os.getcwd())
        apkLength = 0
        for i in range(len(apks)):
            if apks[i].endswith(".msi"):
                apkLength = apkLength + 1
        comm.clear("org.xwalk.test")
        if not comm.cachedir:
            namelist = os.listdir(os.getcwd())
        else:
            newcachedir = os.environ.get('CROSSWALK_APP_TOOLS_CACHE_DIR')
            os.chdir(newcachedir)
            namelist = os.listdir(os.getcwd())
        self.assertEquals(return_code, 0)
        self.assertIn("stable", output[0])
        self.assertIn(version, output[0])
        self.assertIn(crosswalk, namelist)
        self.assertEquals(apkLength, 1)

    def test_create_package_manifest(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.clear("org.xwalk.test")
        os.mkdir("org.xwalk.test")
        if os.path.exists(comm.ConstPath + "/../testapp/start_url/manifest.json"):
            os.remove(comm.ConstPath + "/../testapp/start_url/manifest.json")
        os.chdir('org.xwalk.test')
        cmd = comm.HOST_PREFIX + comm.PackTools + \
            "crosswalk-pkg --platforms=windows --crosswalk=" + comm.XwalkPath + comm.windowsCrosswalk + " --manifest=org.xwalk.test " + comm.ConstPath + "/../testapp/start_url/"
        return_code = os.system(cmd)
        with open(comm.ConstPath + "/../testapp/start_url/manifest.json") as json_file:
            data = json.load(json_file)
        apks = os.listdir(os.getcwd())
        apkLength = 0
        for i in range(len(apks)):
            if apks[i].endswith(".msi"):
                apkLength = apkLength + 1
        comm.clear("org.xwalk.test")
        os.remove(comm.ConstPath + "/../testapp/start_url/manifest.json")
        self.assertEquals(return_code, 0)
        self.assertEquals(data['xwalk_package_id'].strip(os.linesep), "org.xwalk.test")
        self.assertEquals(apkLength, 1)

    def test_create_package_reading_manifest(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.clear("org.xwalk.test")
        os.mkdir("org.xwalk.test")
        if os.path.exists(comm.ConstPath + "/../testapp/start_url/manifest.json"):
            os.remove(comm.ConstPath + "/../testapp/start_url/manifest.json")
        os.chdir('org.xwalk.test')
        cmd = comm.HOST_PREFIX + comm.PackTools + \
            "crosswalk-pkg --platforms=windows --crosswalk=" + comm.XwalkPath + comm.windowsCrosswalk + " --manifest '{ \"xwalk_package_id\": \"org.xwalk.test\", \"start_url\": \"start.html\" }' " + comm.ConstPath + "/../testapp/start_url/"
        return_code = os.system(cmd)
        with open(comm.ConstPath + "/../testapp/start_url/manifest.json") as json_file:
            data = json.load(json_file)
        apks = os.listdir(os.getcwd())
        apkLength = 0
        for i in range(len(apks)):
            if apks[i].endswith(".msi"):
                apkLength = apkLength + 1
        comm.clear("org.xwalk.test")
        os.remove(comm.ConstPath + "/../testapp/start_url/manifest.json")
        self.assertEquals(return_code, 0)
        self.assertEquals(data['xwalk_package_id'].strip(os.linesep), "org.xwalk.test")
        self.assertEquals(apkLength, 1)

    def test_create_package_keep(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.clear("org.xwalk.test")
        os.mkdir("org.xwalk.test")
        os.chdir('org.xwalk.test')
        cmd = comm.HOST_PREFIX + comm.PackTools + \
            "crosswalk-pkg --platforms=windows --crosswalk=" + comm.XwalkPath + comm.windowsCrosswalk + " --keep " + comm.ConstPath + "/../testapp/create_package_basic/"
        (return_code, output) = comm.getstatusoutput(cmd)
        apks = os.listdir(os.getcwd())
        apkLength = 0
        for i in range(len(apks)):
            if apks[i].endswith(".msi"):
                apkLength = apkLength + 1
        projectDir = output[0].split(" * " + os.linesep)[-1].split(' ')[-1].strip(os.linesep)
        comm.clear("org.xwalk.test")
        self.assertEquals(return_code, 0)
        self.assertEquals(apkLength, 1)
        self.assertIn("app", os.listdir(projectDir))
        self.assertIn("prj", os.listdir(projectDir))

    def test_create_package_k(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.clear("org.xwalk.test")
        os.mkdir("org.xwalk.test")
        os.chdir('org.xwalk.test')
        cmd = comm.HOST_PREFIX + comm.PackTools + \
            "crosswalk-pkg --platforms=windows --crosswalk=" + comm.XwalkPath + comm.windowsCrosswalk + " -k " + comm.ConstPath + "/../testapp/create_package_basic/"
        (return_code, output) = comm.getstatusoutput(cmd)
        apks = os.listdir(os.getcwd())
        apkLength = 0
        for i in range(len(apks)):
            if apks[i].endswith(".msi"):
                apkLength = apkLength + 1
        projectDir = output[0].split(" * " + os.linesep)[-1].split(' ')[-1].strip(os.linesep)
        comm.clear("org.xwalk.test")
        self.assertEquals(return_code, 0)
        self.assertEquals(apkLength, 1)
        self.assertIn("app", os.listdir(projectDir))
        self.assertIn("prj", os.listdir(projectDir))

if __name__ == '__main__':
    unittest.main()
