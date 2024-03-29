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
import maya.mel as mel
import pdb
import mtoa.utils as mutils

# Global Variables



#coords_filepath = "C:\\Users\\Rafael\\Desktop\\praktikum bioanaloge\\ci_refine_list_mdl\\ci_refine_list_mdl.pkl"
#coords_filepath = "C:\\Users\\Erik\\Documents\\Elektrotechnik\\Master\\SS2022\\Projektpraktikum\\ci_refine_list_mdl.pkl"
#measurements_filepath = "C:\\Users\\Rafael\\Desktop\\praktikum bioanaloge\\projektpraktikum_animation_ss2022\\Rattay_2013_e7_o2.0_0.001000149883801424A.p"
#measurements_filepath = "C:\\Users\\Erik\\Documents\\Elektrotechnik\\Master\\SS2022\\Projektpraktikum\\projektpraktikum_animation_ss2022\\projektpraktikum_animation_ss2022\\Rattay_2013_e7_o2.0_0.001000149883801424A.p"

class ui_settings(object):

    # constructor
    def __init__(self):
        self.window = "MR_Window"
        self.title = "Settings"
        self.size = (395, 600)

        # close old window is open
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        # create new window
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)

        cmds.columnLayout(adjustableColumn=True)

        # Title
        cmds.text(self.title)
        cmds.separator(height=20)

        # measurement settings
        cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(1, 145), (2, 250)])
        cmds.text(" -Import Settings:")
        cmds.text(" ")
        cmds.text(label='Measurements Filepath:')
        self.filepath = cmds.textField()

        # model folder filepath
        cmds.text(label='Model Folderpath:')
        self.model_folderpath = cmds.textField()
        cmds.text(" ")
        cmds.text(" ")
        cmds.text(" ")
        #cmds.text(" ")

        # Model specifications
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(1, 145), (2, 70)])
        cmds.text(" -Model Specicifactions:")
        cmds.text(" ")
        cmds.text("First Neuron:")
        self.firstNeur = cmds.intField(minValue=0, maxValue=399, value=235)
        cmds.text("Last Neuron:")
        self.lastNeur = cmds.intField(minValue=1, maxValue=400, value=240)
        cmds.text("Step Size:")
        self.neur_stepsize = cmds.intField(minValue=1, maxValue=400, value=1)


        # measurement steps
        # cmds.text(" -Cochlea Structures:")
        # cmds.text(" ")
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 70), (2, 75), (3, 70)])
        cmds.text("Internodes:")
        cmds.text("Show: ", align='right')
        self.show_internodes = cmds.checkBox(label=' ')

        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 70), (2, 75), (3, 70)])
        cmds.text("Sweep:")
        cmds.text("Import: ", align='right')
        self.import_sweeps = cmds.checkBox(label=' ', value=1)
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1, columnAttach=(1, 'left', 0), columnWidth=[(1, 395)])
        self.sweep_color = cmds.colorSliderGrp(label='Colour:', rgb=(0.15, 0.3, 0.5), columnAlign=[1, 'right'])

        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 70), (2, 75), (3, 70)])
        cmds.text("Cochlea:")
        cmds.text("Import: ", align='right')
        self.import_cochlea = cmds.checkBox(label=' ')
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1, columnAttach=(1, 'left', 0), columnWidth=[(1, 395)])
        self.cochlea_transparency = cmds.floatSliderGrp(field=True, label='Transparency:', minValue=0, maxValue=1,
                                                     value=0.9, columnAlign=[1, 'right'])

        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 70), (2, 75), (3, 70)])
        cmds.text("Tube:")
        cmds.text("Import: ", align='right')
        self.import_tube = cmds.checkBox(label=' ')
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1, columnAttach=(1, 'left', 0), columnWidth=[(1, 395)])
        self.tube_transparency = cmds.floatSliderGrp(field=True, label='Transparency:', minValue=0, maxValue=1,
                                                     value=0.9, columnAlign=[1, 'right'])

        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 70), (2, 75), (3, 70)])
        cmds.text("Nerve:")
        cmds.text("Import: ", align='right')
        self.import_nerve = cmds.checkBox(label=' ')
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1, columnAttach=(1, 'left', 0), columnWidth=[(1, 395)])
        self.nerve_transparency = cmds.floatSliderGrp(field=True, label='Transparency:', minValue=0, maxValue=1,
                                                      value=0, columnAlign=[1, 'right'])
        cmds.text(" ")
        cmds.text(" ")

        # Animation settings
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(1, 145), (2, 70)])
        cmds.text(" -Animation Settings:")
        cmds.text(" ")
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1, columnAttach=(1, 'left', 0), columnWidth=[(1, 395)])
        self.light_intensity = cmds.floatSliderGrp(field=True, label='Light Intensity:', minValue=0, maxValue=3,
                                                   value=1,
                                                   columnAlign=[1, 'right'])
        self.camera_radius = cmds.floatSliderGrp(field=True, label='Camera Radius:', minValue=1, maxValue=25, value=15,
                                                columnAlign=[1, 'right'])
        self.camera_start = cmds.floatSliderGrp(field=True, label='Camera Startpoint:', minValue=-360, maxValue=360,
                                                value=0,
                                                columnAlign=[1, 'right'])
        #cmds.text("create keyframes:")
        #self.keyframes = cmds.checkBox(label=' ')

        # Build model button
        cmds.setParent('..')
        cmds.separator(height=30)
        cmds.button(label='Build Model', bgc=[0.4, 0.65, 0.2], command=self.run_variables)

        # display new window
        cmds.showWindow()

    def run_variables(self, *args):
        path = cmds.textField(self.filepath, query=True, text=True)
        model_folderpath = cmds.textField(self.model_folderpath, query=True, text=True)
        firstNeur = cmds.intField(self.firstNeur, query=True, value=True)
        lastNeur = cmds.intField(self.lastNeur, query=True, value=True)
        neur_stepsize = cmds.intField(self.neur_stepsize, query=True, value=True)
        show_internodes = cmds.checkBox(self.show_internodes, query=True, value=True)
        import_sweeps = cmds.checkBox(self.import_sweeps, query=True, value=True)
        sweep_color = cmds.colorSliderGrp(self.sweep_color, query=True, rgbValue=True)
        import_cochlea = cmds.checkBox(self.import_cochlea, query=True, value=True)
        cochlea_transparency = cmds.floatSliderGrp(self.cochlea_transparency, query=True, value=True)
        import_tube = cmds.checkBox(self.import_tube, query=True, value=True)
        tube_transparency = cmds.floatSliderGrp(self.tube_transparency, query=True, value=True)
        import_nerve = cmds.checkBox(self.import_nerve, query=True, value=True)
        nerve_transparency = cmds.floatSliderGrp(self.nerve_transparency, query=True, value=True)
        #keyframes = cmds.checkBox(self.keyframes, query = True, value = True)
        light_intensity = cmds.floatSliderGrp(self.light_intensity, query=True, value=True)
        camera_radius = cmds.floatSliderGrp(self.camera_radius, query=True, value=True)
        camera_start = cmds.floatSliderGrp(self.camera_start, query=True, value=True)

        cmds.deleteUI(self.window, window=True)
        main(path, model_folderpath, firstNeur, lastNeur, neur_stepsize, show_internodes, import_sweeps, sweep_color, import_cochlea, cochlea_transparency,
                  import_tube, tube_transparency, import_nerve, nerve_transparency,
                  light_intensity, camera_radius, camera_start)

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

