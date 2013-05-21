'''
Created on Mar 19, 2012
I am thinking of creating a dictionary of each task. The entry will 
be the task name and the data will be a list containing:
path to file
median RT
number correct
all RT
create list as:
data=['filenamepath', array_of_RT,medianRT,meanRT]
dictionary={'TaskName',data}
then any new entries get added by:
dictionary['newTask']=data
dictionary.keys gives a list of task names
CHECKED
Digit symbol - good EXCEPT for it is adding 5 extra blank trials at the beginning
Letter compare - good
Logical memory - good
Paper Fold - good
LetterSets - good but need to double check what the last trial is and if that is a TRU trial
# or some sort of mistake
Synonyms - good
Antonyms -- good
Pair Assoc -- good
Pattern Comp -- good
Matrix Reasoning -- good
TIMINGS:

SPEED
DgtSym
LetComp
PattComp

VERBAL
Ant
Syn
WordOrder

MEMORY
LetSet
>>PictName<<
LogMem

REASONING
PaperFold
MatReas
PairAssoc


@author: jason
'''
import os
import EPrimeParser
import numpy
import glob
import datetime
import scipy.io as sio
import sys
        
class ReadEPrime():
    #DataFolder='/share/data/users/js2746_Jason/JasonCode/RANNStudy/RANNCode/4505'
    #DataFolder=InFolder
    #DataFolder='C:/Users/Makaye/Desktop/SteffenerColumbia/Projects/RANN/Data/4505'

    
    def __init__(self,InFolder):
        print "Hello World"
        self.FMRIDataBaseFolder='/export/data2/studies/RANN/Subjects'
        self.InFolder=InFolder
        self.DataFolder=os.path.join(InFolder,'log files')
        self.RTLimit=200
        self.AllData = {}
        self.FindNONPracticeFiles()
        self.TaskNames()
        #self.ReadAllFiles()
        #self.CalculateAllSummaryMeasures()
        #self.WriteOut()
        
    def TaskNames(self):
        self.Names = {};
        self.Names['Logical Memory']='LogMem'
        self.Names['Word Order Recognition']='WordOrder'
        self.Names['Paper Folding']='PaperFold'
        self.Names['LetterSets']='LetSet'
        self.Names['DigitSymbol']='DgtSym'
        self.Names['Syn']='Syn'
        self.Names['Antonyms']='Ant'
        self.Names['Paired Associates']='PairAssoc'
        self.Names['PatternComparison']='PattComp'
        self.Names['Matrix Reasoning']='MatReas'
        self.Names['LetterComparision']='LetComp'      
        
    def FindNONPracticeFiles(self):
        #os.chdir(self.DataFolder)
        InFileList=glob.glob(os.path.join(self.DataFolder,'*.txt'))
        #os.chdir('../..')
        self.FileList=[]
        for i in InFileList:
            if i.find('ractice')==-1:
                Fullfile=os.path.join(self.DataFolder,i)
               # print Fullfile
                self.FileList.append(Fullfile)
        
        
    def ReadAllFiles(self):
        for i in self.FileList:
            self.readDataFile(i)

    def MapTaskNameToShorterVersion(self,TaskName):
        # Take the task name as written in the EPrime file and map it onto short 
        # task names
        #print TaskName
        for i in self.Names:
            #NamesEntry=DD.next()
            if TaskName.find(i)>-1:
                return self.Names[i]
                break
        
    def readDataFile(self,File):
        #print '======================'
        #print File
        #self.File=os.path.join(self.DataFolder,self.File)
        try:
            print "Working on File: "+File
            self.RawData = EPrimeParser.EPrimeParser(File)
            DictData=self.RawData.experimentalLists
            TaskName=self.RawData.header['Experiment']
            print TaskName
            TaskName=self.MapTaskNameToShorterVersion(TaskName)
            self.subid=self.RawData.header['Subject']
            print self.subid
            if TaskName:
                self.AllData[TaskName]=[]
                TopLevelNames=DictData.keys()
                TopLevelNames.sort()
                print TopLevelNames
                # Initialize the RT and ACC arrays
                # This approach takes on a zero value at the beginnig of the array which 
                # looks like an extra trial. The purpose of this approach though is to 
                # allow multiple blocks to be found and their arrays of RTs be appended
                # to one another.
                self.AllData[TaskName]={}
                if hasattr(self.RawData,'GetReady'):
                    self.AllData[TaskName]['GetReadyTime']=self.RawData.GetReady
                else:
                    self.AllData[TaskName]['GetReadyTime']=0
                self.AllData[TaskName]['RT']=numpy.array(0)
                self.AllData[TaskName]['ACC']=numpy.array(0)
                self.AllData[TaskName]['OnsetTime']=numpy.array(0)
                self.AllData[TaskName]['OnsetDelay']=numpy.array(0)
                self.AllData[TaskName]['RTTime']=numpy.array(0)
                for j in TopLevelNames:
