import os 
import json 

dataFiles = "./public/data"

def processNames(dataFiles):
    dataFileNames = {}
    for fileName in os.listdir(dataFiles):
        if fileName.endswith(".csv"):
            filePath = os.path.join(dataFiles, fileName)
            dataFileNames[fileName] = filePath
    return dataFileNames

def savetoJSON(dataFileNames, outputPath='filePaths.json'):
    with open(outputPath, 'w') as jsonFile:
        json.dump(dataFileNames, jsonFile, indent=4)
        print(f"file saved to {jsonFile}")

result = processNames(dataFiles)
outputPath = "filePaths.json"

savetoJSON(result, outputPath)