def import_voltage_traces(path):
    print("Import voltage traces...")
    measurements = read_decompress(path)
    # print(len(measurements))
    return measurements

def import_neuron_coordinates(model_folderpath):
    print("Import coordinates...")
    coords_filepath = model_folderpath + "\\ci_refine_list_mdl.pkl"
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

def import_sweeps_fnc(model_folderpath, sweep_color, disp_neur):
    filepath = model_folderpath + "\\Neurons\\"
    print("importing sweeps...")

    for i in disp_neur:
        filename = filepath + "sweep" + str(i + 1) + ".fbx"
        cmds.file(filename, i=True)

    # create new shader and assign a color to it
    sweep_shader = cmds.shadingNode('aiStandardSurface', asShader=1, name='ShaderSweeps')
    cmds.setAttr((sweep_shader + '.baseColor'), sweep_color[0], sweep_color[1], sweep_color[2], type='double3')

    cmds.select("Sweep", hierarchy=True)
    cmds.hyperShade(a=sweep_shader)
    cmds.select(clear=True)

def import_cochlea_fnc(model_folderpath, cochlea_transparency):
    print("importing cochlea model...")
    cochlea_path = model_folderpath + '\\human_CL_anime.stl'
    cochlea_model = cmds.file(cochlea_path, i=True)  # i = import
    objTransform = "human_CL_anime"
    objMesh = cmds.listRelatives(objTransform, shapes=True)[0]
    objSE = cmds.listConnections(objMesh, type="shadingEngine")[0]
    objMat = cmds.listConnections(objSE + ".surfaceShader")[0]
    cmds.setAttr(objMat + '.transparency', cochlea_transparency, cochlea_transparency, cochlea_transparency, type='double3')

