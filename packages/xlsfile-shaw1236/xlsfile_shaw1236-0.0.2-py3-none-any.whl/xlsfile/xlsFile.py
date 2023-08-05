## Purpose: Handle read?write of Excel and CSV files
## Date   : Nov 19, 2019
## Author : Simon Li
'''
Usage  : 
from xlsfile.xlsFile import xlsFile 

Prerequisite modules
-pandas@0.25.3
-openpyxl3.0.1 
-xlrd@1.2.0
'''
import csv
import pandas as pd

class xlsFile:
    def __init__(self):
        pass   # dummy

    @staticmethod
    def read(xlsfile):
        df = pd.read_excel(xlsfile) 
        contents = []        
        for idx in df.index:             # Row of the working sheet
            row = {}
            for col in df.columns:       # Column of the working sheet
                row[col] = df[col][idx]  # assignment of each row
            contents.append(row)         # collect each row 
        return contents                  #[{"col1": v1, "col2": v2, ...}, {"col1": v1, "col2": v2, ...}]

    @staticmethod
    def write(xlsfile, data):
        df = pd.DataFrame(data)
        writer = pd.ExcelWriter(xlsfile)
        df.to_excel(writer, 'Sheet1', index=False)
        writer.save()

    @staticmethod
    def readcsv(csvfile, delimitor = ',', heading = True):
        contents = []
        with open(csvfile, newline = '') as csvDataFile:
            csvReader = csv.reader(csvDataFile, delimiter = delimitor)
            
            # Get the headings
            headers = {}     # {1: "h1", 2: "h2", ...}
            row_count = 0
            for row in csvReader:
                row_count += 1

                # Headings
                if row_count == 1:  # Retrieval of Headings
                    col = 1
                    for idx in row:
                        headers[col] = idx if heading else "Column%d" % col
                        col += 1

                    if heading:   # skip the heading
                        continue

                # Contents
                col = 1
                dict = {}
                for idx in row:
                    dict[headers[col]] = idx
                    col += 1
                contents.append(dict)

        return contents  #[{"col1": v1, "col2": v2, ...}, {"col1": v1, "col2": v2, ...}]         
            
    @staticmethod
    def writecsv(csvfile, contents, delimitor = ','):
        myFile = open(csvfile, 'w', newline = '')
        with myFile:
            writer = csv.writer(myFile, delimiter = delimitor)
            #writer.writerows(contents)
            # [{"col1": v1, "col2": v2, ...}, {"col1": v1, "col2": v2, ...}]   
            writer.writerows([contents[0].keys()])  # headings
            for row in contents:
                writer.writerows([row.values()])

    @staticmethod
    def xls2csv(xlsfile, csvfile, delimitor = ','):
        contents = xlsFile.read(xlsfile)
        xlsFile.writecsv(csvfile, contents, delimitor)

    @staticmethod
    def csv2xls(csvfile, xlsfile, csvdelimitor = ','):
        contents = xlsFile.readcsv(csvfile, csvdelimitor)
        xlsFile.write(xlsfile, contents)

if __name__ == '__main__':
    ## Csv file testing
    print("Test csv file")
    contents = xlsFile.readcsv("test2.csv")
    xlsFile.writecsv("test3.csv", contents)

    input = {}
    input["name"] = ["Test1", "Test2", "Test3"]
    input["email"] = ["test1@gmail.com", "test2@yahoo.com", "test3@gmail.com"]
    input["name"].append("Test4") 
    input["email"].append("test@yahoo.com") 

    filename = "testfamily.xlsx"

    ## Excel file test
    print("\nExcel file test")
    xlsFile.write(filename, input)
    contents = xlsFile.read(filename)
    print(contents)

    ## Excel to csv
    print("\nExcel to csv")
    xlsFile.xls2csv(filename, filename.replace(".xlsx", ".csv"))

    ## csv to Excel
    print("\ncsv to Excel")
    xlsFile.csv2xls(filename.replace(".xlsx", ".csv"), "testfamily2.xlsx")
    contents = xlsFile.read("testfamily2.xlsx")
    print(contents)