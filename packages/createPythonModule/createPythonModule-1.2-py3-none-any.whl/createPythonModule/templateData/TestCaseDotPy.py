from string import Template

templateString="""
# Informazioni per l'avvio del seguente file:
# cd ${moduleName}
# source venv-${moduleName}/bin/activate
# python3 -m unittest tests.testCases.test${moduleName}.Test${moduleName}
# ( pip install coverage )
# coverage run -m unittest tests.testCases.test${moduleName}.Test${moduleName}

import unittest

class Test${moduleName}(unittest.TestCase):
  def test_1(self):
    self.assertTrue(True)

  @unittest.skip('Motivo dello skip qui')
  def suggest(self):
    self.assertEqual(a, b)
    self.assertNotEqual(a, b)
    self.assertTrue(x)
    self.assertFalse(x)
    self.assertIs(a, b)
    self.assertIsNot(a, b)
    self.assertIsNone(x)
    self.assertIsNotNone(x)
    self.assertIn(a, b)
    self.assertNotIn(a, b)
    self.assertIsInstance(a, b)
    self.assertNotIsInstance(a, b)
    self.assertRaises(exc, fun, args, *kwds)
    self.assertRaisesRegexp(exc, r, fun, args, *kwds)
    self.assertAlmostEqual(a, b)
    self.assertNotAlmostEqual(a, b)
    self.assertGreater(a, b)
    self.assertGreaterEqual(a, b)
    self.assertLess(a, b)
    self.assertLessEqual(a, b)
    self.assertRegexpMatches(s, r)
    self.assertNotRegexpMatches(a, b)
    self.assertItemsEqual(a, b)
    self.assertDictContainsSubset(a, b)

  # Private e utils Methods: --------------------------------------------------

  def setUp(self):
    pass

  def tearDown(self):
    pass

if __name__ == '__main__': unittest.main()
"""

class TestCaseDotPy:
  def __init__(self):
    self.tmpl = Template(templateString)
  
  def compile(self, data:dict): 
    assert type(data) == dict
    return self.tmpl.substitute(**data)
