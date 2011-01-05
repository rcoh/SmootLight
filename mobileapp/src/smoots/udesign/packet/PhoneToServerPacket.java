package smoots.udesign.packet;

import java.util.HashMap;

import org.json.JSONObject;

/**
 * Packet object from phone to the server.
 */
public class PhoneToServerPacket implements Packet {
	private HashMap<String, Float> packetMap;
	
	public PhoneToServerPacket(int type, float x, float y, float color) {
		this.packetMap = new HashMap<String, Float>();
		this.packetMap.put("type", (float) type);
		this.packetMap.put("x", x);
		this.packetMap.put("y", y);
		this.packetMap.put("color", color);
	}
	
	public String packetToText() {
		return new JSONObject(this.packetMap).toString();
	}
	
}
