// Copyright (c) 2014 Intel Corporation. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

package org.xwalkview.stability.app;


import java.util.ArrayList;
import java.util.List;

import org.xwalkview.stability.base.XWalkBaseVideoActivity;
import android.text.TextUtils;
import android.view.Gravity;
import android.view.View;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;

public class VideoWebViewsActivity extends XWalkBaseVideoActivity {
    private List<String> idList = new ArrayList<String>();

    @Override
    protected void onXWalkReady() {
        textDes.setText("This sample demonstrates the feasibility to create and destroy many WebViews at same time to load webpages with playing video.");
        mAddViewsButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int max_num = view_num;
                if(!TextUtils.isEmpty(views_num_text.getText())){
                    change_num = Integer.valueOf(views_num_text.getText().toString());
                    max_num = max_num + change_num;
                    int len = checkBoxList.size();
                    for(int i = view_num; i < max_num; i++) {
                        if (url_index >= len) {
                            url_index = 0;
                        }
                        WebView webView = new WebView(VideoWebViewsActivity.this);
                        webView.setId(i);
                        webView.setWebViewClient(new TestWebViewClientBase());
                        webView.getSettings().setJavaScriptEnabled(true);
                        webView.loadUrl(checkBoxList.get(url_index).getText().toString());
                        url_index++;

                        mAddViewsButton.setClickable(false);
                        FrameLayout.LayoutParams params = new FrameLayout.LayoutParams(view_root.getWidth() - i * 10, view_root.getHeight() - i * 10);
                        params.gravity = Gravity.CENTER;
                        view_root.addView(webView, params);
                    }
                    view_num = view_num + change_num;
                }
            }
        });

        mExitViewsButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.exit(0);
            }
        });
        setContentView(root);
    }

    class TestWebViewClientBase extends WebViewClient {
        @Override
        public void onPageFinished(WebView view, String url) {
            String idStr = String.valueOf(view.getId());
            if(!idList.contains(idStr)){
                idList.add(idStr);
                count_num++;
                if(count_num == view_num) {
                    mAddViewsButton.setClickable(true);
                }
                textResultTextView.setText(String.valueOf(count_num));
            }

            super.onPageFinished(view, url);
        }
    }
}
