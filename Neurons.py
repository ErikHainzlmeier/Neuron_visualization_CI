import numpy as np
import pandas as pd
import maya.api.OpenMaya as om


filepath = "C:\\Users\\Erik\\Documents\\Elektrotechnik\\Master\\SS2022\\Projektpraktikum\\ci_refine_list_mdl.pkl"
obj = pd.read_pickle(filepath)

#Create neuron fibres from coordinate data
# ci_refine_list_mdl.pkl
# coordinates for the neuron paths
# list of 400 elements of variable length x 3 matrix
fibreverts = []
fibreedges = []
fibrefaces = []
for coor in obj[i][:]:
    # Create vertices following neuron fibres coordinate
    fibreverts.append(coor)
for verindex in range(0, len(fibreverts) - 1):
    fibreedges.append([verindex, verindex + 1])

positionOrder = [cmds.pointPosition(i) for i in fibreverts]
cmds.curve(p=positionOrder)