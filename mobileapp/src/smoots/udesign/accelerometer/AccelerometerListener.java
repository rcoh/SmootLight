package smoots.udesign.accelerometer;

/**
 * An interface designating an Activity as an Accelerometer Listener, which
 * implements behaviors which happen as Accelerometer detects chagnes.
 * 
 * @author Sun
 * 
 */
public interface AccelerometerListener {

	public void onAccelerationChanged(float x, float y, float z);

	public void onShake(float force);

}
