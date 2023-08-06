# program name: an0_exploratory.py

# optional arguments: --plot/-p + 3 column names (eg. -p bmi sex class)
#                     --debug/-x
#                     --header/-H to determine if a line of headers is present
#
# 

print('========================================================================================')
print('========================================================================================')

print('> start of program an0_exploratory.py')
print('> ONLY USES WINE.DATA ')
# Class,Alcohol,Malic acid,Ash,Alcalinity of ash,Magnesium,Total phenols,
# Flavanoids,Nonflavanoid phenols,Proanthocyanins,Color intensity,Hue,
# OD280/OD315 of diluted wines,Proline

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

print('> define key_exist function')
def key_exist(dd, chkkey):
    print('> does ', chkkey, 'exist?')
    if chkkey in dd:
        print("    Yes")
    else:
        print("    No, quitting")    
        exit()

def plot_data(dd, col1, col2, col3, debug=False):
    print('> executing plot_data function')
    # dd: data_dictionary
    print('> plotting ', col1, 'x', col2, '- categorical:', col3)
    key_exist(dd, col1)
    key_exist(dd, col2)
    key_exist(dd, col3)

# numpy.fromiter(iterable, dtype, count=-1)
# Create a new 1-dimensional array from an iterable object.
    x = np.fromiter(dd[col1], dtype=float)  # need these for the lines below
    y = np.fromiter(dd[col2], dtype=float)

    df = pd.DataFrame.from_dict(dd) 
    #print(df)
    colors = {1:'red', 2:'orange', 3:'green', 4:'blue', 5:'violet'}
    plt.scatter(df[col1], df[col2], c=df[col3].apply(lambda a: colors[a]))

    xp = np.linspace(np.amin(x), np.amax(x), 100)  #only works for numpy arrays
    for degree in range(1,4):
        weights = np.polyfit(x, y, degree)
        model = np.poly1d(weights)
        plt.plot(xp, model(xp), '-', label='degree='+ str(degree))
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.title(col1 + ' x ' + col2.format(x,y))
    plt.legend()
    plt.savefig("plot_" + col1 + '_' + col2 + ".png")
    plt.show()

    
print('> define get_type function')
def get_type(df, col, debug=False):
    print('> executing get_type')
    if isinstance(df[col], str):
        type = 'string'
    else:
        nuval = df[col].nunique()  # number of unique values 
        nvals = df[col].count()    # total number of values
        pct = nuval/nvals * 100
        print('    number of unique values: ' , nuval)
        print('    number of non-null values: ', nvals)
        print('    percent of unique values/total values: ', pct)
        if pct < 20:
            type = 'categorical'
        else:
            type = 'continuous'    
    print('    type: ', type)
    return type


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--plot',   type=str, nargs = 3,
        help='3 columns to plot, X, Y and categorical')
    parser.add_argument('-x', '--debug',  action="store_true", 
        help="only prints start of file")
    parser.add_argument('-H', '--header', action="store_true", 
        help="determines if a header is present")

    args = parser.parse_args()
    print(' ')
    print('    args:', args)
    print(' ')

    data_file = "wine.data"

    dlm = get_delim(data_file)    
    my_data = parse_file(data_file, dlm, debug=args.debug)

    data_dictionary = lines_to_dict(my_data, header=args.header)
    #print(data_dictionary)

    #print('args.plot:',args.plot)
    if args.plot != None: 
        plot_data(data_dictionary, col1= args.plot[0], col2= args.plot[1], col3=args.plot[2],debug=args.debug)
    else:
        print('> plot argument missing, not plotting')

if __name__ == "__main__":
    main()
