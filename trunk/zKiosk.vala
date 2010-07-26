/**
* Preliminary file for Vala port of zombieKiosk
*
*/
using Gtk;
using WebKit;

	public class zKiosk : GLib.Object
	{
		private Builder builder;
		private WebView web_view;
		
		public zKiosk () throws Error
		{
		this.builder = new Builder();
		builder.add_from_file ("zkiosk-ui.glade");
		builder.connect_signals(this);
		var MainWindow = builder.get_object("window1") as Window;
		var Browser = builder.get_object("Browser") as ScrolledWindow;
		this.web_view = new WebView();
		Browser.add(this.web_view);
		int maxx = 1024;
		int maxy = 768;
		MainWindow.set_size_request(maxx,maxy);
		MainWindow.show_all();
		}
	
		// windows only [CCode (cname = "G_MODULE_EXPORT about")]
		[CCode (instance_pos = -1)]
		public void about (Button sender) {
			web_view.go_back();
			stdout.printf("almost Works!\n");
		}
	}
	
	int main (string[] args)
	{
		Gtk.init(ref args);
		try {
			var app = new zKiosk();
			Gtk.main ();
		} catch (Error e) {
			stderr.printf ("Error: %s\n", e.message);
			return 1;
		}
		return 0;
	}