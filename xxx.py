import unittest
from ctypes import POINTER
import comtypes
from comtypes.client import CreateObject, GetModule
from comtypes.gen._1EA4DBF0_3C3B_11CF_810C_00AA00389B71_0_1_1 import IAccessible

GetModule('oleacc.dll')

class TestCase(unittest.TestCase):

    def setUp(self):
        self.ie = CreateObject('InternetExplorer.application')

    def tearDown(self):
        self.ie.Quit()
        del self.ie

    def test(self):
        ie = self.ie
        ie.navigate2("about:blank", 0)
        sp = ie.Document.Body.QueryInterface(comtypes.IServiceProvider)
        pacc = sp.QueryService(comtypes.gen.Accessibility.IAccessible._iid_, comtypes.gen.Accessibility.IAccessible)
        self.assertEqual(type(pacc), POINTER(IAccessible))

if __name__ == "__main__":
    unittest.main()