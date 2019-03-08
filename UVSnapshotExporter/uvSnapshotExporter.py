################################
#
# UV snapshot exporter
# created by Tristan LG
#
# This script export uvSnapshots of all the uvSets of all selected objects
# Report bugs by writing to tristan.legranche@gmail.com
#
# Script under CC-BY-NC licence
#
################################

# Libraries
import os
import maya.cmds as mc
from PySide2 import QtCore
from PySide2 import QtWidgets

# Variables
PLUGIN_NAME = 'UV Snapshot exporter'
PLUGIN_VERSION = '0.1'
TEXTURE_FOLDER = 'sourceImages'
INFOS = 'Report bugs to tristan.legranche@gmail.com \n\nTool under licence CC-BY-NC \nContact me for commercial use'
FILE_TYPES = ['png', 'jpg', 'iff', 'tga']
SIZE = ['4096', '2048', '1024', '512', '256', '128']
COLORS = ['red', 'green', 'blue', 'pink', 'yellow', 'white', 'black']


class Exporter:

    def __init__(self):

        print('\n\n' + PLUGIN_NAME + ' version ' + PLUGIN_VERSION + '\n')
        self.actualWorkspace = mc.workspace(fullName=True)
        self.initUI()

    def initUI(self):
        """
        Creates the UI
        :return: None
        """

        # Create our main window
        self.mainWindow = QtWidgets.QDialog()
        self.mainWindow.setWindowTitle(PLUGIN_NAME + ' version ' + PLUGIN_VERSION)
        self.mainWindow.setFixedSize(350, 350)
        self.mainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # Create vertical layout
        self.layVMainWindowMain = QtWidgets.QVBoxLayout()
        self.mainWindow.setLayout(self.layVMainWindowMain)
        self.mainWindow.setStyleSheet("""
                                       QGroupBox {  }
                                       """)

        # Texture Folder
        self.grpOptions = QtWidgets.QGroupBox('Options')
        self.layVMainWindowMain.addWidget(self.grpOptions)

        self.optionsLayout = QtWidgets.QVBoxLayout()
        self.grpOptions.setLayout(self.optionsLayout)

        # Create the layout
        self.optionsSubLayout4 = QtWidgets.QHBoxLayout()
        self.optionsLayout.insertLayout(0, self.optionsSubLayout4, stretch=0)

        # Create the widgets
        sourceImagesFolder = self.actualWorkspace + '/' + TEXTURE_FOLDER
        self.texturePath = QtWidgets.QLineEdit(sourceImagesFolder)
        self.optionsSubLayout4.addWidget(self.texturePath)

        self.getButton = QtWidgets.QPushButton('Get')
        self.getButton.clicked.connect(lambda: self.getTextureFolder())
        self.optionsSubLayout4.addWidget(self.getButton)


        # Create the layout
        self.optionsSubLayout3 = QtWidgets.QHBoxLayout()
        self.optionsLayout.insertLayout(1, self.optionsSubLayout3, stretch=0)

        # Create the widgets
        self.map1 = QtWidgets.QLabel('UV folder')
        self.optionsSubLayout3.addWidget(self.map1)

        self.uvFolder = QtWidgets.QLineEdit('UV')
        self.optionsSubLayout3.addWidget(self.uvFolder)


        # Create the layout
        self.optionsSubLayout5 = QtWidgets.QHBoxLayout()
        self.optionsLayout.insertLayout(2, self.optionsSubLayout5, stretch=0)

        # Create the widgets
        self.map1 = QtWidgets.QLabel('UV suffix')
        self.optionsSubLayout5.addWidget(self.map1)

        self.uvSuffix = QtWidgets.QLineEdit('_UVSnap')
        self.optionsSubLayout5.addWidget(self.uvSuffix)


        # Create the layout
        self.optionsSubLayout1 = QtWidgets.QHBoxLayout()
        self.optionsLayout.insertLayout(3, self.optionsSubLayout1, stretch=0)

        # Create the widgets
        self.map1 = QtWidgets.QLabel('File type')
        self.optionsSubLayout1.addWidget(self.map1)

        self.fileExtension = QtWidgets.QComboBox()
        self.fileExtension.addItems(FILE_TYPES)
        self.fileExtension.setCurrentIndex(0)
        self.optionsSubLayout1.addWidget(self.fileExtension)


        # Create the layout
        self.optionsSubLayout2 = QtWidgets.QHBoxLayout()
        self.optionsLayout.insertLayout(4, self.optionsSubLayout2, stretch=0)

        # Create the widgets
        self.map1 = QtWidgets.QLabel('Map resolution')
        self.optionsSubLayout2.addWidget(self.map1)

        self.resolution = QtWidgets.QComboBox()
        self.resolution.addItems(SIZE)
        self.resolution.setCurrentIndex(1)
        self.optionsSubLayout2.addWidget(self.resolution)


        # Create the layout
        self.optionsSubLayout6 = QtWidgets.QHBoxLayout()
        self.optionsLayout.insertLayout(5, self.optionsSubLayout6, stretch=0)

        # Create the widgets
        self.map1 = QtWidgets.QLabel('Color')
        self.optionsSubLayout6.addWidget(self.map1)

        self.color = QtWidgets.QComboBox()
        self.color.addItems(COLORS)
        self.color.setCurrentIndex(1)
        self.optionsSubLayout6.addWidget(self.color)

        # Create the layout
        self.optionsSubLayout7 = QtWidgets.QHBoxLayout()
        self.optionsLayout.insertLayout(6, self.optionsSubLayout7, stretch=0)

        # Create the widgets
        self.proceedButton = QtWidgets.QPushButton('Proceed')
        self.proceedButton.clicked.connect(lambda: self.main())
        self.optionsSubLayout7.addWidget(self.proceedButton)

        # Infos
        self.grpInfos = QtWidgets.QGroupBox('Credits')
        self.layVMainWindowMain.addWidget(self.grpInfos)

        self.infosLayout = QtWidgets.QVBoxLayout()
        self.grpInfos.setLayout(self.infosLayout)

        # Infos widgets
        self.infos = QtWidgets.QLabel(INFOS)
        self.infosLayout.addWidget(self.infos)
        self.infos.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        global window

        try:
            window.close()
            window.deleteLater()
        except:
            pass

        window = self.mainWindow
        self.mainWindow.show()
        print('UI opened')

    def getTextureFolder(self):
        """
        Get the base texture path in the interface, the file dialog start in the base texture path of the project
        :return: The texture directory
        """

        # Get project
        projectDirectory = mc.workspace(rootDirectory=True, query=True)

        # Set base texture folder
        textureFolder = projectDirectory + '/' + TEXTURE_FOLDER

        if os.path.isdir(textureFolder):
            sourceImages = textureFolder
        else:
            sourceImages = projectDirectory

        # Open a file dialog
        workDirectory = mc.fileDialog2(startingDirectory=sourceImages, fileMode=2, okCaption='Select')[0]

        # Update the texture path in the interface
        self.texturePath.setText(workDirectory)

        return workDirectory

    def main(self):

        texturesPath = self.texturePath.text()
        uvPath = self.uvFolder.text()
        uvSuffix = self.uvSuffix.text()
        fileExtension = self.fileExtension.currentText()
        mapResolution = self.resolution.currentText()
        color = self.color.currentText()

        meshes = mc.ls(selection=True)

        print('EXPORT STARTED')

        for mesh in meshes:

            shapes = mc.listRelatives(mesh, children=True, shapes=True)

            if shapes:

                for shape in shapes:
                    if mc.objectType(shape)=='mesh':

                        mc.select(shape, replace=True)

                        uvSets = mc.polyUVSet(allUVSets=True, query=True)

                        for uvSet in uvSets:

                            if color == 'green':
                                red = blue = 0
                                green = 255

                            elif color == 'blue':
                                red = green = 0
                                blue = 255

                            elif color == 'red':
                                green = blue = 0
                                red = 255

                            elif color == 'pink':
                                red = blue = 255
                                green = 0
                            elif color == 'yellow':
                                red = green = 255
                                blue = 0

                            elif color == 'white':
                                red = green = blue = 255

                            elif color == 'black':
                                red = green = blue = 0

                            fileName = texturesPath + '/' + uvPath
                            if not fileName == texturesPath:
                                fileName += '/'

                            if not os.path.exists(fileName):
                                os.makedirs(fileName)

                            fileName += mesh + '_' + uvSet + uvSuffix + '.' + fileExtension

                            mc.polyUVSet(currentUVSet=True, uvSet=uvSet)

                            mc.uvSnapshot(overwrite=True, fileFormat=fileExtension, xResolution=int(mapResolution), yResolution=int(mapResolution), antiAliased=True, redColor=red, greenColor=green, blueColor=blue, name=fileName)
                            print fileName + ' as been created'

        mc.select(meshes, replace=True)

        print('EXPORT FINISHED')
