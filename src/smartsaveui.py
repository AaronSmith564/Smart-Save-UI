import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

import mayautils

def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)

class SimpleUI(QtWidgets.QDialog):
    """simple UI test class"""

    def __init__(self):
        """function called whenever you create an object of this class"""
        """Constructor"""
        # Passing the object Simple UI as an argument to super()
        # makes this line python 2 and 3 compatible
        super(SimpleUI, self).__init__(parent=maya_main_window()) # runs the init of the Qdialog class
        self.scene = mayautils.SceneFile()
        print(self.scene.dir)
        print(self.scene.dir)
        self.setWindowTitle("A Simple UI")
        self.resize(500, 200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        # removes the help button from the default flags in the window

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create widgets for our UI"""
        self.title_lbl = QtWidgets.QLabel("Smart Save")
        self.title_lbl.setStyleSheet("font: bold 40px")
        self.dir_lbl = QtWidgets.QLabel("Directory")
        self.dir_le = QtWidgets.QLineEdit()  # widget that takes an input
        self.dir_le.setText(self.scene.dir)
        self.browse_btn = QtWidgets.QPushButton("Browse...")
        self.descriptor_lbl = QtWidgets.QLabel("Descriptor")
        self.descriptor_le = QtWidgets.QLineEdit()  # widget that takes an input
        self.descriptor_le.setText(self.scene.descriptor)
        self.version_lbl = QtWidgets.QLabel("Version")
        self.version_spinbox = QtWidgets.QSpinBox()  # widget that a ranged number
        self.version_spinbox.setValue(self.scene.version) # the default value

        self.ext_lbl = QtWidgets.QLabel("Extension")
        self.ext_le = QtWidgets.QLineEdit()  # widget that takes an input with ma as default
        self.ext_le.setText(self.scene.ext)
        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_incr_btn = QtWidgets.QPushButton("Save and Increment")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        """lay out our widgets in the UI"""

        self.directory_lay = QtWidgets.QHBoxLayout()
        self.directory_lay.addWidget(self.dir_lbl)
        self.directory_lay.addWidget(self.dir_le)
        self.directory_lay.addWidget(self.browse_btn)

        self.descriptor_lay = QtWidgets.QHBoxLayout()
        self.descriptor_lay.addWidget(self.descriptor_lbl)
        self.descriptor_lay.addWidget(self.descriptor_le)

        self.version_lay = QtWidgets.QHBoxLayout()
        self.version_lay.addWidget(self.version_lbl)
        self.version_lay.addWidget(self.version_spinbox)

        self.ext_lay = QtWidgets.QHBoxLayout()
        self.ext_lay.addWidget(self.ext_lbl)
        self.ext_lay.addWidget(self.ext_le)

        self.bottom_btn_lay = QtWidgets.QHBoxLayout()
        self.bottom_btn_lay.addWidget(self.save_incr_btn)
        self.bottom_btn_lay.addWidget(self.save_btn)
        self.bottom_btn_lay.addWidget(self.cancel_btn)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.title_lbl)
        self.main_layout.addLayout(self.directory_lay)
        self.main_layout.addLayout(self.descriptor_lay)
        self.main_layout.addLayout(self.version_lay)
        self.main_layout.addLayout(self.ext_lay)
        self.main_layout.addStretch() # adds a space between the bottom buttons and the rest of the widgets
        self.main_layout.addLayout(self.bottom_btn_lay)
        self.setLayout(self.main_layout)

    def create_connections(self):
        """connects our widgit signals to slots"""
        #connects the bool output of a button to a object attribute
        self.cancel_btn.clicked.connect(self.cancel)
        self.save_btn.clicked.connect(self.save)
        self.save_incr_btn.clicked.connect(self.save_and_increment)

    def _populate_scenefile_properties(self):
        """populates the scenefile objects with values found in the UI"""
        self.scene.dir = self.dir_le.text() # pulls the input from the line
        self.scene.descriptor = self.descriptor_le.text()
        self.scene.version = self.version_spinbox.value()
        self.scene.ext = self.ext_le.text()

    @QtCore.Slot()
    def save(self):
        """saves the dialog"""
        self._populate_scenefile_properties()
        self.scene.save()

    @QtCore.Slot()
    def cancel(self):
        """Quits the dialog"""
        self.close()

    @QtCore.Slot()
    def save_and_increment(self):
        """increments and saves the dialog"""
        self._populate_scenefile_properties()
        self.scene.increment_and_save()