# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 11:42:13 2012

@author: Makaye
"""
import os
import glob
import RANN_EPrime
import datetime
#DataFolder='C:/Users/Makaye/Desktop/SteffenerColumbia/Projects/RANN/Data'
#DataFolder='C:/Users/Makaye/Desktop/SteffenerColumbia/Projects/RANN/Data'
#DataFolder='Z:\Cognitive Reserve\RANN\DesignFiles\CleanData'
DataFolder='/share/data/studies/RANN/DesignFiles'
#DataFolder='C:\Users\Makaye\Desktop\SteffenerColumbia\Projects\RANN'
#DataFolder='/share/data/studies/RANN/Scripts/js2746_Jason/TimSalthouseData'
#DataFolder='/share/data/users/js2746_Jason/JasonCode/RANNStudy/Data'
#DataFolder='/home/sfbirn/jason'
DataFolder=os.path.normpath(DataFolder)
d=glob.glob(os.path.join(DataFolder,'CleanData','*'))
count = 0
now=datetime.datetime.now()
STRtimedate=str(now.hour).zfill(2)+str(now.minute).zfill(2)+"_"+str(now.month).zfill(2)+str(now.day).zfill(2)+str(now.year).zfill(4)
OutFileName='RANN_BehavioralData_'+STRtimedate+'.csv'
fid=open(os.path.join(DataFolder,OutFileName),'wb')
count = 0
CCC=0;
for i in d:
    print str(CCC) + ': ' +i
    CCC=CCC+1
    
i=d[12]     

#    print "Hello"
print i
Q=RANN_EPrime.ReadEPrime(i)
#    Q.FindNONPracticeFiles()
#    Q.TaskNames()
Q.ReadAllFiles()
Q.CalculateAllSummaryMeasures()
if count==0:
    Q.PrintOutHeader(fid)
# If a folder is empty then print this out
if len(Q.AllData)==0:
    # not data files found for this person
    str = 'No Data,'
    fid.write(str)
    fid.write(i)
    fid.write('\n')
else:
    Q.PrintOutOneRow(fid)
    if "PaperFold" in Q.AllData:
        if Q.AllData['PaperFold']['ACC'].shape:
            Q.SaveSPMDesignMatFiles('PaperFold')
    if "MatReas" in Q.AllData:
        if Q.AllData['MatReas']['ACC'].shape:
            Q.SaveSPMDesignMatFiles('MatReas')
    if "LetSet" in Q.AllData:
        if Q.AllData['LetSet']['ACC'].shape:
            Q.SaveSPMDesignMatFiles('LetSet')
    if "DgtSym" in Q.AllData:
        Q.CreateDgtSymDesign()
        
    if "PattComp" in Q.AllData:
        Q.CreateSimpleDesigns('PattComp',36,40,28,5)
    if "LetComp" in Q.AllData:
        Q.CreateSimpleDesigns('LetComp',36,40,28,5)
    if "Syn" in Q.AllData:
        Q.CreateSimpleDesigns('Syn',36,42,28,5)
    if "Ant" in Q.AllData:
        Q.CreateSimpleDesigns('Ant',36,42,28,5)
    # create picture naming 
    Q.CreateSimpleDesigns('PictName',36,40,28,5)
    
count=count+1
    
fid.close()
print "Done!!"
print "Data written to:"
print "    "+os.path.join(DataFolder,OutFileName)
    
    