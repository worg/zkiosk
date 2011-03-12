#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk
import pygtk
import webkit
import ConfigParser
from os import popen, path
from sys import path as spath

#Creamos la variable del módulo para leer la configuración
cfg = ConfigParser.ConfigParser()

localpath = spath[0]
localpath += '/' # ''' Obtenemos la ruta en la que está el programa  y le agregamos / al final '''
configpath = path.expanduser("~/.zkioskrc")

if path.exists(configpath): #'''Si existe el archivo de configuración, lo lee'''
	cfg.read(configpath)

else:

	configf = ConfigParser.ConfigParser() # '''En caso de que no exista, crea uno con valores por default'''
	configf.add_section("Biblio")
	configf.set("Biblio", "web","http://148.204.48.96/uhtbin/webcat")
	configf.set("Biblio", "theme", "gtkrc")
	
	configfl = open(configpath, "wb") #''' Guarda el archivo que creamos ''' 
	configf.write(configfl)
	configfl.close()
		
	cfg.read(configpath)  

#Asignamos los valores de la configuracion a variables para su uso posterior
web = cfg.get("Biblio","web")
theme = cfg.get("Biblio","theme")
	
class zKiosk:
	def __init__(self):
		self.builder = gtk.Builder() 
		self.builder.add_from_file(localpath + 'zkiosk-ui.glade')
		self.window = self.builder.get_object('window')
		self.webview = self.builder.get_object('webView') 

		#Cambia el user-agent (por cuestión estética y de identificación para estadísticas)
		Settings = self.webview.get_settings()		
		useragent = Settings.get_property("user-agent")
		useragent = useragent.replace(' Safari/',' zombieKiosk/DrunkEngine Safari/')
		Settings.set_property("user-agent",useragent)
		Settings.set_property("enable-plugins",False)
		#cambiando a pantalla completa la ventana
		maxx = gtk.gdk.screen_width() 
		maxy = gtk.gdk.screen_height() 
		self.window.set_size_request(maxx,maxy) 
		
		#Parseamos el archivo del estilo visual
		gtk.rc_reset_styles(self.window.get_settings())
		gtk.rc_parse(theme)
		gtk.rc_add_default_file(theme)
		gtk.rc_reparse_all()
		
		#muestra los elementos de la ventana
		self.window.show_all()
		#-------DEBUG---------
		self.webview.connect("navigation-policy-decision-requested",self.VerUri)
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
	
	def VerUri(self,view,frame,net_req,nav_act,pol_dec):
		uri = net_req.get_uri()
		
		if( "http://azul.bnct.ipn.mx" in uri ):
			frame.load_uri(web)
		return False
		
if __name__ == '__main__':
	w = zKiosk()
	popen("xsetroot -cursor_name left_ptr")
	w.webview.load_uri(web)
	gtk.main()
