# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 19:36:33 2017

@author: Akshay
"""
from __future__ import division
from pulp import LpProblem, LpVariable, LpMaximize, LpStatus, LpInteger, LpAffineExpression
import sys
import os
import codecs
from collections import defaultdict
from math import log
#from StringIO import StringIO
from depParse import readParses, DepParse

# this function takes the name of the directory to process
# and returns a set of statistics which are useful for computing tfidf values and depth of nodes
def countStats(textDir):
    termCounts = defaultdict(lambda: defaultdict(int))
    word_depths = defaultdict(lambda: defaultdict(int))
    for fil in textDir:
        ff = open(dire + fil, encoding="utf-8")
        
        count = 0
        #print(readParses(ff))
        for parse in readParses(ff):
            leaves = parse.leaves()
            #print(leaves)
            for (word, pos) in leaves:
                termCounts[dire + fil][word] += 1
                node = str(word + "-" + str(pos))   
                #print(fil + node)
                word_depths[dire + fil][node + "-" + str(count)] = parse.distToRoot(node)
                
            count += 1
        
        #print(fil) 
    return termCounts, word_depths

# this function takes the word, the name of the document it appears in, 
# and the termcounts object returned by countstats
# and returns the tf*idf value for that word in that document
def tfidf(word, doc, termCounts):
    tf = termCounts[doc][word]
    #print tf
    dcount = sum([1 for fi in termCounts if word in termCounts[fi]])
    idf = len(termCounts) / (1 + dcount)
    lidf = log(idf)
    #return tf * lidf
    return lidf

dire = "E:\\SP 17\\5525 SLP\\Project\\Sentence Compression\\Text\\"
textDir = os.listdir("E:\\SP 17\\5525 SLP\\Project\\Sentence Compression\\Text\\")
termCounts, word_depths = countStats(textDir)
print("Done")
#print(word_depths)

s_pred_out_file = open("E:\\SP 17\\5525 SLP\\Project\\Sentence Compression\\support\\Results\\Lex_Compressed_1.txt", "w+")
num = []
for fil in textDir:
    num.append(int(fil))
    
num.sort()

print("Compressing")

for fil in num:
    fil = str(fil)
    fi = dire + fil#"E:\\SP 17\\5525 SLP\\Project\\Sentence Compression\\data\\A1G.11.orig"
    count = 0
    compressed_sentences = []
    
    #print(fi)
    for parse in readParses(open(fi, encoding="utf-8")):
        word_objects = {}
        all_leaves = parse.leaves()
        #print(all_leaves)
        for leaf in all_leaves:
            #print fi
            (word, pos) = leaf
            weight_tfidf = tfidf(word, fi, termCounts)
            node = str(word + "-" + str(pos) + "-" +str(count))
            depth_word = word_depths[fi][node]
            #print(weight_tfidf, depth_word, weight_tfidf - 0.4 * depth_word + 0.5)
            #Strong weight_tfidf - 0.1 * depth_word + 0.5
            #Stronger weight_tfidf - 0.1 * depth_word - 0.5
            #Strongest weight_tfidf - 0.4 * depth_word + 0.5
            word_objects[node] = weight_tfidf - 0.4 * depth_word + 0.5
        
        problem = LpProblem("Sentence Compression 1", LpMaximize)
        varTab = {}
        for obj in word_objects:
            varTab[obj] = LpVariable(obj, 0, 1, LpInteger)
         
        #the first line added to the problem is the objective
        objective = []
        for obj, wt in word_objects.items():
            objective.append( (varTab[obj], wt) )
        problem += LpAffineExpression(objective)
        
        constraint = []
        for obj, wt in word_objects.items():
            constraint.append( (varTab[obj], wt) )
        problem += ( LpAffineExpression(constraint) >= 0)
        
        #solve the problem...
        problem.solve()
        
        num_picked = 0
        wt = 0
        ours = ""
        sentence = []
        for varName, val in varTab.items():
            if val.varValue:
                objWt = word_objects[varName]
                wt += objWt
                num_picked += 1
                ours += " "+varName
                word_pos, co = varName.rsplit("-", 1)
                word, pos = word_pos.rsplit("-", 1)
                sentence.append([int(pos), word])
        sentence.sort()
        #print(sentence)
        c_sen = ""
        for index, node in enumerate(sentence):
            pos, word = node 
            c_sen += " " + word
        compressed_sentences.append(c_sen)
        #access information about the solution
        #print("Total No of words present", len(termCounts[fi]))
        #print("Total No of words picked", num_picked)
        
        #check that this worked
        #print ("Problem status:", LpStatus[problem.status])
        #print("\n\n\n")
        count+=1
        #print(c_sen)
        
    all_sentce = ""
    for index, sentce in enumerate(compressed_sentences):
        if sentce != '':
            all_sentce += sentce + "."
    
    #print(all_sentce)
    s_pred_out_file.write(all_sentce)
    s_pred_out_file.write("\n")
    
s_pred_out_file.close()
