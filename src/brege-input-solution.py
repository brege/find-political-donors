#!/usr/bin/env python3
import numpy as np
import sys
from datetime import datetime

def help():
    print("""
 Usage: 
    
 python3 ./src/brege-solution.py ./input/itcont.txt ./output/medianvals_by_zip.txt ./output/medianvals_by_date.txt
""")

def main():

    input_file = sys.argv[1]

    try:
        output_zip_file = sys.argv[2]
    except:
        help()
        print(" Error: No output file specified for calculating median values by zip code")
        sys.exit(1)

    try:
        output_date_file = sys.argv[3]
    except:
        help()
        print(" Error: No output file specified for calculating median values by date")
        sys.exit(1)


    # load the main data file
    params=np.genfromtxt(input_file,delimiter="|",dtype=np.str)
    params.astype(str)

    # write to the(se) output file(s)
    fd=open(str(output_date_file),"w")
    fz=open(str(output_zip_file),"w")

    # add clear front matter to output files so visualizers
    # know what's in it
    f=[fd,fz]
    for i in range(len(f)):
        print("# [1] CMTE_ID", file=f[i])
        print("# [2] ZIP_CODE", file=f[i])
        print("# [3] TRANSACTION_DT", file=f[i])
        print("# [4] TRANSACTION_AMT", file=f[i])
        print("# [5] OTHER_ID", file=f[i])

    # the main program
    for i in range(len(params)):
        CMTE_ID=params[i][0]
        ZIP_CODE=params[i][10]
        TRANSACTION_DT=params[i][13]
        TRANSACTION_AMT=params[i][14]
        OTHER_ID=params[i][15]


        # skip lines with non-individual contributions
        if OTHER_ID != "":
            print("Skipping CMTE_ID = ",CMTE_ID," since OTHER_ID is non-empty.",sep='')
            continue

        # skip lines with empty CMTE_ID and TRANSACTION_AMT fields
        if CMTE_ID == "" or TRANSACTION_AMT == "":
            print("Skipping an entrie with empty CMTE_ID or TRANSACTION_AMT.",sep='')
            continue

        # we only care about the main zip code, so truncate the 
        # plus-four code off
        if int(str(ZIP_CODE))>99999:
            ZIP_CODE=str(ZIP_CODE)[0:5]

        # append to the date output file if zip code is valid 
        if len(str(ZIP_CODE))==5:
            print(
                    CMTE_ID
                    ,ZIP_CODE
                    ,TRANSACTION_DT
                    ,TRANSACTION_AMT
                    ,sep="|"
                    ,file=fd)

        # if the date of the transaction is malformed do not append to
        # file 
        try:
            datetime.strptime(TRANSACTION_DT, "%m%d%Y")
            print(
                    CMTE_ID
                    ,ZIP_CODE
                    ,TRANSACTION_DT
                    ,TRANSACTION_AMT
                    ,sep="|"
                    ,file=fz)
        except ValueError as err:
            print("Malformed transaction date, ",TRANSACTION_DT,", used for CMTE_ID = ",CMTE_ID,".",sep='')

main()
