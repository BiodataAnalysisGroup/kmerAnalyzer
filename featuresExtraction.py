# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:15:44 2019

@author: User
"""

import TreeClass
import saveToFile
import os
import dataPreProcessing
import time

# Some useful global variables
mychars = ['A', 'C', 'G', 'T']
training_perc = 0.5
kmin = 4
kmax = 80

# Adding all children in a node
def add_all_nodes(current, depth):
    
    chars = ['A', 'C', 'G', 'T']
    for char in chars:
        current.add_child(TreeClass.Node(char, current, depth+1))
    
    return current
    
# Initialization of the tree - depth = 4
def initialize_tree():
    
    tree = TreeClass.Tree()
    root = tree.root
    
    root = add_all_nodes(root , 0)
    for child1 in root.children:
        child1 = add_all_nodes(child1, 1)
        for child2 in child1.children:
            child2 = add_all_nodes(child2, 2)
            for child3 in child2.children:
                child3 = add_all_nodes(child3, 3)
    
    return root, tree

# routine_1 is only for the first scan of file
# This means that routine1 is used only for k = 4
def routine_1(fn, k, tree, numOfLines):
   
    # Open file
    with open(fn, 'r') as fh:
        
        # Initialization
        kmers_examined = 0
        count = 0
        
        for myline in fh:
            
            count += 1
            print(str(count) + ", " + str(k) )
            
            for j in range(len(myline) - k):
                
                kmers_examined += 1
                this_kmer = myline[j:j+k]
                    
                if count < int(numOfLines * training_perc):
                    tree.find_in_tree(this_kmer, False , kmers_examined, k, False, sequenceIndex=count-1)
                else:
                    tree.find_in_tree(this_kmer, True, kmers_examined, k, False,  sequenceIndex=count-1)
            
    return tree
 
    

def routine_2(fn, k, tree, numOfLines):
    
    kmers_examined = 0
    
    with open(fn, 'r') as fh:
        
        count = 0
        
        for myline in fh:  
            count += 1
            print(str(count) + ", " + str(k) )
            
            for j in range(len(myline) - k):
                
                kmers_examined += 1
                this_kmer = myline[j:j+k]
                  
                if count < int(numOfLines * training_perc):
                    tree.find_in_tree(this_kmer, False , kmers_examined, k, True, sequenceIndex=count-1)
                else:
                    tree.find_in_tree(this_kmer, True, kmers_examined, k, True, sequenceIndex=count-1)
        
        TreeClass.check_tree(root, kmers_examined, k)
         
    return tree


# Present the tree using a list
def listTree(tree, curr_node, sequence, treelist, zipList, k):
    
    if  not curr_node.children:
        
        # Forming results
        this_seq = sequence + curr_node.char
        treelist.append([this_seq, curr_node.depth, curr_node.count ,curr_node.evaluation, curr_node.sequenceIndices, curr_node.timesPerSeq])
        
        # Calculating entropy
        if curr_node.depth == k:
            
            zipList.append([this_seq, curr_node.count])
        
        return treelist, zipList
    
    else:
        this_seq = sequence + curr_node.char
        
        for child in curr_node.children:
            
            newnode = tree.move_to_child(curr_node, curr_node.children.index(child))
            treelist, zipList = listTree(tree, newnode, this_seq, treelist,zipList , k)
    
    return treelist, zipList


def listSortBasedOnEvaluation(sub_li): 
    
    return sorted(sub_li, key = lambda x: x[3], reverse = True)

if __name__ == "__main__":
    
    # Delete everything inside folders '~/Input', '~/Output' and '~/ClusteringData'
    saveToFile.clearingFolders('Input')
    saveToFile.clearingFolders('Output')
    saveToFile.clearingFolders('ClusteringData')

    # preprocessing my input data
    exec(open("dataPreProcessing.py").read())

    # Cd
    folder = 'Input'
    files = os.listdir(folder)

    # Staring time
    start = time.time()
    
    # Start
    for filename in files:
        if filename.endswith('.txt'):

            file = folder + '/' + filename
            numOfLines, lenOfLine = dataPreProcessing.file_len(file)
            filename = filename[0:-4]
            
            # Range of k values
            kvals = list(range(kmin,kmax+1))
            
            # Initialization
            root, tree = initialize_tree()
            
            # Main loop 
            for k in kvals:
                
                # Clearing console
                os.system('cls' if os.name == 'nt' else 'clear')

                # Only the first time run the first routine
                if k == 4:
                    tree = routine_1(file, k, tree, numOfLines)
                    #treelist, zipList = listTree(tree, root, '', [], [], k)
                                    
                # Else run the second routine
                else:
                    tree = routine_2(file, k , tree, numOfLines)
                    
                    # Forming treelist
                    # treelist, zipList = listTree(tree, root, '', [], [], k)
                    
                    # Check if it is time to exit
                    # if len(zipList) <= 1:
                    #    break
            
            treelist, zipList = listTree(tree, root, '', [], [], kvals[-1])

            # Printing Tree and forming necessary lists
            treelist = listSortBasedOnEvaluation(treelist)
            seqIndices = [treelist[i][4] for i in range(len(treelist))]
            timesPerSeq = [treelist[i][5] for i in range(len(treelist))]

            for i in range(len(treelist)):
                
                del treelist[i][5]
                del treelist[i][4]

                if seqIndices[i][0] == "":
                    del seqIndices[i][0]
                    del timesPerSeq[i][0]
            
            # Saving the output
            saveToFile.createCsvOutput(filename, treelist)
            saveToFile.createCsvOutputForSeqIndices(filename,seqIndices, timesPerSeq)

            # Printing time
            end = time.time()
            print("Completed in  " + str(time.strftime('%H:%M:%S', time.gmtime(end-start))))
            print("Completed in  " + str(end - start) + " seconds")
            command = "python dataPostProcessing.py "+ filename
            os.system(command)