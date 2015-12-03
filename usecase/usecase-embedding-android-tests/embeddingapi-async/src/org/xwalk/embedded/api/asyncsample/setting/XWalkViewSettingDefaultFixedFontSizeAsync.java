package org.xwalk.embedded.api.asyncsample.setting;

import android.app.AlertDialog;
import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import org.xwalk.core.XWalkInitializer;
import org.xwalk.core.XWalkView;
import org.xwalk.embedded.api.asyncsample.R;

public class XWalkViewSettingDefaultFixedFontSizeAsync extends Activity implements XWalkInitializer.XWalkInitListener {

    public final static String FIXED_FONT_6 = "Fixed Font 6";

    public final static String FIXED_FONT_50 = "Fixed Font 50";

    private XWalkView mXWalkView;
    private TextView mMessage;
    private Button mButton;
    private XWalkInitializer mXWalkInitializer;

    public final static String MESSAGE_TITLE = "Fixed Font Size: ";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        mXWalkInitializer = new XWalkInitializer(this, this);
        mXWalkInitializer.initAsync();
    }

    @Override
    public void onXWalkInitCancelled() {

    }

    @Override
    public void onXWalkInitStarted() {

    }

    @Override
    public void onXWalkInitFailed() {

    }

    @Override
    public void onXWalkInitCompleted() {
        setContentView(R.layout.activity_xwalk_view_setting_default_fixed_font_size_async);
        mXWalkView = (XWalkView) findViewById(R.id.xwalk_view);
        mMessage = (TextView) findViewById(R.id.message_tv);
        mButton = (Button) findViewById(R.id.switch_text_zoom);
        mButton.setText(FIXED_FONT_6);

        StringBuffer mess = new StringBuffer();
        mess.append("Test Purpose: \n\n")
                .append("Sets the default fixed font size. The default is 13." +
                        "param size a non-negative integer between 1 and 72.\n\n")
                .append("Expected Result:\n\n")
                .append("Test passes, if you click 'Font 50', text font size will be changed bigger.");
        new  AlertDialog.Builder(this)
                .setTitle("Info")
                .setMessage(mess.toString())
                .setPositiveButton("confirm", null)
                .show();

        mXWalkView.load("file:///android_asset/text_zoom.html", null);
        mButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (FIXED_FONT_6.equals(mButton.getText())) {
                    mButton.setText(FIXED_FONT_50);
                    mXWalkView.getSettings().setDefaultFixedFontSize(6);
                    mMessage.setText(MESSAGE_TITLE + mXWalkView.getSettings().getDefaultFixedFontSize());
                    mXWalkView.load("file:///android_asset/text_zoom.html", null);
                } else {
                    mButton.setText(FIXED_FONT_6);
                    mXWalkView.getSettings().setDefaultFixedFontSize(50);
                    mMessage.setText(MESSAGE_TITLE + mXWalkView.getSettings().getDefaultFixedFontSize());
                    mXWalkView.load("file:///android_asset/text_zoom.html", null);
                }
            }
        });

        mMessage.setText(MESSAGE_TITLE + mXWalkView.getSettings().getDefaultFixedFontSize());
    }
}
