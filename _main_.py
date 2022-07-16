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
    print("Import voltage traces...")
    measurements = read_decompress(measurements_filepath)
    # print(len(measurements))
    return measurements


def import_neuron_coordinates():
    print("Import coordinates...")
    obj = pd.read_pickle(coords_filepath)

    # Create neuron fibres from coordinate data
    # ci_refine_list_mdl.pkl
    # coordinates for the neuron paths
    # list of 400 elements of variable length x 3 matrix


    vertices = []
    for i in range(0, 400, 1):
        vertices.append(om.MPointArray())
        for eachPos in obj[i][:]:
            # make a point array out of coordinates from .pkl file for every neuron
            mPoint = om.MPoint()
            mPoint.x = eachPos[0]
            mPoint.y = eachPos[1]
            mPoint.z = eachPos[2]
            vertices[i].append(mPoint)

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


def create_curves(vertices, disp_neur):
    # returns list of 400 curve objects, and list of 400 spans (int)
    print("building curves...")

    curves = []
    spans = []
    cmds.group(em=True, name='curves')
    # iterrate through curves
    for i in disp_neur:
        # create a curve for every neuron following along the vertices
        cmds.curve(pw=vertices[i])
        # rebuild curve with different units
        current_spans = cmds.getAttr(".spans")
        spans.append(current_spans)
        current_curve = cmds.rebuildCurve(rt=0, s=current_spans)
        cmds.parent(current_curve, 'curves')
        curves.append(current_curve)

    return curves, spans


def calculate_node_coords(number_of_nodes, curves, spans, disp_neur):
    print("Calcualting coordinates of nodes...")
    node_coords = []

    # limit max number of nodes per neuron
    if number_of_nodes > 49:
        number_of_nodes = 49

    # iterate through every neuron
    for i in range(len(disp_neur)):
        # calculate node positions on the curve
        node_params = np.linspace(0, spans[i], num=number_of_nodes)
        node_coords.append([])

        # iterate through every node
        for j in range(number_of_nodes):
            current_coords = cmds.pointOnCurve(curves[i], pr=node_params[j], p=True)
            node_coords[i].append(current_coords)

    return node_coords


def create_nodes(node_coords, disp_neur):
    print("creating nodes...")
    node_size = 0.03
    node = []
    shader = []
    cmds.group(em=True, name='nodes')

    # iterate through neurons
    for i in range(len(disp_neur)):
        node.append([])  # Neues Neuron erstellen
        shader.append([])
        current_group = cmds.group(em=True, name='neuron' + str(i), parent='nodes')
        #print("Iterating neuron", i, ":", len(node_coords))
        # iterate through nodes
        for j in range(len(node_coords[i])):
            print("Node creation... Neuron", disp_neur[i], "Node", j)
            #current_node = cmds.polySphere(r=node_size, name='mySphere#', sx=5, sy=5)
            current_node = cmds.sphere(r=node_size, s=4, name='mySphere#')
            node[i].append(current_node)
            cmds.parent(node[i][j], current_group)

            cmds.move(node_coords[i][j][0], node_coords[i][j][1], node_coords[i][j][2])


            # create new shader and assign a color to it
            current_shader = cmds.shadingNode('aiStandardSurface', asShader=1, name='Shader#')
            cmds.setAttr((current_shader + '.baseColor'), 1, 1, 1, type='double3')
            shader[i].append(current_shader)
            cmds.select(current_node)
            cmds.hyperShade(a=current_shader)

    return node, shader


def create_frames(shader, measurements, disp_neur):
    print("creating frames...")
    # iterate through all neurons
    for i in range(len(disp_neur)):
        # iterate through all nodes
        for j in range(len(shader[i])):
            print("Frame creation... Neuron", disp_neur[i], "Node", j)
            # iterate through all measurement steps
            max_v = max(measurements[i][j])
            min_v = min(measurements[i][j])
            threshold = min_v + 0.09 * (max_v - min_v)
            pre_threshold = min_v + 0.06 * (max_v - min_v)
            #post_threshold = min_v + 0.65 * (max_v - min_v)
            for k in range(len(measurements[i][j])):
                if measurements[i][j][k] > threshold:
                    red = 1
                    green = min(1, 1 - 20 * measurements[disp_neur[i]][j][k])
                    blue = min(1, 1 - 20 * measurements[disp_neur[i]][j][k])
                    cmds.setKeyframe(shader[i][j], time=k, attribute='baseColorR', value=red)
                    cmds.setKeyframe(shader[i][j], time=k, attribute='baseColorG', value=green)
                    cmds.setKeyframe(shader[i][j], time=k, attribute='baseColorB', value=blue)
                elif measurements[i][j][k] > pre_threshold and measurements[i][j][k] < threshold:
                    red = 1
                    green = 1
                    blue = 1
                    cmds.setKeyframe(shader[i][j], time=k, attribute='baseColorR', value=red)
                    cmds.setKeyframe(shader[i][j], time=k, attribute='baseColorG', value=green)
                    cmds.setKeyframe(shader[i][j], time=k, attribute='baseColorB', value=blue)



def main():
    number_of_nodes = 49
    disp_neur = range(239, 241)   #display neuron from ... to ...
    create_frames = "no"

    vertices = import_neuron_coordinates()
    measurements = import_voltage_traces()

    curves, spans = create_curves(vertices, disp_neur)
    node_coords = calculate_node_coords(number_of_nodes, curves, spans, disp_neur)
    nodes, shader = create_nodes(node_coords, disp_neur)
    if create_frames == "yes":
        create_frames(shader, measurements, disp_neur)

    print("finished :)")

if __name__ == "__main__":
main()