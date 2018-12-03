import sys
import csv
import hashlib

def csv_valid(fname):
    csvfile = open(fname, 'rb')
    freader = csv.reader(csvfile)
    
    # read lines of the csv file
    freader.next()          # skip the title line
    row = freader.next()    # use the data row
    
    # Generate md5checksum using data excluding the last column
    #    Data are combined as a string using ',' as the delimiter
    #    Also make sure the string is of utf-8 encoding
    md5hash = hashlib.md5()
    md5input = ','.join(str(x) for x in row[:-1])
    print md5input
    md5hash.update(md5input.encode("utf-8"))
    md5output = md5hash.hexdigest()
    
    # compare with md5checksum came with the file
    if md5output == str(row[-1]).encode("utf-8"):
        return True

    return False

if __name__ == "__main__":
    # the csv file name is from the command line parameter
    fname = sys.argv[1]
    
    if csv_valid(fname):
        print('CSV checksum passed!')
    else:
        print('CSV checksum failed!')
