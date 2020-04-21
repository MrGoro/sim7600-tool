.PHONY: all clean install

all:
	chmod +x sim-tool
	chmod +x sim-tool.py
	chmod +x sim/lte/*.sh

clean:

install:
	mkdir -p $(DESTDIR)/usr/bin
	cp sim-tool $(DESTDIR)/usr/bin/
	mkdir -p $(DESTDIR)/usr/share/sim-tool
	cp sim-tool.py $(DESTDIR)/usr/share/sim-tool/sim-tool
	cp version $(DESTDIR)/usr/share/sim-tool/version
	cp -R sim $(DESTDIR)/usr/share/sim-tool
