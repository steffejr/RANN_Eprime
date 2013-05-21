  print "Working on File: "+File
            self.RawData = EPrimeParser.EPrimeParser(File)
            DictData=self.RawData.experimentalLists
            TaskName=self.RawData.header['Experiment']
            TaskName=self.MapTaskNameToShorterVersion(TaskName)
            self.subid=self.RawData.header['Subject']
            if TaskName:
                self.AllData[TaskName]=[]
                TopLevelNames=DictData.keys()
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
                                            # but did they during the 85 secon part?
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
