from distutils.core import setup
import py2exe

pliki = [('.', ['splash.png', 'icon.ico'])]

setup(windows=[{"script": 'client.py', "icon_resources": [(1, 'icon.ico')]}],
data_files = pliki,
zipfile = None,
options={
                "py2exe":{
                        "unbuffered": True,
                        "optimize": 2,
                        "bundle_files": 1,
						"includes":["sip", "PyQt4.QtNetwork"]
                }
        }

)