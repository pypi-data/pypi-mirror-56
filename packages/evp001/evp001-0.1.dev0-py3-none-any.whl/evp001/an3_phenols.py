# program name: an3_phenols.py

# no optional arguments: Uses Wine data to display information about the proportions 
# of phenols: flavonoids to nonflavonoid
# 
# output: stacked bar chart
print('========================================================================================')
print('========================================================================================')

print('> start of program an3_phenols.py')
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
# attributes with health benefits: ma mg tphen proline

def plot_means2(dd):
    print('> executing plot_means2')
    df = pd.DataFrame(dd, columns = ['class','tphen','flav', 'nfphen']) 
    c1 = df.loc[(df['class'] == 1) ]  
    c2 = df.loc[(df['class'] == 2) ]
    c3 = df.loc[(df['class'] == 3) ] 

    mean_dict = {'class':[1,2,3],
                 'flav': [c1['flav'].mean(), c2['flav'].mean(), c3['flav'].mean()],
                 'nfphen': [c1['nfphen'].mean(), c2['nfphen'].mean(), c3['nfphen'].mean()],
                 'tphen': [c1['tphen'].mean(), c2['tphen'].mean(), c3['tphen'].mean()] } 

    mean_df = pd.DataFrame(mean_dict)
    print(mean_df)

    # fig = plt.figure()
    labels = ['Class 1', 'Class 2', 'Class 3']

    ind = np.arange(3) 
    width = 0.35
    fig, ax = plt.subplots()

    ax.bar(mean_df['class'], mean_df['flav'], width, color='lightcoral', label='Flavonoids')

    ax.bar(mean_df['class'], mean_df['nfphen'], width,bottom=mean_df['flav'], color='mediumaquamarine', label='Nonflavonoid Phenols')
    ax.set_ylabel('Means')
    ax.set_title('Mean Proportions of Falvonoids and Nonflavonoid Phenols')

    ax.set_xticks((1,2,3))
    ax.set_xticklabels(('Class 1','Class 2', 'Class 3'))

    ax.set_yticks(np.arange(0, 5, 1))
    ax.legend()
    plt.savefig("an3_phenols.png")
    plt.show()

def main():

    data_file = "wine.data"
    dlm = get_delim(data_file)    
    my_data = parse_file(data_file, dlm)
    data_dictionary = lines_to_dict(my_data)
    #print(data_dictionary)

    plot_means2(data_dictionary)

if __name__ == "__main__":
    main()
