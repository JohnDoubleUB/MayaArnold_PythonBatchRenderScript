import maya.cmds as ma

#Code for the UI within maya

#aBRS_UI_v2.py
#UI for aBRS_data class.

class brsUI:
	aBRS_instanceList = [] # To hold instances of aBRS_data class
	mainWindow = "mainWindowObject" #Main window instance Var
	dataDropDown = "dataDropDownObject" #data drop down instance var (for determining which instance of the data class is being handled)
	fileTypeDropDown = "fileTypeDropDownObject"
	fileName = "fileNameObject"
	resW = "resWObject"
	resH = "resHObject"
	uSF = "uniqueStartFrameObject"
	uEF = "uniqueEndFrameObject"
	bUSF = "boolUniqueStartFrameObject"
	bUEF = "boolUniqueEndFrameObject"
	framesToRender = "framesToRenderObject"
	batchDivide = "batchDivideObject"
	batchDivideID = "batchDivideIDObject"
	associatedCamera = "associatedCameraObject"
	renderCamsList = "renderCamsListObject"
	camNameField = "camNameObject"
	startFrameField = "startFrameObject"
	endFrameField = "endFrameObject"
	editCamTickBox = "editCamTickBoxObject"
	mainWindow_width = 450
	mainWindow_height = 600

## -- Refresh functions

def refreshAllInstanceData():
	#Refresh file type dropdown
	refreshFileTypeDropDown()
	#Refresh file name input box
	refreshFileNameInput()
	#Refresh width and height resolution
	refreshWidthAndHeight()
	#Refresh Start and End FrameData
	refreshStartEndFrameData()
	#Refresh Batch Divide Data
	refreshBatchDivideData()
	#Refresh Frames to Render List
	refreshFramesToRender()
	#Refresh Render Cams List
	refreshRenderCamsList()
	#Refresh Cam Edit Property boxes
	refreshCamEditProperties()

def refreshWidthAndHeight():
	if len(brsUI.aBRS_instanceList) > 0:
		ma.textField(brsUI.resW, e= True, tx=getSelectedInstance().getResolutionW(), en=True)
		ma.textField(brsUI.resH, e= True, tx=getSelectedInstance().getResolutionH(), en=True)
	else:
		ma.textField(brsUI.resW, e= True, tx="", en=False)
		ma.textField(brsUI.resH, e= True, tx="", en=False)

def refreshDataDropDownAndData():
	#Delete all existing list items
	ma.optionMenu(brsUI.dataDropDown, e = True, dai = True)
	
	#Refereshing Instance data items
	refreshAllInstanceData()
	
	#If instance list has objects
	if len(brsUI.aBRS_instanceList) > 0:
		for inst in brsUI.aBRS_instanceList:
			ma.menuItem( label=inst.getInstanceName(), p=brsUI.dataDropDown )
		ma.optionMenu(brsUI.dataDropDown, e = True, en=True)
	else:
		ma.optionMenu(brsUI.dataDropDown, e = True, en=False)

def refreshDataDropDown():
	#Delete all existing list items
	ma.optionMenu(brsUI.dataDropDown, e = True, dai = True)
	
	#If instance list has objects
	if len(brsUI.aBRS_instanceList) > 0:
		for inst in brsUI.aBRS_instanceList:
			ma.menuItem( label=inst.getInstanceName(), p=brsUI.dataDropDown )
		ma.optionMenu(brsUI.dataDropDown, e = True, en=True)
	else:
		ma.optionMenu(brsUI.dataDropDown, e = True, en=False)


def refreshFileTypeDropDown():
	#Clear existing menu values
	ma.optionMenu(brsUI.fileTypeDropDown, e = True, dai = True)
	#Check if instance list has objects
	if len(brsUI.aBRS_instanceList) > 0:
		for fileT in getSelectedInstance().getSupportedFileTypes():
			ma.menuItem( label=fileT, p=brsUI.fileTypeDropDown )
		#Get current instances selected filetype and set this to be selected in the drop down
		ma.optionMenu(brsUI.fileTypeDropDown, e = True, sl=getSelectedInstance().getFileTypeIndex()+1, en=True)
	else:
		ma.optionMenu(brsUI.fileTypeDropDown, e = True, en=False)
		
def refreshFileNameInput():
	if len(brsUI.aBRS_instanceList) > 0:
		ma.textField(brsUI.fileName, e=True, tx=getSelectedInstance().getFileName(), en=True)
	else:
		ma.textField(brsUI.fileName, e=True, tx="", en=False)

