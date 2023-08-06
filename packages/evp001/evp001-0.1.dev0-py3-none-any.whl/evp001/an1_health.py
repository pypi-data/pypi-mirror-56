# program name: an1_health.py

# no optional arguments: Uses Wine data to display information about whether certain 
# classes are higher in healthy attributes
# 
# output: side-by-side bar charts

print('========================================================================================')
print('========================================================================================')

print('> start of program wine_analysis2.py')
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

def plot_means(dd):
    df = pd.DataFrame(dd, columns = ['class','ma', 'mg', 'tphen', 'proline']) 
    #print(df)
    c1 = df.loc[(df['class'] == 1) ]  
    c2 = df.loc[(df['class'] == 2) ]
    c3 = df.loc[(df['class'] == 3) ] 
    # get means of each health attribute by class
    mean_dict = {'class':[1,2,3],
                 'ma': [c1['ma'].mean(), c2['ma'].mean(), c3['ma'].mean()],
                 'mg': [c1['mg'].mean(), c2['mg'].mean(), c3['mg'].mean()],
                 'tphen': [c1['tphen'].mean(), c2['tphen'].mean(), c3['tphen'].mean()],
                 'proline': [c1['proline'].mean(), c2['proline'].mean(), c3['proline'].mean()] } 
    # print(mean_dict)
    mean_df = pd.DataFrame(mean_dict)
    print(mean_df)

    labels = ['Class 1', 'Class 2', 'Class 3']
    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars
    fig, ax = plt.subplots()

    rects1 = ax.bar(x -0.3, mean_df['ma'], width, label='Malic Acid', color='firebrick')
    rects2 = ax.bar(x -0.1, mean_df['mg']/100, width, label='Magnesium/100', color='rebeccapurple')
    rects3 = ax.bar(x + 0.1, mean_df['tphen'], width, label='Total Phenols',color='olivedrab')
    rects4 = ax.bar(x + 0.3, mean_df['proline']/1000, width, label = 'Proline/1000', color = 'saddlebrown')

    ax.set_ylabel('Mean Values of Attributes')
    ax.set_title('Mean Values of Beneficial Attributes for Each Class')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.savefig("an1_health.png")
    plt.show()

def main():

    data_file = "wine.data"
    dlm = get_delim(data_file)    
    my_data = parse_file(data_file, dlm)
    data_dictionary = lines_to_dict(my_data)
    #print(data_dictionary)

    plot_means(data_dictionary)

if __name__ == "__main__":
    main()
