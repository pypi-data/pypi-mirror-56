from string import Template

templateString = (
"""#!/usr/bin/env python 

from setuptools import setup, find_packages

setup( 
  # url = 'https://www.python.org/sigs/distutils-sig/',
  name = '${moduleName}',
  author = '${authorName}',
  version = '1.0',
  packages = find_packages(),
  description = '${moduleDescription}',
  author_email = '${authorMail}',
) 
""")

class SetupDotPy:
  def __init__(self):
    self.tmpl = Template(templateString)
  
  def compile(self, data:dict):
    assert type(data) == dict
    return self.tmpl.substitute(**data)