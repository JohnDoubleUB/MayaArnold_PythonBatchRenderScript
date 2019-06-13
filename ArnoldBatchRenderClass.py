import maya.cmds as ma
from mtoa.cmds.arnoldRender import arnoldRender

#This code allows a user to specify multiple cameras inside maya along with frame ranges, so that they can be rendered in sequence.

#renderCams, resolutionW, resolutionH, fileName, fileType, batchDivide, batchDivideID, bUniqueFrameStart, uniqueStartFrame, bUniqueFrameEnd, uniqueEndFrame
#Class that handles all ui data before handing off to aBRS_beginRender
class aBRS_data:
	
	#InstanceIDs
	_instanceID = 0 #Serves as means to define different IDs for instances, also holds a count of the amount of instances created.
	_instanceName = "null"
	
	##Setting up suitableDefaults
	
	# Strings
	_fileType = "jpeg"
	_fileName = "defaultName"
	
	# Integers
	_resolutionW = 0
	_resolutionH = 0
	
	_batchDivide = 1 # Rendering on multiple systems (number of systems)
	_batchDivideID = 1 # Number of given system
	
	_uniqueStartFrame = 0
	_uniqueEndFrame = 0
	
	# Lists
	_renderCamsData = [] # holds rendercam data [cameraName, startFrame, Endframe]
	_interFrameList = [] # Intermediary frame list, usually contains all frame numbers in their entirety
	_frameList = [] # holds final frame list, this is what will be rendered
	
	_supportedFileTypes = [ "jpeg" ,"png" ,"exr" ]
	
	# Bools
	_bUniqueStartFrame = False
	_bUniqueEndFrame = False

	##Data for renderlogs
	
	#Data stored during or after startRender() Function for use in logs
	_lS_frameDataSTR = []
	_lS_frameData = []
	
	_lS_renderStartTime = 0.0
	_lS_renderEndTime = 0.0
	_lS_renderTimeInMinutes = 0.0
	_lS_renderCompletionSuccessful = False #True if last render successfully completed all frames, False if never run or not completed.
	
	_lS_batchDivideID = 1
	_lS_batchDivide = 1
	_lS_fileName = "null"
	_lS_fileType = "null"
	

	def __init__(self):
		#Get default values for self from render settings
		self.matchDefaultRenderSettings(True,True)
		self._establishInstanceID()
	
	
	## -- InstanceID Related functionality
	
	#Used only at instance initialisation, establishes unique ID
	def _establishInstanceID(self):
		aBRS_data._instanceID += 1
		self._instanceID = aBRS_data._instanceID
		self.refreshInstanceName()
	
	#Refreshes instance name
	def refreshInstanceName(self):
		self._instanceName = str(self._fileName) + "_inst" + str(self._instanceID)
	
	#Only to be used when all items are deleted from the outside data list
	def resetInstanceCount(self):
		aBRS_data._instanceID = 0
	
	## -- Default , Reset and Refreshing functions
	
	#matches render settings in class to those available in the maya rendersettings, can effect class defaults or instances
	def matchDefaultRenderSettings(self, setSelf, setClass):
		try:
			if setSelf:
				self._resolutionW = ma.getAttr("defaultResolution.width")
				self._resolutionH = ma.getAttr("defaultResolution.height")
				self._fileType = self.getSafeFileType(ma.getAttr("defaultArnoldDriver.ai_translator"))
				self._renderCamsData = self.getSequencerData()
			if setClass:
				aBRS_data._resolutionW = ma.getAttr("defaultResolution.width")
				aBRS_data._resolutionH = ma.getAttr("defaultResolution.height")
				aBRS_data._fileType = self.getSafeFileType(ma.getAttr("defaultArnoldDriver.ai_translator"))
				aBRS_data._renderCamsData = self.getSequencerData()
		
			self._finalizeFrameData() #Refresh Frame List
		except ValueError:
			raise ValueError("default Arnold Driver not detected! Please open render settings to establish defaults.")
	
	#Resets variables and removes specific instance variables so they conform with default class settings		
	def resetAllToClassDefaults(self):
		self.matchDefaultRenderSettings(True, True)
		
		#String list for variables to remove from instance members (if they exist in a given instance)
		variablesResetList = ["_fileName","_batchDivide", "_batchDivideID", "_uniqueStartFrame", "_uniqueEndFrame", "_bUniqueStartFrame", "_bUniqueEndFrame"] # DO NOT ALTER THIS UNLESS YOU KNOW WHAT IT DOES.
		
		# Remove self variables so that default class variables are inherrited once more
		# Doing it this way reduces code size as if a variable doesn't have a unique instance self an error will be generated.
		for varToRemove in variablesResetList:
			try:exec("del self." + varToRemove)
			except:pass
		
		self._finalizeFrameData() #Refresh Frame List
		self.refreshInstanceName() #Refresh Instance Name
	
	## -- Gettrs for external information
	
	#Get data from mayas camera sequencer
	def getSequencerData(self):
		#List to be populated and then returned
		sequencerData = []
		#Store shot names as a list
		sequencerVar = ma.sequenceManager(lsh = True)
		#In case of there being no data to pull, return empty list
		try:
			#For each shot on the list, retrieve its information
			for sVT in sequencerVar:
				#tempList for storing data
				sVTListTemp = []
				#append cameraName, frameStart and frameEnd
				sVTListTemp.append(str(ma.shot(sVT, q = True, cc = True)))
				sVTListTemp.append(int(ma.shot(sVT, q = True, st = True)))
				sVTListTemp.append(int(ma.shot(sVT, q = True, et = True)))
				#append information to shotPulledList
				sequencerData.append(sVTListTemp)
				#once all shot info has been stored within shotPulledList return
			return sequencerData
		except TypeError:
			return sequencerData
			
	#Opens File Dialog allowing user to choose a file to load, or a file and file name to save. returns False if cancelled.
	def getFilePath(self, dialogButton, bSaveOrLoad):
		try:
			if bSaveOrLoad:
				#File to be saved
				exportPath = ma.fileDialog2(fm=0, okc=dialogButton, cap='Select Export Folder', ff="Batch Render Script File ( *.brsf)")[0]
			else:
				#File to be loaded
				exportPath = ma.fileDialog2(fm=1, okc=dialogButton, cap='Import A File', ff="Batch Render Script File ( *.brsf)")[0]
			return exportPath
		except TypeError:
			print "User Cancelled File Dialog."
			return False
			
	## -- Frame Data Sorting
	
	#Split up a given seq into pieces of a given size, returns the new sequence
	def _splitSeq(self, seq, numpieces):
		#store sequence length
		seqlen = len(seq)
		d, m = divmod(seqlen, numpieces)
		rlist = range(0, ((d + 1) * (m + 1)), (d + 1))
		if d != 0: rlist += range(rlist[-1] + d, seqlen, d) + [seqlen]
		newseq = []
		for i in range(len(rlist) - 1):
			newseq.append(seq[rlist[i]:rlist[i + 1]])
		newseq += [[]] * max(0, (numpieces - seqlen))
		return newseq

	#Determines the percentage of frames from framelist rendered from a given rendered frame count
	def _renderPercentComplete(self, framesRendered):
		return int(round(float(framesRendered)/float(len(self._frameList))*100))
	
	## -- Gettrs
	
	#Sorts and returns a list starting or ending in a specified value, (startEnd = True) = startValue, (startEnd = False) = endValue 
	#(findValue) integer value, (dataList) = list of frames
	def _getStartEndFrame(self, dataList, startEnd, findValue):
		listToReturn = []
		bFrameFound = False
		if startEnd:
			dataListSorted = dataList
			for f in dataListSorted:
				if f >= findValue or bFrameFound:
					listToReturn.append(f)
			return listToReturn
		else:
			dataListSorted = list(reversed(dataList))
			for f in dataListSorted:
				if f <= findValue or bFrameFound:
					listToReturn.append(f)
			return list(reversed(listToReturn))   
	
	#Actually trims and returns a given frame list based on specified start and end frames
	def _trimStartEnd(self, frameList):
		# Check if unique frameStart and frameEnd are enabled, trim accordingly
		if self._bUniqueStartFrame and self._bUniqueEndFrame:
			return self._getStartEndFrame(self._getStartEndFrame(frameList, True, self._uniqueStartFrame), False, self._uniqueEndFrame)
		elif self._bUniqueStartFrame:
			return self._getStartEndFrame(frameList, True, self._uniqueStartFrame)
		elif self._bUniqueEndFrame:
			return self._getStartEndFrame(frameList, False, self._uniqueEndFrame)
		else:
			return frameList
	
	
	#From the class data set (cameraName, startFrame, endFrame) returns the camera associated with a given frame.    
	def _getCam(self, frameNo):
		for dataSet in self._renderCamsData:
			if frameNo >= dataSet[1] and frameNo <= dataSet[2]:
				return dataSet[0]
	
	#To ensure that type given is supported
	def getSafeFileType(self, type):
		for safeTypes in self._supportedFileTypes:
			if type == safeTypes:
				return type
		return self._supportedFileTypes[0]
	
	def getResolutionW(self):
		return self._resolutionW
		
	def getResolutionH(self):
		return self._resolutionH
		
	def getRCData(self):
		return self._renderCamsData
	
	def get_bUniqueStartFrame(self):
		return self._bUniqueStartFrame
	
	def get_bUniqueEndFrame(self):
		return self._bUniqueEndFrame
	
	def getUniqueStartFrame(self):
		return self._uniqueStartFrame
		
	def getUniqueEndFrame(self):
		return self._uniqueEndFrame
		
	def getFileType(self):
		return self._fileType
		
	def getFileTypeIndex(self):
		return self._supportedFileTypes.index(self._fileType)
		
	def getFileName(self):
		return self._fileName
		
	def getBatchDivide(self):
		return self._batchDivide
		
	def getBatchDivideID(self):
		return self._batchDivideID
		
	def getFrameList(self):
		return self._frameList
		
	def getInstanceName(self):
		return self._instanceName
		
	def getSupportedFileTypes(self):
		return self._supportedFileTypes
		
	def getRenderCamsData(self):
	    return self._renderCamsData
	    
	def getRenderCamsDataAsStrList(self):
		stringCamsData = []
		for camData in self._renderCamsData:
			stringCamsData.append(str(camData))
		return stringCamsData
	
	#returns a list of posible batch divide ids according to the batch divide count	
	def getBatchDivideIDs(self):
		tempIDList = []
		for ID in range(self._batchDivide):
			tempIDList.append(ID+1)
		return tempIDList
		
	## -- Settrs
	
	def setResolutionW(self, resolutionW):
		if type(resolutionW) is int:
			self._resolutionW = resolutionW
		
	def setResolutionH(self, resolutionH):
		if type(resolutionH) is int:
			self._resolutionH = resolutionH
		
	def setRCData(self, rCData):
		self._renderCamsData = rCData
		self._finalizeFrameData() #Refresh Frame List
	
	def set_bUniqueStartFrame(self, uSF):
		if type(uSF) is bool:
			self._bUniqueStartFrame = uSF
			self._finalizeFrameData() #Refresh Frame List
	
	def set_bUniqueEndFrame(self, uEF):
		if type(uEF) is bool:
			self._bUniqueEndFrame = uEF
			self._finalizeFrameData() #Refresh Frame List
	
	def setUniqueStartFrame(self, uSF):
		if type(uSF) is int:
			self._uniqueStartFrame = uSF
			self._finalizeFrameData() #Refresh Frame List
		
	def setUniqueEndFrame(self, uEF):
		if type(uEF) == int:
			self._uniqueEndFrame = uEF
			self._finalizeFrameData() #Refresh Frame List
		
	def setFileType(self, fType):
		if type(fType) is int:
			self._fileType = self._supportedFileTypes[fType]
		elif fType in self._supportedFileTypes:
			self._fileType = fType
		
	def setFileName(self, fileName):
		if type(fileName) is str:
			self._fileName = fileName
			self.refreshInstanceName() # Refresh Instance Name
		
	def setBatchDivide(self, bD):
		if type(bD) is int:
			self._batchDivide = bD
			self._finalizeFrameData() #Refresh Frame List
		
	def setBatchDivideID(self, bDID):
		if type(bDID) is int:
			self._batchDivideID = bDID
			self._finalizeFrameData() #Refresh Frame List
	
	## -- Settrs for unique functionality
	def exportInstanceData(self):
		nameAndPath = self.getFilePath("Save File", True)
		if nameAndPath:
			savedInstanceData = {"fT":self._fileType ,"fN":self._fileName ,"rW":self._resolutionW ,"rH":self._resolutionH ,"bD":self._batchDivide ,"bDI":self._batchDivideID ,"uSF":self._uniqueStartFrame ,"uEF":self._uniqueEndFrame ,"rCD":self._renderCamsData ,"bSF":self._bUniqueStartFrame ,"bEF":self._bUniqueEndFrame ,"lFDS":self._lS_frameDataSTR ,"lFD":self._lS_frameData ,"lRS":self._lS_renderStartTime ,"lRE":self._lS_renderEndTime ,"lRM":self._lS_renderTimeInMinutes ,"lRCS":self._lS_renderCompletionSuccessful ,"lBDI":self._lS_batchDivideID ,"lBD":self._lS_batchDivide ,"lFN":self._lS_fileName ,"lFT":self._lS_fileType}
			dataFile = open(nameAndPath, 'w')
			dataFile.write("savedInstanceData=%s" % str(savedInstanceData))
	

	def importInstanceData(self):
		nameAndPath = self.getFilePath("Load File", False)
		if nameAndPath:
			dataFile = open(nameAndPath, 'r')
			dataList = dataFile.readlines()
			for data in dataList:
				if "savedInstanceData=" in data:
					exec(data)
			try:
				self._fileType = savedInstanceData["fT"]
				self._fileName = savedInstanceData["fN"]
				self._resolutionW = savedInstanceData["rW"]
				self._resolutionH = savedInstanceData["rH"]
				self._batchDivide = savedInstanceData["bD"]
				self._batchDivideID = savedInstanceData["bDI"]
				self._uniqueStartFrame = savedInstanceData["uSF"]
				self._uniqueEndFrame = savedInstanceData["uEF"]
				self._renderCamsData = savedInstanceData["rCD"]
				self._bUniqueStartFrame = savedInstanceData["bSF"]
				self._bUniqueEndFrame = savedInstanceData["bEF"]
				self._lS_frameDataSTR = savedInstanceData["lFDS"]
				self._lS_frameData = savedInstanceData["lFD"]
				self._lS_renderStartTime = savedInstanceData["lRS"]
				self._lS_renderEndTime = savedInstanceData["lRE"]
				self._lS_renderTimeInMinutes = savedInstanceData["lRM"]
				self._lS_renderCompletionSuccessful = savedInstanceData["lRCS"]
				self._lS_batchDivideID = savedInstanceData["lBDI"]
				self._lS_batchDivide = savedInstanceData["lBD"]
				self._lS_fileName = savedInstanceData["lFN"]
				self._lS_fileType = savedInstanceData["lFT"]
				self._finalizeFrameData()
			except NameError:pass
	
	#Exports render cams data to a specified location
	def exportRenderCamsData(self):
		renderCamsData = str(self._renderCamsData)
		nameAndPath = self.getFilePath("Save File", True)
		if nameAndPath:
			dataFile = open(nameAndPath, 'w')
			dataFile.write("savedCamsData=%s" % renderCamsData)
	
	#Imports render cams data from a given file		
	def importRenderCamsData(self):
		nameAndPath = self.getFilePath("Load File", False)
		if nameAndPath:
			dataFile = open(nameAndPath, 'r')
			dataList = dataFile.readlines()
			for data in dataList:
				if "savedCamsData=" in data:
					exec(data)
			try:
				tempDataList = savedCamsData
				self.setRCData(tempDataList)
			except NameError:pass
	
	#Removes all existing camera data from an instance
	def clearRCData(self):
		self._renderCamsData = []
		self._finalizeFrameData() #Refresh Frame List
	
	#Adds data to existing instance data set, if none exists list will contain only the given data, does not effect default values
	def appendCameraToDataSet(self, cameraData):
		tempList = []
		for dataSet in self._renderCamsData:
			tempList.append(dataSet)
		tempList.append(cameraData)
		self._renderCamsData = tempList
		
		self._finalizeFrameData() #Refresh Frame List
	
	#Removes data from the data set	according to its index value, does not effect default values.
	def removeCameraFromDataSet(self, cameraDataIndex):
		tempList = []
		for dataSet in self._renderCamsData:
			tempList.append(dataSet)
		del tempList[cameraDataIndex]
		self._renderCamsData = tempList
		
		self._finalizeFrameData() #Refresh Frame List
	
	#Directly manipulates renderCamsData swapping two cameras according to index values, given index values are valid, returns true if successful
	def switchCameraDataPositions(self, posIndex1, posIndex2):
		#Check validity of index values
		if posIndex1 >= 0 and posIndex1 <= len(self._renderCamsData)-1:
			if posIndex2 >= 0 and posIndex2 <= len(self._renderCamsData)-1:
				#Store Data from both index values
				item1 = self._renderCamsData[posIndex1]
				item2 = self._renderCamsData[posIndex2]
				#Place Data at one anothers index values
				self._renderCamsData[posIndex1] = item2
				self._renderCamsData[posIndex2] = item1
				
				self._finalizeFrameData() #Refresh Frame List
				return True
		return False
	
	#Edits values within renderCamsData
	def editRenderCamsData(self, dataSetIndex, dataIndex, newData):
		if dataIndex == 0:
			self._renderCamsData[dataSetIndex][dataIndex] = newData
		else:
			self._renderCamsData[dataSetIndex][dataIndex] = newData
			#In this case change to the frames has taken place therefore
			self._finalizeFrameData() #Refresh Frame List
	
	#Likely to only be called internally, this function does the final preparation ensureing that frame list contains only the frames that will be rendered. (will be called whenever changes are made to the frames to be rendered.)
	#Responsible for refreshing data inside _frameList
	def _finalizeFrameData(self):
		#Check if _renderCamsData currently contains items
		self._frameList = []
		if len(self._renderCamsData) > 0:
			#lists for temporary storage
			tempFrameList = [] # used to store the entire frame list
			tempSplitFrameList = [] # used when storing the newly established frame batches (when rendering across multiple systems)
			#Combine all frame ranges into a list
			for camData in self._renderCamsData:
				tempFrameList.extend(range(camData[1], camData[2]+1))	
			#Check whether the frames are to be divided (for rendering across multiple systems)
			if self._batchDivide <= 1:
				# Check if unique frameStart and frameEnd are enabled, trim accordingly	
				self._frameList = self._trimStartEnd(tempFrameList)	
			else:	
				#split by batchDivide value (batchDivide only)
				tempSplitFrameList = self._splitSeq(tempFrameList, self._batchDivide)
				# Check if unique frameStart and frameEnd are enabled, trim accordingly
				self._frameList = self._trimStartEnd(tempSplitFrameList[self._batchDivideID-1])
	
	
	## -- Render Functions
	
	#stores all render related data that doesn't require a render to have been completed (excluding things like time taken etc.). to be called at render intialisation.
	def storeRenderData(self):
		self._lS_batchDivideID = self._batchDivideID
		self._lS_batchDivide = self._batchDivide
		self._lS_fileName = self._fileName
		self._lS_fileType = self._fileType
	
	#Generates a log file holding information about the render
	def generateRenderLog(self):
		#Store the location of tmp folder according to the location of the workspace and the "defined" project image folder within it.
		renderLogLoc = ma.workspace(q = True, rd = True) + ma.workspace(fre = "images") + "/tmp"
		#Generate file name on the end of the renderLogLoc variable as name path
		logNameAndPath = renderLogLoc + "/" + str(self._lS_fileName) + "_batNo_" + str(self._lS_batchDivide) + "_batID_" + str(self._lS_batchDivideID) + ".txt"
		#Create the log file and store in variable to allow writing
		renderLog = open(logNameAndPath, 'w')
		#Begin writing data into file
		renderLog.write("Render started: %s" % self._lS_renderStartTime)
		renderLog.write(os.linesep)
		renderLog.write("Render ended: %s" % self._lS_renderEndTime)
		renderLog.write(os.linesep + os.linesep)
		renderLog.write("batchDivideCount: " + str(self._lS_batchDivide))
		renderLog.write(os.linesep)
		renderLog.write("batchDivideID (This Systems ID): " + str(self._lS_batchDivideID))
		renderLog.write(os.linesep)
		renderLog.write("RenderCompletedSuccessfully?: " + str(self._lS_renderCompletionSuccessful))
		renderLog.write(os.linesep + os.linesep)
		#store information on each frame rendered with time stamps for completion time
		renderLog.write("frameData(with time initiated);-")
		renderLog.write(os.linesep)
		
		#list rendered frames with time stamps
		for frameData in self._lS_frameDataSTR:
			renderLog.write(str(frameData))
			renderLog.write(os.linesep)
		renderLog.write(os.linesep)
		renderLog.write("Total time taken in minutes: " + str(self._lS_renderTimeInMinutes))

	#script that renders a given frame, with given name, type, camera and resolution values, Also handles any runtime errors while mid render cancelling.
	def tryArnoldRender(self, frame):
		try:
			ma.setAttr("defaultArnoldDriver.ai_translator", self._fileType, type="string")
			ma.setAttr("defaultArnoldDriver.pre", self._fileName, type="string")
			arnoldRender(self._resolutionW, self._resolutionH, True, True, self._getCam(frame), ' -layer defaultRenderLayer')
			return True
		except RuntimeError:
			return False
	
	def startRender(self): # Will also return time taken from start to finish in minutes, to 2 decimal places
	
		frameDataLog = [] #Stores a comprehensive list of each frame as it is rendered with a timestamp for initialisation
		frameDataStringLog = []#Stores a comprehensive string list of each frame as it is rendered with a timestamp for initialisation, for using in the render log
		frameDataLogTemp = [] #Stores frame information temporarily
	
		#ints
		framesRendered = 0 #Stores current amount of frames rendered for determining overall progress
		percentComplete = 0 #Stores the percentage to completion, also used to determine if render completed successfully
		#Strings
		frameDataString = "null" #Stores frame information
		renderStartTimeStamp = ma.date(t=True) #Stores the time in which the render function was first called
		#floats
		renderTimeStamp = 0.0 #Stores the time in which the render completed or was forcably stopped
		#startTimer
		renderTimer = ma.timer(startTimer = True)
	
	
		###WINDOW CREATION
		#createWindow to allow interupting of progress.
		ma.progressWindow(isInterruptable=1, t="aBRS_RENDER", status = "Rendering...")

		#begin rendering frames
		for frame in self._frameList:
			##Allow interuption to stop the render
			if ma.progressWindow(query=True, isCancelled = True):
				print "Render Cancelled by User."
				break
		
			#set current frame
			ma.currentTime(frame)
		
			#store frame data and timestamp for initialisation then print.
			frameDataLogTemp = [self._getCam(frame), frame, ma.date(t=True)] # A nice list storing frame information (incase of storage)
			frameDataString = "Camera: %s, Frame: %s, TimeStarted: %s" % (str(frameDataLogTemp[0]), str(frameDataLogTemp[1]), str(frameDataLogTemp[2]))
		
			#Store data in lists
			frameDataLog.append(frameDataLogTemp)
			frameDataStringLog.append(frameDataString)
		
			#print current string data to viewport
			print frameDataString
			
			"""RENDER OCCURS HERE"""
			
			#try as maya 2018 arnold render returns a runtime error when interuption is detected
			self.tryArnoldRender(frame)
			#Add to frames rendered
			framesRendered += 1
			#Get percentage according to rendered vs total frames
			percentComplete = self._renderPercentComplete(framesRendered)
			#Update the progress window
			ma.progressWindow( edit=True, progress=percentComplete )
		
		'''Rendering has finished - Closing procedures'''	  
	
		#End timer
		renderTimer = ma.timer(endTimer = True)
		#End Progress window
		ma.progressWindow(endProgress=1)
		#Store total render time
		renderTimeStamp = str(round(renderTimer/60, 2))
	
		#record values for log file
		self._lS_frameDataSTR = frameDataStringLog
		self._lS_frameData = frameDataLog
		self._lS_renderStartTime = renderStartTimeStamp
		self._lS_renderEndTime = ma.date(t=True)
		self._lS_renderTimeInMinutes = renderTimeStamp
		self._lS_renderCompletionSuccessful = percentComplete == 100
		self.storeRenderData()
	
	
		#Generate log
		self.generateRenderLog()
	
		return "Render Time in Minutes: " + str(renderTimeStamp)