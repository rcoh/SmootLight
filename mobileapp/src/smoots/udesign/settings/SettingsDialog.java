package smoots.udesign.settings;

import smoots.udesign.main.R;
import android.app.Dialog;
import android.content.Context;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class SettingsDialog extends Dialog {

	private final OnSettingsChangedListener mListener;
	private Button okButton;

	public SettingsDialog(Context context, OnSettingsChangedListener listener) {
		super(context);

		mListener = listener;
	}

	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);

		setContentView(R.layout.settings);
		setTitle("Host Settings");
		
		// PREPARE IP AND PORT.
		((EditText) findViewById(R.id.settings_ip)).setText(mListener.getCurrentIP());
		((EditText) findViewById(R.id.settings_port)).setText(Integer.toString(mListener.getCurrentPort()));
		
		// PREPARE BUTTON
		this.okButton = (Button) this.findViewById(R.id.settings_ok);
		this.okButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				String ipAddr = ((EditText) findViewById(R.id.settings_ip)).getText().toString();
				int port = Integer.parseInt(((EditText) findViewById(R.id.settings_port)).getText().toString());
				
				mListener.onSettingsChanged(ipAddr, port);
				dismiss();
			}
		});
	}

}
