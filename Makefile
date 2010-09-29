INS= /usr/bin/install -D 
install:
	$(INS) zKiosk.py /opt/zKiosk/zKiosk.py
	$(INS) zKiosk.svg /opt/zKiosk/zKiosk.svg
	$(INS) zkiosk-ui.glade /opt/zKiosk/zkiosk-ui.glade
	$(INS) gtkrc /opt/zKiosk/gtkrc
	$(INS) config.cfg ~/.zkioskrc

uninstall:
	rm /opt/zKiosk/zKiosk.py
	rm /opt/zKiosk/zKiosk.svg
	rm /opt/zKiosk/zkiosk-ui.glade
	rm /opt/zKiosk/gtkrc
	rm ~/.zkioskrc
