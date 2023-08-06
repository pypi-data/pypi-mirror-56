import yaml
import os
import sys

def main():
	settingsfile = os.path.join(DATA_DIR,"presets.yml")
	with open(settingsfile,"r") as f:
		settings = yaml.safe_load(f)

	selected = settings[sys.argv[1]]
	os.cwd(selected["path"])
	os.system("youtube-dl " + sys.argv[2])