def refreshStartEndFrameData():
	refresh_bStartEndFrame()
	refreshStartEndFrame()

def refresh_bStartEndFrame():
	if len(brsUI.aBRS_instanceList) > 0:
		ma.checkBox(brsUI.bUSF, e=True, v=getSelectedInstance().get_bUniqueStartFrame(), en=True)
		ma.checkBox(brsUI.bUEF, e=True, v=getSelectedInstance().get_bUniqueEndFrame(), en=True)
	else:
		ma.checkBox(brsUI.bUSF, e=True, v=False, en=False)
		ma.checkBox(brsUI.bUEF, e=True, v=False, en=False)

def refreshStartEndFrame():
	if len(brsUI.aBRS_instanceList) > 0:
		ma.textField(brsUI.uSF, e=True, tx=str(getSelectedInstance().getUniqueStartFrame()))
		ma.textField(brsUI.uEF, e=True, tx=str(getSelectedInstance().getUniqueEndFrame()))
		
		if getSelectedInstance().get_bUniqueStartFrame():
			ma.textField(brsUI.uSF, e=True, en=True)
		else:
			ma.textField(brsUI.uSF, e=True, en=False)
		
		if getSelectedInstance().get_bUniqueEndFrame():
			ma.textField(brsUI.uEF, e=True, en=True)
		else:
			ma.textField(brsUI.uEF, e=True, en=False)
	else:
		ma.textField(brsUI.uSF, e=True, en=False, tx="")
		ma.textField(brsUI.uEF, e=True, en=False, tx="")

def refreshBatchDivideData():
	refreshBatchDivideCount()
	refreshBatchID()

def refreshBatchDivideCount():
	if len(brsUI.aBRS_instanceList) > 0:
		ma.textField(brsUI.batchDivide, e=True, tx=getSelectedInstance().getBatchDivide(), en=True)
	else:
		ma.textField(brsUI.batchDivide, e=True, tx="", en=False)
		
def refreshBatchID():
	ma.optionMenu(brsUI.batchDivideID, e=True, dai=True, en=False)
	if len(brsUI.aBRS_instanceList) > 0:
		for batchID in getSelectedInstance().getBatchDivideIDs():
			ma.menuItem( label=batchID, p=brsUI.batchDivideID )
		if getSelectedInstance().getBatchDivide() > 1:
			ma.optionMenu(brsUI.batchDivideID, e=True, en=True, v=getSelectedInstance().getBatchDivideID())

def refreshFramesToRender():
	ma.textScrollList(brsUI.framesToRender, e=True, ra=True, en=False )
	refreshSelectedFrameInfo()
	if len(brsUI.aBRS_instanceList) > 0:
		ma.textScrollList(brsUI.framesToRender, e=True, a=getSelectedInstance().getFrameList(), en=True)
		
def refreshSelectedFrameInfo():
	try:
		selectedFrame = int(ma.textScrollList(brsUI.framesToRender, q=True, si=True)[0])
		ma.text(brsUI.associatedCamera, e=True, label=getSelectedInstance()._getCam(selectedFrame))
	except TypeError:
		ma.text(brsUI.associatedCamera, e=True, label="")

def refreshRenderCamsList():
    ma.textScrollList(brsUI.renderCamsList, e=True, ra=True, en=False )
    if len(brsUI.aBRS_instanceList) > 0:
        ma.textScrollList(brsUI.renderCamsList, e=True, a=getSelectedInstance().getRenderCamsDataAsStrList(), en=True)

