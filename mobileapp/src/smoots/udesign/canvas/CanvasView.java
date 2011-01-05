/*
 * Copyright (C) 2007 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package smoots.udesign.canvas;

import android.content.Context;
import android.content.res.Resources;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.AttributeSet;
import android.util.Log;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.widget.TextView;

/**
 * a View that takes accelerometer input and draws for CanvasActivity
 */
public class CanvasView extends SurfaceView implements SurfaceHolder.Callback {
	public class CanvasThread extends Thread {
		// ---------------------
		// CONSTANTS
		// ---------------------
		public static final int PIXEL_RADIUS = 10;
		public static final double TILT_THRESHOLD = 0.5;

		public static final int STATE_PAUSE = 1;
		public static final int STATE_RUNNING = 2;

		// Bundle key constants
		private static final String KEY_DX = "mDX";
		private static final String KEY_DY = "mDY";
		private static final String KEY_X = "mX";
		private static final String KEY_Y = "mY";
		private static final String KEY_COLOR = "mColor";

		// ---------------------
		// MEMBER FIELDS
		// ---------------------
		private Paint mPixelPaint;
		private int mPixelColor = Color.WHITE;

		// Position
		private float CENTER_X;
		private float CENTER_Y;
		private float mX;
		private float mY;
		private boolean justStart = true; // if loop for the 1st time, determine
		// the center of the canvas.
		// Velocity
		private float mDX;
		private float mDY;

		// Color
		private int mColor;

		// Canvas size, will be determined when view is started.
		private int mCanvasHeight = 1;
		private int mCanvasWidth = 1;

		/** Message handler used by thread to interact with TextView */
		private Handler mHandler;

		/** Used to figure out elapsed time between frames */
		private long mLastTime;

		/** The state of the game. One of READY, RUNNING, PAUSE, LOSE, or WIN */
		private int mMode;

		/** Indicate whether the surface has been created & is ready to draw */
		private boolean mRun = false;

		/** Handle to the surface manager object we interact with */
		private SurfaceHolder mSurfaceHolder;

		public CanvasThread(SurfaceHolder surfaceHolder, Context context,
				Handler handler) {
			mContext = context;

			// get handles to some important objects
			this.mSurfaceHolder = surfaceHolder;
			this.mHandler = handler;

			mPixelPaint = new Paint();
			mPixelPaint.setAntiAlias(true);
			mPixelPaint.setStyle(Paint.Style.FILL);
			mPixelPaint.setColor(Color.WHITE);

			// initial show-up of lander (not yet playing)
			this.mX = 0;
			this.mY = 0;
			this.mDX = 0;
			this.mDY = 0;
			this.mColor = Color.WHITE;
		}

		/**
		 * Start the view. Set the pixel's initial position.
		 */
		public void doStart() {
			synchronized (mSurfaceHolder) {
				// pick the center location for the pixel.
				this.mX = mCanvasWidth / 2;
				this.mY = mCanvasHeight / 2;

				this.mLastTime = System.currentTimeMillis() + 100;
				setState(STATE_RUNNING);
			}
		}

		/**
		 * Save canvas state to the provided Bundle.
		 * 
		 * @return Bundle with current state
		 */
		public Bundle saveState(Bundle map) {
			synchronized (mSurfaceHolder) {
				if (map != null) {
					map.putDouble(KEY_X, Double.valueOf(this.mX));
					map.putDouble(KEY_Y, Double.valueOf(this.mY));
					map.putDouble(KEY_DX, Double.valueOf(this.mDX));
					map.putDouble(KEY_DY, Double.valueOf(this.mDY));
					map.putInt(KEY_COLOR, this.mColor);
				}
			}
			return map;
		}

		/**
		 * Restores canvas state from the indicated Bundle.
		 * 
		 * @param savedState
		 *            Bundle with the saved state
		 */
		public synchronized void restoreState(Bundle savedState) {
			synchronized (mSurfaceHolder) {
				setState(STATE_PAUSE);

				this.mX = savedState.getFloat(KEY_X);
				this.mY = savedState.getFloat(KEY_Y);
				this.mDX = savedState.getFloat(KEY_DX);
				this.mDY = savedState.getFloat(KEY_DY);
				this.mColor = savedState.getInt("KEY_COLOR");
			}
		}

		public void run() {
			while (this.mRun) {
				Canvas c = null;
				try {
					c = mSurfaceHolder.lockCanvas(null);
					synchronized (mSurfaceHolder) {
						if (mMode == STATE_RUNNING) {
							updatePhysics();
						}
						doDraw(c);
					}
				} finally {
					if (c != null) {
						// keep states consistent.
						mSurfaceHolder.unlockCanvasAndPost(c);
					}
				}
			}
		}

		/**
		 * Set the thread loop handler.
		 * 
		 * @param b whether the thread is running
		 */
		public void setRunning(boolean b) {
			this.mRun = b;
		}

		public void setState(int mode) {
			synchronized (mSurfaceHolder) {
				setState(mode, null);
			}
		}

		/**
		 * Sets the canvas mode.
		 * 
		 * @param mode
		 *            one of the STATE constants
		 * @param message
		 *            string to add to screen or null
		 */
		public void setState(int mode, CharSequence message) {
			/*
			 * This method optionally can cause a text message to be displayed
			 * to the user when the mode changes. Since the View that actually
			 * renders that text is part of the main View hierarchy and not
			 * owned by this thread, we can't touch the state of that View.
			 * Instead we use a Message + Handler to relay commands to the main
			 * thread, which updates the user-text View.
			 */
			synchronized (mSurfaceHolder) {
				mMode = mode;

				if (mMode == STATE_RUNNING) {
					Message msg = mHandler.obtainMessage();
					Bundle b = new Bundle();
					b.putString("text", "");
					b.putInt("viz", View.INVISIBLE);
					msg.setData(b);
					mHandler.sendMessage(msg);
				} else {
					Resources res = mContext.getResources();
					CharSequence str = "";

					Message msg = mHandler.obtainMessage();
					Bundle b = new Bundle();
					b.putString("text", str.toString());
					b.putInt("viz", View.VISIBLE);
					msg.setData(b);
					mHandler.sendMessage(msg);
				}
			}
		}

