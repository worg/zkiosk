INS= /usr/bin/install -C
install:
	$(INS) zKiosk.py /opt/zKiosk/zKiosk.py
	$(INS) zKiosk.svg /opt/zKiosk/zKiosk.svg
	$(INS) zkiosk-ui.glade /opt/zKiosk/zkiosk-ui.glade
	$(INS) gtkrc /opt/zKiosk/gtkrc
	$(INS) config.cfg ~/.zkioskrc
