FILES = server.py tracker.py page_rater.py data_handler.py
PKG = forum-tracker-server_1.0.0-1_i386.deb

package: $(PKG)

$(PKG):
		cp $(FILES) ./debian/usr/share/forum-tracker-server/src
		fakeroot dpkg-deb --build debian $(PKG)

clean:
		rm -f $(PKG)
		for FILE in $(FILES); do rm -f ./debian/usr/share/forum-tracker-server/src/$$FILE; done

.PHONY: clean