		/* Callback invoked when surface dimensions change. */
		public void setSurfaceSize(int width, int height) {
			// synchronized to make sure these all change atomically
			synchronized (mSurfaceHolder) {
				mCanvasWidth = width;
				mCanvasHeight = height;
			}
		}
		
		/**
		 * Pauses the animation.
		 */
		public void pause() {
			synchronized (mSurfaceHolder) {
				if (mMode == STATE_RUNNING)
					setState(STATE_PAUSE);
			}
		}
		
		/**
		 * Resumes from a pause.
		 */
		public void unpause() {
			// Move the real time clock to now
			synchronized (mSurfaceHolder) {
				mLastTime = System.currentTimeMillis() + 100;
			}
			setState(STATE_RUNNING);
		}

		/**
		 * Draws the pixel to the provided Canvas.
		 */
		private void doDraw(Canvas canvas) {
			if (this.justStart) { // initialize pixel position
				Log.d("Canvas", Integer.toString(canvas.getWidth()) + " by "
						+ Integer.toString(canvas.getHeight()));
				this.CENTER_X = canvas.getWidth() / 2;
				this.CENTER_Y = canvas.getHeight() / 2;

				this.mX = this.CENTER_X;
				this.mY = this.CENTER_Y;

				this.justStart = false;
			}

			// Draw the black background.
			this.mPixelPaint.setColor(Color.BLACK);
			canvas.drawPaint(mPixelPaint);

			// Draw pixel.
			this.mPixelPaint.setColor(this.mPixelColor);
			canvas.drawCircle(this.mX, this.mY, PIXEL_RADIUS, this.mPixelPaint);
		}

		/**
		 * Figures the lander state (x, y, fuel, ...) based on the passage of
		 * realtime. Does not invalidate(). Called at the start of draw().
		 * Detects the end-of-game and sets the UI to the next state.
		 */
		private void updatePhysics() {
			long now = System.currentTimeMillis();

			// Do nothing if mLastTime is in the future.
			// This allows the game-start to delay the start of the physics
			// by 100ms or whatever.
			if (mLastTime > now)
				return;

			double elapsed = (now - mLastTime) / 1000.0;

			/*
			 * // Base accelerations -- 0 for x, gravity for y double ddx = 0.0;
			 * double ddy = elapsed;
			 * 
			 * double dxOld = mDX; double dyOld = mDY;
			 * 
			 * // figure speeds for the end of the period mDX += ddx; mDY +=
			 * ddy;
			 * 
			 * // figure position based on average speed during the period mX +=
			 * elapsed * (mDX + dxOld) / 2; mY += elapsed * (mDY + dyOld) / 2;
			 */

			mLastTime = now;
		}

		public void updatePixelColor(int color) {
			this.mPixelColor = color;
		}

		public void updatePixelVelocity(float x, float y, float z) {
			this.mX = (float) (this.CENTER_X - x / 10. * this.CENTER_X);
			this.mY = (float) (this.CENTER_Y + y / 10. * this.CENTER_Y);
		}
	}

	/** Handle to application context */
	private Context mContext;

	/** Pointer to the text view to display "Paused.." etc. */
	private TextView mStatusText;

	/** The thread that actually draws the animation */
	private CanvasThread thread;

	public CanvasView(Context context, AttributeSet attrs) {
		super(context, attrs);

		// register our interest in hearing about changes to our surface
		SurfaceHolder holder = getHolder();
		holder.addCallback(this);

		// create thread only; it's started in surfaceCreated()
		thread = new CanvasThread(holder, context, new Handler() {
			@Override
			public void handleMessage(Message m) {
				mStatusText.setVisibility(m.getData().getInt("viz"));
				mStatusText.setText(m.getData().getString("text"));
			}
		});

		setFocusable(true); // make sure we get key events
	}

	/**
	 * Fetches the animation thread corresponding to this LunarView.
	 * 
	 * @return the animation thread
	 */
	public CanvasThread getThread() {
		return thread;
	}

	/**
	 * Standard window-focus override. Notice focus lost so we can pause on
	 * focus lost. e.g. user switches to take a call.
	 */
	public void onWindowFocusChanged(boolean hasWindowFocus) {
		if (!hasWindowFocus)
			thread.pause();
	}

	/**
	 * Installs a pointer to the text view used for messages.
	 */
	public void setTextView(TextView textView) {
		mStatusText = textView;
	}

	/* Callback invoked when the surface dimensions change. */
	public void surfaceChanged(SurfaceHolder holder, int format, int width,
			int height) {
		thread.setSurfaceSize(width, height);
	}

	/*
	 * Callback invoked when the Surface has been created and is ready to be
	 * used.
	 */
	public void surfaceCreated(SurfaceHolder holder) {
		// start the thread here so that we don't busy-wait in run()
		// waiting for the surface to be created
		thread.setRunning(true);
		thread.start();
	}

	/*
	 * Callback invoked when the Surface has been destroyed. Thread needs to stop.
	 */
	public void surfaceDestroyed(SurfaceHolder holder) {
		boolean retry = true;
		thread.setRunning(false);
		while (retry) {
			try {
				thread.join();
				retry = false;
			} catch (InterruptedException e) {
			}
		}
	}
}