def import_tube_fnc(model_folderpath, tube_transparency):
    print("importing tube model...")
    cochlea_path = model_folderpath + '\\ori_el_tube.stl'
    cochlea_model = cmds.file(cochlea_path, i=True)  # i = import
    objTransform = "ori_el_tube"
    objMesh = cmds.listRelatives(objTransform, shapes=True)[0]
    objSE = cmds.listConnections(objMesh, type="shadingEngine")[0]
    objMat = cmds.listConnections(objSE + ".surfaceShader")[0]
    cmds.setAttr(objMat + '.transparency', tube_transparency, tube_transparency, tube_transparency, type='double3')

def import_nerve_fnc(model_folderpath, nerve_transparency):
    print("importing nerve model...")
    cochlea_path = model_folderpath + '\\human_MDL_v5-extend_v4.stl'
    cochlea_model = cmds.file(cochlea_path, i=True)  # i = import
    objTransform = "human_MDL_v5_extend_v4"
    objMesh = cmds.listRelatives(objTransform, shapes=True)[0]
    objSE = cmds.listConnections(objMesh, type="shadingEngine")[0]
    objMat = cmds.listConnections(objSE + ".surfaceShader")[0]
    cmds.setAttr(objMat + '.transparency', nerve_transparency, nerve_transparency, nerve_transparency, type='double3')

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


def calculate_node_coords(curves, spans, disp_neur, only_nodes, model_folderpath):
    print("Calcualting coordinates of nodes...")
    node_coords = []
    node_created = []

    #comp_lens = pd.read_pickle('C:\\Users\\Rafael\\Documents\\GitHub\\Neuron_visualization_CI\\compartmentlengths_mm.pkl')
    comp_lens = pd.read_pickle(model_folderpath + "\\compartmentlengths_mm.pkl")
    # iterate through every neuron
    for i in range(len(disp_neur)):

        #calculate number of compartments
        curve_len = cmds.arclen(curves[i])
        compare_len = 0
        k = 0
        while compare_len < curve_len:
            compare_len += comp_lens[k]
            k += 1

        node_created.append([])
        node_coords.append([])
        span_param = 0

        # iterate through every node
        for j in range(k):
            #calculate node by relativity
            relativ = comp_lens[j] / compare_len
            pre_span = span_param
            span_param = min(spans[i], span_param + relativ * spans[i])

            if j == 0:
                inter_span = span_param
            else:
                inter_span = (pre_span + span_param) * 0.5 #Länge davor + Länge danach durch 2 ergibt die Mitte beider

            current_coords = cmds.pointOnCurve(curves[i], pr=inter_span, p=True)


            if only_nodes == 1:
                if comp_lens[j] <= 0.1: #node of ranvier sind alle kleiner als 0.1mm, internodes alle größer
                    node_coords[i].append(current_coords)
                    node_created[i].append(1)
                else:
                    node_created[i].append(0)
            else:
                node_coords[i].append(current_coords)
                node_created.append(1)
    print("node coords", node_coords, "\nnode created:", node_created)
            # print("Compartment:", j, "of", k)
            # print("Compartment length:", comp_lens[j], "/ compare length:", compare_len, "=", relativ)
            # print("spans[", i, "]:", spans[i], "span_param:", span_param)
            # print("current coords:", current_coords, "\n\n")

    return node_coords, comp_lens, node_created

