import os
import shutil
import sys
from os import path
from os import mkdir
from venv import EnvBuilder

from createFlaskServer.CfsConst import CfsConst as C
from createFlaskServer.templateData.SetupDotPy import SetupDotPy
from createFlaskServer.templateData.BluePrintFileDotPy import BluePrintFileDotPy
from createFlaskServer.templateData.RestServerConstantsDotPy import RestServerConstantsDotPy
from createFlaskServer.templateData.ConfDotJson import ConfDotJson
from createFlaskServer.templateData.ServerModuleFileDotPy import ServerModuleFileDotPy
from createFlaskServer.templateData.RequirementsFileDotPy import RequirementsFileDotPy

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

  def __makeModuleFiles(self, data:dict):
    modulePath = data['moduleSubFoldPath']
    
    # Crea file init:
    self.__createFileIn( path.join(modulePath, C.__INITFILE__) )
    
    # Crea il file "nomeModulo.py"
    self.__createFileIn( 
      path.join(modulePath, f"{data['moduleName']}.py"),
      self.__getServerModuleFile()
    )
    
    # Crea il requirements
    self.__createFileIn( 
      path.join(modulePath, "requirements.txt"), 
      self.__getRequirementsFile()
    )
    
    #Create server Blueprints e relativa cartella
    mkdir(path.join(data['moduleSubFoldPath'], C.BLUEPRINTS_FOLDER))
    self.__createFileIn( 
      path.join( path.join(modulePath, C.BLUEPRINTS_FOLDER),'Blueprint1.py' ),
      self.__getBluePrintFile()
    )
    
    #Create server Constants
    self.__createFileIn(
      path.join(modulePath, "Constants.py"), self.__getConstFile()
    )
    #Create server Conf
    self.__createFileIn(
      path.join(modulePath, "conf.json"), self.__getConfFile()
    )

    self.__buildVenv(data)
    # TODO: Install Requirements.

  @staticmethod
  def __buildVenv(data:dict):
    EnvBuilder(with_pip=True).create(
      path.join(data['moduleSubFoldPath'], f"venv-{data['moduleName']}"),
    )

  @staticmethod
  def __getServerModuleFile() -> str: return ServerModuleFileDotPy().compile()

  @staticmethod
  def __getRequirementsFile() -> str: return RequirementsFileDotPy().compile()

  @staticmethod
  def __getBluePrintFile() -> str: return BluePrintFileDotPy().compile()

  @staticmethod
  def __getConstFile() -> str: return RestServerConstantsDotPy().compile()

  @staticmethod
  def __getConfFile() -> str: return ConfDotJson().compile()

  @staticmethod
  def __getSetupFile(data:dict) -> str: return SetupDotPy().compile(data)

  @staticmethod
  def __createFileIn(path:object, data = '') -> str:
    testCaseFile = open(path, "w")
    testCaseFile.write(data)
    testCaseFile.close()    


def entryPoint(): CreatePythonModule().createModuleStruct()
if __name__ == "__main__": entryPoint()
