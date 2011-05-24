INS			   = /usr/bin/install -D
IPATH		   = /opt
PROGRAM        = zkiosk
ARCH           = $(shell uname -s)
VALAC          = valac
VALACOPTS      = -g -D $(ARCH)
PKGS           = --pkg gtk+-2.0 --pkg gmodule-2.0 --pkg webkit-1.0
SRC            = zKiosk.gs

all:
	@$(VALAC) $(VALACOPTS) $(SRC) -o $(PROGRAM) $(PKGS)

install:
	$(INS) zKiosk.py $(IPATH)/zKiosk/zKiosk.py
	$(INS) zKiosk.svg $(IPATH)/zKiosk/zKiosk.svg
	$(INS) zkiosk-ui.glade $(IPATH)/zKiosk/zkiosk-ui.glade
	$(INS) gtkrc $(IPATH)/zKiosk/gtkrc
	$(INS) config.cfg ~/.zkioskrc

uninstall:
	rm $(IPATH)/zKiosk/zKiosk.py
	rm $(IPATH)/zKiosk/zKiosk.svg
	rm $(IPATH)/zKiosk/zkiosk-ui.glade
	rm $(IPATH)/zKiosk/gtkrc
	rm ~/.zkioskrc
