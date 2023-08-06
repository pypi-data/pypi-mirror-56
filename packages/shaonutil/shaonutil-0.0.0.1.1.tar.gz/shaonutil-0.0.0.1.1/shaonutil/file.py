import json,codecs,configparser,subprocess,platform,os,glob

def ConfigSectionMap(Config, section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

class CaseConfigParser(configparser.SafeConfigParser):
    def optionxform(self, optionstr):
        return optionstr

def read_configuration_ini(filename):
	config = configparser.ConfigParser()
	config.readfp(codecs.open(filename, "r", "utf8"))
	return config

def read_safecase_configuration_ini(filename):
	config = CaseConfigParser()
	config.readfp(codecs.open(filename, "r", "utf8"))
	return config


def read_json(filename):
	with codecs.open(filename, "r", encoding="utf-8") as fp:
		data = json.load(fp)
	#Print Formatted Dictionary
	#print(json.dumps(data, indent=4))
	return data

def write_json(obj,filename):
	with codecs.open(filename, "w", encoding='utf-8') as fp:
	    json.dump(obj, fp, indent=1)

def read_file(filename):
	with codecs.open(filename, "r", encoding="utf-8") as file_reader:
		lines = file_reader.readlines()

	ill_chars = ['\r','\n']
	_ = []
	for line in lines:
		for ic in ill_chars:
			line = line.replace(ic,'')
		_.append(line)
	filtered_lines = _
	return filtered_lines

def write_file(filename, strs,mode="w"):
	import codecs
	with codecs.open(filename, mode, encoding='utf-8') as file_appender:
		file_appender.writelines(strs)


def open_file_with_default_app(filepath):
	import subprocess
	if platform.system() == 'Darwin':       # macOS
	    subprocess.call(('open', filepath))
	elif platform.system() == 'Windows':    # Windows
	    os.startfile(filepath)
	elif platform.system() == 'Windows':    # Windows
		subprocess.call(('xdg-open', filepath))
	else:                                   # linux variants
	    subprocess.call(('xdg-open', filepath))

def get_last_file_of_dir(filename):
	list_of_files = glob.glob(filename)
	latest_file = max(list_of_files, key=os.path.getctime)
	return latest_file


if __name__ == '__main__':
	pass
