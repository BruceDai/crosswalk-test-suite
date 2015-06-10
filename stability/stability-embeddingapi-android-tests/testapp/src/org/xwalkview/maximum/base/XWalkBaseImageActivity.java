// Copyright (c) 2014 Intel Corporation. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

package org.xwalkview.maximum.base;

import java.util.ArrayList;
import java.util.List;

import org.xwalkview.maximum.app.R;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.CheckBox;
import android.widget.Toast;

public class XWalkBaseImageActivity extends Activity {
	protected List<CheckBox> checkBoxList = new ArrayList<CheckBox>();

    protected Button mDetailInfoButton;
    protected StringBuffer message;
    protected TextView textDes;

    protected int url_index = 0;
    protected int view_num = 0;
    protected int count_num = 0;
    protected int change_num = 0;
    protected RelativeLayout root;
    protected RelativeLayout view_root;
    protected Button mAddViewsButton;
    protected Button mExitViewsButton;
    protected TextView textResultTextView;
    protected EditText views_num_text;

    //CheckBox for URL
    protected CheckBox cb_flickr;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
    	super.onCreate(savedInstanceState);
        setContentView(R.layout.view_image);

        root = (RelativeLayout) findViewById(R.id.view_image);
        view_root = (RelativeLayout) findViewById(R.id.view_root);
        textDes = (TextView)findViewById(R.id.xwalk_des);
        textDes.setText("This sample demonstrates Create/destroy many xwalkview at same time to load webpages with image contents.");
        
        textResultTextView = (TextView)findViewById(R.id.result_show);

        views_num_text = (EditText) findViewById(R.id.views_num);

        cb_flickr = (CheckBox) findViewById(R.id.cb_flickr);
        checkBoxList.add(cb_flickr);


        for(CheckBox checkBox : checkBoxList) {
        	checkBox.setOnCheckedChangeListener(listener);
        }

        mAddViewsButton = (Button) findViewById(R.id.run_add);
        mExitViewsButton = (Button) findViewById(R.id.run_exit);
    }

    protected void showDetailInfo(final Context context) {
        mDetailInfoButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new  AlertDialog.Builder(context)
                .setTitle("Info" )
                .setMessage(message.toString())
                .setPositiveButton("confirm" ,  null )
                .show();
            }
        });
    }

    CompoundButton.OnCheckedChangeListener listener = new CompoundButton.OnCheckedChangeListener() {  

        @Override  
        public void onCheckedChanged(CompoundButton buttonView,  
                boolean isChecked) {
            CheckBox box = (CheckBox) buttonView;  
            if(box.isChecked()) {
            	checkBoxList.add(box);
            } else {
            	if(checkBoxList.size() <= 1) {
            		Toast.makeText(getApplicationContext(),  
                            "At least one url checkbox should be Selected", 
                            Toast.LENGTH_LONG).show();
            		box.setChecked(true);
            		return;
            	}
            	checkBoxList.remove(box);
            }

        }  
    };
}
