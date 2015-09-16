package org.xwalk.embedding.base;

import org.xwalk.core.XWalkView;

import android.app.Activity;
import android.content.Context;
import android.content.res.AssetManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.util.Log;
import android.view.View;

import java.io.IOException;


public class SetLayerTypeXWalkView extends XWalkView {

    public final static String TAG = "SetLayerTypeXWalkView";

    public SetLayerTypeXWalkView(Context context) {
        super(context);
    }

    public SetLayerTypeXWalkView(Context context, Activity activity) {
        super(context, activity);
    }

    public SetLayerTypeXWalkView(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    private MessageListener mListener;

    public interface MessageListener{
        public void onMessageSent(String msg);
    }

    public void setMessageListener(MessageListener listener){
        this.mListener = listener;
    }

    public MessageListener getMessageListener(){
        return this.mListener;
    }

    @Override
    protected void dispatchDraw(Canvas canvas) {
        super.dispatchDraw(canvas);

        String msg = null;
        Log.i(TAG, "+++++++++++++++Canvas Hardware accelerated: " + canvas.isHardwareAccelerated());

        if(!canvas.isHardwareAccelerated()) {

            Paint mGridPaint = new Paint(Paint.LINEAR_TEXT_FLAG);

            AssetManager am = this.getContext().getAssets();

            try {
                Bitmap bm = BitmapFactory.decodeStream(am.open("ic_launcher.png"));
                canvas.drawBitmap(bm, 0, 0, mGridPaint);
            } catch (IOException e) {
                Log.e(TAG, "the bitmap is not found!");
            }
            Log.i(TAG, "------------------------------------DispatchDraw is completed without Hardware accelerated");
            msg = "DispatchDraw is completed without Hardware accelerated changed by setLayerType";
        }else{
            this.setLayerType(View.LAYER_TYPE_SOFTWARE, null);
            Log.i(TAG, "------------------------------------DispatchDraw is completed with Hardware accelerated");
            msg = "DispatchDraw is completed with Hardware accelerated";
        }
        getMessageListener().onMessageSent(msg);
    }
}
