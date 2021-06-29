# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 16:44:55 2019

@author: User
"""

import os
import numpy as np
import shutil
import pandas as pd

def clearingFolders(folder):
    
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    
    os.makedirs(folder)
    
    return

def createCsvOutput(filename, treelist):

    directory = "Output/" + str(filename) + "/"
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    name = 'output.csv'
    path = directory + name

    df = pd.DataFrame(treelist, columns = ['K-mer', 'Length', 'Count', 'Evaluation'])
    df.to_csv(path, index=False)
    
    return

def createCsvOutputForSeqIndices(filename, seqIndices, timesPerSeq):

    directory = "Output/" + str(filename) + "/"
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    name_1 = 'seqIndices.csv'
    path_1 = directory + name_1

    df = pd.DataFrame(seqIndices)
    df.to_csv(path_1, index=False,header=False)


    name_2 = 'timesPerSeq.csv'
    path_2 = directory + name_2

    df = pd.DataFrame(timesPerSeq)
    df.to_csv(path_2, index=False,header=False)

    return