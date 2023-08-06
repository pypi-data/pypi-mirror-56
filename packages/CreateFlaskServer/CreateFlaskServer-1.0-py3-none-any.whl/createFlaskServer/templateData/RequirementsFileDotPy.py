from string import Template

templateString = (
"""Click==7.0
Flask==1.1.1
Flask-Cors==3.0.8
itsdangerous==1.1.0
Jinja2==2.10.1
MarkupSafe==1.1.1
six==1.12.0
Werkzeug==0.15.4
waitress==1.3.1
""")

class RequirementsFileDotPy:
  def __init__(self):
    self.tmpl = Template(templateString)
  
  def compile(self, data = {}):
    assert type(data) == dict
    return self.tmpl.substitute(**data)




