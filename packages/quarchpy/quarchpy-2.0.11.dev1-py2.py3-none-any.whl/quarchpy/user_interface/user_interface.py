# Needed for python2 compatibility
# coding: utf-8
from __future__ import print_function

import sys
import os
from quarchpy.utilities import TestCenter

# This is a singleton class, it will only ever refer to the same object
class User_interface:

    instance = None

    class __user_interface:
        def __init__(self,ui):
            if ui in ["console","testcenter"]:
                self.selectedInterface = ui
            else:
                raise ValueError("requested ui type not valid")

    def __init__(self,ui):
        # if we haven't create a user_interface object before
        if not User_interface.instance:
            # create a user interface object with our selected interface type
            User_interface.instance = User_interface.__user_interface(ui)
        # otherwise change the existing user interface object to the new type
        else:
            User_interface.instance.selectedInterface = ui

'''
def listSelection(title,message,selectionList)

    prompts the user to return a selection from the list
    list format is a comma delimited string (key1=value1,key2=value2...)
    the function will return the selected key
    
    THIS IS MORE LIKE A DICTIONARY SELECTION FUNC THAT RETURNS THE VALUE
'''
def listSelection(title="",message="",selectionList="", nice = False):
    if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":

        return TestCenter.testPoint("Quarch_Host.ShowGenericDialog", "Title=" + __formatForTestcenter(title),
                                "Message=" + __formatForTestcenter(message),
                                "ItemListString=" + __formatForTestcenter(selectionList));

    else: #default mode console output

        #print message
        print(message)
        print("")

        if nice is True:
            return niceListSelection(selectionList)

        #split selection list into key=value pairs and print each value
        # first split on ','s into list of key=value pairs
        selectionList = selectionList.split(',')
        # then split each list item on '=' into a [key,value] list
        selectionList = [str(x).split("=") for x in selectionList]
        count=1
        for item in selectionList:
            # if list item has index and value print them
            if len(item)>1:
                print(str(count) + " - " + item[1])
            else:
                print(item[0])
            count += 1

        print("")
        # Request user selection
        while (True):
            if sys.version_info.major >= 3:
                userStr = input("please select an option:\n>")
            else:
                userStr = raw_input("please select an option:\n>")

            # Validate the response
            try:
                userNumber = int(userStr)
                if (userNumber <= len(selectionList) and userNumber >= 1):
                    break
            except:
                print ("INVALID SELECTION!")

        # return the key associated with this entry
        return selectionList[userNumber-1][0]

'''
niceListSelection
THIS IS MORE LIKE A TRUE LIST SELECTION FUNCTION RATHER THAN A DICT SELECTION IT RETURNS A LIST OBJ
'''
def niceListSelection(selectionList, tableHeaders=None, indexReq=True):
    # take in a 2d list and display it with an index column for selection
    # get user input of selection
    # return 2d[selection]

    displayTable(selectionList, indexReq=indexReq, tableHeaders=tableHeaders)
    print("")
    # Request user selection
    while (True):
        if sys.version_info.major >= 3:
            userStr = input("please select an option:\n>")
        else:
            userStr = raw_input("please select an option:\n>")

        # Validate the response
        try:
            userNumber = int(userStr)
            if (userNumber <= len(selectionList) and userNumber >= 1):
                break
        except:
            print("INVALID SELECTION!")

    # return the key associated with this entry
    return selectionList[userNumber - 1]


'''
printText(text)

    prints out the specified text via the currently selected user interface

    arguments:
        text - a string of text, or a list of strings
        fillLine - If true print will cover the width of the screen (useful when using "\r" to write on the same line)
        terminalWidth - Width of terminal writing to
        fill - The character that will be used to fill the remaining space 
    

'''
def printText(text, fillLine=False, terminalWidth=100, fill=" ",**kwargs):

        if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":
            # if line is not empty
            if text.strip()!="":
                TestCenter.testPoint ("Quarch_Host.LogComment","Message=" + __formatForTestcenter(text))

        else:
            if fillLine:
                text +=fill*(terminalWidth-len(text)) #TODO Split string at \n or \r\n make a list, add the line fill for each item,then add back the \n and \r\n and combine together again.
            if kwargs!= {}:
                print(text,**kwargs)
            else:
                print(text)
        return

'''
showDialog(title,message)

    prints a message to the user and waits for acknowledgement

'''
def showDialog(message="",title=""):


        if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":
            TestCenter.testPoint ("Quarch_Host.ShowDialog","Title=" + __formatForTestcenter(title),"Message=" + __formatForTestcenter(message))

        else:
            print(message)
            if sys.version_info.major >= 3:
                userStr = input("press enter to continue\n>")
            else:
                userStr = raw_input("press enter to continue\n>")



