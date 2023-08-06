from string import Template

templateString="""import os, sys
from flask import Blueprint
from flask import request
from Constants import Constants as C

BLUEPRINTNAME = os.path.splitext(os.path.basename(__file__))[0]

PUT = C.PUT
GET = C.GET
POST = C.POST
PATCH = C.PATCH
DELETE = C.DELETE

# TODO: EditHere
URL_PREFIX = '/provaEndpoint'

blueprint = Blueprint(BLUEPRINTNAME, BLUEPRINTNAME, url_prefix = URL_PREFIX)

@blueprint.route('/', methods=[POST])
def post():
  payload = request.json
  # TODO: EditHere
  return None

@blueprint.route('/', methods=[GET])
def get():
  # TODO: EditHere
  return None

@blueprint.route('/', methods=[PUT])
def put():
  payload = request.json
  # TODO: EditHere
  return None

@blueprint.route('/', methods=[DELETE])
def delete():
  # TODO: EditHere
  return None

#------------------------------------------
# TODO: Edit Here

@blueprint.route('/<id>', methods=[GET])
def getById(id:str):
  return None

#------------------------------------------

thismodule = sys.modules[__name__]
setattr(thismodule, BLUEPRINTNAME, blueprint)
"""

class BluePrintFileDotPy:
  def __init__(self):
    self.tmpl = Template(templateString)
  
  def compile(self, data = {}): 
    assert type(data) == dict
    return self.tmpl.substitute(**data)


