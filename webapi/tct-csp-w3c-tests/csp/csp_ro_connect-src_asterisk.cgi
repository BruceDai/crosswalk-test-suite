#!/bin/sh
echo "Content-Security-Policy-Report-Only: connect-src *"
echo "X-Content-Security-Policy-Report-Only: connect-src *"
echo "X-WebKit-CSP-Report-Only: connect-src *"
echo
echo '<!DOCTYPE html>

<!--
Copyright (c) 2013 Samsung Electronics Co., Ltd.

Licensed under the Apache License, Version 2.0 (the License);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Authors:
        Ran, Wang <ran22.wang@samsung.com>
-->

<html>
  <head>
    <title>CSP Test: csp_ro_connect-src_asterisk</title>
    <link rel="author" title="Samsung" href="http://www.Samsung.com"/>
    <link rel="help" href="http://www.w3.org/TR/2012/CR-CSP-20121115/#connect-src"/>
    <meta name="flags" content=""/>
    <meta name="assert" content="connect-src *"/>
    <meta charset="utf-8"/>
    <script src="../resources/testharness.js"></script>
    <script src="../resources/testharnessreport.js"></script>
  </head>
  <body>
    <div id="log"></div>
    <script>
        test(function() {
            var xhr = new XMLHttpRequest();
            try {
                xhr.open("GET", "support/csp.js");
            } catch(e) {
                assert_unreached("should not reach here, got exception: "+e.message);
            }
        }, document.title + "_allowed");

        test(function() {
            var xhr = new XMLHttpRequest();
            try {
                xhr.open("GET", "http://www.w3.org");
            } catch(e) {
                assert_unreached("should not reach here, got exception: "+e.message);
            }
        }, document.title + "_allowed_ext");

        function log123(message) {
            var client = new XMLHttpRequest();
            client.open("POST", "http://127.0.0.1:8000/log123");
            client.send(message);
        }
    </script>
  </body>
</html> '
