
import numpy as np
import pandas as pd



filepath = "C:\\Users\\Erik\\Documents\\Elektrotechnik\\Master\\SS2022\\Projektpraktikum\\ci_refine_list_mdl.pkl"
obj = pd.read_pickle(filepath)





for i in range(0,399,2):
    for j in range(len(obj[i])-2):
        x_vals = [obj[i][j][0], obj[i][j+1][0]]
        y_vals = [obj[i][j][1], obj[i][j+1][1]]
        z_vals = [obj[i][j][2], obj[i][j+1][2]]


plt.show()






#result = cmds.polyCylinder( w=0.01, h=9, d=9, name='myCube#')