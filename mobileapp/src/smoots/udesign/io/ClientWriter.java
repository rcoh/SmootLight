package smoots.udesign.io;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.concurrent.BlockingQueue;

import smoots.udesign.packet.Packet;
import smoots.udesign.packet.PhoneToServerPacket;

/**
 * A class in charge of taking packets from queue and parses them into JSON
 * formatted messages and - Send messages to the server.
 */
public class ClientWriter extends Thread {
	private static final String TAG = "ClientWriter";
	private final PrintWriter out;
	private BlockingQueue<Packet> packetQ;
	private boolean mRun = false;

	/**
	 * Constructor that initializes: the output writer, and a packet queue for
	 * sending data.
	 * 
	 * @param clientSocket
	 *            the Socket the Client's going to use.
	 * @throws IOException
	 *             possible during socket i/o
	 */
	public ClientWriter(BlockingQueue<Packet> packetQ, Socket clientSocket)
			throws IOException {
		this.out = new PrintWriter(clientSocket.getOutputStream(), true);
		this.packetQ = packetQ;
	}

	/**
	 * Converting a packet into text form and send it to the server.
	 */
	public void send() {
		Packet pac;
		try {
			pac = this.packetQ.take();
			if (pac != null) {
				this.out.println(pac.packetToText());
			}
			// this.out.println("gosgos1");
		} catch (InterruptedException e) {
			// PhoneDebugger.debug(TAG, e);
		}
	}

	/**
	 * Set the running status of the thread.
	 * 
	 * @param b
	 *            If the thread is running
	 */
	public void setRunning(boolean b) {
		this.mRun = b;
	}

	/**
	 * runtime method, keep sending packets from the queue.
	 */
	public void run() {
		while (this.mRun) {
			this.send();
		}
		this.out.println("end");
	}
}
