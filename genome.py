#!/usr/bin/env python3

#########
#
# 23andMe raw data analysis program
#
# See: https://you.23andme.com/tools/data/download/
#
# Author: Michael E. OConnor
#
#########

import time
import sys
import os
import glob
from foundMyFitness import FMF_NOTEWORTHY

class GetSNPs:

    def __init__(self, pattern):

        '''When passed a filename pattern, identify desired file by prompting
           user with a list of possible choices based on pattern match in
           current user directory. 
        '''

        myfiles = glob.glob('./' + pattern)

        if len(myfiles) == 0:
            print("Sorry, didn't find any files matching: " + pattern)
            sys.exit()
        else:
            print('Found the following file names matching: ' + pattern + '\n')

        # Display indexed list of matching filenames, prompt use to pick one and
        # validate use input.

        for i in range(len(myfiles)):
            print('{}: {}'.format(i+1, myfiles[i]))

        response = input('\nPlease select number of file to process: ')

        try:
            i = int(response)
            if i > len(myfiles) or i == 0:
                raise ValueError
        except Exception as e:
            print('Sorry, valid input is 1 though {}'.format(len(myfiles)))
            # print(sys.exc_info())
            sys.exit()

        self.filename = os.path.abspath(myfiles[i-1])

    def getname(self):

        return self.filename

    def validate(self, file):

        '''Read file contents into dictionary data structure and close file
           Use ID as primary key with chromosome, position and genotype as
           associated values - {rsid : [chromosome, position, genotype]}
        '''

        firstline = True
        self.snps = {}

        with open(file, 'r') as fp:
            for line in fp:
                items = line.split()
                if firstline:
                    firstline = False               # Only check first line
                    if '23andMe' in items:          # Confirm correct header
                        continue
                    else:
                        print('File: {} does not appear to be 23andMe raw data'\
                            .format(os.path.relpath(file)))
                        sys.exit()

                if items[0].startswith('#'):        # Ignore subsequent comments
                    continue
                else:                               # Load valid data into dict
                    id, values = items[0], items[1:]
                    self.snps[id] = values
        fp.close()

    def dict(self):
        '''Simply return dictionary structure containing formatted SNP data'''

        return self.snps


def processSNPs(snps):

    # Define CONSTANTS used to control console character output color

    BLUE = '\033[94m'       # Blue
    GREEN = '\033[92m'      # Green
    WARN = '\033[93m'       # Yellow
    MATCH = '\033[91m'      # Red
    ENDC = '\033[0m'        # Reset to default
    BOLD = '\033[1m'        # Bold

    # Define data structures to hold genomic data

    geno_cnt = {}               # Key:value pair = genotype : # counted
    chromo_cnt = {}             # Key:value pair = chromosome : # of positions

    chromosome = []             # List of unique chromosome pairs identified
    position = []               # Not currently doing anything with this data
    genotype = []               # List of unique genotypes identified

    # First pass through raw data to identify unique chromosomes and genotype
    # information and number of External vs. Internal references.

    print("\nProcessing {} SNPs sorted by Chromosome".format(len(snps)), end='')\

    i_cnt, rs_cnt = 0, 0
    last_position = ''

    # Iterate through data to create lists and counts of unique elements
    # Note: Male data will have separate X and Y data so treat as XY pair

    for key, val in snps.items():

        if key.startswith('rs'):         # rsid or internal?
            rs_cnt += 1
        else:
            i_cnt += 1

        if val[0] == 'X' or val[0] == 'Y':
            val[0] = 'X?'

        if val[0] not in chromosome:        # Chromosome
            chromosome.append(val[0])
            print("\n{:>2}:".format(val[0]), end='', flush=True)

        if not (rs_cnt + i_cnt) % 1000:
            print('.', end='', flush=True)

        if val[1] != last_position:         # Position data
            position.append(val[1])
            last_position = val[1]

        if val[2] not in genotype:          # Genotype
            genotype.append(val[2])

    print("\n\nDetected: {} chromosomes, {} positions, {} genotypes\n".\
            format(len(chromosome), len(position), len(genotype)))

    print("rsID count: {}, Internal ID count: {}".format(rs_cnt, i_cnt))

    # Output a sorted list of each unique genotype and number of occurances.
    # First, initialize dictionary using genotype as key with value set to 0.
    # Then, scan all SNP records updating the count for each unique genotype.
    # Finally, sort the dictionary to produce a list of tuples containing
    # unique genotypes and correspondng number of occurance and print

    # Initialize counters

    for gt in genotype:
        geno_cnt[gt] = 0

    for ct in chromosome:
        chromo_cnt[ct] = 0

    # Re-scan raw data to count number of positions associated with each
    # Chromosome and unique genotype

    print('\nCalculating number of unique occurrences per genotype\n')

    for key, val in snps.items():

        try:
            chromo_cnt[val[0]] += 1
            geno_cnt[val[2]] += 1
        except:
            # print('.', end='', flush=True)
            continue

    # Reverse sort and display results

    sorted_cnt = sorted(geno_cnt.items(), key=lambda kv: kv[1], reverse=True)

    for item in sorted_cnt:
        print("Genotype: {:2} = {:6}".format(item[0], item[1]))

    print('\nNumber of positions per chromosome pair\n')

    sorted_cnt = sorted(chromo_cnt.items(), key=lambda kv: kv[1], reverse=True)

    for item in sorted_cnt:
        print("Chromosome: {:2} = {:5}".format(item[0], item[1]))

    # Rescan SNPs for match with Found My Fitness data.
    # Display RED if RAW Variant and FoundMyFitness varient are identical
    # Display BLUE if RAW and FoundMyFitness variants are complementary
    # Warn if SNP is one of concern and reported raw data variant is '--'

    print('\nScanning Found My Fitness data for possible issues\n')

    for key, val in FMF_NOTEWORTHY.items():
        if key.startswith('*'):
            key = key[1:]           # Strip away first character
        if key in snps:
            if val[1] == snps[key][2]:
                color = MATCH
            elif (val[1] == 'GG') and (snps[key][2] == 'CC'):
                color = BLUE
            elif (val[1] == 'CC') and (snps[key][2] == 'GG'):
                color = BLUE
            elif (val[1] == 'CT') and (snps[key][2] == 'AG'):
                color = BLUE
            elif (val[1] == 'AC') and (snps[key][2] == 'GT'):
                color = BLUE
            elif (val[1] == 'AG') and (snps[key][2] == 'CT'):
                color = BLUE
            elif (val[1] == 'TT') and (snps[key][2] == 'AA'):
                color = BLUE
            elif (val[1] == 'AA') and (snps[key][2] == 'TT'):
                color = BLUE
            elif (snps[key][2] == '--'):
                color = WARN
            else:
                color = False

            if color:
                print('{:>2} {:10} {}{}:{}  {}{:10} {}'.format(snps[key][0], key, \
                    color, snps[key][2], val[1], ENDC, val[0], val[2]))
                print('   See: https://www.snpedia.com/index.php/{}\n'.format(key))


def main():

    # Given a specific file name pattern, identify specific file of interest,
    # validate it appears to be correct format, read contents into data
    # dictionary structure and analyze

    PATTERN = 'genome_*.txt'

    file = GetSNPs(PATTERN)         # Determine raw file based on pattern
    fp = file.getname()             # Determine path to raw 23andMe data file
    file.validate(fp)               # Confirm that file is correct format
    snps = file.dict()              # If so, return contents as dictionary
    processSNPs(snps)               # Analyze data, output results


if __name__ == "__main__":
  main()