'''
printProgressBar (iteration,total,prefix='',suffix='',decimals=1,length=100,fill='█')

    prints a text based progress bar

        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)

'''
def progressBar (iteration, total,prefix = '', suffix = '', decimals = 1, fill = '█', fullWidth = 100):
    if iteration >=0 and total >0:

        if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":
            TestCenter.testPoint ("Quarch_Host.ShowTaskProgress","Title=Task Progress", "Iteration="+str(iteration), "Total="+str(total));

        else:
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            length = fullWidth - (len(prefix)+len(suffix)+len(percent) +4) #the length of the bar must scale acording to anything else on the line

            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)
            print('%s|%s|%s%%%s' % (prefix, bar, percent, suffix), end = '\r')

            # Print New Line on Complete
            if iteration >= total:
                print()


'''
startTestBlock(text)

    prints out the specified text via the currently selected user interface

    arguments:
        text - a string of text, or a list of strings

'''
def startTestBlock(text):

        if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":
            TestCenter.beginTestBlock(__formatForTestcenter(text))

        else:
            print("")
            print(text)
            print("")


        return

'''
endTestBlock()

    finishes the current test block in testcenter, no action in console

'''
def endTestBlock():

        if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":
            TestCenter.endTestBlock()
        else:
            pass

        return

'''
logCalibrationResult(title,result)
'''
def logCalibrationResult(title,report):

    if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":
        if report["result"]:
            TestCenter.testPoint("Quarch_Host.LogTestPoint", "Test=" + __formatForTestcenter(title), "Result=True",
                                 "Message=" + __formatForTestcenter(
                                     title) + " Passed, worst case: " + __formatForTestcenter(report["worst case"]))
            # add the report as comments
            for line in report["report"].splitlines():
                TestCenter.testPoint("Quarch_Host.LogComment", "Message=" + __formatForTestcenter(line))
            TestCenter.endTestBlock()
        else:

            TestCenter.testPoint("Quarch_Host.LogTestPoint", "Test=" + __formatForTestcenter(title), "Result=False",
                                 "Message=" + __formatForTestcenter(
                                     title) + " Failed, worst case: " + __formatForTestcenter(report["worst case"]))
            # add the report as comments
            for line in report["report"].splitlines():
                TestCenter.testPoint("Quarch_Host.LogComment", "Message=" + __formatForTestcenter(line))
            TestCenter.endTestBlock()
            #TestCenter.testPoint("Quarch_Internal.storeMessage", "Message=" + __formatForTestcenter(title) + " Failed") #old logging meathod

    else:
        if report["result"]:
            print("\n\t" + title + " Passed")
            print("")
            print("\tworst case: " + report["worst case"])
        else:
            print("\n\t" + title + " Failed")
            print("")
            print(report["report"])


'''
logsSimpleCalibrationResult(title,result)
'''
def logSimpleResult(title,result):

    if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":
        if result:
            TestCenter.testPoint("Quarch_Host.LogTestPoint", "Test=" + __formatForTestcenter(title), "Result=True",
                                 "Message=" + __formatForTestcenter(title))
        else:

            TestCenter.testPoint("Quarch_Host.LogTestPoint", "Test=" + __formatForTestcenter(title), "Result=False",
                                 "Message=" + __formatForTestcenter(title))
            #TestCenter.testPoint("Quarch_Internal.storeMessage", "Message=" + __formatForTestcenter(title) + " Failed") #old logging meathod

    else:
        if result:
            print("\n\t" + title + " Passed")
        else:
            print("\n\t" + title + " Failed")

'''
logResults(test,notes)
'''
def logResults(test,notes):

        if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":
            TestCenter.testPoint ("Quarch_Host.ResultDialog","Test="+ __formatForTestcenter(test),"Notes=" + __formatForTestcenter(notes))

        else:
            print(notes)

        return

'''
storeDeviceInfo()
'''
def storeDeviceInfo(**kwargs):

        if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":
            # Store the serial number from the DUT scan for logging and verification
            if 'serial' in kwargs:
                TestCenter.testPoint ("Quarch_Internal.StoreSerial","Serial="+kwargs['serial']);
            if 'idn' in kwargs:
                # replace line endings
                IDNString = '|'.join(kwargs['idn'].splitlines())
                TestCenter.testPoint ("Quarch_Internal.StoreDutActualIdn","Idn="+IDNString)

        # We need to provide testcenter with the information to populate the database
        else:
            pass
'''
requestDialog(title, message)
'''
def requestDialog( title="", message = "", desiredType = None, minRange=None, maxRange=None, defaultUserInput=""):
    validValue = False
    if desiredType != None and desiredType.lower() == "string": #If "string" or None do the same thing. Default is string type.
        desiredType = None
    while validValue == False:
        if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":

            userStr = TestCenter.testPoint("Quarch_Host.ShowRequestDialog","Title= " + __formatForTestcenter(title), "Message=" + __formatForTestcenter(message));

        else:  # default mode console output
            print(message)
            print("")
            # Request user selection

            if sys.version_info.major >= 3:
                userStr = input("please input an option:\n>")
            else:
                userStr = raw_input("please input an option:\n>")
        if userStr == "":
            userStr = defaultUserInput
        validValue = validateUserInput(userStr, desiredType, minRange, maxRange)

    return userStr