# This is an unfortunate exception but for the Digit Symbol task there is something
# called a block which the program thinks is 5 empty trials. I am sure
# that there is a more ellegant solution but for now this may work                 
                    if (len(DictData[j][0]['loggingObjects'].keys())>0) & (j.find('Blocks')<0):
                        TrialLevelNames=DictData[j][0]['loggingObjects'].keys()
                        NTrials=len(DictData[j])
                        #  print NTrials
                        # cycle over trials
                        RTdata = numpy.zeros(NTrials)
                        ACCdata = numpy.zeros(NTrials)
                        OnsetTimedata = numpy.zeros(NTrials)
                        OnsetDelaydata = numpy.zeros(NTrials)
                        RTTimedata = numpy.zeros(NTrials)
                        for i in range(0,NTrials):
                            #RTdata=0
                            # for each trial there may be two conditions
                            # this was necessary for the LetterSet task and 2 others 
                            # where a trial has two parts.
                          #  print "====================="RTdata.append(tempRT)
                                            
                            for k in TrialLevelNames:
                                if "RT" in DictData[j][i]['loggingObjects'][k]:
# If there is n RT for stim11 then this is the RT to use, otherwise use the 85 one
# But this is going to run through the trials TWICE                                    
                                    # Check to see what the response is. It looks like the last trial 
                                    # on some experiments may be incomplete

                                    tempRT=long(DictData[j][i]['loggingObjects'][k]['RT'])     
                                    tempACC=long(DictData[j][i]['loggingObjects'][k]['ACC'])
                                    try: 
                                        #DictData[j][i]['loggingObjects'][k]['OnsetTime']
                                        tempOnsetTime=long(DictData[j][i]['loggingObjects'][k]['OnsetTime'])
                                    except:
                                        tempOnsetTime=-99
                                    try:
                                        tempOnsetDelay=long(DictData[j][i]['loggingObjects'][k]['OnsetDelay'])
                                    except:
                                        tempOnsetDelay=-99
                                    try:
                                        tempRTTime=long(DictData[j][i]['loggingObjects'][k]['RTTime'])
                                    except:
                                        tempRTTime=-99

                                    if (k == 'stimulus11') & (tempRT!=0):
                                        # This a response during the first 11 seconds
                                        RTdata[i]=tempRT
                                        ACCdata[i]=tempACC
                                        OnsetTimedata[i]=tempOnsetTime
                                        OnsetDelaydata[i]=tempOnsetDelay
                                        RTTimedata[i]=tempRTTime

                                    elif k=='stimulus85':
                                        # This is a value in the 85 part of the trial and NO 
                                        # value in the 11 part
                                        if long(DictData[j][i]['loggingObjects']['stimulus11']['RT'])==0:
                                            # This trial had no RT during the 11 sec part
                                            # but did they during the 85 second part?
                                            if tempRT>0:
                                                RTdata[i]=tempRT+11000
                                                ACCdata[i]=tempACC
						OnsetTimedata[i]=tempOnsetTime
						OnsetDelaydata[i]=tempOnsetDelay
						RTTimedata[i]=tempRTTime
                                            else:
                                                RTdata[i]=tempRT
                                                ACCdata[i]=tempACC
						OnsetTimedata[i]=tempOnsetTime
						OnsetDelaydata[i]=tempOnsetDelay
						RTTimedata[i]=tempRTTime
                                    else:
                                        RTdata[i]=tempRT
                                        ACCdata[i]=tempACC
					OnsetTimedata[i]=tempOnsetTime
					OnsetDelaydata[i]=tempOnsetDelay
					RTTimedata[i]=tempRTTime
                                        
 
                        self.AllData[TaskName]['RT']=numpy.append(self.AllData[TaskName]['RT'],numpy.asarray(RTdata))
                        self.AllData[TaskName]['ACC']=numpy.append(self.AllData[TaskName]['ACC'],numpy.asarray(ACCdata))
			self.AllData[TaskName]['OnsetTime']=numpy.append(self.AllData[TaskName]['OnsetTime'],numpy.asarray(OnsetTimedata))
			self.AllData[TaskName]['OnsetDelay']=numpy.append(self.AllData[TaskName]['OnsetDelay'],numpy.asarray(OnsetDelaydata))
			self.AllData[TaskName]['RTTime']=numpy.append(self.AllData[TaskName]['RTTime'],numpy.asarray(RTTimedata))
            self.AllData[TaskName]['RT']=self.AllData[TaskName]['RT'][1:]
            self.AllData[TaskName]['ACC']=self.AllData[TaskName]['ACC'][1:]
            self.AllData[TaskName]['OnsetTime']=self.AllData[TaskName]['OnsetTime'][1:]
            self.AllData[TaskName]['OnsetDelay']=numpy.append(self.AllData[TaskName]['OnsetDelay'],numpy.asarray(OnsetDelaydata))
            self.AllData[TaskName]['RTTime']=numpy.append(self.AllData[TaskName]['RTTime'],numpy.asarray(RTTimedata))
