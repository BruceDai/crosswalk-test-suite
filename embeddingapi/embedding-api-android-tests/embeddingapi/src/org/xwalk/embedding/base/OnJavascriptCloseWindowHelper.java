// Copyright (c) 2014 Intel Corporation. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

package org.xwalk.embedding.base;

import org.chromium.content.browser.test.util.CallbackHelper;

public class OnJavascriptCloseWindowHelper extends CallbackHelper {
    private boolean mCalled = false;

    public boolean getCalled() {
        assert getCallCount() > 0;
        return mCalled;
    }

    public void notifyCalled(boolean called) {
        mCalled = called;
        notifyCalled();
    }
}
