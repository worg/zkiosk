[indent = 4]

/*
*       Copyright 2011 Hiram Jeronimo Perez "wøRg" <worg@linuxmail.org>
*
*      This program is free software; you can redistribute it and/or modify
*      it under the terms of the GNU General Public License as published by
*      the Free Software Foundation; either version 3 of the License, or
*      (at your option) any later version.
*
*      This program is distributed in the hope that it will be useful,
*      but WITHOUT ANY WARRANTY; without even the implied warranty of
*      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*      GNU General Public License for more details.
*
*      You should have received a copy of the GNU General Public License
*      along with this program; if not, write to the Free Software
*      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
*      MA 02110-1301, USA.
*       
*/

uses
    Gtk
    WebKit
    
URL : string
cfgPath : string

    
class zKiosk : GLib.Object
    builder     : private Builder
    webView     : private WebView
    localPath   : private string
    userAgent   : private string
    webSettings : private WebSettings
    mainWindow  : Window
    browser     : ScrolledWindow
    aboutDlg    : AboutDialog
    
    construct (ref args : unowned array of string)
        localPath = Path.get_dirname (args[0])
        builder = new Builder ()
        UIPath : string = Path.build_filename(localPath, "zkiosk.ui")
        try
            builder.add_from_file (UIPath)
        except e : Error
            main_quit()
            error ("%s\nDoh, la interfáz no se pudo cargar", e.message)
        
        mainWindow = builder.get_object ("window") as Window
        browser = builder.get_object ("Browser") as ScrolledWindow
        aboutDlg = builder.get_object ("aboutb") as AboutDialog
        webView = new WebView ()
        
        browser.add(webView)
        
        //Cambiamos el user-agent (por cuestión estética y de identificación para estadísticas)
        webSettings = webView.get_settings ();
        userAgent = webSettings.user_agent
        userAgent = userAgent.replace (" Safari/"," zombieKiosk/DrunkEngine Safari/")
        webSettings.user_agent = userAgent
        webSettings.enable_plugins = false
        
        //Mostramos la ventana en pantalla completa
        maxy : int = Gdk.Screen.height ()
        maxx : int = Gdk.Screen.width ()
        mainWindow.set_size_request (maxx, maxy)
        
        //Mostramos los elementos de la ventana
        mainWindow.show_all ()
        
        //Conectamos las señales de la interfáz a las funciones
        builder.connect_signals (this)
        webView.navigation_policy_decision_requested.connect (uriChk)
        
    [CCode (cname = "G_MODULE_EXPORT about")] [CCode (instance_pos = -1)]
    def about (sender : Button)
        aboutDlg.set_url_hook (linkHdl); // Evita abrir los links del cuadro de dialogo
        aboutDlg.run ()
        aboutDlg.hide ()
    
    def linkHdl (sender : AboutDialog, url : string)
        url = ""
        
    [CCode (cname = "G_MODULE_EXPORT back")] [CCode (instance_pos = -1)]
    def back (sender : Button)
        webView.go_back ()
    
    [CCode (cname = "G_MODULE_EXPORT fwd")] [CCode (instance_pos = -1)]
    def fwd (sender : Button)
        webView.go_forward ()
        
    [CCode (cname = "G_MODULE_EXPORT home")] [CCode (instance_pos = -1)]
    def home (sender : Button?)
        webView.load_uri (URL)
        
    [CCode (cname = "G_MODULE_EXPORT refresh")] [CCode (instance_pos = -1)]
    def refresh (sender : Button)
        webView.reload ()
        
    [CCode (cname = "G_MODULE_EXPORT noclose")] [CCode (instance_pos = -1)]
    def noclose (sender : Button) : bool
        return true
    
    def uriChk(view : WebView, frame : WebFrame, req : NetworkRequest, act : WebNavigationAction, pold : WebPolicyDecision) : bool
        uri : string = req.get_uri ()
        
        if ("http://azul.bnct.ipn.mx" in uri)
            print uri
            frame.load_uri(URL)
        return false

init
    Gtk.init  (ref args)
    get_config ()
    app : zKiosk
    GLib.Process.spawn_command_line_sync("xsetroot -cursor_name left_ptr")
    app = new zKiosk (ref args)
    app.home(null)
    Gtk.main ()

def get_config()
    cfgFile : KeyFile = new KeyFile ()
    cfgPath = Environment. get_home_dir ()
    
    cfgPath = Path.build_filename (cfgPath, ".zkioskrc")
    
    try
        cfgFile.load_from_file (cfgPath, KeyFileFlags.NONE);
        URL = cfgFile.get_value ("Biblio", "web")
    except e : KeyFileError
        warning (e.message)
    except e : FileError
        warning ("%s\nDoh, la configuración no existe\ncreando una por defecto", e.message)
        cfgFile.set_string ("Biblio", "web", "http://148.204.48.96/uhtbin/webcat/")
        rawCfg : string = cfgFile.to_data (null)
        
        try
            FileUtils.set_contents (cfgPath, rawCfg, rawCfg.length)
        except e : Error
            warning (e.message)
    
