import numpy as np
import pandas as pd
import fpzip
import pickle
import importlib
import peakutils as peak
import functools
import operator
import maya.api.OpenMaya as om
import maya.cmds as cmds

# Global Variables

coords_filepath = "C:\\Users\\Rafael\\Desktop\\praktikum bioanaloge\\ci_refine_list_mdl\\ci_refine_list_mdl.pkl"
# coords_filepath = "C:\\Users\\Erik\\Documents\\Elektrotechnik\\Master\\SS2022\\Projektpraktikum\\ci_refine_list_mdl.pkl"
measurements_filepath = "C:\\Users\\Rafael\\Desktop\\praktikum bioanaloge\\projektpraktikum_animation_ss2022\\Rattay_2013_e7_o2.0_0.001000149883801424A.p"
number_of_nodes = 49


def unflatten_nlist(l):
    # restore a previously for compression purpose flattened list
    # this function is coded to re-nest according to specific parameters added while flattening

    l[np.isnan(l)] = l[2]  # replace nans with resting potential

    rec_l = []
    if type(l) != np.ndarray:
        raise ValueError("Not a numpy array")
    if len(np.shape(l)) != 1:
        raise ValueError("Not of depth 1")
    neuron_numbers = np.where(l >= 70000)[0]

    for i in range(len(neuron_numbers)):
        rec_l = rec_l + [
            l[neuron_numbers[i] + 1:(None if i == len(neuron_numbers) - 1 else neuron_numbers[i + 1])].tolist()]

    recc_l = []
    for i in range(len((rec_l))):
        compartments = np.where(np.array(rec_l[i]) >= 7000)[0]
        # fehler: es muessen alle durchgegangen werden. und sonderbehandlung fuer letztes element? Da index overflow
        # --> muesste behoben sein. Ich erinnere mich nicht mehr an den Fehler, aber afaik funktioniert alles inzwischen, vmtl habe ich vergessen diese zeile zu löschen -> TODO check

        recc_l = recc_l + [[]]
        for j in range(len(compartments)):
            recc_l[i] = recc_l[i] + [
                rec_l[i][compartments[j] + 1:(None if j == len(compartments) - 1 else compartments[j + 1])]]

    return recc_l


def decompress(data):
    # decompress data and return list into the nested format, indexed by [neuron number][compartment][time], values in V
    decompressed = fpzip.decompress(data, order='C')
    while np.shape(decompressed)[0] == 1:
        decompressed = decompressed[0]

    return unflatten_nlist(decompressed)


def read_decompress(save_path, us_before=50):
    # this returns decompressed data of a neuron population and stimulation amplitude. The return list indices are [neuron_number, compartment, time]

    decompressed = decompress(pickle.load(open(save_path, "rb")))
    # decompressed is a restored 3-Dimensional list. 1st D is neuron number, 2cnd D is compartment, 3rd D is time
    # the data has the first 50 µs removed (time before the stimulus), and everything after the last spike in each compartment
    # This is "restored" here, by setting it to v_res

    maxlen_ = lambda L: (max(map(maxlen_, L)) if isinstance(L[0], list) else len(L))
    maxlen = maxlen_(decompressed)
    v_res = 0
    # get resting V
    for d1 in decompressed:
        for d2 in d1:
            v_res = min(v_res, d2[0])

    # fill nested list to get uniform dimensions
    for id1, d1 in enumerate(decompressed):
        for id2, d2 in enumerate(d1):
            decompressed[id1][id2] = np.tile(v_res, us_before).tolist() + decompressed[id1][id2] + np.tile(v_res,
                                                                                                           maxlen - len(
                                                                                                               decompressed[
                                                                                                                   id1][
                                                                                                                   id2])).tolist()

    return decompressed


def import_voltage_traces():
    measurements = read_decompress(measurements_filepath)
    # print(len(measurements))
    return measurements


