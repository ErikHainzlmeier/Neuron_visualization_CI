import numpy as np
import pandas as pd
import maya.api.OpenMaya as om


number_of_nodes = 49
node_size = 0.03

filepath = "C:\\Users\\Rafael\\Desktop\\praktikum bioanaloge\\ci_refine_list_mdl\\ci_refine_list_mdl.pkl"
#"C:\\Users\\Erik\\Documents\\Elektrotechnik\\Master\\SS2022\\Projektpraktikum\\ci_refine_list_mdl.pkl"



obj = pd.read_pickle(filepath)

#Create neuron fibres from coordinate data
# ci_refine_list_mdl.pkl
# coordinates for the neuron paths
# list of 400 elements of variable length x 3 matrix

vertices = om.MPointArray()
neuron_number = 200

vertices = om.MPointArray()
for eachPos in obj[neuron_number][:]:
# make a point array out of coordinates from .pkl file for every neuron
    mPoint      = om.MPoint ()
    mPoint.x    = eachPos[0]
    mPoint.y    = eachPos[1]
    mPoint.z    = eachPos[2]
    vertices.append (mPoint)


# create a curve for every neuron following along the vertices
curve1 = cmds.curve(pw=vertices)
spans = cmds.getAttr(".spans")
cmds.rebuildCurve( rt=0, s=spans )

if number_of_nodes > 49:
    number_of_nodes = 49

node_params = np.linspace(0,spans,num=number_of_nodes)
for j in range(number_of_nodes):
    node_coords = cmds.pointOnCurve( 'curve1', pr=node_params[j], p=True )
    cmds.polySphere(r=node_size, name='mySphere#')
    cmds.move(node_coords[0],node_coords[1],node_coords[2])



print(cmds.arclen('curve1'))



