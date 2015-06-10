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
import commands


class TestCrosswalkApptoolsFunctions(unittest.TestCase):

    def test_mainactivity_changed_warning(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.create(self)
        os.chdir('org.xwalk.test/prj/android/src/org/xwalk/test')
        fp = open("MainActivity.java", 'r+')
        fp.read().replace("org.xwalk.test", "org.xwalk.test1")
        fp.close()
        os.chdir(comm.XwalkPath + "org.xwalk.test")
        updatecmd = comm.PackTools + "crosswalk-app update"
        updatestatus = commands.getstatusoutput(updatecmd)
        os.chdir('prj/android/src/org/xwalk/test')
        javalist = os.listdir(os.getcwd())
        comm.clear("org.xwalk.test")
        self.assertIn("WARNING: Please port any custom java code to the new MainActivity.java", updatestatus[1])
        self.assertEquals(len(javalist), 1)

    def test_mainactivity_changed_update(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.create(self)
        os.chdir('org.xwalk.test/prj/android/src/org/xwalk/test')
        fp = open("MainActivity.java", 'r+')
        fp.read().replace("org.xwalk.test", "org.xwalk.test1")
        fp.close()
        os.chdir(comm.XwalkPath + "org.xwalk.test")
        updatecmd = comm.PackTools + "crosswalk-app update"
        updatestatus = commands.getstatusoutput(updatecmd)
        comm.clear("org.xwalk.test")
        self.assertEquals(updatestatus[0], 0)

    def test_mainactivity_changed_build(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.create(self)
        os.chdir('org.xwalk.test/prj/android/src/org/xwalk/test')
        fp = open("MainActivity.java", 'r+')
        fp.read().replace("org.xwalk.test", "org.xwalk.test1")
        fp.close()
        os.chdir(comm.XwalkPath + "org.xwalk.test")
        buildcmd = comm.PackTools + "crosswalk-app build"
        buildstatus = commands.getstatusoutput(buildcmd)
        comm.clear("org.xwalk.test")
        self.assertEquals(buildstatus[0], 0)

if __name__ == '__main__':
    unittest.main()
