FILES = client.py connection_dialog.py gui.py main_form.py websocket.py
PKG = forum-tracker-client_1.0.0-1_i386.deb

package: $(PKG)

$(PKG):
		mkdir -p ./debian/usr/share/forum-tracker-client/src
		cp $(FILES) ./debian/usr/share/forum-tracker-client/src
		fakeroot dpkg-deb --build debian $(PKG)

clean:
		rm -f $(PKG)
		for FILE in $(FILES); do rm -f ./debian/usr/share/forum-tracker-client/src/$$FILE; done

.PHONY: clean
