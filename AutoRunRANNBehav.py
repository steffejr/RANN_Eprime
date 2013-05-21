'''
Created on Jul 24, 2012

@author: jason
'''


import os
import fnmatch
import datetime
import shutil
import filecmp
os.sys.path.append('/share/data/users/js2746_Jason/Scripts/eclipse/RANN_Eprime')
import Run_RANN_Behav
BasePath = '/share/studies/RANN/DesignFiles'
FileName = 'RANN_BehavioralData_'
today = datetime.datetime.now()
timeStamp = today.strftime('%H%M_%m%d%Y')
Str='Started calculations at: '+timeStamp
os.system('echo '+Str+ ' >> '+os.path.join(BasePath,'logFile.log'))

# create the new results
Run_RANN_Behav.Run_RANN_Behav()
# find the most recent file
all_sub = [d for d in os.listdir(BasePath) if fnmatch.fnmatch(d, FileName+'*.csv')]
if len(all_sub)>0:
    for i in range(0,len(all_sub),1):
        all_sub[i] = os.path.join(BasePath,all_sub[i])
    latestFile=max(all_sub, key=os.path.getmtime)
    tempFileName = os.path.join(BasePath,'tempRANN_BehavioralData.csv')
    if filecmp.cmp(latestFile,tempFileName):
        print "Same File"
        os.remove(tempFileName)
    else:
        print "Different Files"
        today = datetime.datetime.now()
        timeStamp = today.strftime('%H%M_%m%d%Y')
        OutFile=os.path.join(BasePath,FileName+timeStamp+'.csv')
        shutil.move(tempFileName,OutFile)
else:
    today = datetime.datetime.now()
    timeStamp = today.strftime('%H%M_%m%d%Y')
    OutFile=os.path.join(BasePath,FileName+timeStamp+'.csv')
    shutil.move(tempFileName,OutFile)
    
today = datetime.datetime.now()
timeStamp = today.strftime('%H%M_%m%d%Y')
Str='Finished calculations at: '+timeStamp
os.system('echo '+Str+ ' >> '+os.path.join(BasePath,'logFile.log'))      
os.system('echo ' + ' >> '+os.path.join(BasePath,'logFile.log'))
 