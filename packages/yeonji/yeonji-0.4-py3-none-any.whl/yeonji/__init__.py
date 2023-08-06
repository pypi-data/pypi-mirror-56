name = "yeonji"
author = {
	"name":"Johannes Krattenmacher",
	"email":"python@krateng.dev",
	"github":"krateng"
}
desc = "Collection of command line tools"
version = 0,4

# local data
import os
try:
	DATA_DIR = os.environ["XDG_DATA_HOME"].split(":")[0]
	assert os.path.exists(DATA_DIR)
except:
	DATA_DIR = os.path.join(os.environ["HOME"],".local/share/")
DATA_DIR = os.path.join(DATA_DIR,"yeonji")
os.makedirs(DATA_DIR,exist_ok=True)

# package finder
import pkgutil, importlib, sys
modulenames = [modname for importer, modname, ispkg in pkgutil.iter_modules(__import__(__name__).__path__)]
modules = {name:importlib.import_module("." + name,package=__name__) for name in modulenames}

# give packages their own directories
for m in modules:
	mod = modules[m]
	dir = os.path.join(DATA_DIR,m)
	os.makedirs(dir,exist_ok=True)
	mod.DATA_DIR = dir


requires = [
	"tabulate",
	"send2trash"
]

resources = [
]



commands = {
	mod:mod + ":main"
	for mod in modulenames
}