def create_nodes(node_coords, disp_neur, material_name):
    print("creating nodes...")
    node_size = 0.03
    node = []
    shader = []
    cmds.group(em=True, name='nodes')

    # iterate through neurons
    for i in range(len(disp_neur)):
        print("Node creation... Neuron", disp_neur[i])
        node.append([])  # Neues Neuron erstellen
        shader.append([])
        current_group = cmds.group(em=True, name='neuron' + str(i), parent='nodes')
        #print("Iterating neuron", i, ":", len(node_coords))
        # iterate through nodes
        for j in range(len(node_coords[i])):

            #current_node = cmds.polySphere(r=node_size, name='mySphere#', sx=5, sy=5)
            current_node = cmds.sphere(r=node_size, s=4, name='mySphere#') # output of current_node is i.e ['mySphere1', 'makeNurbSphere1']
            node[i].append(current_node)
            cmds.parent(node[i][j][0], current_group) # here we have to reference to the first entry of current_node, otherwise parenting can not happen

            cmds.move(node_coords[i][j][0], node_coords[i][j][1], node_coords[i][j][2])


            # create new shader and assign a color to it
            current_shader, shading_Group = applyMaterial(current_node[0], material_name)
            #current_shader = cmds.shadingNode('standardSurface', asShader=1, name='Shader#')
            #cmds.setAttr((current_shader + '.baseColor'), 1, 1, 1, type='double3')
            shader[i].append(current_shader)
            cmds.sets(current_node[0], forceElement=shading_Group)
            #cmds.select(current_node[0])
            #cmds.hyperShade(a=current_shader)

    return node, shader

def applyMaterial(node, material_name): #
    if cmds.objExists(node): # create a shader with material_name & shading group node named for the object
        shd = cmds.shadingNode(material_name, name="%s_shader" % node, asShader=True)
        shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
        #cmds.sets(node, empty=True, forceElement=shdSG)
        return shd, shdSG

