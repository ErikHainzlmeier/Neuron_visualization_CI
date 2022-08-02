import pandas as pd


vertices = pd.read_pickle(r'C:\\Users\\Erik\\Documents\\Elektrotechnik\\Master\\SS2022\\Projektpraktikum\\ci_refine_list_mdl.pkl')
for i in range(0, len(vertices[0])):
    cmds.polyCube(w=0.01, h=0.01, d= 0.01)
    cmds.move(vertices[0][i][0], vertices[0][i][1], vertices[0][i][2])