def refreshCamEditProperties():
	if len(brsUI.aBRS_instanceList) > 0:
		try:
			#Attempt to store selected item, if none are selected an exception error is raised
			selectedCamIndex = getSelectedCamSetIndex()
			selectedCamData = getSelectedInstance().getRenderCamsData()[selectedCamIndex]
			
			#Send collected data to text fields
			ma.textField(brsUI.camNameField, e=True, tx=str(selectedCamData[0]))
			ma.textField(brsUI.startFrameField, e=True, tx=str(selectedCamData[1]))
			ma.textField(brsUI.endFrameField, e=True, tx=str(selectedCamData[2]))
			
			#Check if editing is enabled, if so make the fields editable.
			if ma.checkBox(brsUI.editCamTickBox, q=True, v=True):
				ma.textField(brsUI.camNameField, e=True, en=True)
				ma.textField(brsUI.startFrameField, e=True, en=True)
				ma.textField(brsUI.endFrameField, e=True, en=True)
			else:
				ma.textField(brsUI.camNameField, e=True, en=False)
				ma.textField(brsUI.startFrameField, e=True, en=False)
				ma.textField(brsUI.endFrameField, e=True, en=False)
			
		except TypeError:
			ma.textField(brsUI.camNameField, e=True, tx="", en=False)
			ma.textField(brsUI.startFrameField, e=True, tx="", en=False)
			ma.textField(brsUI.endFrameField, e=True, tx="", en=False)
	else:
		ma.textField(brsUI.camNameField, e=True, tx="", en=False)
		ma.textField(brsUI.startFrameField, e=True, tx="", en=False)
		ma.textField(brsUI.endFrameField, e=True, tx="", en=False)

## -- Set Functions
	
def setFileName(fileName):
	currentIndexVal = getCurrentInstanceIndex() + 1
	getSelectedInstance().setFileName(str(fileName))
	#as this directly effects instance name, refresh instance list
	#first store current index val
	refreshDataDropDown()
	setDataDropDown(currentIndexVal)
	
def setFileTypeDropDown(fileType):
	getSelectedInstance().setFileType(fileType)

def setDataDropDown(indexVal):
	ma.optionMenu(brsUI.dataDropDown, e = True, sl=indexVal)
	
def setResolutionWidth(width):
	try:
		widthInteger = int(width)
		getSelectedInstance().setResolutionW(widthInteger)
	except ValueError:
		refreshWidthAndHeight()
	
def setResolutionHeight(height):
	try:
		heightInteger = int(height)
		getSelectedInstance().setResolutionH(heightInteger)
	except ValueError:
		refreshWidthAndHeight()

def enableStartFrame(bEnable):
	getSelectedInstance().set_bUniqueStartFrame(bEnable)
	refreshStartEndFrame()
	refreshFramesToRender()
	
def enableEndFrame(bEnable):
	getSelectedInstance().set_bUniqueEndFrame(bEnable)
	refreshStartEndFrame()
	refreshFramesToRender()

def setStartFrame(startFrame):
	try:
		startFrameInt = int(startFrame)
		getSelectedInstance().setUniqueStartFrame(startFrameInt)
		refreshFramesToRender()
	except ValueError:
		refreshStartEndFrame()
	
def setEndFrame(endFrame):
	try:
		endFrameInt = int(endFrame)
		getSelectedInstance().setUniqueEndFrame(endFrameInt)
		refreshFramesToRender()
	except ValueError:
		refreshStartEndFrame()
		
def setBatchDivideCount(batchDivide):
	try:
		batchDivideInt = int(batchDivide)
		setBatchDivideID(1)
		getSelectedInstance().setBatchDivide(batchDivideInt)
		refreshBatchID()
		refreshFramesToRender()
	except ValueError:
		refreshBatchDivideCount()

def setBatchDivideID(ID):
	idInt = int(ID)
	getSelectedInstance().setBatchDivideID(idInt)
	refreshFramesToRender()
	
def setCamName(camName):
	selectedData = getSelectedCamSetIndex()
	getSelectedInstance().editRenderCamsData(selectedData, 0, str(camName))
	refreshRenderCamsList()
	ma.textScrollList(brsUI.renderCamsList, e=True, sii=selectedData+1)
	
def setCamStartFrame(startFrame):
	try:
		startFrameInt = int(startFrame)
		selectedData = getSelectedCamSetIndex()
		getSelectedInstance().editRenderCamsData(selectedData, 1, startFrameInt)
		refreshFramesToRender()
		refreshRenderCamsList()
		ma.textScrollList(brsUI.renderCamsList, e=True, sii=selectedData+1)
	except ValueError:
		refreshCamEditProperties()
	
def setCamEndFrame(endFrame):
	try:
		endFrameInt = int(endFrame)
		selectedData = getSelectedCamSetIndex()
		getSelectedInstance().editRenderCamsData(selectedData, 2, endFrameInt)
		refreshFramesToRender()
		refreshRenderCamsList()
		ma.textScrollList(brsUI.renderCamsList, e=True, sii=selectedData+1)
	except ValueError:
		refreshCamEditProperties()

## -- Get Functions
			
def getCurrentInstanceIndex():
	return (ma.optionMenu(brsUI.dataDropDown, q= True, sl= True) -1)
	