def create_frames(shader, measurements, node, disp_neur, only_nodes, comp_lens, node_created):
    print("creating frames...")
    # iterate through all neurons
    max_v = np.max(measurements)
    rest_v = measurements[0][0][-1]
    threshold = rest_v + 0.7 * abs(max_v - rest_v)
    yellow_threshold = 0.5 #nicht veränderbar
    radius_threshold = 0.5
    print("threshold",threshold, "max value", max_v,"rest v", rest_v)

    #iterate through all neurons
    for i in range(len(disp_neur)):
        print("Frame creation... Neuron", disp_neur[i])
        # iterate through all nodes
        l = -1
        for j in range(len(node_created[i])):
            if node_created[i][j] == 0:
                #print("j:", j, "node_created:", node_created[i][j])
                continue
            l += 1
            #print("j:", j, "node_created:", node_created[i][j], "l:", l)
            #pdb.set_trace()
            max_v_node = max(measurements[disp_neur[i]][j])
            toggle = 0
            color_toggle2 = 0
            radius_toggle2 = 0

            # iterate through all measurement steps
            for k in range(0, len(measurements[disp_neur[i]][j])):

                temp_meas = measurements[disp_neur[i]][j][k]
                rel = (temp_meas - threshold) / (max_v - threshold)

                #Anfangs Keyframe
                if k == 0:
                    green = 1
                    blue = 1
                    red = 1
                    cmds.setKeyframe(shader[i][l], time=k, attribute='baseColorR', value=red)
                    cmds.setKeyframe(shader[i][l], time=k, attribute='baseColorG', value=green)
                    cmds.setKeyframe(shader[i][l], time=k, attribute='baseColorB', value=blue)
                    cmds.setKeyframe(node[i][l], time=k, attribute='visibility', value=0)
                    #Über/unter ersten Threshold
                if toggle == 0 and rel > 0:
                    toggle = 1
                    blue = 1
                    radius = 0.01
                    visibility = 1
                    cmds.setKeyframe(shader[i][l], time=k, attribute='baseColorB', value=blue)
                    cmds.setKeyframe(node[i][l], time=k, attribute='visibility', value=visibility)
                    cmds.setKeyframe(node[i][l], time=k, attribute='radius', value=radius)
                elif toggle > 0 and rel < 0:
                    toggle = 0
                    blue = 1
                    radius = 0.01
                    visibility = 0
                    cmds.setKeyframe(shader[i][l], time=k, attribute='baseColorB', value=blue)
                    cmds.setKeyframe(node[i][l], time=k, attribute='visibility', value=visibility)
                    cmds.setKeyframe(node[i][l], time=k, attribute='radius', value=radius)

                #über/unter zweiten Threshold color:
                if color_toggle2 == 0 and rel > yellow_threshold:
                    color_toggle2 = 1
                    blue = 0
                    green = 1
                    cmds.setKeyframe(shader[i][l], time=k, attribute='baseColorB', value=blue)
                    cmds.setKeyframe(shader[i][l], time=k, attribute='baseColorG', value=green)
                if color_toggle2 == 1 and rel < yellow_threshold:
                    color_toggle2 = 0
                    blue = 0
                    green = 1
                    cmds.setKeyframe(shader[i][l], time=k, attribute='baseColorB', value=blue)
                    cmds.setKeyframe(shader[i][l], time=k, attribute='baseColorG', value=green)

                #über/unter zweiten Threshold Größe:
                if radius_toggle2 == 0 and rel > radius_threshold:
                    radius_toggle2 = 1
                    radius = 0.03
                    cmds.setKeyframe(node[i][l], time=k, attribute='radius', value=radius)
                elif radius_toggle2 == 1 and rel < radius_threshold:
                    radius_toggle2 = 0
                    radius = 0.03
                    cmds.setKeyframe(node[i][l], time=k, attribute='radius', value=radius)

                #peak
                if temp_meas == max_v_node:
                    #Color:
                    if rel <= yellow_threshold:
                        #keyframe yellow calculation
                        blue = min(1, max(0, 1 - 2 * rel))
                        cmds.setKeyframe(shader[i][l], time=k, attribute='baseColorB', value=blue)
                    else:
                        # keyframe orange calculation
                        green = min(1, max(0, 2 - 2 * rel))
                        cmds.setKeyframe(shader[i][l], time=k, attribute='baseColorG', value=green)

                    #Größe:
                    if rel <= radius_threshold:
                        #radius calculation
                        radius = 0.01 + 0.02 * rel / radius_threshold
                        cmds.setKeyframe(node[i][l], time=k, attribute='radius', value=radius)


