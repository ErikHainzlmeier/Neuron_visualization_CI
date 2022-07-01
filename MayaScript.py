import numpy as np
import pandas as pd


filepath = "C:\\Users\\Rafael\\Desktop\\praktikum bioanaloge\\ci_refine_list_mdl\\ci_refine_list_mdl.pkl"
obj = pd.read_pickle(filepath)


for i in range(0,399,100):
    for j in range(len(obj[i])-2):
        print("iteration1:", i, "iteration2:", j)
        x = obj[i][j][0]
        y = obj[i][j][1]
        z = obj[i][j][2]

        cmds.polyCylinder(r=0.02, name='myCylinder#')
        cmds.move(x, y, z)
        print("iteration finished")