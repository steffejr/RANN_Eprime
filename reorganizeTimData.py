# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 18:18:16 2012

@author: Makaye
"""

import glob
import os
import shutil

DataFolder='C:\Users\Makaye\Desktop\SteffenerColumbia\Projects\RANN'
DataFolder='/share/data/studies/RANN/Scripts/js2746_Jason/TimSalthouseData'
#DataFolder='/share/data/users/js2746_Jason/JasonCode/RANNStudy/Data'
#DataFolder='/home/sfbirn/jason'
DataFolder=os.path.normpath(DataFolder)
d=glob.glob(os.path.join(DataFolder))

InFileList=glob.glob(os.path.join(d[0],'Data','*.txt'))
for i in InFileList:
    print i
    FileName=os.path.basename(i)
    subid=FileName.split('-')[1]
    OutFolder=os.path.join(d[0],subid)
    if not os.path.exists(os.path.join(OutFolder,'log files')):
        os.mkdir(OutFolder)        
        os.mkdir(os.path.join(OutFolder,'log files'))
    shutil.move(i,os.path.join(OutFolder,'log files',FileName))

