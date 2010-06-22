import gtk
import pygtk
import webkit
class Window:
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file('zkiosk-ui.glade')
		self.window = self.builder.get_object('window1')
		self.Browser = self.builder.get_object('Browser')
		self.window.show_all()
		
		self.webview = webkit.WebView()
		self.Browser.add(self.webview)
		self.Browser.show_all()
		
		#cambiando a pantalla completa
		maxx = gtk.gdk.screen_width() 
		maxy = gtk.gdk.screen_height() 
		self.window.set_size_request(maxx,maxy) 
		
		#conectando los botones a las funciones
		self.builder.connect_signals(self)
		
            
	def home(self, widget):
		self.webview.open("http://148.204.48.96/uhtbin/webcat")
				
	def back(self, widget):
		self.webview.go_back()

	def fwd(self, widget):
		self.webview.go_forward()

	def refresh(self, widget):
		self.webview.reload()
		
	def about(self, widget):
		self.window.set_modal(False)
		self.About=self.builder.get_object('aboutb')
		Respuesta = self.About.run()
		if Respuesta == gtk.RESPONSE_DELETE_EVENT or Respuesta == gtk.RESPONSE_CANCEL:
			self.About.hide()
			self.window.set_modal(True)
	
	def noclose(widget, event,data):
		return True
				
if __name__ == '__main__':
	w = Window()
	w.webview.open("http://148.204.48.96/uhtbin/webcat")
	gtk.main()
