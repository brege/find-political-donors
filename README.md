### The Challenge

This code is a solution to the Insight Data Science [Engineering challenge](https://github.com/InsightDataScience/find-political-donors/blob/master/README.md#input-file-considerations) which takes an input file in the same format as the data provided by the [Federal Election Commission](http://classic.fec.gov/finance/disclosure/ftpdet.shtml) and produces two outputs:

1. `./output/medianvals_by_zip.txt`, which contains a calculated median, total dollar ammount and number of contributions by recipient and zip code.

2. `./output/medianvals_by_date.txt`, which calculates the same quantities as 1.) except by date instead of zip code.

The source code can be found in `./src/brege-solution.py` within this repo.

To run the code:
```
./run.sh
```

### Dependencies

This code is written in and tested with Python 3.6.2, and depends on the following library:

 - python3-numpy

### Description of the solution

In my approach, I first check and enforce the items from "Input file considerations" to write two temporary input files containing only the fields that are required for performing the calculations.  These two temporary files aare each read in, used a paramater array, destroyed, then written with the solutions for median values by zip code and median values by date.

My solution passes the unit test that came from the [original repo](https://github.com/InsightDataScience/find-political-donors/tree/master/insight_testsuite), and also passes my own unit test that has duplication and catches the cases noted in the "Input file considerations" that the original input file doesn't entirely encompass.
