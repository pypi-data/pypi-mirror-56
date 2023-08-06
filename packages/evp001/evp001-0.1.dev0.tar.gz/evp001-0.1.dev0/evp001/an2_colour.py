# program name: an2_colour.py

# no optional arguments: Uses Wine data to display information about the relationship of 
# various attributes with colour and hue 

print('========================================================================================')
print('========================================================================================')

print('> start of program an2_colour.py')
print('> import libraries')

import argparse
import os.path as op
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy.polynomial.polynomial import polyfit

print('> define convert_type function')
def convert_type(data_value):
    try:
        return int(data_value)
    except ValueError:
        try:
            return float(data_value)
        except ValueError:
            return data_value

print("> define get_delim function")
def get_delim(sourcefile1):
    print('> executing get_delim function')
    data = open(sourcefile1, 'r') 
    my_read_data = data.read()
    if my_read_data.find(',') > 0:
        print('    delimiter: comma')
        return ','
    else:
        print('    delimiter: space')
        return ' '      
    print(' ')

def lines_to_dict(lines, header=False):
    print('> executing lines_to_dict')
    # column_titles = ['Class','Alcohol','Malic acid','Ash','Alcalinity of ash','Magnesium','Total phenols','Flavanoids','Nonflavanoid phenols','Proanthocyanins','Color intensity','Hue',
    #     'OD280/OD315 of diluted wines','Proline']
    column_titles = ['class','alc','ma','ash','alkash','mg','tphen','flav','nfphen','pac','ci','hue',
        'od','proline']
    
    data_dict = {}
    for idx, column in enumerate(column_titles):
        data_dict[column] = []
        for row in lines:
            data_dict[column] += [row[idx]]
    return data_dict

def parse_file(data_file, dlm, debug=False):   # took delimiter out
    print('> executing parse_file')
    # Verify the file exists
    assert(op.isfile(data_file))

    # open it as a csv 
    with open(data_file, 'r') as fhandle:
        csv_reader = csv.reader(fhandle, delimiter=dlm)
        # Add each line in the file to a list
        lines = []
        if debug:
            count = 0
        for line in csv_reader:
            if debug:
                if count > 2:
                    break
                count += 1
            newline = []
            for value in line:
                newline += [convert_type(value)]
            if len(newline) > 0:
                lines += [newline]

    print('> view a few lines')
    print(' ')
    for line in lines[0:2]:
        print(line)
    print(' ')
    # Return all the contents of our file
    return lines


# class','alc','ma','ash','alkash','mg','tphen','flav','nfphen','pac','ci','hue',
#        'od','proline

    
def plot_data3(dd, col1, label1, 
                col2a, col2b,
                label2a, label2b, n,
                debug=False):
    df = pd.DataFrame.from_dict(dd) 
    x = np.fromiter(dd[col1], dtype=float)  # need these for the lines below
    y1 = np.fromiter(dd[col2a], dtype=float)
    y2 = np.fromiter(dd[col2b], dtype=float)

    # print(df)  
    fig, ax1 = plt.subplots()
    plt.title(label1 + ' by ' + label2a + ' and ' + label2b)

    clra = 'indigo'
    ax1.set_xlabel(label1)
    ax1.set_ylabel(label2a, color=clra)  # left side

    ax1.scatter(df[col1], df[col2a], color=clra, marker = '^')

    xp = np.linspace(np.amin(x), np.amax(x), 100)  #only works for numpy arrays
    weights = np.polyfit(x, y1, 1)
    model = np.poly1d(weights)
    plt.plot(xp, model(xp), '-', c=clra)
    ax1.tick_params(axis='y', labelcolor=clra)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    clrb = 'darkgreen'
    ax2.set_ylabel(label2b, color=clrb)  # we already handled the x-label with ax1
    # ax2.plot(df[col1], df[col2b], color=color)
    ax2.scatter(df[col1], df[col2b], color= clrb)
    ax2.tick_params(axis='y', labelcolor=clrb)

    xp = np.linspace(np.amin(x), np.amax(x), 100)  #only works for numpy arrays
    weights = np.polyfit(x, y2, 1)
    model = np.poly1d(weights)
    plt.plot(xp, model(xp), '-', c=clrb)
    ax1.tick_params(axis='y', labelcolor=clra)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig('an2_colour' + n + '.png')
    plt.show()

# Cases where there is a possible correlation with colour intensity or hue. 
# color intensity:
# check against :     alc, flav, od, proline
# hue:
# check against:    ma, tphen, flav, pac, od

def main():

    data_file = "wine.data"
    dlm = get_delim(data_file)    
    my_data = parse_file(data_file, dlm)
    data_dictionary = lines_to_dict(my_data)
    #print(data_dictionary)

    plot_data3(data_dictionary, 'ci', 'Colour Intensity', 'alc', 'flav', 'Alcohol', 'Flavonoids', '1')
    plot_data3(data_dictionary, 'hue', 'Hue', 'pac', 'od', 'Proanthocyanidins', 'OD280/OD315 of Diluted Wines', '2')

if __name__ == "__main__":
    main()
