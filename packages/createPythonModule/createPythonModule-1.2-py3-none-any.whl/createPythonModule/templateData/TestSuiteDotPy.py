from string import Template

templateString="""
# Informazioni per l'avvio del seguente file:
# cd ${moduleName}
# source venv-${moduleName}/bin/activate
# python3 -m unittest tests.TestSuite
# ( pip install coverage )
# coverage run -m unittest tests.TestSuite

import unittest

# carico le singole classi di test:
from .testCases.test${moduleName}.Test${moduleName} import Test${moduleName}

# metto le classi di test in un iterabile:
testClasses = [ Test${moduleName} ]

# Instanzio il loader delle classi:
loader = unittest.TestLoader()

# Genero una lista di classi caricate dal loader di test:
suites = [loader.loadTestsFromTestCase(testClass) for testClass in testClasses]

# Eseguo tutti i test
unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(suites))
"""

class TestSuiteDotPy:
  def __init__(self):
    self.tmpl = Template(templateString)
  
  def compile(self, data:dict): 
    assert type(data) == dict
    return self.tmpl.substitute(**data)
    