#		self.AdjustTime(TaskName,'RTTime')
            self.AdjustTime(TaskName,'OnsetTime')
            if TaskName == 'LetSet':
                print TaskName
                self.RemoveEndTrials(TaskName)
            if TaskName == 'PaperFold':
                print TaskName
                self.RemoveEndTrials(TaskName)
            if TaskName == 'MatReas':
                print TaskName
                self.RemoveEndTrials(TaskName)
        except: 
            print "Unexpected error:", sys.exc_info()[0]
            print "unknown File type"
            
    def RemoveEndTrials(self,TaskName):
        F = (860000 - self.AllData[TaskName]['OnsetTime'])>30000
        self.AllData[TaskName]['RT'] = self.AllData[TaskName]['RT'][F]
        self.AllData[TaskName]['OnsetTime'] = self.AllData[TaskName]['OnsetTime'][F]
        self.AllData[TaskName]['ACC'] = self.AllData[TaskName]['ACC'][F]
        self.AllData[TaskName]['OnsetDelay'] = self.AllData[TaskName]['OnsetDelay'][F]
        self.AllData[TaskName]['RTTime']  = self.AllData[TaskName]['RTTime'][F]
                
    def AdjustTime(self,TaskName,Measure):
        self.AllData[TaskName][Measure] = self.AllData[TaskName][Measure]-long(self.AllData[TaskName]['GetReadyTime'])

    def CalculateAllSummaryMeasures(self):
        for i in self.AllData.keys():
            self.CalculateSummaryMeasures(i)   
                   
    def CalculateSummaryMeasures(self,TaskName):
        i = TaskName

        print "Calculating Measures:"+i
        RT=self.AllData[i]['RT']
        ACC=self.AllData[i]['ACC']
        
        # Check to see if RT is empty 
        if numpy.any(RT):
            self.AllData[i]['NumTrials']=ACC.shape[0]
            self.AllData[i]['meanAllRT']=RT.mean()
            self.AllData[i]['medianAllRT']=numpy.median(RT)
        # Find time outs
            NumTimeOuts=len(numpy.where(RT<self.RTLimit)[0])
        
            OnTimeList=numpy.where(RT>=self.RTLimit)[0]
            NumOnTime=len(OnTimeList)
        #OnTimeList=numpy.nonzero(RT)[0]
            OnTimeRT=RT[OnTimeList]
        # Find incorrects
            IncList=numpy.where(ACC==0)[0]
            CorList=numpy.where(ACC==1)[0]            
            OnTimeCorList=numpy.where((RT*ACC)>=self.RTLimit)[0]
            OnTimeIncList=numpy.where((RT*numpy.abs(ACC-1))>self.RTLimit)[0]            
        
            NumOnTimeInc=len(OnTimeIncList)            
            NumCor=len(OnTimeCorList)       
            IncRT=RT[OnTimeIncList]
            CorRT=RT[OnTimeCorList]

            self.AllData[i]['NumCor']=NumCor
            self.AllData[i]['NumOnTimeInc']=NumOnTimeInc
            self.AllData[i]['NumTO']=NumTimeOuts
        else:
            self.AllData[i]['NumTrials']=0
            self.AllData[i]['NumCor']=0
            self.AllData[i]['NumOnTimeInc']=0
            self.AllData[i]['NumTO']=0

        if self.AllData[i]['NumTrials']>0:
            self.AllData[i]['PropOnTimeCor']=float(NumCor)/NumOnTime
            self.AllData[i]['PropOnTimeInc']=float(NumOnTimeInc)/NumOnTime
            self.AllData[i]['meanAllOnTimeRT']=OnTimeRT.mean()
            self.AllData[i]['medianAllOnTimeRT']=numpy.median(OnTimeRT)
        else:
            self.AllData[i]['PropOnTimeCor']=0
            self.AllData[i]['PropOnTimeInc']=0
            self.AllData[i]['meanAllOnTimeRT']=0
            self.AllData[i]['medianAllOnTimeRT']=0
            self.AllData[i]['meanCorRT']=0
            self.AllData[i]['medianCorRT']=0
            self.AllData[i]['meanInOnTimecRT']=0
            self.AllData[i]['medianIncOnTimeRT']=0
            
        if self.AllData[i]['NumCor']>0:
            self.AllData[i]['medianCorRT']=numpy.median(CorRT)
            self.AllData[i]['meanCorRT']=CorRT.mean()
        else:
            self.AllData[i]['medianCorRT']=0
            self.AllData[i]['meanCorRT']=0
        
        if self.AllData[i]['NumOnTimeInc']>0:
            self.AllData[i]['meanIncOnTimeRT']=IncRT.mean()
            self.AllData[i]['medianIncOnTimeRT']=numpy.median(IncRT)
        else:
            self.AllData[i]['meanIncOnTimeRT']=0
            self.AllData[i]['medianIncOnTimeRT']=0

        self.ParameterList=[];
        self.ParameterList.append('NumTrials')        
        self.ParameterList.append('NumCor')        
        self.ParameterList.append('NumOnTimeInc')        
        self.ParameterList.append('NumTO')  
        self.ParameterList.append('meanAllRT')
        self.ParameterList.append('medianAllRT')
        self.ParameterList.append('meanAllOnTimeRT')
        self.ParameterList.append('meanCorRT')
        self.ParameterList.append('meanIncOnTimeRT')
        self.ParameterList.append('medianAllOnTimeRT')
        self.ParameterList.append('medianCorRT')
        self.ParameterList.append('medianIncOnTimeRT')
        self.ParameterList.append('PropOnTimeCor')
        self.ParameterList.append('PropOnTimeInc')

    def WriteOut(self):
        fid=self.OpenOutputFile()
        self.PrintOutHeader(fid)
        self.PrintOutOneRow(fid)
        fid.close()
        
    def OpenOutputFile(self):
        fid=open(self.OutFile,'wb')
        return fid
        
    def PrintOutHeader(self,fid):
        # This prints out the Names in the Task Dictionary
        # NOT the names of the task files found. Therefore, the header has ALL
        # tasks that SHOULD have been given.
        fid.write('InFolder,')
        fid.write('subid')
        for i in self.Names.values():            
            for j in self.ParameterList:
                fid.write(',' + i + '_' + j)
        fid.write('\n')            
            
    def PrintOutOneRow(self,fid):
        fid.write(self.InFolder+',')
        fid.write(self.subid+',')
        for i in self.Names.values():
            for j in self.ParameterList:
                # This tries to print out data for ALL tasks that SHOULD have been given
                # If it cannot find a task then -99 values are written out
                try:
                    fid.write("%0.4f"%self.AllData[i][j]+',')            
                except:
                    fid.write("-99,")
        fid.write('\n')    
    
    def DisplayFileList(self):
        count = 0
	for i in range(0,len(self.FileList)):
