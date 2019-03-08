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

uvPath = 'UV'            # The folder in sourceImage used to stock the uv snapshots
uvColor = 'green'        # Choose between red, green and blue
uvFileType = 'png'       # The file type you want to use for the snapshots
uvSize = 2048            # The pixel resolution of the snapshots
uvSuffixe = 'uvSnap'    # The name of the snapshots will be mesh_uvSet_uvSuffixe

import maya.cmds as mc

meshes = mc.ls(selection=True)
actualWorkspace = mc.workspace(fullName=True)

for mesh in meshes:
    
    for shape in mc.listRelatives(mesh, children=True, shapes=True):
        if mc.objectType(shape)=='mesh': 
            mc.select(shape, replace=True)   
            uvSets = mc.polyUVSet(allUVSets=True, query=True)
            
            for uvSet in uvSets:
                if uvColor == 'green':
                    red = blue = 0
                    green = 255
                elif uvColor == 'blue':
                    red = green = 0
                    blue = 255
                elif uvColor == 'red':
                    green = blue = 0
                    red = 255
                
                fileName = actualWorkspace + '/sourceImages/' + mesh + '_' + uvSet + '_' + uvSuffixe + '.' + uvFileType
                mc.uvSnapshot(overwrite=True, fileFormat=uvFileType, xResolution=uvSize, yResolution=uvSize, antiAliased=True, redColor=red, greenColor=green, blueColor=blue, name=fileName)
                print fileName + ' as been created'
                
            
mc.select(meshes, replace=True)