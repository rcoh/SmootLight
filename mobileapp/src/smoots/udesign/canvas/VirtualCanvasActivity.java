package smoots.udesign.canvas;

import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.HashMap;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

import smoots.udesign.accelerometer.AccelerometerListener;
import smoots.udesign.accelerometer.AccelerometerManager;
import smoots.udesign.canvas.CanvasView.CanvasThread;
import smoots.udesign.colorpicker.ColorPickerDialog;
import smoots.udesign.colorpicker.ColorPickerListener;
import smoots.udesign.io.ClientWriter;
import smoots.udesign.main.R;
import smoots.udesign.main.R.id;
import smoots.udesign.main.R.layout;
import smoots.udesign.main.R.menu;
import smoots.udesign.packet.MotionType;
import smoots.udesign.packet.Packet;
import smoots.udesign.packet.PhoneToServerPacket;
import smoots.udesign.settings.OnSettingsChangedListener;
import smoots.udesign.settings.SettingsDialog;
import smoots.udesign.util.PhoneDebugger;
import android.app.Activity;
import android.content.Context;
import android.graphics.Color;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.widget.TextView;
import android.widget.Toast;

public class VirtualCanvasActivity extends Activity implements
		AccelerometerListener, ColorPickerListener, OnSettingsChangedListener {

	private static final String TAG = "VirtualCanvasActivity";
	private static Context CONTEXT;
	private static String DEFAULT_IP = "18.244.3.179";
	// private static String DEFAULT_IP = "10.189.17.92";
	private int DEFAULT_PORT = 20120;
	private static final long TIME_INTERVAL_THRESHOLD = 500;

	// ACCELEROMETER INFO
	private HashMap<String, Float> sendData;

	// SENDER INFO
	private ClientWriter writerThread;
	private String ipAddr;
	private int port;
	private BlockingQueue<Packet> packetQ;
	private boolean isSending = false;
	private long timeKeeper;

	// COLOR PICKER INFO
	private static final String BRIGHTNESS_PREFERENCE_KEY = "brightness";
	private static final String COLOR_PREFERENCE_KEY = "color";

	// VIRTUALIZATION VIEW AND THREAD
	private CanvasThread mCanvasThread;
	private CanvasView mCanvasView;

	// -------------------------
	// ACTIVITY ATTRIBUTES
	// -------------------------
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		initControls();

		if (savedInstanceState == null) {
			// we were just launched: set up a new canvas
			mCanvasThread.setState(CanvasThread.STATE_RUNNING);
			Log.w(this.getClass().getName(), "SIS is null");
		} else {
			// resume a saved canvas
			mCanvasThread.restoreState(savedInstanceState);
			Log.w(this.getClass().getName(), "SIS is nonnull");
		}
	}

	private void initControls() {
		setContentView(R.layout.canvaslo);
		CONTEXT = this;

		this.mCanvasView = (CanvasView) findViewById(R.id.canvas_view);
		this.mCanvasThread = mCanvasView.getThread();
		this.mCanvasView.setTextView((TextView) findViewById(R.id.status_text));

		this.ipAddr = DEFAULT_IP;
		this.port = DEFAULT_PORT;
		this.packetQ = new LinkedBlockingQueue<Packet>();

		this.sendData = new HashMap<String, Float>();
		this.sendData.put("color", (float) 0);

		// txtSendStatus = (TextView) findViewById(R.id.txtSendStatus);
		this.timeKeeper = System.currentTimeMillis();
	}

	protected void onPause() {
		super.onPause();
		this.mCanvasView.getThread().pause(); // pause canvas when Activity pauses
	}

	protected void onResume() {
		super.onResume();
		if (AccelerometerManager.isSupported()) {
			AccelerometerManager.startListening(this);
		}
	}

	protected void onDestroy() {
		super.onDestroy();
		if (AccelerometerManager.isListening()) {
			AccelerometerManager.stopListening();
		}
	}

	protected void onSaveInstanceState(Bundle outState) {
		// just have the View's thread save its state into our Bundle
		super.onSaveInstanceState(outState);
		this.mCanvasThread.saveState(outState);
		Log.w(this.getClass().getName(), "SaveInstanceState called");
	}

	public boolean onCreateOptionsMenu(Menu menu) {
		MenuInflater inflater = getMenuInflater();
		inflater.inflate(R.menu.canvas_menu, menu);
		return true;
	}

	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle item selection
		switch (item.getItemId()) {
		case R.id.send:
			toggleSending();

			/*
			 * // pass Sending Intent to PacketSender Intent toPacketSender =
			 * new Intent(this, PacketSenderService.class); //
			 * toPacketSender.putExtra("ipAddr", this.ipAddr); //
			 * toPacketSender.putExtra("port", this.port);
			 * toPacketSender.putExtra("ipAddr", "18.244.6.28");
			 * toPacketSender.putExtra("port", "20120"); if (!isSending) {
			 * startService(toPacketSender); isSending = true; } else {
			 * stopService(toPacketSender); isSending = false; }
			 */
			return true;

		case R.id.color_picker:
			int color = PreferenceManager.getDefaultSharedPreferences(
					VirtualCanvasActivity.this).getInt(COLOR_PREFERENCE_KEY,
					Color.WHITE);
			new ColorPickerDialog(VirtualCanvasActivity.this,
					VirtualCanvasActivity.this, color).show();
			return true;

		// case R.id.effect_picker:
		// return true;

		case R.id.settings:
			new SettingsDialog(VirtualCanvasActivity.this,
					VirtualCanvasActivity.this).show();
			return true;

		default:
			return super.onOptionsItemSelected(item);
		}
	}

	// -------------------------
	// STATIC
	// -------------------------
	public static Context getContext() {
		return CONTEXT;
	}

	// -------------------------
	// HELPERS
	// -------------------------
	private void toggleSending() {
		// Toast.makeText(this, this.ipAddr + ":" + Integer.toString(this.port),
		// Toast.LENGTH_SHORT).show();

		if (!this.isSending) {
			Log.d(TAG, "Start Sending");
			Socket socket = null;
			try {
				socket = new Socket(this.ipAddr, this.port);
				this.writerThread = new ClientWriter(this.packetQ, socket);
				this.writerThread.setRunning(true);
				this.writerThread.start();
				this.isSending = true;
			} catch (UnknownHostException e) {
				PhoneDebugger.debug(TAG, e);
				Toast.makeText(this, "Socket Not Created", Toast.LENGTH_SHORT)
						.show();
			} catch (IOException e) {
				PhoneDebugger.debug(TAG, e);
				Toast.makeText(this, "Socket Not Created", Toast.LENGTH_SHORT)
						.show();
			}
		} else {
			Log.d(TAG, "Stop Sending");

			this.writerThread.setRunning(false);
			this.writerThread.interrupt();

			Toast.makeText(this, "Writer stopped", Toast.LENGTH_SHORT).show();
			this.isSending = false;
		}

		// String serverAddr = "www.google.com";
		// int serverPort =
		// Integer.parseInt(((EditText)findViewById(R.id.settings_port)).getText().toString());

		/*
		 * String serverAddr = this.ipAddr; //String serverAddr =
		 * ((EditText)findViewById(R.id.settings_ip)).getText().toString(); int
		 * serverPort = this.port; Toast.makeText(this, serverAddr,
		 * Toast.LENGTH_LONG).show();
		 * 
		 * Socket socket = null; try { socket = new Socket(serverAddr,
		 * serverPort); //socket = new Socket(serverAddr, 80); } catch
		 * (Exception e) { printScr("Exception!"); printScr(e.getMessage());
		 * printScr(e.getStackTrace().toString()); } printScr("connecting");
		 * String message = new JSONObject(this.xyzPhonePos).toString();
		 * printScr(message); try { PrintWriter out = new
		 * PrintWriter(socket.getOutputStream(), true); out.println(message);
		 * printScr("sent"); } catch (Exception e) {
		 * printScr("exception occurs"); } finally { printScr("close socket");
		 * socket.close(); }
		 */
	}

	// -------------------------
	// LISTENERS
	// -------------------------
	/**
	 * onAccelerationChanged callback function
	 */
	public void onAccelerationChanged(float x, float y, float z) {
		Log.d(TAG, "accerleration changed to" + Float.toString(x) + ", "
				+ Float.toString(y) + ", " + Float.toString(z));
		this.sendData.put("xPos", x);
		this.sendData.put("yPos", y);
		this.sendData.put("zPos", z);
		// ((TextView) findViewById(R.id.x)).setText(String.valueOf(x));
		// ((TextView) findViewById(R.id.y)).setText(String.valueOf(y));
		// ((TextView) findViewById(R.id.z)).setText(String.valueOf(z));

		this.mCanvasThread.updatePixelVelocity(x, y, z);

		if (this.isSending == true
				&& System.currentTimeMillis() - this.timeKeeper > TIME_INTERVAL_THRESHOLD) {
			// Toast.makeText(this, "Send" + Float.toString(x) + ", " +
			// Float.toString(y) + ", " + Float.toString(z),
			// Toast.LENGTH_SHORT).show();
			this.timeKeeper = System.currentTimeMillis();
			
			this.packetQ.add(new PhoneToServerPacket(
					MotionType.MOVE, 
					this.sendData.get("xPos"), 
					this.sendData.get("yPos"),
					this.sendData.get("color"))
			);
		}
	}

	/**
	 * onShake callback
	 */
	public void onShake(float force) {
		Toast.makeText(this, "Phone shaked : " + force, Toast.LENGTH_LONG)
				.show();

		this.packetQ.add(new PhoneToServerPacket(2, 0, 0, this.sendData.get("color")));
	}

	/**
	 * onColorChanged callback function
	 */
	public void onColorChanged(int color) {
		// txtSendStatus.setText(Integer.toString(color));
		this.sendData.put("color", (float) color);

		this.mCanvasThread.updatePixelColor(color);
		// Button colorBtn = (Button) findViewById(R.id.color_button);
		// colorBtn.getBackground()
		// .setColorFilter(color, PorterDuff.Mode.MULTIPLY);
	}

	/**
	 * onSettingsChanged callback
	 */
	public void onSettingsChanged(String ipAddr, int port) {
		this.ipAddr = ipAddr;
		this.port = port;
	}

	public String getCurrentIP() {
		return this.ipAddr;
	}

	public int getCurrentPort() {
		return this.port;
	}

}