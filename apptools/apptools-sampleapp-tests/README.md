## Introduction

This test suite is for apptools-sampleapp-tests

## Common Precondition

1. The node.js must be functional
2. Install nodeunit: sudo npm install nodeunit -g
3. Download crosswalk-app-tools to apptools-sampleapp-tests/tools, then install npm
  3.1 cd tools, then download source code from https://github.com/crosswalk-project/crosswalk-app-tools
  3.2 Run commands: cd crosswalk-app-tools, then run: npm install
4. The main script is crosswalk-app-tools/src/crosswalk-app. Set environment PATH or invoke with directory
  (Note: On Windows, Need create 'crosswalk-app' env, invoke with 'crosswalk-app-tools/src/crosswalk-app' directory).


## Precondition for AppTools on Android

1. Connect Android devices to your localhost
2. The Android SDK, JDK and apache ant must be functional
3. Environment variable configuration on Android:
  3.1 export ANDROID_HOME=$(dirname $(dirname $(which android)))
  3.2 export CROSSWALK_APP_TOOLS_CACHE_DIR=/path/to/opt/apptools-sampleapp-tests/tools
4. Environment variable configuration on Windows:
  4.1 Set ANDORID_HOME env
  4.2 Set CROSSWALK_APP_TOOLS_CACHE_DIR env to /path/to/opt/apptools-sampleapp-tests/tools


## Precondition for AppTools on Windows

1. Install WiX per https://msdn.microsoft.com/en-us/library/gg513936.aspx (do not forget to add the WiX tools to the windows path environment variable)
2 Download Crosswalk windows binary to the same path with crosswalk-app-tools


## Precondition for AppTools on Deepin

1. The debuild tool, and the Crosswalk runtime must be functional
2. Checkout the deb backend: cd crosswalk-app-tools/node_modules, then download source code from https://github.com/crosswalk-project/crosswalk-app-tools-deb.git crosswalk-app-tools-backend-deb  
3. Install dependencies: cd crosswalk-app-tools-backend-deb, then npm install, and cd ../..  


## Precondition for AppTools on iOS

1. Connect iOS devices to your localhost
2. the Xcode command line tools, and the Xcode iOS SDK 8.1 must be functional
3. Checkout the iOS backend: cd crosswalk-app-tools/node_modules, then download source code from https://github.com/crosswalk-project/crosswalk-app-tools-ios.git crosswalk-app-tools-backend-ios
4. Install dependencies: cd crosswalk-app-tools-backend-ios, then npm install, and cd ../..

## Test Steps

1. unzip apptools-sampleapp-tests<version>.zip -d [testprefix-path]
2. cd [testprefix-path]/opt/apptools-sampleapp-tests/
3. run test case
   testkit-lite -f [testprefix-path]/opt/apptools-sampleapp-tests/tests.xml -M -o [testprefix-path]/opt/apptools-sampleapp-tests/result.xml --comm androidmobile --deviceid=Medfield3C6DFF2E
   --testprefix=[testprefix-path], DEVICE_ID can also be multiple ids like "DEVICE_ID=Medfield3C6DFF2E,Medfield3C6DFF00".
Query device id by command "adb devices -l" in host.

## Authors:

* Liu, Yun <yunx.liu@intel.com>

## LICENSE

Copyright (c) 2015 Intel Corporation.
Except as noted, this software is licensed under BSD-3-Clause License.
Please see the COPYING file for the BSD-3-Clause License.
