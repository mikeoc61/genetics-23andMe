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

# Define CONSTANTS used in program

BLUE = '\033[94m'
GREEN = '\033[92m'
WARN = '\033[93m'       # Yellow color
MATCH = '\033[91m'      # Red color
ENDC = '\033[0m'        # Reset color
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

FILEPATTERN = 'genome_*.txt'   # Pattern of filenames for 23andMe data

# Define data structures to hold genomic data

snps = {}                   # Raw data - rsid : [chromosome, position, genotype]
geno_cnt = {}               # Key:value pair = genotype : # counted
chromo_cnt = {}             # Key:value pair = chromosome : # of positions

chromosome = []             # List of unique chromosome pairs identified
position = []               # Not currently doing anything with this data
genotype = []               # List of unique genotypes identified


def main():

    # Generate a list of all files in current directory that match pattern

    myfiles = glob.glob('./' + FILEPATTERN)

    if len(myfiles) == 0:
        print("Sorry, didn't find any files matching: " + FILEPATTERN)
        sys.exit()
    else:
        print('Found the following file names matching: ' + FILEPATTERN + '\n')

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

    # Read file contents into dictionary data structure and close file
    # Use ID as primary key with chromosome, position and genotype as
    # associated values - {rsid : [chromosome, position, genotype]}

    FILEPATH = os.path.abspath(myfiles[i-1])
    print('Opening: ' + FILEPATH)

    cnt = 0
    firstline = True

    with open(FILEPATH, 'r') as fp:
        for line in fp:
            items = line.split()
            if firstline:
                firstline = False               # Only check first line
                if '23andMe' in items:          # Confirm correct header
                    continue
                else:
                    print('File does not appear to be 23andMe raw data')
                    sys.exit()

            if items[0].startswith('#'):        # Ignore subsequent comments
                continue
            else:                               # Load valid data into dict
                id, values = items[0], items[1:]
                snps[id] = values
                cnt += 1
    fp.close()

    print('\nImported total of {} SNPs...\n'.format(cnt))

    # First pass through raw data to identify unique chromosomes and genotype
    # information and number of External vs. Internal references.

    i_cnt, rs_cnt = 0, 0
    last_position = ''

    # Iterate through data to create lists and counts of unique elements
    # Note: Male data will have separate X and Y data so treat as XY pair

    print("Processing Chromosome: ", end='')

    for key, val in snps.items():
        if val[0] == 'MT':              # Not interested in MT records
            break

        if key.startswith('rs'):         # rsid or internal?
            rs_cnt += 1
        else:
            i_cnt += 1

        if val[0] == 'X' or val[0] == 'Y':
            val[0] = 'XY'

        if val[0] not in chromosome:
            chromosome.append(val[0])
            print("\n{:>2}:".format(val[0]), end='', flush=True)

        if not (rs_cnt + i_cnt) % 1000:
            print('.', end='', flush=True)

        if val[1] != last_position:     # Position data
            position.append(val[1])
            last_position = val[1]

        if val[2] not in genotype:      # Genotype
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
    # Warn if SNP is one of concern and individual variant is '--'

    print('\nScanning Found My Fitness data for possible issues\n')

    for key, myval in snps.items():
        if key in FMF_NOTEWORTHY:
            if (myval[2] != FMF_NOTEWORTHY[key][1]) and (myval[2] != '--'):
                color = BLUE
            elif (myval[2] != FMF_NOTEWORTHY[key][1]) and (myval[2] == '--'):
                color = WARN
            elif myval[2] == FMF_NOTEWORTHY[key][1]:
                color = MATCH
            else:
                color = False

            if color:
                print('{:>2} {:10} {}{}:  {}  {}{:10} {}'.format(val[0], key, \
                    color, myval[2], FMF_NOTEWORTHY[key][1], ENDC, \
                    FMF_NOTEWORTHY[key][0], FMF_NOTEWORTHY[key][2]))
                print('   See: https://www.snpedia.com/index.php/{}'.format(key))


if __name__ == "__main__":
  main()
