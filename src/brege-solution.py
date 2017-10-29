#!/usr/bin/env python3
import numpy as np
import sys
from datetime import datetime
from statistics import median
from decimal import Decimal, ROUND_HALF_UP

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

    if len(sys.argv) == 1:
        help()
    elif len(sys.argv) == 2 or len(sys.argv) == 3:
        print("Please specify exactly two output files")
        help()
    elif len(sys.argv) > 4:
        print("Too many arguments.")
        help()

    # load the main data file
    params=np.genfromtxt(input_file,delimiter="|",dtype=np.str)
    params.astype(str)

    # write to the(se) output file(s)
    fd=open(str(output_date_file),"w")
    fz=open(str(output_zip_file),"w")

    # The main script to clean the input given "Input file
    # considerations" from the challenge
    #
    # Output: './output/medianvals_by_zip.txt'
    #         './output/medianvals_by_date.txt'
    #
    # Note these output files will be over written when the analysis
    # is performed **after** this routine has created the proper
    # inputs

    for i in range(len(params)):
        CMTE_ID=params[i][0]
        ZIP_CODE=params[i][10]
        TRANSACTION_DT=params[i][13]
        TRANSACTION_AMT=params[i][14]
        OTHER_ID=params[i][15]

        # skip lines with non-individual contributions
        if OTHER_ID != "":
            print("Skipping CMTE_ID = "
                    ,CMTE_ID
                    ," since OTHER_ID is non-empty."
                    ,sep='')
            continue

        # skip lines with empty CMTE_ID and TRANSACTION_AMT fields
        if CMTE_ID == "" or TRANSACTION_AMT == "":
            print("Skipping an entrie with empty CMTE_ID or TRANSACTION_AMT.",sep='')
            continue

        # we only care about the main zip code, so truncate the 
        # plus-four code off
        if len(str(ZIP_CODE))>5:
            ZIP_CODE=str(ZIP_CODE)[0:5]

        # append to the zip code output file only if zip code is valid 
        if len(str(ZIP_CODE))==5:
            print(
                    CMTE_ID
                    ,ZIP_CODE
                    ,TRANSACTION_DT
                    ,TRANSACTION_AMT
                    ,sep="|"
                    ,file=fz)

        # append to the date output file only if the date is non-empty 
        # and properly formed
        try:
            datetime.strptime(TRANSACTION_DT, "%m%d%Y")
            print(
                    CMTE_ID
                    ,ZIP_CODE
                    ,TRANSACTION_DT
                    ,TRANSACTION_AMT
                    ,sep="|"
                    ,file=fd)
        except ValueError as err:
            print("Malformed transaction date, "
                    ,TRANSACTION_DT
                    ,", used for CMTE_ID = "
                    ,CMTE_ID
                    ,".  Skipping this entry."
                    ,sep='')

    fz.close()
    fd.close()

    # The routine to find the median contribution if the same recipient 
    # receives one or more contributions from the same zip code
    #
    # Output: './output/medianvals_by_zip.txt'

    fz=open(str(output_zip_file),"r")
    params=np.genfromtxt(output_zip_file,delimiter="|",dtype=np.str)
    fz.close()
    params.astype(str)

    fz=open(str(output_zip_file),"w")
    """
    # add clear front matter to the output file
    print("# [1] Recipient (CMTE_ID)", file=fd)
    print("# [2] Five digit Zip code", file=fd)
    print("# [3] Median transaction ammount for zip code", file=fd)
    print("# [4] Number of contributions for zip code ", file=fd)
    print("# [5] Total running contribution ammount", file=fd)
    """
    
    params=np.array(params)
    medianizer = []

    for i in range(len(params)):
        medianizer.append(int(params[i][3]))
        name=params[i,0]
        zipcode=params[i,1]

        index = np.where(np.logical_and(params[0:i,1]==zipcode
                                        ,params[0:i,0]==name))
        if len(index[0])>0:
            for l in range(len(index[0])):
                medianizer.append(int(params[index[0][l],3]))
                #print(medianizer)
        #else: 
        #    print("No matching name identifier..",i,name)
                
        print(
                params[i][0]
                ,params[i][1]
                ,Decimal(median(medianizer)).quantize(0,ROUND_HALF_UP)
                ,len(medianizer)
                ,sum(medianizer)
                ,file=fz
                ,sep='|'
                )
        medianizer=[]

    # The routine to find the median contribution if the same recipient 
    # receives one or more contributions on the same date
    #
    # Output: './output/medianvals_by_zip.txt'

    fd=open(str(output_date_file),"r")
    params=np.genfromtxt(output_date_file,delimiter="|",dtype=np.str)
    fd.close()
    params.astype(str)

    # sort by recipient, then TX date, then zip code, then ammount
    sorted_by_id=np.array(sorted(params, 
                                    key=lambda 
                                    ident: (ident[0],ident[2],ident[1],ident[3] ))) 
    fd=open(str(output_date_file),"w")
    """
    # add clear front matter to the output file
    print("# [1] Recipient (CMTE_ID)", file=fd)
    print("# [2] Date of contribution - mmddyyyy (TRANSACTION_DT)", file=fd)
    print("# [3] Median transaction ammount for date", file=fd)
    print("# [4] Number of contributions for date", file=fd)
    print("# [5] Total running contribution ammount", file=fd)
    """

    medianizer = []

    for i in range(len(sorted_by_id)):
        if i == 0:
            medianizer.append(int(sorted_by_id[i][3]))
            continue
        elif i > 0 and sorted_by_id[i][2] != sorted_by_id[i-1][2]:
            print(
                sorted_by_id[i-1][0]
                ,sorted_by_id[i-1][2]
                ,Decimal(median(medianizer)).quantize(0,ROUND_HALF_UP)
                ,len(medianizer)
                ,sum(medianizer)
                ,file=fd
                ,sep='|'
                )
            medianizer=[]
            medianizer.append(int(sorted_by_id[i][3]))
        else:
            medianizer.append(int(sorted_by_id[i][3]))
            if i < len(sorted_by_id)-1:
                continue
            elif i == len(sorted_by_id)-1:
                print(
                sorted_by_id[i-1][0]
                ,sorted_by_id[i-1][2]
                ,Decimal(median(medianizer)).quantize(0,ROUND_HALF_UP)
                ,len(medianizer)
                ,sum(medianizer)
                ,file=fd
                ,sep='|'
                )
                
main()
