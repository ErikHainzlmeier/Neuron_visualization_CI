import numpy as np
import pandas as pd
import maya.api.OpenMaya as om
import maya.cmds as cmds

#Liste aller Nodes: 400(Neuronen) x 50(Nodes)
node = []
node.append([]) #Neues Neuron erstellen

shaderlist = []
shaderlist.append([])

for i in range(3):

    #crerate new Sohere and move it slightly
    selection = cmds.polySphere(r=1, name='mySphereTest#')
    node[0].append(selection)  #Neuen Knoten erstellen fürr Neuron 0
    cmds.move(1*i, 0, 0)

    #create new shader and assign a color to it
    shader = cmds.shadingNode('aiStandardSurface', asShader=1, name='Shader#')
    shaderlist[0].append(shader)
    cmds.setAttr((shader + '.baseColor'), 0, 0, 0, type='double3')

    #Verbinde Object mit Shader
    #selection = cmds.ls(sl=1)
    cmds.select(selection[0])
    cmds.hyperShade(a=shader)

    for j in range(5):
        cmds.setKeyframe(shader, time=10*j, attribute='baseColorR', value=0.05*j*i)
        cmds.setKeyframe(shader, time=10*j, attribute='baseColorG', value=1-0.05*j*i)
        cmds.setKeyframe(shader, time=10*j, attribute='baseColorB', value=0.2*j)



#cmds.setAttr((shaderlist[0][3] + '.baseColor'), 1, 1, 1, type='double3')