def getSelectedInstance():
	return brsUI.aBRS_instanceList[getCurrentInstanceIndex()]
	
def getSelectedCamSetIndex():
	indexValue = ma.textScrollList(brsUI.renderCamsList, q=True, sii=True)
	return indexValue[0]-1
	#Will return a Type error if no object is selected

## -- Camera Data Management

#Imports instance from outside file
def importInstanceOverCurrent():
	if len(brsUI.aBRS_instanceList) > 0:
		getSelectedInstance().importInstanceData()
		refreshAllInstanceData()

#Exports current instance
def exportCurrentInstance():
	if len(brsUI.aBRS_instanceList) > 0:
		getSelectedInstance().exportInstanceData()

#Imports frame data from an outside file
def importFrameDataToInstance():
	if len(brsUI.aBRS_instanceList) > 0:
		getSelectedInstance().importRenderCamsData()
		#Refresh Frames to Render List
		refreshFramesToRender()
		#Refresh Render Cams List
		refreshRenderCamsList()
		#Refresh Cam Edit Property boxes
		refreshCamEditProperties()

#Exports Current Frame data		
def exportFrameDataInstanceToFile():
	if len(brsUI.aBRS_instanceList) > 0:
		getSelectedInstance().exportRenderCamsData()

def deleteSelectedCam():
	if len(brsUI.aBRS_instanceList) > 0:
		try:
			selectedIndexValue = getSelectedCamSetIndex()
			getSelectedInstance().removeCameraFromDataSet(selectedIndexValue)
			refreshRenderCamsList()
			refreshFramesToRender()
			
			#if item isn't index 0
			if selectedIndexValue > 0:
				ma.textScrollList(brsUI.renderCamsList, e=True, sii=selectedIndexValue) #Select the item above the deleted item
				
			#Else if it is index 0 but items are still on the list
			elif len(getSelectedInstance().getRenderCamsData()) > 0:
				ma.textScrollList(brsUI.renderCamsList, e=True, sii=1) #Select the top most item
			
			#Refresh Cam Edit Properties
			refreshCamEditProperties()
				
		except TypeError: pass
		
def addNewCam():
	if len(brsUI.aBRS_instanceList) > 0:
		getSelectedInstance().appendCameraToDataSet(["UntitledCamera", 0, 0])
		refreshRenderCamsList()
		refreshFramesToRender()
		#Determine the index of the newly appended item
		newItemIndex = len(ma.textScrollList(brsUI.renderCamsList, q=True, ai=True))
		#Select the new index item
		ma.textScrollList(brsUI.renderCamsList, e=True, sii=newItemIndex)
		#Refresh Cam Edit Properties
		refreshCamEditProperties()
		
def shiftSelectedCamUpwards():
	if len(brsUI.aBRS_instanceList) > 0:
		changed=False
		try:
			selectedIndexValue = getSelectedCamSetIndex()
			upValue = selectedIndexValue-1
			changed=getSelectedInstance().switchCameraDataPositions(selectedIndexValue, upValue)
			#Refresh Data
			refreshRenderCamsList()
			refreshFramesToRender()
			if changed:
				#Make the selected item the item previously selected
				ma.textScrollList(brsUI.renderCamsList, e=True, sii=upValue+1)
			else:
				ma.textScrollList(brsUI.renderCamsList, e=True, sii=selectedIndexValue+1)
			#Refresh Cam Edit Properties
			refreshCamEditProperties()
			
		except TypeError: pass

def shiftSelectedCamDownwards():
	if len(brsUI.aBRS_instanceList) > 0:
		changed=False
		try:
			selectedIndexValue = getSelectedCamSetIndex()
			downValue = selectedIndexValue+1
			changed=getSelectedInstance().switchCameraDataPositions(selectedIndexValue, downValue)
			#Refresh Data
			refreshRenderCamsList()
			refreshFramesToRender()
			if changed:
				#Make the selected item the item previously selected
				ma.textScrollList(brsUI.renderCamsList, e=True, sii=downValue+1)
			else:
				ma.textScrollList(brsUI.renderCamsList, e=True, sii=selectedIndexValue+1)
			#Refresh Cam Edit Properties
			refreshCamEditProperties()
			
		except TypeError: pass

## -- Instance Management

