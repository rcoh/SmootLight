package smoots.udesign.main;

import smoots.udesign.canvas.VirtualCanvasActivity;
import android.app.TabActivity;
import android.content.Intent;
import android.content.res.Resources;
import android.os.Bundle;
import android.widget.TabHost;

public class UDesignTabWidget extends TabActivity {
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);

		Resources res = getResources(); // Resource object to get Drawables
		TabHost tabHost = getTabHost(); // The activity TabHost
		TabHost.TabSpec spec; // Reusable TabSpec for each tab
		Intent intent; // Reusable Intent for each tab

		// Create an Intent to launch an Activity for the tab (to be reused)
		intent = new Intent().setClass(this, VirtualCanvasActivity.class);
		// Initialize a TabSpec for each tab and add it to the TabHost
		spec = tabHost.newTabSpec("canvas").setIndicator("Canvas",
				res.getDrawable(R.drawable.ic_tab_canvas)).setContent(intent);
		tabHost.addTab(spec);

		// Do the same for the other tabs
		/*
		 * intent = new Intent().setClass(this, ColorActivity.class); spec =
		 * tabHost.newTabSpec("color").setIndicator("Color",
		 * res.getDrawable(R.drawable.ic_tab_color)) .setContent(intent);
		 * tabHost.addTab(spec);
		 */

		intent = new Intent().setClass(this, InteractionsActivity.class);
		spec = tabHost.newTabSpec("interactions").setIndicator("Interactions",
				res.getDrawable(R.drawable.ic_tab_interactions)).setContent(
				intent);
		tabHost.addTab(spec);

		tabHost.setCurrentTab(0);
	}
}