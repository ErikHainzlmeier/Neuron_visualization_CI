import numpy as np
import fpzip
import pickle
import importlib
import peakutils as peak
#import thorns as th
#from sys import getsizeof
#from brian2 import *

import functools
import operator

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm

#import voltage traces
'''
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
	while np.shape(decompressed)[0]==1:
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


def main():
    save_path = "C:\\Users\\Rafael\\Desktop\\praktikum bioanaloge\\projektpraktikum_animation_ss2022\\Rattay_2013_e7_o2.0_0.001000149883801424A.p"
    #data = pd.read_pickle(filepath)

    measurements = read_decompress(save_path)
    print(len(measurements))


    plot = 'yes'

    if plot == 'yes':

        starting_neuron = 0
        number_of_plots = range(starting_neuron,400,50)
        number_of_nodes = len(measurements[starting_neuron])
        number_of_timesteps = len(measurements[starting_neuron][0])
        time_steps = list(range(number_of_timesteps))

        for k in number_of_plots:
            current_neuron = starting_neuron +k
            fig = plt.figure(k)
            ax = fig.add_subplot(111, projection='3d')

            for i in range(number_of_nodes):
                x_vals = time_steps
                y_vals = i + np.zeros(number_of_timesteps)
                z_vals = measurements[current_neuron][i][0:number_of_timesteps]
                ax.plot(x_vals, y_vals, z_vals)

            plt.xlabel('timestep')
            plt.ylabel('compartment')

            plt.show()

'''



main()