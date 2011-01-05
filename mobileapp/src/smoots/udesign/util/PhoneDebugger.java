package smoots.udesign.util;

import android.util.Log;

/**
 * Util Class for the purpose of debugging.
 *
 * @author Sun
 */
public class PhoneDebugger {	
	private static boolean DEBUG = true;
	
	/**
	 * Add the error exception to the Android log
	 * @param tag Tag for the log
	 * @param e Exception error
	 */
	public static void debug(String tag, Exception e) {
		if (DEBUG == true) {
			Log.d(tag, e.getMessage());
		}
	}
}
