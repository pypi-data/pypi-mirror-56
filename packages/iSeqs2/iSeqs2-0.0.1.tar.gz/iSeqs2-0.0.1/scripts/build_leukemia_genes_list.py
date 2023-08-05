#!/usr/bin/env python

import argparse
import os.path
import sys


def get_genes_from_lgldb(lgld):
    """Parse the file downloaded from Leukemia gene and literature database (dbLGL)

    Parameters:

    lgld (string): the path of the downloaded file from dbLGL


    Returns:
    list:The list of genes from dbLGL
    """
    if os.path.isfile(lgld) == False:
        print("{} do not exists".format(lgld), file=sys.stderr)
        return -1
    
    genes_from_lgldb = []

    with open(lgld) as lgld:
        for line in lgld.readlines():
            splitted_line = line.split()
            if len(splitted_line) > 3:
                gene_symbol = splitted_line[1]
                genes_from_lgldb.append(gene_symbol)
                aliases = splitted_line[2].split("|")
                if aliases != ["-"]:
                    for alias in aliases: genes_from_lgldb.append(alias)
    return list(set(genes_from_lgldb))


def get_genes_from_cosmic(cosmic):
    """Parse the file downloaded from Catalogue of Somatic Mutations In Cancer (COSMIC)

    Parameters:

    cosmic (string): the path of the cancer_gene_census.csv file downloaded from COSMIC


    Returns:
    list:The list of genes from COSMIC
    """

    if os.path.isfile(cosmic) == False:
        print("{} do not exists".format(cosmic, file=sys.stderr))
        return -1

    genes_from_cosmic = []

    with open(cosmic) as cosmic:
        for line in cosmic.readlines():
            splitted_line = line.split(",")
            gene_symbol = splitted_line[0]
            genes_from_cosmic.append(gene_symbol)

            splitted_line = line.split('\"')
            if len(splitted_line) > 1:
                synonyms = splitted_line[-2].split(',')
                for synonym in synonyms: genes_from_cosmic.append(synonym)
    return list(set(genes_from_cosmic))



def main():
    parser = argparse.ArgumentParser(description="Builds a list of leukemia genes from Leukemia Gene Literature Database and COSMIC")
    parser.add_argument('-l', '--lgld', action='store', type=str, help="The flat file from human cancer leukemia genes", required=True)
    parser.add_argument('-c', '--cosmic', action='store', type=str, help="The flat file from COSMIC's Cancer Gene Census (CGC)", required=True)
    args = parser.parse_args()

    lgld = args.lgld
    cosmic = args.cosmic

    genes_from_lgldb = get_genes_from_lgldb(lgld)
    genes_from_cosmic = get_genes_from_cosmic(cosmic)

    genes_from_lgldb = set(genes_from_lgldb)
    all_genes = list(genes_from_lgldb.union(genes_from_cosmic))

    for gene in all_genes:
        print(gene)

    return 1

if  __name__ == "__main__":
    main()

