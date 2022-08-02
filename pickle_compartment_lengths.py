import csv
import pickle

compartmentlengths_array = []
with open('R13_2.3mm_compartment_lengths.csv', newline='') as inputfile:
    # transforming the compartmentlengths from the csv file from meter to millimeter in order to make them the same
    # unit as the coordinates for the neurons
    for row in csv.reader(inputfile):
        compartmentlengths_array.append(float(row[0])*1e3)

with open('compartmentlengths_mm.pkl', 'wb') as f:
    pickle.dump(compartmentlengths_array, f)

with open('centercoordinates.pkl', 'rb') as f:
    results = pickle.load(f)

#results = np.array(results)


print(results)
