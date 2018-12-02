#
# python script for counting deliminaters in lines
#
START_WITH = "INSERT"
FILE = "treat.sql"
DELIMINATER = ","
N_EXPECT = 0

line_num = 0
nstart = len(START_WITH)
for line in open(FILE):
    line_num = line_num + 1
    if nstart==0 or line.strip()[0:nstart]==START_WITH:
        c = line.count(DELIMINATER)
        if N_EXPECT==0 or c!=N_EXPECT:
            print '%5s:  %5s' % (line_num, c)