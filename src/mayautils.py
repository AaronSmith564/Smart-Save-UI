import pymel.core as pmc

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
    dir(str, optional): Directory to the scene file, defaults to none
    descriptor(str, optional): Short descriptor of the scene file, defaults to main
    version (int, optional): Version number, defaults to 1
    ext (str, optional): extension defaults to "ma"
    """
    def __init__(self, dir=None, descriptor='main', version=1, ext="ma"):
        self.dir = dir
        self.descriptor = descriptor
        self.version = version
        self.ext = ext



    def basename(self):
        """Returns the DCC scene file's name

        Returns:
            STR: THE NAME OF THE SCENE FILE"""
        name_pattern = "{descriptor}_{version:03d}.{ext}"
        name = name_pattern.format(descriptor=self.descriptor, version=self.version, ext=self.ext)
        return name
