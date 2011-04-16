import os, sys, subprocess

class MAME(object):
    def __init__(self, path, options={}):
        if not os.access(path, os.X_OK):
            raise Exception("%s is not an executable program" % path)
        self.path = path
        self.options = options

    def play(self, game, options={}):
        allopts = self.options.copy()
        allopts.update(options)
        cmd = [self.path,]
        for name,val in allopts.items():
            if not name == '':
                cmd.append(str(name))
            if not val == '':
                cmd.append(str(val))
        cmd.append(game.name)
        return subprocess.Popen(cmd)
