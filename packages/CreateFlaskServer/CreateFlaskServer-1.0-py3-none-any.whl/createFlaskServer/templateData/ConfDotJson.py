from string import Template

templateString = (
"""{
  "blueprintsFolder":"blueprints",
  "server": {
    "port": "2001",
    "host": "0.0.0.0"
  }
}""")

class ConfDotJson:
  def __init__(self):
    self.tmpl = Template(templateString)
  
  def compile(self, data = {}):
    assert type(data) == dict
    return self.tmpl.substitute(**data)



