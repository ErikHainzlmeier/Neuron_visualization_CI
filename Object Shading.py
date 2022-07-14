import numpy as np
import pandas as pd
import maya.api.OpenMaya as om
import maya.cmds as cmds

#Liste aller Nodes: 400(Neuronen) x 50(Nodes)
node = []
node.append([]) #Neues Neuron erstellen

shaderlist = []
shaderlist.append([])

for i in range(5):

    #crerate new Sohere and move it slightly
    selection = cmds.polySphere(r=1, name='mySphereTest#')
    node[0].append(selection)  #Neuen Knoten erstellen fürr Neuron 0
    cmds.move(1*i, 0, 0)

    #create new shader and assign a color to it
    shader = cmds.shadingNode('aiStandardSurface', asShader=1, name='Shader#')
    shaderlist[0].append(shader)
    cmds.setAttr((shader + '.baseColor'), 1-0.1*i, 0.1*i, 0.1*i, type='double3')

    #Verbinde Object mit Shader
    #selection = cmds.ls(sl=1)
    cmds.select(selection[0])
    cmds.hyperShade(a=shader)

#Wenn man den Shader ändert, wird das direkt aufs Objekt übertragen
cmds.setAttr((shader + '.baseColor'), 0, 1, 0, type='double3')
cmds.setAttr((shaderlist[0][3] + '.baseColor'), 1, 1, 1, type='double3')