'''
Takes string checks if can cast to desired type and returns it as that type, can check if within range for ints and floats.
'''
def validateUserInput ( userStr, desiredType, minRange, maxRange):
    validValue = False
    if desiredType == None:
        validValue = True
    if desiredType == "float":
        try:
            userStr = float(userStr)
            if ((minRange != None and maxRange != None) and (userStr < minRange or userStr > maxRange)):
                validValue = False
            else:
                validValue = True
        except:
            pass

    elif desiredType == "int":
        try:
            userStr = int(userStr)
            if ((minRange != None and maxRange != None) and (userStr< minRange or userStr > maxRange)):
                validValue = False
            else:
                validValue = True
        except:
            pass
    elif desiredType == "path":
        if (os.path.isdir(userStr) == False):
            validValue = False
        else:
            validValue = True
    if validValue == False:
            printText ( str(userStr)+ " is not a valid " + str(desiredType))
            if minRange != None and maxRange != None:
                printText("Please enter a " + str(desiredType) + " between " + str(minRange) + " and " + str(maxRange))
            else:
                printText("Please enter a valid " + str(desiredType))
    return validValue

'''
Takes a string input of comma seperated ints or range of ints and converts it to an array of strings with padding if requested eg:
 2-5, 9,11,31-35  ->  002,003,004,005,009,011,031,032,033,034,035
intLength tells the function to zeo pad the int before returning it.
'''
def userRangeIntSelection(inputString, intLength=3 ):
    inputList = inputString.split(",")
    returnList=[]
    for item in inputList:
        if "-" in item:
            myRange = item.split("-")
            myRange = range(int(myRange[0]),int(myRange[1])+1)
            returnList.extend(myRange)
        else:
            if vaidateUserInput(item,"int",0,999):
                returnList.append(item)

    for i, item in enumerate(returnList):
        returnList[i] = str(item)
        if intLength != None:
            returnList[i] = returnList[i].zfill(intLength)
    return returnList

'''nice table'''


def displayTable(tableData=[[""]], title="", message="", tableHeaders=None, indexReq=False):
    '''
      function will take the following types in tableData
      listoflist
      listoftuple
      tupleoftuple
      tupleoflist

      with processing
      list
      tuple


      check:
      dict
      '''

    if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":
        printText("displayTable only available in console mode")

    else:
    # default mode console output

        if isinstance(tableData, dict):
            tempList = []
            tempEl = []
            for k, v in tableData.items():
                tempEl = []

                tempEl.append(v)
                charPos = k.find(":")
                tempEl.append(k)
                tempList.append(tempEl)
            tableData = tempList

        #Process list to make it into 2d list to display.
        try:
            if not isinstance(tableData[0], tuple) and not isinstance(tableData[0], list) and not isinstance(tableData[0], dict):
                tempList=list()
                for item in tableData:
                    tempList.append(list([item]))
                tableData = tempList
        except:
            pass
        # print message
        print(message)
        print("")

        if indexReq:
            if tableHeaders is not None:
                tableHeaders.insert(0,"i")
            counter =1
            for rows in tableData:
                rows.insert(0,counter)
                counter+=1

        '''calculate required column width for each column'''
        columnWidths = []
        itemLegnth = 0
        for rowData in tableData:
            index = 0
            for item in rowData:
                itemLegnth = len(str(item))
                try:
                    if columnWidths[index] < itemLegnth:
                        columnWidths[index] = itemLegnth
                except:  # if null pointer
                    columnWidths.append(itemLegnth)
                index += 1
        if tableHeaders is not None:
            index = 0
            for item in tableHeaders:
                itemLegnth = len(str(item))
                try:
                    if columnWidths[index] < itemLegnth:
                        columnWidths[index] = itemLegnth
                except:  # if null pointer
                    columnWidths.append(itemLegnth)
                index += 1

        #Calculate the edge to be displayed at the top and bottom
        edge = ""
        for columnWidth in columnWidths:
            edge += "+" + "-" * (columnWidth + 2)
        edge += "+"

        if tableHeaders is not None:
            rowString = "|"
            index = 0
            print(edge)
            for item in tableHeaders:
                rowString += str(item) + " " * (columnWidths[index] - len(str(item)) + 2) + "|"
                index += 1
            print(rowString)

        print(edge)
        for rowData in tableData:
            index = 0
            rowString = "|"
            for item in rowData:
                rowString += str(item) + " " * (columnWidths[index] - len(str(item)) + 2) + "|"
                index += 1
            print(rowString)
        print(edge)
'''
'''
def __formatForTestcenter(text):
    # escape special characters
    # turn \' to \\'s
    text = text.replace('\\','\\\\')
    #get rid of any alarms that may be included in console mode
    text = text.replace('\a', '')
    # replace line endings
    text = '|'.join(text.splitlines())
    return text
    
