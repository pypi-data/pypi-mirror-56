import locale
import os

class jdTranslationHelper():
    def __init__(self, lang=None, default_language="en_GB"):
        if not lang:
            self.selected_language = locale.getlocale()[0]
        else:
            self.selected_language = lang
        self.default_language = default_language
        self.strings = {}

    def readLanguageFile(self, language_filename):
        with open(language_filename, encoding="utf-8") as lines:
            for line in lines:
                line = line.replace("\n","")
                if line == "" or line.startswith("#"):
                    continue
                key, op, value = line.rstrip().partition('=')
                if not op:
                    print('Error loading line "{}" in file {}'.format(line, language_filename))
                else:
                    self.strings[key] = value

    def loadDirectory(self, path):
        language_filename = os.path.join(path, self.default_language + ".lang")
        if not os.path.isfile(language_filename):
            print("{} was not found".format(language_filename))
            return
        self.readLanguageFile(language_filename)
        language_filename = os.path.join(path, self.selected_language + ".lang")
        if os.path.isfile(language_filename):
            self.readLanguageFile(language_filename)

    def translate(self, key, default=None):
        if default is None:
            default = key
        return self.strings.get(key, default)

    def getStrings(self):
        return self.strings
