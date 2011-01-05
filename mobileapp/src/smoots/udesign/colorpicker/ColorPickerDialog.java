package smoots.udesign.colorpicker;

import android.app.Dialog;
import android.content.Context;
import android.os.Bundle;
import android.view.Gravity;
import android.widget.LinearLayout;

public class ColorPickerDialog extends Dialog {

	private final ColorPickerListener mListener;
	private final int mInitialColor;

	public ColorPickerDialog(Context context, ColorPickerListener listener, int initialColor) {
		super(context);

		mListener = listener;
		mInitialColor = initialColor;
	}

	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		ColorPickerListener l = new ColorPickerListener() {
			public void onColorChanged(int color) {
				mListener.onColorChanged(color);
				dismiss();
			}
		};

		LinearLayout layout = new LinearLayout(getContext());
		layout.setOrientation(LinearLayout.VERTICAL);
		layout.setGravity(Gravity.CENTER);
		layout.setPadding(10, 10, 10, 10);
		layout.addView(new ColorPickerView(getContext(), l, mInitialColor),
				new LinearLayout.LayoutParams(
						LinearLayout.LayoutParams.WRAP_CONTENT,
						LinearLayout.LayoutParams.WRAP_CONTENT));

		setContentView(layout);
		setTitle("Pick a Color");
	}
}
