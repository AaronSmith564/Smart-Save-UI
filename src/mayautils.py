import logging
import os
import maya.cmds as cmds

import pymel.core as pmc
from   pymel.core.system import Path

from pymel.core.system import versions

log = logging.getLogger(__name__)


def main():
    counter = 0
    while(counter<3):
        # Do something
        if counter >= 10:
            break
        cubexform, cubeshape = pmc.polyCube()
        cubexform.translateY.set(1.5 * counter)  # translate 1.5*counter units
        counter += 1


class SceneFile(object):
    """Class used to represent a DCC software scene file

    can be used to manipulate scene files without needing direct influence on the scene

    Attributes:
    dir(str, optional): Directory to the scene file, defaults to ''
    descriptor(str, optional): Short descriptor of the scene file, defaults to main
    version (int, optional): Version number, defaults to 1
    ext (str, optional): extension defaults to "ma"
    """
    def __init__(self, dir='', descriptor='main', version=1, ext="ma"):
        FilePath = cmds.file(q=True, sn=True)
        if(FilePath == ""):
            self._dir = Path(dir)
            self.descriptor = descriptor
            self.version = version
            self.ext = ext
        else:
            parts = os.path.split(FilePath)
            self._dir = parts[0]
            Name = parts[1].split('_v')
            self.descriptor = Name[0]
            Split2 = Name[1].split('.')
            self.version = int(Split2[0])
            self.ext = Split2[1]
    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, val):
        self._dir = Path(val)

    def basename(self):
        """Returns the DCC scene file's name

        Returns:
            STR: THE NAME OF THE SCENE FILE"""
        name_pattern = "{descriptor}_{version:03d}.{ext}"
        name = name_pattern.format(descriptor=self.descriptor, version=self.version, ext=self.ext)
        return name

    def path(self):
        """The function returns a path to scene file
        includes drive letter, any directory path and the file name

        Returns:
            Path: The path to the scene file
            """
        return Path(self.dir) / self.basename()

    def save(self):
        """Saves the scene file.

        Returns:
            :obj:'Path': The path to the scene file if successful, None, otherwise
            """
        try:
            Path = self.dir+ "\\" + self.descriptor + '_v0' + str(self.version) + '.' + self.ext
            pmc.system.saveAs(Path)
        except RuntimeError:
            log.warning("Missing directories. creating directories")
            self.dir.makedirs_p()
            Path = self.dir + "\\" + self.descriptor + '_v0' + str(self.version) + '.' + self.ext
            pmc.system.saveAs(Path)

    def increment_and_save(self):
        """finds the latest version on disk and increments before saving"""
        CurrentVersion = self.version
        for f in self.dir.files('*.ma'):
            parts = os.path.split(f)
            Directory = parts[0]
            Name = parts[1].split('_v')
            Descriptor = Name[0]
            Split2 = Name[1].split('.')
            Version = int(Split2[0])
            Extension = Split2[1]
            if(self.descriptor == Descriptor):
                if CurrentVersion < Version:
                    CurrentVersion = Version
        CurrentVersion = CurrentVersion + 1
        Path = self.dir + "\\" + self.descriptor + '_v0' + str(CurrentVersion) + '.' + self.ext
        pmc.system.saveAs(Path)
