package smoots.udesign.settings;

public interface OnSettingsChangedListener {
	String getCurrentIP();
	int getCurrentPort();
	
	void onSettingsChanged(String ipAddr, int port);
}