def createNewDataInstance():
	#Create new instance
	brsUI.aBRS_instanceList.append(aBRS_data())
	#Refresh dataDropDown
	refreshDataDropDownAndData()
	#Make this the new selected item
	ma.optionMenu(brsUI.dataDropDown, e = True, sl = len(brsUI.aBRS_instanceList))
	
def deleteCurrentDataInstance():
	#Check there are currently any instances
	if len(brsUI.aBRS_instanceList) > 0:
		#if deleting item will result in list being empty, reset the instance ID count
		if len(brsUI.aBRS_instanceList) - 1 < 1:
			brsUI.aBRS_instanceList[0].resetInstanceCount()
		#Get selected instance value -1 to convert to list index values
		itemToDelete = ma.optionMenu(brsUI.dataDropDown, q = True, sl = True) - 1
		#Remove this item from the index
		del brsUI.aBRS_instanceList[itemToDelete]
		#Refresh the dropdown
		refreshDataDropDownAndData()

def deleteAllInstances():
	#Check if any instances exist
	if len(brsUI.aBRS_instanceList) > 0:
		#Reset instance count
		brsUI.aBRS_instanceList[0].resetInstanceCount()
		#Empty instance list
		brsUI.aBRS_instanceList = []
		#Refresh dropdown
		refreshDataDropDownAndData()
		
def resetInstanceToDefault():
	if len(brsUI.aBRS_instanceList) > 0:
		indexVal = getCurrentInstanceIndex()
		getSelectedInstance().resetAllToClassDefaults()
		refreshAllInstanceData()
		refreshDataDropDown()
		setDataDropDown(indexVal+1)

## -- Instance Sub options

#Generates instance render log file
def generateInstanceLogFile():
	if len(brsUI.aBRS_instanceList) > 0:
		getSelectedInstance().generateRenderLog()


def initiateInstanceRender():
	if len(brsUI.aBRS_instanceList) > 0:
		getSelectedInstance().startRender()

#Check if window already exists, if so remove it
if ma.window ( brsUI.mainWindow, exists = True ):
        ma.deleteUI( brsUI.mainWindow )


#Create main window
brsUI.mainWindow = ma.window( brsUI.mainWindow, title = "MtoA Python Batch Render Script", sizeable=False, resizeToFitChildren=True, menuBar = True) 

#Define Menubar items
ma.menu( label='Instance Options', tearOff=True )
ma.menuItem( divider=True, label="Instance Management")
ma.menuItem( label='Create New Instance', c="createNewDataInstance()")
ma.menuItem( label='Delete Current Instance', c="deleteCurrentDataInstance()" )
ma.menuItem( divider=True, label="Instance Properties")
ma.menuItem( label='Reset Instance to Default', c="resetInstanceToDefault()")
ma.menuItem( divider=True )
ma.menuItem( label='Delete All Instances', c="deleteAllInstances()")
ma.menu( label='Import/Export Options', tearOff=True )
ma.menuItem( label='Import Instance FrameData', c="importFrameDataToInstance()" )
ma.menuItem( label='Export Current Instance FrameData', c="exportFrameDataInstanceToFile()" )
ma.menuItem( divider=True )
ma.menuItem( label='Import Instance Over Current', c="importInstanceOverCurrent()" )
ma.menuItem( label='Export Current Instance', c="exportCurrentInstance()" )
ma.menuItem( divider=True )
ma.menuItem( label='Generate Instance Log File', c="generateInstanceLogFile()" )

#Begin adding a base layout
ma.rowColumnLayout("SingleColumn", numberOfColumns = 1, columnWidth = (1,brsUI.mainWindow_width))

#Adding Data set managing row
ma.rowColumnLayout(brsUI.mainWindow, numberOfColumns = 2, columnWidth = [(1,(brsUI.mainWindow_width/3)*2),(2,brsUI.mainWindow_width/3)])
brsUI.dataDropDown = ma.optionMenu(brsUI.dataDropDown, label='  Instance Data Set:', changeCommand="refreshAllInstanceData()", en=False)
ma.setParent("..")
ma.separator()

#Create Tabs
brsUI.tabs = ma.tabLayout()

####Tab1
brsUI.child1 = ma.rowColumnLayout("SingleColumnTab1", numberOfColumns = 1, columnWidth = (1,brsUI.mainWindow_width -8))

#Resolution Settings Header
ma.rowColumnLayout(numberOfColumns = 2, columnWidth = ((1,brsUI.mainWindow_width/3),(2,brsUI.mainWindow_width/3*2 )))
ma.text(label = "Resolution Settings", bgc=(0.2,0.2,0.2), al="left" )
ma.separator()
ma.setParent( '..' )

