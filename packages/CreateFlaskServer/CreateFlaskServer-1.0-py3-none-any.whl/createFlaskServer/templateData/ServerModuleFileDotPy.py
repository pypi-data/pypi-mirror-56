from string import Template

templateString = (
"""from waitress import serve
from os.path import dirname, join, abspath
import pkgutil
import json

from flask import Flask
from flask_cors import CORS

from Constants import Constants as C

# Loading delle configurazioni:
CONF_PATH = abspath(join(dirname(__file__), './conf.json'))
with open(CONF_PATH) as confFile: 
  GLOBAL_CONF = json.loads(confFile.read())

#Loading cartella Blueprints
BLUEPRINTS_FOLDER_PATH = GLOBAL_CONF[C.BLUEPRINTS_FOLDER]
MODULES_PATH = abspath( join( dirname(__file__), f'{BLUEPRINTS_FOLDER_PATH}' ) ) 

class RestServer:

  def __init__(self, serverConf = GLOBAL_CONF):
    self.conf = serverConf[C.SERVER]
    print("Global server configuration are: ", self.conf)

    self.app = Flask(__name__)
    self.__setUpApp()
    self.__loadAndSetUpBP() 
    print("Starting server: ")
    serve(self.app, host=self.conf[C.HOST], port=self.conf[C.PORT])

  # Sistema di caricamento e inizializzazione delle Blueprints
  def __loadAndSetUpBP(self):
    blueprintsList = []
    for (_, bpName, _) in pkgutil.iter_modules([MODULES_PATH]):
      className = bpName
      module = __import__(f'{BLUEPRINTS_FOLDER_PATH}.{bpName}', fromlist=[className])
      blueprintsList.append(getattr(module, className))
    
    print(C.HR)
    for bp in blueprintsList: 
      print("Registering:", bp.name)
      self.app.register_blueprint(bp)
    print(C.HR)

  # Decoratori da applicare alla app.
  def __setUpApp(self):
    CORS(self.app)

if __name__ == '__main__': RestServer()""")

class ServerModuleFileDotPy:
  def __init__(self):
    self.tmpl = Template(templateString)
  
  def compile(self, data = {}):
    assert type(data) == dict
    return self.tmpl.substitute(**data)