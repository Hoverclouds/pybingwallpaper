#!/usr/bin/env python3

import log
from setter import *
import sys
import subprocess
import tempfile
import os

_log = log.getChild('osx_setter')

if sys.platform == 'darwin':
    def set_desktop_background(filename):
        SCRIPT = """
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
"""
        scr = subprocess.Popen('/usr/bin/osascript',
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = scr.communicate((SCRIPT%filename).encode('utf8'))
        #subprocess.Popen(SCRIPT%filename, shell=True)
        return (scr.poll(), out, err)

    class OsxWallpaperSetter(WallpaperSetter):
        def set(self, path, args):
            tf = tempfile.NamedTemporaryFile(delete=False)
            tf.close()
            try:
                _log.debug('copy to temp file %s', tf.name)
                subprocess.call(['cp', '-a', path, tf.name])
                _log.debug('set to temp file')
                ret, out, err = set_desktop_background(tf.name)
                _log.debug('script return %s:(%s, %s)', ret, out, err)
                _log.info('set desktop to %s', path)
                set_desktop_background(path)
                _log.debug('script return %s:(%s, %s)', ret, out, err)
            finally:
                _log.debug('remove temp file %s', tf.name)
                os.remove(tf.name)

    register('osx', OsxWallpaperSetter)

    if __name__ == '__main__':
        set_desktop_background('/Users/genzj/MyBingWallpapers/wallpaper.jpg')