ma.rowColumnLayout(numberOfColumns = 2, columnWidth = ((1,brsUI.mainWindow_width/2),(2,brsUI.mainWindow_width/2)))

#Width Resolution
ma.rowColumnLayout(numberOfColumns = 2)
ma.text(label = "Resolution Width: ")
brsUI.resW = ma.textField(brsUI.resW, w=120, en=False, changeCommand=setResolutionWidth)
ma.setParent( '..' )

#Height Resolution
ma.rowColumnLayout(numberOfColumns = 2)
ma.text(label = "Resolution Height: ")
brsUI.resH = ma.textField(brsUI.resH, w=116, en=False, changeCommand=setResolutionHeight)
ma.setParent( '..' )

ma.setParent( '..' )

#File Settings Header
ma.rowColumnLayout(numberOfColumns = 2, columnWidth = ((1,brsUI.mainWindow_width/3),(2,brsUI.mainWindow_width/3*2 -8)))
ma.text(label = "File Settings", bgc=(0.2,0.2,0.2), al="left" )
ma.separator()

#FileName
ma.text(label = "File Name: ", al = "right")
brsUI.fileName = ma.textField(brsUI.fileName, changeCommand=setFileName, en=False)
ma.setParent( '..' )

#FileType DropDown
ma.rowColumnLayout(numberOfColumns = 3, columnWidth = ((1,brsUI.mainWindow_width/3),(2,brsUI.mainWindow_width/3), (3,brsUI.mainWindow_width/3)))
ma.text(label = "File Type: ", al = "right")
brsUI.fileTypeDropDown = ma.optionMenu(brsUI.fileTypeDropDown, cc=setFileTypeDropDown, en=False)
ma.text(label = "")
ma.setParent( '..' )

#Frame Settings Header
ma.rowColumnLayout(numberOfColumns = 2, columnWidth = ((1,brsUI.mainWindow_width/3),(2,brsUI.mainWindow_width/3*2 -8)))
ma.text(label = "Frame Settings", bgc=(0.2,0.2,0.2), al="left" )
ma.separator()
ma.setParent( '..' )

#Unique Start Frame
ma.rowColumnLayout(numberOfColumns = 3, columnWidth = ((1,brsUI.mainWindow_width/3),(2,brsUI.mainWindow_width/3), (3,brsUI.mainWindow_width/3)))
ma.text(label = "Unique Start Frame: ", al = "right")
brsUI.uSF = ma.textField(brsUI.uSF, en=False, cc=setStartFrame)

#Unique Start Frame tick box
ma.rowLayout( numberOfColumns=2 , columnWidth2=(1, brsUI.mainWindow_width/3-1))
ma.text(label = "")
brsUI.bUSF = ma.checkBox(brsUI.bUSF, label='Enable', cc=enableStartFrame, en=False)
ma.setParent( '..' )

#Unique End Frame
ma.text(label = "Unique End Frame: ", al = "right")
brsUI.uEF = ma.textField(brsUI.uEF, en=False, cc=setEndFrame)

#Unique End Frame tick box
ma.rowLayout( numberOfColumns=2 , columnWidth2=(1, brsUI.mainWindow_width/3-1))
ma.text(label = "")
brsUI.bUEF = ma.checkBox(brsUI.bUEF, label='Enable', cc=enableEndFrame, en=False)
ma.setParent( '..' )

ma.separator(h=5)
ma.separator()
ma.separator()

#Batch Divide Count Field
ma.text(label = "Batch Divide Count: ", al = "right")
brsUI.batchDivide = ma.textField(brsUI.batchDivide, en=False, cc=setBatchDivideCount)

#BatchDivideID Drop Down
ma.rowLayout( numberOfColumns=3 , columnWidth3=(1, (brsUI.mainWindow_width/3)-13, 12))
ma.text(label = "")
brsUI.batchDivideID = ma.optionMenu(brsUI.batchDivideID, label="Batch Divide ID",en=False, cc=setBatchDivideID)
ma.text(label = "")
ma.setParent( '..' )
ma.setParent( '..' )

ma.setParent( '..' )

#####HERE!

####Tab2
brsUI.child2 = ma.rowColumnLayout("SingleColumnTab2", numberOfColumns = 1, columnWidth = (1,brsUI.mainWindow_width - 8))

