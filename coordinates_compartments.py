import math
#import sys
#sys.path.append("C:/Users/Erik/Documents/Elektrotechnik/Master/SS2022/Projektpraktikum/Neuron_visualization_CI")
#import _main_
import pandas as pd
import maya.api.OpenMaya as om


def geometry(x_dist, y_dist, z_dist, distance, pos1, restcomp_len):
    ratio = restcomp_len/distance
    pos1[0] = pos1[0] + ratio * x_dist
    pos1[1] = pos1[1] + ratio * y_dist
    pos1[2] = pos1[2] + ratio * z_dist
    geometry_point = []
    geometry_point.append(pos1[0])
    geometry_point.append(pos1[1])
    geometry_point.append(pos1[2])
    rest_distance = distance - restcomp_len
    cmds.polySphere(r=0.01)
    cmds.move(geometry_point[0], geometry_point[1], geometry_point[2])
    return geometry_point, rest_distance

def main():
    vertices = pd.read_pickle(r'C:\\Users\\Erik\\Documents\\Elektrotechnik\\Master\\SS2022\\Projektpraktikum\\ci_refine_list_mdl.pkl')
    comp_coords=[]
    #with open('compartmentlengths_mm.pkl', 'rb') as compartment_lengths:
    compartment_lengths = pd.read_pickle(r'C:\\Users\\Erik\\Documents\\Elektrotechnik\\Master\\SS2022\\Projektpraktikum\\Neuron_visualization_CI\\compartmentlengths_mm.pkl')

    for i in range(0, len(vertices)-1): # from neuron 0 to 399
        comp_coords.append([])
        k = 0
        for eachPos in range(0,len(vertices[i])-1):
            x_dist = (vertices[i][eachPos+1][0] - vertices[i][eachPos][0])
            y_dist = (vertices[1][eachPos+1][1] - vertices[i][eachPos][1])
            z_dist = (vertices[i][eachPos+1][2] - vertices[i][eachPos][2])
            distance = math.sqrt(x_dist**2 + y_dist**2 + z_dist**2)
            if compartment_lengths[k] <= distance:
                while compartment_lengths[k] <= distance:
                    geometry_point, rest_distance = geometry(x_dist, y_dist, z_dist, distance, vertices[i][eachPos], compartment_lengths[k])
                    comp_coords[i].append(geometry_point)
                    k += 1
                    distance = rest_distance

                compartment_lengths[k] = compartment_lengths[k] - distance

            else:
                compartment_lengths[k] = compartment_lengths[k] - distance
    print(len(compartment_lengths))




if __name__ == "__main__":
    main()