def create_camera(disp_neur, node_coords, camera_start, camera_radius): # make a turntable camera for animation
    #create normal camera
    camera = cmds.camera()  # creates a camera
    cameraName = camera[0]  # gives back the camera name
    #cameraShape = camera[1]
    x_sum = 0
    y_sum = 0
    z_sum = 0
    counter = 0
    for i in range(len(disp_neur)):
        for j in range(len(node_coords[i])):
            x_sum += node_coords[i][j][0]
            y_sum += node_coords[i][j][1]
            z_sum += node_coords[i][j][2]
            counter+= 1
        #x_sum += x_sum
        #y_sum += y_sum
        #z_sum += z_sum

    x_average = x_sum /counter
    y_average = y_sum /counter
    z_average = z_sum /counter
                
    sphere = cmds.sphere()
    cmds.setAttr(sphere[0] +'.translateX', x_average)
    cmds.setAttr(sphere[0] + '.translateY', y_average)
    cmds.setAttr(sphere[0] + '.translateZ', z_average)

    # set the aim to the calculated center sphere and use the up vector as upside down, because the model is upside down
    cmds.aimConstraint(sphere, cameraName, aimVector=(0, 0, -1), upVector = (0,-1,0))
    cmds.setAttr(sphere[0] + '.rotateY', camera_start) #set the camera start by rotating the center sphere

    circle = cmds.circle(nr=(0, -1, 0), r=camera_radius) # create circle around center sphere for motion path of camera
    cmds.setAttr(circle[0] + '.visibility', 0)  # motion path should never be seen
    cmds.parent(circle[0], sphere[0], relative=True)
    cmds.setAttr(sphere[0] + '.visibility', 0) # parent the motion path to the sphere so the center of the circle is the sphere location
    # before creation of path animation, already the rendersettings/timeslider settings (fps) should be done
    # constrain the camera to the circle path and set start time and end time of rotation
    cmds.pathAnimation(cameraName, stu=130, etu=600, curve=circle[0])

def create_light(light_intensity):
    Dommy = mutils.createLocator("aiSkyDomeLight", asLight=True)
    objTransform = "aiSkyDomeLight1"
    objMesh = cmds.listRelatives(objTransform, shapes=True)[0]
    cmds.setAttr(objMesh + ".intensity", light_intensity)

def main(path, model_folderpath, firstNeur, lastNeur, neur_stepsize, show_internodes, import_sweeps, sweep_color, import_cochlea, cochlea_transparency,
                  import_tube, tube_transparency, import_nerve, nerve_transparency,
                  light_intensity, camera_radius, camera_start):

    #if path == "1":
        #path = "C:\Users\Rafael\Desktop\praktikum bioanaloge\projektpraktikum_animation_ss2022\Rattay_2013_e7_o2.0_0.001000149883801424A.p"
    #if model_folderpath == "1":
        #model_folderpath = "C:\Users\Rafael\Desktop\praktikum bioanaloge\CL_geom_v2"

    ## cleaning the scene and all unused objects before creating new ones
    cmds.select(all=True)
    mySel = cmds.ls(sl=1)
    if len(mySel) != 0: # my current selection
        cmds.cutKey(mySel, s=True)  # delete key command
        cmds.delete()
        mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    ###################################################

    disp_neur = range(firstNeur, lastNeur, neur_stepsize)   #display neuron from ... to ...
    creation_frames = "yes"
    material_name= 'aiStandardSurface'
    only_nodes = 1 - show_internodes #das wird falschrum abgefragt, also kurz umdrehen
    if import_sweeps:
        import_sweeps_fnc(model_folderpath, sweep_color, disp_neur)
    if import_cochlea:
        import_cochlea_fnc(model_folderpath, cochlea_transparency)
    if import_tube:
        import_tube_fnc(model_folderpath, tube_transparency)
    if import_nerve:
        import_nerve_fnc(model_folderpath, nerve_transparency)

    vertices = import_neuron_coordinates(model_folderpath)
    measurements = import_voltage_traces(path) #path is the path from the UI for measurements filepath

    curves, spans = create_curves(vertices, disp_neur)
    node_coords, comp_lens, node_created = calculate_node_coords(curves, spans, disp_neur, only_nodes, model_folderpath)
    nodes, shader = create_nodes(node_coords, disp_neur, material_name)
    if creation_frames == "yes":
        create_frames(shader, measurements, nodes, disp_neur, only_nodes, comp_lens, node_created)
        create_camera(disp_neur, node_coords, camera_start, camera_radius) # camera_start gives the starting point of the camera during the animation
        create_light(light_intensity)
        
    print("deleting curves...")
    cmds.select("curves", hierarchy=True)
    cmds.delete()

    print("finished :)")

if __name__ == "__main__":
    ui_settings()