#        for i in self.FileList:
            print str(count) +'\t'+self.FileList[i]
            count = count + 1
    
    def DisplayNumberOfTrials(self):
        for i in self.AllData.iterkeys():
            print i + str(len(self.AllData[i]['RT']))

    def SaveSPMDesignMatFiles(self,TaskName):
        if self.FindSubjectFolder():
            now=datetime.datetime.now()
            DateStr = str(now.month).zfill(2)+'_'+str(now.day).zfill(2)+'_'+str(now.year)+'_'+str(now.hour).zfill(2)+str(now.minute).zfill(2)
            FileName = self.subid+'_'+TaskName+'.mat'
            OutFile=os.path.join(self.DesignFolder,FileName)
            
            CorList=numpy.where(self.AllData[TaskName]['ACC']==1)[0]
            IncList=numpy.where(self.AllData[TaskName]['ACC']==0)[0]            
            
            
            onsets=[]
            durations=[]
            
            
            onsets.append(self.AllData[TaskName]['OnsetTime'][CorList]/1000)
            durations.append(self.AllData[TaskName]['RT'][CorList]/1000)

            IncRTList=self.AllData[TaskName]['RT'][IncList]/1000
            if IncRTList.size > 0:
                names=numpy.zeros((2,),dtype=numpy.object)
                names[0]=[TaskName+'Cor']
                names[1]=[TaskName+'Inc']
                for i in range(0,IncRTList.size,1):
                    if IncRTList[i] == 0:
                        IncRTList[i]=85
                        
                durations.append(IncRTList)
                onsets.append(self.AllData[TaskName]['OnsetTime'][IncList]/1000)
            else:
                names=numpy.zeros((1,),dtype=numpy.object)
                names[0]=[TaskName+'Cor']
                
            sio.savemat(OutFile,{'names':names,'durations':durations,'onsets':onsets})
    
    def FindSubjectFolder(self):
        dataFolder1=os.path.join(self.FMRIDataBaseFolder,'P'+str(self.subid).zfill(8),'S0001')
        dataFolder2=os.path.join(self.FMRIDataBaseFolder,'P'+str(self.subid).zfill(8),'S0002')
        if os.path.exists(dataFolder1):
            dataFolder=dataFolder1
        elif os.path.exists(dataFolder2):
            dataFolder=dataFolder2
        else:
            dataFolder=dataFolder1
            
        if os.path.exists(dataFolder):
            flag = True
            #found the fmri folder
            if not os.path.exists(os.path.join(dataFolder,'DesignFiles')):
                os.mkdir(os.path.join(dataFolder,'DesignFiles'))
            self.DesignFolder=os.path.join(dataFolder,'DesignFiles')
        else:
            flag = False
        return flag
                
    def CreateSimpleDesigns(self,TaskName,Intro,On,Off,Cycle):
        if self.FindSubjectFolder():
            onsets=numpy.zeros(Cycle)
            durations=numpy.zeros(Cycle)
            for i in range(0,Cycle,1):
                onsets[i]=Intro+i*(On+Off)
                durations[i]=On
            names=TaskName
            FileName = self.subid+'_'+TaskName+'.mat'
            OutFile=os.path.join(self.DesignFolder,FileName)
            sio.savemat(OutFile,{'names':names,'durations':durations,'onsets':onsets})
    
    def CreateDgtSymDesign(self):
        if self.FindSubjectFolder():
            # find the on times
            On=self.AllData['DgtSym']['OnsetTime']
            # find the difference between the on times
            D=numpy.diff(On,1)
            # find the big differences which are the time between blocks
            A=numpy.where(D>4000)[0]+1
            # create an array of block on times
            BlockStart=On[A]
            BlockStart=numpy.insert(BlockStart,0,On[0])
            BlockStart=BlockStart/1000
            Cycle=BlockStart.size
            onsets=numpy.zeros(Cycle)
            durations=numpy.zeros(Cycle)
            for i in range(0,Cycle,1):
                onsets[i]=BlockStart[i]
                durations[i]=49
            names='DgtSym'
            TaskName=names
            FileName = self.subid+'_'+TaskName+'.mat'
            OutFile=os.path.join(self.DesignFolder,FileName)
            sio.savemat(OutFile,{'names':names,'durations':durations,'onsets':onsets})

    def CreateLogMemDesign(self):
        if self.FindSubjectFolder():
            # find the on times
            On=self.AllData['LogMem']['OnsetTime']
            # find the difference between the on times
            D=numpy.diff(On,1)
            # find the big differences which are the time between blocks
            A=numpy.where(D>13000)[0]+1
            # create an array of block on times
            BlockStart=On[A]
            BlockStart=numpy.insert(BlockStart,0,On[0])
            BlockStart=BlockStart/1000
            Cycle=BlockStart.size
            onsets=numpy.zeros(Cycle)
            durations=numpy.zeros(Cycle)
            for i in range(0,Cycle,1):
                onsets[i]=BlockStart[i]
                durations[i]=125
            names='LogMem'
            TaskName=names
            FileName = self.subid+'_'+TaskName+'.mat'
            OutFile=os.path.join(self.DesignFolder,FileName)
            sio.savemat(OutFile,{'names':names,'durations':durations,'onsets':onsets})

        
        
    def CreatePairAssocTask(self):
        if self.FindSubjectFolder():
            TaskName = 'PairAssoc'
        
            StudyList1On=numpy.array([30, 37.6, 41.1, 45.3, 47.8, 50])
            StudyList1Dur = numpy.array([2, 2, 2, 2, 2, 2])
            #StudyList2On = numpy.array([152, 158.1, 162, 165.6, 168.1, 172])
            StudyList2On = numpy.array([114, 120.1, 124, 127.6, 130.1, 134])
            StudyList2Dur = numpy.array([2, 2, 2, 2, 2, 2])
            QuestionsList1On = numpy.array([62])
            QuestionsList1Dur = numpy.array([42])
            QuestionsList2On = numpy.array([146])
            QuestionsList2Dur = numpy.array([42])
            
            names=numpy.zeros((4,),dtype=numpy.object)
            names[0]=['StudyList1']
            names[1]=['StudyList2']
            names[2]=['QuestionList1']
            names[3]=['QuestionList2']
            durations=[]
            durations.append(StudyList1Dur)
            durations.append(StudyList2Dur)
            durations.append(QuestionsList1Dur)
            durations.append(QuestionsList2Dur)
            onsets=[]
            onsets.append(StudyList1On)
            onsets.append(StudyList2On)
            onsets.append(QuestionsList1On)
            onsets.append(QuestionsList2On)
            FileName = self.subid+'_'+TaskName+'.mat'
            OutFile=os.path.join(self.DesignFolder,FileName)
            sio.savemat(OutFile,{'names':names,'durations':durations,'onsets':onsets})
            print "Paired Associates Task"
        
    def CreateWordOrderTask(self):
        if self.FindSubjectFolder():
            TaskName = 'WordOrder'
            # the number lists all need to be created as arrays so that the save function will work.
            StudyList1On=numpy.array([30, 31.2, 42.2, 49.9, 58.2, 63.6, 76.2, 84.5, 89.2, 101.5, 111.5, 118])
            StudyList1Dur = numpy.array([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])
            StudyList2On=numpy.array([222.0,  229.1, 236.4, 245.2, 253.9, 259.5, 269.2, 284.6, 290.9, 298.4, 303.4, 310]) 
            StudyList2Dur=numpy.array([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])
            QuestionsList1On=numpy.array([132])# off by 12 seconds
            QuestionsList1Dur=numpy.array([80]) 
            QuestionsList2On = numpy.array([324])# off by 17 seconds
            QuestionsList2Dur = numpy.array([80])
    #        TotalDur=608
            names=numpy.zeros((4,),dtype=numpy.object)
            names[0]=['StudyList1']
            names[1]=['StudyList2']
            names[2]=['QuestionList1']
            names[3]=['QuestionList2']
            durations=[]
            durations.append(StudyList1Dur)
            durations.append(StudyList2Dur)
            durations.append(QuestionsList1Dur)
            durations.append(QuestionsList2Dur)
            onsets=[]
            onsets.append(StudyList1On)
            onsets.append(StudyList2On)
            onsets.append(QuestionsList1On)
            onsets.append(QuestionsList2On)
            FileName = self.subid+'_'+TaskName+'.mat'
            OutFile=os.path.join(self.DesignFolder,FileName)
            sio.savemat(OutFile,{'names':names,'durations':durations,'onsets':onsets})
            print "wrote Word Order Task"
    
        
        