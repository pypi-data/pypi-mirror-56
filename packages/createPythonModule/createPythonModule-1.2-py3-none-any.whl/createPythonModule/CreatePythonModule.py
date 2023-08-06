import os
import shutil
import sys
from os import path
from os import mkdir
from venv import EnvBuilder

print("This is the name of the script: ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("The arguments are: " , str(sys.argv))

from createPythonModule.CpmConst import CpmConst as C
from createPythonModule.templateData.SetupDotPy import SetupDotPy
from createPythonModule.templateData.DotGitIgnore import DotGitIgnore
from createPythonModule.templateData.TestCaseDotPy import TestCaseDotPy
from createPythonModule.templateData.TestSuiteDotPy import TestSuiteDotPy

class CreatePythonModule:
  def createModuleStruct(self):
    print(C.ASCIILOGO)
    print(C.MODDESCRIPTION)

    data = self.__gatherData()
    self.__deleteIfPresent(data)
    self.__makeBaseDir(data)
    self.__makeSetupFile(data)
    self.__makeReadMeFile(data)
    self.__makeModuleFiles(data)
    self.__makeGitIgnoreFile(data)

    print(C.SUCCESSCREATION)

  # Private Methods: ----------------------------------------------------------

  @staticmethod
  def __deleteIfPresent(data:dict):
    if path.exists(data['moduleBaseDirFullPath']): 
      shutil.rmtree(data['moduleBaseDirFullPath'])
  
  def __gatherData(self) -> dict:
    data = {
      'moduleSubFoldTargetPath': os.getcwd(),
      'moduleBaseDirFullPath':'',
      'moduleTestFoldPath':'',
      'moduleSubFoldPath':'',
      'moduleDescription':'',
      'moduleName': (
        self.__cleanModuleName( sys.argv[1] ) if len(sys.argv) > 1 else ''
      ),
      'authorName':'',
      'authorMail':'',
      'docsDir':'',
    }

    if (len(sys.argv) == 1):
      data['moduleName'] = self.__cleanModuleName(self.__inpt(C.INSMODNAME))
      data['moduleSubFoldTargetPath'] = (self.__inpt(C.INSMODPATH) or os.getcwd())
      data['moduleDescription'] = self.__inpt(C.INSMODDESC)
      data['authorName'] = self.__inpt(C.INSAUTHOR)
      data['authorMail'] = self.__inpt(C.INSAUTHORMAIL)
    
    data['moduleBaseDirFullPath'] = path.join(
      data['moduleSubFoldTargetPath'], self.__decapitalize(data['moduleName'])
    )
    data['moduleSubFoldPath'] = path.join(
      data['moduleBaseDirFullPath'], self.__decapitalize(data['moduleName'])
    )
    data['moduleTestFoldPath'] = path.join(
      data['moduleSubFoldPath'], C.TESTS
    )
    data['docsDir'] = path.join(
      data['moduleBaseDirFullPath'], C.DOCS
    )

    return data

  @staticmethod
  def __cleanModuleName(name:str) -> str:
    name = name.replace(" ", "")
    return name[0].upper() + name[1:]

  @staticmethod
  def __decapitalize(word:str) -> str:
    return word[0].lower() + word[1:]

  @staticmethod
  def __inpt(descr:str) -> str:
    return str( input(descr) ).strip()

  @staticmethod
  def __makeBaseDir(data:dict):
    mkdir(data['moduleBaseDirFullPath'])
    mkdir(data['moduleSubFoldPath'])
    mkdir(data['docsDir'])

  def __makeSetupFile(self, data:dict):
    self.__createFileIn(
      path.join(data['moduleBaseDirFullPath'], C.SETUPDOTPY),
      self.__getSetupFile(data)
    )

  def __makeReadMeFile(self, data:dict):
    self.__createFileIn(
      path.join(data['moduleBaseDirFullPath'], C.READMEDOTMD)
    )

  def __makeGitIgnoreFile(self, data:dict):
    self.__createFileIn(
      path.join(data['moduleBaseDirFullPath'], C.DOTGITIGNORE),
      self.__getDotIgnoreFile(data)
    )

  def __makeModuleFiles(self, data:dict):
    modulePath = data['moduleSubFoldPath']
    self.__createFileIn( path.join(modulePath, C.__INITFILE__) )
    self.__createFileIn( path.join(modulePath, f"{data['moduleName']}.py") )
    self.__createFileIn( path.join(modulePath, "requirements.txt") )
    self.__makeTestFolder(data)
    self.__buildVenv(data)

  @staticmethod
  def __buildVenv(data:dict):
    EnvBuilder(with_pip=True).create(
      path.join(data['moduleSubFoldPath'], f"venv-{data['moduleName']}"),
    )

  def __makeTestFolder(self, data:dict):
    testPath = data['moduleTestFoldPath']
    mkdir(testPath)

    self.__createFileIn(
      path.join(testPath, C.TESTSUITE),
      self.__getTestSuiteFile(data)
    )

    self.__createFileIn( path.join(testPath, C.__INITFILE__) )

    testCasesPath = path.join(testPath, C.TESTCASES)
    mkdir(testCasesPath)

    testCase1Path = path.join(testCasesPath, "test{moduleName}".format(**data))
    mkdir(testCase1Path)

    self.__createFileIn(
      path.join(testCase1Path, "Test{moduleName}.py".format(**data)),
      self.__getTestCaseFile(data)
    )

  @staticmethod
  def __getSetupFile(data:dict) -> str:
    return SetupDotPy().compile(data)

  @staticmethod
  def __getDotIgnoreFile(data: dict) -> str:
    return DotGitIgnore().compile()

  @staticmethod
  def __createFileIn(path:object, data = '') -> str:
    testCaseFile = open(path, "w")
    testCaseFile.write(data)
    testCaseFile.close()    

  @staticmethod
  def __getTestSuiteFile(data:dict) -> str:
    return TestSuiteDotPy().compile(data)

  @staticmethod
  def __getTestCaseFile(data:dict) -> str:
    return TestCaseDotPy().compile(data)

def entryPoint(): CreatePythonModule().createModuleStruct()
if __name__ == "__main__": entryPoint()