def import_neuron_coordinates():
    obj = pd.read_pickle(coords_filepath)

    # Create neuron fibres from coordinate data
    # ci_refine_list_mdl.pkl
    # coordinates for the neuron paths
    # list of 400 elements of variable length x 3 matrix

    vertices = om.MPointArray()
    for i in range(0, 400, 1):
        vertices = om.MPointArray()
        for eachPos in obj[i][:]:
            # make a point array out of coordinates from .pkl file for every neuron
            mPoint = om.MPoint()
            mPoint.x = eachPos[0]
            mPoint.y = eachPos[1]
            mPoint.z = eachPos[2]
            vertices.append(mPoint)

        # print(len(obj[i][:]))
        # if i != 0:
        # cmds.curve(pw=vertices[len(obj[i-1][:])+1 : len(obj[i-1][:])+len(obj[i][:])])
        # print(vertices[len(obj[i-1][:])+1 : len(obj[i-1][:])+len(obj[i][:])])
        # else:

        # create a curve for every neuron following along the vertices
        #cmds.curve(pw=vertices)

    '''
        obj = pd.read_pickle(coords_filepath)
        for i in range(0,399,100):
            for j in range(len(obj[i])-2):
                x = obj[i][j][0]
                y = obj[i][j][1]
                z = obj[i][j][2]
                cmds.polyCylinder(r=0.02, name='myCylinder#')
                cmds.move(x, y, z)
    '''

    return vertices


def create_curves(vertices):
    # returns list of 400 curve objects, and list of 400 spans (int)

    curves = []
    cmds.group(em=True, name='curves')

    # iterrate through curves
    for i in range(len(vertices)):
        # create a curve for every neuron following along the vertices
        cmds.curve(pw=vertices[i])

        # rebuild curve with different units
        spans = cmds.getAttr(".spans")
        current_curve = cmds.rebuildCurve(rt=0, s=spans)
        cmds.parent(current_curve, 'curves')

        curves.append(current_curve)

    return curves, spans


def calculate_node_coords(curves, spans):
    node_coords = []

    # limit max number of nodes per neuron
    if number_of_nodes > 49:
        number_of_nodes = 49

    # iterate through every neuron
    for i in range(len(curves)):
        # calculate node positions on the curve
        node_params = np.linspace(0, spans[i], num=number_of_nodes)
        node_coords.append([])

        # iterate through every node
        for j in range(number_of_nodes):
            current_coords = cmds.pointOnCurve(curves[i], pr=node_params[j], p=True)
            node_coords[i].append(current_coords)

    return node_coords


def create_nodes(node_coords):
    node_size = 0.03
    node = []
    shader = []
    cmds.group(em=True, name='nodes')

    # iterate through neurons
    for i in range(len(node_coords)):
        node.append([])  # Neues Neuron erstellen
        shader.append([])
        current_group = cmds.group(em=True, name='neuron' + str(i), parent='nodes')

        # iterate through nodes
        for j in range():
            current_node = cmds.polySphere(r=node_size, name='mySphere#')
            node[i][j] = current_node
            cmds.parent(node[i][j], current_group)

            cmds.move(node_coords[i][j][0], node_coords[i][j][1], node_coords[i][j][2])

            # create new shader and assign a color to it
            current_shader = cmds.shadingNode('aiStandardSurface', asShader=1, name='Shader#')
            cmds.setAttr((current_shader + '.baseColor'), 1, 1, 1, type='double3')
            shader[i][j].append(current_shader)

            # Verbinde Object mit Shader
            # selection = cmds.ls(sl=1)
            cmds.select(selection[0])
            cmds.hyperShade(a=current_shader)

    return node, shader


def create_frames(shader, measurements):
    # iterate through all neurons
    for i in range(len(shader)):
        # iterate through all nodes
        for j in range(len(shader[i])):
            # iterate through all measurement steps
            for k in range(len(measurements[i][j])):
                red = measurements[i][j][k]
                green = 1 - measurements[i][j][k]
                blue = 1 - measurements[i][j][k]
                cmds.setKeyframe(shader[i][j], time=k, attribute='baseColorR', value=red)
                cmds.setKeyframe(shader[i][j], time=k, attribute='baseColorG', value=green)
                cmds.setKeyframe(shader[i][j], time=k, attribute='baseColorB', value=blue)


def main():
    vertices = import_neuron_coordinates()
    measurements = import_voltage_traces()

    curves, spans = create_curves(vertices)
    node_coords = calculate_node_coords(curves, spans)
    nodes, shader = create_nodes(node_coords)
    create_frames(shader, measurements)


main()
