from string import Template

templateString = (
"""class Constants:
  HR = '--------------------------------------------'
  PORT = 'port'
  HOST = 'host'
  SERVER = 'server'
  BLUEPRINTS_FOLDER = 'blueprintsFolder'

  # HTTP Methods
  PUT = 'PUT'
  GET = 'GET'
  POST = 'POST'
  PATCH = 'PATCH'
  DELETE = 'DELETE'
""")

class RestServerConstantsDotPy:
  def __init__(self):
    self.tmpl = Template(templateString)
  
  def compile(self, data = {}):
    assert type(data) == dict
    return self.tmpl.substitute(**data)

