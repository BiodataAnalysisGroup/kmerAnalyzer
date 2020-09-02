# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 16:44:55 2019

@author: User
"""

import os
import numpy as np
import csv

def createCsvOutput(filename, treelist):

    directory = "Output/" + str(filename) + "/"
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    name = 'output.csv'
    path = directory + name

    with open(path, 'w') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        for i in range(len(treelist)):
            # Add contents of list as last row in the csv file
            csv_writer.writerow(treelist[i])

    return

def createCsvOutputForSeqIndices(filename, seqIndices, timesPerSeq):

    directory = "Output/" + str(filename) + "/"
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    name_1 = 'seqIndices.csv'
    path_1 = directory + name_1

    with open(path_1, 'w') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        for i in range(len(seqIndices)):
            # Add contents of list as last row in the csv file
            csv_writer.writerow(seqIndices[i])

    name_2 = 'timesPerSeq.csv'
    path_2 = directory + name_2

    with open(path_2, 'w') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        for i in range(len(timesPerSeq)):
            # Add contents of list as last row in the csv file
            csv_writer.writerow(timesPerSeq[i])

    return


def checkIfOutputFileExists(filename):
    
    directory = "Output/" + str(filename) + "/"
    name = 'output.csv'
    path = directory + name
    
    if os.path.exists(path):
        os.remove(path)
        print('Done')

    return
