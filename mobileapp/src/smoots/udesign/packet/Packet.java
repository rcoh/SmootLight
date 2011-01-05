package smoots.udesign.packet;

/**
 * Interface for the Packet that contains phone input to the server. 
 */
public interface Packet {
	/**
	 * Return JSON formatted packet that can be sent through socket.
	 * @return JSON formatted packet
	 */
	public String packetToText();
}
