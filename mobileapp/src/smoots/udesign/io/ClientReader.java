package smoots.udesign.io;

import java.io.IOException;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

import smoots.udesign.accelerometer.AccelerometerListener;
import smoots.udesign.accelerometer.AccelerometerManager;
import smoots.udesign.packet.MotionType;
import smoots.udesign.packet.Packet;
import smoots.udesign.packet.PhoneToServerPacket;

/**
 * ClientReader is in charge of receiving data from the view, parsing
 * the textual protocol into executable packets, and send the packets to the
 * processor. 1 per client.
 */
public class ClientReader implements Runnable, AccelerometerListener {
	private BlockingQueue<Packet> accPktQ;
	private BlockingQueue<Packet> packetQ;
	private boolean stopped;

	/**
	 * Initialize the queue of accelerometer data.
	 * 
	 * @param packetQ The queue of packets 
	 */
	public ClientReader(BlockingQueue<Packet> packetQ) {
		this.accPktQ = new LinkedBlockingQueue<Packet>();
		this.packetQ = packetQ;
		
//		if (AccelerometerManager.isSupported()) {
			AccelerometerManager.startListening(this);
//		}
	}

	/**
	 * From the queue, extract a packet of Accelerometer data and forward it to the
	 * processor, which will execute the packet accordingly.
	 * 
	 * @throws InterruptedException 
	 */
	public void forward() throws InterruptedException {
		packetQ.add(accPktQ.take());
	}

	/**
	 * runtime method, do the following actions in sequence:
	 * 		receive -> forward.
	 */
	public void run() {
		while (true) {
			try {
				Thread.sleep(1000);
				forward(); // to the processor
			} catch (InterruptedException e) {
				break;
			}
		}
	}

	public void onAccelerationChanged(float x, float y, float z) {
		// CHANGE ACCELEROMETER READINGS TO LIGHT LOCATIONS
		// ...
		
		accPktQ.add(new PhoneToServerPacket(MotionType.MOVE, (int)x, (int)y, (int)z));
	}

	public void onShake(float force) {
		// TODO Auto-generated method stub
		
	}

}
