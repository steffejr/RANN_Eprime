'''
Created on May 21, 2012

@author: jason
'''

import os
import glob
import RANN_EPrime
import datetime
import numpy
DataFolder='/share/data/studies/RANN/DesignFiles'
DataFolder=os.path.normpath(DataFolder)
d=glob.glob(os.path.join(DataFolder,'CleanData','*'))

i='/share/data/studies/RANN/DesignFiles/CleanData/4205'
Q=RANN_EPrime.ReadEPrime(i)
Q.ReadAllFiles()
On=Q.AllData['DgtSym']['OnsetTime']
D=numpy.diff(On,1)
A=numpy.where(D>4000)[0]+1
On[A]





import scipy.io as sio

TaskName = 'WordOrder'
InstructOn=numpy.array([30])
InstructDur=numpy.array([20])
StudyList1On=numpy.array([50, 58.2, 64.2, 72.9, 82.2, 85.6, 102.2, 111.5, 117.2, 130.5, 142.5, 150])
StudyList1Dur = numpy.array([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])
StudyList2On=numpy.array([295.0,  303.1,  311.4,  321.2,  330.9,  337.5,  348.2,  364.6, 371.9,  380.4,  386.1,  394.0])
StudyList2Dur=numpy.array([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])
QuestionsList1On=numpy.array([165])
QuestionsList1Dur=numpy.array([120]) 
QuestionsList2On = numpy.array([409])
QuestionsList2Dur = numpy.array([120])
#        TotalDur=608
names=numpy.zeros((5,),dtype=numpy.object)
names[0]=['Intructions']
names[1]=['StudyList1']
names[2]=['StudyList2']
names[3]=['QuestionList1']
names[4]=['QuestionList2']
durations=[]
durations.append(InstructDur)
durations.append(StudyList1Dur)
durations.append(StudyList2Dur)
durations.append(QuestionsList1Dur)
durations.append(QuestionsList2Dur)
onsets=[]
onsets.append(InstructOn)
onsets.append(StudyList1On)
onsets.append(StudyList2On)
onsets.append(QuestionsList1On)
onsets.append(QuestionsList2On)

FileName = Q.subid+'_'+TaskName+'.mat'
OutFile=os.path.join(Q.DesignFolder,FileName)
sio.savemat(OutFile,{'names':names,'durations':durations,'onsets':onsets})
print "wrote Word Order Task"