import numpy as np
import pandas as pd
import maya.api.OpenMaya as om


filepath = "C:\\Users\\Rafael\\Desktop\\praktikum bioanaloge\\ci_refine_list_mdl\\ci_refine_list_mdl.pkl"
#"C:\\Users\\Erik\\Documents\\Elektrotechnik\\Master\\SS2022\\Projektpraktikum\\ci_refine_list_mdl.pkl"
obj = pd.read_pickle(filepath)

#Create neuron fibres from coordinate data
# ci_refine_list_mdl.pkl
# coordinates for the neuron paths
# list of 400 elements of variable length x 3 matrix

vertices = om.MPointArray()
for i in range(0,400,1):
    vertices = om.MPointArray()
    for eachPos in obj[i][:] :
# make a point array out of coordinates from .pkl file for every neuron
        mPoint      = om.MPoint ()
        mPoint.x    = eachPos[0]
        mPoint.y    = eachPos[1]
        mPoint.z    = eachPos[2]
        vertices.append (mPoint)

        #print(len(obj[i][:]))
    #if i != 0:
        #cmds.curve(pw=vertices[len(obj[i-1][:])+1 : len(obj[i-1][:])+len(obj[i][:])])
        #print(vertices[len(obj[i-1][:])+1 : len(obj[i-1][:])+len(obj[i][:])])
    #else:

# create a curve for every neuron following along the vertices
    cmds.curve(pw=vertices)



