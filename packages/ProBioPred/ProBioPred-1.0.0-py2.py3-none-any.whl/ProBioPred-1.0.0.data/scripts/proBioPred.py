#!python

#from optparse import OptionParser
import argparse
import probiopred.probiopred as mydef
import os
import sys
import subprocess

parser = argparse.ArgumentParser(description="Wrapper for running ProBioPred. Searches for "
                                             "probiotic, virulent and antibiotic resistence "
                                             "genes in query genome. Then predicts the probability "
                                             "score of genome being probiotic or non-probiotic "
                                             "based on SVM model.")
parser.add_argument('-i','--input_genome',metavar='PATH',required=True,
                    type=str,help='Query genome sequence in FASTA format')
parser.add_argument('-g','--genus',metavar='GENUS',required=True,type=str,
                    help='Genus of query genome. Currently support only following 9 genera.'
                         '[bacillus, clostridium, lactobacillus, leuconostoc, streptococcus, '
                         'bifidobacterium, enterococcus, lactococcus, pediococcus]',
                         choices =['bacillus', 'clostridium', 'lactobacillus', 'leuconostoc', 'streptococcus',
                         'bifidobacterium', 'enterococcus', 'lactococcus', 'pediococcus'])
parser.add_argument('-o','--output_dir',metavar='PATH',required=False,
                    default='ProBioPred_out',type=str,help='Path of output directory [Default: ProBioPred_out].')
parser.add_argument('-t','--threads',default=1,type=int,
                    help='Number of threads to run for BLAST and RGI.')

args = parser.parse_args()

genus = args.genus
genomeFile = os.getcwd() + '/' + str(args.input_genome)
userFolder = args.output_dir
threads = str(args.threads)

#sample input given by nitin
try:
    os.mkdir(userFolder,0o777)
    os.chdir(userFolder)
except:
    exit(userFolder + " already exists.")

#read input
proFile,vfdbFile,model = mydef.readInput(genus)

#makeblastdb
makedbflag = mydef.makeBlastDB(genomeFile)
scoreDict = dict()

#Run RGI
rgiResponse,rgiScore = mydef.runRGI(genomeFile,threads)

if(rgiResponse == True):
    scoreDict["ardb"] = rgiScore
elif(not rgiResponse ==True):
    exit("Failed to run RGI : " + str(rgiResponse))
#blast for virulent genes
if(os.path.isfile(vfdbFile)):
    #do vfdb blast
    if(makedbflag == True):
        blastFlag = mydef.blast(vfdbFile)
        #if blast is successful do filtering
        if(blastFlag == True):
            filterFlag = mydef.filterBlastOutput("out.blast","vfdb_outFiltered.blast")
            nvfdb = mydef.count_no_of_lines("vfdb_outFiltered.blast")
            scoreDict["vfdb"] = nvfdb
            #extract sequence
            mydef.extractSeq(mydef.listOfGeneHits("vfdb_outFiltered.blast"),vfdbFile,"vfdb_hits.pfasta")
        else:
            filterFlag = False
            print("Could not filter blast output file : \n" + str(blastFlag))
    else:
        blastFlag = False
        print("Could not proceed with blast : \n" + str(makedbflag))

#probiotic blast, filtering and creation of scores dictionary
if(makedbflag == True):
    blastFlag = mydef.blast(proFile)
    #filter results
    if(blastFlag == True):
        filterFlag = mydef.filterBlastOutput("out.blast","pro_outFiltered.blast")
        if(filterFlag ==True):
            #If no probiotic genes found 
            if(mydef.count_no_of_lines("pro_outFiltered.blast") < 1 ):
                print("Cannot proceed. No probiotic genes found")
                exit(1)
            #add prodict to scoreDict
            scoreDict = mydef.merge_dicts(scoreDict,mydef.proResults("pro_outFiltered.blast"))
            #extract sequences
            mydef.extractSeq(mydef.listOfGeneHits("pro_outFiltered.blast"),proFile,"pro_hits.pfasta")
        elif(filterFlag ==False):
            print("Could not filter blast output : " + str(blastFlag))
    elif(not blastFlag ==True):
        print("Could not do blast : " + str(blastFlag))

########### preparing output ############
scoreDict["class"] = "pro"    #dummy class label
mydef.writeResultsToFile(scoreDict,"resulTab.csv") #writing csv file of all scores
#convert csv to libsvm
flagCsv2Libsvm = mydef.csvToLibSVM("resulTab.csv")
if(flagCsv2Libsvm):
    pass
else:
    print("Failed to make LibSVM data.")
    exit(1)

################# preparation for running predictions ##############
flagPredict = mydef.runPrediction("resulTab.libsvm",model)

if(flagPredict):
    libSvmOut = open("out.libsvm","r")
    predictLines = libSvmOut.readlines()
    scores = predictLines[1].split(" ")
    scorePositive, scoreNegative = scores[1],scores[2]
    if(scorePositive > scoreNegative):
        print("Probiotic : " + scorePositive)
    else:
        print("Non Probiotic : " + scoreNegative)

mydef.removeTempFiles(genomeFile)
