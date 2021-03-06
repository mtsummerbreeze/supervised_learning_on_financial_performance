import csv
import os

cwd = os.getcwd()

data_type = 'real' #select 'real' or 'test' data

source1 = cwd + '/' + data_type + 'data/companylist.csv'
source2 = cwd + '/' + data_type + 'data/ratios.csv'
dow_jones = cwd + '/' + data_type + 'data/DowJonesMarketMonthly.csv'
risk_free = cwd + '/' + data_type + 'data/riskfree.csv'
output_path = cwd + '/output/output.csv'

##IMPORT
with open(source1, 'r') as fp:
    reader = csv.reader(fp, delimiter=',', quotechar='"')
    company_list = [row for row in reader]

with open(source2, 'r') as fp:
    reader = csv.reader(fp, delimiter=',', quotechar='"')
    ratios = [row for row in reader]

#Add PRC row to the table
output = ratios #store in modifyable table to not corrupt inital values
output[0].append(company_list[0][6]) #adds price header to list
#loop through both tables
for rowR in output:
    for rowC in company_list:
        if rowR[0] == rowC[0]: #company code must be the same
            if rowC[1][3:] == rowR[3][3:]: #public_date(ratios) must be the same as date(companylist) only looking at month and year (publishing dates by actual day can differ)
                rowR.append(rowC[6])

#Store modified data in a .csv file, which can then be used for analysis
def export_matrix_to_csv(output_path, matrix):
    with open(output_path, "w") as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerows(matrix)
    print('export done successfully')


#transpose a matrix
def transpose_matrix(matrix):
    N = len(matrix)
    C = len(matrix[0])
    column_list = [[matrix[row][column] for row in range(N)] for column in range(C)]
    return column_list

#extracts a column from matrix with header = columnheader and returns it as an array
def extract_column(matrix, columnheader):
    i = 1
    #calculates position in which the column with columnheader is located in the original matrix
    for item in matrix[0]:
        if item == columnheader:
            column_position = i
        i += 1
    t_matrix = transpose_matrix(matrix)
    column = t_matrix[column_position-1]
    column = column[1:] #remove header
    c_column = [float(numeric_string) for numeric_string in column] #convert string array into float array
    return c_column

#generates support array that consists of all transitions in the permno codes
def get_support_array(matrix):
    i = 0;
    support_array = []
    for row in matrix:
        if row[0] != matrix[i-1][0]:
            support_array.append(i)
        i += 1
    support_array.pop(0)
    for item in support_array:
        item += 0
    return support_array

#calculates a return of a given array (price) for a certain amount of months (basic value is one month return)
def calculate_return(price,support_array, months = 1):
    i = 0
    z = -1
    r3turn = []
    r3turn.append('return' + str(months) + 'months')
    while i in range(0,len(price)):
        if i+1 in support_array or z in range(0,months):
            r3turn.append('NaN')
            if z == months-1:
                z = -1
            else:
                z += 1
        else:
            r3turn.append((price[i]/price[i-months])-1)
        i += 1
    return r3turn

#writes the return into the last column of output
def add_return_to_output(r3turn, output):
    i = 0
    for row in output:
        row.append(r3turn[i])
        i += 1
    return None

#generation of support array
support_array = get_support_array(ratios)
#extraction of the price-data
price = extract_column(ratios, 'PRC')
#addition of all wanted returns, here: 1-12 month return
for i in range(1,13):
    add_return_to_output(calculate_return(price,support_array, i),output)

#writing the derived table into the output file
export_matrix_to_csv(output_path,output)



