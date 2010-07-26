/**
* Preliminary file for Vala port of zombieKiosk
*
*/
using Gtk;
using WebKit;

//const string WEB = "http://148.204.48.96/uhtbin/webcat/";
const string WEB = "http://whatsmyuseragent.com";
const string THEME = "gtkrc";



	public class zKiosk : GLib.Object
	{
		private Builder builder;
		private WebView web_view;
		

		public zKiosk () throws Error
		{
			this.builder = new Builder();
			builder.add_from_file ("zkiosk-ui.glade");
			builder.connect_signals(this);
			var MainWindow = builder.get_object("window") as Window;
			var Browser = builder.get_object("Browser") as ScrolledWindow;
			this.web_view = new WebView();
			Browser.add(this.web_view);
			var WSettings = web_view.get_settings();
			GLib.Value ua = GLib.Value (typeof(string));
			WSettings.get_property("user-agent", ref ua);
			string useragent = ua.get_string();
			useragent = useragent.replace("en-us","es-mx");
			useragent = useragent.replace(" Safari/"," zombieKiosk/DrunkEngine Safari/");
			ua.set_string(useragent);
			WSettings.set_property("user-agent", ua);
			
			this.web_view.load_uri(WEB);
			rc_reset_styles(MainWindow.get_settings());
			rc_parse(THEME);
			rc_add_default_file(THEME);
			rc_reparse_all();
			MainWindow.fullscreen();
			MainWindow.show_all();
		}
	
		public void openW(Gtk.AboutDialog sender, string url) {}
		
		[CCode (instance_pos = -1)]
		[CCode(cname="G_MODULE_EXPORT about")]
		public void about (Button sender) {
			var About = this.builder.get_object("aboutb") as AboutDialog; //Accesamos al objeto correspondiente al cuadro de dialogo
			About.set_url_hook(openW); // Evita abrir los links en el cuadro de dialogo
			About.run();
			About.hide();
			
		}

		[CCode (instance_pos = -1)]
		[CCode(cname="G_MODULE_EXPORT back")]
		public void back (Button sender) {
			this.web_view.go_back();
		}

		[CCode (instance_pos = -1)]
		[CCode(cname="G_MODULE_EXPORT fwd")]
		public void fwd (Button sender) {
			this.web_view.go_forward();
		}

		[CCode (instance_pos = -1)]
		[CCode(cname="G_MODULE_EXPORT home")]
		public void home (Button sender) {
			web_view.load_uri(WEB);
		}
		
		[CCode (instance_pos = -1)]
		[CCode(cname="G_MODULE_EXPORT refresh")]
		public void refresh (Button sender) {
			this.web_view.reload();
		}

		[CCode (instance_pos = -1)]
		[CCode(cname="G_MODULE_EXPORT noclose")]
		public bool noclose (Button sender) {
			return true;
		}
	}
	
int main (string[] args)
{
	Gtk.init(ref args);
	try {
		var app = new zKiosk();
		GLib.Process.spawn_command_line_sync("xsetroot -cursor_name left_ptr");
		rc_parse(THEME);
		Gtk.main ();
	} catch (Error e) {
		stderr.printf ("Error: %s\n", e.message);
		return 1;
	}
	return 0;
}

