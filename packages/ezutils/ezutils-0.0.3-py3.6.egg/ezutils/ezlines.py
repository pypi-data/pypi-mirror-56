import os


class EzLines:

    def fromfile(self, filename):
        self.fromfile = filename
        return self

    def readlines(self):
        f = open(os.path.abspath(fromfile))
        lines = f.readlines()
        f.close()
        return lines

    def writelines(self, lines):
        self.lines = lines

    def newline(self, with_newline):
        self.with_newline
        return self

    def tofile(self, filename):
        f = open(filename, 'w')
        f.writelines(lines)
        f.close()
