#!/usr/bin/env python
import gtk
import pygtk
import webkit
import ConfigParser
from os import popen
from sys import path

#Introducimos el valor por default a la configuracion, en caso de que no exista
cfg = ConfigParser.SafeConfigParser({"web": "http://148.204.48.96/uhtbin/webcat", "theme": "gtkrc"})
# Leemos el archivo de configuracion
localpath = path[0]
localpath += '/'
cfg.read([localpath +"config.cfg"])  
#Asignamos los valores de la configuracion a variables para su uso posterior
web = cfg.get("Biblio","web")
theme = cfg.get("Biblio","theme")
	
class Window:
	def __init__(self):
		self.builder = gtk.Builder() 
		self.builder.add_from_file(localpath + 'zkiosk-ui.glade')
		self.window = self.builder.get_object('window1')
		self.Browser = self.builder.get_object('Browser')

		#inicializa el widget del motor de renderizado y lo agrega a la interfaz
		self.webview = webkit.WebView() 
		self.Browser.add(self.webview)
		Settings = self.webview.get_settings()
		Settings.set_property("user-agent","Mozilla/5.0 (X11; U; Linux i686; es-mx) AppleWebKit/531.2+ (KHTML, like Gecko) zombieKiosk/TequilaEngine 0.1.2 Safari/531.2+")
		#cambiando a pantalla completa
		maxx = gtk.gdk.screen_width() 
		maxy = gtk.gdk.screen_height() 
		self.window.set_size_request(maxx,maxy) 
		
		#Parseamos el archivo del estilo visual
		gtk.rc_reset_styles(self.window.get_settings())
		gtk.rc_parse(theme)
		gtk.rc_add_default_file(theme)
		gtk.rc_reparse_all()
		
		self.window.show_all() #mustra los elementos de la ventana
		
		#conectando los botones y eventos de la ventana a las funciones 
		self.builder.connect_signals(self)
		            
	def home(self, widget):
		self.webview.load_uri(web)
				
	def back(self, widget):
		self.webview.go_back()

	def fwd(self, widget):
		self.webview.go_forward()

	def refresh(self, widget):
		self.webview.reload()
		
	def about(self, widget):
		self.window.set_modal(False) #Quita la exclusividad del foco de la ventana principal y permite controlar el cuadro de acerca de..
		self.About=self.builder.get_object('aboutb') #Accesamos al objeto correspondiente a ese dialogo
		
		def openW(widget,url,url2): # Evita abrir el sitio en el cuadro de dialogo acerca de
			print url
		
		gtk.about_dialog_set_url_hook(openW,"") # Evita abrir el sitio en el cuadro de dialogo acerca de
		# Obtenemos los eventos generados
		Response = self.About.run()
		#Si se presiona el boton de cerrar o se cierra el cuadro lo oculta y restaura el foco en la ventana principal
		if Response == gtk.RESPONSE_DELETE_EVENT or Response == gtk.RESPONSE_CANCEL: 
			self.About.hide()
			self.window.set_modal(True)
							
	def noclose(widget, event,data): #evita que se cierre la ventana principal
		return True
				
if __name__ == '__main__':
	w = Window()
	popen("xsetroot -cursor_name left_ptr")
	w.webview.load_uri(web)
	gtk.main()