#Render Cams Header
ma.rowColumnLayout(numberOfColumns = 2, columnWidth = ((1,brsUI.mainWindow_width/3),(2,brsUI.mainWindow_width/3*2 -8)))
ma.text(label = "Renderable Camera Sets", bgc=(0.2,0.2,0.2), al="left")
ma.separator()
ma.setParent( '..' )

#Information
ma.text(label = "Data order : (Camera Name, Start Frame, End Frame)", al="left" )

#Layout
ma.rowColumnLayout(numberOfColumns = 2, columnWidth = ((1,brsUI.mainWindow_width/2),(2,brsUI.mainWindow_width/2)))

#Render Cams Scroll list
brsUI.renderCamsList = ma.textScrollList(brsUI.renderCamsList, numberOfRows=8, en=False, sc="refreshCamEditProperties()")

#Side Buttons
ma.rowColumnLayout(numberOfColumns = 1, columnWidth = (1,brsUI.mainWindow_width/2))
ma.separator()
ma.button(label = "Delete Selected Cam", c="deleteSelectedCam()")
ma.separator()
ma.button(label = "Add New Cam", c="addNewCam()")
ma.separator()
ma.text(label = "~~~~~~~~Edit Selected~~~~~~~~", bgc=(0.2,0.2,0.2))
ma.separator()

#Side TextFields
ma.rowColumnLayout(numberOfColumns = 2, columnWidth = ((1,brsUI.mainWindow_width/6),(2,brsUI.mainWindow_width/4*2)))
ma.text(label = "Camera Name: ", al="right")
brsUI.camNameField = ma.textField(brsUI.camNameField, en=False, cc=setCamName)
ma.text(label = "Start Frame: ", al="right")
brsUI.startFrameField = ma.textField(brsUI.startFrameField, en=False, cc=setCamStartFrame)
ma.text(label = "End Frame: ", al="right")
brsUI.endFrameField = ma.textField(brsUI.endFrameField, en=False, cc=setCamEndFrame)
ma.setParent( '..' )
ma.separator()
ma.setParent( '..' )

#Move item buttons
ma.rowColumnLayout(numberOfColumns = 2, columnWidth = ((1,brsUI.mainWindow_width/4),(2,brsUI.mainWindow_width/4)))
ma.button(label = "/\ /\\", c="shiftSelectedCamUpwards()")
ma.button(label = "\/ \/", c="shiftSelectedCamDownwards()")
ma.setParent( '..' )

ma.rowColumnLayout(numberOfColumns = 2)
ma.text(label = "")
brsUI.editCamTickBox = ma.checkBox(brsUI.editCamTickBox, label="Enable Data Editing", cc="refreshCamEditProperties()", v=False)
ma.setParent( '..' )

ma.setParent( '..' )
ma.setParent( '..' )
 
ma.tabLayout( brsUI.tabs, edit=True, tabLabel=((brsUI.child1, 'Render Setup'), (brsUI.child2, 'Data Set')))
ma.setParent( '..' )
#Tab end

#Frames to render Header
ma.rowColumnLayout(numberOfColumns = 2, columnWidth = ((1,brsUI.mainWindow_width/3),(2,brsUI.mainWindow_width/3*2 -8)))
ma.text(label = "Frame Set for this System", bgc=(0.2,0.2,0.2), al="left")
ma.separator()
ma.setParent( '..' )

brsUI.framesToRender = ma.textScrollList(brsUI.framesToRender, numberOfRows=8, en=False, sc=refreshSelectedFrameInfo)

#Frame Set Information Header
ma.rowColumnLayout(numberOfColumns = 2, columnWidth = ((1,brsUI.mainWindow_width/3),(2,brsUI.mainWindow_width/3*2 -8)))
ma.text(label = "Selected Frame Information", bgc=(0.2,0.2,0.2), al="left" )
ma.separator()
ma.setParent( '..' )

ma.rowColumnLayout(numberOfColumns = 2)
ma.text(label = "Associated Camera: ", al="left" )
brsUI.associatedCamera = ma.text(brsUI.associatedCamera, label = "", al="left" )
ma.setParent( '..' )
ma.separator(h=15)
ma.button( label="Begin Instance Render", h=50, c="initiateInstanceRender()")
ma.separator(h=15)

ma.window( brsUI.mainWindow, edit=True, widthHeight=(brsUI.mainWindow_width, brsUI.mainWindow_height) )

ma.showWindow(brsUI.mainWindow)